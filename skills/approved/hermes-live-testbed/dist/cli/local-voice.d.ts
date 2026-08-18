import type { AppConfig } from "../config.js";
import { type CommandRunner } from "./process.js";
import { type ServiceCommand, type ServiceStatus } from "./service-manager.js";
export declare const HUGGINGFACE_SPEECH_TO_SPEECH_VERSION = "0.2.11";
export declare const MIN_MANAGED_LOCAL_MEMORY_BYTES: number;
export declare const MANAGED_LOCAL_MIN_SILENCE_MS = 700;
export declare const MANAGED_LOCAL_MAX_NEW_TOKENS = 96;
export declare const MANAGED_LOCAL_ENTRYPOINT: string;
export interface LocalVoiceCommand extends ServiceCommand {
}
interface LocalVoiceDependencies {
    env?: NodeJS.ProcessEnv;
    home?: string;
    platform?: NodeJS.Platform;
    arch?: string;
    totalMemoryBytes?: number;
    uid?: number;
    runner?: CommandRunner;
    findCommand?: (name: string, env: NodeJS.ProcessEnv) => Promise<string | undefined>;
    runForeground?: (command: string, args: string[], env: NodeJS.ProcessEnv) => Promise<number>;
    probeEndpoint?: (url: string) => Promise<boolean>;
}
export interface LocalVoiceServiceStatus extends ServiceStatus {
    endpoint: {
        url: string;
        listening: boolean;
    };
}
export declare function runLocalVoiceCommand(args: string[], config: Pick<AppConfig, "local">, dependencies?: LocalVoiceDependencies): Promise<void>;
export declare function probeLocalVoiceEndpoint(url: string, timeoutMs?: number): Promise<boolean>;
export declare function localVoiceStartupProgress(logs: string): string | undefined;
export declare function resolveLocalVoiceCommand(config: Pick<AppConfig, "local">, dependencies?: Pick<LocalVoiceDependencies, "env" | "platform" | "arch" | "totalMemoryBytes" | "findCommand">): Promise<LocalVoiceCommand>;
export declare function buildLocalVoiceCommand(input: {
    uv: string;
    endpoint: string;
    platform: NodeJS.Platform;
    arch: string;
    caBundle?: string;
    runtimeEntrypoint?: string;
}): LocalVoiceCommand;
export declare function printLocalVoiceHelp(): void;
export {};
//# sourceMappingURL=local-voice.d.ts.map