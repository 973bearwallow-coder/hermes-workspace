import { Modality } from "@google/genai";
import { type AppConfig } from "../../../config.js";
import { type LiveModelAdapter, type LiveModelAudio, type LiveModelConnectParams, type LiveModelEvent, type LiveModelSession, type LiveTaskNotification, type LiveToolCall } from "../../../application/live-gateway/ports/realtime-model.port.js";
interface ProviderCloseConfirmation {
    readonly promise: Promise<void>;
    isClosed(): boolean;
    confirm(): void;
}
export declare class GeminiLiveAdapter implements LiveModelAdapter {
    private readonly config;
    private readonly closeTimeoutMs;
    constructor(config: AppConfig["gemini"], closeTimeoutMs?: number);
    connect(params: LiveModelConnectParams): Promise<LiveModelSession>;
    private assertConfigured;
    private createClient;
}
export declare function buildGeminiClientOptions(config: AppConfig["gemini"]): Record<string, unknown>;
export declare function officialGeminiApiBaseUrl(config: Pick<AppConfig["gemini"], "enterprise" | "location">): string;
export declare function createGeminiLiveEventForwarder(onEvent: (event: LiveModelEvent) => void): (message: unknown) => void;
export declare function buildGeminiLiveConnectConfig(systemInstruction: string, availableTools?: LiveModelConnectParams["availableTools"]): {
    responseModalities: Modality[];
    inputAudioTranscription: {};
    outputAudioTranscription: {};
    systemInstruction: string;
    tools?: {
        functionDeclarations: {
            name: "continue_hermes_conversation" | "follow_up_background_task" | "get_background_task" | "list_background_tasks" | "pause_voice_input" | "start_background_task" | "stop_background_task";
            description: "Delegate meaningful work to Hermes Agent as a durable background task. Returns quickly; the user may keep talking or disconnect while the task continues." | "List this user's active and recent Hermes background tasks from the durable task inbox." | "Pause microphone listening only when the user explicitly asks to pause, mute, or stop listening. This keeps Live Voice connected and leaves every background task running; the user resumes from the client control." | "Read the exact status or retained result of one Hermes background task." | "Request cooperative cancellation of one exact Hermes background task." | "Send one conversational turn to the Hermes session selected by the user. Use it for answers, memory, and follow-ups that must remain in that persisted chat; use a background task for long independent work." | "Start durable follow-up work from a finished task and its retained result. Use the exact task_id returned by the gateway. The follow-up is a new independently stoppable task in the same lineage.";
            parametersJsonSchema: {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly message: {
                        readonly type: "string";
                        readonly description: "The complete user request to append to the selected Hermes conversation.";
                    };
                };
                readonly required: readonly ["message"];
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly message: {
                        readonly type: "string";
                        readonly description: "The complete, concise task Hermes should perform.";
                    };
                    readonly title: {
                        readonly type: "string";
                        readonly description: "A short user-facing title for the task inbox.";
                    };
                    readonly recent_voice_context: {
                        readonly type: "string";
                        readonly description: "Only the minimum recent voice context required to resolve references in the task.";
                    };
                    readonly execution_mode: {
                        readonly type: "string";
                        readonly enum: readonly ["exclusive", "parallel_read_only"];
                        readonly description: "Use exclusive unless the task is provably read-only. Read-only tasks overlap only when their resource_keys are disjoint; mutating tasks are serialized.";
                    };
                    readonly resource_keys: {
                        readonly type: "array";
                        readonly maxItems: 8;
                        readonly items: {
                            readonly type: "string";
                        };
                        readonly description: "Stable resources read or touched by the task, such as an absolute repository path or deployment target. Tasks sharing a key never overlap.";
                    };
                };
                readonly required: readonly ["message"];
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly include_completed: {
                        readonly type: "boolean";
                        readonly description: "Include recent terminal tasks. Defaults to true.";
                    };
                    readonly summary_only: {
                        readonly type: "boolean";
                        readonly description: "Return a short safe spoken count instead of task details when the user asks only what is running.";
                    };
                };
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly task_id: {
                        readonly type: "string";
                        readonly pattern: "^task_[a-f0-9]{32}$";
                        readonly description: "The stable Hermes Live task id returned by start_background_task or list_background_tasks.";
                    };
                    readonly include_output: {
                        readonly type: "boolean";
                        readonly description: "Include the bounded final output when it is available and the user asked for details.";
                    };
                };
                readonly required: readonly ["task_id"];
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly task_id: {
                        readonly type: "string";
                        readonly pattern: "^task_[a-f0-9]{32}$";
                        readonly description: "The stable Hermes Live task id returned by start_background_task or list_background_tasks.";
                    };
                    readonly message: {
                        readonly type: "string";
                        readonly description: "The user's complete follow-up request.";
                    };
                    readonly title: {
                        readonly type: "string";
                        readonly description: "Optional short title for the follow-up task.";
                    };
                };
                readonly required: readonly ["task_id", "message"];
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {
                    readonly task_id: {
                        readonly type: "string";
                        readonly pattern: "^task_[a-f0-9]{32}$";
                        readonly description: "The stable Hermes Live task id returned by start_background_task or list_background_tasks.";
                    };
                    readonly reason: {
                        readonly type: "string";
                        readonly description: "A short reason for the cancellation request.";
                    };
                };
                readonly required: readonly ["task_id"];
            } | {
                readonly type: "object";
                readonly additionalProperties: false;
                readonly properties: {};
            };
        }[];
    }[] | undefined;
};
export declare class GeminiLiveSession implements LiveModelSession {
    private readonly session;
    private readonly closeConfirmation;
    private readonly closeTimeoutMs;
    private closeOperation?;
    constructor(session: any, closeConfirmation: ProviderCloseConfirmation, closeTimeoutMs?: number);
    sendRealtimeAudio(audio: LiveModelAudio): Promise<void>;
    sendText(text: string): Promise<void>;
    sendAudioStreamEnd(): Promise<boolean>;
    cancelResponse(): Promise<boolean>;
    sendToolResponse(call: LiveToolCall, response: Record<string, unknown>): Promise<void>;
    sendTaskNotification(notification: LiveTaskNotification): Promise<void>;
    close(): Promise<void>;
    private closeAndConfirm;
}
export declare function buildGeminiRealtimeAudioInput(audio: LiveModelAudio): {
    audio: {
        data: string;
        mimeType: string;
    };
};
export declare function buildGeminiRealtimeTextInput(text: string): {
    text: string;
};
export declare function buildGeminiTextTurn(text: string): {
    turns: Array<{
        role: "user";
        parts: Array<{
            text: string;
        }>;
    }>;
    turnComplete: true;
};
export declare function buildGeminiTaskNotificationInput(notification: LiveTaskNotification): ReturnType<typeof buildGeminiRealtimeTextInput>;
export declare function buildGeminiToolResponse(call: LiveToolCall, response: Record<string, unknown>): {
    functionResponses: Array<{
        id: string;
        name: string;
        response: Record<string, unknown>;
    }>;
};
export declare function normalizeGeminiLiveMessage(message: unknown): LiveModelEvent[];
export {};
//# sourceMappingURL=gemini-live.adapter.d.ts.map