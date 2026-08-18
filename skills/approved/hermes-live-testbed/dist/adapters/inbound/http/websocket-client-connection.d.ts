import type WebSocket from "ws";
import type { ClientConnectionPort, ClientInboundFrame } from "../../../application/live-gateway/ports/client-connection.port.js";
export declare const MAX_CLIENT_BUFFERED_BYTES: number;
export declare class WebSocketClientConnection implements ClientConnectionPort {
    private readonly socket;
    constructor(socket: WebSocket);
    onMessage(handler: (data: ClientInboundFrame) => void): void;
    onClose(handler: () => void): void;
    onError(handler: (error: unknown) => void): void;
    sendText(payload: string): void;
    close(code: number, reason: string): void;
}
//# sourceMappingURL=websocket-client-connection.d.ts.map