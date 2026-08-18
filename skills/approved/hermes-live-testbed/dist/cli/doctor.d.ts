import { type ReadinessReport } from "../readiness.js";
import { type CommandRunner } from "./process.js";
import { type ServiceStatus } from "./service-manager.js";
import { HERMES_COMPATIBILITY } from "../hermes-compatibility.js";
export type DiagnosticStatus = "pass" | "warn" | "fail";
export interface DiagnosticCheck {
    id: string;
    label: string;
    status: DiagnosticStatus;
    detail: string;
    fix?: string;
}
export interface DoctorReport {
    ok: boolean;
    version: string;
    compatibility: typeof HERMES_COMPATIBILITY;
    checks: DiagnosticCheck[];
    readiness?: ReadinessReport;
    service?: ServiceStatus;
    localService?: ServiceStatus;
}
export interface DoctorOptions {
    json: boolean;
    providerSmoke: boolean;
    configPath?: string;
    pluginsDir?: string;
    hermesCommand?: string;
}
export interface DoctorDependencies {
    env?: NodeJS.ProcessEnv;
    home?: string;
    platform?: NodeJS.Platform;
    arch?: string;
    uid?: number;
    nodeVersion?: string;
    totalMemoryBytes?: number;
    runner?: CommandRunner;
    findCommand?: (name: string, env: NodeJS.ProcessEnv) => Promise<string | undefined>;
    probeLocalEndpoint?: (url: string) => Promise<boolean>;
    fetch?: typeof globalThis.fetch;
}
export declare function parseDoctorOptions(args: string[]): DoctorOptions;
export declare function runDoctor(options: DoctorOptions, dependencies?: DoctorDependencies): Promise<DoctorReport>;
export declare function diagnoseManagedLocalMemory(totalMemoryBytes: number, memoryPressureOutput?: string, swapUsageOutput?: string): DiagnosticCheck;
export declare function runDoctorCommand(args: string[]): Promise<void>;
export declare function printDoctorHelp(): void;
//# sourceMappingURL=doctor.d.ts.map