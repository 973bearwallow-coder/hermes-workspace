import { GoogleGenAI, Modality } from "@google/genai";
import { GEMINI_LIVE_INPUT_SAMPLE_RATE, normalizePcm16Audio } from "../../../domain/audio/pcm.js";
import { isSafeGoogleCloudLocation, isSafeGoogleCloudProject, isSafeGoogleGenAiApiVersion, } from "../../../config.js";
import { selectHermesLiveToolDeclarations } from "../../../application/live-gateway/tool-definitions.js";
import { requireLiveTaskNotification, } from "../../../application/live-gateway/ports/realtime-model.port.js";
const DEFAULT_PROVIDER_CLOSE_TIMEOUT_MS = 4_000;
const GEMINI_DEVELOPER_API_BASE_URL = "https://generativelanguage.googleapis.com/";
const VERTEX_GLOBAL_API_BASE_URL = "https://aiplatform.googleapis.com/";
const VERTEX_MULTI_REGIONAL_LOCATIONS = new Set(["us", "eu"]);
export class GeminiLiveAdapter {
    config;
    closeTimeoutMs;
    constructor(config, closeTimeoutMs = DEFAULT_PROVIDER_CLOSE_TIMEOUT_MS) {
        this.config = config;
        this.closeTimeoutMs = closeTimeoutMs;
    }
    async connect(params) {
        this.assertConfigured();
        const ai = this.createClient();
        const forwardMessage = createGeminiLiveEventForwarder(params.callbacks.onEvent);
        const closeConfirmation = createCloseConfirmation();
        const session = await ai.live.connect({
            model: this.config.model,
            config: buildGeminiLiveConnectConfig(params.systemInstruction, params.availableTools),
            callbacks: {
                onopen: () => params.callbacks.onOpen?.(),
                onclose: (event) => {
                    closeConfirmation.confirm();
                    params.callbacks.onClose?.(event);
                },
                onerror: (event) => params.callbacks.onError?.(event),
                onmessage: forwardMessage,
            },
        });
        return new GeminiLiveSession(session, closeConfirmation, this.closeTimeoutMs);
    }
    assertConfigured() {
        assertSafeGeminiEndpointConfig(this.config);
        if (!this.config.enterprise && !this.config.apiKey) {
            throw new Error("GEMINI_API_KEY or GOOGLE_API_KEY is required when HERMES_LIVE_PROVIDER=gemini.");
        }
    }
    createClient() {
        return new GoogleGenAI(buildGeminiClientOptions(this.config));
    }
}
export function buildGeminiClientOptions(config) {
    assertSafeGeminiEndpointConfig(config);
    const common = {
        httpOptions: { baseUrl: officialGeminiApiBaseUrl(config) },
        ...(config.apiVersion ? { apiVersion: config.apiVersion } : {}),
    };
    if (config.enterprise) {
        return {
            ...common,
            enterprise: true,
            project: config.project,
            location: config.location,
        };
    }
    return {
        ...common,
        enterprise: false,
        apiKey: config.apiKey,
    };
}
export function officialGeminiApiBaseUrl(config) {
    if (!config.enterprise)
        return GEMINI_DEVELOPER_API_BASE_URL;
    if (!isSafeGoogleCloudLocation(config.location)) {
        throw new Error("GOOGLE_CLOUD_LOCATION must be a canonical Google Cloud location.");
    }
    if (config.location === "global")
        return VERTEX_GLOBAL_API_BASE_URL;
    if (VERTEX_MULTI_REGIONAL_LOCATIONS.has(config.location)) {
        return `https://aiplatform.${config.location}.rep.googleapis.com/`;
    }
    return `https://${config.location}-aiplatform.googleapis.com/`;
}
function assertSafeGeminiEndpointConfig(config) {
    if (config.enterprise && !config.project) {
        throw new Error("GOOGLE_CLOUD_PROJECT is required when GOOGLE_GENAI_USE_ENTERPRISE=true.");
    }
    if (config.enterprise && !isSafeGoogleCloudProject(config.project)) {
        throw new Error("GOOGLE_CLOUD_PROJECT must be a canonical Google Cloud project id.");
    }
    if (!isSafeGoogleCloudLocation(config.location)) {
        throw new Error("GOOGLE_CLOUD_LOCATION must be a canonical Google Cloud location.");
    }
    if (config.apiVersion && !isSafeGoogleGenAiApiVersion(config.apiVersion)) {
        throw new Error("GOOGLE_GENAI_API_VERSION must be a bounded v1/v1beta/v1alpha-style token.");
    }
}
export function createGeminiLiveEventForwarder(onEvent) {
    let responseActive = false;
    return (message) => {
        for (const event of normalizeGeminiLiveMessage(message)) {
            const startsAssistantResponse = event.type === "audio" ||
                (event.type === "text" && (event.speaker ?? "assistant") === "assistant");
            if (startsAssistantResponse && !responseActive) {
                responseActive = true;
                onEvent({ type: "response", status: "started" });
            }
            onEvent(event);
            if (event.type === "response" && event.status !== "started")
                responseActive = false;
        }
    };
}
export function buildGeminiLiveConnectConfig(systemInstruction, availableTools) {
    const functionDeclarations = selectHermesLiveToolDeclarations(availableTools);
    return {
        responseModalities: [Modality.AUDIO],
        inputAudioTranscription: {},
        outputAudioTranscription: {},
        systemInstruction,
        ...(functionDeclarations.length > 0 ? { tools: [{ functionDeclarations }] } : {}),
    };
}
export class GeminiLiveSession {
    session;
    closeConfirmation;
    closeTimeoutMs;
    closeOperation;
    constructor(session, closeConfirmation, closeTimeoutMs = DEFAULT_PROVIDER_CLOSE_TIMEOUT_MS) {
        this.session = session;
        this.closeConfirmation = closeConfirmation;
        this.closeTimeoutMs = closeTimeoutMs;
    }
    async sendRealtimeAudio(audio) {
        await this.session.sendRealtimeInput(buildGeminiRealtimeAudioInput(audio));
    }
    async sendText(text) {
        if (typeof this.session.sendRealtimeInput === "function") {
            await this.session.sendRealtimeInput(buildGeminiRealtimeTextInput(text));
            return;
        }
        if (typeof this.session.sendClientContent === "function") {
            await this.session.sendClientContent(buildGeminiTextTurn(text));
            return;
        }
        throw new Error("Gemini Live session does not support realtime text input.");
    }
    async sendAudioStreamEnd() {
        await this.session.sendRealtimeInput({ audioStreamEnd: true });
        return true;
    }
    async cancelResponse() {
        // Gemini Live handles barge-in through live audio activity. The SDK does not
        // currently expose a direct response-cancel event.
        return false;
    }
    async sendToolResponse(call, response) {
        await this.session.sendToolResponse(buildGeminiToolResponse(call, response));
    }
    async sendTaskNotification(notification) {
        const input = buildGeminiTaskNotificationInput(notification);
        if (typeof this.session.sendRealtimeInput !== "function") {
            throw new Error("Gemini Live session does not support realtime text input for task notifications.");
        }
        // Gemini Live has no response-scoped, out-of-band trusted instruction
        // equivalent to OpenAI Realtime's conversation="none". Gemini 3.1 also
        // reserves sendClientContent for initial history; mid-session text must use
        // sendRealtimeInput. Delivery is therefore best-effort and not a durable or
        // deterministically ordered completed turn. The session instruction accepts
        // only this gateway-authenticated nonce marker as a task notification.
        await this.session.sendRealtimeInput(input);
    }
    close() {
        if (this.closeConfirmation.isClosed())
            return Promise.resolve();
        if (this.closeOperation)
            return this.closeOperation;
        const operation = this.closeAndConfirm();
        this.closeOperation = operation;
        void operation.catch(() => {
            if (this.closeOperation === operation)
                this.closeOperation = undefined;
        });
        return operation;
    }
    async closeAndConfirm() {
        if (typeof this.session.close !== "function") {
            throw new Error("Gemini Live session does not expose a close operation.");
        }
        this.session.close();
        await withTimeout(this.closeConfirmation.promise, this.closeTimeoutMs, `Gemini Live session did not confirm closure within ${this.closeTimeoutMs}ms.`);
    }
}
function createCloseConfirmation() {
    let closed = false;
    let resolveClosed;
    const promise = new Promise((resolve) => {
        resolveClosed = resolve;
    });
    return {
        promise,
        isClosed: () => closed,
        confirm: () => {
            if (closed)
                return;
            closed = true;
            resolveClosed();
        },
    };
}
async function withTimeout(promise, timeoutMs, message) {
    let timeout;
    try {
        return await Promise.race([
            promise,
            new Promise((_, reject) => {
                timeout = setTimeout(() => reject(new Error(message)), timeoutMs);
                timeout.unref?.();
            }),
        ]);
    }
    finally {
        if (timeout)
            clearTimeout(timeout);
    }
}
export function buildGeminiRealtimeAudioInput(audio) {
    const normalized = normalizePcm16Audio(audio, GEMINI_LIVE_INPUT_SAMPLE_RATE);
    return { audio: { data: normalized.data, mimeType: normalized.mimeType } };
}
export function buildGeminiRealtimeTextInput(text) {
    return { text };
}
export function buildGeminiTextTurn(text) {
    return {
        turns: [{ role: "user", parts: [{ text }] }],
        turnComplete: true,
    };
}
export function buildGeminiTaskNotificationInput(notification) {
    const { context } = requireLiveTaskNotification(notification);
    return buildGeminiRealtimeTextInput(context);
}
export function buildGeminiToolResponse(call, response) {
    if (!call.id) {
        throw new Error(`Gemini Live function call ${call.name} did not include an id.`);
    }
    return { functionResponses: [{ id: call.id, name: call.name, response }] };
}
export function normalizeGeminiLiveMessage(message) {
    const events = [];
    const root = unwrapMessage(message);
    const serverContent = root?.serverContent ?? root?.server_content;
    const inputTranscription = extractTranscription(serverContent, "inputTranscription", "input_transcription");
    const interimInputTranscription = extractTranscription(serverContent, "interimInputTranscription", "interim_input_transcription");
    const outputTranscription = extractTranscription(serverContent, "outputTranscription", "output_transcription");
    // A finalized/standard input transcript supersedes a low-latency interim
    // transcript when Gemini includes both in one server message. Fall back to
    // the interim value if the standard field is present but has no text yet.
    const userTranscriptEvent = normalizeTranscription(inputTranscription, "user") ??
        normalizeTranscription(interimInputTranscription, "user", false);
    if (userTranscriptEvent)
        events.push(userTranscriptEvent);
    const assistantTranscriptEvent = normalizeTranscription(outputTranscription, "assistant");
    if (assistantTranscriptEvent)
        events.push(assistantTranscriptEvent);
    for (const call of extractFunctionCalls(root)) {
        events.push({ type: "tool_call", call });
    }
    const cancelledToolCallIds = extractToolCallCancellationIds(root);
    if (cancelledToolCallIds) {
        events.push({ type: "tool_call_cancelled", callIds: cancelledToolCallIds });
    }
    const parts = extractParts(root);
    const hasInlineAudio = parts.some((part) => {
        const inlineData = part.inlineData ?? part.inline_data;
        return typeof inlineData?.data === "string";
    });
    const data = root?.data;
    // LiveServerMessage.data is an SDK convenience getter. It concatenates the
    // same inlineData parts exposed below, so use it only as a fallback for raw
    // messages that do not carry part-level audio.
    if (typeof data === "string" && !hasInlineAudio) {
        events.push({
            type: "audio",
            audio: { data, mimeType: root.mimeType ?? root.mime_type ?? "audio/pcm;rate=24000" },
        });
    }
    for (const part of parts) {
        const text = typeof part.text === "string" ? part.text : undefined;
        // Native-audio responses may expose the same spoken content as both a
        // model text part and outputTranscription. Prefer the transcript because
        // it carries Gemini's completion signal.
        if (text && !assistantTranscriptEvent) {
            events.push({ type: "text", text });
        }
        const inlineData = part.inlineData ?? part.inline_data;
        const data = inlineData?.data;
        if (typeof data === "string") {
            events.push({
                type: "audio",
                audio: { data, mimeType: inlineData.mimeType ?? inlineData.mime_type ?? "audio/pcm;rate=24000" },
            });
        }
    }
    if (serverContent?.interrupted === true) {
        events.push({ type: "response", status: "cancelled" });
    }
    else if (serverContent?.turnComplete === true || serverContent?.turn_complete === true) {
        events.push({ type: "response", status: "completed" });
    }
    return events;
}
function extractTranscription(serverContent, camelCaseKey, snakeCaseKey) {
    return serverContent?.[camelCaseKey] ?? serverContent?.[snakeCaseKey];
}
function normalizeTranscription(transcription, speaker, finalOverride) {
    const text = transcription?.text;
    if (typeof text !== "string" || text.length === 0) {
        return undefined;
    }
    const finished = transcription?.finished ?? transcription?.is_finished;
    const final = finalOverride ?? (typeof finished === "boolean" ? finished : undefined);
    return {
        type: "text",
        speaker,
        text,
        ...(final === undefined ? {} : { final }),
    };
}
function unwrapMessage(message) {
    if (message && typeof message === "object" && "data" in message) {
        const data = message.data;
        if (data && typeof data === "object") {
            return data;
        }
    }
    return message;
}
function extractFunctionCalls(root) {
    const candidates = [
        root?.toolCall?.functionCalls,
        root?.tool_call?.function_calls,
        root?.functionCalls,
        root?.function_calls,
        root?.serverContent?.modelTurn?.parts?.map((part) => part.functionCall ?? part.function_call),
    ];
    return candidates
        .flat()
        .filter(Boolean)
        .map((call) => ({
        id: call.id ?? call.callId ?? call.call_id,
        name: String(call.name ?? ""),
        args: normalizeArgs(call.args ?? call.arguments ?? {}),
    }))
        .filter((call) => call.name.length > 0);
}
function extractToolCallCancellationIds(root) {
    const cancellation = root?.toolCallCancellation ?? root?.tool_call_cancellation;
    if (cancellation === undefined)
        return undefined;
    const ids = cancellation?.ids;
    return Array.isArray(ids) && ids.every((id) => typeof id === "string") ? ids : [];
}
function extractParts(root) {
    return [
        root?.serverContent?.modelTurn?.parts,
        root?.server_content?.model_turn?.parts,
        root?.modelTurn?.parts,
        root?.content?.parts,
        root?.parts,
    ]
        .flat()
        .filter(Boolean);
}
function normalizeArgs(value) {
    if (typeof value === "string") {
        try {
            const parsed = JSON.parse(value);
            return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : {};
        }
        catch {
            return {};
        }
    }
    return value && typeof value === "object" && !Array.isArray(value) ? value : {};
}
//# sourceMappingURL=gemini-live.adapter.js.map