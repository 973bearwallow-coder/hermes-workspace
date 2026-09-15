import { createHash } from "node:crypto";
import { embeddedAgentLog } from "openclaw/plugin-sdk/agent-harness-registration";
import { z } from "zod";
//#region extensions/codex/src/app-server/managed-thread-store.ts
const CODEX_MANAGED_THREAD_NAMESPACE = "app-server-managed-threads";
const CODEX_MANAGED_THREAD_MAX_ENTRIES = 2e4;
const managedThreadSchema = z.object({
	version: z.literal(1),
	kind: z.literal("managed-thread"),
	sourceHomeId: z.string().min(1),
	threadId: z.string().min(1),
	rolloutPath: z.string().min(1).optional()
});
async function markStartedCodexManagedThread(store, params) {
	if (!store) return;
	try {
		await store.mark({
			sourceHomeId: params.sourceHomeId,
			threadId: params.threadId,
			...params.rolloutPath ? { rolloutPath: params.rolloutPath } : {}
		});
	} catch (error) {
		embeddedAgentLog.warn("failed to record Codex managed thread ownership", { error });
	}
}
function managedThreadStoreKey(sourceHomeId, threadId) {
	return `sha256:${createHash("sha256").update("openclaw:codex-managed-thread:v1\0").update(sourceHomeId).update("\0").update(threadId).digest("hex")}`;
}
/** Durable ownership index for Codex threads created by OpenClaw. */
function createCodexManagedThreadStore(state) {
	return {
		async has(sourceHomeId, threadId) {
			const parsed = managedThreadSchema.safeParse(state.lookup(managedThreadStoreKey(sourceHomeId, threadId)));
			return parsed.success && parsed.data.sourceHomeId === sourceHomeId && parsed.data.threadId === threadId;
		},
		async mark(params) {
			try {
				const value = managedThreadSchema.parse({
					version: 1,
					kind: "managed-thread",
					sourceHomeId: params.sourceHomeId.trim(),
					threadId: params.threadId.trim(),
					...params.rolloutPath?.trim() ? { rolloutPath: params.rolloutPath.trim() } : {}
				});
				state.registerIfAbsent(managedThreadStoreKey(value.sourceHomeId, value.threadId), value);
				return true;
			} catch (error) {
				embeddedAgentLog.warn("failed to record Codex managed thread ownership", { error });
				return false;
			}
		},
		async snapshot() {
			const byHome = /* @__PURE__ */ new Map();
			for (const entry of state.entries()) {
				const parsed = managedThreadSchema.safeParse(entry.value);
				if (!parsed.success) continue;
				const ids = byHome.get(parsed.data.sourceHomeId) ?? /* @__PURE__ */ new Set();
				ids.add(parsed.data.threadId);
				byHome.set(parsed.data.sourceHomeId, ids);
			}
			return byHome;
		}
	};
}
//#endregion
export { markStartedCodexManagedThread as i, CODEX_MANAGED_THREAD_NAMESPACE as n, createCodexManagedThreadStore as r, CODEX_MANAGED_THREAD_MAX_ENTRIES as t };
