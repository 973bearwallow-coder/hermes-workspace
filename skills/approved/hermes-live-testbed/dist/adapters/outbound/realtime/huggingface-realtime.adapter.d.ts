import type { AppConfig } from "../../../config.js";
import type { LiveModelAdapter, LiveModelConnectParams, LiveModelSession } from "../../../application/live-gateway/ports/realtime-model.port.js";
export declare const DEFAULT_LOCAL_RESPONSE_TIMEOUT_MS = 120000;
export declare const DEFAULT_LOCAL_PIPELINE_RELEASE_GRACE_MS = 150;
/**
 * Adapter for Hugging Face speech-to-speech's OpenAI Realtime-compatible
 * server. The wire vocabulary is shared with OpenAI, but the server owns
 * VAD-driven response creation and does not acknowledge session.update.
 */
export declare class HuggingFaceRealtimeAdapter implements LiveModelAdapter {
    private readonly config;
    private readonly connectTimeoutMs;
    private readonly closeTimeoutMs;
    private readonly responseTimeoutMs;
    private readonly pipelineReleaseGraceMs;
    constructor(config: AppConfig["local"], connectTimeoutMs?: number, closeTimeoutMs?: number, responseTimeoutMs?: number, pipelineReleaseGraceMs?: number);
    connect(params: LiveModelConnectParams): Promise<LiveModelSession>;
    private connectOnce;
}
export declare function buildHuggingFaceSessionUpdate(config: AppConfig["local"], systemInstruction: string, availableTools?: LiveModelConnectParams["availableTools"]): {
    type: "session.update";
    session: Record<string, unknown>;
};
//# sourceMappingURL=huggingface-realtime.adapter.d.ts.map