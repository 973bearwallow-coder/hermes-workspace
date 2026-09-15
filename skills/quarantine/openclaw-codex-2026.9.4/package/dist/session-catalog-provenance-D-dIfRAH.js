import { o as isJsonObject } from "./protocol-5bh1G-H7.js";
import path from "node:path";
import { createZstdDecompress } from "node:zlib";
import { root } from "openclaw/plugin-sdk/file-access-runtime";
//#region extensions/codex/src/session-catalog-provenance.ts
const MAX_SESSION_META_BYTES = 1048576;
const SESSION_META_READ_CHUNK_BYTES = 65536;
const MAX_PROVENANCE_CACHE_ENTRIES = 2e4;
const provenanceByPath = /* @__PURE__ */ new Map();
function cacheProvenance(key, value) {
	provenanceByPath.delete(key);
	provenanceByPath.set(key, value);
	while (provenanceByPath.size > MAX_PROVENANCE_CACHE_ENTRIES) {
		const oldest = provenanceByPath.keys().next().value;
		if (oldest === void 0) break;
		provenanceByPath.delete(oldest);
	}
}
/** Undefined means the metadata line is not durable enough to cache yet. */
async function readCodexSessionMeta(sessionsRoot, rolloutPath, threadId) {
	let safeRoot;
	try {
		safeRoot = await root(sessionsRoot, {
			hardlinks: "reject",
			maxBytes: Number.MAX_SAFE_INTEGER,
			symlinks: "reject"
		});
	} catch {
		return;
	}
	const candidates = rolloutPath.endsWith(".zst") ? [rolloutPath, rolloutPath.slice(0, -4)] : [rolloutPath, `${rolloutPath}.zst`];
	for (const candidate of candidates) {
		let opened;
		try {
			opened = await safeRoot.open(path.relative(sessionsRoot, candidate));
		} catch {
			continue;
		}
		const input = opened.handle.createReadStream({
			autoClose: false,
			highWaterMark: SESSION_META_READ_CHUNK_BYTES
		});
		const reader = candidate.endsWith(".zst") ? input.pipe(createZstdDecompress()) : input;
		try {
			const chunks = [];
			let bytesReadTotal = 0;
			let line;
			for await (const value of reader) {
				const chunk = Buffer.isBuffer(value) ? value : Buffer.from(value);
				const remaining = MAX_SESSION_META_BYTES - bytesReadTotal;
				if (remaining <= 0) break;
				const bounded = chunk.subarray(0, remaining);
				bytesReadTotal += bounded.length;
				const newline = bounded.indexOf(10);
				chunks.push(newline >= 0 ? bounded.subarray(0, newline) : bounded);
				if (newline >= 0) {
					line = Buffer.concat(chunks).toString("utf8");
					break;
				}
			}
			if (!line) continue;
			let parsed;
			try {
				parsed = JSON.parse(line);
			} catch {
				continue;
			}
			if (!isJsonObject(parsed) || parsed.type !== "session_meta" || !isJsonObject(parsed.payload)) return null;
			const payload = parsed.payload;
			return payload.id === threadId ? payload : null;
		} catch {
			continue;
		} finally {
			reader.destroy();
			input.destroy();
			await opened.handle.close().catch(() => void 0);
		}
	}
}
/**
* Codex 0.147 reports OpenClaw app-server rollouts as `vscode`, so the rollout's
* immutable session metadata is the authoritative historical provenance.
*/
async function isOpenClawManagedCodexThread(thread, localSessionsRoot) {
	const rolloutPath = typeof thread.path === "string" ? thread.path.trim() : "";
	if (!localSessionsRoot || !rolloutPath) return false;
	const cacheKey = `${localSessionsRoot}\0${rolloutPath}`;
	const cached = provenanceByPath.get(cacheKey);
	if (cached !== void 0) return cached;
	const metadata = await readCodexSessionMeta(localSessionsRoot, rolloutPath, thread.id);
	const managed = metadata === void 0 ? void 0 : metadata?.originator === "openclaw";
	if (managed !== void 0) cacheProvenance(cacheKey, managed);
	return managed ?? false;
}
//#endregion
export { readCodexSessionMeta as n, isOpenClawManagedCodexThread as t };
