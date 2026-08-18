export interface CommandResult {
    command: string;
    args: string[];
    code: number;
    signal?: NodeJS.Signals;
    stdout: string;
    stderr: string;
    timedOut: boolean;
}
export interface RunCommandOptions {
    cwd?: string;
    env?: NodeJS.ProcessEnv;
    timeoutMs?: number;
    maxOutputBytes?: number;
}
export type CommandRunner = (command: string, args: string[], options?: RunCommandOptions) => Promise<CommandResult>;
export declare const runCommand: CommandRunner;
export declare function findExecutable(name: string, env?: NodeJS.ProcessEnv): Promise<string | undefined>;
//# sourceMappingURL=process.d.ts.map