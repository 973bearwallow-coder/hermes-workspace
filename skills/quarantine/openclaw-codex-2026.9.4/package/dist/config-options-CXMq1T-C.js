import { a as normalizeHeaders, d as readNumberEnv, f as readRecord, i as normalizeCodexServiceTier, o as normalizePositiveNumber, p as resolveArgs, r as normalizeCodexAppServerSecretInput, s as readBooleanEnv, t as hashSecretForKey, u as readNonEmptyString } from "./config-utils-DujwEnhg.js";
import { _ as assertCodexAppServerCommandHasNoInlineArgs, d as DEFAULT_CODEX_APP_SERVER_NETWORK_PROXY_PROFILE_PREFIX, f as DEFAULT_CODEX_COMPUTER_USE_LIVE_TEST_TIMEOUT_MS, g as DEFAULT_CODEX_COMPUTER_USE_TOOL_CALL_TIMEOUT_MS, h as DEFAULT_CODEX_COMPUTER_USE_PLUGIN_NAME, l as resolveCodexAppServerUserHomeDir, o as isJsonObject, p as DEFAULT_CODEX_COMPUTER_USE_MARKETPLACE_DISCOVERY_TIMEOUT_MS, s as resolveCodexAppServerHomeDir, x as readCodexPluginConfig } from "./protocol-5bh1G-H7.js";
import { r as readCodexAppServerConfigOptions } from "./launch-args-RXQwn8zV.js";
import { normalizeTrimmedStringList } from "openclaw/plugin-sdk/string-coerce-runtime";
import { createHash } from "node:crypto";
import { AgentHarnessPreflightError } from "openclaw/plugin-sdk/agent-harness-registration";
import { parse } from "smol-toml";
import { readFileSync } from "node:fs";
import path from "node:path";
import { hostname } from "node:os";
import { isLoopbackHost } from "openclaw/plugin-sdk/request-url";
//#region extensions/codex/src/app-server/config-exec-policy.ts
function selectForcedPromptingSandbox(params) {
	if (params.configuredSandbox === "read-only" || params.defaultSandbox === "read-only") return "read-only";
	return params.defaultSandbox ?? "workspace-write";
}
function selectForcedDangerFullAccessSandbox(params) {
	if (params.configuredSandbox === "read-only") return "read-only";
	if (params.defaultPolicy?.dangerFullAccessAllowed === false) {
		if (params.openClawSandboxActive) return params.defaultPolicy.sandbox ?? "workspace-write";
		throw new Error("legacy full exec security with ask requires Codex app-server danger-full-access");
	}
	return "danger-full-access";
}
function selectGuardianSandbox(allowedSandboxModes) {
	if (allowedSandboxModes === void 0 || allowedSandboxModes.has("workspace-write")) return "workspace-write";
	if (allowedSandboxModes.has("read-only")) return "read-only";
	if (allowedSandboxModes.has("danger-full-access")) return "danger-full-access";
	return "workspace-write";
}
function resolveApprovalPolicy(value) {
	if (value === "untrusted") throw new Error("Codex app-server approval policy \"untrusted\" is retired; run \"openclaw doctor --fix\" and use \"on-request\".");
	if (value === "on-failure") return "on-request";
	return value === "on-request" || value === "never" ? value : void 0;
}
function resolveSandbox(value) {
	return value === "read-only" || value === "workspace-write" || value === "danger-full-access" ? value : void 0;
}
function resolveApprovalsReviewer(value) {
	return value === "auto_review" || value === "guardian_subagent" || value === "user" ? value : void 0;
}
function resolveEffectiveOpenClawExecModeForCodexAppServer(params) {
	if (params.execPolicy?.touched === true) return params.execPolicy.mode;
	return params.execMode;
}
function resolveCodexPolicyModeForOpenClawExecMode(mode) {
	if (!mode || mode === "full") return;
	return "guardian";
}
function assertCodexAppServerAllowedForOpenClawExecMode(mode) {
	if (mode === "deny" || mode === "allowlist") throw new AgentHarnessPreflightError(`Codex app-server local execution is unavailable because effective tools.exec.mode=${mode}. Execution-host approvals are authoritative. For gateway turns, inspect them with \`openclaw approvals get --gateway\` and update that same target with \`openclaw approvals set --gateway --stdin\`; for local \`agent exec\`, omit \`--gateway\`. Intentionally align that host policy before retrying.`, { scope: "harness" });
}
//#endregion
//#region extensions/codex/src/app-server/config-requirements.ts
const UNIX_CODEX_REQUIREMENTS_PATH = "/etc/codex/requirements.toml";
const WINDOWS_CODEX_REQUIREMENTS_SUFFIX = "\\OpenAI\\Codex\\requirements.toml";
function readCodexRequirementsToml(params) {
	if (params.requirementsToml !== void 0) return params.requirementsToml ?? void 0;
	const requirementsPath = readNonEmptyString(params.requirementsPath) ?? resolveCodexRequirementsPath(params.env ?? process.env, params.platform ?? process.platform);
	try {
		if (params.readRequirementsFile) return params.readRequirementsFile(requirementsPath);
		return readFileSync(requirementsPath, "utf8");
	} catch {
		return;
	}
}
function resolveCodexRequirementsPath(env, platform) {
	if (platform === "win32") return `${(readNonEmptyString(env.ProgramData) ?? "C:\\ProgramData").replace(/[\\/]+$/, "")}${WINDOWS_CODEX_REQUIREMENTS_SUFFIX}`;
	return UNIX_CODEX_REQUIREMENTS_PATH;
}
function parseAllowedSandboxModesFromCodexRequirements(content, hostName) {
	const remoteSandboxModes = parseMatchingRemoteSandboxModesFromCodexRequirements(content, hostName);
	if (remoteSandboxModes !== void 0) return remoteSandboxModes;
	return parseRequirementsSandboxModes(parseTopLevelRequirementsStringArray(content, "allowed_sandbox_modes"));
}
function parseAllowedApprovalPoliciesFromCodexRequirements(content) {
	const values = parseTopLevelRequirementsStringArray(content, "allowed_approval_policies");
	if (values === void 0) return;
	const normalizedPolicies = values.map((entry) => normalizeRequirementsApprovalPolicy(entry)).filter((entry) => entry !== void 0);
	return normalizedPolicies.length > 0 ? new Set(normalizedPolicies) : void 0;
}
function parseAllowedApprovalsReviewersFromCodexRequirements(content) {
	const values = parseTopLevelRequirementsStringArray(content, "allowed_approvals_reviewers");
	if (values === void 0) return;
	const normalizedReviewers = values.map((entry) => normalizeRequirementsApprovalsReviewer(entry)).filter((entry) => entry !== void 0);
	return normalizedReviewers.length > 0 ? new Set(normalizedReviewers) : void 0;
}
function parseMatchingRemoteSandboxModesFromCodexRequirements(content, hostName) {
	const normalizedHostName = normalizeRequirementsHostName(hostName);
	if (normalizedHostName === void 0) return;
	for (const section of parseTomlArrayTableSections(content, "remote_sandbox_config")) {
		const patterns = parseRequirementsStringArray(section, "hostname_patterns");
		if (!patterns || !requirementsHostNameMatchesAnyPattern(normalizedHostName, patterns)) continue;
		return parseRequirementsSandboxModes(parseRequirementsStringArray(section, "allowed_sandbox_modes"));
	}
}
function parseRequirementsSandboxModes(values) {
	if (values === void 0) return;
	const normalizedModes = values.map((entry) => normalizeRequirementsSandboxMode(entry)).filter((entry) => entry !== void 0);
	return normalizedModes.length > 0 ? new Set(normalizedModes) : void 0;
}
function parseTopLevelRequirementsStringArray(content, key) {
	return parseRequirementsStringArray(stripTomlLineComments(content).slice(0, firstTomlTableOffset(content)), key);
}
function parseTomlStringValue(content, key) {
	return parseTomlStringAssignmentValue(content, tomlDottedKeyPattern(key));
}
function parseInlineOpenAIModelProviderBaseUrl(content) {
	return parseTomlStringAssignmentValue(content, `${tomlKeyPattern("model_providers")}\\s*=\\s*\\{[\\s\\S]*?${tomlKeyPattern("openai")}\\s*=\\s*\\{[\\s\\S]*?${tomlKeyPattern("base_url")}`);
}
function parseTomlStringAssignmentValue(content, keyPattern) {
	const assignment = content.match(new RegExp(`(?:^|\\n)\\s*${keyPattern}\\s*=\\s*([^\\r\\n]*)`));
	if (!assignment) return;
	const rawValue = assignment[1]?.trimStart() ?? "";
	if (rawValue.startsWith("\"\"\"") || rawValue.startsWith("'''")) return false;
	const match = parseTomlStringAssignment(content, keyPattern);
	return match ? match[1] ?? match[2] ?? "" : false;
}
function parseTomlStringAssignment(content, keyPattern) {
	return content.match(new RegExp(`(?:^|\\n)\\s*${keyPattern}\\s*=\\s*(?:"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"|'([^']*)')`));
}
function tomlDottedKeyPattern(key) {
	return key.split(".").map(tomlKeyPattern).join("\\s*\\.\\s*");
}
function tomlKeyPattern(key) {
	const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	return `(?:"${escaped}"|'${escaped}'|${escaped})`;
}
function parseRequirementsStringArray(content, key) {
	const match = content.match(new RegExp(`(?:^|\\n)\\s*${key}\\s*=\\s*\\[([\\s\\S]*?)\\]`));
	if (!match) return;
	const arrayBody = match[1] ?? "";
	const stringMatches = [...arrayBody.matchAll(/"([^"\\]*(?:\\.[^"\\]*)*)"|'([^']*)'/g)];
	if (stringMatches.length === 0 && arrayBody.trim().length > 0) return;
	return stringMatches.map((entry) => entry[1] ?? entry[2] ?? "");
}
function parseTomlTableSection(content, table) {
	const strippedContent = stripTomlLineComments(content);
	const tablePattern = tomlDottedKeyPattern(table);
	const match = new RegExp(`^\\s*\\[\\s*${tablePattern}\\s*\\]\\s*$`, "m").exec(strippedContent);
	if (!match) return;
	const sectionStart = match.index + match[0].length;
	const rest = strippedContent.slice(sectionStart);
	const nextTableOffset = rest.search(/^\s*\[/m);
	return nextTableOffset === -1 ? rest : rest.slice(0, nextTableOffset);
}
function parseTomlArrayTableSections(content, table) {
	const strippedContent = stripTomlLineComments(content);
	const escapedTable = table.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	const headerPattern = new RegExp(`^\\s*\\[\\[\\s*${escapedTable}\\s*\\]\\]\\s*$`, "gm");
	const sections = [];
	for (let match = headerPattern.exec(strippedContent); match; match = headerPattern.exec(strippedContent)) {
		const sectionStart = headerPattern.lastIndex;
		const rest = strippedContent.slice(sectionStart);
		const nextTableOffset = rest.search(/^\s*\[/m);
		sections.push(nextTableOffset === -1 ? rest : rest.slice(0, nextTableOffset));
	}
	return sections;
}
function firstTomlTableOffset(content) {
	return content.match(/^\s*\[[^\]\n]/m)?.index ?? content.length;
}
function stripTomlLineComments(value) {
	let output = "";
	let quote;
	let escaped = false;
	for (let index = 0; index < value.length; index += 1) {
		const char = value[index] ?? "";
		if (quote) {
			output += char;
			if (quote === "\"" && escaped) {
				escaped = false;
				continue;
			}
			if (quote === "\"" && char === "\\") {
				escaped = true;
				continue;
			}
			if (char === quote) quote = void 0;
			continue;
		}
		if (char === "\"" || char === "'") {
			quote = char;
			output += char;
			continue;
		}
		if (char === "#") {
			while (index < value.length && value[index] !== "\n") index += 1;
			if (value[index] === "\n") output += "\n";
			continue;
		}
		output += char;
	}
	return output;
}
function normalizeRequirementsSandboxMode(value) {
	const compact = value.replace(/[\s_-]/g, "").toLowerCase();
	if (compact === "readonly") return "read-only";
	if (compact === "workspacewrite") return "workspace-write";
	if (compact === "dangerfullaccess") return "danger-full-access";
}
function normalizeRequirementsHostName(value) {
	const normalized = value.trim().replace(/\.+$/g, "").toLowerCase();
	return normalized.length > 0 ? normalized : void 0;
}
function requirementsHostNameMatchesAnyPattern(hostName, patterns) {
	return patterns.some((pattern) => {
		const normalizedPattern = normalizeRequirementsHostName(pattern);
		return normalizedPattern !== void 0 && globPatternMatches(hostName, normalizedPattern);
	});
}
function globPatternMatches(value, pattern) {
	let regex = "^";
	for (const char of pattern) if (char === "*") regex += ".*";
	else if (char === "?") regex += ".";
	else regex += char.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
	regex += "$";
	return new RegExp(regex).test(value);
}
function normalizeRequirementsApprovalPolicy(value) {
	const normalized = value.trim().toLowerCase();
	if (normalized === "on-failure") return "on-request";
	if (normalized === "untrusted") return normalized;
	return resolveApprovalPolicy(normalized);
}
function normalizeRequirementsApprovalsReviewer(value) {
	return resolveApprovalsReviewer(value.trim().toLowerCase());
}
function selectGuardianApprovalPolicy(allowedApprovalPolicies, execModeRequiringPromptingApprovals) {
	if (allowedApprovalPolicies === void 0 || allowedApprovalPolicies.has("on-request")) return "on-request";
	if (allowedApprovalPolicies.has("untrusted")) return "untrusted";
	if (execModeRequiringPromptingApprovals) throw new Error(`tools.exec.mode=${execModeRequiringPromptingApprovals} requires Codex app-server prompting approvals`);
	if (allowedApprovalPolicies.has("never")) return "never";
	return "on-request";
}
function selectGuardianApprovalsReviewer(allowedApprovalsReviewers, execModeRequiringAutoReviewer) {
	if (allowedApprovalsReviewers === void 0 || allowedApprovalsReviewers.has("auto_review")) return "auto_review";
	if (allowedApprovalsReviewers.has("guardian_subagent")) return "guardian_subagent";
	if (execModeRequiringAutoReviewer) throw new Error(`tools.exec.mode=${execModeRequiringAutoReviewer} requires Codex app-server auto approvals`);
	if (allowedApprovalsReviewers.has("user")) return "user";
	return "auto_review";
}
function selectUserApprovalsReviewer(allowedApprovalsReviewers, execModeRequiringUserReviewer) {
	if (allowedApprovalsReviewers === void 0 || allowedApprovalsReviewers.has("user")) return "user";
	throw new Error(`tools.exec.mode=${execModeRequiringUserReviewer ?? "ask"} requires Codex app-server user approvals`);
}
//#endregion
//#region extensions/codex/src/app-server/config-layer-policy.ts
const CODEX_SESSION_OVERRIDABLE_LAYER_TYPES = /* @__PURE__ */ new Set([
	"packagedDefaults",
	"mdm",
	"system",
	"enterpriseManaged",
	"user",
	"project",
	"sessionFlags"
]);
/** Read one effective snapshot for the current boundary's reviewer and tool-policy checks. */
async function readCodexEffectiveConfig(client, cwd, options) {
	const response = await client.request("config/read", {
		cwd: path.resolve(cwd),
		includeLayers: true
	}, options);
	if (!isJsonObject(response) || !isJsonObject(response.config)) throw new Error("Codex config/read returned an invalid effective config");
	return response;
}
//#endregion
//#region extensions/codex/src/app-server/config-reviewer-policy.ts
const CODEX_CONFIG_TOML_FILENAME = "config.toml";
/** Cloud/system config can redirect reviews after local home/profile checks have passed. */
async function assertCodexModelBackedReviewerEffectiveConfig(params) {
	if (params.approvalsReviewer !== "auto_review" && params.approvalsReviewer !== "guardian_subagent") return;
	const response = await readCodexEffectiveConfig(params.client, params.cwd, { signal: params.signal });
	const effectiveConfig = response.config;
	const modelProvider = effectiveConfig.model_provider;
	const providers = effectiveConfig.model_providers;
	const providerRecords = providers == null ? void 0 : readRecord(providers);
	const provider = providerRecords?.openai;
	const openAIProvider = provider == null ? void 0 : readRecord(provider);
	if (modelProvider != null && modelProvider !== "openai" || providers != null && !providerRecords || provider != null && !openAIProvider || !isTrustedOptionalReviewerEndpoint(effectiveConfig.openai_base_url, isNativeOpenAIBaseUrl) || !isTrustedOptionalReviewerEndpoint(effectiveConfig.chatgpt_base_url, isNativeChatGPTBaseUrl) || !isTrustedOptionalReviewerEndpoint(openAIProvider?.base_url, isNativeOpenAIBaseUrl)) throw new Error("Codex model-backed approval reviewer requires the running server to use a trusted OpenAI endpoint");
	return response;
}
function isTrustedOptionalReviewerEndpoint(value, isTrusted) {
	return value == null || typeof value === "string" && isTrusted(value);
}
function canUseCodexModelBackedApprovalsReviewerForModel(params, resolveAuthProviderId) {
	const explicitProvider = params.modelProvider?.trim().toLowerCase();
	const inferredProvider = inferProviderFromModelRef(params.model);
	if (explicitProvider && explicitProvider !== "codex" && explicitProvider !== "openai") return false;
	return (inferredProvider ?? explicitProvider) === "openai" && isTrustedCodexModelBackedOpenAIProvider(params, resolveAuthProviderId);
}
function isTrustedCodexModelBackedOpenAIProvider(params, resolveAuthProviderId) {
	if (!openAIBaseUrlEnvOverridesAreTrustedForModelBackedReview(params.env)) return false;
	const codexBaseUrlOverrides = readCodexBaseUrlOverridesForModelBackedReview(params);
	if (codexBaseUrlOverrides === false || !codexBaseUrlOverrides.openAI.every(isNativeOpenAIBaseUrl) || !codexBaseUrlOverrides.chatGPT.every(isNativeChatGPTBaseUrl)) return false;
	const openAIProviders = readConfiguredOpenAIProvidersForModelBackedReview(params.config, resolveAuthProviderId);
	if (openAIProviders.length === 0) return true;
	return openAIProviders.every((openAIProvider) => configuredOpenAIProviderIsTrustedForModelBackedReview(openAIProvider, params.model));
}
function resolveCodexModelBackedReviewerPolicyContext(params) {
	const provider = params.provider?.trim();
	if (provider && provider.toLowerCase() !== "codex") return {
		modelProvider: normalizeCodexModelBackedReviewerPolicyProvider(provider),
		model: params.model
	};
	const bindingModelProvider = params.bindingModelProvider?.trim();
	const currentModel = params.model?.trim();
	const bindingModel = params.bindingModel?.trim();
	if (bindingModelProvider && currentModel && bindingModel && currentModel === bindingModel) return {
		modelProvider: normalizeCodexModelBackedReviewerPolicyProvider(bindingModelProvider),
		model: params.model ?? params.bindingModel
	};
	const currentModelProvider = inferProviderFromModelRef(params.model);
	if (currentModelProvider) return {
		modelProvider: normalizeCodexModelBackedReviewerPolicyProvider(currentModelProvider),
		model: params.model
	};
	if (bindingModelProvider) return {
		modelProvider: normalizeCodexModelBackedReviewerPolicyProvider(bindingModelProvider),
		model: params.model ?? params.bindingModel
	};
	return {
		modelProvider: params.nativeAuthProfile === true ? "openai" : void 0,
		model: params.model ?? params.bindingModel
	};
}
function readCodexBaseUrlOverridesForModelBackedReview(params) {
	const configToml = readCodexAppServerConfigToml(params);
	if (configToml === false) return false;
	const configTomls = configToml === void 0 ? [] : [configToml];
	const nativeOverrides = readNativeCodexReviewerConfigOverrides(params);
	if (nativeOverrides === false) return false;
	configTomls.push(...nativeOverrides);
	const openAI = [];
	const chatGPT = [];
	for (const content of configTomls) {
		const topLevelContent = stripTomlLineComments(content).slice(0, firstTomlTableOffset(content));
		const modelProviderOpenAISection = parseTomlTableSection(content, "model_providers.openai");
		const modelProvider = parseTomlStringValue(topLevelContent, "model_provider");
		if (modelProvider === false || modelProvider && modelProvider !== "openai") return false;
		openAI.push(parseTomlStringValue(topLevelContent, "openai_base_url"), parseTomlStringValue(topLevelContent, "model_providers.openai.base_url"), parseInlineOpenAIModelProviderBaseUrl(topLevelContent), modelProviderOpenAISection ? parseTomlStringValue(modelProviderOpenAISection, "base_url") : void 0);
		chatGPT.push(parseTomlStringValue(topLevelContent, "chatgpt_base_url"));
	}
	if ([...openAI, ...chatGPT].includes(false)) return false;
	return {
		openAI: openAI.filter((entry) => typeof entry === "string"),
		chatGPT: chatGPT.filter((entry) => typeof entry === "string")
	};
}
function readNativeCodexReviewerConfigOverrides(params) {
	if (params.codexArgs?.some((arg) => !arg)) return false;
	const overrides = [];
	let profile;
	for (const { name, value } of readCodexAppServerConfigOptions(params.codexArgs ?? [])) {
		if (!value) return false;
		if (name === "--profile" || name === "-p") profile = value;
		else overrides.push(`${value}\n`);
	}
	if (profile) {
		if (path.basename(profile) !== profile || profile === "." || profile === "..") return false;
		const configPath = resolveCodexAppServerConfigPath(params);
		if (!configPath) return false;
		try {
			overrides.unshift(readFileSync(path.join(path.dirname(configPath), `${profile}.config.toml`), "utf8"));
		} catch (error) {
			if (readErrorCode(error) !== "ENOENT") return false;
		}
	}
	return overrides;
}
function readCodexAppServerConfigToml(params) {
	if (params.codexConfigToml !== void 0) return params.codexConfigToml ?? void 0;
	const configPath = resolveCodexAppServerConfigPath(params);
	if (!configPath) return;
	try {
		return readFileSync(configPath, "utf8");
	} catch (error) {
		return readErrorCode(error) === "ENOENT" ? void 0 : false;
	}
}
function codexConfigEnablesNativeComputerUse(params) {
	const configToml = readCodexAppServerConfigToml(params);
	if (configToml === false) return true;
	if (configToml === void 0) return false;
	let parsedConfig;
	try {
		parsedConfig = parse(configToml, { integersAsBigInt: true });
	} catch {
		return true;
	}
	const rawPlugins = parsedConfig.plugins;
	if (rawPlugins === void 0) return false;
	const plugins = readRecord(rawPlugins);
	if (!plugins) return true;
	for (const [pluginId, rawPluginConfig] of Object.entries(plugins)) {
		if (!params.pluginNames.some((pluginName) => pluginId === pluginName || pluginId.startsWith(`${pluginName}@`))) continue;
		const pluginConfig = readRecord(rawPluginConfig);
		if (!pluginConfig) return true;
		if (pluginConfig.enabled === false) continue;
		return true;
	}
	return false;
}
function resolveCodexAppServerConfigPath(params) {
	if (params.homeScope === "user") return path.join(resolveCodexAppServerUserHomeDir(params.env), CODEX_CONFIG_TOML_FILENAME);
	const agentDir = readNonEmptyString(params.agentDir);
	return agentDir ? path.join(resolveCodexAppServerHomeDir(agentDir), CODEX_CONFIG_TOML_FILENAME) : void 0;
}
function readErrorCode(error) {
	return error && typeof error === "object" && "code" in error ? String(error.code) : void 0;
}
function readConfiguredOpenAIProvidersForModelBackedReview(config, resolveAuthProviderId) {
	const providerRecords = readRecord(readRecord(readRecord(config)?.models)?.providers);
	if (!providerRecords) return [];
	const openAIProviders = [];
	for (const [providerId, providerConfig] of Object.entries(providerRecords)) {
		if (resolveAuthProviderId(providerId, { config }) !== "openai") continue;
		const record = readRecord(providerConfig);
		if (record) openAIProviders.push(record);
	}
	return openAIProviders;
}
function configuredOpenAIProviderIsTrustedForModelBackedReview(openAIProvider, modelInput) {
	if (readRecord(openAIProvider.localService) || hasNonEmptyRecord(openAIProvider.headers) || hasNonEmptyRecord(openAIProvider.request) || typeof openAIProvider.authHeader === "boolean" || !isNativeOpenAIBaseUrl(openAIProvider.baseUrl)) return false;
	const models = openAIProvider.models;
	if (!Array.isArray(models)) return true;
	const modelId = normalizeOpenAIModelBackedReviewerModelId(modelInput);
	if (!modelId) return false;
	for (const entry of models) {
		const model = readRecord(entry);
		if (typeof model?.id !== "string" || !matchesConfiguredOpenAIModelId(modelId, model.id)) continue;
		if (hasNonEmptyRecord(model.headers) || hasNonEmptyRecord(model.request) || !isNativeOpenAIBaseUrl(model.baseUrl)) return false;
	}
	return true;
}
function normalizeOpenAIModelBackedReviewerModelId(modelInput) {
	const normalized = modelInput?.trim() ?? "";
	const authProfileIndex = normalized.indexOf("@");
	const withoutAuthProfile = authProfileIndex > 0 ? normalized.slice(0, authProfileIndex) : normalized;
	const slashIndex = withoutAuthProfile.indexOf("/");
	return slashIndex > 0 ? withoutAuthProfile.slice(slashIndex + 1).trim() : withoutAuthProfile;
}
function matchesConfiguredOpenAIModelId(modelId, configuredModelId) {
	const configured = normalizeOpenAIModelBackedReviewerModelId(configuredModelId);
	return Boolean(configured) && (modelId === configured || modelId.startsWith(`${configured}@`));
}
function hasNonEmptyRecord(value) {
	const record = readRecord(value);
	return record !== void 0 && Object.keys(record).length > 0;
}
function isNativeOpenAIBaseUrl(value) {
	if (typeof value !== "string" || !value.trim()) return true;
	try {
		const url = new URL(value);
		return url.protocol === "https:" && url.hostname.toLowerCase() === "api.openai.com";
	} catch {
		return false;
	}
}
function openAIBaseUrlEnvOverridesAreTrustedForModelBackedReview(env) {
	return [env?.OPENAI_BASE_URL, env?.OPENAI_API_BASE].every(isNativeOpenAIBaseUrl);
}
function isNativeChatGPTBaseUrl(value) {
	if (typeof value !== "string" || !value.trim()) return true;
	try {
		const url = new URL(value);
		return url.protocol === "https:" && url.hostname.toLowerCase() === "chatgpt.com";
	} catch {
		return false;
	}
}
function normalizeCodexModelBackedReviewerPolicyProvider(provider) {
	return provider.toLowerCase() === "openai" ? "openai" : provider;
}
function inferProviderFromModelRef(model) {
	const normalized = model?.trim().toLowerCase();
	const slashIndex = normalized?.indexOf("/") ?? -1;
	return slashIndex > 0 ? normalized?.slice(0, slashIndex) : void 0;
}
//#endregion
//#region extensions/codex/src/app-server/config-security.ts
function shouldAutoApproveCodexAppServerApprovals(appServer) {
	return appServer.networkProxy === void 0 && appServer.approvalPolicy === "never" && appServer.sandbox === "danger-full-access";
}
function resolveCodexAppServerNetworkProxy(config, sandbox) {
	if (config?.enabled !== true) return {};
	const fileSystemMode = config.baseProfile === "read-only" || !config.baseProfile && sandbox === "read-only" ? "read" : "write";
	const networkConfig = removeUndefinedJsonFields({
		enabled: true,
		mode: config.mode,
		domains: normalizeNetworkProxyPermissionMap(config.domains),
		unix_sockets: normalizeNetworkProxyPermissionMap(config.unixSockets),
		proxy_url: readNonEmptyString(config.proxyUrl),
		socks_url: readNonEmptyString(config.socksUrl),
		enable_socks5: config.enableSocks5,
		enable_socks5_udp: config.enableSocks5Udp,
		allow_upstream_proxy: config.allowUpstreamProxy,
		allow_local_binding: config.allowLocalBinding,
		dangerously_allow_non_loopback_proxy: config.dangerouslyAllowNonLoopbackProxy,
		dangerously_allow_all_unix_sockets: config.dangerouslyAllowAllUnixSockets
	});
	const profile = {
		filesystem: {
			":minimal": "read",
			":project_roots": { ".": fileSystemMode }
		},
		network: networkConfig
	};
	const profileName = resolveNetworkProxyPermissionProfileName(config, profile);
	const configPatch = {
		"features.network_proxy.enabled": true,
		default_permissions: profileName,
		permissions: { [profileName]: profile }
	};
	return { networkProxy: {
		profileName,
		configFingerprint: fingerprintCodexAppServerNetworkProxyConfigPatch(configPatch),
		configPatch
	} };
}
function resolveNetworkProxyPermissionProfileName(config, profile) {
	const explicitProfileName = readNonEmptyString(config.profileName);
	if (explicitProfileName) return explicitProfileName;
	const suffix = createHash("sha256").update(stableStringifyJson({
		version: 1,
		profile
	})).digest("hex").slice(0, 16);
	return `${DEFAULT_CODEX_APP_SERVER_NETWORK_PROXY_PROFILE_PREFIX}-${suffix}`;
}
function fingerprintCodexAppServerNetworkProxyConfigPatch(configPatch) {
	return createHash("sha256").update(stableStringifyJson(configPatch)).digest("hex");
}
function normalizeNetworkProxyPermissionMap(value) {
	const entries = Object.entries(value ?? {}).map(([key, permission]) => [key.trim(), permission]).filter(([key]) => key.length > 0);
	return entries.length > 0 ? Object.fromEntries(entries) : void 0;
}
function removeUndefinedJsonFields(value) {
	return Object.fromEntries(Object.entries(value).filter((entry) => entry[1] !== void 0));
}
function stableStringifyJson(value) {
	if (Array.isArray(value)) return `[${value.map((item) => stableStringifyJson(item)).join(",")}]`;
	if (value && typeof value === "object") return `{${Object.entries(value).toSorted(([left], [right]) => left.localeCompare(right)).map(([key, item]) => `${JSON.stringify(key)}:${stableStringifyJson(item)}`).join(",")}}`;
	return JSON.stringify(value);
}
/** Explicit MCP prompting must bypass Codex's unconditional Never-policy approval. */
function hasCodexMcpToolApprovalOverrides(servers, serverNames, projectedMcpServers) {
	const modes = new Map(Object.entries(projectedMcpServers ?? {}).map(([name, server]) => [name, server.default_tools_approval_mode]));
	for (const name of serverNames ?? Object.keys(servers ?? {})) {
		const server = servers?.[name];
		const mode = server?.codex?.defaultToolsApprovalMode;
		if (mode !== void 0 && (serverNames !== void 0 || server?.enabled !== false)) modes.set(name, mode);
	}
	return [...modes.values()].some((mode) => mode === "auto" || mode === "prompt");
}
function withMcpElicitationsApprovalPolicy(policy) {
	if (policy === "untrusted") return policy;
	if (typeof policy !== "string") return { granular: {
		...policy.granular,
		mcp_elicitations: true
	} };
	if (policy === "never") return { granular: {
		mcp_elicitations: true,
		rules: false,
		sandbox_approval: false,
		request_permissions: false,
		skill_approval: false
	} };
	return { granular: {
		mcp_elicitations: true,
		rules: true,
		sandbox_approval: true,
		request_permissions: true,
		skill_approval: true
	} };
}
function resolveTransport(value) {
	return value === "websocket" || value === "unix" ? value : "stdio";
}
function normalizeRemoteWorkspaceRoot(value) {
	return readNonEmptyString(value);
}
function inferCodexAppServerConnectionClass(params) {
	if (params.transport !== "websocket") return "local-loopback";
	return params.url && isLoopbackWebSocketUrl(params.url) ? "local-loopback" : "remote";
}
function assertCodexAppServerConnectionClassConfig(params) {
	if (params.connectionClass === "remote" && !hasIdentityBearingWebSocketAuth({
		authToken: params.authToken,
		headers: params.headers
	})) throw new Error("remote Codex app-server WebSocket URLs require appServer.authToken or an Authorization header");
}
/** Applies the canonical remote-auth boundary to any Codex AppServer transport. */
function assertCodexAppServerConnectionSecurity(params) {
	assertCodexAppServerConnectionClassConfig({
		connectionClass: inferCodexAppServerConnectionClass(params),
		authToken: params.authToken,
		headers: params.headers
	});
}
function isLoopbackWebSocketUrl(value) {
	let parsed;
	try {
		parsed = new URL(value);
	} catch {
		return false;
	}
	if (parsed.protocol !== "ws:" && parsed.protocol !== "wss:") return false;
	return isLoopbackHost(parsed.hostname);
}
function hasIdentityBearingWebSocketAuth(params) {
	if (readNonEmptyString(params.authToken)) return true;
	return Object.entries(params.headers).some(([key, value]) => key.trim().toLowerCase() === "authorization" && Boolean(readNonEmptyString(value)));
}
function resolvePolicyMode(value) {
	return value === "guardian" || value === "yolo" ? value : void 0;
}
function resolveDefaultCodexAppServerPolicy(params) {
	if (params.transport !== "stdio") return {
		mode: "yolo",
		dangerFullAccessAllowed: true
	};
	const content = readCodexRequirementsToml(params);
	if (content === void 0) {
		if (!params.forceGuardian) return {
			mode: "yolo",
			dangerFullAccessAllowed: true
		};
		return {
			mode: "guardian",
			dangerFullAccessAllowed: true,
			approvalPolicy: selectGuardianApprovalPolicy(void 0, params.execModeRequiringPromptingApprovals),
			approvalsReviewer: params.forceUserReviewer ? selectUserApprovalsReviewer(void 0, params.execModeRequiringUserReviewer) : selectGuardianApprovalsReviewer(void 0, params.execModeRequiringPromptingApprovals === "auto" ? "auto" : void 0),
			sandbox: selectGuardianSandbox(void 0)
		};
	}
	const allowedSandboxModes = parseAllowedSandboxModesFromCodexRequirements(content, readNonEmptyString(params.hostName) ?? hostname());
	const allowedApprovalPolicies = parseAllowedApprovalPoliciesFromCodexRequirements(content);
	const allowedApprovalsReviewers = parseAllowedApprovalsReviewersFromCodexRequirements(content);
	const yoloSandboxAllowed = allowedSandboxModes === void 0 || allowedSandboxModes.has("danger-full-access");
	const yoloApprovalAllowed = allowedApprovalPolicies === void 0 || allowedApprovalPolicies.has("never") && !allowedApprovalPolicies.has("untrusted");
	const yoloReviewerAllowed = allowedApprovalsReviewers === void 0 || allowedApprovalsReviewers.has("user");
	if (!params.forceGuardian && yoloSandboxAllowed && yoloApprovalAllowed && yoloReviewerAllowed) return {
		mode: "yolo",
		dangerFullAccessAllowed: true
	};
	return {
		mode: "guardian",
		dangerFullAccessAllowed: yoloSandboxAllowed,
		approvalPolicy: selectGuardianApprovalPolicy(allowedApprovalPolicies, params.execModeRequiringPromptingApprovals),
		approvalsReviewer: params.forceUserReviewer ? selectUserApprovalsReviewer(allowedApprovalsReviewers, params.execModeRequiringUserReviewer) : selectGuardianApprovalsReviewer(allowedApprovalsReviewers, params.execModeRequiringPromptingApprovals === "auto" ? "auto" : void 0),
		sandbox: selectGuardianSandbox(allowedSandboxModes)
	};
}
//#endregion
//#region extensions/codex/src/app-server/config-options.ts
/**
* Sole owner of the app-server home-scope decision. Ordinary harness connections
* default to the isolated agent home; the supervision connection owns the operator's
* native Codex home on local transports. Auth handoffs must read the scope from here
* (or from resolved start options) because a prepared login on a native home rewrites
* the account Codex CLI and Desktop share.
*/
function resolveCodexAppServerHomeScope(params) {
	const configured = params.appServer?.homeScope;
	if (configured) return configured;
	return params.connectionScope === "supervision" && resolveTransport(params.appServer?.transport) !== "websocket" ? "user" : "agent";
}
function createCodexAppServerConfig({ resolveProviderIdForAuth }) {
	function resolveCodexAppServerRuntimeOptions(params = {}) {
		const env = params.env ?? process.env;
		const pluginConfig = readCodexPluginConfig(params.pluginConfig);
		const config = pluginConfig.appServer ?? {};
		const transport = resolveTransport(config.transport);
		const homeScope = resolveCodexAppServerHomeScope({ appServer: config });
		if (transport !== "stdio" && pluginConfig.sessionCatalog?.homes?.length) throw new Error("plugins.entries.codex.config.sessionCatalog.homes requires appServer.transport=stdio");
		const configCommand = readNonEmptyString(config.command);
		const envCommand = readNonEmptyString(env.OPENCLAW_CODEX_APP_SERVER_BIN);
		const command = configCommand ?? envCommand ?? "codex";
		const commandSource = configCommand ? "config" : envCommand ? "env" : "managed";
		if (commandSource === "config" || commandSource === "env") assertCodexAppServerCommandHasNoInlineArgs({
			command,
			source: commandSource
		});
		const args = resolveArgs(config.args, env.OPENCLAW_CODEX_APP_SERVER_ARGS);
		const headers = normalizeHeaders(config.headers);
		const clearEnv = normalizeTrimmedStringList(config.clearEnv);
		const authToken = normalizeCodexAppServerSecretInput({
			value: config.authToken,
			path: "plugins.entries.codex.config.appServer.authToken"
		});
		const url = readNonEmptyString(config.url) ?? (transport === "unix" ? "unix://" : void 0);
		const connectionClass = inferCodexAppServerConnectionClass({
			transport,
			url
		});
		const remoteAppsSubstrate = "preconfigured";
		const remoteWorkspaceRoot = normalizeRemoteWorkspaceRoot(config.remoteWorkspaceRoot);
		const execMode = resolveEffectiveOpenClawExecModeForCodexAppServer({
			execMode: params.execMode,
			execPolicy: params.execPolicy
		});
		if (!params.sessionPermissionMode) assertCodexAppServerAllowedForOpenClawExecMode(execMode);
		const explicitPolicyMode = resolvePolicyMode(config.mode) ?? resolvePolicyMode(env.OPENCLAW_CODEX_APP_SERVER_MODE);
		const configuredSandbox = resolveSandbox(config.sandbox) ?? resolveSandbox(env.OPENCLAW_CODEX_APP_SERVER_SANDBOX);
		const explicitApprovalsReviewer = resolveApprovalsReviewer(config.approvalsReviewer);
		const normalizedPolicyMode = resolveCodexPolicyModeForOpenClawExecMode(execMode);
		const ignoreLegacyYoloPolicyMode = normalizedPolicyMode === "guardian" && explicitPolicyMode === "yolo";
		const canUseModelBackedReviewer = canUseCodexModelBackedApprovalsReviewerForModel({
			modelProvider: params.modelProvider,
			model: params.model,
			config: params.config,
			env,
			agentDir: params.agentDir,
			codexConfigToml: params.codexConfigToml,
			homeScope
		}, resolveProviderIdForAuth);
		const forceUserReviewer = !canUseModelBackedReviewer && (explicitApprovalsReviewer === "auto_review" || explicitApprovalsReviewer === "guardian_subagent" || explicitPolicyMode === "guardian" && explicitApprovalsReviewer !== "user") || execMode !== void 0 && execMode !== "full" && (execMode !== "auto" || !canUseModelBackedReviewer);
		const forceGuardianReviewer = execMode === "auto" && canUseModelBackedReviewer;
		const execModeRequiringPromptingApprovals = execMode === "auto" || execMode === "ask" ? execMode : forceUserReviewer ? "ask" : void 0;
		const forceDangerFullAccessSandbox = params.execPolicy?.touched === true && params.execPolicy.security === "full" && params.execPolicy.ask === "always";
		const forcePerCommandApprovals = params.execPolicy?.ask === "always";
		const requirementsToml = forcePerCommandApprovals ? readCodexRequirementsToml({
			env,
			requirementsToml: params.requirementsToml,
			requirementsPath: params.requirementsPath,
			readRequirementsFile: params.readRequirementsFile,
			platform: params.platform
		}) ?? null : params.requirementsToml;
		if (forcePerCommandApprovals && requirementsToml && parseAllowedApprovalPoliciesFromCodexRequirements(requirementsToml)?.has("untrusted") === false) throw new Error("tools.exec.ask=always requires Codex app-server per-command approvals");
		const forceRuntimePolicy = forceUserReviewer || forceGuardianReviewer || forceDangerFullAccessSandbox;
		const defaultPolicy = explicitPolicyMode && !forceRuntimePolicy && !ignoreLegacyYoloPolicyMode ? void 0 : resolveDefaultCodexAppServerPolicy({
			transport,
			env,
			forceGuardian: normalizedPolicyMode === "guardian",
			forceUserReviewer: forceUserReviewer || !canUseModelBackedReviewer,
			execModeRequiringPromptingApprovals,
			requirementsToml,
			requirementsPath: params.requirementsPath,
			readRequirementsFile: params.readRequirementsFile,
			platform: params.platform,
			hostName: params.hostName,
			execModeRequiringUserReviewer: forceUserReviewer ? execMode : void 0
		});
		const preserveExplicitAutoSandbox = forceGuardianReviewer && configuredSandbox === "read-only";
		const forcedPolicy = forceRuntimePolicy ? {
			approvalPolicy: forcePerCommandApprovals ? "untrusted" : defaultPolicy?.approvalPolicy ?? "on-request",
			sandbox: preserveExplicitAutoSandbox ? void 0 : forceDangerFullAccessSandbox ? selectForcedDangerFullAccessSandbox({
				configuredSandbox,
				defaultPolicy,
				openClawSandboxActive: Boolean(params.openClawSandboxActive)
			}) : selectForcedPromptingSandbox({
				configuredSandbox,
				defaultSandbox: defaultPolicy?.sandbox
			}),
			approvalsReviewer: defaultPolicy?.approvalsReviewer ?? (forceUserReviewer ? "user" : "auto_review")
		} : void 0;
		const policyMode = ignoreLegacyYoloPolicyMode ? normalizedPolicyMode : explicitPolicyMode ?? normalizedPolicyMode ?? defaultPolicy?.mode ?? "yolo";
		const serviceTier = normalizeCodexServiceTier(config.serviceTier);
		const resolvedSandbox = forcedPolicy?.sandbox ?? configuredSandbox ?? defaultPolicy?.sandbox ?? (policyMode === "guardian" ? "workspace-write" : "danger-full-access");
		if (transport === "websocket" && !url) throw new Error("plugins.entries.codex.config.appServer.url is required when appServer.transport is websocket");
		if (transport === "websocket" && homeScope === "user") throw new Error("plugins.entries.codex.config.appServer.homeScope=user requires appServer.transport=stdio or unix");
		if (transport === "unix" && homeScope !== "user") throw new Error("plugins.entries.codex.config.appServer.transport=unix requires appServer.homeScope=user");
		if (transport === "unix" && !url?.startsWith("unix://")) throw new Error("plugins.entries.codex.config.appServer.url must use unix:// when appServer.transport is unix");
		assertCodexAppServerConnectionSecurity({
			transport,
			url,
			authToken,
			headers
		});
		const configApprovalPolicy = resolveApprovalPolicy(config.approvalPolicy);
		const envApprovalPolicy = resolveApprovalPolicy(env.OPENCLAW_CODEX_APP_SERVER_APPROVAL_POLICY);
		const approvalPolicy = configApprovalPolicy ?? envApprovalPolicy ?? defaultPolicy?.approvalPolicy ?? (policyMode === "guardian" ? "on-request" : "never");
		const approvalPolicySource = configApprovalPolicy ? "config" : envApprovalPolicy ? "env" : defaultPolicy?.approvalPolicy ? "requirements" : "implicit";
		const computerUseConfig = resolveCodexComputerUseConfig({
			pluginConfig: params.pluginConfig,
			env
		});
		const managedCommandOrder = params.managedCommandOrder ?? (homeScope === "user" || computerUseConfig.enabled ? "desktop-first" : "package-first");
		const includeManagedCommandOrder = commandSource === "managed" && (managedCommandOrder === "desktop-first" || params.managedCommandOrder === "package-first");
		const managedComputerUsePluginNames = [.../* @__PURE__ */ new Set([DEFAULT_CODEX_COMPUTER_USE_PLUGIN_NAME, computerUseConfig.pluginName])];
		return {
			start: {
				transport,
				homeScope,
				command,
				commandSource,
				...includeManagedCommandOrder ? { managedCommandOrder } : {},
				...commandSource === "managed" ? { managedComputerUsePluginNames } : {},
				args: args.length > 0 ? args : [
					"app-server",
					"--listen",
					"stdio://"
				],
				...url ? { url } : {},
				...authToken ? { authToken } : {},
				headers,
				...transport === "stdio" && clearEnv.length > 0 ? { clearEnv } : {}
			},
			connectionClass,
			remoteAppsSubstrate,
			...remoteWorkspaceRoot ? { remoteWorkspaceRoot } : {},
			codeModeOnly: config.codeModeOnly === true,
			loopDetectionPreToolUseRelay: config.loopDetectionPreToolUseRelay !== false,
			requestTimeoutMs: normalizePositiveNumber(config.requestTimeoutMs, 6e4),
			approvalPolicy: forcedPolicy?.approvalPolicy ?? approvalPolicy,
			approvalPolicySource,
			sandbox: resolvedSandbox,
			approvalsReviewer: forcedPolicy?.approvalsReviewer ?? explicitApprovalsReviewer ?? defaultPolicy?.approvalsReviewer ?? (policyMode === "guardian" ? "auto_review" : "user"),
			...serviceTier ? { serviceTier } : {},
			...resolveCodexAppServerNetworkProxy(config.networkProxy, resolvedSandbox)
		};
	}
	/** Resolves the passive supervision control connection without changing harness defaults. */
	function resolveCodexSupervisionAppServerRuntimeOptions(params = {}) {
		const pluginConfig = readCodexPluginConfig(params.pluginConfig);
		const appServer = pluginConfig.appServer ?? {};
		const homeScope = resolveCodexAppServerHomeScope({
			appServer,
			connectionScope: "supervision"
		});
		return resolveCodexAppServerRuntimeOptions({
			...params,
			pluginConfig: {
				...pluginConfig,
				appServer: {
					...appServer,
					homeScope
				}
			}
		});
	}
	return {
		resolveCodexAppServerRuntimeOptions,
		resolveCodexSupervisionAppServerRuntimeOptions
	};
}
/**
* Rechecks Codex-owned plugin state at the final spawn boundary, where the
* effective agent home is known, so Computer Use keeps the desktop app's TCC ownership.
*/
function resolveCodexAppServerStartOptionsForAgent(params) {
	const startOptions = params.startOptions;
	if (startOptions.transport !== "stdio" || startOptions.commandSource !== "managed" || startOptions.managedCommandOrder !== void 0) return startOptions;
	if (startOptions.homeScope === "user") return {
		...startOptions,
		managedCommandOrder: "desktop-first"
	};
	return codexConfigEnablesNativeComputerUse({
		agentDir: params.agentDir,
		codexConfigToml: params.codexConfigToml,
		env: params.env,
		homeScope: "agent",
		pluginNames: startOptions.managedComputerUsePluginNames ?? ["computer-use"]
	}) ? {
		...startOptions,
		managedCommandOrder: "desktop-first"
	} : startOptions;
}
function resolveCodexComputerUseConfig(params = {}) {
	const env = params.env ?? process.env;
	const config = readCodexPluginConfig(params.pluginConfig).computerUse ?? {};
	const marketplaceSource = readNonEmptyString(params.overrides?.marketplaceSource) ?? readNonEmptyString(config.marketplaceSource) ?? readNonEmptyString(env.OPENCLAW_CODEX_COMPUTER_USE_MARKETPLACE_SOURCE);
	const marketplacePath = readNonEmptyString(params.overrides?.marketplacePath) ?? readNonEmptyString(config.marketplacePath) ?? readNonEmptyString(env.OPENCLAW_CODEX_COMPUTER_USE_MARKETPLACE_PATH);
	const marketplaceName = readNonEmptyString(params.overrides?.marketplaceName) ?? readNonEmptyString(config.marketplaceName) ?? readNonEmptyString(env.OPENCLAW_CODEX_COMPUTER_USE_MARKETPLACE_NAME);
	const configuredPluginName = readNonEmptyString(params.overrides?.pluginName) ?? readNonEmptyString(config.pluginName) ?? readNonEmptyString(env.OPENCLAW_CODEX_COMPUTER_USE_PLUGIN_NAME);
	const configuredMcpServerName = readNonEmptyString(params.overrides?.mcpServerName) ?? readNonEmptyString(config.mcpServerName) ?? readNonEmptyString(env.OPENCLAW_CODEX_COMPUTER_USE_MCP_SERVER_NAME);
	const autoInstall = params.overrides?.autoInstall ?? config.autoInstall ?? readBooleanEnv(env.OPENCLAW_CODEX_COMPUTER_USE_AUTO_INSTALL) ?? false;
	const marketplaceDiscoveryTimeoutMs = normalizePositiveNumber(params.overrides?.marketplaceDiscoveryTimeoutMs ?? config.marketplaceDiscoveryTimeoutMs ?? readNumberEnv(env.OPENCLAW_CODEX_COMPUTER_USE_MARKETPLACE_DISCOVERY_TIMEOUT_MS), DEFAULT_CODEX_COMPUTER_USE_MARKETPLACE_DISCOVERY_TIMEOUT_MS);
	const liveTestTimeoutMs = normalizePositiveNumber(params.overrides?.liveTestTimeoutMs ?? config.liveTestTimeoutMs ?? readNumberEnv(env.OPENCLAW_CODEX_COMPUTER_USE_LIVE_TEST_TIMEOUT_MS), DEFAULT_CODEX_COMPUTER_USE_LIVE_TEST_TIMEOUT_MS);
	const toolCallTimeoutMs = normalizePositiveNumber(params.overrides?.toolCallTimeoutMs ?? config.toolCallTimeoutMs ?? readNumberEnv(env.OPENCLAW_CODEX_COMPUTER_USE_TOOL_CALL_TIMEOUT_MS), DEFAULT_CODEX_COMPUTER_USE_TOOL_CALL_TIMEOUT_MS);
	const healthCheckIntervalMinutes = normalizeComputerUseHealthCheckIntervalMinutes(params.overrides?.healthCheckIntervalMinutes ?? config.healthCheckIntervalMinutes ?? readNumberEnv(env.OPENCLAW_CODEX_COMPUTER_USE_HEALTH_CHECK_INTERVAL_MINUTES));
	const healthCheckEnabled = params.overrides?.healthCheckEnabled ?? config.healthCheckEnabled ?? readBooleanEnv(env.OPENCLAW_CODEX_COMPUTER_USE_HEALTH_CHECK_ENABLED) ?? false;
	const pluginCacheMode = normalizeComputerUsePluginCacheMode(params.overrides?.pluginCacheMode) ?? normalizeComputerUsePluginCacheMode(config.pluginCacheMode) ?? normalizeComputerUsePluginCacheMode(env.OPENCLAW_CODEX_COMPUTER_USE_PLUGIN_CACHE_MODE) ?? "independent";
	const strictReadiness = params.overrides?.strictReadiness ?? config.strictReadiness ?? readBooleanEnv(env.OPENCLAW_CODEX_COMPUTER_USE_STRICT_READINESS) ?? false;
	const autoRepair = params.overrides?.autoRepair ?? config.autoRepair ?? readBooleanEnv(env.OPENCLAW_CODEX_COMPUTER_USE_AUTO_REPAIR) ?? false;
	return {
		enabled: params.overrides?.enabled ?? config.enabled ?? readBooleanEnv(env.OPENCLAW_CODEX_COMPUTER_USE) ?? Boolean(autoInstall || marketplaceSource || marketplacePath || marketplaceName || configuredPluginName || configuredMcpServerName),
		autoInstall,
		marketplaceDiscoveryTimeoutMs,
		liveTestTimeoutMs,
		toolCallTimeoutMs,
		healthCheckEnabled,
		healthCheckIntervalMinutes,
		pluginCacheMode,
		strictReadiness,
		autoRepair,
		pluginName: configuredPluginName ?? "computer-use",
		mcpServerName: configuredMcpServerName ?? "computer-use",
		...marketplaceSource ? { marketplaceSource } : {},
		...marketplacePath ? { marketplacePath } : {},
		...marketplaceName ? { marketplaceName } : {}
	};
}
function normalizeComputerUseHealthCheckIntervalMinutes(value) {
	return value === 30 || value === 60 || value === 120 || value === 240 ? value : 60;
}
function normalizeComputerUsePluginCacheMode(value) {
	return value === "shared" || value === "independent" ? value : null;
}
function codexAppServerStartOptionsKey(options, params = {}) {
	return JSON.stringify({
		transport: options.transport,
		command: options.command,
		commandSource: options.commandSource ?? null,
		managedCommandOrder: options.managedCommandOrder ?? "package-first",
		managedComputerUsePluginNames: [...options.managedComputerUsePluginNames ?? []].toSorted(),
		managedFallbackCommandPaths: [...options.managedFallbackCommandPaths ?? []],
		args: options.args,
		cwd: options.cwd ?? null,
		url: options.url ?? null,
		authToken: hashSecretForKey(options.authToken, "authToken"),
		headers: Object.entries(options.headers).toSorted(([left], [right]) => left.localeCompare(right)).map(([key, value]) => [key, hashSecretForKey(value, `header:${key}`)]),
		env: Object.entries(options.env ?? {}).toSorted(([left], [right]) => left.localeCompare(right)).map(([key, value]) => [key, hashSecretForKey(value, `env:${key}`)]),
		clearEnv: [...options.clearEnv ?? []].toSorted(),
		authProfileId: params.authProfileId ?? null,
		authBindingFingerprint: params.authBindingFingerprint ?? null,
		agentDir: params.agentDir ?? null,
		fallbackApiKeyCacheKey: params.fallbackApiKeyCacheKey ?? null
	});
}
function codexSandboxPolicyForTurn(mode, cwd, nativeArgs = []) {
	if (mode === "danger-full-access") return { type: "dangerFullAccess" };
	if (mode === "read-only") return {
		type: "readOnly",
		networkAccess: false
	};
	let excludeTmpdirEnvVar = false;
	let excludeSlashTmp = false;
	for (const { name, value: override } of readCodexAppServerConfigOptions(nativeArgs)) {
		if (name !== "-c" && name !== "--config" || !override) continue;
		const separator = override.indexOf("=");
		if (separator < 0) continue;
		const key = override.slice(0, separator).trim();
		const isTmpdirExclusion = key === "sandbox_workspace_write.exclude_tmpdir_env_var";
		if (!isTmpdirExclusion && key !== "sandbox_workspace_write.exclude_slash_tmp") continue;
		let value;
		try {
			value = parse(`_x_ = ${override.slice(separator + 1).trim()}`)["_x_"];
		} catch {
			continue;
		}
		if (typeof value !== "boolean") continue;
		if (isTmpdirExclusion) excludeTmpdirEnvVar = value;
		else excludeSlashTmp = value;
	}
	return {
		type: "workspaceWrite",
		writableRoots: [cwd],
		networkAccess: false,
		excludeTmpdirEnvVar,
		excludeSlashTmp
	};
}
//#endregion
export { selectUserApprovalsReviewer as C, selectGuardianApprovalsReviewer as S, parseAllowedApprovalPoliciesFromCodexRequirements as _, resolveCodexAppServerStartOptionsForAgent as a, readCodexRequirementsToml as b, hasCodexMcpToolApprovalOverrides as c, withMcpElicitationsApprovalPolicy as d, assertCodexModelBackedReviewerEffectiveConfig as f, readCodexEffectiveConfig as g, CODEX_SESSION_OVERRIDABLE_LAYER_TYPES as h, resolveCodexAppServerHomeScope as i, resolveCodexAppServerNetworkProxy as l, resolveCodexModelBackedReviewerPolicyContext as m, codexSandboxPolicyForTurn as n, resolveCodexComputerUseConfig as o, canUseCodexModelBackedApprovalsReviewerForModel as p, createCodexAppServerConfig as r, assertCodexAppServerConnectionSecurity as s, codexAppServerStartOptionsKey as t, shouldAutoApproveCodexAppServerApprovals as u, parseAllowedApprovalsReviewersFromCodexRequirements as v, selectGuardianSandbox as w, selectGuardianApprovalPolicy as x, parseAllowedSandboxModesFromCodexRequirements as y };
