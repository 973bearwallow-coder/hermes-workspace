import { t as __exportAll } from "./rolldown-runtime-8H4AJuhK.js";
import { x as readCodexPluginConfig } from "./protocol-5bh1G-H7.js";
import { a as resolveCodexCatalogConnectionHome, t as buildCodexAppServerConnectionFingerprint } from "./plugin-app-cache-key-d0eKxy7b.js";
import { n as resolveCodexAppServerRuntimeOptions, r as resolveCodexSupervisionAppServerRuntimeOptions } from "./config-runtime-D0zGNIHu.js";
import { AgentHarnessPreflightError } from "openclaw/plugin-sdk/agent-harness-registration";
//#region extensions/codex/src/app-server/binding-connection.ts
var binding_connection_exports = /* @__PURE__ */ __exportAll({
	assertCodexSessionRuntimeOwnership: () => assertCodexSessionRuntimeOwnership,
	requireCodexSupervisionModelSelection: () => requireCodexSupervisionModelSelection,
	resolveCodexBindingAppServerConnection: () => resolveCodexBindingAppServerConnection
});
/** Prevents a prepared native session from becoming a fresh thread after its binding changes. */
function assertCodexSessionRuntimeOwnership(binding, expected) {
	if (!expected) return;
	const auth = binding?.connectionScope === "supervision" ? "native" : "host";
	const hostModelChanged = expected.auth === "host" && (!expected.modelRef || binding?.model !== expected.modelRef.model || binding?.modelProvider !== expected.modelRef.provider);
	if (binding?.preserveNativeModel !== true || auth !== expected.auth || hostModelChanged) throw new AgentHarnessPreflightError("Codex native session ownership is missing or changed. Reattach the original native session or create a new chat with a concrete model; no replacement thread was started.");
}
/** Requires the native model pair after a supervised pending branch has materialized. */
function requireCodexSupervisionModelSelection(binding) {
	const model = binding.model?.trim();
	const modelProvider = binding.modelProvider?.trim();
	if (binding.connectionScope !== "supervision" || !model || !modelProvider) throw new Error("Codex supervised binding is missing its native model and provider; refusing request selection");
	return {
		model,
		modelProvider
	};
}
/** Resolves connection and auth ownership exclusively from the private thread binding. */
function resolveCodexBindingAppServerConnection(params) {
	const { binding, authProfileId, ...runtimeParams } = params;
	const usesSupervisionConnection = binding?.connectionScope === "supervision";
	if (usesSupervisionConnection && readCodexPluginConfig(runtimeParams.pluginConfig).supervision?.enabled !== true) throw new Error("Codex supervision is disabled; refusing to open a native user-home supervised session");
	let appServer = (usesSupervisionConnection ? resolveCodexSupervisionAppServerRuntimeOptions : resolveCodexAppServerRuntimeOptions)(runtimeParams);
	if (usesSupervisionConnection) {
		const persistedFingerprint = binding.pendingSupervisionBranch?.connectionFingerprint ?? binding.appServerRuntimeFingerprint;
		const catalogHome = persistedFingerprint ? resolveCodexCatalogConnectionHome(persistedFingerprint, runtimeParams.agentDir) : void 0;
		if (catalogHome) appServer = {
			...appServer,
			start: {
				...appServer.start,
				homeScope: "user",
				env: {
					...appServer.start.env,
					CODEX_HOME: catalogHome
				}
			}
		};
		const currentFingerprint = buildCodexAppServerConnectionFingerprint(appServer, runtimeParams.agentDir);
		if (!persistedFingerprint || persistedFingerprint !== currentFingerprint) throw new Error("Codex supervision connection changed; refusing to operate on its bound native thread");
	}
	return {
		appServer,
		usesSupervisionConnection,
		requestAuthProfileId: usesSupervisionConnection ? void 0 : authProfileId,
		clientAuthProfileId: usesSupervisionConnection ? null : authProfileId
	};
}
//#endregion
export { resolveCodexBindingAppServerConnection as i, binding_connection_exports as n, requireCodexSupervisionModelSelection as r, assertCodexSessionRuntimeOwnership as t };
