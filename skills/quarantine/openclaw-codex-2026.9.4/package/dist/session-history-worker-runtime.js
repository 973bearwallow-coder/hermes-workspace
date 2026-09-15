import { n as codexHistoryRejectionReason } from "./history-rejection-B4nOXNXF.js";
import { n as runCodexHistoryWorkerInput, t as codexHistoryWorkerUrl } from "./session-history.worker-BeK1YOyT.js";
import { n as resolveCodexHistoryTarget } from "./session-history-Cz-tOOYj.js";
import { WorkerTaskPool } from "openclaw/plugin-sdk/process-runtime";
import { isIncognitoSessionKey } from "openclaw/plugin-sdk/session-key-runtime";
import { SessionTranscriptReadFenceError, captureCodexSessionTranscriptReadAdmission, validateCodexSessionTranscriptContextVersion, validateCodexSessionTranscriptReadAdmission } from "openclaw/plugin-sdk/codex-session-transcript-runtime";
//#region extensions/codex/session-history-worker-runtime.ts
const historyReads = new WorkerTaskPool({
	workerUrl: codexHistoryWorkerUrl,
	maxWorkers: 1
});
async function readHistory(target, operation, admission, signal) {
	signal?.throwIfAborted();
	const resolved = resolveCodexHistoryTarget(target, admission);
	const receipt = admission ?? (resolved.kind === "sqlite" ? captureCodexSessionTranscriptReadAdmission(resolved.target) : void 0);
	const input = {
		...operation,
		target: resolved,
		sessionId: target.sessionId,
		...receipt ? { admission: { ...receipt } } : {}
	};
	const result = resolved.kind === "sqlite" && isIncognitoSessionKey(resolved.target.sessionKey) ? await runCodexHistoryWorkerInput(input) : await historyReads.run(input, {
		timeoutMs: 6e4,
		signal
	});
	signal?.throwIfAborted();
	if (resolved.kind === "sqlite") try {
		if (input.admission) validateCodexSessionTranscriptReadAdmission(resolved.target, input.admission);
		else validateCodexSessionTranscriptContextVersion(resolved.target, result.version);
	} catch (error) {
		return {
			...result,
			result: {
				status: "rejected",
				reason: error instanceof SessionTranscriptReadFenceError ? "snapshot_invalidated" : codexHistoryRejectionReason(error)
			}
		};
	}
	return result;
}
async function readCodexHistoryMessagesInWorker(target, admission, signal) {
	const result = await readHistory(target, { kind: "messages" }, admission, signal);
	return result.kind === "messages" && result.result.status === "ok" ? result.result.value : void 0;
}
async function projectCodexSettledHistoryInWorker(target, signal) {
	const result = await readHistory(target, {
		kind: "settled",
		evidence: {
			mirroredMessages: target.mirroredMessages,
			settledMessages: target.settledMessages,
			turnId: target.turnId
		}
	}, void 0, signal);
	return result.kind === "settled" ? result.result : {
		status: "rejected",
		reason: "history_read_failed"
	};
}
//#endregion
export { projectCodexSettledHistoryInWorker, readCodexHistoryMessagesInWorker };
