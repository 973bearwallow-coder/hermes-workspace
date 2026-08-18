import type { TaskListOptions, TaskPruneOptions, TaskPruneResult, TaskStorePort, TaskUpdateOptions } from "../../../application/task-supervisor/ports/task-store.port.js";
import { type TaskRecord } from "../../../domain/tasks/index.js";
export interface FileTaskStoreOptions {
    directory: string;
    filename?: string;
    maxRecords?: number;
    retentionMs?: number;
    maxStoreBytes?: number;
    terminalReserveSlots?: number;
    automaticPruning?: boolean;
    now?: () => number;
}
export interface ClearAbandonedTaskStoreLockResult {
    cleared: boolean;
    ownerPid?: number;
    ownerHostname?: string;
    ownerMetadataValid?: boolean;
}
export declare class TaskStoreCorruptionError extends Error {
    constructor(message: string, options?: ErrorOptions);
}
export declare class TaskStoreCapacityError extends Error {
    constructor(message: string);
}
export declare class TaskStoreConflictError extends Error {
    constructor(message: string);
}
export declare class TaskStoreLockedError extends Error {
    constructor(message: string);
}
export declare class FileTaskStore implements TaskStorePort {
    readonly filePath: string;
    private readonly directory;
    private readonly lockDirectory;
    private readonly lockOwnerPath;
    private readonly lockToken;
    private readonly maxRecords;
    private readonly retentionMs;
    private readonly maxStoreBytes;
    private readonly maximumStoreBytes;
    private readonly terminalReserveSlots;
    private readonly automaticPruning;
    private readonly now;
    private capacityLimitBytes;
    private records?;
    private documentUpdatedAt;
    private operationTail;
    private poisoned?;
    private lockCleanupFailure?;
    private lockHeld;
    private closed;
    private closePromise?;
    constructor(options: FileTaskStoreOptions);
    close(): Promise<void>;
    load(taskId: string): Promise<TaskRecord | undefined>;
    list(options?: TaskListOptions): Promise<TaskRecord[]>;
    put(value: TaskRecord): Promise<TaskRecord>;
    update(taskId: string, updater: (current: TaskRecord) => TaskRecord, options?: TaskUpdateOptions): Promise<TaskRecord>;
    delete(taskId: string): Promise<boolean>;
    prune(options?: TaskPruneOptions): Promise<TaskPruneResult>;
    private serialized;
    private ensureLoaded;
    private ensureDirectory;
    private persist;
    private fitDocumentToByteLimit;
    private pruneMap;
    private acquireLock;
    private assertLockOwned;
    private releaseLock;
}
/**
 * Clears a lock left behind by an unclean exit. This is intentionally explicit:
 * automatic stale-lock reclamation can let two processes become writers during
 * an event-loop stall. A same-host live PID is always refused.
 */
export declare function clearAbandonedTaskStoreLock(options: Pick<FileTaskStoreOptions, "directory" | "filename">): Promise<ClearAbandonedTaskStoreLockResult>;
/** Directory sync is not available on every supported operating system. */
export declare function syncDirectoryHandle(handle: {
    sync(): Promise<void>;
}): Promise<void>;
//# sourceMappingURL=file-task-store.d.ts.map