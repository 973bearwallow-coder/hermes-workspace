import type { AppConfig } from "../../../config.js";
import { type LiveModelAudio, type LiveModelEvent, type LiveTaskNotification } from "../../../application/live-gateway/ports/realtime-model.port.js";
import type { RealtimeResponseTruncation } from "../../../domain/protocol/client-protocol.js";
import type { LiveModelAdapter, LiveModelConnectParams, LiveModelSession } from "../../../application/live-gateway/ports/realtime-model.port.js";
export declare const OPENAI_MAX_HANDLED_TOOL_CALLS = 4096;
export declare const OPENAI_MAX_QUEUED_RESPONSE_REQUESTS = 32;
export declare class OpenAIRealtimeAdapter implements LiveModelAdapter {
    private readonly config;
    private readonly connectTimeoutMs;
    private readonly closeTimeoutMs;
    constructor(config: AppConfig["openai"], connectTimeoutMs?: number, closeTimeoutMs?: number);
    connect(params: LiveModelConnectParams): Promise<LiveModelSession>;
}
export declare function buildOpenAITaskNotificationResponse(notification: LiveTaskNotification): Record<string, unknown>;
export declare function normalizeOpenAIRealtimeEvent(event: unknown, outputAudioFormat?: AppConfig["openai"]["outputAudioFormat"], options?: {
    provider?: "openai" | "local";
    pcmSampleRate?: number;
    includeCompletedInputTranscript?: boolean;
    includeCompletedOutputTranscript?: boolean;
}): LiveModelEvent[];
export declare function buildOpenAIRealtimeAudioAppend(audio: LiveModelAudio, inputFormat?: AppConfig["openai"]["inputAudioFormat"]): {
    type: "input_audio_buffer.append";
    audio: string;
};
export declare function buildOpenAIResponseCancel(responseId?: string, eventId?: string): {
    type: "response.cancel";
    event_id?: string;
    response_id?: string;
};
export declare function buildOpenAIConversationItemTruncate(truncate: RealtimeResponseTruncation): {
    type: "conversation.item.truncate";
    item_id: string;
    content_index: number;
    audio_end_ms: number;
};
export declare function buildOpenAISessionUpdate(config: AppConfig["openai"], systemInstruction: string, availableTools?: LiveModelConnectParams["availableTools"]): {
    type: "session.update";
    session: Record<string, unknown>;
};
//# sourceMappingURL=openai-realtime.adapter.d.ts.map