import { asOptionalRecord } from "openclaw/plugin-sdk/string-coerce-runtime";
import { createHash } from "node:crypto";
//#region extensions/codex/src/app-server/native-subagent-history-owner.ts
function codexNativeSubagentHistoryConnectionFingerprint(binding) {
	if (!binding.appServerRuntimeFingerprint) return;
	return createHash("sha256").update(JSON.stringify([
		binding.appServerRuntimeFingerprint,
		binding.connectionScope ?? null,
		binding.authProfileId ?? null
	])).digest("hex");
}
function createCodexNativeSubagentHistoryOwner(params) {
	const connectionFingerprint = codexNativeSubagentHistoryConnectionFingerprint(params.binding);
	return connectionFingerprint ? {
		parentThreadId: params.parentThreadId,
		sessionId: params.sessionId,
		...params.lifecycleRevision ? { lifecycleRevision: params.lifecycleRevision } : {},
		connectionFingerprint
	} : void 0;
}
function readCodexNativeSubagentHistoryOwner(detail) {
	const value = asOptionalRecord(detail)?.nativeHistory;
	if (value === void 0) return;
	const owner = asOptionalRecord(value);
	if (typeof owner?.parentThreadId !== "string" || !owner.parentThreadId.trim() || typeof owner.sessionId !== "string" || !owner.sessionId.trim() || owner.lifecycleRevision !== void 0 && (typeof owner.lifecycleRevision !== "string" || !owner.lifecycleRevision.trim()) || typeof owner.connectionFingerprint !== "string" || !/^[a-f0-9]{64}$/u.test(owner.connectionFingerprint)) throw new Error("Subagent history owner is invalid.");
	return {
		parentThreadId: owner.parentThreadId,
		sessionId: owner.sessionId,
		...typeof owner.lifecycleRevision === "string" ? { lifecycleRevision: owner.lifecycleRevision } : {},
		connectionFingerprint: owner.connectionFingerprint
	};
}
//#endregion
export { createCodexNativeSubagentHistoryOwner as n, readCodexNativeSubagentHistoryOwner as r, codexNativeSubagentHistoryConnectionFingerprint as t };
