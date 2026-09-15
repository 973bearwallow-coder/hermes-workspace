import { r as readCodexAppServerConfigOptions } from "./launch-args-RXQwn8zV.js";
import { C as readCodexErrorNotification, E as createCodexElicitationResponse, b as assertCodexThreadStartResponse, x as assertCodexTurnStartResponse } from "./client-B57KWPQx.js";
import "./config-oIORaQ5T.js";
import { n as resolveCodexAppServerRuntimeOptions } from "./config-runtime-D0zGNIHu.js";
import { u as isCodexAppServerStartSelectionChangedError } from "./shared-client-CscigXXL.js";
import { a as closeCodexStartupClientBestEffort, o as interruptCodexTurnAndWaitBestEffort, t as CODEX_APP_SERVER_INTERRUPT_TIMEOUT_MS } from "./attempt-client-cleanup-DKHzbwt5.js";
import { t as CodexEphemeralTurn } from "./ephemeral-turn-D78_VmzO.js";
import { r as readModelListResult } from "./models-PCKOim-h.js";
import { Et as mergeCodexThreadConfigs, K as attestCodexRestrictedToolSurfaceMcpServersDisabled, _ as assertCodexManagedRequirementsDoNotOverrideToolPolicy, v as buildCodexRingZeroThreadConfigPatch, x as readCodexInheritedMcpServerNames, y as buildCodexRuntimeThreadConfig } from "./thread-lifecycle-DXl1-I6b.js";
import { resolveTimerTimeoutMs } from "openclaw/plugin-sdk/number-runtime";
import path from "node:path";
import fs from "node:fs/promises";
import { resolvePreferredOpenClawTmpDir, withTempWorkspace } from "openclaw/plugin-sdk/temp-path";
//#region extensions/codex/src/app-server/bounded-turn.ts
const CODEX_APP_SERVER_ARGS_ENV_KEY = "OPENCLAW_CODEX_APP_SERVER_ARGS";
const CODEX_BOUNDED_THREAD_CONFIG = {
	"agents.enabled": false,
	"features.multi_agent": false,
	"features.multi_agent_v2": false,
	"features.apps": false,
	"features.plugins": false,
	"features.image_generation": false,
	"features.standalone_web_search": false,
	web_search: "disabled"
};
const CODEX_PRIVATE_BOUNDED_THREAD_CONFIG = {
	"features.hooks": false,
	notify: []
};
const CODEX_SETTLED_FINALIZER_THREAD_CONFIG = {
	"skills.include_instructions": false,
	include_environment_context: false
};
var CodexBoundedTurnTimeoutError = class extends Error {
	constructor(taskLabel, timeoutMs) {
		const bound = timeoutMs % 1e3 === 0 ? `${timeoutMs / 1e3}s` : `${timeoutMs}ms`;
		super(`codex app-server ${taskLabel} turn timed out after ${bound}`);
		this.name = "TimeoutError";
	}
};
async function runBoundedCodexAppServerTurn(params) {
	params.assertCurrent?.();
	const appServer = resolveCodexAppServerRuntimeOptions({
		pluginConfig: params.options.pluginConfig,
		managedCommandOrder: params.isolation === "private-stdio" ? "package-first" : void 0
	});
	if (params.isolation === "configured-transport") return await runBoundedCodexAppServerTurnInWorkspace(params, appServer, { cwd: params.agentDir?.trim() || process.cwd() });
	if (appServer.start.transport !== "stdio") throw new Error("Bounded Codex turns require stdio transport so native tools can be isolated.");
	return await withTempWorkspace({
		rootDir: resolvePreferredOpenClawTmpDir(),
		prefix: "codex-bounded-turn-"
	}, async (workspace) => {
		const codexHome = path.join(workspace.dir, "codex-home");
		const cwd = path.join(workspace.dir, "workspace");
		await Promise.all([fs.mkdir(codexHome, { recursive: true }), fs.mkdir(cwd, { recursive: true })]);
		return await runBoundedCodexAppServerTurnInWorkspace(params, appServer, {
			codexHome,
			cwd
		});
	});
}
async function runBoundedCodexAppServerTurnInWorkspace(params, appServer, workspace, selectionAttempt = 0, timing) {
	const totalTimeoutMs = timing?.timeoutMs ?? resolveTimerTimeoutMs(params.timeoutMs, 100, 100);
	const timeoutError = new CodexBoundedTurnTimeoutError(params.taskLabel, totalTimeoutMs);
	const deadline = timing?.deadline ?? performance.now() + totalTimeoutMs;
	const timeoutMs = deadline - performance.now();
	if (timeoutMs <= 0) throw timeoutError;
	params.assertCurrent?.();
	const agentDir = params.agentDir?.trim() || void 0;
	const startOptions = workspace.codexHome ? buildPrivateCodexAppServerStartOptions(appServer.start, workspace.codexHome) : appServer.start;
	const ownsClient = !params.options.clientFactory;
	const clientOptions = {
		startOptions,
		...params.preparedAuth ? { preparedAuth: params.preparedAuth } : { authProfileId: params.profile },
		authRequirement: params.authRequirement,
		agentDir,
		config: params.config,
		timeoutMs,
		assertCurrent: params.assertCurrent,
		...params.signal ? { abandonSignal: params.signal } : {}
	};
	const client = params.options.clientFactory ? await params.options.clientFactory(clientOptions) : await import("./shared-client-CscigXXL.js").then((n) => n.y).then(({ createIsolatedCodexAppServerClient }) => createIsolatedCodexAppServerClient({
		...clientOptions,
		authProfileStore: params.authProfileStore
	}));
	const abortController = new AbortController();
	let activeThreadId;
	let activeTurnId = "";
	let interruptPromise;
	const requestInterrupt = () => {
		if (!activeThreadId || interruptPromise) return;
		interruptPromise = interruptCodexTurnAndWaitBestEffort(client, {
			threadId: activeThreadId,
			turnId: activeTurnId,
			timeoutMs: CODEX_APP_SERVER_INTERRUPT_TIMEOUT_MS
		});
	};
	const abortRun = (reason) => {
		abortController.abort(reason);
		requestInterrupt();
	};
	const abortFromCaller = () => abortRun(params.signal?.reason ?? "aborted");
	if (params.signal?.aborted) abortFromCaller();
	else params.signal?.addEventListener("abort", abortFromCaller, { once: true });
	const remainingRunMs = deadline - performance.now();
	if (remainingRunMs <= 0) abortRun(timeoutError);
	const timeout = setTimeout(() => abortRun(timeoutError), Math.max(1, remainingRunMs));
	timeout.unref?.();
	let retrySelection = false;
	const requestOptions = {
		timeoutMs,
		signal: abortController.signal,
		assertCurrent: params.assertCurrent
	};
	try {
		params.assertCurrent?.();
		const modelSelection = await resolveCodexBoundedTurnModel({
			client,
			selection: params.model,
			requiredModalities: params.requiredModalities,
			...requestOptions
		});
		const inheritedMcpServerNames = params.requireNoExternalCapabilities ? await readCodexInheritedMcpServerNames(client, workspace.cwd, abortController.signal) : [];
		if (params.requireNoExternalCapabilities) await assertCodexManagedRequirementsDoNotOverrideToolPolicy(client, { restrictedToolSurface: true }, abortController.signal);
		const threadConfig = buildCodexRuntimeThreadConfig(resolveBoundedThreadConfig(params, workspace, inheritedMcpServerNames), { nativeCodeModeEnabled: false });
		params.assertCurrent?.();
		const thread = assertCodexThreadStartResponse(await client.request("thread/start", {
			model: modelSelection.runtimeModelId,
			...params.modelProvider ? { modelProvider: params.modelProvider } : {},
			cwd: workspace.cwd,
			approvalPolicy: "on-request",
			sandbox: "read-only",
			serviceName: "OpenClaw",
			...params.requireNoExternalCapabilities ? { baseInstructions: "" } : {},
			developerInstructions: params.developerInstructions,
			config: threadConfig,
			environments: [],
			dynamicTools: [],
			experimentalRawEvents: true,
			ephemeral: true
		}, requestOptions));
		activeThreadId = thread.thread.id;
		if (abortController.signal.aborted) requestInterrupt();
		if (params.requireNoExternalCapabilities) await attestCodexRestrictedToolSurfaceMcpServersDisabled(client, thread.thread.id, threadConfig, abortController.signal);
		if (params.historyItems?.length) await client.request("thread/inject_items", {
			threadId: thread.thread.id,
			items: params.historyItems
		}, requestOptions);
		params.assertCurrent?.();
		const collector = new CodexEphemeralTurn(client, thread.thread.id, {
			textMode: "all",
			onRequest: createCodexBoundedApprovalHandler(params.taskLabel)
		});
		try {
			const turn = assertCodexTurnStartResponse(await client.request("turn/start", {
				threadId: thread.thread.id,
				input: params.input,
				approvalPolicy: "on-request",
				effort: "low"
			}, requestOptions));
			activeTurnId = turn.turn.id;
			if (abortController.signal.aborted) requestInterrupt();
			const result = await collector.wait(turn.turn, {
				signal: abortController.signal,
				abortError: () => resolveCodexBoundedTurnAbortError(abortController.signal, params.taskLabel, timeoutError)
			});
			if (result.error || result.turn?.status === "failed") throw new Error((result.error ? readCodexErrorNotification(result.error)?.error.message : result.turn?.error?.message) ?? `codex app-server ${params.taskLabel} turn failed`);
			if (result.turn?.status !== "completed") throw new Error(`codex app-server ${params.taskLabel} turn ended with status ${result.turn?.status ?? "unknown"}`);
			if (!result.text && !params.allowEmptyText) throw new Error(`Codex app-server ${params.taskLabel} turn returned no text.`);
			params.assertCurrent?.();
			return {
				text: result.text,
				items: result.items,
				usage: result.usage,
				model: modelSelection.catalogId,
				nativeSelection: {
					model: thread.model,
					modelProvider: thread.modelProvider
				}
			};
		} finally {
			await interruptPromise;
			collector.route.release();
		}
	} catch (error) {
		if (abortController.signal.aborted) throw resolveCodexBoundedTurnAbortError(abortController.signal, params.taskLabel, timeoutError);
		if (ownsClient && isCodexAppServerStartSelectionChangedError(error) && selectionAttempt === 0) retrySelection = true;
		else throw error;
	} finally {
		clearTimeout(timeout);
		params.signal?.removeEventListener("abort", abortFromCaller);
		await interruptPromise;
		if (ownsClient) await closeCodexStartupClientBestEffort(client);
	}
	if (retrySelection) return await runBoundedCodexAppServerTurnInWorkspace(params, appServer, workspace, selectionAttempt + 1, {
		deadline,
		timeoutMs: totalTimeoutMs
	});
	throw new Error("Codex bounded turn selection retry exited unexpectedly");
}
function resolveBoundedThreadConfig(params, workspace, inheritedMcpServerNames) {
	const boundedConfig = mergeCodexThreadConfigs(CODEX_BOUNDED_THREAD_CONFIG, params.threadConfig) ?? CODEX_BOUNDED_THREAD_CONFIG;
	const privateConfig = workspace.codexHome ? mergeCodexThreadConfigs(boundedConfig, CODEX_PRIVATE_BOUNDED_THREAD_CONFIG) ?? boundedConfig : boundedConfig;
	if (!params.requireNoExternalCapabilities) return privateConfig;
	return mergeCodexThreadConfigs(privateConfig, CODEX_SETTLED_FINALIZER_THREAD_CONFIG, buildCodexRingZeroThreadConfigPatch({ toolsAllow: ["openclaw"] }, true, inheritedMcpServerNames)) ?? privateConfig;
}
function buildPrivateCodexAppServerStartOptions(start, codexHome) {
	const providerArgs = readCodexAppServerConfigOptions(start.args).flatMap(({ name, value }) => (name === "-c" || name === "--config") && value && /^\s*(?:openai_base_url|model_catalog_json)\s*=/u.test(value) ? ["-c", value] : []);
	const privateEnv = Object.fromEntries(Object.entries(start.env ?? {}).filter(([name]) => name.trim().toUpperCase() !== CODEX_APP_SERVER_ARGS_ENV_KEY));
	const clearEnv = (start.clearEnv ?? []).filter((name) => {
		const normalized = name.trim().toUpperCase();
		return normalized !== "CODEX_HOME" && normalized !== CODEX_APP_SERVER_ARGS_ENV_KEY;
	});
	return {
		...start,
		homeScope: "agent",
		args: [
			"app-server",
			...providerArgs,
			"--listen",
			"stdio://"
		],
		env: {
			...privateEnv,
			CODEX_HOME: codexHome
		},
		clearEnv: [...clearEnv, CODEX_APP_SERVER_ARGS_ENV_KEY]
	};
}
function createCodexBoundedApprovalHandler(taskLabel) {
	return (request) => {
		if (request.method === "item/commandExecution/requestApproval" || request.method === "item/fileChange/requestApproval") return {
			decision: "decline",
			reason: `OpenClaw Codex ${taskLabel} does not grant tool or file approvals.`
		};
		if (request.method === "item/permissions/requestApproval") return {
			permissions: {},
			scope: "turn"
		};
		if (request.method.includes("requestApproval")) return {
			decision: "decline",
			reason: `OpenClaw Codex ${taskLabel} does not grant native approvals.`
		};
		if (request.method === "mcpServer/elicitation/request") return createCodexElicitationResponse("decline", null, { message: `OpenClaw Codex ${taskLabel} does not support interactive input.` });
	};
}
async function resolveCodexBoundedTurnModel(params) {
	const result = await params.client.request("model/list", {
		limit: null,
		cursor: null,
		includeHidden: params.selection.mode === "required"
	}, {
		timeoutMs: Math.min(params.timeoutMs, 5e3),
		signal: params.signal,
		assertCurrent: params.assertCurrent
	});
	const listed = readModelListResult(result).models;
	if (params.selection.mode === "live-default") {
		const supported = listed.filter((entry) => params.requiredModalities.every((modality) => entry.inputModalities.includes(modality)));
		const selected = supported.find((entry) => entry.isDefault) ?? supported[0];
		if (!selected) throw new Error(`Codex app-server has no model supporting ${params.requiredModalities.join(" and ")} input.`);
		return {
			catalogId: selected.id,
			runtimeModelId: selected.model
		};
	}
	const model = params.selection.id;
	const match = listed.find((entry) => entry.model === model || entry.id === model);
	if (!match) throw new Error(`Codex app-server model not found: ${model}`);
	if (params.requiredModalities.includes("image") && !match.inputModalities.includes("image")) throw new Error(`Codex app-server model does not support images: ${model}`);
	if (params.requiredModalities.includes("text") && !match.inputModalities.includes("text")) throw new Error(`Codex app-server model does not support text: ${model}`);
	return {
		catalogId: match.id,
		runtimeModelId: match.model
	};
}
function resolveCodexBoundedTurnAbortError(signal, taskLabel, timeoutError) {
	return signal.reason === timeoutError ? timeoutError : /* @__PURE__ */ new Error(`codex app-server ${taskLabel} turn aborted`);
}
//#endregion
export { runBoundedCodexAppServerTurn };
