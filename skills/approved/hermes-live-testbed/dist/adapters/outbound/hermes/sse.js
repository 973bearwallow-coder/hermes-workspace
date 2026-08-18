export const MAX_SSE_EVENT_BYTES = 1_000_000;
export function parseSseEventBlock(block) {
    assertSseEventSize(block);
    const dataLines = [];
    let eventName;
    for (const line of block.split(/\r?\n/)) {
        if (!line || line.startsWith(":")) {
            continue;
        }
        if (line.startsWith("event:")) {
            eventName = line.slice(6).trimStart();
            continue;
        }
        if (line.startsWith("data:")) {
            dataLines.push(line.slice(5).trimStart());
        }
    }
    if (dataLines.length === 0) {
        return null;
    }
    const payload = dataLines.join("\n");
    try {
        const parsed = JSON.parse(payload);
        if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
            return eventName && typeof parsed.event !== "string"
                ? { event: eventName, ...parsed }
                : parsed;
        }
        return { event: eventName ?? "hermes.raw", data: parsed };
    }
    catch {
        return { event: eventName ?? "hermes.raw", data: payload };
    }
}
export async function* parseSseStream(stream, options = {}) {
    const reader = stream.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let reachedEof = false;
    try {
        while (true) {
            const { value, done } = await readSseChunk(reader, options);
            if (done) {
                reachedEof = true;
                break;
            }
            buffer += decoder.decode(value, { stream: true });
            let boundary = findBoundary(buffer);
            while (boundary >= 0) {
                const block = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + delimiterLength(buffer, boundary));
                const event = parseSseEventBlock(block);
                if (event) {
                    yield event;
                }
                boundary = findBoundary(buffer);
            }
            assertSseEventSize(buffer);
        }
        buffer += decoder.decode();
        if (buffer.trim()) {
            assertSseEventSize(buffer);
            const event = parseSseEventBlock(buffer);
            if (event) {
                yield event;
            }
        }
    }
    finally {
        if (!reachedEof) {
            await reader.cancel().catch(() => undefined);
        }
        reader.releaseLock();
    }
}
async function readSseChunk(reader, options) {
    const timeoutMs = options.idleTimeoutMs;
    if (timeoutMs === undefined || timeoutMs <= 0) {
        return await reader.read();
    }
    let timeout;
    try {
        return await Promise.race([
            readUntilActivity(reader),
            new Promise((_resolve, reject) => {
                timeout = setTimeout(() => {
                    try {
                        options.onIdle?.();
                    }
                    catch {
                        // The timeout remains authoritative even if transport cleanup fails.
                    }
                    reject(new Error(options.idleTimeoutMessage ?? `SSE stream was idle for ${timeoutMs}ms.`));
                }, timeoutMs);
                timeout.unref?.();
            }),
        ]);
    }
    finally {
        if (timeout)
            clearTimeout(timeout);
    }
}
async function readUntilActivity(reader) {
    while (true) {
        const result = await reader.read();
        if (result.done || result.value.byteLength > 0)
            return result;
    }
}
function assertSseEventSize(value) {
    if (Buffer.byteLength(value, "utf8") > MAX_SSE_EVENT_BYTES) {
        throw new Error(`Hermes SSE event exceeded the ${MAX_SSE_EVENT_BYTES}-byte safety limit.`);
    }
}
function findBoundary(value) {
    const lf = value.indexOf("\n\n");
    const crlf = value.indexOf("\r\n\r\n");
    if (lf === -1) {
        return crlf;
    }
    if (crlf === -1) {
        return lf;
    }
    return Math.min(lf, crlf);
}
function delimiterLength(value, boundary) {
    return value.startsWith("\r\n\r\n", boundary) ? 4 : 2;
}
//# sourceMappingURL=sse.js.map