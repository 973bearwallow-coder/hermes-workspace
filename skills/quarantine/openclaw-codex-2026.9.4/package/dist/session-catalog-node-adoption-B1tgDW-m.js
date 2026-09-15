import { c as CatalogParamsError } from "./thread-history-page-D0JIp48V.js";
import { isRecord } from "openclaw/plugin-sdk/string-coerce-runtime";
import { parseAgentSessionKey } from "openclaw/plugin-sdk/routing";
import { resolveStorePath } from "openclaw/plugin-sdk/session-store-paths";
import { listSessionCatalogEntries, sessionCatalogAdoptedSessionKey, sessionCatalogAdoptedSourceKey } from "openclaw/plugin-sdk/session-catalog";
//#region extensions/codex/src/session-catalog-node-adoption.ts
const CODEX_NODE_SESSION_KEY_PREFIX = "harness:codex:node-session:";
const continueOperations = /* @__PURE__ */ new Map();
const sessionActionTails = /* @__PURE__ */ new Map();
async function runSessionActionExclusive(threadId, run) {
	const operation = (sessionActionTails.get(threadId) ?? Promise.resolve()).then(run);
	const tail = operation.then(() => void 0, () => void 0);
	sessionActionTails.set(threadId, tail);
	try {
		return await operation;
	} finally {
		if (sessionActionTails.get(threadId) === tail) sessionActionTails.delete(threadId);
	}
}
function adoptionSessionKeyRest(sessionKey) {
	const trimmed = sessionKey.trim();
	return parseAgentSessionKey(trimmed)?.rest ?? trimmed;
}
function nodeAdoptionSessionKey(hostId, threadId) {
	const source = JSON.stringify([hostId, threadId]);
	return sessionCatalogAdoptedSessionKey(CODEX_NODE_SESSION_KEY_PREFIX, source);
}
function readNodeSessionMarker(entry) {
	const codex = isRecord(entry.pluginExtensions?.codex) ? entry.pluginExtensions.codex : void 0;
	const marker = codex && isRecord(codex.sessionCatalog) ? codex.sessionCatalog : void 0;
	if (!marker || typeof marker.sourceHostId !== "string" || !marker.sourceHostId.startsWith("node:") || typeof marker.sourceThreadId !== "string" || !marker.sourceThreadId.trim() || typeof marker.nodeId !== "string" || !marker.nodeId.trim()) return;
	return {
		sourceHostId: marker.sourceHostId,
		sourceThreadId: marker.sourceThreadId,
		nodeId: marker.nodeId,
		...marker.initializing === true ? { initializing: true } : {}
	};
}
function listNodeAdoptedSessionEntries(params) {
	const adopted = /* @__PURE__ */ new Map();
	for (const { agentId, entry, sessionKey } of listSessionCatalogEntries({
		...params.agentId ? { agentId: params.agentId } : {},
		config: params.config ?? {},
		runtime: params.runtime,
		sessionEntries: params.sessionEntries
	})) {
		const marker = readNodeSessionMarker(entry);
		const sessionId = entry.sessionId?.trim();
		if (!marker || marker.initializing === true && params.includeInitializing !== true || entry.initializationPending === true || entry.agentHarnessId !== "codex" || entry.modelSelectionLocked !== true || !sessionId || adoptionSessionKeyRest(sessionKey) !== nodeAdoptionSessionKey(marker.sourceHostId, marker.sourceThreadId) || marker.sourceHostId !== `node:${marker.nodeId}`) continue;
		const sourceKey = sessionCatalogAdoptedSourceKey(marker.sourceHostId, marker.sourceThreadId);
		if (adopted.has(sourceKey)) throw new Error(`multiple OpenClaw sessions adopt Codex thread ${marker.sourceThreadId} on ${marker.sourceHostId}`);
		adopted.set(sourceKey, {
			key: sessionKey,
			sessionId,
			agentId,
			...marker.initializing === true ? { initializing: true } : {}
		});
	}
	return adopted;
}
function findNodeAdoptedSessionEntry(params) {
	return listNodeAdoptedSessionEntries(params).get(sessionCatalogAdoptedSourceKey(params.hostId, params.threadId));
}
function nodeSessionMarker(params) {
	return {
		sourceHostId: params.hostId,
		sourceThreadId: params.threadId,
		nodeId: params.nodeId,
		...params.initializing === true ? { initializing: true } : {}
	};
}
async function finalizeNodeAdoptedSession(params) {
	const changedError = () => new CatalogParamsError("Codex OpenClaw session changed before it could be bound. Retry.");
	let finalized;
	try {
		finalized = await params.api.runtime.agent.session.patchSessionEntry({
			sessionKey: params.adopted.key,
			readConsistency: "latest",
			preserveActivity: true,
			update: (entry) => {
				const current = readNodeSessionMarker(entry);
				if (entry.sessionId?.trim() !== params.adopted.sessionId || entry.initializationPending === true || entry.agentHarnessId !== "codex" || entry.modelSelectionLocked !== true || !current || current.sourceHostId !== params.marker.sourceHostId || current.sourceThreadId !== params.marker.sourceThreadId || current.nodeId !== params.marker.nodeId) throw changedError();
				if (current.initializing !== true) return {
					archivedAt: void 0,
					archivedBy: void 0,
					archiveReason: void 0
				};
				const codex = isRecord(entry.pluginExtensions?.codex) ? entry.pluginExtensions.codex : {};
				return {
					archivedAt: void 0,
					archivedBy: void 0,
					archiveReason: void 0,
					pluginExtensions: {
						...entry.pluginExtensions,
						codex: {
							...codex,
							sessionCatalog: params.marker
						}
					}
				};
			}
		});
	} catch (error) {
		const currentEntry = params.api.runtime.agent.session.getSessionEntry({
			sessionKey: params.adopted.key,
			readConsistency: "latest"
		});
		const current = currentEntry ? readNodeSessionMarker(currentEntry) : void 0;
		if (currentEntry?.sessionId?.trim() === params.adopted.sessionId && current?.initializing !== true && current?.sourceHostId === params.marker.sourceHostId && current.sourceThreadId === params.marker.sourceThreadId && current.nodeId === params.marker.nodeId) return;
		throw error;
	}
	if (!finalized) throw changedError();
}
async function createOrReuseNodeAdoptedSession(params) {
	const existing = findNodeAdoptedSessionEntry({
		agentId: params.agentId,
		config: params.config,
		runtime: params.api.runtime,
		hostId: params.hostId,
		threadId: params.record.threadId,
		includeInitializing: true
	});
	if (existing) return existing;
	const initializingMarker = {
		...nodeSessionMarker({
			hostId: params.hostId,
			threadId: params.record.threadId,
			nodeId: params.nodeId
		}),
		initializing: true
	};
	try {
		const created = await params.api.runtime.agent.session.createSessionEntry({
			cfg: params.config,
			key: nodeAdoptionSessionKey(params.hostId, params.record.threadId),
			agentId: params.agentId,
			recoverMatchingInitialEntry: true,
			displayName: params.record.name ?? void 0,
			...params.record.cwd?.trim() ? { spawnedCwd: params.record.cwd.trim() } : {},
			initialEntry: {
				agentHarnessId: "codex",
				modelSelectionLocked: true,
				pluginExtensions: { codex: { sessionCatalog: initializingMarker } }
			},
			afterCreate: async (entry) => {
				const storePath = resolveStorePath(params.config.session?.store, { agentId: entry.agentId });
				const { importCodexThreadHistoryToTranscript } = await import("./transcript-mirror-C5CKgNy6.js").then((n) => n.a);
				await importCodexThreadHistoryToTranscript({
					thread: params.history.thread,
					throughTurnId: params.history.throughTurnId,
					storePath,
					sessionId: entry.sessionId,
					sessionKey: entry.key,
					agentId: entry.agentId,
					...params.record.cwd?.trim() ? { cwd: params.record.cwd.trim() } : {},
					modelProvider: params.record.modelProvider,
					config: params.config
				});
				return { pluginExtensions: { codex: { sessionCatalog: initializingMarker } } };
			}
		});
		return {
			key: created.key,
			sessionId: created.sessionId,
			agentId: created.agentId,
			initializing: true
		};
	} catch (error) {
		const raced = findNodeAdoptedSessionEntry({
			agentId: params.agentId,
			config: params.config,
			runtime: params.api.runtime,
			hostId: params.hostId,
			threadId: params.record.threadId,
			includeInitializing: true
		});
		if (raced) return raced;
		throw error;
	}
}
//#endregion
export { adoptionSessionKeyRest, continueOperations, createOrReuseNodeAdoptedSession, finalizeNodeAdoptedSession, findNodeAdoptedSessionEntry, listNodeAdoptedSessionEntries, nodeSessionMarker, runSessionActionExclusive };
