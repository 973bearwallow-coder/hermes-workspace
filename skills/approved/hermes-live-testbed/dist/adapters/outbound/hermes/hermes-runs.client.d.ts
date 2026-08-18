import { type AppConfig } from "../../../config.js";
import type { ApprovalChoice } from "../../../domain/protocol/client-protocol.js";
import type { HermesRunEvent } from "../../../domain/protocol/server-protocol.js";
import type { ApprovalResult, CreateHermesSessionOptions, HermesCapabilities, HermesRequestOptions, HermesRunSnapshot, HermesRunsPort, HermesSessionChatResult, HermesSessionHistory, HermesSessionSummary, ListHermesSessionsOptions, StartRunParams, StartRunResult } from "../../../application/live-gateway/ports/hermes-runs.port.js";
export declare const MAX_HERMES_JSON_RESPONSE_BYTES = 1000000;
export declare const MAX_HERMES_RUN_OUTPUT_CHARS = 200000;
export declare const MAX_HERMES_RETRY_AFTER_CHARS = 128;
export declare const REQUIRED_HERMES_SESSION_FEATURES: readonly ["session_resources", "session_chat", "session_chat_streaming", "model_options", "session_model_lock"];
export declare class HermesRequestError extends Error {
    readonly status: number;
    readonly publicPath: string;
    readonly name = "HermesRequestError";
    readonly retryAfter?: string;
    readonly errorCode?: string;
    constructor(status: number, publicPath: string, retryAfter?: string, messagePrefix?: string, errorCode?: string);
}
export declare class HermesClient implements HermesRunsPort {
    readonly baseUrl: string;
    private readonly apiKey;
    private readonly model;
    private readonly timeoutMs;
    private readonly streamIdleTimeoutMs;
    private readonly sessionModelsReady;
    constructor(config: AppConfig["hermes"]);
    health(signal?: AbortSignal): Promise<Record<string, unknown>>;
    capabilities(signal?: AbortSignal): Promise<HermesCapabilities>;
    assertRunsSupported(signal?: AbortSignal): Promise<HermesCapabilities>;
    assertSessionsSupported(signal?: AbortSignal): Promise<HermesCapabilities>;
    listSessions(options?: ListHermesSessionsOptions): Promise<HermesSessionSummary[]>;
    createSession(options?: CreateHermesSessionOptions): Promise<HermesSessionSummary>;
    getSession(sessionId: string, signal?: AbortSignal): Promise<HermesSessionSummary>;
    getSessionHistory(sessionId: string, signal?: AbortSignal): Promise<HermesSessionHistory>;
    chatSession(sessionId: string, message: string, options?: {
        signal?: AbortSignal;
        sessionKey?: string;
        instructions?: string;
    }): Promise<HermesSessionChatResult>;
    private defaultModelSelection;
    private ensureSessionModelReady;
    startRun(params: StartRunParams, signal?: AbortSignal): Promise<StartRunResult>;
    getRun(runId: string, options?: AbortSignal | HermesRequestOptions): Promise<HermesRunSnapshot>;
    stopRun(runId: string, options?: AbortSignal | HermesRequestOptions): Promise<{
        run_id: string;
        status: "stopping";
    }>;
    submitApproval(runId: string, choice: ApprovalChoice, options?: {
        approvalId?: string;
        resolveAll?: boolean;
        signal?: AbortSignal;
        sessionKey?: string;
    }): Promise<ApprovalResult>;
    streamRunEvents(runId: string, options?: AbortSignal | HermesRequestOptions): AsyncGenerator<HermesRunEvent>;
    private requestJson;
    private headers;
    private sessionHeaders;
}
//# sourceMappingURL=hermes-runs.client.d.ts.map