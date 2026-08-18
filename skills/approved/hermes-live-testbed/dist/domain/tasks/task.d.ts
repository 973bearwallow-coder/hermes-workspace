import { z } from "zod";
export declare const TASK_RECORD_SCHEMA_VERSION: 1;
export declare const MAX_TASK_TITLE_CHARS = 256;
export declare const MAX_TASK_INPUT_CHARS = 100000;
export declare const MAX_TASK_OUTPUT_CHARS = 200000;
export declare const MAX_TASK_ERROR_CHARS = 4000;
export declare const MAX_TASK_EVENT_SUMMARY_CHARS = 2000;
export declare const MAX_TASK_EVENTS = 128;
export declare const MAX_TASK_RESOURCE_KEYS = 16;
export declare const MAX_TASK_RESOURCE_KEY_CHARS = 256;
export declare const MAX_TASK_USAGE_FIELDS = 32;
export declare const TaskIdSchema: z.ZodString;
export declare const TaskOwnerIdSchema: z.ZodString;
export declare const TaskRunIdSchema: z.ZodEffects<z.ZodString, string, string>;
export declare const TaskHermesSessionIdSchema: z.ZodEffects<z.ZodString, string, string>;
export declare const TaskResourceKeySchema: z.ZodEffects<z.ZodString, string, string>;
export declare const TaskStatusSchema: z.ZodEnum<["queued", "dispatching", "running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown", "dispatch_unknown"]>;
export type TaskStatus = z.infer<typeof TaskStatusSchema>;
export declare const TaskExecutionModeSchema: z.ZodEnum<["exclusive", "parallel_read_only"]>;
export type TaskExecutionMode = z.infer<typeof TaskExecutionModeSchema>;
export declare const TaskKindSchema: z.ZodEnum<["background", "follow_up"]>;
export type TaskKind = z.infer<typeof TaskKindSchema>;
export declare const TaskEventTypeSchema: z.ZodEnum<["queued", "dispatching", "running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown", "dispatch_unknown", "progress", "stop_requested", "approval_required", "notification.announced", "notification.acknowledged", "operator_contained"]>;
export type TaskEventType = z.infer<typeof TaskEventTypeSchema>;
export declare const TaskUsageSchema: z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodNumber>, Record<string, number>, Record<string, number>>;
export type TaskUsage = z.infer<typeof TaskUsageSchema>;
export declare const TaskEventSchema: z.ZodObject<{
    sequence: z.ZodNumber;
    type: z.ZodEnum<["queued", "dispatching", "running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown", "dispatch_unknown", "progress", "stop_requested", "approval_required", "notification.announced", "notification.acknowledged", "operator_contained"]>;
    timestamp: z.ZodNumber;
    summary: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
}, "strict", z.ZodTypeAny, {
    sequence: number;
    type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
    timestamp: number;
    summary?: string | undefined;
}, {
    sequence: number;
    type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
    timestamp: number;
    summary?: string | undefined;
}>;
export type TaskEvent = z.infer<typeof TaskEventSchema>;
export declare const TaskNotificationSchema: z.ZodEffects<z.ZodObject<{
    unread: z.ZodBoolean;
    announcedAt: z.ZodOptional<z.ZodNumber>;
    acknowledgedAt: z.ZodOptional<z.ZodNumber>;
}, "strict", z.ZodTypeAny, {
    unread: boolean;
    announcedAt?: number | undefined;
    acknowledgedAt?: number | undefined;
}, {
    unread: boolean;
    announcedAt?: number | undefined;
    acknowledgedAt?: number | undefined;
}>, {
    unread: boolean;
    announcedAt?: number | undefined;
    acknowledgedAt?: number | undefined;
}, {
    unread: boolean;
    announcedAt?: number | undefined;
    acknowledgedAt?: number | undefined;
}>;
export type TaskNotification = z.infer<typeof TaskNotificationSchema>;
export declare const TaskRecordSchema: z.ZodEffects<z.ZodObject<{
    schemaVersion: z.ZodLiteral<1>;
    taskId: z.ZodString;
    ownerId: z.ZodString;
    kind: z.ZodOptional<z.ZodEnum<["background", "follow_up"]>>;
    parentTaskId: z.ZodOptional<z.ZodString>;
    rootTaskId: z.ZodOptional<z.ZodString>;
    originConversationId: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
    input: z.ZodEffects<z.ZodString, string, string>;
    title: z.ZodEffects<z.ZodString, string, string>;
    hermesSessionId: z.ZodEffects<z.ZodString, string, string>;
    runId: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
    executionMode: z.ZodEnum<["exclusive", "parallel_read_only"]>;
    resourceKeys: z.ZodArray<z.ZodEffects<z.ZodString, string, string>, "many">;
    status: z.ZodEnum<["queued", "dispatching", "running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown", "dispatch_unknown"]>;
    createdAt: z.ZodNumber;
    updatedAt: z.ZodNumber;
    revision: z.ZodNumber;
    sequence: z.ZodNumber;
    events: z.ZodArray<z.ZodObject<{
        sequence: z.ZodNumber;
        type: z.ZodEnum<["queued", "dispatching", "running", "waiting_for_approval", "stopping", "completed", "failed", "cancelled", "unknown", "dispatch_unknown", "progress", "stop_requested", "approval_required", "notification.announced", "notification.acknowledged", "operator_contained"]>;
        timestamp: z.ZodNumber;
        summary: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
    }, "strict", z.ZodTypeAny, {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }, {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }>, "many">;
    stopRequestedAt: z.ZodOptional<z.ZodNumber>;
    upstreamRunMissingAt: z.ZodOptional<z.ZodNumber>;
    operatorContainedAt: z.ZodOptional<z.ZodNumber>;
    output: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
    outputTruncated: z.ZodOptional<z.ZodBoolean>;
    usage: z.ZodOptional<z.ZodEffects<z.ZodRecord<z.ZodString, z.ZodNumber>, Record<string, number>, Record<string, number>>>;
    error: z.ZodOptional<z.ZodEffects<z.ZodString, string, string>>;
    notification: z.ZodEffects<z.ZodObject<{
        unread: z.ZodBoolean;
        announcedAt: z.ZodOptional<z.ZodNumber>;
        acknowledgedAt: z.ZodOptional<z.ZodNumber>;
    }, "strict", z.ZodTypeAny, {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    }, {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    }>, {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    }, {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    }>;
}, "strict", z.ZodTypeAny, {
    schemaVersion: 1;
    taskId: string;
    ownerId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    originConversationId?: string | undefined;
    input: string;
    title: string;
    hermesSessionId: string;
    runId?: string | undefined;
    executionMode: "exclusive" | "parallel_read_only";
    resourceKeys: string[];
    status: "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "queued" | "running" | "stopping" | "unknown" | "waiting_for_approval";
    createdAt: number;
    updatedAt: number;
    revision: number;
    sequence: number;
    events: {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }[];
    stopRequestedAt?: number | undefined;
    upstreamRunMissingAt?: number | undefined;
    operatorContainedAt?: number | undefined;
    output?: string | undefined;
    outputTruncated?: boolean | undefined;
    usage?: Record<string, number> | undefined;
    error?: string | undefined;
    notification: {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    };
}, {
    schemaVersion: 1;
    taskId: string;
    ownerId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    originConversationId?: string | undefined;
    input: string;
    title: string;
    hermesSessionId: string;
    runId?: string | undefined;
    executionMode: "exclusive" | "parallel_read_only";
    resourceKeys: string[];
    status: "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "queued" | "running" | "stopping" | "unknown" | "waiting_for_approval";
    createdAt: number;
    updatedAt: number;
    revision: number;
    sequence: number;
    events: {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }[];
    stopRequestedAt?: number | undefined;
    upstreamRunMissingAt?: number | undefined;
    operatorContainedAt?: number | undefined;
    output?: string | undefined;
    outputTruncated?: boolean | undefined;
    usage?: Record<string, number> | undefined;
    error?: string | undefined;
    notification: {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    };
}>, {
    schemaVersion: 1;
    taskId: string;
    ownerId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    originConversationId?: string | undefined;
    input: string;
    title: string;
    hermesSessionId: string;
    runId?: string | undefined;
    executionMode: "exclusive" | "parallel_read_only";
    resourceKeys: string[];
    status: "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "queued" | "running" | "stopping" | "unknown" | "waiting_for_approval";
    createdAt: number;
    updatedAt: number;
    revision: number;
    sequence: number;
    events: {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }[];
    stopRequestedAt?: number | undefined;
    upstreamRunMissingAt?: number | undefined;
    operatorContainedAt?: number | undefined;
    output?: string | undefined;
    outputTruncated?: boolean | undefined;
    usage?: Record<string, number> | undefined;
    error?: string | undefined;
    notification: {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    };
}, {
    schemaVersion: 1;
    taskId: string;
    ownerId: string;
    kind?: "background" | "follow_up" | undefined;
    parentTaskId?: string | undefined;
    rootTaskId?: string | undefined;
    originConversationId?: string | undefined;
    input: string;
    title: string;
    hermesSessionId: string;
    runId?: string | undefined;
    executionMode: "exclusive" | "parallel_read_only";
    resourceKeys: string[];
    status: "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "queued" | "running" | "stopping" | "unknown" | "waiting_for_approval";
    createdAt: number;
    updatedAt: number;
    revision: number;
    sequence: number;
    events: {
        sequence: number;
        type: "approval_required" | "cancelled" | "completed" | "dispatch_unknown" | "dispatching" | "failed" | "notification.acknowledged" | "notification.announced" | "operator_contained" | "progress" | "queued" | "running" | "stop_requested" | "stopping" | "unknown" | "waiting_for_approval";
        timestamp: number;
        summary?: string | undefined;
    }[];
    stopRequestedAt?: number | undefined;
    upstreamRunMissingAt?: number | undefined;
    operatorContainedAt?: number | undefined;
    output?: string | undefined;
    outputTruncated?: boolean | undefined;
    usage?: Record<string, number> | undefined;
    error?: string | undefined;
    notification: {
        unread: boolean;
        announcedAt?: number | undefined;
        acknowledgedAt?: number | undefined;
    };
}>;
export type TaskRecord = z.infer<typeof TaskRecordSchema>;
export interface CreateTaskRecordInput {
    ownerIdentity: string;
    input: string;
    title?: string;
    executionMode?: TaskExecutionMode;
    resourceKeys?: readonly string[];
    now?: number;
    taskId?: string;
    kind?: TaskKind;
    parentTaskId?: string;
    rootTaskId?: string;
    originConversationId?: string;
}
export declare function createTaskId(): string;
export declare function hashTaskOwnerId(ownerIdentity: string): string;
export declare function hermesSessionIdForTask(taskId: string): string;
export declare function createTaskRecord(input: CreateTaskRecordInput): TaskRecord;
export declare function sanitizeTaskTitle(value: string): string;
export declare function sanitizeTaskEventSummary(value: string): string;
export declare function sanitizeTaskOutput(value: string): string;
export declare function sanitizeTaskError(value: string): string;
export declare function sanitizeTaskUsage(value: unknown): TaskUsage | undefined;
export declare function parseTaskRecord(value: unknown): TaskRecord;
export declare function normalizeResourceKeys(values: readonly string[]): string[];
export declare function parseTaskTimestamp(value: number, label?: string): number;
//# sourceMappingURL=task.d.ts.map