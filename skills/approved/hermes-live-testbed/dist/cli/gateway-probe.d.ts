export type GatewayEndpointState = "available" | "hermes-live" | "occupied";
export interface GatewayEndpointProbeOptions {
    fetch?: typeof globalThis.fetch;
    tcpProbe?: (host: string, port: number, timeoutMs: number) => Promise<boolean>;
    timeoutMs?: number;
}
export declare function gatewayOrigin(host: string, port: number): string;
export declare function probeGatewayEndpoint(host: string, port: number, options?: GatewayEndpointProbeOptions): Promise<GatewayEndpointState>;
export declare function probeGatewayReadiness(origin: string, options?: {
    authToken?: string;
    fetch?: typeof globalThis.fetch;
    timeoutMs?: number;
}): Promise<{
    ok: true;
} | {
    ok: false;
    error: string;
}>;
export declare function readBoundedGatewayJson(response: Response): Promise<Record<string, unknown>>;
//# sourceMappingURL=gateway-probe.d.ts.map