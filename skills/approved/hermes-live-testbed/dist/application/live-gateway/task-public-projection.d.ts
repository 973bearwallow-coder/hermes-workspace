import type { TaskRecord, TaskStatus } from "../../domain/tasks/index.js";
import type { PublicTaskSnapshot, ServerMessage, TaskNotification } from "../../domain/protocol/server-protocol.js";
export interface ProjectTaskOptions {
    includeOutput?: boolean;
}
export declare function projectTaskSnapshot(record: TaskRecord, options?: ProjectTaskOptions): PublicTaskSnapshot;
export declare function projectTaskLifecycle(record: TaskRecord, requestId?: string): ServerMessage;
export declare function projectTaskNotification(record: TaskRecord): TaskNotification | undefined;
/**
 * Withdraw a previously projected notice when an uncertain task re-enters a
 * non-notifiable recovery state. Reconnects do not need this projection because
 * the durable unread bit is already clear; it exists for connected clients
 * that still hold the old notification identity.
 */
export declare function projectSupersededTaskNotification(record: TaskRecord): TaskNotification | undefined;
export declare function notificationIdForTask(record: Pick<TaskRecord, "taskId" | "sequence" | "status" | "events" | "operatorContainedAt">): string;
export declare function isTaskNotificationState(status: TaskStatus): boolean;
//# sourceMappingURL=task-public-projection.d.ts.map