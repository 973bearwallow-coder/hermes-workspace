import { t as __exportAll } from "./rolldown-runtime-8H4AJuhK.js";
import { n as withTimeout, t as withAbortableTimeout } from "./timeout-BVw8aaM1.js";
//#region extensions/codex/src/app-server/request.ts
var request_exports = /* @__PURE__ */ __exportAll({
	CodexAppServerScopedRequestRejectedError: () => CodexAppServerScopedRequestRejectedError,
	readCodexAppServerUsage: () => readCodexAppServerUsage,
	requestCodexAppServerClientJson: () => requestCodexAppServerClientJson,
	requestCodexAppServerJson: () => requestCodexAppServerJson,
	withCodexAppServerJsonClient: () => withCodexAppServerJsonClient
});
/** Sends one guarded request over a client lease owned by the caller. */
async function requestCodexAppServerClientJson(params) {
	const { resolveCodexAppServerDirectSandboxBypassBlock } = await import("./sandbox-guard-BxgyoM8M.js").then((n) => n.r);
	const sandboxBlock = resolveCodexAppServerDirectSandboxBypassBlock({
		method: params.method,
		requestParams: params.requestParams,
		config: params.config,
		sessionKey: params.sessionKey,
		sessionId: params.sessionId
	});
	if (sandboxBlock) throw new Error(sandboxBlock);
	const timeoutMs = params.timeoutMs ?? 6e4;
	return await withTimeout(params.client.request(params.method, params.requestParams, {
		timeoutMs,
		signal: params.signal,
		...params.assertCurrent ? { assertCurrent: () => assertRequestOwnerCurrent(params.assertCurrent) } : {}
	}), timeoutMs, `codex app-server ${params.method} timed out`);
}
async function requestCodexAppServerJson(params) {
	const { resolveCodexAppServerDirectSandboxBypassBlock } = await import("./sandbox-guard-BxgyoM8M.js").then((n) => n.r);
	const sandboxBlock = resolveCodexAppServerDirectSandboxBypassBlock({
		method: params.method,
		requestParams: params.requestParams,
		config: params.config,
		sessionKey: params.sessionKey,
		sessionId: params.sessionId
	});
	if (sandboxBlock) throw new Error(sandboxBlock);
	return await withCodexAppServerJsonClient({
		...params,
		timeoutMessage: `codex app-server ${params.method} timed out`
	}, async (request) => await request({
		method: params.method,
		requestParams: params.requestParams
	}));
}
/** A scoped guard rejected the request before a physical write. */
var CodexAppServerScopedRequestRejectedError = class extends Error {
	constructor(message, options) {
		super(message, options);
		this.name = "CodexAppServerScopedRequestRejectedError";
	}
};
function assertRequestOwnerCurrent(assertCurrent) {
	try {
		assertCurrent?.();
	} catch (cause) {
		throw new CodexAppServerScopedRequestRejectedError(cause instanceof Error ? cause.message : String(cause), { cause });
	}
}
const CODEX_USAGE_ISOLATED_SHUTDOWN = {
	forceKillDelayMs: 200,
	exitTimeoutMs: 300
};
const CODEX_ACCOUNT_READ_MAX_TIMEOUT_MS = 4e3;
const CODEX_USAGE_DEADLINE_RESERVE_MS = CODEX_USAGE_ISOLATED_SHUTDOWN.forceKillDelayMs + CODEX_USAGE_ISOLATED_SHUTDOWN.exitTimeoutMs + 250;
/** Reads rate limits and best-effort account identity from one isolated app-server session. */
async function readCodexAppServerUsage(options) {
	const deadline = Date.now() + options.timeoutMs;
	return await withCodexAppServerJsonClient({
		timeoutMs: options.timeoutMs,
		timeoutMessage: "codex app-server usage read timed out",
		agentDir: options.agentDir,
		...options.authProfileId ? { authProfileId: options.authProfileId } : {},
		config: options.config,
		startOptions: options.startOptions,
		isolated: true,
		isolatedShutdown: CODEX_USAGE_ISOLATED_SHUTDOWN
	}, async (request) => {
		const rateLimits = await request({ method: "account/rateLimits/read" });
		const accountEmail = await readCodexAccountEmailBestEffort(request, deadline);
		return {
			rateLimits,
			...accountEmail ? { accountEmail } : {}
		};
	});
}
function extractCodexAccountEmail(value) {
	if (!value || typeof value !== "object") return;
	const record = value;
	const account = record.account && typeof record.account === "object" ? record.account : record;
	const email = account.email ?? account.accountEmail;
	return typeof email === "string" && email.trim() ? email.trim() : void 0;
}
async function readCodexAccountEmailBestEffort(request, deadline) {
	const boundMs = Math.min(CODEX_ACCOUNT_READ_MAX_TIMEOUT_MS, deadline - Date.now() - CODEX_USAGE_DEADLINE_RESERVE_MS);
	if (boundMs <= 0) return;
	const read = request({
		method: "account/read",
		requestParams: {}
	}).then((account) => extractCodexAccountEmail(account), () => void 0);
	let timer;
	const timeout = new Promise((resolve) => {
		timer = setTimeout(() => resolve(void 0), boundMs);
		timer.unref?.();
	});
	try {
		return await Promise.race([read, timeout]);
	} finally {
		if (timer) clearTimeout(timer);
	}
}
/**
* Runs several guarded requests over one acquired client (shared lease or
* isolated child) so related reads see the same app-server session. The whole
* callback re-runs once when the client's start selection changed underneath it.
*/
async function withCodexAppServerJsonClient(params, run) {
	const timeoutMs = params.timeoutMs ?? 6e4;
	const timeoutMessage = params.timeoutMessage ?? "codex app-server request timed out";
	const timeoutController = new AbortController();
	const deadline = Number.isFinite(timeoutMs) && timeoutMs > 0 ? Date.now() + timeoutMs : void 0;
	const isPastDeadline = () => deadline !== void 0 && Date.now() >= deadline;
	const throwIfAbandoned = () => {
		if (timeoutController.signal.aborted && timeoutController.signal.reason instanceof Error) throw timeoutController.signal.reason;
		if (timeoutController.signal.aborted || isPastDeadline()) throw new CodexAppServerScopedRequestRejectedError(timeoutMessage);
	};
	const remainingTimeoutMs = () => {
		throwIfAbandoned();
		return deadline === void 0 ? timeoutMs : Math.max(1, deadline - Date.now());
	};
	try {
		return await withAbortableTimeout({
			signal: timeoutController.signal,
			timeoutMs,
			timeoutMessage,
			promise: (async () => {
				const { resolveCodexAppServerDirectSandboxBypassBlock } = await import("./sandbox-guard-BxgyoM8M.js").then((n) => n.r);
				const { createIsolatedCodexAppServerClient, getLeasedSharedCodexAppServerClient, isCodexAppServerStartSelectionChangedError, releaseLeasedSharedCodexAppServerClient, retireSharedCodexAppServerClientIfCurrent } = await import("./shared-client-CscigXXL.js").then((n) => n.y);
				for (let attempt = 0; attempt < 2; attempt += 1) {
					throwIfAbandoned();
					const client = await (params.isolated ? createIsolatedCodexAppServerClient : getLeasedSharedCodexAppServerClient)({
						startOptions: params.startOptions,
						pluginConfig: params.pluginConfig,
						timeoutMs: remainingTimeoutMs(),
						authProfileId: params.authProfileId,
						authProfileStore: params.authProfileStore,
						authBindingFingerprint: params.authBindingFingerprint,
						preparedAuth: params.preparedAuth,
						authRequirement: params.authRequirement,
						agentDir: params.agentDir,
						config: params.config,
						abandonSignal: timeoutController.signal
					});
					let scopeActive = true;
					const assertCurrent = () => {
						throwIfAbandoned();
						if (!scopeActive) throw new CodexAppServerScopedRequestRejectedError("Codex app-server request scope is closed");
						assertRequestOwnerCurrent(params.assertCurrent);
					};
					try {
						assertCurrent();
						const scopedRequest = async (request) => {
							const sandboxBlock = resolveCodexAppServerDirectSandboxBypassBlock({
								method: request.method,
								requestParams: request.requestParams,
								config: params.config,
								sessionKey: params.sessionKey,
								sessionId: params.sessionId
							});
							if (sandboxBlock) throw new CodexAppServerScopedRequestRejectedError(sandboxBlock);
							assertCurrent();
							return await client.request(request.method, request.requestParams, {
								timeoutMs: remainingTimeoutMs(),
								signal: timeoutController.signal,
								assertCurrent: () => {
									assertCurrent();
									request.assertCurrent?.();
								}
							});
						};
						return await run(scopedRequest, client, {
							assertCurrent,
							abort: (reason) => {
								if (scopeActive) timeoutController.abort(reason);
							}
						});
					} catch (error) {
						if (!isCodexAppServerStartSelectionChangedError(error) || attempt > 0) throw error;
						if (!params.isolated) retireSharedCodexAppServerClientIfCurrent(client);
						throwIfAbandoned();
					} finally {
						scopeActive = false;
						if (params.isolated) await client.closeAndWait({
							exitTimeoutMs: params.isolatedShutdown?.exitTimeoutMs ?? 2e3,
							forceKillDelayMs: params.isolatedShutdown?.forceKillDelayMs ?? 250
						});
						else releaseLeasedSharedCodexAppServerClient(client);
					}
				}
				throw new Error("Codex app-server selection retry loop exited unexpectedly");
			})()
		});
	} catch (error) {
		if (isPastDeadline()) throw new Error(timeoutMessage, { cause: error });
		throw error;
	} finally {
		timeoutController.abort(new CodexAppServerScopedRequestRejectedError(timeoutMessage));
	}
}
//#endregion
export { request_exports as a, requestCodexAppServerJson as i, readCodexAppServerUsage as n, withCodexAppServerJsonClient as o, requestCodexAppServerClientJson as r, CodexAppServerScopedRequestRejectedError as t };
