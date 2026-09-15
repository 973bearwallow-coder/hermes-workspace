import { l as sessionBindingIdentity } from "./session-binding-record-Bcvslnhf.js";
import { c as resolveCodexAppServerLocalHomeDir, i as assertCodexThreadForkParams, l as resolveCodexAppServerUserHomeDir, s as resolveCodexAppServerHomeDir, x as readCodexPluginConfig } from "./protocol-5bh1G-H7.js";
import { n as isCodexThreadReadMissingError } from "./rpc-error-ttN_QjEm.js";
import { t as CODEX_CONTROL_METHODS } from "./capabilities-8vx68WLH.js";
import { C as readPageParams, D as unwrapNodeInvokePayload, E as toCatalogSession, S as readGatewayParams, T as requireOnlyKeys, _ as parseCatalogPage, a as CODEX_APP_SERVER_THREAD_TURNS_LIST_COMMAND, b as readBoundedOptionalString, c as CatalogParamsError, d as NODE_INVOKE_TIMEOUT_MS, g as normalizeLimit, h as isInteractiveThreadSource, i as CODEX_APP_SERVER_THREADS_LIST_COMMAND, l as MAX_CURSOR_LENGTH, m as filterCatalogPageByTitle, n as readLegacyCodexHistoryPage, o as CODEX_CATALOG_TRANSCRIPT_READ_COMMAND, p as catalogError, r as CODEX_APP_SERVER_THREADS_CAPABILITY, s as CODEX_LOCAL_SESSION_HOST_ID, t as readCodexThreadHistoryPage, u as MAX_TRANSCRIPT_PAGE_BYTES, v as parseJsonParams, x as readControlCursor, y as parseTranscriptPage } from "./thread-history-page-D0JIp48V.js";
import { i as projectCodexUserItemText } from "./transcript-history-projection-v17wXgdK.js";
import { r as codexUpstreamContinueResult } from "./session-upstream-marker-D15C9NHp.js";
import { i as replaceCodexCatalogConnectionHomes, t as buildCodexAppServerConnectionFingerprint } from "./plugin-app-cache-key-d0eKxy7b.js";
import { n as withTimeout } from "./timeout-BVw8aaM1.js";
import { n as codexCatalogHomeId, t as canonicalCodexCatalogHome } from "./session-catalog-home-id-CwhLdC03.js";
import { n as readCodexSessionMeta, t as isOpenClawManagedCodexThread } from "./session-catalog-provenance-D-dIfRAH.js";
import { isRecord } from "openclaw/plugin-sdk/string-coerce-runtime";
import { resolveDefaultAgentDir } from "openclaw/plugin-sdk/agent-harness-registration";
import { listAgentIds, resolveAgentDir, resolveDefaultAgentId, resolveSessionAgentIdsStrict } from "openclaw/plugin-sdk/agent-scope-runtime";
import { z } from "zod";
import fs from "node:fs";
import path from "node:path";
import { publishSessionCatalogHost, sessionCatalogPaging } from "openclaw/plugin-sdk/session-catalog-paging";
import { decodeNodePtyResumeParams, decodeNodePtyStartParams, resolveNodeHostExecutable, runNodePtyCommand } from "openclaw/plugin-sdk/node-host";
import { pruneMapToMaxSize } from "openclaw/plugin-sdk/collection-runtime";
//#region extensions/codex/src/session-catalog-create.ts
const CODEX_AGENT_RUNTIME_ID = "codex";
const CODEX_CATALOG_DEFAULT_MODEL_REF = "openai/gpt-5.6-sol";
function resolveCodexCatalogCreateSession(modelConfig, config, requestedAgentId) {
	if (!config) return;
	const agentId = requestedAgentId ?? resolveDefaultAgentId(config);
	const defaultModel = modelConfig.resolveDefaultModelForAgent({
		cfg: config,
		agentId
	});
	return "error" in modelConfig.resolveAllowedModelRef({
		cfg: config,
		catalog: [],
		raw: CODEX_CATALOG_DEFAULT_MODEL_REF,
		defaultProvider: defaultModel.provider,
		defaultModel: defaultModel.model,
		agentId
	}) ? void 0 : {
		model: CODEX_CATALOG_DEFAULT_MODEL_REF,
		agentRuntime: CODEX_AGENT_RUNTIME_ID
	};
}
//#endregion
//#region extensions/codex/src/session-catalog-node-lookup.ts
async function lookupNodeCodexCatalogRecord(params) {
	let cursor;
	const seenCursors = /* @__PURE__ */ new Set();
	for (let pageIndex = 0; pageIndex < 100; pageIndex += 1) {
		const raw = await params.runtime.nodes.invoke({
			nodeId: params.nodeId,
			command: CODEX_APP_SERVER_THREADS_LIST_COMMAND,
			params: {
				agentId: params.agentId,
				limit: 100,
				...cursor ? { cursor } : {}
			},
			timeoutMs: NODE_INVOKE_TIMEOUT_MS,
			scopes: ["operator.write"]
		});
		const page = parseCatalogPage(unwrapNodeInvokePayload(raw));
		const record = page.sessions.find((candidate) => candidate.threadId === params.threadId);
		if (record) return {
			kind: "found",
			record
		};
		const nextCursor = page.nextCursor?.trim();
		if (!nextCursor) break;
		if (seenCursors.has(nextCursor)) return { kind: "cursor-cycle" };
		seenCursors.add(nextCursor);
		cursor = nextCursor;
	}
	return { kind: "missing" };
}
//#endregion
//#region extensions/codex/src/session-catalog-terminal.ts
const CODEX_TERMINAL_RESUME_COMMAND = "codex.terminal.resume.v1";
const CODEX_TERMINAL_START_COMMAND = "codex.terminal.start.v1";
function createCodexTerminalStartNodeHostCommand() {
	return {
		command: CODEX_TERMINAL_START_COMMAND,
		cap: CODEX_APP_SERVER_THREADS_CAPABILITY,
		dangerous: false,
		duplex: true,
		isAvailable: ({ env }) => Boolean(resolveNodeHostExecutable("codex", {
			env,
			strategy: "direct"
		})),
		handle: async (paramsJSON, io) => {
			if (!io) throw new Error("Codex terminal command requires duplex transport");
			const params = decodeNodePtyStartParams(paramsJSON);
			const resolution = resolveNodeHostExecutable("codex", { strategy: "direct" });
			if (!resolution) throw new Error("Codex CLI is unavailable; install codex on this node and reconnect");
			return JSON.stringify(await runNodePtyCommand({
				file: resolution.executable,
				args: params.initialMessage !== void 0 ? ["--", params.initialMessage] : [],
				cwd: params.cwd,
				requiredCwd: true,
				cols: params.cols,
				rows: params.rows
			}, io));
		}
	};
}
function resolveCodexCatalogTerminalHome(sources) {
	const runtimeConfig = sources.getRuntimeConfig();
	if (!runtimeConfig) throw new Error("OpenClaw runtime config is unavailable");
	const agentDir = sources.source?.agentDir ?? (sources.agentId ? resolveAgentDir(runtimeConfig, sources.agentId) : resolveDefaultAgentDir(runtimeConfig));
	const startOptions = sources.source?.appServer.start ?? sources.resolveRuntimeOptions({ pluginConfig: sources.getPluginConfig() }).start;
	return resolveCodexAppServerLocalHomeDir(startOptions, agentDir);
}
function resolveLocalCodexTerminalExecutable(env = process.env) {
	return resolveLocalCodexTerminalResolution(env)?.executable;
}
function resolveLocalCodexTerminalResolution(env = process.env) {
	return resolveNodeHostExecutable("codex", {
		env,
		pathEnv: env.PATH ?? env.Path ?? "",
		strategy: "fallback"
	});
}
function codexNodeTerminalCapability(node) {
	const commands = node.invocableCommands ?? node.commands;
	return {
		canOpenTerminalCodex: node.connected === true && commands?.includes("codex.terminal.resume.v1") === true,
		canStartTerminal: node.connected === true && node.invocableCommands?.includes("codex.terminal.start.v1") === true
	};
}
function createCodexTerminalNodeHostCommand(bindRequest, configSources) {
	return {
		command: CODEX_TERMINAL_RESUME_COMMAND,
		cap: CODEX_APP_SERVER_THREADS_CAPABILITY,
		dangerous: false,
		duplex: true,
		isAvailable: ({ env }) => Boolean(resolveNodeHostExecutable("codex", {
			env,
			pathEnv: env.PATH ?? env.Path ?? "",
			strategy: "direct"
		})),
		handle: async (paramsJSON, io) => {
			if (!io) throw new Error("Codex terminal command requires duplex transport");
			const request = bindRequest(paramsJSON);
			const resume = decodeNodePtyResumeParams(request.paramsJSON, (value) => {
				if (typeof value !== "string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/iu.test(value)) throw new CatalogParamsError("threadId must be a UUID");
				return value;
			});
			const record = await request.control.requireEligibleThread(resume.threadId);
			const resolution = resolveNodeHostExecutable("codex", {
				env: process.env,
				pathEnv: process.env.PATH ?? process.env.Path ?? "",
				strategy: "direct"
			});
			if (!resolution) throw new Error("Codex CLI is unavailable");
			return JSON.stringify(await runNodePtyCommand({
				file: resolution.executable,
				args: ["resume", resume.threadId],
				...record.cwd ? { cwd: record.cwd } : {},
				env: { CODEX_HOME: resolveCodexCatalogTerminalHome({
					...configSources,
					agentId: request.agentId
				}) },
				cols: resume.cols,
				rows: resume.rows
			}, io));
		}
	};
}
async function openCodexCatalogTerminal(params) {
	const title = `codex resume ${params.threadId.slice(0, 8)}…`;
	if (params.hostId === "gateway:local" || params.hostId.startsWith(`gateway:local:`)) {
		const record = await params.control.requireEligibleThread(params.threadId);
		const resolution = resolveLocalCodexTerminalResolution();
		if (!resolution) throw new CatalogParamsError("Codex CLI is unavailable");
		return {
			kind: "local",
			argv: [
				resolution.executable,
				"resume",
				params.threadId
			],
			...record.cwd ? { cwd: record.cwd } : {},
			env: { CODEX_HOME: resolveCodexCatalogTerminalHome(params) },
			...resolution.pathEnv ? { pathEnv: resolution.pathEnv } : {},
			title
		};
	}
	if (!params.hostId.startsWith("node:")) throw new CatalogParamsError("hostId is invalid");
	const nodeId = params.hostId.slice(5);
	if (!(await params.api.runtime.nodes.list()).nodes.find((candidate) => {
		const commands = candidate.invocableCommands ?? candidate.commands;
		return candidate.nodeId === nodeId && candidate.connected === true && commands?.includes("codex.appServer.threads.list.v1") === true && commands.includes("codex.terminal.resume.v1");
	})) throw new CatalogParamsError("paired-node Codex terminal is unavailable");
	const lookup = await lookupNodeCodexCatalogRecord({
		agentId: params.agentId,
		runtime: params.api.runtime,
		nodeId,
		threadId: params.threadId
	});
	if (lookup.kind !== "found" || !isInteractiveThreadSource(lookup.record.source)) throw new CatalogParamsError("Codex session is not a non-archived interactive Codex session");
	const record = lookup.record;
	return {
		kind: "node",
		nodeId,
		command: CODEX_TERMINAL_RESUME_COMMAND,
		uploadPathStyle: "native",
		paramsJSON: JSON.stringify({
			agentId: params.agentId,
			threadId: params.threadId
		}),
		...record.cwd ? { cwd: record.cwd } : {},
		title
	};
}
async function startCodexCatalogTerminal(params) {
	if (params.nodeId) return {
		kind: "node",
		nodeId: params.nodeId,
		command: CODEX_TERMINAL_START_COMMAND,
		uploadPathStyle: "native",
		paramsJSON: JSON.stringify({
			cwd: params.cwd,
			initialMessage: params.initialMessage
		}),
		cwd: params.cwd,
		title: "codex"
	};
	const resolution = resolveLocalCodexTerminalResolution();
	if (!resolution) throw new CatalogParamsError("Codex CLI is unavailable; install Codex or add codex to PATH, then try again");
	return {
		kind: "local",
		argv: [resolution.executable, ...params.initialMessage !== void 0 ? ["--", params.initialMessage] : []],
		cwd: params.cwd,
		env: { CODEX_HOME: resolveCodexCatalogTerminalHome(params) },
		...resolution.pathEnv ? { pathEnv: resolution.pathEnv } : {},
		title: "codex"
	};
}
//#endregion
//#region extensions/codex/src/session-catalog-transcript-item.ts
const CODEX_MESSAGE_TYPES = /* @__PURE__ */ new Map([
	["userMessage", "userMessage"],
	["agentMessage", "agentMessage"],
	["reasoning", "reasoning"]
]);
const CODEX_TOOL_TYPES = /* @__PURE__ */ new Set([
	"commandExecution",
	"fileChange",
	"mcpToolCall",
	"dynamicToolCall",
	"collabAgentToolCall",
	"webSearch",
	"imageView",
	"imageGeneration"
]);
function toGenericTranscriptItem(item) {
	let type = CODEX_MESSAGE_TYPES.get(item.type);
	if (!type && CODEX_TOOL_TYPES.has(item.type)) type = item.result !== void 0 || Boolean(item.aggregatedOutput) ? "toolResult" : "toolCall";
	type ??= "other";
	const fallback = item.title ?? item.name ?? item.tool ?? item.command ?? item.query ?? void 0;
	const resultText = item.aggregatedOutput || (item.result === void 0 ? void 0 : JSON.stringify(item.result, null, 2));
	const changesText = Array.isArray(item.changes) ? item.changes.map((change) => `${change.kind}: ${change.path}`).join("\n") || void 0 : void 0;
	const text = item.type === "userMessage" ? projectCodexUserItemText(item) : item.text || resultText || changesText || fallback;
	return {
		id: item.id,
		type,
		...text ? { text } : {},
		raw: item
	};
}
//#endregion
//#region extensions/codex/src/session-catalog-transcript.ts
const transcriptPageSchema = z.strictObject({
	items: z.array(z.strictObject({
		id: z.string(),
		type: z.enum([
			"userMessage",
			"agentMessage",
			"reasoning",
			"toolCall",
			"toolResult",
			"other"
		]),
		text: z.string().optional(),
		raw: z.record(z.string(), z.json()).optional(),
		truncated: z.boolean().optional()
	})),
	nextCursor: z.string().optional()
});
function parseCodexCatalogTranscriptPage(value) {
	return transcriptPageSchema.parse(value);
}
function projectTranscriptPage(items, limit) {
	const projected = items.map(toGenericTranscriptItem);
	const page = sessionCatalogPaging.boundTranscriptPage(projected.toReversed(), limit, 0).items;
	for (const [index, item] of page.entries()) if (item.text !== projected[index]?.text && projected[index]?.text) item.truncated = true;
	return page;
}
function pageFitsNodeTransport(page) {
	return Buffer.byteLength(JSON.stringify({ payloadJSON: JSON.stringify(page) }), "utf8") <= MAX_TRANSCRIPT_PAGE_BYTES;
}
/** The legacy API can anchor a turn, but cannot continue within that turn. */
async function readLegacyCodexTranscriptPage(readTurns, request) {
	return readLegacyCodexHistoryPage(readTurns, request, {
		project: (entries, limit) => projectTranscriptPage(entries.map(({ item }) => item), limit),
		fits: pageFitsNodeTransport
	});
}
/** Uses the native store's item cursor whenever that store supports item history. */
async function readCodexCatalogTranscriptPage(control, request) {
	const thread = await control.requireEligibleThread(request.threadId);
	return readCodexThreadHistoryPage(control, thread, request, {
		project: (entries, limit) => projectTranscriptPage(entries.map(({ item }) => item), limit),
		fits: pageFitsNodeTransport
	});
}
//#endregion
//#region extensions/codex/src/session-catalog-listing.ts
async function listVisiblePage(params) {
	const excluded = params.excludedThreadIds;
	const sessions = [];
	let cursor = params.cursor;
	let nextCursor;
	let backwardsCursor;
	const seenCursors = /* @__PURE__ */ new Set();
	for (let pageIndex = 0; pageIndex < 20; pageIndex += 1) {
		params.signal?.throwIfAborted();
		let excludedFromPage = false;
		const rawPage = await params.control.listPage({
			limit: params.limit - sessions.length,
			...cursor ? { cursor } : {},
			...params.searchTerm ? { searchTerm: params.searchTerm } : {},
			...params.cwd ? { cwd: params.cwd } : {}
		});
		params.signal?.throwIfAborted();
		const page = filterCatalogPageByTitle(parseCatalogPage(rawPage), params.searchTerm);
		if (pageIndex === 0) backwardsCursor = page.backwardsCursor;
		for (const managed of rawPage.managedThreads ?? []) {
			excludedFromPage = true;
			params.signal?.throwIfAborted();
			await params.onExcludedThread?.(managed);
		}
		for (const session of page.sessions) {
			if (!excluded?.has(session.threadId)) {
				sessions.push(session);
				continue;
			}
			excludedFromPage = true;
			params.signal?.throwIfAborted();
			await params.onExcludedThread?.({ threadId: session.threadId });
		}
		nextCursor = page.nextCursor;
		if (!nextCursor || sessions.length >= params.limit || !excludedFromPage) break;
		if (seenCursors.has(nextCursor)) throw new Error("Codex session catalog returned a repeated exclusion cursor");
		seenCursors.add(nextCursor);
		cursor = nextCursor;
	}
	return {
		sessions: sessions.slice(0, params.limit),
		...nextCursor ? { nextCursor } : {},
		...backwardsCursor ? { backwardsCursor } : {}
	};
}
async function listGatewayHost(params) {
	const hostId = params.source?.hostId ?? "gateway:local";
	const label = params.source?.label ?? "Local Codex";
	const sourceHomeId = params.source?.sourceHomeId ?? "gateway:local";
	try {
		const page = await listVisiblePage({
			control: params.control,
			cursor: params.query.cursors?.[hostId],
			excludedThreadIds: params.excludedThreadIds,
			limit: params.query.limitPerHost,
			onExcludedThread: params.onExcludedThread,
			searchTerm: params.query.search,
			signal: params.signal
		});
		params.signal?.throwIfAborted();
		const { listAdoptedSessionEntries } = await import("./session-catalog-adoption-tcZi1IfX.js");
		const { sessionCatalogAdoptedSourceKey } = await import("openclaw/plugin-sdk/session-catalog");
		params.signal?.throwIfAborted();
		const adoptedSessions = await listAdoptedSessionEntries({
			agentId: params.agentId,
			bindingStore: params.bindingStore,
			config: params.config,
			runtime: params.runtime,
			sessionEntries: params.sessionEntries
		});
		return {
			hostId,
			label,
			kind: "gateway",
			connected: true,
			...page,
			sessions: page.sessions.map((session) => {
				const adopted = adoptedSessions.get(sessionCatalogAdoptedSourceKey(sourceHomeId, session.threadId)) ?? (hostId === "gateway:local" ? adoptedSessions.get(sessionCatalogAdoptedSourceKey("gateway:local", session.threadId)) : void 0);
				const sourced = params.source ? Object.assign({}, session, { sourceHomeId: params.source.sourceHomeId }) : session;
				return adopted ? Object.assign({}, sourced, { sessionKey: adopted.key }) : sourced;
			})
		};
	} catch (error) {
		return {
			hostId,
			label,
			kind: "gateway",
			connected: false,
			sessions: [],
			error: catalogError("APP_SERVER_UNAVAILABLE", error)
		};
	}
}
/** Lists Gateway-local and paired-node Codex sessions with per-host failures. */
async function listCodexSessionCatalog(params) {
	const agentId = resolveSessionAgentIdsStrict({
		config: params.config ?? {},
		agentId: params.agentId
	}).sessionAgentId;
	const query = readGatewayParams(params.query);
	const requestedHostIds = query.hostIds ? new Set(query.hostIds) : void 0;
	const localSources = params.localHomes?.filter((source) => !requestedHostIds || requestedHostIds.has(source.hostId)) ?? (params.includeLocal !== false && (!requestedHostIds || requestedHostIds.has("gateway:local")) ? [void 0] : []);
	const managedThreads = await params.bindingStore.managedThreads?.snapshot();
	params.signal?.throwIfAborted();
	const fallbackSource = params.control.homesForAgent(agentId)[0];
	const localHosts = localSources.map((source) => (() => {
		const ownershipSource = source ?? fallbackSource;
		const managedThreadIds = ownershipSource ? managedThreads?.get(ownershipSource.sourceHomeId) : void 0;
		return listGatewayHost({
			agentId,
			bindingStore: params.bindingStore,
			config: params.config,
			control: params.control.forRequest(agentId, ownershipSource),
			query,
			runtime: params.runtime,
			sessionEntries: params.sessionEntries,
			signal: params.signal,
			excludedThreadIds: managedThreadIds,
			...ownershipSource && params.bindingStore.managedThreads ? { onExcludedThread: async ({ threadId, rolloutPath }) => {
				if (!managedThreadIds?.has(threadId)) await params.bindingStore.managedThreads?.mark({
					sourceHomeId: ownershipSource.sourceHomeId,
					threadId,
					...rolloutPath ? { rolloutPath } : {}
				});
			} } : {},
			...source ? { source } : {}
		});
	})());
	for (const host of localHosts) publishSessionCatalogHost(params, host);
	if (!(!requestedHostIds || query.hostIds?.some((hostId) => hostId.startsWith("node:")))) return { hosts: await Promise.all(localHosts) };
	let nodes;
	try {
		nodes = (await (params.listNodes?.() ?? params.runtime.nodes.list())).nodes.filter((node) => node.gatewayLocal !== true && (node.commands?.includes("codex.appServer.threads.list.v1") || codexNodeTerminalCapability(node).canStartTerminal) && (!requestedHostIds || requestedHostIds.has(`node:${node.nodeId}`))).slice(0, 100 - localHosts.length);
	} catch (error) {
		const registryHost = {
			hostId: "node:registry",
			label: "Paired nodes",
			kind: "node",
			connected: false,
			canStartTerminal: false,
			sessions: [],
			error: catalogError("NODE_LIST_FAILED", error)
		};
		params.onHost?.(registryHost);
		return { hosts: [...await Promise.all(localHosts), registryHost] };
	}
	params.signal?.throwIfAborted();
	const { listNodeAdoptedSessionEntries } = await import("./session-catalog-node-adoption-B1tgDW-m.js");
	const { compareNodeLabels, listPairedNode } = await import("./session-catalog-node-continue-Ci-DXyJP.js");
	params.signal?.throwIfAborted();
	const adoptedNodeSessions = listNodeAdoptedSessionEntries({
		agentId,
		config: params.config,
		runtime: params.runtime,
		sessionEntries: params.sessionEntries
	});
	const nodeHosts = nodes.toSorted(compareNodeLabels).map((node) => listPairedNode({
		agentId,
		runtime: params.runtime,
		node,
		query,
		adoptedSessions: adoptedNodeSessions,
		terminalCapabilities: codexNodeTerminalCapability(node),
		waitUntil: params.waitUntil,
		signal: params.signal,
		...params.onHost ? { onHost: params.onHost } : {}
	}));
	return { hosts: await Promise.all([...localHosts, ...nodeHosts]) };
}
/** Builds the node-local read-only Codex app-server catalog command. */
function createCodexSessionCatalogNodeHostCommands(controlFactory, configSources, bindingStore) {
	const bindRequest = (paramsJSON) => {
		const parsed = parseJsonParams(paramsJSON);
		if (!isRecord(parsed)) throw new CatalogParamsError("Codex session catalog parameters must be an object");
		const requestedAgentId = readBoundedOptionalString(parsed, "agentId", 256);
		const config = configSources.getRuntimeConfig() ?? {};
		const agentId = resolveSessionAgentIdsStrict({
			config,
			agentId: requestedAgentId
		}).sessionAgentId;
		if (!listAgentIds(config).includes(agentId)) throw new CatalogParamsError(`unknown Codex session catalog agent: ${agentId}`);
		const request = { ...parsed };
		delete request.agentId;
		const source = controlFactory.homesForAgent(agentId)[0];
		return {
			agentId,
			control: controlFactory.forRequest(agentId, source),
			sourceHomeId: source?.sourceHomeId,
			params: request,
			paramsJSON: JSON.stringify(request)
		};
	};
	const commands = [
		{
			command: CODEX_APP_SERVER_THREADS_LIST_COMMAND,
			cap: CODEX_APP_SERVER_THREADS_CAPABILITY,
			dangerous: false,
			handle: async (paramsJSON) => {
				const request = bindRequest(paramsJSON);
				const pageParams = readPageParams(request.params);
				try {
					const managedThreads = await bindingStore?.managedThreads?.snapshot();
					const sourceHomeId = request.sourceHomeId;
					const managedThreadIds = sourceHomeId ? managedThreads?.get(sourceHomeId) : void 0;
					const page = await listVisiblePage({
						control: request.control,
						cursor: pageParams.cursor,
						cwd: pageParams.cwd,
						excludedThreadIds: managedThreadIds,
						limit: pageParams.limit,
						...sourceHomeId && bindingStore?.managedThreads ? { onExcludedThread: async ({ threadId, rolloutPath }) => {
							if (!managedThreadIds?.has(threadId)) await bindingStore.managedThreads?.mark({
								sourceHomeId,
								threadId,
								...rolloutPath ? { rolloutPath } : {}
							});
						} } : {},
						searchTerm: pageParams.searchTerm
					});
					return JSON.stringify(page);
				} catch {
					throw new Error("Codex app-server catalog is unavailable");
				}
			}
		},
		{
			command: CODEX_APP_SERVER_THREAD_TURNS_LIST_COMMAND,
			cap: CODEX_APP_SERVER_THREADS_CAPABILITY,
			dangerous: false,
			handle: async (paramsJSON) => {
				const request = bindRequest(paramsJSON);
				const action = readNodeTranscriptParams(request.params);
				try {
					await request.control.requireEligibleThread(action.threadId);
					const page = parseTranscriptPage(await request.control.listTurnPage({
						threadId: action.threadId,
						limit: action.limit,
						sortDirection: "desc",
						itemsView: "full",
						...action.cursor ? { cursor: action.cursor } : {}
					}));
					return JSON.stringify(page);
				} catch (error) {
					if (error instanceof CatalogParamsError) throw error;
					throw new Error("Codex app-server transcript is unavailable", { cause: error });
				}
			}
		},
		{
			command: CODEX_CATALOG_TRANSCRIPT_READ_COMMAND,
			cap: CODEX_APP_SERVER_THREADS_CAPABILITY,
			dangerous: false,
			handle: async (paramsJSON) => {
				const request = bindRequest(paramsJSON);
				const action = readNodeTranscriptParams(request.params);
				try {
					return JSON.stringify(await readCodexCatalogTranscriptPage(request.control, action));
				} catch (error) {
					if (error instanceof CatalogParamsError) throw error;
					throw new Error("Codex app-server transcript is unavailable", { cause: error });
				}
			}
		},
		createCodexTerminalNodeHostCommand(bindRequest, configSources),
		createCodexTerminalStartNodeHostCommand()
	];
	return process.env.OPENCLAW_NODE_EXEC_HOST?.trim().toLowerCase() === "app" ? commands.filter(({ command }) => command !== CODEX_CATALOG_TRANSCRIPT_READ_COMMAND) : commands;
}
function readNodeTranscriptParams(value) {
	if (!isRecord(value)) throw new CatalogParamsError("Codex session read parameters must be an object");
	requireOnlyKeys(value, /* @__PURE__ */ new Set([
		"threadId",
		"cursor",
		"limit"
	]));
	const threadId = readBoundedOptionalString(value, "threadId", 256);
	if (!threadId) throw new CatalogParamsError("threadId is required");
	const cursor = readBoundedOptionalString(value, "cursor", MAX_CURSOR_LENGTH);
	return {
		threadId,
		limit: readBoundedLimit(value.limit, "limit", 20, 50),
		...cursor ? { cursor } : {}
	};
}
function readBoundedLimit(value, key, fallback, max) {
	if (value === void 0) return fallback;
	if (!Number.isInteger(value) || value < 1 || value > max) throw new CatalogParamsError(`${key} must be an integer from 1 to ${max}`);
	return value;
}
/** Reads the persisted transcript for a Gateway-local or paired-node Codex session. */
async function readCodexSessionTranscript(params) {
	const cursor = readControlCursor(params.cursor, "transcript request");
	const limit = readBoundedLimit(params.limit, "limit", 20, 50);
	if (params.source || params.hostId === "gateway:local") {
		const page = await readCodexCatalogTranscriptPage(params.control, {
			threadId: params.threadId,
			limit,
			cursor
		});
		return {
			hostId: params.hostId,
			label: params.source?.label ?? "Local Codex",
			threadId: params.threadId,
			...page
		};
	}
	const nodeId = params.hostId.slice(5);
	const node = (await params.runtime.nodes.list()).nodes.find((candidate) => candidate.nodeId === nodeId && candidate.connected === true && candidate.commands?.includes("codex.appServer.thread.turns.list.v1"));
	if (!node) throw new CatalogParamsError("paired-node Codex session host is offline or unavailable");
	const invoke = async (command, request) => unwrapNodeInvokePayload(await params.runtime.nodes.invoke({
		nodeId,
		command,
		params: {
			agentId: params.agentId,
			threadId: params.threadId,
			...request
		},
		timeoutMs: NODE_INVOKE_TIMEOUT_MS,
		scopes: ["operator.write"]
	}));
	const page = node.commands?.includes("codex.sessionCatalog.transcript.read.v1") ? parseCodexCatalogTranscriptPage(await invoke(CODEX_CATALOG_TRANSCRIPT_READ_COMMAND, {
		cursor,
		limit
	})) : await readLegacyCodexTranscriptPage(async ({ cursor: turnCursor, limit: turnLimit }) => parseTranscriptPage(await invoke(CODEX_APP_SERVER_THREAD_TURNS_LIST_COMMAND, {
		cursor: turnCursor,
		limit: turnLimit
	})), {
		threadId: params.threadId,
		cursor,
		limit
	});
	const { nodeLabel } = await import("./session-catalog-node-continue-Ci-DXyJP.js");
	return {
		hostId: params.hostId,
		label: nodeLabel(node),
		threadId: params.threadId,
		...page
	};
}
//#endregion
//#region extensions/codex/src/session-upstream-activity.ts
const CODEX_UPSTREAM_TURN_LIMIT = 100;
function readMarker(probe) {
	if (!isRecord(probe.marker)) return;
	const turnId = probe.marker.turnId;
	if (turnId !== null && typeof turnId !== "string") return;
	const count = probe.marker.userMessageCount;
	if (count !== void 0 && (!Number.isSafeInteger(count) || count < 0)) return;
	return {
		turnId,
		...count === void 0 ? {} : { userMessageCount: count }
	};
}
function upstreamConnectionFingerprint(probe) {
	return isRecord(probe.upstreamRef) && typeof probe.upstreamRef.connectionFingerprint === "string" ? probe.upstreamRef.connectionFingerprint : void 0;
}
function classifyCodexUpstreamTurns(params) {
	const marker = readMarker(params.probe);
	if (!marker) return;
	const newest = params.turns[0];
	if (!newest?.id) return;
	const markerIndex = marker.turnId === null ? -1 : params.turns.findIndex((turn) => turn.id === marker.turnId);
	const candidateTurns = markerIndex < 0 ? params.turns : params.turns.slice(0, markerIndex + 1);
	const newestUserMessageCount = countUserMessages(newest);
	if (!(marker.turnId !== newest.id || marker.userMessageCount === void 0 || newestUserMessageCount > marker.userMessageCount)) return;
	const ownTexts = new Set(params.probe.ownRecentUserTexts);
	let humanTurns = 0;
	let occurredAt;
	for (const turn of candidateTurns) {
		const userMessages = turn.items.filter((item) => item.type === "userMessage");
		const alreadySeen = turn.id === marker.turnId ? marker.userMessageCount ?? userMessages.length : 0;
		for (const item of userMessages.slice(alreadySeen)) {
			const texts = normalizeUserMessageTexts(item);
			if (ownTexts.has(texts.join(" ")) || texts.length > 1 && texts.every((text) => ownTexts.has(text))) continue;
			humanTurns += 1;
			if (occurredAt === void 0) {
				const timestampSeconds = turn.completedAt ?? turn.startedAt;
				occurredAt = typeof timestampSeconds === "number" && Number.isFinite(timestampSeconds) ? timestampSeconds * 1e3 : params.now ?? Date.now();
			}
		}
	}
	const activityId = `${newest.id}:${newestUserMessageCount}`;
	return {
		kind: "activity",
		sessionKey: params.probe.sessionKey,
		humanTurns,
		nextMarker: {
			turnId: newest.id,
			userMessageCount: newestUserMessageCount
		},
		...humanTurns > 0 ? {
			occurredAt: occurredAt ?? params.now ?? Date.now(),
			dedupeId: activityId
		} : {}
	};
}
function countUserMessages(turn) {
	return turn.items.filter((item) => item.type === "userMessage").length;
}
function normalizeUserMessageTexts(item) {
	const typed = item;
	const contentTexts = typed.content?.filter((input) => input.type === "text").map((input) => input.text.trim().replace(/\s+/g, " ")).filter(Boolean);
	return contentTexts?.length ? contentTexts : [(typed.text ?? "").trim().replace(/\s+/g, " ")];
}
async function checkCodexUpstreamActivity(probes, control, resolveThreadId = (probe) => probe.threadId) {
	return await control.withPinnedConnection(async (pinned) => {
		const activities = [];
		for (const probe of probes) {
			const fingerprint = upstreamConnectionFingerprint(probe);
			if (probe.upstreamKind !== "codex-app-server" || !fingerprint || fingerprint !== pinned.connectionFingerprint) continue;
			try {
				const threadId = resolveThreadId(probe);
				const page = await pinned.listTurnPage({
					threadId,
					limit: CODEX_UPSTREAM_TURN_LIMIT,
					sortDirection: "desc",
					itemsView: "full"
				});
				const marker = readMarker(probe);
				if (page.data.length === 0 && marker) {
					try {
						await pinned.readThread(threadId, false);
					} catch (error) {
						if (isCodexThreadReadMissingError(error, threadId)) activities.push({
							kind: "missing",
							sessionKey: probe.sessionKey
						});
					}
					continue;
				}
				const activity = classifyCodexUpstreamTurns({
					probe,
					turns: page.data
				});
				if (activity) activities.push(activity);
			} catch {}
		}
		return activities;
	});
}
function createChecker(params) {
	const resolveThreadId = (probe) => {
		const config = params.getRuntimeConfig();
		const sessionId = params.api.runtime.agent.session.getSessionEntry({
			agentId: probe.agentId,
			sessionKey: probe.sessionKey,
			readConsistency: "latest"
		})?.sessionId?.trim();
		if (!sessionId) return probe.threadId;
		const binding = params.bindingStore.read(sessionBindingIdentity({
			sessionId,
			sessionKey: probe.sessionKey,
			config
		}));
		return binding?.connectionScope === "supervision" && binding.supervisionSourceThreadId === probe.threadId ? binding.threadId : probe.threadId;
	};
	return async (probes) => {
		const groups = /* @__PURE__ */ new Map();
		for (const probe of probes) {
			const fingerprint = upstreamConnectionFingerprint(probe);
			if (!fingerprint) continue;
			const control = params.control.forUpstream(probe.agentId, fingerprint);
			if (!control) continue;
			const key = `${probe.agentId}\0${fingerprint}`;
			const group = groups.get(key) ?? {
				control,
				probes: []
			};
			group.probes.push(probe);
			groups.set(key, group);
		}
		return (await Promise.all([...groups.values()].map((group) => checkCodexUpstreamActivity(group.probes, group.control, resolveThreadId)))).flat();
	};
}
//#endregion
//#region extensions/codex/src/session-catalog-homes.ts
function existingCatalogHomeCandidates(value, label) {
	const codexHome = canonicalCodexCatalogHome(value);
	try {
		if (!fs.statSync(codexHome).isDirectory()) return [];
	} catch {
		return [];
	}
	return [{
		codexHome,
		label: `Local Codex · ${label ?? path.basename(codexHome)}`
	}];
}
/** Resolves every local Codex store the operator already owns, without path disclosure. */
function resolveCodexCatalogHomes(params) {
	const { config, env, ownerAgentId, pluginConfig } = params;
	const ownerAgentDir = resolveAgentDir(config, ownerAgentId, env);
	const configuredHomes = readCodexPluginConfig(pluginConfig).sessionCatalog?.homes ?? [];
	const base = params.resolveRuntimeOptions({
		pluginConfig,
		env,
		agentDir: ownerAgentDir,
		config
	});
	const primaryCodexHome = canonicalCodexCatalogHome(resolveCodexAppServerLocalHomeDir(base.start, ownerAgentDir, env));
	const processUserHome = canonicalCodexCatalogHome(resolveCodexAppServerUserHomeDir(env));
	const processHomeConfigured = Boolean(env.CODEX_HOME?.trim());
	const candidates = [{
		codexHome: primaryCodexHome,
		label: "Local Codex",
		usesProcessHomeFallback: base.start.transport === "stdio" && base.start.homeScope === "user" && !processHomeConfigured
	}];
	if (base.start.transport === "stdio") {
		candidates.push({
			codexHome: processUserHome,
			label: "Local Codex · user",
			usesProcessHomeFallback: !processHomeConfigured
		});
		const agentIds = listAgentIds(config).toSorted((left, right) => left === ownerAgentId ? -1 : right === ownerAgentId ? 1 : left.localeCompare(right));
		candidates.push(...agentIds.flatMap((agentId) => existingCatalogHomeCandidates(resolveCodexAppServerHomeDir(resolveAgentDir(config, agentId, env)), agentId)), ...configuredHomes.flatMap((entry) => {
			const { path: home, label } = typeof entry === "string" ? { path: entry } : entry;
			return existingCatalogHomeCandidates(home, label);
		}));
	}
	const seen = /* @__PURE__ */ new Set();
	const homes = [];
	for (const candidate of candidates) {
		if (seen.has(candidate.codexHome)) continue;
		seen.add(candidate.codexHome);
		const sourceHomeId = codexCatalogHomeId(candidate.codexHome);
		const primary = homes.length === 0;
		homes.push({
			sourceHomeId,
			hostId: primary ? CODEX_LOCAL_SESSION_HOST_ID : `${CODEX_LOCAL_SESSION_HOST_ID}:${sourceHomeId}`,
			label: candidate.label,
			agentDir: ownerAgentDir,
			appServer: primary ? base : {
				...base,
				start: {
					...base.start,
					homeScope: "user",
					env: {
						...base.start.env,
						CODEX_HOME: candidate.codexHome
					}
				}
			},
			...base.connectionClass === "remote" ? {} : { localSessionsRoot: path.join(candidate.codexHome, "sessions") },
			usesProcessHomeFallback: candidate.usesProcessHomeFallback ?? false
		});
		if (homes.length >= 100) break;
	}
	return homes;
}
/** Discovers Codex homes once per immutable Gateway config generation. */
function createCodexCatalogHomeResolver(params) {
	const env = params.env ?? process.env;
	const homesByConfig = /* @__PURE__ */ new WeakMap();
	const buildSnapshot = (config) => {
		const pluginConfig = params.getPluginConfig();
		const homesByAgent = new Map(listAgentIds(config).map((agentId) => [agentId, resolveCodexCatalogHomes({
			config,
			pluginConfig,
			ownerAgentId: agentId,
			env,
			resolveRuntimeOptions: params.resolveRuntimeOptions
		})]));
		replaceCodexCatalogConnectionHomes([...homesByAgent.values()].flatMap((homes) => homes.filter((home) => home.appServer.start.transport === "stdio").map((home) => ({
			agentDir: home.agentDir,
			fingerprint: buildCodexAppServerConnectionFingerprint(home.appServer, home.agentDir),
			codexHome: resolveCodexAppServerLocalHomeDir(home.appServer.start, home.agentDir, env)
		}))));
		homesByConfig.set(config, homesByAgent);
		return homesByAgent;
	};
	let lastSnapshot = buildSnapshot(params.config);
	return { forAgent(agentId) {
		const config = params.getRuntimeConfig();
		if (!config) return lastSnapshot.get(agentId) ?? [];
		const cached = homesByConfig.get(config);
		if (cached) return cached.get(agentId) ?? [];
		lastSnapshot = buildSnapshot(config);
		return lastSnapshot.get(agentId) ?? [];
	} };
}
//#endregion
//#region extensions/codex/src/session-catalog-control.ts
const CODEX_SESSION_CATALOG_LIST_TTL_MS = 32e3;
const CODEX_SESSION_CATALOG_LIST_CACHE_MAX_ENTRIES = 32;
function codexCatalogPageCacheKey(params, agentId, source) {
	return JSON.stringify([
		agentId,
		source?.sourceHomeId ?? null,
		params.cursor ?? null,
		params.limit ?? null,
		params.searchTerm?.trim().toLocaleLowerCase() || null,
		params.cwd?.trim() || null
	]);
}
function createCodexCatalogRequestSnapshot(requestTimeoutMs, request) {
	return {
		requestTimeoutMs,
		listThreads: (params, timeoutMs) => request(CODEX_CONTROL_METHODS.listThreads, params, timeoutMs),
		listThreadTurns: (params) => request(CODEX_CONTROL_METHODS.listThreadTurns, params),
		listThreadItems: (params) => request(CODEX_CONTROL_METHODS.listThreadItems, params),
		forkThread: (params, assertCurrent) => request(CODEX_CONTROL_METHODS.forkThread, assertCodexThreadForkParams(params), void 0, assertCurrent),
		readThread: async (threadId, includeTurns, timeoutMs) => (await request(CODEX_CONTROL_METHODS.readThread, {
			threadId,
			includeTurns
		}, timeoutMs)).thread,
		archiveThread: async (threadId, assertCurrent) => {
			await request(CODEX_CONTROL_METHODS.archiveThread, { threadId }, void 0, assertCurrent);
		}
	};
}
function createCodexSessionCatalogControlFromRequests(params) {
	return {
		forkContext: params.forkContext,
		...params.clientId ? { clientId: params.clientId } : {},
		...params.connectionFingerprint ? { connectionFingerprint: params.connectionFingerprint } : {},
		withPinnedConnection: params.withPinnedConnection,
		async requireEligibleThread(threadId) {
			const requests = params.createRequestSnapshot();
			const deadline = params.now() + requests.requestTimeoutMs;
			const unverified = () => new CatalogParamsError("Codex session eligibility could not be verified. Refresh the catalog and verify the session in its native Codex home before retrying.");
			const remaining = () => {
				const timeoutMs = Math.ceil(deadline - params.now());
				if (timeoutMs <= 0) throw unverified();
				return timeoutMs;
			};
			const verify = async () => {
				if (params.sourceHomeId && await params.managedThreads?.has(params.sourceHomeId, threadId)) throw unverified();
				const root = params.localSessionsRoot;
				const thread = root ? await requests.readThread(threadId, false, remaining()) : void 0;
				if (root && (!thread || thread.id !== threadId || !isInteractiveThreadSource(thread.source))) throw unverified();
				let cursor;
				const seenCursors = /* @__PURE__ */ new Set();
				for (let pageIndex = 0; pageIndex < 100; pageIndex += 1) {
					const page = await requests.listThreads({
						archived: false,
						limit: 100,
						modelProviders: [],
						sortKey: root ? "recency_at" : "updated_at",
						sortDirection: "desc",
						...root ? {
							useStateDbOnly: true,
							...thread?.cwd ? { cwd: thread.cwd } : {}
						} : {},
						...cursor ? { cursor } : {}
					}, remaining());
					remaining();
					const candidate = page.data.find((value) => value.id === threadId);
					if (candidate) {
						if (!isInteractiveThreadSource(candidate.source)) throw unverified();
						if (root && thread) {
							const rolloutPath = thread.path;
							if (!rolloutPath || !candidate.path || rolloutPath.replace(/\.zst$/u, "") !== candidate.path.replace(/\.zst$/u, "")) throw unverified();
							const metadata = await readCodexSessionMeta(root, rolloutPath, threadId);
							remaining();
							if (!metadata || !isInteractiveThreadSource(metadata.source) || metadata.originator === "openclaw") throw unverified();
							return thread;
						}
						return candidate;
					}
					const nextCursor = readControlCursor(page.nextCursor, "next response");
					if (!nextCursor || seenCursors.has(nextCursor)) throw unverified();
					seenCursors.add(nextCursor);
					cursor = nextCursor;
				}
				throw unverified();
			};
			return await withTimeout(verify(), requests.requestTimeoutMs, "Codex session eligibility could not be verified", unverified);
		},
		retireConnection: params.retireConnection,
		async listPage(pageParams) {
			const limit = normalizeLimit(pageParams.limit, "limit");
			const search = pageParams.searchTerm?.trim().toLocaleLowerCase() || void 0;
			const cwd = pageParams.cwd?.trim() || void 0;
			const maxPages = search ? 20 : 1;
			const sessions = [];
			const managedThreads = [];
			let cursor = readControlCursor(pageParams.cursor, "request");
			let nextCursor;
			let backwardsCursor;
			const seenCursors = new Set(cursor ? [cursor] : []);
			const requests = params.createRequestSnapshot();
			const deadline = params.now() + requests.requestTimeoutMs;
			const { sanitizeTerminalText } = await import("openclaw/plugin-sdk/text-chunking");
			for (let pageIndex = 0; pageIndex < maxPages; pageIndex += 1) {
				const remainingTimeoutMs = Math.ceil(deadline - params.now());
				if (remainingTimeoutMs <= 0) throw new Error("Codex session catalog listing timed out");
				const response = await requests.listThreads({
					archived: false,
					limit: limit - sessions.length,
					modelProviders: [],
					sortKey: "updated_at",
					sortDirection: "desc",
					...cwd ? { cwd } : {},
					...cursor ? { cursor } : {}
				}, remainingTimeoutMs);
				if (pageIndex === 0) backwardsCursor = readControlCursor(response.backwardsCursor, "backwards response");
				for (const thread of response.data) {
					if (await isOpenClawManagedCodexThread(thread, params.localSessionsRoot)) {
						const rolloutPath = typeof thread.path === "string" ? thread.path.trim() : "";
						managedThreads.push({
							threadId: thread.id,
							...rolloutPath ? { rolloutPath } : {}
						});
						continue;
					}
					const session = toCatalogSession(thread, false, sanitizeTerminalText);
					if (session && (!search || (session.name ?? session.fallbackName)?.toLocaleLowerCase().includes(search))) sessions.push(session);
				}
				nextCursor = readControlCursor(response.nextCursor, "next response");
				if (!nextCursor || sessions.length >= limit) break;
				if (seenCursors.has(nextCursor)) throw new Error("Codex session catalog returned a repeated search cursor");
				seenCursors.add(nextCursor);
				cursor = nextCursor;
			}
			return {
				sessions,
				...managedThreads.length > 0 ? { managedThreads } : {},
				...nextCursor ? { nextCursor } : {},
				...backwardsCursor ? { backwardsCursor } : {}
			};
		},
		async listDescendantPage(listParams) {
			const requests = params.createRequestSnapshot();
			return await requests.listThreads(listParams, requests.requestTimeoutMs);
		},
		async readThread(threadId, includeTurns = false) {
			return await params.createRequestSnapshot().readThread(threadId, includeTurns);
		},
		async listTurnPage(listParams) {
			return await params.createRequestSnapshot().listThreadTurns(listParams);
		},
		listItemPage: (listParams) => params.createRequestSnapshot().listThreadItems(listParams),
		async forkThread(forkParams, assertCurrent) {
			return await params.createRequestSnapshot().forkThread(forkParams, assertCurrent);
		},
		async archiveThread(threadId, assertCurrent) {
			await params.createRequestSnapshot().archiveThread(threadId, assertCurrent);
		}
	};
}
/** Builds the passive catalog over the Codex plugin's canonical shared client. */
function createCodexSessionCatalogControl(params) {
	const now = params.now ?? Date.now;
	const getPluginConfig = () => params.getPluginConfig();
	const homeResolver = createCodexCatalogHomeResolver({
		config: params.getRuntimeConfig() ?? params.config ?? {},
		getRuntimeConfig: params.getRuntimeConfig,
		getPluginConfig: params.getPluginConfig,
		resolveRuntimeOptions: params.resolveRuntimeOptions,
		...params.env ? { env: params.env } : {}
	});
	const requestOptionsByConfig = /* @__PURE__ */ new WeakMap();
	const catalogPagesByConfig = /* @__PURE__ */ new WeakMap();
	const resolveRequestOptions = (startOptions, agentId, source) => {
		const runtimeConfig = params.getRuntimeConfig();
		const agentDir = source?.agentDir ?? resolveAgentDir(runtimeConfig ?? {}, agentId);
		const resolvedStartOptions = source?.appServer.start ?? startOptions;
		if (!runtimeConfig) return {
			agentDir,
			config: void 0,
			startOptions: structuredClone(resolvedStartOptions)
		};
		let byAgent = requestOptionsByConfig.get(runtimeConfig);
		const cacheKey = `${agentId ?? ""}\0${source?.sourceHomeId ?? ""}`;
		const cached = byAgent?.get(cacheKey);
		if (cached) return cached;
		const resolved = {
			agentDir,
			config: structuredClone(runtimeConfig),
			startOptions: structuredClone(resolvedStartOptions)
		};
		if (!byAgent) {
			byAgent = /* @__PURE__ */ new Map();
			requestOptionsByConfig.set(runtimeConfig, byAgent);
		}
		byAgent.set(cacheKey, resolved);
		return resolved;
	};
	const createRequestSnapshot = (agentId, source) => {
		const pluginConfig = getPluginConfig();
		const runtime = source?.appServer ?? params.resolveRuntimeOptions({ pluginConfig });
		const requestOptions = resolveRequestOptions(runtime.start, agentId, source);
		return createCodexCatalogRequestSnapshot(runtime.requestTimeoutMs, async (method, requestParams, timeoutMs, assertCurrent) => {
			const { codexControlRequest } = await import("./command-rpc-CR5EOEZX.js").then((n) => n.n);
			return await codexControlRequest(pluginConfig, method, requestParams, {
				...requestOptions,
				assertCurrent,
				...timeoutMs === void 0 ? {} : { timeoutMs }
			});
		});
	};
	const forRequest = (agentId, source) => {
		const withPinnedConnection = async (run) => {
			const pluginConfig = getPluginConfig();
			const runtime = source?.appServer ?? params.resolveRuntimeOptions({ pluginConfig });
			const { agentDir, config: runtimeConfig, startOptions } = resolveRequestOptions(runtime.start, agentId, source);
			const { getLeasedSharedCodexAppServerClient, releaseLeasedSharedCodexAppServerClient, retireSharedCodexAppServerClientIfCurrent } = await import("./shared-client-CscigXXL.js").then((n) => n.y);
			const { resolveCodexAppServerClientInstanceId } = await import("./client-B57KWPQx.js").then((n) => n.n);
			const { requestCodexAppServerClientJson } = await import("./request-B7hEkBGq.js").then((n) => n.a);
			const client = await getLeasedSharedCodexAppServerClient({
				agentDir,
				config: runtimeConfig,
				startOptions,
				timeoutMs: runtime.requestTimeoutMs
			});
			try {
				const requests = createCodexCatalogRequestSnapshot(runtime.requestTimeoutMs, async (method, requestParams, timeoutMs, assertCurrent) => await requestCodexAppServerClientJson({
					client,
					method,
					requestParams,
					config: runtimeConfig,
					timeoutMs: timeoutMs ?? runtime.requestTimeoutMs,
					assertCurrent
				}));
				const pinnedControl = createCodexSessionCatalogControlFromRequests({
					forkContext: {
						client,
						appServer: runtime,
						pluginConfig,
						agentDir,
						localSessionsRoot: source?.localSessionsRoot
					},
					clientId: resolveCodexAppServerClientInstanceId(client),
					retireConnection: () => {
						retireSharedCodexAppServerClientIfCurrent(client);
					},
					connectionFingerprint: buildCodexAppServerConnectionFingerprint(runtime, agentDir),
					createRequestSnapshot: () => requests,
					...source?.localSessionsRoot ? { localSessionsRoot: source.localSessionsRoot } : {},
					sourceHomeId: source?.sourceHomeId,
					managedThreads: params.managedThreads,
					now,
					withPinnedConnection: async (nestedRun) => await nestedRun(pinnedControl)
				});
				return await run(pinnedControl);
			} finally {
				releaseLeasedSharedCodexAppServerClient(client);
			}
		};
		const control = createCodexSessionCatalogControlFromRequests({
			createRequestSnapshot: () => createRequestSnapshot(agentId, source),
			...source?.localSessionsRoot ? { localSessionsRoot: source.localSessionsRoot } : {},
			now,
			withPinnedConnection
		});
		return {
			...control,
			requireEligibleThread: (threadId) => withPinnedConnection((pinned) => pinned.requireEligibleThread(threadId)),
			async listPage(pageParams) {
				const runtimeConfig = params.getRuntimeConfig();
				if (!runtimeConfig) return await control.listPage(pageParams);
				let cache = catalogPagesByConfig.get(runtimeConfig);
				if (!cache) {
					cache = /* @__PURE__ */ new Map();
					catalogPagesByConfig.set(runtimeConfig, cache);
				}
				const key = codexCatalogPageCacheKey(pageParams, agentId, source);
				const cached = cache.get(key);
				if (cached) {
					cache.delete(key);
					cache.set(key, cached);
					if (cached.expiresAt > now()) return cached.value ?? await cached.page;
				}
				if (cached) cache.delete(key);
				const page = control.listPage(pageParams);
				const staleValue = cached?.value;
				const entry = {
					expiresAt: Number.POSITIVE_INFINITY,
					page,
					...staleValue ? { value: staleValue } : {}
				};
				cache.set(key, entry);
				pruneMapToMaxSize(cache, CODEX_SESSION_CATALOG_LIST_CACHE_MAX_ENTRIES);
				const settle = (value) => {
					if (cache.get(key) === entry) {
						entry.value = value;
						entry.expiresAt = now() + CODEX_SESSION_CATALOG_LIST_TTL_MS;
					}
					return value;
				};
				const restore = () => {
					if (cache.get(key) !== entry) return;
					if (staleValue) cache.set(key, {
						expiresAt: now(),
						page: Promise.resolve(staleValue),
						value: staleValue
					});
					else cache.delete(key);
				};
				if (staleValue) {
					page.then(settle, restore);
					return staleValue;
				}
				try {
					return settle(await page);
				} catch (error) {
					restore();
					throw error;
				}
			}
		};
	};
	const homesForAgent = (agentId) => homeResolver.forAgent(agentId);
	const forUpstream = (agentId, connectionFingerprint) => {
		const source = homesForAgent(agentId).find((home) => buildCodexAppServerConnectionFingerprint(home.appServer, home.agentDir) === connectionFingerprint);
		return source ? forRequest(agentId, source) : void 0;
	};
	return {
		forRequest,
		forUpstream,
		homesForAgent
	};
}
//#endregion
//#region extensions/codex/src/session-catalog.ts
/** Allows read-only catalog and transcript commands on supported paired-node platforms. */
function createCodexSessionCatalogNodeInvokePolicies() {
	return [{
		commands: [
			CODEX_APP_SERVER_THREADS_LIST_COMMAND,
			CODEX_APP_SERVER_THREAD_TURNS_LIST_COMMAND,
			CODEX_CATALOG_TRANSCRIPT_READ_COMMAND,
			CODEX_TERMINAL_RESUME_COMMAND,
			CODEX_TERMINAL_START_COMMAND
		],
		defaultPlatforms: [
			"macos",
			"linux",
			"windows"
		],
		handle: (context) => {
			if (context.command === "codex.terminal.start.v1") return context.client?.scopes?.includes("operator.admin") && context.config.gateway?.cliAgents?.enabled === true && context.config.gateway?.terminal?.enabled !== false ? { ok: true } : {
				ok: false,
				message: "Native terminal start requires operator.admin and enabled CLI agents and terminals"
			};
			return context.command === "codex.terminal.resume.v1" ? { ok: true } : context.invokeNode();
		}
	}];
}
function toGenericCatalogHost(host, localTerminalAvailable) {
	const local = isLocalCodexCatalogHost(host.hostId);
	return {
		hostId: host.hostId,
		label: host.label,
		kind: host.kind,
		connected: host.connected,
		...host.nodeId ? { nodeId: host.nodeId } : {},
		sessions: host.sessions.map((session) => {
			const continuableStatus = !session.archived && (session.status === "idle" || session.status === "notLoaded");
			const canContinue = (local || host.canContinueCodex === true) && continuableStatus && isInteractiveThreadSource(session.source);
			const canArchive = local && continuableStatus && isInteractiveThreadSource(session.source);
			const canOpenTerminal = isInteractiveThreadSource(session.source) && (local ? localTerminalAvailable : host.canOpenTerminalCodex === true);
			const name = session.name ?? session.fallbackName;
			return {
				threadId: session.threadId,
				...session.sourceHomeId ? { sourceHomeId: session.sourceHomeId } : {},
				...name ? { name } : {},
				...session.cwd ? { cwd: session.cwd } : {},
				status: session.status,
				...session.createdAt != null ? { createdAt: session.createdAt } : {},
				...session.updatedAt != null ? { updatedAt: session.updatedAt } : {},
				...session.recencyAt != null ? { recencyAt: session.recencyAt } : {},
				...session.source ? { source: session.source } : {},
				...session.modelProvider ? { modelProvider: session.modelProvider } : {},
				...session.cliVersion ? { cliVersion: session.cliVersion } : {},
				...session.gitBranch ? { gitBranch: session.gitBranch } : {},
				archived: session.archived,
				...session.sessionKey ? { sessionKey: session.sessionKey } : {},
				canContinue,
				canArchive,
				canOpenTerminal
			};
		}),
		...host.nextCursor ? { nextCursor: host.nextCursor } : {},
		...host.error ? { error: host.error } : {}
	};
}
function isLocalCodexCatalogHost(hostId) {
	return hostId === "gateway:local" || hostId.startsWith(`gateway:local:`);
}
function resolveLocalCatalogHomeForThread(params) {
	if (params.homes.length === 0) throw new CatalogParamsError("local Codex sessions are unavailable in isolated state");
	const exact = params.sourceHomeId ? params.homes.filter((home) => home.sourceHomeId === params.sourceHomeId) : params.homes.filter((home) => home.hostId === params.hostId);
	if (exact.length === 0 || params.sourceHomeId && exact[0]?.hostId !== params.hostId) throw new CatalogParamsError("Codex session source home is unavailable");
	return exact[0];
}
function registerCodexSessionCatalog(params) {
	const catalogHomes = (agentId, allowProcessHomeFallback) => {
		const homes = params.control.homesForAgent(agentId);
		return allowProcessHomeFallback === false ? homes.filter((home) => !home.usesProcessHomeFallback) : homes;
	};
	const resolveRequestAgentId = (agentId) => resolveSessionAgentIdsStrict({
		config: params.getRuntimeConfig() ?? params.api.config,
		agentId
	}).sessionAgentId;
	const bindRequest = (request) => {
		const agentId = resolveRequestAgentId(request.agentId);
		const source = isLocalCodexCatalogHost(request.hostId) ? resolveLocalCatalogHomeForThread({
			homes: [...catalogHomes(agentId, request.allowProcessHomeFallback)],
			hostId: request.hostId,
			...request.sourceHomeId ? { sourceHomeId: request.sourceHomeId } : {}
		}) : void 0;
		return {
			agentId,
			source,
			control: params.control.forRequest(agentId, source)
		};
	};
	const bindLocalRequest = (request) => {
		const bound = bindRequest(request);
		if (!bound.source) throw new CatalogParamsError("Codex session catalog hostId is invalid");
		return {
			...bound,
			source: bound.source
		};
	};
	const checkUpstreamActivity = createChecker(params);
	params.api.registerSessionCatalog({
		id: "codex",
		label: "Codex",
		supportsProcessHomeIsolation: true,
		resolveCreateSession: ({ agentId }) => resolveCodexCatalogCreateSession(params.api.runtime.modelConfig, params.getRuntimeConfig() ?? params.api.config, agentId),
		list: async (query) => {
			const localTerminalAvailable = resolveLocalCodexTerminalExecutable() !== void 0;
			const { agentId: requestedAgentId, allowProcessHomeFallback, listNodes, onHost, waitUntil, signal, sessionEntries, ...gatewayQuery } = query;
			const agentId = resolveRequestAgentId(requestedAgentId);
			const localHomes = [...catalogHomes(agentId, allowProcessHomeFallback)];
			const mapHost = (host) => ({
				...toGenericCatalogHost(host, localTerminalAvailable),
				canStartTerminal: host.kind === "gateway" ? localTerminalAvailable && host.hostId === "gateway:local" && localHomes.some((home) => home.hostId === host.hostId && home.appServer.start.transport === "stdio") : host.canStartTerminal === true
			});
			return (await listCodexSessionCatalog({
				agentId,
				bindingStore: params.bindingStore,
				config: params.getRuntimeConfig(),
				runtime: params.api.runtime,
				control: params.control,
				query: gatewayQuery,
				listNodes,
				waitUntil,
				signal,
				sessionEntries,
				localHomes,
				...onHost ? { onHost: (host) => onHost(mapHost(host)) } : {}
			})).hosts.map(mapHost);
		},
		read: async (request) => {
			const { agentId, source, control } = bindRequest(request);
			return await readCodexSessionTranscript({
				agentId,
				runtime: params.api.runtime,
				control,
				hostId: request.hostId,
				threadId: request.threadId,
				cursor: request.cursor,
				limit: request.limit ?? 20,
				...source ? { source } : {}
			});
		},
		continueSession: async (request) => {
			const config = params.getRuntimeConfig();
			if (!config) throw new Error("OpenClaw runtime config is unavailable");
			if (request.hostId.startsWith("node:")) return await continueNodeCodexSession({
				agentId: resolveRequestAgentId(request.agentId),
				api: params.api,
				config,
				hostId: request.hostId,
				threadId: request.threadId,
				clientScopes: request.clientScopes
			});
			if (!isLocalCodexCatalogHost(request.hostId)) throw new CatalogParamsError("Codex session catalog hostId is invalid");
			const { agentId, source, control } = bindLocalRequest(request);
			let upstreamBaseline;
			const continued = await continueLocalCodexSession({
				agentId,
				api: params.api,
				bindingStore: params.bindingStore,
				config,
				control,
				threadId: request.threadId,
				hostId: source.hostId,
				sourceHomeId: source.sourceHomeId,
				...source.hostId === "gateway:local" ? { allowLegacy: true } : {},
				onContinued: (baseline) => {
					upstreamBaseline = baseline;
				}
			});
			return codexUpstreamContinueResult(continued.sessionKey, request.threadId, upstreamBaseline);
		},
		checkUpstreamActivity: (probes, policy) => checkUpstreamActivity(probes.filter((probe) => !isLocalCodexCatalogHost(probe.hostId) || policy?.allowProcessHomeFallback !== false || catalogHomes(probe.agentId, false).some((home) => home.hostId === probe.hostId))),
		archive: async (request) => {
			if (request.confirmNoOtherRunner !== true) throw new CatalogParamsError("archive requires confirmation that no other runner is active");
			if (!isLocalCodexCatalogHost(request.hostId)) throw new CatalogParamsError("paired-node Codex sessions are view-only");
			const config = params.getRuntimeConfig();
			if (!config) throw new Error("OpenClaw runtime config is unavailable");
			const { agentId, source, control } = bindLocalRequest(request);
			await archiveLocalCodexSession({
				agentId,
				bindingStore: params.bindingStore,
				config,
				control,
				runtime: params.api.runtime,
				threadId: request.threadId,
				hostId: source.hostId,
				sourceHomeId: source.sourceHomeId,
				...source.hostId === "gateway:local" ? { allowLegacy: true } : {}
			});
			return { ok: true };
		},
		openTerminal: async (request) => {
			const { agentId, source, control } = bindRequest(request);
			return await openCodexCatalogTerminal({
				api: params.api,
				control,
				getPluginConfig: params.getPluginConfig,
				getRuntimeConfig: params.getRuntimeConfig,
				resolveRuntimeOptions: params.resolveRuntimeOptions,
				...source ? { source } : {},
				...request,
				agentId
			});
		},
		startTerminalSession: async (request) => {
			if (!request.nodeId && request.hostId && request.hostId !== "gateway:local") throw new CatalogParamsError("Codex terminal host is unavailable; select the local machine or a connected node");
			const source = request.nodeId ? void 0 : resolveLocalCatalogHomeForThread({
				homes: [...catalogHomes(request.agentId, request.allowProcessHomeFallback)],
				hostId: request.hostId ?? "gateway:local"
			});
			if (source && source.appServer.start.transport !== "stdio") throw new CatalogParamsError("Native terminal start requires a local Codex source");
			return await startCodexCatalogTerminal({
				getPluginConfig: params.getPluginConfig,
				getRuntimeConfig: params.getRuntimeConfig,
				resolveRuntimeOptions: params.resolveRuntimeOptions,
				...request,
				source
			});
		}
	});
}
const codexSessionCatalogRuntime = {
	register: registerCodexSessionCatalog,
	list: listCodexSessionCatalog,
	readTranscript: readCodexSessionTranscript,
	continueLocal: continueLocalCodexSession,
	continueNode: continueNodeCodexSession,
	archiveLocal: archiveLocalCodexSession
};
async function continueLocalCodexSession(...args) {
	const { continueLocalCodexSession: run } = await import("./session-catalog-adoption-tcZi1IfX.js");
	return run(...args);
}
async function archiveLocalCodexSession(...args) {
	const { archiveLocalCodexSession: run } = await import("./session-catalog-archive-CwKg8Xz2.js");
	return run(...args);
}
async function continueNodeCodexSession(...args) {
	const { continueNodeCodexSession: run } = await import("./session-catalog-node-continue-Ci-DXyJP.js");
	return run(...args);
}
//#endregion
export { lookupNodeCodexCatalogRecord as a, createCodexSessionCatalogNodeHostCommands as i, createCodexSessionCatalogNodeInvokePolicies as n, createCodexSessionCatalogControl as r, codexSessionCatalogRuntime as t };
