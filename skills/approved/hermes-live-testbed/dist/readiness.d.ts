import { type AppConfig } from "./config.js";
import type { HermesRunsPort } from "./application/live-gateway/ports/hermes-runs.port.js";
export interface ReadinessSection extends Record<string, unknown> {
    ok: boolean;
}
export interface ReadinessReport {
    ok: boolean;
    gateway: ReadinessSection;
    hermes: ReadinessSection;
    realtime: ReadinessSection;
    tasks: ReadinessSection;
}
export interface TaskRuntimeHealthPort {
    health(): Promise<void>;
}
export interface BuildReadinessReportOptions {
    hermes?: HermesRunsPort;
    tasks?: TaskRuntimeHealthPort;
    requireHermesApiKey?: boolean;
    requireRealtimeProviderConfig?: boolean;
}
export declare function buildReadinessReport(config: AppConfig, options?: BuildReadinessReportOptions): Promise<ReadinessReport>;
//# sourceMappingURL=readiness.d.ts.map