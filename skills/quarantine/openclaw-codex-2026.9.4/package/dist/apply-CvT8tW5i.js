import { c as CODEX_PLUGINS_MARKETPLACE_NAME } from "./plugin-inventory-oL4Na1ZG.js";
import { x as readCodexPluginConfig } from "./protocol-5bh1G-H7.js";
import { s as resolveCodexAppServerFallbackApiKeyCacheKey } from "./auth-cache-key-7orQae_j.js";
import { r as buildCodexPluginAppCacheKey, s as defaultCodexAppInventoryCache } from "./plugin-app-cache-key-d0eKxy7b.js";
import { i as requestCodexAppServerJson } from "./request-B7hEkBGq.js";
import "./config-oIORaQ5T.js";
import { n as resolveCodexAppServerRuntimeOptions } from "./config-runtime-D0zGNIHu.js";
import { i as resolveCodexAppServerAuthProfileIdForAgent } from "./auth-profile-CwzO4_RG.js";
import { c as getLeasedSharedCodexAppServerClient, et as resolveCodexAppServerAuthAccountCacheKey, h as releaseLeasedSharedCodexAppServerClient, o as clearSharedCodexAppServerClientIfCurrentAndWait } from "./shared-client-CscigXXL.js";
import { t as ensureCodexPluginActivation } from "./plugin-activation-BYQculil.js";
import { CODEX_PLUGIN_CONFIG_PATH, buildCodexMigrationPlan, buildCodexPluginsConfigValue, hasCodexPluginConfigConflict, n as applyCodexAuthItems, r as resolveCodexConfigPatchMode, readCodexPluginMigrationConfigEntry, t as resolveCodexMigrationTargets } from "./plan-7uG-Fp36.js";
import { uniqueStrings } from "openclaw/plugin-sdk/string-coerce-runtime";
import { parseStrictNonNegativeInteger } from "openclaw/plugin-sdk/number-runtime";
import path from "node:path";
import { coerceErrorMessage } from "openclaw/plugin-sdk/error-runtime";
import { sleep } from "openclaw/plugin-sdk/runtime-env";
import { MIGRATION_REASON_TARGET_EXISTS, applyMigrationManualItem, markMigrationItemConflict, markMigrationItemError, markMigrationItemSkipped, resolveMigrationConfigRuntime, summarizeMigrationItems, writeMigrationConfigPath } from "openclaw/plugin-sdk/migration";
import { archiveMigrationItem, copyMemoryMigrationFileItem, copyMigrationFileItem, withCachedMigrationConfigRuntime, writeMigrationReport } from "openclaw/plugin-sdk/migration-runtime";
//#region extensions/codex/src/migration/apply-report.ts
function codexPluginActivationReportState(result) {
	switch (result.reason) {
		case "already_active":
		case "installed": return {
			installed: true,
			enabled: true
		};
		case "auth_required": return {
			installed: true,
			enabled: false
		};
		case "disabled":
		case "install_failed":
		case "marketplace_missing":
		case "plugin_missing": return {
			installed: false,
			enabled: false
		};
		case "refresh_failed": return {
			installed: true,
			enabled: false
		};
	}
	return result.reason;
}
function sanitizeAppsNeedingAuth(apps) {
	return apps.map((app) => ({
		id: app.id,
		name: app.name,
		needsAuth: true
	}));
}
//#endregion
//#region extensions/codex/src/migration/apply.ts
const CODEX_PLUGIN_AUTH_REQUIRED_REASON = "auth_required";
const CODEX_PLUGIN_NOT_SELECTED_REASON = "not selected for migration";
const CODEX_PLUGIN_LOAD_WARNING = "Some Codex plugins could not be migrated. Run `openclaw migrate codex` after onboarding.";
const TARGET_CODEX_MARKETPLACE_DISCOVERY_POLL_MS = 250;
const TARGET_CODEX_MARKETPLACE_DISCOVERY_TIMEOUT_MS = 3e4;
const TARGET_CODEX_MARKETPLACE_DISCOVERY_TIMEOUT_ENV = "OPENCLAW_CODEX_MIGRATION_PLUGIN_LIST_TIMEOUT_MS";
var CodexPluginConfigConflictError = class extends Error {
	constructor(reason) {
		super(reason);
		this.reason = reason;
		this.name = "CodexPluginConfigConflictError";
	}
};
function shouldReturnCodexPluginConfigPatch(ctx) {
	return resolveCodexConfigPatchMode(ctx) === "return";
}
function prepareTargetCodexAppServer(ctx) {
	const appServer = resolveTargetCodexAppServer(ctx);
	const targets = resolveCodexMigrationTargets(ctx);
	let warmedClient;
	const ready = getLeasedSharedCodexAppServerClient({
		startOptions: appServer.start,
		timeoutMs: 6e4,
		agentDir: targets.agentDir,
		config: ctx.config
	}).then((client) => {
		warmedClient = client;
	}, () => void 0);
	return { async dispose() {
		await ready;
		if (warmedClient) releaseLeasedSharedCodexAppServerClient(warmedClient);
		await clearSharedCodexAppServerClientIfCurrentAndWait(warmedClient, {
			exitTimeoutMs: 2e3,
			forceKillDelayMs: 250
		});
	} };
}
async function applyCodexMigrationPlan(params) {
	const plan = params.plan ?? await buildCodexMigrationPlan(params.ctx);
	const reportDir = params.ctx.reportDir ?? path.join(params.ctx.stateDir, "migration", "codex");
	const items = [];
	const targets = resolveCodexMigrationTargets(params.ctx);
	const codexHome = typeof plan.metadata?.codexHome === "string" && plan.metadata.codexHome.trim() ? plan.metadata.codexHome : plan.source;
	const authSource = {
		codexHome,
		authPath: path.join(codexHome, "auth.json"),
		modelsCachePath: path.join(codexHome, "models_cache.json")
	};
	const runtime = withCachedMigrationConfigRuntime(params.ctx.runtime ?? params.runtime, params.ctx.config);
	const applyCtx = {
		...params.ctx,
		runtime
	};
	for (const item of plan.items) {
		if (item.status !== "planned") {
			items.push(item);
			continue;
		}
		if (item.id === "config:codex-plugins") items.push(await applyCodexPluginConfigItem(applyCtx, item, items));
		else if (item.kind === "auth") items.push(...await applyCodexAuthItems({
			ctx: applyCtx,
			item,
			source: authSource,
			targets
		}));
		else if (item.kind === "plugin" && item.action === "install") items.push(await applyCodexPluginInstallItem(applyCtx, item));
		else if (item.kind === "manual") items.push(applyMigrationManualItem(item));
		else if (item.action === "archive") items.push(await archiveMigrationItem(item, reportDir));
		else if (item.kind === "memory") items.push(await copyMemoryMigrationFileItem(item, reportDir, {
			workspaceDir: targets.workspaceDir,
			overwrite: params.ctx.overwrite
		}));
		else items.push(await copyMigrationFileItem(item, reportDir, { overwrite: params.ctx.overwrite }));
	}
	const result = {
		...plan,
		items,
		summary: summarizeMigrationItems(items),
		backupPath: params.ctx.backupPath,
		reportDir
	};
	if (items.some(isCodexPluginLoadWarningItem)) {
		result.warnings = uniqueStrings([...result.warnings ?? [], CODEX_PLUGIN_LOAD_WARNING]);
		result.nextSteps = uniqueStrings([CODEX_PLUGIN_LOAD_WARNING, ...result.nextSteps ?? []]);
	}
	await writeMigrationReport(result, { title: "Codex Migration Report" });
	return result;
}
async function applyCodexPluginInstallItem(ctx, item) {
	const policy = readCodexPluginPolicy(item);
	if (!policy) return {
		...markMigrationItemError(item, "invalid Codex plugin migration item"),
		details: {
			...item.details,
			code: "invalid_plugin_item"
		}
	};
	try {
		const appCacheKey = await buildTargetCodexPluginAppCacheKey(ctx);
		const appServer = resolveTargetCodexAppServer(ctx);
		const result = await ensureCodexPluginActivation({
			identity: policy,
			installEvenIfActive: true,
			request: async (method, requestParams) => await requestTargetCodexAppServerJson({
				method,
				requestParams,
				timeoutMs: 6e4,
				startOptions: appServer.start,
				agentDir: resolveCodexMigrationTargets(ctx).agentDir,
				config: ctx.config,
				isolated: false
			}),
			appCache: defaultCodexAppInventoryCache,
			appCacheKey
		});
		const baseDetails = {
			...item.details,
			code: result.reason,
			activationReason: result.reason,
			...codexPluginActivationReportState(result),
			installAttempted: result.installAttempted,
			diagnostics: result.diagnostics.map((diagnostic) => diagnostic.message)
		};
		if (result.ok) return {
			...item,
			status: "migrated",
			...result.reason === "already_active" ? { reason: "already active" } : {},
			details: baseDetails
		};
		if (result.reason === CODEX_PLUGIN_AUTH_REQUIRED_REASON) return {
			...item,
			status: "skipped",
			reason: CODEX_PLUGIN_AUTH_REQUIRED_REASON,
			details: {
				...baseDetails,
				appsNeedingAuth: sanitizeAppsNeedingAuth(result.installResponse?.appsNeedingAuth ?? [])
			}
		};
		if (result.reason === "plugin_missing" || result.reason === "marketplace_missing") return {
			...item,
			status: "warning",
			reason: result.reason,
			message: `Codex plugin "${policy.pluginName}" could not be migrated automatically`,
			details: {
				...baseDetails,
				warningReason: CODEX_PLUGIN_LOAD_WARNING
			}
		};
		return {
			...item,
			status: "error",
			reason: result.reason,
			details: baseDetails
		};
	} catch (error) {
		if (isCodexPluginInventoryLoadError(error)) return {
			...item,
			status: "warning",
			reason: "plugin_inventory_unavailable",
			message: `Codex plugin "${policy.pluginName}" could not be migrated automatically`,
			details: {
				...item.details,
				code: "plugin_inventory_unavailable",
				warningReason: CODEX_PLUGIN_LOAD_WARNING,
				diagnostic: coerceErrorMessage(error)
			}
		};
		return {
			...item,
			status: "error",
			reason: coerceErrorMessage(error),
			details: {
				...item.details,
				code: "plugin_install_failed"
			}
		};
	}
}
function isCodexPluginInventoryLoadError(error) {
	return coerceErrorMessage(error).includes("codex app-server plugin/list timed out");
}
function resolveTargetCodexAppServer(ctx) {
	return resolveCodexAppServerRuntimeOptions({ pluginConfig: readCodexPluginConfig(ctx.config) });
}
async function requestTargetCodexAppServerJson(params) {
	if (params.method !== "plugin/list") return await requestCodexAppServerJson(params);
	const deadline = Date.now() + params.timeoutMs;
	const discoveryTimeoutMs = targetCodexMarketplaceDiscoveryTimeoutMs();
	const discoveryDeadline = Math.min(deadline, Date.now() + discoveryTimeoutMs);
	let lastResponse;
	let attempt = 0;
	do {
		attempt += 1;
		const remainingMs = Math.max(1, discoveryDeadline - Date.now());
		lastResponse = await requestCodexAppServerJson({
			...params,
			timeoutMs: remainingMs
		});
		if (hasOpenAiCuratedMarketplace(lastResponse)) return lastResponse;
		if (Date.now() >= discoveryDeadline) return lastResponse;
		const waitMs = Math.min(TARGET_CODEX_MARKETPLACE_DISCOVERY_POLL_MS, discoveryDeadline - Date.now());
		await sleep(waitMs);
	} while (Date.now() < discoveryDeadline);
	return lastResponse;
}
function hasOpenAiCuratedMarketplace(response) {
	if (!response || typeof response !== "object" || !("marketplaces" in response)) return false;
	const marketplaces = response.marketplaces;
	return Array.isArray(marketplaces) && marketplaces.some((marketplace) => marketplace && typeof marketplace === "object" && marketplace.name === "openai-curated");
}
function targetCodexMarketplaceDiscoveryTimeoutMs(env = process.env) {
	const configured = parseStrictNonNegativeInteger(env[TARGET_CODEX_MARKETPLACE_DISCOVERY_TIMEOUT_ENV]);
	if (configured !== void 0) return configured;
	return TARGET_CODEX_MARKETPLACE_DISCOVERY_TIMEOUT_MS;
}
function isCodexPluginLoadWarningItem(item) {
	return item.kind === "plugin" && item.action === "install" && item.status === "warning" && item.details?.warningReason === CODEX_PLUGIN_LOAD_WARNING;
}
async function buildTargetCodexPluginAppCacheKey(ctx) {
	const targets = resolveCodexMigrationTargets(ctx);
	const appServer = resolveTargetCodexAppServer(ctx);
	const authProfileId = resolveCodexAppServerAuthProfileIdForAgent({
		agentDir: targets.agentDir,
		config: ctx.config
	});
	const accountId = await resolveCodexAppServerAuthAccountCacheKey({
		authProfileId,
		agentDir: targets.agentDir,
		config: ctx.config
	});
	const envApiKeyFingerprint = authProfileId ? void 0 : resolveCodexAppServerFallbackApiKeyCacheKey({ startOptions: appServer.start });
	return buildCodexPluginAppCacheKey({
		appServer,
		agentDir: targets.agentDir,
		authProfileId,
		accountId,
		envApiKeyFingerprint
	});
}
async function applyCodexPluginConfigItem(ctx, item, appliedItems) {
	if (appliedItems.filter((candidate) => candidate.kind === "plugin" && candidate.action === "install" && readCodexPluginPolicy(candidate) !== void 0 && !isCodexPluginConfigTerminal(candidate)).length > 0) return {
		...item,
		status: "warning",
		reason: "selected Codex plugin activation is incomplete"
	};
	const entries = appliedItems.map(readAppliedPluginConfigEntry).filter((entry) => entry !== void 0);
	if (entries.length === 0) return {
		...markMigrationItemSkipped(item, "no selected Codex plugins"),
		deferredCompletion: true
	};
	const returnPatch = shouldReturnCodexPluginConfigPatch(ctx);
	const configApi = resolveMigrationConfigRuntime(ctx);
	const currentConfig = returnPatch ? ctx.config : configApi?.current?.();
	if (!currentConfig) return markMigrationItemError(item, "config runtime unavailable");
	const value = buildCodexPluginsConfigValue(entries, currentConfig);
	if (!ctx.overwrite && hasCodexPluginConfigConflict(currentConfig, value)) return markMigrationItemConflict(item, MIGRATION_REASON_TARGET_EXISTS);
	const migratedItem = {
		...item,
		status: "migrated",
		details: {
			...item.details,
			path: [...CODEX_PLUGIN_CONFIG_PATH],
			value
		}
	};
	if (returnPatch) return migratedItem;
	if (!configApi?.mutateConfigFile) return markMigrationItemError(item, "config runtime unavailable");
	try {
		await configApi.mutateConfigFile({
			base: "runtime",
			afterWrite: { mode: "auto" },
			mutate(draft) {
				if (!ctx.overwrite && hasCodexPluginConfigConflict(draft, value)) throw new CodexPluginConfigConflictError(MIGRATION_REASON_TARGET_EXISTS);
				writeMigrationConfigPath(draft, CODEX_PLUGIN_CONFIG_PATH, value);
			}
		});
		return migratedItem;
	} catch (error) {
		if (error instanceof CodexPluginConfigConflictError) return markMigrationItemConflict(item, error.reason);
		return markMigrationItemError(item, coerceErrorMessage(error));
	}
}
function isCodexPluginConfigTerminal(item) {
	return item.status === "migrated" || item.status === "skipped" && (item.deferredCompletion === true || item.reason === CODEX_PLUGIN_NOT_SELECTED_REASON || item.reason === CODEX_PLUGIN_AUTH_REQUIRED_REASON);
}
function readAppliedPluginConfigEntry(item) {
	if (item.status === "migrated" || item.deferredCompletion === true) return readCodexPluginMigrationConfigEntry(item, true);
	if (item.status === "skipped" && item.reason === CODEX_PLUGIN_AUTH_REQUIRED_REASON) return readCodexPluginMigrationConfigEntry(item, false);
}
function readCodexPluginPolicy(item) {
	const entry = readCodexPluginMigrationConfigEntry(item, true);
	if (!entry) return;
	return {
		configKey: entry.configKey,
		marketplaceName: CODEX_PLUGINS_MARKETPLACE_NAME,
		pluginName: entry.pluginName,
		enabled: true,
		allowDestructiveActions: true,
		destructiveApprovalMode: "allow"
	};
}
//#endregion
export { applyCodexMigrationPlan, prepareTargetCodexAppServer };
