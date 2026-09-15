import { o as isJsonObject } from "./protocol-5bh1G-H7.js";
import { asSafeIntegerInRange, readStringField } from "openclaw/plugin-sdk/string-coerce-runtime";
import { normalizeUsage } from "openclaw/plugin-sdk/agent-harness-runtime";
//#region extensions/codex/src/app-server/event-projector-usage.ts
function readTokenCount(record, key) {
	return asSafeIntegerInRange(record[key], { min: 0 });
}
function readCodexThreadTokenUsage(params) {
	const tokenUsage = isJsonObject(params.tokenUsage) ? params.tokenUsage : void 0;
	const last = tokenUsage && isJsonObject(tokenUsage.last) ? tokenUsage.last : void 0;
	return last ? normalizeCodexResponseTokenUsage(last) : void 0;
}
function readCodexThreadContextSnapshot(params) {
	const tokenUsage = isJsonObject(params.tokenUsage) ? params.tokenUsage : void 0;
	const last = tokenUsage && isJsonObject(tokenUsage.last) ? tokenUsage.last : void 0;
	const modelContextWindow = tokenUsage ? readTokenCount(tokenUsage, "modelContextWindow") : void 0;
	const activeContextTokens = last ? readTokenCount(last, "totalTokens") : void 0;
	const inputTokens = last ? readTokenCount(last, "inputTokens") : void 0;
	const cachedInputTokens = last ? readTokenCount(last, "cachedInputTokens") : void 0;
	const cacheWriteInputTokens = last ? readTokenCount(last, "cacheWriteInputTokens") : void 0;
	const reasoningOutputTokens = last ? readTokenCount(last, "reasoningOutputTokens") : void 0;
	return {
		...activeContextTokens !== void 0 ? { activeContextTokens } : {},
		...cachedInputTokens !== void 0 ? { cachedInputTokens } : {},
		...cacheWriteInputTokens !== void 0 ? { cacheWriteInputTokens } : {},
		...inputTokens !== void 0 ? { inputTokens } : {},
		...modelContextWindow && modelContextWindow > 0 ? { modelContextWindow } : {},
		...inputTokens !== void 0 ? { promptTokens: inputTokens } : {},
		...reasoningOutputTokens !== void 0 ? { reasoningOutputTokens } : {}
	};
}
function normalizeCodexResponseTokenUsage(record) {
	const totalTokens = readTokenCount(record, "totalTokens");
	const inputTokens = readTokenCount(record, "inputTokens");
	const cacheRead = readTokenCount(record, "cachedInputTokens");
	const output = readTokenCount(record, "outputTokens");
	const reasoningTokens = readTokenCount(record, "reasoningOutputTokens");
	const cacheWrite = record.cacheWriteInputTokens === void 0 ? 0 : readTokenCount(record, "cacheWriteInputTokens");
	const hasCoherentInput = inputTokens !== void 0 && cacheRead !== void 0 && cacheWrite !== void 0 && cacheRead + cacheWrite <= inputTokens;
	const hasCoherentContext = hasCoherentInput && totalTokens !== void 0 && output !== void 0 && totalTokens === inputTokens + output;
	const usage = normalizeUsage({
		input: hasCoherentInput ? inputTokens - cacheRead - cacheWrite : void 0,
		output,
		cacheRead,
		cacheWrite,
		reasoningTokens,
		total: totalTokens
	});
	if (!usage) return;
	return {
		...usage,
		contextUsage: hasCoherentContext ? {
			state: "available",
			promptTokens: inputTokens,
			totalTokens
		} : { state: "unavailable" }
	};
}
var CodexUsageProjection = class {
	constructor() {
		this.responseIds = /* @__PURE__ */ new Set();
	}
	get usage() {
		const usage = this.responseUsage ?? this.threadUsage;
		return usage ? {
			...usage,
			contextUsage: this.contextUsage
		} : void 0;
	}
	get modelIterations() {
		return this.responseIds.size;
	}
	invalidateContext() {
		this.contextUsage = { state: "unavailable" };
	}
	recordThread(params) {
		const usage = readCodexThreadTokenUsage(params);
		this.threadUsage = usage ?? this.threadUsage;
		if (!this.responseUsage && usage) this.contextUsage = usage.contextUsage;
		return readCodexThreadContextSnapshot(params);
	}
	record(params, reportOutputTokens) {
		const responseId = readStringField(params, "responseId");
		if (!responseId || this.responseIds.has(responseId)) return;
		this.responseIds.add(responseId);
		const usage = isJsonObject(params.usage) ? normalizeCodexResponseTokenUsage(params.usage) : void 0;
		this.contextUsage = usage?.contextUsage ?? { state: "unavailable" };
		this.responseUsage ??= {};
		for (const field of [
			"input",
			"output",
			"cacheRead",
			"cacheWrite",
			"reasoningTokens",
			"total"
		]) if (usage?.[field] !== void 0) this.responseUsage[field] = (this.responseUsage[field] ?? 0) + usage[field];
		const outputTokens = usage?.output;
		if (outputTokens !== void 0) reportOutputTokens?.(outputTokens);
	}
};
//#endregion
export { readCodexThreadContextSnapshot as n, CodexUsageProjection as t };
