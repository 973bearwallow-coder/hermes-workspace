import type { Readable, Writable } from "node:stream";
import type { PublicConversation, PublicTaskSnapshot } from "../domain/protocol/server-protocol.js";
import type { ConversationSelection } from "../domain/protocol/client-protocol.js";
export interface TerminalGatewaySessionOptions {
    url: string;
    authToken?: string;
    userLabel?: string;
    connectTimeoutMs?: number;
    onLine?: (line: string) => void;
    conversation?: ConversationSelection;
}
export interface InteractiveTerminalOptions extends TerminalGatewaySessionOptions {
    input?: Readable;
    output?: Writable;
}
export interface TerminalGatewaySnapshot {
    connected: boolean;
    sessionId?: string;
    provider?: string;
    model?: string;
    conversation?: PublicConversation;
    responseActive: boolean;
    tasks: PublicTaskSnapshot[];
    activeTaskIds: string[];
    lastTaskId?: string;
}
export interface TerminalCommandResult {
    closeRequested: boolean;
}
/**
 * A text-only client for a running Hermes Live gateway. Background work is
 * server-owned: closing this session detaches and never implies cancellation.
 */
export declare class TerminalGatewaySession {
    private readonly url;
    private readonly authToken?;
    private readonly userLabel;
    private readonly connectTimeoutMs;
    private readonly onLine;
    private readonly conversationSelection;
    private socket?;
    private ready;
    private intentionalClose;
    private requestSequence;
    private sessionId?;
    private provider?;
    private model?;
    private conversation?;
    private responseActive;
    private assistantTranscript;
    private responseHadAudio;
    private readonly tasks;
    private readonly taskLifecycleSequences;
    private readonly taskLifecycleRevisions;
    private readonly taskNotifications;
    private taskOrder;
    private lastTaskId?;
    private readonly pendingRequests;
    private readonly renderedNotifications;
    private resolveClosed;
    private closedResolved;
    readonly closed: Promise<void>;
    constructor(options: TerminalGatewaySessionOptions);
    get snapshot(): TerminalGatewaySnapshot;
    connect(): Promise<void>;
    execute(input: string): TerminalCommandResult;
    close(): Promise<void>;
    private handleSessionReady;
    private handleServerMessage;
    private handleTaskSnapshot;
    private applyTaskLifecycle;
    private taskFromLifecycle;
    private renderTaskLifecycle;
    private requestTaskList;
    private requestTask;
    private requestStop;
    private requestFollowUp;
    private requestNotificationAcknowledgement;
    private trackAndSend;
    private upsertTaskSnapshot;
    private retainTask;
    private handleTaskNotification;
    private orderedTasks;
    private renderTaskList;
    private renderTaskDetail;
    private renderTaskResult;
    private flushAssistantResponse;
    private resetResponseOutput;
    private printHelp;
    private printStatus;
    private send;
    private nextRequestId;
    private line;
    private resolveClosedOnce;
}
export declare function runInteractiveTerminal(options: InteractiveTerminalOptions): Promise<void>;
export declare function normalizeGatewayWebSocketUrl(value: string): string;
export declare function sanitizeTerminalText(value: string, maxChars?: number): string;
//# sourceMappingURL=terminal-session.d.ts.map