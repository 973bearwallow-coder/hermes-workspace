import type { FollowUpBackgroundTaskInput, SubmitBackgroundTaskInput, TaskNotificationAnnouncementClaim, TaskRecordListener, TaskSupervisorPort } from "../live-gateway/ports/task-supervisor.port.js";
import type { HermesRunsPort } from "../live-gateway/ports/hermes-runs.port.js";
import type { TaskStorePort } from "./ports/task-store.port.js";
import { type TaskRecord } from "../../domain/tasks/index.js";
export interface TaskSupervisorScheduler {
    setTimeout(callback: () => void, delayMs: number): unknown;
    clearTimeout(handle: unknown): void;
}
export interface TaskSupervisorOptions {
    store: TaskStorePort;
    hermes: HermesRunsPort;
    maxConcurrent?: number;
    trustDeclaredReadOnly?: boolean;
    maxQueued?: number;
    pollIntervalMs?: number;
    retryBaseMs?: number;
    retryMaxMs?: number;
    runInstructions?: string;
    now?: () => number;
    scheduler?: TaskSupervisorScheduler;
    onError?: (error: unknown) => void;
}
export declare class TaskQueueFullError extends Error {
    constructor(limit: number);
}
export declare class TaskNotFoundError extends Error {
    constructor(taskId: string);
}
export declare class TaskSupervisorClosedError extends Error {
    constructor();
}
/**
 * Server-owned background task runtime. Every state emitted to a subscriber has
 * already been durably written through TaskStorePort.
 */
export declare class TaskSupervisor implements TaskSupervisorPort {
    private readonly store;
    private readonly hermes;
    private readonly maxConcurrent;
    private readonly trustDeclaredReadOnly;
    private readonly maxQueued;
    private readonly pollIntervalMs;
    private readonly retryBaseMs;
    private readonly retryMaxMs;
    private readonly runInstructions?;
    private readonly now;
    private readonly scheduler;
    private readonly onError?;
    private readonly ownerSessionKeys;
    private readonly notificationAnnouncementClaims;
    private readonly subscribers;
    private readonly timers;
    private readonly retryAttempts;
    private readonly retryNotBefore;
    private readonly acceptedRunsAwaitingPersistence;
    private readonly taskStateFailures;
    private readonly progressEventCounts;
    private readonly watching;
    private readonly pollSuppressed;
    private readonly confirmedStopRequests;
    private readonly stopRequests;
    private readonly containingApprovals;
    private readonly backgroundOperations;
    private readonly abortController;
    private operationTail;
    private initializePromise?;
    private closePromise?;
    private initialized;
    private closed;
    private drainQueued;
    private drainRunning;
    private drainRequested;
    private lastCreatedAt?;
    constructor(options: TaskSupervisorOptions);
    initialize(): Promise<void>;
    close(): Promise<void>;
    private closeOnce;
    registerOwner(ownerIdentity: string, sessionKey: string): string;
    submit(input: SubmitBackgroundTaskInput): Promise<TaskRecord>;
    followUp(input: FollowUpBackgroundTaskInput): Promise<TaskRecord>;
    list(ownerId: string, limit?: number): Promise<TaskRecord[]>;
    listActive(ownerId: string): Promise<TaskRecord[]>;
    listUnreadNotifications(ownerId: string): Promise<TaskRecord[]>;
    get(ownerId: string, taskId: string): Promise<TaskRecord | undefined>;
    stop(ownerId: string, taskId: string, reason?: string): Promise<TaskRecord>;
    acknowledgeNotification(ownerId: string, taskId: string): Promise<TaskRecord>;
    markNotificationAnnounced(ownerId: string, taskId: string): Promise<TaskRecord>;
    claimNotificationAnnouncement(ownerId: string, taskId: string, claimantId: string): Promise<TaskNotificationAnnouncementClaim>;
    completeNotificationAnnouncement(ownerId: string, taskId: string, claimantId: string): Promise<TaskRecord>;
    releaseNotificationAnnouncement(ownerId: string, taskId: string, claimantId: string): void;
    health(): Promise<void>;
    subscribe(ownerId: string, listener: TaskRecordListener): () => void;
    private initializeOnce;
    private requestStop;
    private sendStopRequest;
    private updateOwnedNotification;
    private requireOwned;
    private assertReady;
    private assertOpen;
    private scheduleDrain;
    private performDrain;
    private admitNextTask;
    private dispatchTask;
    private handleDispatchStartFailure;
    private activateAcceptedRun;
    private persistAcceptedRun;
    private startWatcher;
    private consumeRunEvents;
    private handleRunEvent;
    private handleApprovalRequest;
    private containUncorrelatedApproval;
    private appendBoundedProgress;
    private reconcileTask;
    private applySnapshot;
    private moveToStatus;
    private markUnknown;
    private transitionPersist;
    private mutatePersist;
    private recordTaskStateFailure;
    private requireTask;
    private schedulePoll;
    private pollTask;
    private scheduleTimer;
    private publish;
    private serialized;
    private reportError;
    private trackBackground;
    private nextCreationTimestamp;
}
//# sourceMappingURL=task-supervisor.d.ts.map