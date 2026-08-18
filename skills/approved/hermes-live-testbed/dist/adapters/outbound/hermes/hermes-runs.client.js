import { DEFAULT_HERMES_STREAM_IDLE_TIMEOUT_MS } from "../../../config.js";
import { parseSseStream } from "./sse.js";
export const MAX_HERMES_JSON_RESPONSE_BYTES = 1_000_000;
export const MAX_HERMES_RUN_OUTPUT_CHARS = 200_000;
export const MAX_HERMES_RETRY_AFTER_CHARS = 128;
export const REQUIRED_HERMES_SESSION_FEATURES = [
    "session_resources",
    "session_chat",
    "session_chat_streaming",
    "model_options",
    "session_model_lock",
];
const MAX_TIMER_TIMEOUT_MS = 2_147_483_647;
const MAX_HERMES_RETRY_AFTER_SECONDS = 86_400;
const MAX_HERMES_RUN_METADATA_CHARS = 512;
const MAX_HERMES_SESSION_TITLE_CHARS = 100;
const MAX_HERMES_SESSION_TEXT_CHARS = 20_000;
const MAX_HERMES_SESSION_MESSAGES = 10_000;
const MAX_HERMES_PROVIDER_ID_CHARS = 80;
const HERMES_RUN_STATUSES = new Set([
    "queued",
    "running",
    "waiting_for_approval",
    "stopping",
    "completed",
    "failed",
    "cancelled",
]);
export class HermesRequestError extends Error {
    status;
    publicPath;
    name = "HermesRequestError";
    retryAfter;
    errorCode;
    constructor(status, publicPath, retryAfter, messagePrefix = "Hermes request failed", errorCode) {
        super(`${messagePrefix}: ${status} ${publicPath}`);
        this.status = status;
        this.publicPath = publicPath;
        this.retryAfter = boundedRetryAfterValue(retryAfter);
        this.errorCode = boundedHermesErrorCode(errorCode);
    }
}
export class HermesClient {
    baseUrl;
    apiKey;
    model;
    timeoutMs;
    streamIdleTimeoutMs;
    sessionModelsReady = new Set();
    constructor(config) {
        this.baseUrl = config.baseUrl;
        this.apiKey = config.apiKey;
        this.model = config.model;
        this.timeoutMs = config.timeoutMs;
        this.streamIdleTimeoutMs = validStreamIdleTimeout(config.streamIdleTimeoutMs ?? DEFAULT_HERMES_STREAM_IDLE_TIMEOUT_MS);
    }
    async health(signal) {
        return this.requestJson("/health", withSignal({ method: "GET" }, signal));
    }
    async capabilities(signal) {
        return this.requestJson("/v1/capabilities", withSignal({ method: "GET" }, signal));
    }
    async assertRunsSupported(signal) {
        const capabilities = await this.capabilities(signal);
        const features = capabilities.features ?? {};
        const required = ["run_submission", "run_status", "run_events_sse", "run_stop", "run_approval_response"];
        const missing = required.filter((name) => features[name] !== true);
        if (missing.length > 0) {
            throw new Error(`Hermes API Server is missing required features: ${missing.join(", ")}`);
        }
        return capabilities;
    }
    async assertSessionsSupported(signal) {
        const capabilities = await this.capabilities(signal);
        const features = capabilities.features ?? {};
        const missing = REQUIRED_HERMES_SESSION_FEATURES.filter((name) => features[name] !== true);
        if (missing.length > 0) {
            throw new Error(`Hermes API Server is missing required session features: ${missing.join(", ")}`);
        }
        return capabilities;
    }
    async listSessions(options = {}) {
        const limit = boundedInteger(options.limit ?? 50, 1, 200, "Hermes session list limit");
        const offset = boundedInteger(options.offset ?? 0, 0, 1_000_000, "Hermes session list offset");
        const query = new URLSearchParams({ limit: String(limit), offset: String(offset) });
        if (options.source !== undefined) {
            query.set("source", boundedSafeText(options.source, 64, "Hermes session source"));
        }
        const response = await this.requestJson(`/api/sessions?${query.toString()}`, {
            method: "GET",
            ...signalInit(options.signal),
        });
        if (!isRecord(response) || response.object !== "list" || !Array.isArray(response.data)) {
            throw new Error("Hermes returned an invalid session list.");
        }
        if (response.data.length > 200) {
            throw new Error("Hermes returned too many sessions.");
        }
        return response.data.map((value) => parseHermesSessionSummary(value));
    }
    async createSession(options = {}) {
        const body = {};
        const modelSelection = this.model
            ? { model: this.model }
            : await this.defaultModelSelection(options.signal);
        if (modelSelection) {
            body.model = modelSelection.model;
            if (modelSelection.provider)
                body.provider = modelSelection.provider;
        }
        if (options.title !== undefined) {
            body.title = boundedSafeText(options.title, MAX_HERMES_SESSION_TITLE_CHARS, "Hermes session title");
        }
        const response = await this.requestJson("/api/sessions", {
            method: "POST",
            body: JSON.stringify(body),
            ...signalInit(options.signal),
        });
        if (!isRecord(response) || response.object !== "hermes.session") {
            throw new Error("Hermes returned an invalid created session.");
        }
        const session = parseHermesSessionSummary(response.session);
        if (modelSelection && session.model === modelSelection.model) {
            this.sessionModelsReady.add(session.id);
        }
        return session;
    }
    async getSession(sessionId, signal) {
        requireHermesSessionId(sessionId);
        const response = await this.requestJson(`/api/sessions/${encodeURIComponent(sessionId)}`, {
            method: "GET",
            ...signalInit(signal),
        });
        if (!isRecord(response) || response.object !== "hermes.session") {
            throw new Error("Hermes returned an invalid session.");
        }
        return parseHermesSessionSummary(response.session, sessionId);
    }
    async getSessionHistory(sessionId, signal) {
        requireHermesSessionId(sessionId);
        const response = await this.requestJson(`/api/sessions/${encodeURIComponent(sessionId)}/messages`, {
            method: "GET",
            ...signalInit(signal),
        });
        if (!isRecord(response)
            || response.object !== "list"
            || !isBoundedHermesIdentifier(response.session_id)
            || !Array.isArray(response.data)) {
            throw new Error("Hermes returned an invalid session history.");
        }
        if (response.data.length > MAX_HERMES_SESSION_MESSAGES) {
            throw new Error(`Hermes session history exceeds ${MAX_HERMES_SESSION_MESSAGES} messages.`);
        }
        return {
            sessionId: response.session_id,
            messages: response.data.map((value) => parseHermesSessionMessage(value)),
        };
    }
    async chatSession(sessionId, message, options = {}) {
        requireHermesSessionId(sessionId);
        const input = boundedSafeText(message, 100_000, "Hermes session message", true);
        await this.ensureSessionModelReady(sessionId, options.signal);
        const body = { message: input };
        if (options.instructions !== undefined) {
            body.instructions = boundedSafeText(options.instructions, 100_000, "Hermes session instructions", true);
        }
        const response = await this.requestJson(`/api/sessions/${encodeURIComponent(sessionId)}/chat`, {
            method: "POST",
            body: JSON.stringify(body),
            headers: this.sessionHeaders(options.sessionKey),
            ...signalInit(options.signal),
        });
        if (!isRecord(response)
            || response.object !== "hermes.session.chat.completion"
            || !isBoundedHermesIdentifier(response.session_id)
            || !isRecord(response.message)
            || response.message.role !== "assistant"
            || typeof response.message.content !== "string") {
            throw new Error("Hermes returned an invalid session chat completion.");
        }
        const content = response.message.content.slice(0, MAX_HERMES_RUN_OUTPUT_CHARS);
        const usage = safeParseHermesRunUsage(response.usage);
        return {
            sessionId: response.session_id,
            content,
            ...(usage ? { usage } : {}),
        };
    }
    async defaultModelSelection(signal) {
        const response = await this.requestJson("/api/model/options", {
            method: "GET",
            ...signalInit(signal),
        });
        if (!isRecord(response)) {
            throw new Error("Hermes returned invalid model options.");
        }
        const model = optionalBoundedSafeText(response.model, MAX_HERMES_RUN_METADATA_CHARS, "Hermes selected model");
        if (!model) {
            throw new Error("Hermes did not report its selected model.");
        }
        const provider = optionalBoundedSafeText(response.provider, MAX_HERMES_PROVIDER_ID_CHARS, "Hermes selected provider");
        return { model, ...(provider ? { provider } : {}) };
    }
    async ensureSessionModelReady(sessionId, signal) {
        if (this.sessionModelsReady.has(sessionId))
            return;
        const [session, capabilities] = await Promise.all([
            this.getSession(sessionId, signal),
            this.assertSessionsSupported(signal),
        ]);
        const virtualModel = optionalBoundedSafeText(capabilities.model, MAX_HERMES_RUN_METADATA_CHARS, "Hermes virtual model");
        if (!session.model || !virtualModel || session.model !== virtualModel) {
            this.sessionModelsReady.add(sessionId);
            return;
        }
        const selection = this.model
            ? { model: this.model }
            : await this.defaultModelSelection(signal);
        if (!selection) {
            throw new Error("Hermes could not resolve a real model for this saved conversation.");
        }
        const response = await this.requestJson(`/api/sessions/${encodeURIComponent(sessionId)}/model`, {
            method: "POST",
            body: JSON.stringify(selection),
            ...signalInit(signal),
        });
        if (!isRecord(response)
            || response.object !== "hermes.session.model_lock"
            || response.session_id !== sessionId) {
            throw new Error("Hermes did not confirm the saved conversation model.");
        }
        this.sessionModelsReady.add(sessionId);
    }
    async startRun(params, signal) {
        const body = {
            input: params.input,
            session_id: params.sessionId,
        };
        if (this.model)
            body.model = this.model;
        if (params.instructions) {
            body.instructions = params.instructions;
        }
        if (params.conversationHistory?.length) {
            body.conversation_history = params.conversationHistory;
        }
        const response = await this.requestJson("/v1/runs", {
            method: "POST",
            body: JSON.stringify(body),
            headers: this.sessionHeaders(params.sessionKey),
            ...signalInit(signal),
        });
        if (response?.run_id !== undefined && !isBoundedHermesIdentifier(response.run_id)) {
            throw new Error("Hermes returned an invalid run_id.");
        }
        if (response?.runId !== undefined && !isBoundedHermesIdentifier(response.runId)) {
            throw new Error("Hermes returned an invalid runId alias.");
        }
        if (response?.run_id !== undefined && response.runId !== undefined && response.run_id !== response.runId) {
            throw new Error("Hermes returned conflicting run identifiers.");
        }
        const runId = response?.run_id ?? response?.runId;
        if (!isBoundedHermesIdentifier(runId)) {
            throw new Error("Hermes did not return a valid bounded run_id.");
        }
        return {
            runId,
            status: response.status === "started" || (typeof response.status === "string"
                && HERMES_RUN_STATUSES.has(response.status))
                ? response.status
                : "started",
        };
    }
    async getRun(runId, options) {
        requireHermesRunId(runId);
        const requestOptions = normalizeHermesRequestOptions(options);
        const response = await this.requestJson(`/v1/runs/${encodeURIComponent(runId)}`, {
            method: "GET",
            headers: this.sessionHeaders(requestOptions.sessionKey),
            ...signalInit(requestOptions.signal),
        });
        return parseHermesRunSnapshot(response, runId);
    }
    async stopRun(runId, options) {
        requireHermesRunId(runId);
        const requestOptions = normalizeHermesRequestOptions(options);
        const response = await this.requestJson(`/v1/runs/${encodeURIComponent(runId)}/stop`, {
            method: "POST",
            body: "{}",
            headers: this.sessionHeaders(requestOptions.sessionKey),
            ...signalInit(requestOptions.signal),
        });
        if (response.run_id !== runId ||
            response.status !== "stopping" ||
            (response.runId !== undefined && response.runId !== runId)) {
            throw new Error("Hermes returned an invalid stop confirmation.");
        }
        return { run_id: runId, status: "stopping" };
    }
    async submitApproval(runId, choice, options = {}) {
        requireHermesRunId(runId);
        return await this.requestJson(`/v1/runs/${encodeURIComponent(runId)}/approval`, {
            method: "POST",
            body: JSON.stringify({
                choice,
                resolve_all: options.resolveAll ?? false,
                ...(options.approvalId ? { approval_id: options.approvalId } : {}),
            }),
            headers: this.sessionHeaders(options.sessionKey),
            ...signalInit(options.signal),
        });
    }
    async *streamRunEvents(runId, options) {
        requireHermesRunId(runId);
        const requestOptions = normalizeHermesRequestOptions(options);
        const path = `/v1/runs/${encodeURIComponent(runId)}/events`;
        const publicPath = "/v1/runs/{run_id}/events";
        const idleTimeoutMessage = `Hermes events stream was idle for ${this.streamIdleTimeoutMs}ms: ${publicPath}`;
        const requestSignal = createRequestSignal(requestOptions.signal, this.timeoutMs, `Hermes events request timed out after ${this.timeoutMs}ms: ${publicPath}`);
        let response;
        try {
            response = await fetch(`${this.baseUrl}${path}`, {
                method: "GET",
                redirect: "error",
                headers: this.headers({ accept: "text/event-stream", ...this.sessionHeaders(requestOptions.sessionKey) }),
                signal: requestSignal.signal,
            });
            if (!response.ok) {
                const metadata = await readHermesErrorMetadata(response, MAX_HERMES_JSON_RESPONSE_BYTES);
                throw new HermesRequestError(response.status, publicPath, metadata.retryAfter, "Hermes events request failed", metadata.errorCode);
            }
            if (!response.body) {
                throw new Error("Hermes events response did not include a body.");
            }
            requestSignal.clearTimeout();
            yield* parseSseStream(response.body, {
                idleTimeoutMs: this.streamIdleTimeoutMs,
                idleTimeoutMessage,
                onIdle: () => requestSignal.abort(new Error(idleTimeoutMessage)),
            });
        }
        catch (error) {
            throw requestSignal.timedOut()
                ? new Error(`Hermes events request timed out after ${this.timeoutMs}ms: ${publicPath}`)
                : error;
        }
        finally {
            requestSignal.cleanup();
        }
    }
    async requestJson(path, init) {
        const publicPath = publicHermesRequestPath(path);
        const requestSignal = createRequestSignal(init.signal ?? undefined, this.timeoutMs, `Hermes request timed out after ${this.timeoutMs}ms: ${publicPath}`);
        try {
            const response = await fetch(`${this.baseUrl}${path}`, {
                ...init,
                redirect: "error",
                signal: requestSignal.signal,
                headers: this.headers(init.headers),
            });
            if (!response.ok) {
                const metadata = await readHermesErrorMetadata(response, MAX_HERMES_JSON_RESPONSE_BYTES);
                throw new HermesRequestError(response.status, publicPath, metadata.retryAfter, "Hermes request failed", metadata.errorCode);
            }
            const body = await readBoundedResponseText(response, MAX_HERMES_JSON_RESPONSE_BYTES);
            try {
                return JSON.parse(body);
            }
            catch {
                throw new Error(`Hermes returned invalid JSON for ${publicPath}.`);
            }
        }
        catch (error) {
            throw requestSignal.timedOut()
                ? new Error(`Hermes request timed out after ${this.timeoutMs}ms: ${publicPath}`)
                : error;
        }
        finally {
            requestSignal.cleanup();
        }
    }
    headers(extra = {}) {
        return {
            accept: "application/json",
            "content-type": "application/json",
            ...(this.apiKey ? { authorization: `Bearer ${this.apiKey}` } : {}),
            ...extra,
        };
    }
    sessionHeaders(sessionKey) {
        return this.apiKey && sessionKey ? { "X-Hermes-Session-Key": sessionKey } : {};
    }
}
async function readBoundedResponseText(response, maximumBytes) {
    const declaredLength = Number(response.headers.get("content-length"));
    if (Number.isFinite(declaredLength) && declaredLength > maximumBytes) {
        await response.body?.cancel().catch(() => undefined);
        throw new Error(`Hermes response exceeded the ${maximumBytes}-byte safety limit.`);
    }
    if (!response.body)
        return "";
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let bytes = 0;
    let text = "";
    let reachedEof = false;
    try {
        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                reachedEof = true;
                break;
            }
            bytes += value.byteLength;
            if (bytes > maximumBytes) {
                throw new Error(`Hermes response exceeded the ${maximumBytes}-byte safety limit.`);
            }
            text += decoder.decode(value, { stream: true });
        }
        return text + decoder.decode();
    }
    finally {
        if (!reachedEof)
            await reader.cancel().catch(() => undefined);
        reader.releaseLock();
    }
}
async function readHermesErrorMetadata(response, maximumBytes) {
    const retryAfter = boundedRetryAfter(response);
    let body;
    try {
        body = await readBoundedResponseText(response, maximumBytes);
    }
    catch {
        // An unreadable or oversized body cannot prove a safe POST rejection.
        return { retryAfter };
    }
    let parsed;
    try {
        parsed = JSON.parse(body);
    }
    catch {
        return { retryAfter };
    }
    if (!isRecord(parsed))
        return { retryAfter };
    const nested = isRecord(parsed.error) ? parsed.error.code : undefined;
    const errorCode = boundedHermesErrorCode(nested ?? parsed.code);
    return { retryAfter, ...(errorCode ? { errorCode } : {}) };
}
function parseHermesRunSnapshot(value, expectedRunId) {
    if (!isRecord(value)) {
        throw invalidHermesRunSnapshot("response must be an object");
    }
    if (value.object !== "hermes.run") {
        throw invalidHermesRunSnapshot("object must be hermes.run");
    }
    if (!isBoundedHermesIdentifier(value.run_id)) {
        throw invalidHermesRunSnapshot("run_id must be a bounded identifier");
    }
    if (value.run_id !== expectedRunId) {
        throw invalidHermesRunSnapshot("run_id did not match the requested run");
    }
    if (value.runId !== undefined) {
        if (!isBoundedHermesIdentifier(value.runId) || value.runId !== value.run_id) {
            throw invalidHermesRunSnapshot("run identifier aliases conflict");
        }
    }
    if (typeof value.status !== "string" || !HERMES_RUN_STATUSES.has(value.status)) {
        throw invalidHermesRunSnapshot("status is unsupported");
    }
    const status = value.status;
    const snapshot = {
        object: "hermes.run",
        run_id: value.run_id,
        status,
    };
    copyOptionalRunIdentifier(value, snapshot, "session_id");
    copyOptionalRunMetadata(value, snapshot, "model");
    copyOptionalRunMetadata(value, snapshot, "last_event");
    copyOptionalRunTimestamp(value, snapshot, "created_at");
    copyOptionalRunTimestamp(value, snapshot, "updated_at");
    if (status === "completed") {
        if (typeof value.output !== "string") {
            throw invalidHermesRunSnapshot("completed output is missing");
        }
        const outputTruncated = value.output.length > MAX_HERMES_RUN_OUTPUT_CHARS;
        return {
            ...snapshot,
            status,
            output: value.output.slice(0, MAX_HERMES_RUN_OUTPUT_CHARS),
            ...(outputTruncated ? { outputTruncated: true } : {}),
            usage: parseHermesRunUsage(value.usage),
        };
    }
    if (status === "failed") {
        // Upstream failure text can contain provider, tool, host-path, or secret
        // details. The task runtime needs only the terminal fact; keep diagnostics
        // on the Hermes side and expose a stable generic boundary value here.
        return { ...snapshot, status, error: "Hermes run failed." };
    }
    if (status === "cancelled") {
        return { ...snapshot, status };
    }
    return { ...snapshot, status };
}
function parseHermesRunUsage(value) {
    if (!isRecord(value)) {
        throw invalidHermesRunSnapshot("completed usage must be an object");
    }
    const inputTokens = boundedTokenCount(value.input_tokens);
    const outputTokens = boundedTokenCount(value.output_tokens);
    const totalTokens = boundedTokenCount(value.total_tokens);
    if (inputTokens === undefined || outputTokens === undefined || totalTokens === undefined) {
        throw invalidHermesRunSnapshot("completed usage contains invalid token counts");
    }
    return {
        input_tokens: inputTokens,
        output_tokens: outputTokens,
        total_tokens: totalTokens,
    };
}
function safeParseHermesRunUsage(value) {
    if (!isRecord(value))
        return undefined;
    const inputTokens = boundedTokenCount(value.input_tokens);
    const outputTokens = boundedTokenCount(value.output_tokens);
    const totalTokens = boundedTokenCount(value.total_tokens);
    return inputTokens === undefined || outputTokens === undefined || totalTokens === undefined
        ? undefined
        : { input_tokens: inputTokens, output_tokens: outputTokens, total_tokens: totalTokens };
}
function parseHermesSessionSummary(value, expectedId) {
    if (!isRecord(value) || !isBoundedHermesIdentifier(value.id)) {
        throw new Error("Hermes returned an invalid session summary.");
    }
    if (expectedId !== undefined && value.id !== expectedId) {
        throw new Error("Hermes returned a different session than requested.");
    }
    const summary = { id: value.id };
    copyOptionalSessionText(value, summary, "source", 64);
    copyOptionalSessionText(value, summary, "model", MAX_HERMES_RUN_METADATA_CHARS);
    copyOptionalSessionText(value, summary, "title", MAX_HERMES_SESSION_TITLE_CHARS);
    copyOptionalSessionText(value, summary, "preview", MAX_HERMES_SESSION_TEXT_CHARS);
    copyOptionalSessionTimestamp(value, summary, "started_at", "startedAt");
    copyOptionalSessionTimestamp(value, summary, "ended_at", "endedAt");
    copyOptionalSessionTimestamp(value, summary, "last_active", "lastActive");
    if (value.message_count !== undefined) {
        const messageCount = boundedTokenCount(value.message_count);
        if (messageCount === undefined)
            throw new Error("Hermes returned an invalid session message count.");
        summary.messageCount = messageCount;
    }
    if (value.parent_session_id !== undefined && value.parent_session_id !== null) {
        if (!isBoundedHermesIdentifier(value.parent_session_id)) {
            throw new Error("Hermes returned an invalid parent session id.");
        }
        summary.parentSessionId = value.parent_session_id;
    }
    return summary;
}
function parseHermesSessionMessage(value) {
    if (!isRecord(value) || !["system", "user", "assistant", "tool"].includes(String(value.role))) {
        throw new Error("Hermes returned an invalid session message.");
    }
    const content = value.content === null || value.content === undefined ? "" : value.content;
    if (typeof content !== "string" || content.length > MAX_HERMES_SESSION_TEXT_CHARS * 10) {
        throw new Error("Hermes returned an invalid session message content.");
    }
    return {
        role: value.role,
        content,
    };
}
function copyOptionalSessionText(source, target, key, maximum) {
    const value = source[key];
    if (value === undefined || value === null || value === "")
        return;
    target[key] = boundedSafeText(value, maximum, `Hermes session ${key}`);
}
function copyOptionalSessionTimestamp(source, target, sourceKey, targetKey) {
    const value = source[sourceKey];
    if (value === undefined || value === null)
        return;
    if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
        throw new Error(`Hermes returned an invalid session ${sourceKey}.`);
    }
    // Hermes session timestamps use seconds; the public Hermes Live protocol
    // consistently uses integer milliseconds.
    target[targetKey] = Math.round(value * 1_000);
}
function boundedSafeText(value, maximum, label, multiline = false) {
    if (typeof value !== "string" || value.length === 0 || value.length > maximum) {
        throw new Error(`${label} must be non-empty text of at most ${maximum} characters.`);
    }
    const unsafe = multiline
        ? /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f-\u009f]/u
        : /[\u0000-\u001f\u007f-\u009f\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069]/u;
    if (unsafe.test(value))
        throw new Error(`${label} contains unsafe characters.`);
    return value;
}
function optionalBoundedSafeText(value, maximum, label) {
    if (value === undefined || value === null || value === "")
        return undefined;
    return boundedSafeText(value, maximum, label);
}
function boundedInteger(value, minimum, maximum, label) {
    if (!Number.isInteger(value) || value < minimum || value > maximum) {
        throw new Error(`${label} must be an integer between ${minimum} and ${maximum}.`);
    }
    return value;
}
function boundedTokenCount(value) {
    return typeof value === "number" && Number.isSafeInteger(value) && value >= 0
        ? value
        : undefined;
}
function copyOptionalRunIdentifier(source, target, key) {
    const value = source[key];
    if (value === undefined)
        return;
    if (!isBoundedHermesIdentifier(value)) {
        throw invalidHermesRunSnapshot(`${key} must be a bounded identifier`);
    }
    target[key] = value;
}
function copyOptionalRunMetadata(source, target, key) {
    const value = source[key];
    if (value === undefined)
        return;
    if (typeof value !== "string" ||
        value.length === 0 ||
        value.length > MAX_HERMES_RUN_METADATA_CHARS ||
        /[\u0000-\u001f\u007f-\u009f\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069]/u.test(value)) {
        throw invalidHermesRunSnapshot(`${key} must be bounded text`);
    }
    target[key] = value;
}
function copyOptionalRunTimestamp(source, target, key) {
    const value = source[key];
    if (value === undefined)
        return;
    if (typeof value !== "number" || !Number.isFinite(value) || value < 0) {
        throw invalidHermesRunSnapshot(`${key} must be a non-negative finite number`);
    }
    target[key] = value;
}
function invalidHermesRunSnapshot(reason) {
    return new Error(`Hermes returned an invalid run snapshot: ${reason}.`);
}
function isRecord(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}
function requireHermesRunId(runId) {
    if (!isBoundedHermesIdentifier(runId)) {
        throw new Error("Hermes run id must be a bounded identifier.");
    }
}
function requireHermesSessionId(sessionId) {
    if (!isBoundedHermesIdentifier(sessionId)) {
        throw new Error("Hermes session id must be a bounded identifier.");
    }
}
function boundedRetryAfter(response) {
    return boundedRetryAfterValue(response.headers.get("retry-after") ?? undefined);
}
function boundedRetryAfterValue(value) {
    if (value === undefined)
        return undefined;
    const normalized = value.trim();
    if (normalized.length === 0 ||
        normalized.length > MAX_HERMES_RETRY_AFTER_CHARS ||
        /[\u0000-\u001f\u007f]/u.test(normalized)) {
        return undefined;
    }
    if (/^\d{1,10}$/u.test(normalized)) {
        const seconds = Number(normalized);
        return Number.isSafeInteger(seconds) && seconds <= MAX_HERMES_RETRY_AFTER_SECONDS
            ? String(seconds)
            : undefined;
    }
    return /^(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4} \d{2}:\d{2}:\d{2} GMT$/u.test(normalized) &&
        Number.isFinite(Date.parse(normalized))
        ? normalized
        : undefined;
}
function boundedHermesErrorCode(value) {
    return typeof value === "string" && /^[a-z][a-z0-9_.-]{0,127}$/u.test(value)
        ? value
        : undefined;
}
function normalizeHermesRequestOptions(options) {
    if (!options) {
        return {};
    }
    return "aborted" in options && "addEventListener" in options ? { signal: options } : options;
}
function isBoundedHermesIdentifier(value) {
    return typeof value === "string"
        && value.length > 0
        && value.length <= 256
        && !/[\u0000-\u001f\u007f-\u009f\u061c\u200e\u200f\u2028\u2029\u202a-\u202e\u2066-\u2069]/u.test(value);
}
function publicHermesRequestPath(path) {
    if (["/health", "/v1/capabilities", "/v1/runs", "/api/model/options"].includes(path))
        return path;
    if (/^\/api\/sessions(?:\?.*)?$/u.test(path))
        return "/api/sessions";
    if (/^\/api\/sessions\/[^/]+\/messages$/u.test(path))
        return "/api/sessions/{session_id}/messages";
    if (/^\/api\/sessions\/[^/]+\/chat$/u.test(path))
        return "/api/sessions/{session_id}/chat";
    if (/^\/api\/sessions\/[^/]+\/model$/u.test(path))
        return "/api/sessions/{session_id}/model";
    if (/^\/api\/sessions\/[^/]+$/u.test(path))
        return "/api/sessions/{session_id}";
    if (/^\/v1\/runs\/[^/]+\/events$/u.test(path))
        return "/v1/runs/{run_id}/events";
    if (/^\/v1\/runs\/[^/]+\/stop$/u.test(path))
        return "/v1/runs/{run_id}/stop";
    if (/^\/v1\/runs\/[^/]+\/approval$/u.test(path))
        return "/v1/runs/{run_id}/approval";
    if (/^\/v1\/runs\/[^/]+$/u.test(path))
        return "/v1/runs/{run_id}";
    return "/unknown";
}
function validStreamIdleTimeout(value) {
    if (!Number.isInteger(value) || value <= 0 || value > MAX_TIMER_TIMEOUT_MS) {
        throw new Error("Hermes event-stream idle timeout must be a positive timer-safe integer.");
    }
    return value;
}
function signalInit(signal) {
    return signal ? { signal } : {};
}
function withSignal(init, signal) {
    return { ...init, ...signalInit(signal) };
}
function createRequestSignal(parentSignal, timeoutMs, timeoutMessage) {
    const controller = new AbortController();
    let timeout;
    let timedOut = false;
    const onParentAbort = () => {
        controller.abort(parentSignal?.reason ?? new Error("Hermes request aborted."));
    };
    if (parentSignal?.aborted) {
        onParentAbort();
    }
    else {
        parentSignal?.addEventListener("abort", onParentAbort, { once: true });
    }
    if (timeoutMs > 0) {
        timeout = setTimeout(() => {
            timedOut = true;
            controller.abort(new Error(timeoutMessage));
        }, timeoutMs);
    }
    const clearRequestTimeout = () => {
        if (timeout) {
            clearTimeout(timeout);
            timeout = undefined;
        }
    };
    return {
        signal: controller.signal,
        timedOut: () => timedOut,
        clearTimeout: clearRequestTimeout,
        abort: (reason) => controller.abort(reason),
        cleanup: () => {
            clearRequestTimeout();
            parentSignal?.removeEventListener("abort", onParentAbort);
        },
    };
}
//# sourceMappingURL=hermes-runs.client.js.map