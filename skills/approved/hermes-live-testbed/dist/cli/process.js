import { spawn } from "node:child_process";
import { constants as fsConstants } from "node:fs";
import { access } from "node:fs/promises";
import { delimiter, join } from "node:path";
const DEFAULT_TIMEOUT_MS = 30_000;
const DEFAULT_MAX_OUTPUT_BYTES = 256 * 1024;
export const runCommand = async (command, args, options = {}) => {
    const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
    const maxOutputBytes = options.maxOutputBytes ?? DEFAULT_MAX_OUTPUT_BYTES;
    return await new Promise((resolve) => {
        const child = spawn(command, args, {
            shell: false,
            stdio: ["ignore", "pipe", "pipe"],
            ...(options.cwd ? { cwd: options.cwd } : {}),
            ...(options.env ? { env: options.env } : {}),
        });
        let stdout = Buffer.alloc(0);
        let stderr = Buffer.alloc(0);
        let timedOut = false;
        let settled = false;
        const append = (current, chunk) => {
            if (current.byteLength >= maxOutputBytes)
                return current;
            const next = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
            return Buffer.concat([current, next.subarray(0, maxOutputBytes - current.byteLength)]);
        };
        child.stdout?.on("data", (chunk) => {
            stdout = append(stdout, chunk);
        });
        child.stderr?.on("data", (chunk) => {
            stderr = append(stderr, chunk);
        });
        const timer = setTimeout(() => {
            timedOut = true;
            child.kill("SIGTERM");
            setTimeout(() => child.kill("SIGKILL"), 1_000).unref();
        }, timeoutMs);
        timer.unref?.();
        const finish = (code, signal) => {
            if (settled)
                return;
            settled = true;
            clearTimeout(timer);
            resolve({
                command,
                args: [...args],
                code,
                ...(signal ? { signal } : {}),
                stdout: stdout.toString("utf8"),
                stderr: stderr.toString("utf8"),
                timedOut,
            });
        };
        child.on("error", (error) => {
            stderr = append(stderr, error.message);
            finish(error.code === "ENOENT" ? 127 : 1);
        });
        child.on("close", (code, signal) => finish(code ?? (signal ? 1 : 0), signal ?? undefined));
    });
};
export async function findExecutable(name, env = process.env) {
    if (name.includes("/") || (process.platform === "win32" && name.includes("\\"))) {
        return await isExecutable(name) ? name : undefined;
    }
    const pathEntries = (env.PATH ?? "").split(delimiter).filter(Boolean);
    const suffixes = process.platform === "win32"
        ? (env.PATHEXT ?? ".EXE;.CMD;.BAT;.COM").split(";")
        : [""];
    for (const directory of pathEntries) {
        for (const suffix of suffixes) {
            const candidate = join(directory, `${name}${suffix}`);
            if (await isExecutable(candidate))
                return candidate;
        }
    }
    return undefined;
}
async function isExecutable(path) {
    try {
        await access(path, process.platform === "win32" ? fsConstants.F_OK : fsConstants.X_OK);
        return true;
    }
    catch {
        return false;
    }
}
//# sourceMappingURL=process.js.map