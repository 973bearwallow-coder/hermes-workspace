const LEVELS = {
    debug: 10,
    info: 20,
    warn: 30,
    error: 40,
};
export function createLogger(level = "info") {
    const threshold = LEVELS[level] ?? LEVELS.info;
    const write = (entryLevel, message, data) => {
        if (LEVELS[entryLevel] < threshold) {
            return;
        }
        const payload = {
            level: entryLevel,
            message,
            time: new Date().toISOString(),
            ...(data === undefined ? {} : { data }),
        };
        const line = JSON.stringify(payload);
        if (entryLevel === "error") {
            console.error(line);
        }
        else if (entryLevel === "warn") {
            console.warn(line);
        }
        else {
            console.log(line);
        }
    };
    return {
        debug: (message, data) => write("debug", message, data),
        info: (message, data) => write("info", message, data),
        warn: (message, data) => write("warn", message, data),
        error: (message, data) => write("error", message, data),
    };
}
//# sourceMappingURL=logger.js.map