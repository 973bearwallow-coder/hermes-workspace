import type { AppConfig } from "./config.js";
export declare const LOCAL_FUNCTIONAL_PROVIDER_SMOKE_TIMEOUT_MS = 120000;
export interface LiveProviderSmokeReport {
    ok: true;
    provider: Exclude<AppConfig["realtime"]["provider"], "mock">;
    model: string;
    connected: true;
    openCallback: boolean;
    elapsedMs: number;
    eventCount: number;
    sampleEvents: Array<Record<string, unknown>>;
    functional?: {
        checked: true;
        toolCall: true;
        spokenReceipt: true;
        elapsedMs: number;
    };
    closeEvent?: Record<string, unknown>;
}
export interface LiveProviderSmokeOptions {
    timeoutMs?: number;
    verifyToolCall?: boolean;
}
export declare function runLiveProviderSmoke(config: AppConfig, options?: LiveProviderSmokeOptions): Promise<LiveProviderSmokeReport>;
//# sourceMappingURL=live-provider-smoke.d.ts.map