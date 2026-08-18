export interface Logger {
    debug(message: string, data?: unknown): void;
    info(message: string, data?: unknown): void;
    warn(message: string, data?: unknown): void;
    error(message: string, data?: unknown): void;
}
type LogLevel = "debug" | "info" | "warn" | "error";
export declare function createLogger(level?: LogLevel): Logger;
export {};
//# sourceMappingURL=logger.d.ts.map