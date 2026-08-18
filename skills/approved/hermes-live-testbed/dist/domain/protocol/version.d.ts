export declare const HERMES_LIVE_PROTOCOL_VERSION: 6;
export declare const HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS: readonly [3, 4, 5, 6];
export type HermesLiveProtocolVersion = (typeof HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS)[number];
export declare const HERMES_LIVE_PROTOCOL_ERROR_CODE: "unsupported_protocol_version";
export declare function isHermesLiveProtocolVersion(value: unknown): value is HermesLiveProtocolVersion;
export declare function incompatibleProtocolVersionMessage(value: unknown): string;
export declare function assertHermesLiveProtocolVersion(value: unknown): asserts value is HermesLiveProtocolVersion;
export declare class UnsupportedHermesLiveProtocolVersionError extends Error {
    readonly code: "unsupported_protocol_version";
    readonly expected: 6;
    readonly supported: readonly [3, 4, 5, 6];
    readonly received: unknown;
    constructor(received: unknown);
}
//# sourceMappingURL=version.d.ts.map