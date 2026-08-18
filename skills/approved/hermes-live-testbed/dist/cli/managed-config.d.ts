export declare const MANAGED_CONFIG_KEYS: readonly ["GEMINI_API_KEY", "GEMINI_MODEL", "GOOGLE_API_KEY", "GOOGLE_CLOUD_LOCATION", "GOOGLE_CLOUD_PROJECT", "GOOGLE_GENAI_API_VERSION", "GOOGLE_GENAI_USE_ENTERPRISE", "HERMES_AGENT_API_SERVER_KEY", "HERMES_API_KEY", "HERMES_BASE_URL", "HERMES_LIVE_ALLOW_ORIGIN", "HERMES_LIVE_ALLOW_UNAUTHENTICATED", "HERMES_LIVE_AUTH_TOKEN", "HERMES_LIVE_DEMO_ENABLED", "HERMES_LIVE_HERMES_STREAM_IDLE_TIMEOUT_MS", "HERMES_LIVE_HERMES_TIMEOUT_MS", "HERMES_LIVE_HOST", "HERMES_LIVE_LOCAL_ALLOW_REMOTE", "HERMES_LIVE_LOCAL_OWNS_TURN_ROUTING", "HERMES_LIVE_LOCAL_URL", "HERMES_LIVE_LOCAL_VOICE", "HERMES_LIVE_MAX_AUDIO_BYTES", "HERMES_LIVE_MAX_CONCURRENT_TASKS", "HERMES_LIVE_MAX_QUEUED_TASKS", "HERMES_LIVE_MAX_SESSIONS", "HERMES_LIVE_MAX_TEXT_CHARS", "HERMES_LIVE_PORT", "HERMES_LIVE_PROFILE_ID", "HERMES_LIVE_PROVIDER", "HERMES_LIVE_PROVIDER_READY_TIMEOUT_MS", "HERMES_LIVE_RUN_INSTRUCTIONS", "HERMES_LIVE_SESSION_PREFIX", "HERMES_LIVE_TASK_HISTORY_LIMIT", "HERMES_LIVE_TASK_POLL_INTERVAL_MS", "HERMES_LIVE_TASK_RETENTION_HOURS", "HERMES_LIVE_TASK_STATE_FILE", "HERMES_LIVE_TRUST_CLIENT_IDENTITY", "HERMES_LIVE_TRUST_DECLARED_READ_ONLY", "HERMES_LIVE_USER_LABEL", "HERMES_MODEL", "OPENAI_API_KEY", "OPENAI_REALTIME_BASE_URL", "OPENAI_REALTIME_INPUT_AUDIO_FORMAT", "OPENAI_REALTIME_INPUT_TRANSCRIPTION_LANGUAGE", "OPENAI_REALTIME_INPUT_TRANSCRIPTION_MODEL", "OPENAI_REALTIME_MODEL", "OPENAI_REALTIME_OUTPUT_AUDIO_FORMAT", "OPENAI_REALTIME_REASONING_EFFORT", "OPENAI_REALTIME_TURN_DETECTION", "OPENAI_REALTIME_VOICE"];
export type ManagedConfigKey = (typeof MANAGED_CONFIG_KEYS)[number];
export type ManagedConfigValues = Partial<Record<ManagedConfigKey, string>>;
export interface ManagedConfigReadResult {
    path: string;
    exists: boolean;
    values: ManagedConfigValues;
}
export interface ManagedConfigOptions {
    path?: string;
    home?: string;
    hermesHome?: string;
}
export declare function managedConfigPath(options?: ManagedConfigOptions): string;
export declare function applyManagedConfigToProcess(options?: ManagedConfigOptions): Promise<ManagedConfigReadResult>;
export declare function resolvedManagedEnvironment(env?: NodeJS.ProcessEnv, options?: ManagedConfigOptions): Promise<NodeJS.ProcessEnv>;
export declare function readManagedConfig(options?: ManagedConfigOptions): Promise<ManagedConfigReadResult>;
export declare function writeManagedConfig(values: ManagedConfigValues, options?: ManagedConfigOptions): Promise<string>;
export declare function parseManagedConfig(source: string, sourceLabel?: string): ManagedConfigValues;
export declare function serializeManagedConfig(values: ManagedConfigValues): string;
//# sourceMappingURL=managed-config.d.ts.map