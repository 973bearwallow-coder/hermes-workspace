import { type DoctorOptions, type DoctorReport } from "./doctor.js";
export interface DiagnosticsOptions extends Omit<DoctorOptions, "json"> {
    output?: string;
}
export interface DiagnosticBundle {
    schemaVersion: 1;
    generatedAt: string;
    package: {
        name: string;
        version: string;
    };
    runtime: {
        platform: NodeJS.Platform;
        arch: string;
        node: string;
    };
    doctor: DoctorReport;
}
export declare function parseDiagnosticsOptions(args: readonly string[]): DiagnosticsOptions;
export declare function runDiagnosticsCommand(args: string[]): Promise<void>;
export declare function createDiagnosticBundle(doctor: DoctorReport, options?: {
    generatedAt?: string;
    home?: string;
    secrets?: readonly string[];
}): DiagnosticBundle;
export declare function sanitizeDiagnosticValue(value: unknown, options?: {
    home?: string;
    secrets?: readonly string[];
}): unknown;
export declare function writeDiagnosticBundle(path: string, bundle: DiagnosticBundle): Promise<void>;
export declare function diagnosticsHelp(): string;
//# sourceMappingURL=diagnostics.d.ts.map