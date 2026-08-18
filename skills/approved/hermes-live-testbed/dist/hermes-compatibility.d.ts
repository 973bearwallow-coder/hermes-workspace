export declare const HERMES_COMPATIBILITY: {
    readonly minimumVersion: "0.18.2";
    readonly testedVersion: "0.20.0";
    readonly testedReleaseTag: "v2026.8.3";
    readonly testedImage: "nousresearch/hermes-agent:v2026.8.3@sha256:16788311e2fa3035456bdc1bafb8ec2b1777db64ebf020af9bb7eb73c3712c9e";
};
export type HermesVersionStatus = "unsupported" | "supported" | "tested" | "newer" | "unknown";
export declare function parseHermesVersion(output: string): string | undefined;
export declare function classifyHermesVersion(version: string | undefined): HermesVersionStatus;
//# sourceMappingURL=hermes-compatibility.d.ts.map