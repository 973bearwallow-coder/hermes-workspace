import type { HermesCapabilities, HermesRunsPort } from "./ports/hermes-runs.port.js";
export declare const HERMES_TARGETED_APPROVAL_FEATURE: "run_approval_response_by_id";
export interface HermesApprovalCompatibility {
    uiSupported: false;
    interactive: false;
    fallback: "deny_all_then_stop";
    requiredFeature: typeof HERMES_TARGETED_APPROVAL_FEATURE;
    upstreamTargetedResponseAdvertised: boolean;
    negotiated: boolean;
}
export declare function hermesApprovalCompatibility(capabilities: Pick<HermesCapabilities, "features">): HermesApprovalCompatibility;
export declare function unnegotiatedHermesApprovalCompatibility(): HermesApprovalCompatibility;
export declare function negotiateHermesApprovalCompatibility(hermes: Pick<HermesRunsPort, "capabilities">): Promise<HermesApprovalCompatibility>;
//# sourceMappingURL=hermes-approval-compatibility.d.ts.map