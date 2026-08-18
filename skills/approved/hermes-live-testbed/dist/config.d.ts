export declare const MAX_COMPATIBLE_AUDIO_FRAME_BYTES = 5900000;
export declare const MAX_COMPATIBLE_TEXT_CHARS = 1000000;
export declare const DEFAULT_HERMES_STREAM_IDLE_TIMEOUT_MS = 120000;
export type RealtimeProvider = "local" | "gemini" | "openai" | "mock";
export interface AppConfig {
    server: {
        host: string;
        port: number;
        authToken?: string;
        allowUnauthenticated: boolean;
        allowOrigin?: string;
        sessionPrefix: string;
        defaultProfileId: string;
        defaultUserLabel: string;
        trustClientIdentity: boolean;
        maxSessions: number;
        maxAudioBytes: number;
        maxTextChars: number;
        providerReadyTimeoutMs: number;
        demoEnabled: boolean;
    };
    hermes: {
        baseUrl: string;
        apiKey?: string;
        model?: string;
        instructions?: string;
        timeoutMs: number;
        streamIdleTimeoutMs?: number;
    };
    tasks: {
        stateFile: string;
        maxConcurrent: number;
        trustDeclaredReadOnly: boolean;
        maxQueued: number;
        historyLimit: number;
        retentionMs: number;
        pollIntervalMs: number;
    };
    realtime: {
        provider: RealtimeProvider;
        model: string;
    };
    local: {
        url: string;
        voice: string;
        allowRemote: boolean;
        /** Managed runtime compatibility mode; external upstream endpoints leave this unset. */
        ownsTurnRouting?: boolean;
    };
    gemini: {
        apiKey?: string;
        model: string;
        enterprise: boolean;
        project?: string;
        location: string;
        apiVersion?: string;
    };
    openai: {
        apiKey?: string;
        baseUrl: string;
        model: string;
        voice: string;
        reasoningEffort: "minimal" | "low" | "medium" | "high" | "xhigh";
        turnDetection: "disabled" | "semantic_vad" | "server_vad";
        inputAudioFormat: "pcm16" | "g711_ulaw" | "g711_alaw";
        outputAudioFormat: "pcm16" | "g711_ulaw" | "g711_alaw";
        inputTranscriptionModel?: string;
        inputTranscriptionLanguage?: string;
    };
}
export declare function loadConfig(env?: NodeJS.ProcessEnv): AppConfig;
export declare function assertRuntimeConfig(config: AppConfig): void;
export declare function assertHermesApiConfig(config: Pick<AppConfig, "hermes">): void;
export declare function assertGatewayExposureConfig(config: Pick<AppConfig, "server">): void;
export declare function assertRealtimeProviderConfig(config: Pick<AppConfig, "realtime" | "local" | "gemini" | "openai">): void;
export declare function realtimeProviderConfigured(config: Pick<AppConfig, "realtime" | "local" | "gemini" | "openai">): boolean;
export declare function sanitizeSessionComponent(value: string): string;
export declare function makeSessionKey(prefix: string, profileId: string, userLabel: string): string;
export declare function isSafeGoogleCloudProject(value: string): boolean;
export declare function isSafeGoogleCloudLocation(value: string): boolean;
export declare function isSafeGoogleGenAiApiVersion(value: string): boolean;
export declare function publicBaseUrl(value: string): string;
export declare function isLoopbackHostname(hostname: string): boolean;
//# sourceMappingURL=config.d.ts.map