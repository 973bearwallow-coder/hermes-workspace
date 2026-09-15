import { c as CODEX_PLUGINS_MARKETPLACE_NAME, i as pluginReadParams, n as isOpenAiCuratedMarketplace, r as isOpenAiCuratedMarketplaceName, t as findCodexMarketplacePluginSummary } from "./plugin-inventory-oL4Na1ZG.js";
import { t as CodexAppServerRpcError } from "./rpc-error-ttN_QjEm.js";
import "./config-oIORaQ5T.js";
import { coerceErrorMessage } from "openclaw/plugin-sdk/error-runtime";
//#region extensions/codex/src/app-server/plugin-activation.ts
/**
* Activates legacy curated Codex plugins while requiring owner-managed
* installation for every other marketplace.
*/
/** Activates legacy curated plugins without granting install authority to other marketplaces. */
async function ensureCodexPluginActivation(params) {
	if (params.identity.marketplaceName === "workspace-directory") return activationFailure(params.identity, "disabled", { message: "workspace-directory plugins must be installed and enabled outside OpenClaw before use." });
	if (!isOpenAiCuratedMarketplaceName(params.identity.marketplaceName)) {
		const target = params.identity.pluginName.endsWith(`@${params.identity.marketplaceName}`) ? params.identity.pluginName : `${params.identity.pluginName}@${params.identity.marketplaceName}`;
		return activationFailure(params.identity, "disabled", { message: `${params.identity.marketplaceName} plugins must be installed and enabled by an owner before use. Run /codex plugins install ${target}.` });
	}
	const listed = await listCuratedCodexPluginMetadata(params);
	const resolved = findCodexMarketplacePluginSummary(listed, params.identity.marketplaceName, params.identity.pluginName);
	if (!resolved) {
		if (!listed.marketplaces.some((marketplace) => isOpenAiCuratedMarketplace(marketplace))) return activationFailure(params.identity, "marketplace_missing", { message: `Codex marketplace ${CODEX_PLUGINS_MARKETPLACE_NAME} was not found.` });
		return activationFailure(params.identity, "plugin_missing", { message: `${params.identity.pluginName} was not found in ${CODEX_PLUGINS_MARKETPLACE_NAME}.` });
	}
	if (resolved.marketplace.remoteMarketplaceName && !resolved.summary.remotePluginId) return activationFailure(params.identity, "plugin_missing", { message: `${params.identity.pluginName} detail unavailable: Codex did not return a remote plugin id.` });
	if (resolved.summary.availability === "DISABLED_BY_ADMIN" || resolved.summary.installPolicy === "NOT_AVAILABLE") return activationFailure(params.identity, "disabled", { message: `${params.identity.pluginName} was disabled or made unavailable by its marketplace administrator.` });
	if (resolved.summary.installed && resolved.summary.enabled && !params.installEvenIfActive) return {
		identity: params.identity,
		ok: true,
		reason: "already_active",
		installAttempted: false,
		marketplace: resolved.marketplace,
		diagnostics: []
	};
	const remotePluginId = resolved.marketplace.remoteMarketplaceName ? resolved.summary.remotePluginId : void 0;
	let installResponse;
	try {
		installResponse = await params.request("plugin/install", pluginReadParams(resolved.marketplace, remotePluginId ?? params.identity.pluginName));
	} catch (error) {
		if (!(error instanceof CodexAppServerRpcError) || error.code !== -32600 || !remotePluginId || error.message !== `remote plugin ${remotePluginId} is disabled by admin` && error.message !== `remote plugin ${remotePluginId} is not available for install`) throw error;
		return {
			identity: params.identity,
			ok: false,
			reason: "install_failed",
			installAttempted: true,
			marketplace: resolved.marketplace,
			diagnostics: [{ message: `Codex plugin install failed: ${coerceErrorMessage(error)}` }]
		};
	}
	if (params.metadataCache && params.appCacheKey) params.metadataCache.invalidate(params.appCacheKey);
	const refreshDiagnostics = [];
	let refreshFailed = false;
	try {
		const refreshResult = await refreshCodexPluginRuntimeState({
			request: params.request,
			appCache: params.appCache,
			appCacheKey: params.appCacheKey,
			configCwd: params.configCwd,
			metadataCache: params.metadataCache,
			deferAppInventoryRefresh: params.deferAppInventoryRefresh,
			targetAppIds: params.targetAppIds
		});
		refreshDiagnostics.push(...refreshResult.diagnostics);
	} catch (error) {
		refreshFailed = true;
		refreshDiagnostics.push({ message: `Codex plugin runtime refresh failed after install: ${coerceErrorMessage(error)}` });
	}
	const authRequired = installResponse.appsNeedingAuth.length > 0;
	return {
		identity: params.identity,
		ok: !authRequired && !refreshFailed,
		reason: refreshFailed ? "refresh_failed" : authRequired ? "auth_required" : resolved.summary.installed && resolved.summary.enabled ? "already_active" : "installed",
		installAttempted: true,
		marketplace: resolved.marketplace,
		installResponse,
		diagnostics: [...refreshDiagnostics, ...installResponse.appsNeedingAuth.map((app) => ({ message: `${app.name} requires app authentication before plugin tools are exposed.` }))]
	};
}
/** Forces Codex plugin, skill, hook, MCP, and app inventory refreshes after activation. */
async function refreshCodexPluginRuntimeState(params) {
	const diagnostics = [];
	await listCuratedCodexPluginMetadata(params, { forceRefetch: true });
	await params.request("skills/list", {
		cwds: params.configCwd ? [params.configCwd] : [],
		forceReload: true
	});
	try {
		await params.request("hooks/list", { cwds: params.configCwd ? [params.configCwd] : [] });
	} catch (error) {
		diagnostics.push({ message: `Codex hooks refresh skipped: ${coerceErrorMessage(error)}` });
	}
	await params.request("config/mcpServer/reload", void 0);
	if (params.appCache && params.appCacheKey) try {
		await refreshCodexAppRuntimeState({
			...params,
			appCache: params.appCache,
			appCacheKey: params.appCacheKey
		});
	} catch (error) {
		diagnostics.push({ message: `Codex app inventory refresh skipped: ${coerceErrorMessage(error)}` });
	}
	return { diagnostics };
}
/** Refreshes hosted app tools without reloading unrelated active threads. */
async function refreshCodexAppRuntimeState(params) {
	params.appCache.invalidate(params.appCacheKey, "Codex plugin app inventory refresh requested", void 0, params.targetAppIds);
	if (params.deferAppInventoryRefresh) return;
	const request = async (method, requestParams) => await params.request(method, requestParams);
	await params.appCache.refreshNow({
		key: params.appCacheKey,
		request,
		forceRefetch: true,
		targetAppIds: params.targetAppIds
	});
}
async function listCuratedCodexPluginMetadata(params, options = {}) {
	const requestParams = {
		...params.configCwd ? { cwds: [params.configCwd] } : {},
		...options.forceRefetch ? { forceRefetch: true } : {}
	};
	if (!params.metadataCache || !params.appCacheKey) return await params.request("plugin/list", requestParams);
	return (await params.metadataCache.load({
		appCacheKey: params.appCacheKey,
		queryKind: "curated-global",
		requestParams,
		request: async (method, listedParams) => await params.request(method, listedParams),
		cacheable: (response) => response.marketplaces.some((marketplace) => isOpenAiCuratedMarketplace(marketplace))
	})).response;
}
function activationFailure(identity, reason, diagnostic, extraDiagnostics = []) {
	return {
		identity,
		ok: false,
		reason,
		installAttempted: false,
		diagnostics: [diagnostic, ...extraDiagnostics]
	};
}
//#endregion
export { refreshCodexAppRuntimeState as n, refreshCodexPluginRuntimeState as r, ensureCodexPluginActivation as t };
