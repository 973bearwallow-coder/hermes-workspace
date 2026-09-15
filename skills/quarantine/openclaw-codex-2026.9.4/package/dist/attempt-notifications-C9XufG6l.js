import { o as isJsonObject } from "./protocol-5bh1G-H7.js";
import { readStringField } from "openclaw/plugin-sdk/string-coerce-runtime";
//#region extensions/codex/src/app-server/attempt-notifications.ts
const CODEX_TURN_ABORT_MARKER_START = "<turn_aborted>";
const CODEX_TURN_ABORT_MARKER_END = "</turn_aborted>";
/** Tracks actual native items for explicit terminal-tool batching. */
function updateActiveTurnItemIds(notification, activeItemIds) {
	if (notification.method !== "item/started" && notification.method !== "item/completed") return;
	const itemId = readNotificationItemId(notification);
	if (!itemId) return;
	if (notification.method === "item/started") {
		activeItemIds.add(itemId);
		return;
	}
	activeItemIds.delete(itemId);
}
/** Reads an item id from supported notification envelope shapes. */
function readNotificationItemId(notification) {
	if (!isJsonObject(notification.params)) return;
	const item = isJsonObject(notification.params.item) ? notification.params.item : void 0;
	return (item ? readStringField(item, "id") : void 0) ?? readStringField(notification.params, "itemId") ?? readStringField(notification.params, "id");
}
/** Detects completion for an OpenClaw dynamic tool result still awaited by Codex. */
function isPendingOpenClawDynamicToolCompletionNotification(notification, pendingOpenClawDynamicToolCompletionIds) {
	if (notification.method !== "item/completed" || !isJsonObject(notification.params)) return false;
	const itemId = readNotificationItemId(notification);
	if (!itemId || !pendingOpenClawDynamicToolCompletionIds.has(itemId)) return false;
	const item = isJsonObject(notification.params.item) ? notification.params.item : void 0;
	const itemType = item ? readStringField(item, "type") : void 0;
	return itemType === void 0 || itemType === "dynamicToolCall";
}
function isRawFunctionToolOutputCompletionNotification(notification) {
	if (notification.method !== "rawResponseItem/completed" || !isJsonObject(notification.params)) return false;
	const item = isJsonObject(notification.params.item) ? notification.params.item : void 0;
	return item ? readStringField(item, "type") === "function_call_output" : false;
}
/** Distinguishes progress-only assistant items from conversation answers. */
function isAssistantCommentaryCompletionNotification(notification) {
	if (!isJsonObject(notification.params) || notification.method !== "item/completed") return false;
	const item = isJsonObject(notification.params.item) ? notification.params.item : void 0;
	return Boolean(item && readStringField(item, "type") === "agentMessage" && (readStringField(item, "phase") === "commentary" || readStringField(item, "delivery") === "async"));
}
/** Returns true for terminal app-server thread status strings. */
function isTerminalTurnStatus(status) {
	return status === "completed" || status === "interrupted" || status === "failed";
}
/** Detects Codex's interrupted-turn marker, not user-authored copies of it. */
function isCodexTurnAbortMarkerNotification(notification, options = {}) {
	if (notification.method !== "rawResponseItem/completed" || !isJsonObject(notification.params)) return false;
	const item = notification.params.item;
	const role = isJsonObject(item) ? readStringField(item, "role") : void 0;
	if (!isJsonObject(item) || readStringField(item, "type") !== "message" || role !== "user" && role !== "developer") return false;
	const text = extractRawResponseItemText(item).trim();
	const currentPromptTexts = [options.currentPromptText, ...options.currentPromptTexts ?? []].filter(isNonEmptyString).map((prompt) => prompt.trim());
	if (role === "user" && currentPromptTexts.includes(text)) return false;
	return readCodexTurnAbortMarkerBody(text) !== void 0;
}
function readCodexTurnAbortMarkerBody(text) {
	if (!text.startsWith(CODEX_TURN_ABORT_MARKER_START) || !text.endsWith(CODEX_TURN_ABORT_MARKER_END)) return;
	return text.slice(14, -15).trim();
}
function extractRawResponseItemText(item) {
	const content = item.content;
	if (!Array.isArray(content)) return "";
	return content.flatMap((entry) => {
		if (!isJsonObject(entry)) return [];
		const type = readStringField(entry, "type");
		if (type !== "input_text" && type !== "text") return [];
		const text = readStringField(entry, "text");
		return text ? [text] : [];
	}).join("");
}
/** Reads a typed Codex item from notification params when id/type are present. */
function readCodexNotificationItem(params) {
	if (!isJsonObject(params) || !isJsonObject(params.item)) return;
	const item = params.item;
	return typeof item.id === "string" && typeof item.type === "string" ? item : void 0;
}
/** Reads the stable call id from a model-emitted raw tool item. */
function readRawResponseToolCallId(notification) {
	if (notification.method !== "rawResponseItem/completed" || !isJsonObject(notification.params)) return;
	const item = isJsonObject(notification.params.item) ? notification.params.item : void 0;
	if (!item) return;
	switch (readStringField(item, "type")) {
		case "custom_tool_call":
		case "function_call":
		case "local_shell_call":
		case "tool_search_call": return readStringField(item, "call_id");
		case "image_generation_call":
		case "web_search_call": return readStringField(item, "id");
		default: return;
	}
}
/** Maps Codex item types to the tool name shown in execution progress. */
function codexExecutionToolName(item) {
	if (item.type === "dynamicToolCall" && typeof item.tool === "string") return item.tool;
	if (item.type === "mcpToolCall" && typeof item.tool === "string") {
		const server = typeof item.server === "string" && item.server ? item.server : void 0;
		return server ? `${server}.${item.tool}` : item.tool;
	}
	if (item.type === "commandExecution") return "bash";
	if (item.type === "fileChange") return "apply_patch";
	if (item.type === "webSearch") return "web_search";
}
function isNonEmptyString(value) {
	return typeof value === "string" && value.length > 0;
}
//#endregion
export { isRawFunctionToolOutputCompletionNotification as a, readNotificationItemId as c, isPendingOpenClawDynamicToolCompletionNotification as i, readRawResponseToolCallId as l, isAssistantCommentaryCompletionNotification as n, isTerminalTurnStatus as o, isCodexTurnAbortMarkerNotification as r, readCodexNotificationItem as s, codexExecutionToolName as t, updateActiveTurnItemIds as u };
