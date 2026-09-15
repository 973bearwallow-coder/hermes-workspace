import { o as isJsonObject } from "./protocol-5bh1G-H7.js";
//#region extensions/codex/src/app-server/rpc-error.ts
/** RPC error wrapper that preserves app-server error code and data. */
var CodexAppServerRpcError = class extends Error {
	constructor(error, method) {
		super(formatCodexAppServerRpcErrorMessage(error, method));
		this.name = "CodexAppServerRpcError";
		this.code = error.code;
		this.data = error.data;
		this.method = method;
	}
};
function isCodexThreadReadMissingError(error, threadId) {
	return error instanceof CodexAppServerRpcError && error.method === "thread/read" && error.code === -32600 && error.message === `thread not loaded: ${threadId}`;
}
function formatCodexAppServerRpcErrorMessage(error, method) {
	const message = error.message || `${method} failed`;
	const detail = readCodexAppServerRpcReloginDetail(error.data);
	return detail && !message.includes(detail) ? `${message}: ${detail}` : message;
}
function readCodexAppServerRpcReloginDetail(data) {
	const record = isJsonObject(data) ? data : void 0;
	const nested = isJsonObject(record?.error) ? record.error : record;
	if (!nested) return;
	const isRelogin = nested.action === "relogin" || nested.reason === "cloudRequirements" && nested.errorCode === "Auth";
	const detail = typeof nested.detail === "string" ? nested.detail.trim() : "";
	return isRelogin && detail ? detail : void 0;
}
//#endregion
export { isCodexThreadReadMissingError as n, CodexAppServerRpcError as t };
