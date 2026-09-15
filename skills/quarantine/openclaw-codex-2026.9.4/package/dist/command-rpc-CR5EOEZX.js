import { t as __exportAll } from "./rolldown-runtime-8H4AJuhK.js";
import { o as isJsonObject } from "./protocol-5bh1G-H7.js";
import { n as describeControlFailure, t as CODEX_CONTROL_METHODS } from "./capabilities-8vx68WLH.js";
import { i as requestCodexAppServerJson, o as withCodexAppServerJsonClient } from "./request-B7hEkBGq.js";
import "./config-oIORaQ5T.js";
import { n as resolveCodexAppServerRuntimeOptions, r as resolveCodexSupervisionAppServerRuntimeOptions } from "./config-runtime-D0zGNIHu.js";
import { r as prepareCodexAppServerAuthBinding } from "./auth-binding-CWlKVccJ.js";
import { a as resolveCodexAppServerAuthProfileStore, r as resolveCodexAppServerAuthProfileId } from "./auth-profile-CwzO4_RG.js";
import { tt as resolveCodexAppServerPreparedAuthHandoff } from "./shared-client-CscigXXL.js";
import { a as closeCodexStartupClientBestEffort } from "./attempt-client-cleanup-DKHzbwt5.js";
import { n as listCodexAppServerModels } from "./models-PCKOim-h.js";
import { n as createCodexSessionGenerationSupersededError } from "./session-binding-CI8UuilT.js";
import { t as resumeCodexAppServerThread } from "./thread-resume-DsDOZpFg.js";
import { resolveAgentDir, resolveSessionAgentIdsStrict } from "openclaw/plugin-sdk/agent-scope-runtime";
import { resolveAgentWorkspaceDir } from "openclaw/plugin-sdk/agent-runtime";
import { prepareAgentRuntimeAuth } from "openclaw/plugin-sdk/agent-harness-runtime";
import { getSessionEntry, resolveStorePath } from "openclaw/plugin-sdk/session-store-runtime";
import { resolveSessionModelRef } from "openclaw/plugin-sdk/model-session-runtime";
import { resolveApiKeyForProvider } from "openclaw/plugin-sdk/provider-auth-runtime";
//#region extensions/codex/src/command-rpc.ts
var command_rpc_exports = /* @__PURE__ */ __exportAll({
	codexControlRequest: () => codexControlRequest,
	prepareCodexControlSessionAuth: () => prepareCodexControlSessionAuth,
	readCodexStatusProbes: () => readCodexStatusProbes,
	requestOptions: () => requestOptions,
	safeCodexControlRequest: () => safeCodexControlRequest
});
/** Selects the same prepared auth partition as an admitted session turn. */
async function prepareCodexControlSessionAuth(options, startOptions) {
	if (!options.config || !options.sessionKey || !options.sessionId) {
		if (options.onResponse) throw new Error("Codex control subscription requires admitted session authority.");
		return {
			authProfileId: options.authProfileId ?? void 0,
			clientOptions: { authProfileId: options.authProfileId }
		};
	}
	const config = options.config;
	const { sessionAgentId } = resolveSessionAgentIdsStrict({
		config,
		sessionKey: options.sessionKey,
		agentId: options.agentId
	});
	const agentDir = options.agentDir ?? resolveAgentDir(config, sessionAgentId);
	const workspaceDir = resolveAgentWorkspaceDir(config, sessionAgentId);
	const entry = getSessionEntry({
		agentId: sessionAgentId,
		storePath: options.storePath?.trim() || resolveStorePath(config.session?.store, { agentId: sessionAgentId }),
		sessionKey: options.sessionKey,
		hydrateSkillPromptRefs: false,
		readConsistency: "latest"
	});
	if (entry?.sessionId !== options.sessionId) throw createCodexSessionGenerationSupersededError(options.sessionId);
	if (options.authProfileId === null || startOptions.homeScope === "user") return {
		authProfileId: options.authProfileId ?? void 0,
		clientOptions: { authProfileId: options.authProfileId }
	};
	const model = resolveSessionModelRef(config, entry, sessionAgentId);
	const authProfileId = entry?.authProfileOverride ?? options.authProfileId;
	const store = resolveCodexAppServerAuthProfileStore({
		agentDir,
		config,
		authProfileId
	});
	const { plan, attempts } = prepareAgentRuntimeAuth({
		provider: model.provider,
		modelId: model.model,
		config,
		agentDir,
		workspaceDir,
		authProfileStore: store,
		sessionAuthProfileId: authProfileId,
		sessionAuthProfileSource: entry?.authProfileOverrideSource,
		harnessId: "codex",
		harnessAuthBootstrap: "harness"
	});
	const route = plan.modelRoute;
	const resolvedAuth = route ? await resolveApiKeyForProvider({
		provider: route.provider,
		modelId: route.modelId,
		modelApi: route.api,
		cfg: config,
		agentDir,
		workspaceDir,
		store,
		profileId: attempts[0]?.profileId,
		lockedProfile: plan.forwardedAuthProfileSource === "user",
		allowAuthProfileFallback: attempts[0]?.allowAuthProfileFallback,
		skipSetupProviderFallback: true
	}) : void 0;
	const handoff = await resolveCodexAppServerPreparedAuthHandoff({
		authRequirement: route?.authRequirement,
		resolvedApiKey: resolvedAuth?.apiKey,
		authProfileId: route ? plan.forwardedAuthProfileId : resolveCodexAppServerAuthProfileId({
			authProfileId: plan.forwardedAuthProfileId,
			store,
			config
		}),
		authProfileStore: store,
		agentDir,
		homeScope: startOptions.homeScope ?? "agent",
		config,
		subscriptionProfileRequiredError: "Prepared Codex subscription route requires a forwarded OpenAI OAuth or token profile.",
		subscriptionProfileUnusableError: "Prepared Codex subscription auth profile is unusable."
	});
	const binding = handoff.authProfileId ? await prepareCodexAppServerAuthBinding({
		authProfileId: handoff.authProfileId,
		authProfileStore: store,
		agentDir,
		config
	}) : void 0;
	return {
		authProfileId: handoff.authProfileId,
		clientOptions: {
			...handoff.preparedAuth ? { preparedAuth: handoff.preparedAuth } : { authProfileId: handoff.authProfileId },
			authRequirement: route?.authRequirement,
			authProfileStore: binding?.authProfileStore ?? store,
			authBindingFingerprint: binding?.fingerprint,
			agentDir
		}
	};
}
function requestOptions(pluginConfig, limit, config, agentDir) {
	const runtime = resolveCodexAppServerRuntimeOptions({ pluginConfig });
	return {
		limit,
		timeoutMs: runtime.requestTimeoutMs,
		startOptions: runtime.start,
		config,
		agentDir
	};
}
async function codexControlRequest(pluginConfig, method, requestParams, options = {}) {
	const runtime = options.startOptions ? resolveCodexSupervisionAppServerRuntimeOptions({ pluginConfig }) : resolveCodexAppServerRuntimeOptions({ pluginConfig });
	const startOptions = options.startOptions ?? runtime.start;
	const auth = options.onResponse ? await prepareCodexControlSessionAuth(options, startOptions) : {
		authProfileId: options.authProfileId ?? void 0,
		clientOptions: { authProfileId: options.authProfileId }
	};
	const controlRequestOptions = {
		timeoutMs: options.timeoutMs ?? runtime.requestTimeoutMs,
		assertCurrent: options.assertCurrent,
		startOptions,
		config: options.config,
		sessionKey: options.sessionKey,
		sessionId: options.sessionId,
		agentDir: options.agentDir,
		isolated: options.isolated,
		...auth.clientOptions
	};
	if (options.onResponse || options.beforeRequest) return await withCodexAppServerJsonClient(controlRequestOptions, async (request, client, scope) => {
		await options.beforeRequest?.(request, client, scope);
		scope.assertCurrent();
		let response;
		if (method === "thread/resume") {
			if (!isJsonObject(requestParams) || typeof requestParams.threadId !== "string") throw new Error("Codex thread/resume requires a thread id.");
			response = await resumeCodexAppServerThread({
				client,
				request: {
					...requestParams,
					threadId: requestParams.threadId
				},
				requestResume: () => request({
					method,
					requestParams
				}),
				abandonClient: () => closeCodexStartupClientBestEffort(client)
			});
		} else response = await request({
			method,
			requestParams
		});
		await options.onResponse?.(response, client, {
			authProfileId: auth.authProfileId,
			assertCurrent: scope.assertCurrent
		});
		scope.assertCurrent();
		return response;
	});
	return await requestCodexAppServerJson({
		method,
		requestParams,
		...controlRequestOptions
	});
}
async function safeCodexControlRequest(pluginConfig, method, requestParams, options = {}) {
	return await safeValue(async () => await codexControlRequest(pluginConfig, method, requestParams, options));
}
async function safeCodexModelList(pluginConfig, limit, config, agentDir) {
	return await safeValue(async () => await listCodexAppServerModels(requestOptions(pluginConfig, limit, config, agentDir)));
}
async function readCodexStatusProbes(pluginConfig, config, agentDir) {
	const [models, account, limits, mcps, skills] = await Promise.all([
		safeCodexModelList(pluginConfig, 20, config, agentDir),
		safeCodexControlRequest(pluginConfig, CODEX_CONTROL_METHODS.account, { refreshToken: false }, {
			config,
			agentDir
		}),
		safeCodexControlRequest(pluginConfig, CODEX_CONTROL_METHODS.rateLimits, void 0, {
			config,
			agentDir
		}),
		safeCodexControlRequest(pluginConfig, CODEX_CONTROL_METHODS.listMcpServers, { limit: 100 }, {
			config,
			agentDir
		}),
		safeCodexControlRequest(pluginConfig, CODEX_CONTROL_METHODS.listSkills, {}, {
			config,
			agentDir
		})
	]);
	return {
		models,
		account,
		limits,
		mcps,
		skills
	};
}
async function safeValue(read) {
	try {
		return {
			ok: true,
			value: await read()
		};
	} catch (error) {
		return {
			ok: false,
			error: describeControlFailure(error)
		};
	}
}
//#endregion
export { requestOptions as a, readCodexStatusProbes as i, command_rpc_exports as n, safeCodexControlRequest as o, prepareCodexControlSessionAuth as r, codexControlRequest as t };
