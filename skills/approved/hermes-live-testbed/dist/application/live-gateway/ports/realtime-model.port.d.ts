import type { RealtimeResponseTruncation } from "../../../domain/protocol/client-protocol.js";
export interface LiveToolCall {
    id?: string;
    name: string;
    args: Record<string, unknown>;
}
export type LiveToolName = "continue_hermes_conversation" | "start_background_task" | "list_background_tasks" | "get_background_task" | "follow_up_background_task" | "stop_background_task" | "pause_voice_input";
export interface LiveModelAudio {
    data: string;
    mimeType: string;
    itemId?: string;
    contentIndex?: number;
}
export interface LiveTaskNotification {
    /** Gateway-built marker with only generic safe copy. Never include a raw task title, output, or error. */
    context: string;
    /** Short, already-sanitized generic sentence that may be spoken to the user. */
    announcement: string;
}
export declare const MAX_LIVE_TASK_NOTIFICATION_CONTEXT_CHARS = 1000;
export declare const MAX_LIVE_TASK_NOTIFICATION_ANNOUNCEMENT_CHARS = 500;
export declare function requireLiveTaskNotification(value: unknown): LiveTaskNotification;
export type LiveModelEvent = {
    type: "audio";
    audio: LiveModelAudio;
} | {
    type: "text";
    text: string;
    speaker?: "user" | "assistant" | "system";
    final?: boolean;
} | {
    type: "response";
    status: "started" | "completed" | "cancelled" | "failed";
    responseId?: string;
    scope?: "conversation" | "task_notification";
    error?: string;
} | {
    type: "tool_call";
    call: LiveToolCall;
} | {
    type: "tool_call_cancelled";
    callIds: string[];
} | {
    type: "input_speech_started";
    provider: "openai" | "local";
    itemId?: string;
    audioStartMs?: number;
} | {
    type: "input_speech_stopped";
    provider: "openai" | "local";
    itemId?: string;
    audioEndMs?: number;
};
export interface LiveModelCallbacks {
    onEvent(event: LiveModelEvent): void;
    onOpen?(): void;
    onClose?(event?: unknown): void;
    onError?(error: unknown): void;
}
export interface LiveModelSession {
    sendRealtimeAudio(audio: LiveModelAudio): Promise<void>;
    sendText(text: string): Promise<void>;
    /** Returns true when this call starts or schedules a provider response. */
    sendAudioStreamEnd(): Promise<boolean>;
    cancelResponse(reason?: string, truncate?: RealtimeResponseTruncation): Promise<boolean>;
    sendToolResponse(call: LiveToolCall, response: Record<string, unknown>): Promise<void>;
    sendTaskNotification?(notification: LiveTaskNotification): Promise<void>;
    close(): Promise<void>;
}
export interface LiveModelConnectParams {
    sessionId: string;
    systemInstruction: string;
    /** Only tools that can succeed for this negotiated client/session. */
    availableTools?: readonly LiveToolName[];
    safetyIdentifier?: string;
    callbacks: LiveModelCallbacks;
}
export interface LiveModelAdapter {
    connect(params: LiveModelConnectParams): Promise<LiveModelSession>;
}
//# sourceMappingURL=realtime-model.port.d.ts.map