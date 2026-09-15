import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
//#region extensions/codex/src/session-catalog-home-id.ts
function canonicalCodexCatalogHome(value) {
	const resolved = path.resolve(value);
	try {
		return fs.realpathSync.native(resolved);
	} catch {
		return resolved;
	}
}
/** One canonical identity for catalog discovery and durable ownership rows. */
function codexCatalogHomeId(codexHome) {
	return createHash("sha256").update("openclaw:codex-session-catalog-home:v1\0").update(canonicalCodexCatalogHome(codexHome)).digest("hex");
}
//#endregion
export { codexCatalogHomeId as n, canonicalCodexCatalogHome as t };
