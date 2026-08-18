// Keep enough headroom for multiple default-sized audio frames, but never let a
// stalled client turn provider output into an unbounded process-level buffer.
export const MAX_CLIENT_BUFFERED_BYTES = 8 * 1024 * 1024;
export class WebSocketClientConnection {
    socket;
    constructor(socket) {
        this.socket = socket;
    }
    onMessage(handler) {
        this.socket.on("message", (data) => handler(normalizeWebSocketFrame(data)));
    }
    onClose(handler) {
        this.socket.on("close", handler);
    }
    onError(handler) {
        this.socket.on("error", handler);
    }
    sendText(payload) {
        if (this.socket.readyState !== this.socket.OPEN) {
            return;
        }
        const payloadBytes = Buffer.byteLength(payload, "utf8");
        if (this.socket.bufferedAmount + payloadBytes > MAX_CLIENT_BUFFERED_BYTES) {
            this.socket.terminate();
            return;
        }
        try {
            this.socket.send(payload);
        }
        catch {
            // The socket can leave OPEN between the readyState check and send(). A
            // hard close is safe here and ensures the session observes termination.
            this.socket.terminate();
        }
    }
    close(code, reason) {
        if (this.socket.readyState === this.socket.OPEN) {
            this.socket.close(code, reason);
        }
        else if (this.socket.readyState === this.socket.CONNECTING) {
            this.socket.once("open", () => this.socket.close(code, reason));
        }
    }
}
function normalizeWebSocketFrame(data) {
    if (typeof data === "string") {
        return data;
    }
    if (Buffer.isBuffer(data)) {
        return data;
    }
    if (data instanceof ArrayBuffer) {
        return new Uint8Array(data);
    }
    return Buffer.concat(data);
}
//# sourceMappingURL=websocket-client-connection.js.map