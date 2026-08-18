export const HERMES_LIVE_PROTOCOL_VERSION = 6;
export const HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS = [3, 4, 5, 6];
export const HERMES_LIVE_PROTOCOL_ERROR_CODE = "unsupported_protocol_version";
export function isHermesLiveProtocolVersion(value) {
    return HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS.some((version) => version === value);
}
export function incompatibleProtocolVersionMessage(value) {
    const received = typeof value === "number" && Number.isInteger(value) ? `v${value}` : "an invalid version";
    return (`Hermes Live protocol ${received} is incompatible with supported protocols ` +
        `${HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS.map((version) => `v${version}`).join(", ")}. ` +
        "Upgrade hermes-live-voice before reconnecting.");
}
export function assertHermesLiveProtocolVersion(value) {
    if (!isHermesLiveProtocolVersion(value)) {
        throw new UnsupportedHermesLiveProtocolVersionError(value);
    }
}
export class UnsupportedHermesLiveProtocolVersionError extends Error {
    code = HERMES_LIVE_PROTOCOL_ERROR_CODE;
    expected = HERMES_LIVE_PROTOCOL_VERSION;
    supported = HERMES_LIVE_SUPPORTED_PROTOCOL_VERSIONS;
    received;
    constructor(received) {
        super(incompatibleProtocolVersionMessage(received));
        this.name = "UnsupportedHermesLiveProtocolVersionError";
        this.received = received;
    }
}
//# sourceMappingURL=version.js.map