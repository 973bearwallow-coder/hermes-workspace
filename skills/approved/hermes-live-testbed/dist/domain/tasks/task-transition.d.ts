import { type TaskEventType, type TaskRecord, type TaskStatus } from "./task.js";
export interface TaskTransitionOptions {
    now?: number;
    summary?: string;
    runId?: string;
    output?: string;
    outputTruncated?: boolean;
    usage?: unknown;
    error?: string;
    upstreamRunMissing?: boolean;
}
export interface AppendTaskEventInput {
    type?: TaskEventType;
    summary: string;
    now?: number;
}
export interface MarkTaskStopRequestedInput {
    now?: number;
    summary?: string;
}
export declare class TaskTransitionError extends Error {
    constructor(from: TaskStatus, to: TaskStatus);
}
export declare function isTaskTerminal(status: TaskStatus): boolean;
export declare function canTransitionTask(from: TaskStatus, to: TaskStatus): boolean;
export declare function transitionTask(value: TaskRecord, nextStatus: TaskStatus, options?: TaskTransitionOptions): TaskRecord;
export declare function appendTaskEvent(value: TaskRecord, input: AppendTaskEventInput): TaskRecord;
/**
 * Persist a cancellation intent independently from the upstream stop request.
 * This marker is append-only so a gateway restart or an ambiguous stop response
 * can never make the task look like ordinary running work again.
 */
export declare function markTaskStopRequested(value: TaskRecord, input?: MarkTaskStopRequestedInput): TaskRecord;
export declare function markTaskNotificationAnnounced(value: TaskRecord, now?: number): TaskRecord;
export declare function acknowledgeTaskNotification(value: TaskRecord, now?: number): TaskRecord;
export declare function containIndeterminateTask(value: TaskRecord, now?: number): TaskRecord;
//# sourceMappingURL=task-transition.d.ts.map