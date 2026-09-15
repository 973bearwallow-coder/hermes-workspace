import { i as resolveCodexAppServerHomeScope } from "./config-options-CXMq1T-C.js";
import { x as readCodexPluginConfig } from "./protocol-5bh1G-H7.js";
import { g as assertCodexPassiveTurnItems } from "./client-B57KWPQx.js";
import "./config-oIORaQ5T.js";
import { tt as resolveCodexAppServerPreparedAuthHandoff } from "./shared-client-CscigXXL.js";
import { runBoundedCodexAppServerTurn } from "./bounded-turn-C_Hneydj.js";
import { a as createAttributedCodexAssistantMessage } from "./event-projector-assistant-message-BmBM4qBV.js";
//#region extensions/codex/src/app-server/isolated-completion.ts
/** Runs prompt-only Codex inference on an ephemeral, ring-zero native thread. */
async function runCodexIsolatedCompletion(params, options) {
	params.assertCurrent?.();
	const authorization = params.authorization;
	if (authorization.owner !== "harness") throw new Error("Codex native isolated completion requires harness-owned authorization.");
	const pluginConfig = readCodexPluginConfig(options.pluginConfig);
	const authRequirement = authorization.plan.modelRoute?.authRequirement;
	const authHandoff = await resolveCodexAppServerPreparedAuthHandoff({
		authRequirement,
		authProfileId: authorization.plan.forwardedAuthProfileId,
		authProfileStore: authorization.authProfileStore,
		agentDir: params.agentDir,
		homeScope: resolveCodexAppServerHomeScope({ appServer: pluginConfig.appServer }),
		config: params.config,
		subscriptionProfileRequiredError: "Prepared Codex subscription route requires a scoped native OAuth or token profile.",
		subscriptionProfileUnusableError: `Prepared Codex auth profile "${authorization.plan.forwardedAuthProfileId}" is unusable.`
	});
	params.assertCurrent?.();
	const authSelection = authHandoff.preparedAuth ? { preparedAuth: authHandoff.preparedAuth } : { profile: authHandoff.authProfileId };
	const result = await runBoundedCodexAppServerTurn({
		config: params.config,
		model: {
			mode: "required",
			id: params.modelId
		},
		...authSelection,
		authRequirement,
		timeoutMs: params.timeoutMs,
		signal: params.abortSignal,
		assertCurrent: params.assertCurrent,
		agentDir: params.agentDir,
		authProfileStore: authorization.authProfileStore,
		options,
		taskLabel: "isolated completion",
		developerInstructions: params.systemPrompt,
		input: [{
			type: "text",
			text: params.prompt,
			text_elements: []
		}],
		requiredModalities: ["text"],
		isolation: "configured-transport",
		requireNoExternalCapabilities: true
	});
	params.assertCurrent?.();
	assertCodexPassiveTurnItems(result.items, params.prompt, "isolated completion");
	return { assistant: createAttributedCodexAssistantMessage({
		api: "openai-chatgpt-responses",
		provider: params.provider,
		modelId: result.model
	}, result.text, {
		tokenUsage: result.usage,
		aborted: false,
		promptError: null
	}) };
}
//#endregion
export { runCodexIsolatedCompletion };
