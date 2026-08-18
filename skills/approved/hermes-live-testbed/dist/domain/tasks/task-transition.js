import { MAX_TASK_EVENTS, TaskEventSchema, TaskRecordSchema, TaskRunIdSchema, TaskStatusSchema, parseTaskRecord, parseTaskTimestamp, sanitizeTaskError, sanitizeTaskEventSummary, sanitizeTaskOutput, sanitizeTaskUsage, } from "./task.js";
const TERMINAL_TASK_STATUSES = new Set(["completed", "failed", "cancelled"]);
const ALLOWED_TASK_TRANSITIONS = {
    queued: new Set(["dispatching", "cancelled"]),
    dispatching: new Set(["queued", "running", "failed", "cancelled", "dispatch_unknown"]),
    running: new Set(["waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown"]),
    waiting_for_approval: new Set(["running", "stopping", "failed", "cancelled", "unknown"]),
    stopping: new Set(["completed", "failed", "cancelled", "unknown"]),
    completed: new Set(),
    failed: new Set(),
    cancelled: new Set(),
    unknown: new Set(["running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled"]),
    dispatch_unknown: new Set(["running", "stopping", "completed", "failed", "cancelled", "unknown"]),
};
export class TaskTransitionError extends Error {
    constructor(from, to) {
        super(`Task cannot transition from ${from} to ${to}.`);
        this.name = "TaskTransitionError";
    }
}
export function isTaskTerminal(status) {
    return TERMINAL_TASK_STATUSES.has(status);
}
export function canTransitionTask(from, to) {
    return from === to || ALLOWED_TASK_TRANSITIONS[from].has(to);
}
export function transitionTask(value, nextStatus, options = {}) {
    const record = parseTaskRecord(value);
    const target = TaskStatusSchema.parse(nextStatus);
    const recordingMissingRun = record.status === target
        && target === "unknown"
        && options.upstreamRunMissing === true
        && record.upstreamRunMissingAt === undefined;
    if (record.status === target && !recordingMissingRun)
        return record;
    if (!recordingMissingRun && !ALLOWED_TASK_TRANSITIONS[record.status].has(target)) {
        throw new TaskTransitionError(record.status, target);
    }
    if (options.output !== undefined && target !== "completed") {
        throw new Error("Task output can be assigned only when a task completes.");
    }
    if (options.outputTruncated !== undefined && target !== "completed") {
        throw new Error("Task output truncation can be assigned only when a task completes.");
    }
    if (options.outputTruncated === true && options.output === undefined && record.output === undefined) {
        throw new Error("Truncated task output requires a retained output prefix.");
    }
    if (options.upstreamRunMissing === true && target !== "unknown") {
        throw new Error("A confirmed missing upstream run can be recorded only on an unknown task.");
    }
    const now = monotonicTaskTimestamp(record, options.now);
    const runId = resolveRunId(record.runId, options.runId);
    const event = createNextEvent(record, target, options.summary ?? defaultTransitionSummary(target), now);
    const usage = sanitizeTaskUsage(options.usage);
    const notificationRequired = [
        "completed",
        "failed",
        "cancelled",
        "unknown",
        "dispatch_unknown",
    ].includes(target);
    // A recovered unknown outcome is no longer the current inbox fact once the
    // task re-enters running/stopping work. Clear the durable notice on every
    // non-notifiable transition; the gateway projects an explicit withdrawal to
    // already-connected clients.
    const clearNotification = !notificationRequired;
    const next = {
        ...record,
        status: target,
        updatedAt: now,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
        ...(runId ? { runId } : {}),
        ...(options.output === undefined ? {} : { output: sanitizeTaskOutput(options.output) }),
        ...(options.outputTruncated === undefined ? {} : { outputTruncated: options.outputTruncated }),
        ...(usage ? { usage } : {}),
        ...(options.error === undefined ? {} : { error: sanitizeTaskError(options.error) }),
        ...(options.upstreamRunMissing === true ? { upstreamRunMissingAt: now } : {}),
        notification: notificationRequired
            ? { unread: true }
            : clearNotification
                ? { unread: false }
                : record.notification,
    };
    if (target !== "unknown")
        delete next.upstreamRunMissingAt;
    if (target === "completed")
        delete next.error;
    return TaskRecordSchema.parse(next);
}
export function appendTaskEvent(value, input) {
    const record = parseTaskRecord(value);
    const now = monotonicTaskTimestamp(record, input.now);
    const event = createNextEvent(record, input.type ?? "progress", input.summary, now);
    return TaskRecordSchema.parse({
        ...record,
        updatedAt: now,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
    });
}
/**
 * Persist a cancellation intent independently from the upstream stop request.
 * This marker is append-only so a gateway restart or an ambiguous stop response
 * can never make the task look like ordinary running work again.
 */
export function markTaskStopRequested(value, input = {}) {
    const record = parseTaskRecord(value);
    if (record.stopRequestedAt !== undefined)
        return record;
    const now = monotonicTaskTimestamp(record, input.now);
    const event = createNextEvent(record, "stop_requested", input.summary ?? "Exact task stop requested.", now);
    return TaskRecordSchema.parse({
        ...record,
        stopRequestedAt: now,
        updatedAt: now,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
    });
}
export function markTaskNotificationAnnounced(value, now = Date.now()) {
    const record = parseTaskRecord(value);
    if (!record.notification.unread || record.notification.announcedAt !== undefined)
        return record;
    const timestamp = monotonicTaskTimestamp(record, now);
    const event = createNextEvent(record, "notification.announced", "Task notification announced.", timestamp);
    return TaskRecordSchema.parse({
        ...record,
        updatedAt: timestamp,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
        notification: { ...record.notification, announcedAt: timestamp },
    });
}
export function acknowledgeTaskNotification(value, now = Date.now()) {
    const record = parseTaskRecord(value);
    if (!record.notification.unread)
        return record;
    const timestamp = monotonicTaskTimestamp(record, now);
    const event = createNextEvent(record, "notification.acknowledged", "Task notification acknowledged.", timestamp);
    return TaskRecordSchema.parse({
        ...record,
        updatedAt: timestamp,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
        notification: {
            ...record.notification,
            unread: false,
            acknowledgedAt: timestamp,
        },
    });
}
export function containIndeterminateTask(value, now = Date.now()) {
    const record = parseTaskRecord(value);
    if (record.operatorContainedAt !== undefined)
        return record;
    if (record.status !== "unknown" && record.status !== "dispatch_unknown") {
        throw new Error("Only an unknown task can be contained by an operator.");
    }
    const timestamp = monotonicTaskTimestamp(record, now);
    const event = createNextEvent(record, "operator_contained", "Operator confirmed the indeterminate task is contained.", timestamp);
    return TaskRecordSchema.parse({
        ...record,
        operatorContainedAt: timestamp,
        updatedAt: timestamp,
        revision: record.revision + 1,
        sequence: event.sequence,
        events: appendRetainedEvent(record.events, event),
        notification: { unread: true },
    });
}
function createNextEvent(record, type, summary, timestamp) {
    return TaskEventSchema.parse({
        sequence: record.sequence + 1,
        type,
        timestamp,
        summary: sanitizeTaskEventSummary(summary),
    });
}
function appendRetainedEvent(events, event) {
    return [...events, event].slice(-MAX_TASK_EVENTS);
}
function monotonicTaskTimestamp(record, now = Date.now()) {
    return Math.max(record.updatedAt, parseTaskTimestamp(now));
}
function resolveRunId(current, candidate) {
    if (candidate === undefined)
        return current;
    const parsed = TaskRunIdSchema.parse(candidate);
    if (current && current !== parsed)
        throw new Error("A task run ID is immutable after assignment.");
    return parsed;
}
function defaultTransitionSummary(status) {
    return `Task ${status.replaceAll("_", " ")}.`;
}
//# sourceMappingURL=task-transition.js.map