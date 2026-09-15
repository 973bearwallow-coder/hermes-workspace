import { withTimeout } from "openclaw/plugin-sdk/time-runtime";
//#region extensions/codex/src/app-server/timeout.ts
/**
* Thin Codex app-server timeout adapter around OpenClaw's shared timeout helper.
*/
function resolveAbortError(signal) {
	return signal.reason instanceof Error ? signal.reason : new Error("Codex app-server operation aborted", { cause: signal.reason });
}
/** Awaits a promise with a Codex-specific timeout error message. */
async function withTimeout$1(promise, timeoutMs, timeoutMessage, createError) {
	return await withTimeout(promise, timeoutMs, {
		message: timeoutMessage,
		...createError ? { createError } : {}
	});
}
/** Bounds an operation by both its owner lifecycle and one total wall-clock budget. */
async function withAbortableTimeout(params) {
	const signal = params.signal;
	if (signal?.aborted) throw resolveAbortError(signal);
	let removeAbortListener;
	const operation = signal ? Promise.race([params.promise, new Promise((_, reject) => {
		const onAbort = () => reject(resolveAbortError(signal));
		signal.addEventListener("abort", onAbort, { once: true });
		removeAbortListener = () => signal.removeEventListener("abort", onAbort);
	})]) : params.promise;
	try {
		return await withTimeout$1(operation, params.timeoutMs, params.timeoutMessage, params.createTimeoutError);
	} finally {
		removeAbortListener?.();
	}
}
//#endregion
export { withTimeout$1 as n, withAbortableTimeout as t };
