import type { HermesRunEvent } from "../../../domain/protocol/server-protocol.js";
export declare const MAX_SSE_EVENT_BYTES = 1000000;
export interface SseStreamOptions {
    idleTimeoutMs?: number;
    idleTimeoutMessage?: string;
    onIdle?: () => void;
}
export declare function parseSseEventBlock(block: string): HermesRunEvent | null;
export declare function parseSseStream(stream: ReadableStream<Uint8Array>, options?: SseStreamOptions): AsyncGenerator<HermesRunEvent>;
//# sourceMappingURL=sse.d.ts.map