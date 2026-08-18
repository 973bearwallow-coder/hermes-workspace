import { type CommandResult, type CommandRunner } from "./process.js";
export declare const SERVICE_LABEL = "dev.hermes-live-voice.gateway";
export declare const LOCAL_VOICE_SERVICE_LABEL = "dev.hermes-live-voice.local";
export type ServicePlatform = "launchd" | "systemd" | "unsupported";
export type ServiceAction = "install" | "uninstall" | "start" | "stop" | "restart" | "status" | "logs";
export type ServiceKind = "gateway" | "local-voice";
export interface ServiceCommand {
    command: string;
    args: string[];
    environment?: Record<string, string>;
}
export interface ServiceManagerOptions {
    kind?: ServiceKind;
    command?: ServiceCommand;
    home?: string;
    platform?: NodeJS.Platform;
    nodePath?: string;
    cliPath?: string;
    configPath?: string;
    uid?: number;
    runner?: CommandRunner;
}
export interface ServiceStatus {
    platform: ServicePlatform;
    definitionPath?: string;
    installed: boolean;
    running: boolean;
    detail: string;
}
export declare function runServiceAction(action: ServiceAction, options?: ServiceManagerOptions): Promise<ServiceStatus | CommandResult>;
export declare function serviceStatus(options?: ServiceManagerOptions): Promise<ServiceStatus>;
export declare function resolveServicePlatform(platform?: NodeJS.Platform): ServicePlatform;
export declare function launchdServiceDefinition(options?: ServiceManagerOptions): string;
export declare function systemdServiceDefinition(options?: ServiceManagerOptions): string;
//# sourceMappingURL=service-manager.d.ts.map