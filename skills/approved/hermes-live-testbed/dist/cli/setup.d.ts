import { loadConfig, type RealtimeProvider } from "../config.js";
import { type ReadinessReport } from "../readiness.js";
import { type PluginInstallStatus } from "./plugin-installer.js";
import { type CommandRunner } from "./process.js";
import { type ServiceStatus } from "./service-manager.js";
import { type GatewayEndpointState } from "./gateway-probe.js";
export interface SetupOptions {
    provider?: RealtimeProvider;
    hermesUrl?: string;
    configPath?: string;
    pluginsDir?: string;
    hermesCommand?: string;
    enablePlugin: boolean;
    service: boolean;
    nonInteractive: boolean;
    json: boolean;
}
export interface SetupReport {
    ok: boolean;
    config: {
        path: string;
        written: boolean;
    };
    provider: RealtimeProvider;
    plugin: PluginInstallStatus;
    hermesCli: {
        command?: string;
        enabled: boolean;
        skipped: boolean;
        error?: string;
    };
    hermesGateway: {
        managed: boolean;
        configured: boolean;
        ready: boolean;
        action: "already-running" | "installed" | "skipped" | "failed";
        error?: string;
    };
    readiness: ReadinessReport;
    providerSession: {
        checked: boolean;
        ok: boolean;
        error?: string;
    };
    localService: ServiceStatus | {
        skipped: true;
        reason: string;
        error?: string;
    };
    service: ServiceStatus | {
        skipped: true;
        reason: string;
    };
    gateway: {
        checked: boolean;
        ready: boolean;
        url: string;
        error?: string;
    };
    nextSteps: string[];
}
export interface SetupDependencies {
    env?: NodeJS.ProcessEnv;
    home?: string;
    platform?: NodeJS.Platform;
    arch?: string;
    totalMemoryBytes?: number;
    uid?: number;
    nodePath?: string;
    cliPath?: string;
    runner?: CommandRunner;
    findCommand?: (name: string, env: NodeJS.ProcessEnv) => Promise<string | undefined>;
    prompt?: (message: string) => Promise<string>;
    promptSecret?: (message: string) => Promise<string>;
    fetch?: typeof globalThis.fetch;
    gatewayReadyTimeoutMs?: number;
    hermesApiReadyTimeoutMs?: number;
    localProviderReadyTimeoutMs?: number;
    progress?: (message: string) => void;
    providerSessionCheck?: (config: ReturnType<typeof loadConfig>) => Promise<SetupReport["providerSession"]>;
    localProviderProgress?: () => Promise<string | undefined>;
    localEndpointProbe?: (url: string) => Promise<boolean>;
    gatewayEndpointProbe?: (host: string, port: number) => Promise<GatewayEndpointState>;
    readinessCheck?: (config: ReturnType<typeof loadConfig>) => Promise<ReadinessReport>;
}
export declare function parseSetupOptions(args: string[]): SetupOptions;
export declare function runSetup(options: SetupOptions, dependencies?: SetupDependencies): Promise<SetupReport>;
export declare function runSetupCommand(args: string[]): Promise<void>;
export declare function printSetupHelp(): void;
export declare function resolveSetupGatewayPort(input: {
    host: string;
    port: number;
    explicit: boolean;
    probe: (host: string, port: number) => Promise<GatewayEndpointState>;
    progress?: (message: string) => void;
}): Promise<number>;
export declare function resolveSetupLocalVoiceUrl(input: {
    url: string;
    explicit: boolean;
    ownedServiceUrl?: string;
    probe: (url: string) => Promise<boolean>;
    progress?: (message: string) => void;
}): Promise<string>;
//# sourceMappingURL=setup.d.ts.map