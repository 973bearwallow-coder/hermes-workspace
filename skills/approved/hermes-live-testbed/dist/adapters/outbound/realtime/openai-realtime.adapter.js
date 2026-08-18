import { randomUUID } from "node:crypto";
import WebSocket from "ws";
import { normalizePcm16Audio } from "../../../domain/audio/pcm.js";
import { requireLiveTaskNotification, } from "../../../application/live-gateway/ports/realtime-model.port.js";
import { errorToMessage } from "../../../domain/error-message.js";
import { selectOpenAIHermesLiveTools } from "../../../application/live-gateway/tool-definitions.js";
const OPENAI_REALTIME_PCM_SAMPLE_RATE = 24_000;
const OPENAI_CANCEL_ACK_TIMEOUT_MS = 2_000;
const OPENAI_HANDSHAKE_TIMEOUT_MS = 10_000;
const DEFAULT_PROVIDER_CONNECT_TIMEOUT_MS = 15_000;
const DEFAULT_PROVIDER_CLOSE_TIMEOUT_MS = 4_000;
const OPENAI_MAX_EVENT_BYTES = 16 * 1024 * 1024;
const OPENAI_MAX_BUFFERED_BYTES = 8 * 1024 * 1024;
export const OPENAI_MAX_HANDLED_TOOL_CALLS = 4_096;
export const OPENAI_MAX_QUEUED_RESPONSE_REQUESTS = 32;
const OPENAI_MAX_DEFERRED_VAD_INPUT_EVENTS = 32;
const OPENAI_MAX_TERMINAL_RESPONSE_IDS = 256;
const OPENAI_MAX_TRACKED_CANCEL_EVENTS = 32;
const OPENAI_RESPONSE_CANCEL_NOT_ACTIVE_CODE = "response_cancel_not_active";
export class OpenAIRealtimeAdapter {
    config;
    connectTimeoutMs;
    closeTimeoutMs;
    constructor(config, connectTimeoutMs = DEFAULT_PROVIDER_CONNECT_TIMEOUT_MS, closeTimeoutMs = DEFAULT_PROVIDER_CLOSE_TIMEOUT_MS) {
        this.config = config;
        this.connectTimeoutMs = connectTimeoutMs;
        this.closeTimeoutMs = closeTimeoutMs;
    }
    async connect(params) {
        if (!this.config.apiKey) {
            throw new Error("OPENAI_API_KEY is required when HERMES_LIVE_PROVIDER=openai.");
        }
        const url = buildRealtimeUrl(this.config.baseUrl, this.config.model);
        const headers = { Authorization: `Bearer ${this.config.apiKey}` };
        if (params.safetyIdentifier) {
            headers["OpenAI-Safety-Identifier"] = params.safetyIdentifier;
        }
        const ws = new WebSocket(url, {
            headers,
            followRedirects: false,
            handshakeTimeout: Math.min(OPENAI_HANDSHAKE_TIMEOUT_MS, this.connectTimeoutMs),
            maxPayload: OPENAI_MAX_EVENT_BYTES,
        });
        const session = new OpenAIRealtimeSession(ws, this.config, params.callbacks, this.closeTimeoutMs);
        return await new Promise((resolve, reject) => {
            let startupFailurePending = false;
            const readyTimeout = setTimeout(() => {
                onInitialError(new Error(`OpenAI Realtime session did not acknowledge session.update within ${this.connectTimeoutMs}ms.`));
            }, this.connectTimeoutMs);
            readyTimeout.unref?.();
            const cleanup = () => {
                clearTimeout(readyTimeout);
                ws.off("error", onInitialError);
                ws.off("close", onInitialClose);
                ws.off("open", onOpen);
                ws.off("message", onInitialMessage);
            };
            const onInitialError = (error) => {
                if (startupFailurePending)
                    return;
                startupFailurePending = true;
                const failure = error instanceof Error ? error : new Error(errorToMessage(error));
                cleanup();
                if (ws.readyState === WebSocket.CLOSED) {
                    reject(failure);
                    return;
                }
                const forceClose = setTimeout(() => {
                    if (ws.readyState !== WebSocket.CLOSED)
                        ws.terminate();
                }, this.closeTimeoutMs);
                forceClose.unref?.();
                ws.once("close", () => {
                    clearTimeout(forceClose);
                    reject(failure);
                });
                // Keep the connect promise pending until close is observed. The gateway
                // can then distinguish confirmed startup cleanup from an upstream
                // socket that never actually closed. Force local teardown after the
                // provider close deadline so an uncooperative peer cannot leak a socket.
                closeWebSocket(ws, 1011, "OpenAI Realtime session start failed");
            };
            const onInitialClose = (code, reason) => {
                cleanup();
                reject(new Error(`OpenAI Realtime WebSocket closed before session start: ${code} ${reason.toString("utf8")}`));
            };
            const onOpen = () => session.configure(params.systemInstruction, params.availableTools);
            const onInitialMessage = (raw) => {
                const event = parseOpenAIEvent(raw);
                if (!event) {
                    onInitialError(new Error("OpenAI Realtime event was not valid JSON."));
                }
                else if (event.type === "session.updated") {
                    session.markReady();
                    cleanup();
                    params.callbacks.onOpen?.();
                    resolve(session);
                }
                else if (event.type === "error") {
                    onInitialError(event.error ?? event);
                }
            };
            ws.once("error", onInitialError);
            ws.once("close", onInitialClose);
            ws.once("open", onOpen);
            ws.on("message", onInitialMessage);
        });
    }
}
class OpenAIRealtimeSession {
    ws;
    config;
    callbacks;
    closeTimeoutMs;
    handledToolCalls = new Map();
    terminalResponseIds = new Set();
    queuedResponses = [];
    deferredVadInputEvents = [];
    responseActive = false;
    responsePending = false;
    vadResponsesAwaitingCreation = 0;
    pendingResponseKind;
    activeResponseKind;
    activeResponseId;
    toolSuppressedResponseId;
    cancellationPending = false;
    cancelTaskNotificationWhenCreated = false;
    trackedCancelEvents = new Map();
    activeCancelEventId;
    cancelAckTimeout;
    closeOperation;
    closing = false;
    ready = false;
    audioBuffered = false;
    suppressNextVadStopResponse = false;
    constructor(ws, config, callbacks, closeTimeoutMs) {
        this.ws = ws;
        this.config = config;
        this.callbacks = callbacks;
        this.closeTimeoutMs = closeTimeoutMs;
        this.ws.on("message", (raw) => this.handleMessage(raw));
        this.ws.on("close", (code, reason) => {
            this.closing = true;
            this.resetResponseState();
            callbacks.onClose?.({ code, reason: reason.toString("utf8") });
        });
        this.ws.on("error", (error) => callbacks.onError?.(error));
    }
    configure(systemInstruction, availableTools) {
        this.sendJson(buildOpenAISessionUpdate(this.config, systemInstruction, availableTools));
    }
    markReady() {
        this.ready = true;
    }
    async sendRealtimeAudio(audio) {
        this.sendJson(buildOpenAIRealtimeAudioAppend(audio, this.config.inputAudioFormat));
        this.audioBuffered = true;
    }
    async sendText(text) {
        const responseRequest = { kind: "default" };
        this.sendInputAndRequestResponse({
            type: "conversation.item.create",
            item: { type: "message", role: "user", content: [{ type: "input_text", text }] },
        }, responseRequest);
    }
    async sendAudioStreamEnd() {
        if (!this.audioBuffered)
            return false;
        const responseRequest = { kind: "default" };
        this.assertResponseCanBeRequested(responseRequest);
        this.sendJson({ type: "input_audio_buffer.commit" });
        this.audioBuffered = false;
        this.suppressNextVadStopResponse = this.config.turnDetection !== "disabled";
        this.requestResponse(responseRequest);
        return true;
    }
    async cancelResponse(_reason, truncate) {
        const responseInFlight = this.responsePending || this.responseActive;
        if (!responseInFlight && !this.cancellationPending && !truncate) {
            return false;
        }
        if (responseInFlight && !this.cancellationPending) {
            if (this.responseActive) {
                if (!this.activeResponseId) {
                    throw new Error("OpenAI Realtime active response did not include an exact response id.");
                }
                this.beginCancellation(this.activeResponseId);
            }
            else if (this.responsePending && this.pendingResponseKind === "task_notification") {
                // A response id is assigned only by response.created. Never send an
                // untargeted cancel here: OpenAI defines that as cancelling the default
                // conversation, not this out-of-band response.
                this.cancelTaskNotificationWhenCreated = true;
            }
            else {
                this.beginCancellation();
            }
        }
        if (truncate
            && this.activeResponseKind !== "task_notification"
            && this.pendingResponseKind !== "task_notification") {
            this.sendJson(buildOpenAIConversationItemTruncate(truncate));
        }
        return true;
    }
    async sendToolResponse(call, response) {
        if (!call.id) {
            throw new Error(`OpenAI function call ${call.name} did not include a call_id.`);
        }
        const responseRequest = { kind: "default" };
        this.sendInputAndRequestResponse({
            type: "conversation.item.create",
            item: { type: "function_call_output", call_id: call.id, output: JSON.stringify(response) },
        }, responseRequest);
    }
    async sendTaskNotification(notification) {
        this.requestResponse({
            kind: "task_notification",
            response: buildOpenAITaskNotificationResponse(notification),
        });
    }
    close() {
        if (this.ws.readyState === WebSocket.CLOSED) {
            this.closing = true;
            this.resetResponseState();
            return Promise.resolve();
        }
        if (this.closeOperation)
            return this.closeOperation;
        this.closing = true;
        this.resetResponseState();
        const operation = closeWebSocketAndWait(this.ws, 1000, "session closed", this.closeTimeoutMs);
        this.closeOperation = operation;
        void operation.catch(() => {
            if (this.closeOperation === operation)
                this.closeOperation = undefined;
        });
        return operation;
    }
    handleMessage(raw) {
        if (this.closing)
            return;
        const event = parseOpenAIEvent(raw);
        if (!event) {
            this.handleProviderError(new Error("OpenAI Realtime event was not valid JSON."), true);
            return;
        }
        if (event.type === "error") {
            if (this.handleRecoverableCancelError(event))
                return;
            this.handleProviderError(event.error ?? event);
            return;
        }
        const correlatedScope = event?.type === "response.created"
            ? responseScopeForKind(this.pendingResponseKind)
            : isOpenAITerminalResponseEvent(event)
                ? responseScopeForKind(this.activeResponseKind)
                : undefined;
        const modelEvents = normalizeOpenAIRealtimeEvent(event, this.config.outputAudioFormat, {
            includeCompletedInputTranscript: Boolean(this.config.inputTranscriptionModel),
        });
        const toolEvents = modelEvents.filter((modelEvent) => modelEvent.type === "tool_call");
        const hasUnseenToolCall = toolEvents.some((modelEvent) => {
            const fingerprint = toolCallFingerprint(modelEvent.call);
            const key = modelEvent.call.id ?? fingerprint;
            return this.handledToolCalls.get(key) !== fingerprint;
        });
        const activeResponseIdBeforeEvent = this.activeResponseId;
        const responseId = openAIResponseId(event);
        const suppressUnseenToolCall = hasUnseenToolCall && (this.cancellationPending
            || Boolean(responseId && responseId === this.toolSuppressedResponseId));
        const lifecycleAccepted = this.trackResponseState(event, hasUnseenToolCall && !suppressUnseenToolCall);
        if (lifecycleAccepted === false)
            return;
        if (lifecycleAccepted === undefined && !this.acceptsResponsePayloadEvent(event))
            return;
        if (!suppressUnseenToolCall
            && toolEvents.length > 0
            && (!activeResponseIdBeforeEvent || responseId !== activeResponseIdBeforeEvent)) {
            this.handleProviderError(new Error("OpenAI Realtime tool event did not include the exact active response id."));
            return;
        }
        if (!suppressUnseenToolCall && toolEvents.length > 1) {
            this.handleProviderError(new Error("OpenAI Realtime returned multiple tool calls in one response; this session requires serialized tools."));
            return;
        }
        const deliverableEvents = [];
        for (const normalizedEvent of modelEvents) {
            const modelEvent = normalizedEvent.type === "response"
                && normalizedEvent.scope === undefined
                && correlatedScope !== undefined
                ? { ...normalizedEvent, scope: correlatedScope }
                : normalizedEvent;
            if (modelEvent.type === "tool_call") {
                if (suppressUnseenToolCall)
                    continue;
                const fingerprint = toolCallFingerprint(modelEvent.call);
                const key = modelEvent.call.id ?? fingerprint;
                const handledFingerprint = this.handledToolCalls.get(key);
                if (handledFingerprint && handledFingerprint !== fingerprint) {
                    this.handleProviderError(new Error("OpenAI Realtime reused a tool-call id for different tool data."));
                    return;
                }
                if (handledFingerprint) {
                    continue;
                }
                if (this.handledToolCalls.size >= OPENAI_MAX_HANDLED_TOOL_CALLS) {
                    this.handleProviderError(new Error(`OpenAI Realtime exceeded the safe lifetime limit of ${OPENAI_MAX_HANDLED_TOOL_CALLS} tool calls.`));
                    return;
                }
                this.handledToolCalls.set(key, fingerprint);
            }
            deliverableEvents.push(modelEvent);
        }
        for (const modelEvent of deliverableEvents) {
            this.callbacks.onEvent(modelEvent);
        }
    }
    acceptsResponsePayloadEvent(event) {
        const type = typeof event?.type === "string" ? event.type : "";
        if (!type.startsWith("response."))
            return true;
        if (!this.responseActive)
            return false;
        const responseId = openAIResponseId(event);
        return Boolean(responseId && this.activeResponseId && responseId === this.activeResponseId);
    }
    sendJson(payload) {
        if (this.ws.readyState !== WebSocket.OPEN) {
            throw new Error("OpenAI Realtime WebSocket is not open.");
        }
        const serialized = JSON.stringify(payload);
        const payloadBytes = Buffer.byteLength(serialized, "utf8");
        if (this.ws.bufferedAmount + payloadBytes > OPENAI_MAX_BUFFERED_BYTES) {
            this.ws.terminate();
            throw new Error("OpenAI Realtime WebSocket exceeded the safe outbound buffer limit.");
        }
        this.ws.send(serialized);
    }
    trackResponseState(event, deferQueuedResponse = false) {
        if (event?.type === "input_audio_buffer.speech_started") {
            this.suppressNextVadStopResponse = false;
        }
        if (event?.type === "input_audio_buffer.speech_started"
            && this.config.turnDetection !== "disabled"
            && this.responseActive
            && this.activeResponseKind !== "task_notification"
            && this.activeResponseId) {
            // With interrupt_response enabled, server VAD can stop the active
            // conversation response before a client-side cancel reaches us. Suppress
            // any late, newly completed tool call from that exact response at once.
            this.toolSuppressedResponseId = this.activeResponseId;
        }
        if (event?.type === "input_audio_buffer.speech_stopped"
            && this.config.turnDetection !== "disabled") {
            this.audioBuffered = false;
            if (this.suppressNextVadStopResponse) {
                this.suppressNextVadStopResponse = false;
                return undefined;
            }
            // VAD commits the audio turn, while this adapter owns response creation.
            // A distinct request preserves the voice-turn snapshot and serializes it
            // behind any out-of-band task announcement already in flight.
            this.vadResponsesAwaitingCreation += 1;
            try {
                this.requestResponse({ kind: "vad" });
            }
            catch (error) {
                this.handleProviderError(error);
            }
            return undefined;
        }
        if (event?.type === "response.created") {
            const responseId = openAIResponseId(event);
            if (responseId && this.terminalResponseIds.has(responseId))
                return false;
            if (this.responseActive)
                return false;
            if (responseId && this.activeResponseId && responseId !== this.activeResponseId)
                return false;
            const responseKind = this.pendingResponseKind;
            if (!this.responsePending || !responseKind) {
                this.handleProviderError(new Error("OpenAI Realtime created an unsolicited response."));
                return false;
            }
            if (!responseId) {
                this.handleProviderError(new Error("OpenAI Realtime created a response without an exact response id."));
                return false;
            }
            const observedScope = openAIResponseScope(event);
            if (!responseScopeMatchesKind(observedScope, responseKind)) {
                this.handleProviderError(new Error("OpenAI Realtime response scope did not match the scheduled response."));
                return false;
            }
            this.responsePending = false;
            this.pendingResponseKind = undefined;
            this.responseActive = true;
            this.activeResponseKind = responseKind;
            this.activeResponseId = responseId;
            if (this.cancellationPending && responseId) {
                this.toolSuppressedResponseId = responseId;
            }
            if (responseKind === "vad") {
                this.vadResponsesAwaitingCreation = Math.max(0, this.vadResponsesAwaitingCreation - 1);
            }
            if (this.vadResponsesAwaitingCreation === 0 && this.deferredVadInputEvents.length > 0) {
                if (!this.flushDeferredVadInputEvents())
                    return false;
            }
            if (this.cancelTaskNotificationWhenCreated) {
                this.cancelTaskNotificationWhenCreated = false;
                if (responseKind !== "task_notification" || !responseId) {
                    this.handleProviderError(new Error("OpenAI Realtime could not target the pending task-notification cancellation."));
                    return false;
                }
                try {
                    this.beginCancellation(responseId);
                }
                catch (error) {
                    this.handleProviderError(error);
                    return false;
                }
            }
            return true;
        }
        else if (event?.type === "response.done" ||
            event?.type === "response.cancelled" ||
            event?.type === "response.failed" ||
            event?.response?.status === "completed" ||
            event?.response?.status === "cancelled" ||
            event?.response?.status === "failed" ||
            event?.response?.status === "incomplete") {
            const responseId = openAIResponseId(event);
            if (responseId && this.terminalResponseIds.has(responseId))
                return false;
            if (responseId && this.activeResponseId && responseId !== this.activeResponseId)
                return false;
            // `response.created` precedes every terminal response on the Realtime
            // protocol. Requiring an active response makes a late duplicate unable to
            // release another queued request.
            if (!this.responseActive)
                return false;
            if (!responseId || !this.activeResponseId) {
                this.handleProviderError(new Error("OpenAI Realtime terminal response did not include the exact active response id."));
                return false;
            }
            if (!responseScopeMatchesKind(openAIResponseScope(event), this.activeResponseKind)) {
                this.handleProviderError(new Error("OpenAI Realtime terminal response scope did not match the active response."));
                return false;
            }
            if (responseId)
                this.rememberTerminalResponseId(responseId);
            if (!responseId || this.toolSuppressedResponseId === responseId) {
                this.toolSuppressedResponseId = undefined;
            }
            this.responsePending = false;
            this.pendingResponseKind = undefined;
            this.responseActive = false;
            this.activeResponseKind = undefined;
            this.activeResponseId = undefined;
            this.cancellationPending = false;
            this.activeCancelEventId = undefined;
            this.cancelTaskNotificationWhenCreated = false;
            this.clearCancelAckTimeout();
            if (!deferQueuedResponse)
                this.flushQueuedResponse();
            return true;
        }
        return undefined;
    }
    requestResponse(request) {
        if (this.closing) {
            throw new Error("OpenAI Realtime session is closing.");
        }
        if (this.responsePending ||
            this.responseActive ||
            this.cancellationPending ||
            this.queuedResponses.length > 0) {
            this.enqueueResponse(request);
            this.flushQueuedResponse();
            return;
        }
        this.createResponse(request);
    }
    handleProviderError(error, closeBeforeReady = false) {
        this.callbacks.onError?.(error);
        if (!this.ready && !closeBeforeReady)
            return;
        this.closing = true;
        this.resetResponseState();
        closeWebSocket(this.ws, 1011, "OpenAI Realtime provider error");
    }
    flushQueuedResponse() {
        if (this.closing ||
            this.queuedResponses.length === 0 ||
            this.responsePending ||
            this.responseActive ||
            this.cancellationPending) {
            return;
        }
        let requestIndex = 0;
        if (this.vadResponsesAwaitingCreation > 0) {
            const vadIndex = this.queuedResponses.findIndex((request) => request.kind === "vad");
            if (vadIndex < 0) {
                this.handleProviderError(new Error("OpenAI Realtime lost a queued VAD response."));
                return;
            }
            requestIndex = vadIndex;
        }
        const [request] = this.queuedResponses.splice(requestIndex, 1);
        if (!request)
            return;
        try {
            this.createResponse(request);
        }
        catch (error) {
            this.handleProviderError(error);
        }
    }
    createResponse(request) {
        this.responsePending = true;
        this.pendingResponseKind = request.kind;
        try {
            this.sendJson({
                type: "response.create",
                ...(request.response ? { response: request.response } : {}),
            });
        }
        catch (error) {
            this.responsePending = false;
            this.pendingResponseKind = undefined;
            throw error;
        }
    }
    sendInputAndRequestResponse(inputEvent, request) {
        this.assertResponseCanBeRequested(request);
        if (this.vadResponsesAwaitingCreation === 0) {
            this.sendJson(inputEvent);
            this.requestResponse(request);
            return;
        }
        if (this.deferredVadInputEvents.length >= OPENAI_MAX_DEFERRED_VAD_INPUT_EVENTS) {
            throw new Error(`OpenAI Realtime VAD input queue exceeded ${OPENAI_MAX_DEFERRED_VAD_INPUT_EVENTS} pending events.`);
        }
        this.deferredVadInputEvents.push(inputEvent);
        try {
            this.requestResponse(request);
        }
        catch (error) {
            this.deferredVadInputEvents.pop();
            throw error;
        }
    }
    flushDeferredVadInputEvents() {
        try {
            for (const inputEvent of this.deferredVadInputEvents)
                this.sendJson(inputEvent);
            this.deferredVadInputEvents.length = 0;
            return true;
        }
        catch (error) {
            this.handleProviderError(error);
            return false;
        }
    }
    enqueueResponse(request) {
        const tail = this.queuedResponses[this.queuedResponses.length - 1];
        if (request.kind === "default" && tail?.kind === "default") {
            return;
        }
        if (this.queuedResponses.length >= OPENAI_MAX_QUEUED_RESPONSE_REQUESTS) {
            throw new Error(`OpenAI Realtime response queue exceeded ${OPENAI_MAX_QUEUED_RESPONSE_REQUESTS} pending requests.`);
        }
        this.queuedResponses.push(request);
    }
    assertResponseCanBeRequested(request) {
        if (this.closing) {
            throw new Error("OpenAI Realtime session is closing.");
        }
        const wouldQueue = this.responsePending ||
            this.responseActive ||
            this.vadResponsesAwaitingCreation > 0 ||
            this.cancellationPending ||
            this.queuedResponses.length > 0;
        if (!wouldQueue)
            return;
        const tail = this.queuedResponses[this.queuedResponses.length - 1];
        if (request.kind === "default" && tail?.kind === "default")
            return;
        if (this.queuedResponses.length >= OPENAI_MAX_QUEUED_RESPONSE_REQUESTS) {
            throw new Error(`OpenAI Realtime response queue exceeded ${OPENAI_MAX_QUEUED_RESPONSE_REQUESTS} pending requests.`);
        }
    }
    rememberTerminalResponseId(responseId) {
        if (this.terminalResponseIds.size >= OPENAI_MAX_TERMINAL_RESPONSE_IDS) {
            const oldest = this.terminalResponseIds.values().next().value;
            if (oldest)
                this.terminalResponseIds.delete(oldest);
        }
        this.terminalResponseIds.add(responseId);
    }
    resetResponseState() {
        this.responsePending = false;
        this.responseActive = false;
        this.vadResponsesAwaitingCreation = 0;
        this.pendingResponseKind = undefined;
        this.activeResponseKind = undefined;
        this.activeResponseId = undefined;
        this.toolSuppressedResponseId = undefined;
        this.cancellationPending = false;
        this.cancelTaskNotificationWhenCreated = false;
        this.trackedCancelEvents.clear();
        this.activeCancelEventId = undefined;
        this.queuedResponses.length = 0;
        this.deferredVadInputEvents.length = 0;
        this.terminalResponseIds.clear();
        this.handledToolCalls.clear();
        this.clearCancelAckTimeout();
    }
    beginCancellation(responseId) {
        const eventId = `cancel_${randomUUID()}`;
        this.rememberCancelEvent(eventId, {
            ...(responseId ? { responseId } : {}),
            ...((this.activeResponseKind ?? this.pendingResponseKind)
                ? { responseKind: this.activeResponseKind ?? this.pendingResponseKind }
                : {}),
        });
        this.cancellationPending = true;
        if (responseId)
            this.toolSuppressedResponseId = responseId;
        this.activeCancelEventId = eventId;
        this.cancelAckTimeout = setTimeout(() => {
            this.cancelAckTimeout = undefined;
            if (!this.cancellationPending)
                return;
            const error = new Error(`OpenAI Realtime did not confirm response cancellation within ${OPENAI_CANCEL_ACK_TIMEOUT_MS}ms.`);
            this.callbacks.onError?.(error);
            this.closing = true;
            this.resetResponseState();
            closeWebSocket(this.ws, 1011, "OpenAI Realtime cancel timeout");
        }, OPENAI_CANCEL_ACK_TIMEOUT_MS);
        this.cancelAckTimeout.unref?.();
        try {
            this.sendJson(buildOpenAIResponseCancel(responseId, eventId));
        }
        catch (error) {
            this.trackedCancelEvents.delete(eventId);
            this.cancellationPending = false;
            if (responseId && this.toolSuppressedResponseId === responseId) {
                this.toolSuppressedResponseId = undefined;
            }
            this.activeCancelEventId = undefined;
            this.clearCancelAckTimeout();
            throw error;
        }
    }
    rememberCancelEvent(eventId, attempt) {
        while (this.trackedCancelEvents.size >= OPENAI_MAX_TRACKED_CANCEL_EVENTS) {
            const oldest = this.trackedCancelEvents.keys().next().value;
            if (!oldest)
                break;
            this.trackedCancelEvents.delete(oldest);
        }
        this.trackedCancelEvents.set(eventId, attempt);
    }
    handleRecoverableCancelError(event) {
        const error = event?.error;
        const eventId = typeof error?.event_id === "string" ? error.event_id : undefined;
        if (error?.type !== "invalid_request_error"
            || error?.code !== OPENAI_RESPONSE_CANCEL_NOT_ACTIVE_CODE
            || !eventId) {
            return false;
        }
        const attempt = this.trackedCancelEvents.get(eventId);
        if (!attempt)
            return false;
        // response.done can win the race with the error generated by a redundant
        // client cancel. Retain a bounded correlation ledger so that a late, exact
        // acknowledgement stays harmless without weakening unrelated errors.
        if (this.activeCancelEventId !== eventId) {
            this.trackedCancelEvents.delete(eventId);
            return true;
        }
        // Release queued work only when the cancel targeted the exact response that
        // this adapter still considers active. A pending anonymous response cannot
        // be reconciled safely from a no-active error alone.
        if (!attempt.responseId
            || !this.responseActive
            || this.activeResponseId !== attempt.responseId) {
            return false;
        }
        const responseId = attempt.responseId;
        const responseKind = attempt.responseKind ?? this.activeResponseKind;
        this.trackedCancelEvents.delete(eventId);
        this.rememberTerminalResponseId(responseId);
        this.responsePending = false;
        this.pendingResponseKind = undefined;
        this.responseActive = false;
        this.activeResponseKind = undefined;
        this.activeResponseId = undefined;
        if (this.toolSuppressedResponseId === responseId) {
            this.toolSuppressedResponseId = undefined;
        }
        this.cancellationPending = false;
        this.activeCancelEventId = undefined;
        this.cancelTaskNotificationWhenCreated = false;
        this.clearCancelAckTimeout();
        this.callbacks.onEvent({
            type: "response",
            status: "cancelled",
            responseId,
            scope: responseKind === "task_notification" ? "task_notification" : "conversation",
        });
        this.flushQueuedResponse();
        return true;
    }
    clearCancelAckTimeout() {
        if (this.cancelAckTimeout) {
            clearTimeout(this.cancelAckTimeout);
            this.cancelAckTimeout = undefined;
        }
    }
}
export function buildOpenAITaskNotificationResponse(notification) {
    const { announcement } = requireLiveTaskNotification(notification);
    return {
        conversation: "none",
        input: [],
        instructions: `Say exactly this one short task-status sentence and nothing else: ${JSON.stringify(announcement)}`,
        output_modalities: ["audio"],
        tools: [],
        tool_choice: "none",
        metadata: { hermes_live_purpose: "task_notification" },
    };
}
function openAIResponseId(event) {
    return typeof event?.response?.id === "string"
        ? event.response.id
        : typeof event?.response_id === "string"
            ? event.response_id
            : undefined;
}
function openAIResponseScope(event) {
    const response = event?.response;
    if (response?.metadata?.hermes_live_purpose === "task_notification")
        return "task_notification";
    if (response?.conversation_id === null)
        return "task_notification";
    if (typeof response?.conversation_id === "string")
        return "conversation";
    return undefined;
}
function responseScopeMatchesKind(scope, kind) {
    if (!scope || !kind)
        return true;
    return scope === "task_notification"
        ? kind === "task_notification"
        : kind !== "task_notification";
}
function responseScopeForKind(kind) {
    if (!kind)
        return undefined;
    return kind === "task_notification" ? "task_notification" : "conversation";
}
function isOpenAITerminalResponseEvent(event) {
    return event?.type === "response.done"
        || event?.type === "response.cancelled"
        || event?.type === "response.failed"
        || ["completed", "cancelled", "failed", "incomplete"].includes(event?.response?.status);
}
function closeWebSocket(ws, code, reason) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.close(code, reason);
    }
    else if (ws.readyState === WebSocket.CONNECTING) {
        ws.terminate();
    }
}
function closeWebSocketAndWait(ws, code, reason, timeoutMs) {
    if (ws.readyState === WebSocket.CLOSED)
        return Promise.resolve();
    return new Promise((resolve, reject) => {
        let timeout;
        const cleanup = () => {
            if (timeout)
                clearTimeout(timeout);
            ws.off("close", onClose);
        };
        const onClose = () => {
            cleanup();
            resolve();
        };
        ws.once("close", onClose);
        timeout = setTimeout(() => {
            cleanup();
            if (ws.readyState !== WebSocket.CLOSED)
                ws.terminate();
            reject(new Error(`OpenAI Realtime session did not confirm closure within ${timeoutMs}ms.`));
        }, timeoutMs);
        timeout.unref?.();
        if (ws.readyState === WebSocket.CLOSED) {
            onClose();
        }
        else {
            closeWebSocket(ws, code, reason);
        }
    });
}
export function normalizeOpenAIRealtimeEvent(event, outputAudioFormat = "pcm16", options = {}) {
    const events = [];
    const root = event;
    const provider = options.provider ?? "openai";
    const calls = extractOpenAIFunctionCalls(root);
    const response = normalizeOpenAIResponseLifecycle(root);
    const deferTerminalResponse = calls.length > 0 && response?.status !== "started";
    if (response && !deferTerminalResponse)
        events.push(response);
    if ((root?.type === "response.output_audio.delta" || root?.type === "response.audio.delta") && typeof root.delta === "string") {
        events.push({
            type: "audio",
            audio: {
                data: root.delta,
                mimeType: openAiAudioMimeType(outputAudioFormat, options.pcmSampleRate),
            },
        });
        const audio = events[events.length - 1];
        if (audio?.type === "audio") {
            if (typeof root.item_id === "string") {
                audio.audio.itemId = root.item_id;
            }
            if (typeof root.content_index === "number") {
                audio.audio.contentIndex = root.content_index;
            }
        }
    }
    if ((root?.type === "response.output_text.delta" ||
        root?.type === "response.output_audio_transcript.delta" ||
        root?.type === "response.audio_transcript.delta") &&
        typeof root.delta === "string") {
        events.push({ type: "text", text: root.delta });
    }
    if (options.includeCompletedOutputTranscript
        && root?.type === "response.output_audio_transcript.done"
        && typeof root.transcript === "string"
        && root.transcript.length > 0) {
        events.push({ type: "text", text: root.transcript, speaker: "assistant", final: true });
    }
    if (options.includeCompletedInputTranscript
        && root?.type === "conversation.item.input_audio_transcription.completed"
        && typeof root.transcript === "string"
        && root.transcript.length > 0) {
        events.push({ type: "text", text: root.transcript, speaker: "user", final: true });
    }
    if (root?.type === "input_audio_buffer.speech_started") {
        events.push({
            type: "input_speech_started",
            provider,
            ...(typeof root.item_id === "string" ? { itemId: root.item_id } : {}),
            ...(typeof root.audio_start_ms === "number" ? { audioStartMs: root.audio_start_ms } : {}),
        });
    }
    if (root?.type === "input_audio_buffer.speech_stopped") {
        events.push({
            type: "input_speech_stopped",
            provider,
            ...(typeof root.item_id === "string" ? { itemId: root.item_id } : {}),
            ...(typeof root.audio_end_ms === "number" ? { audioEndMs: root.audio_end_ms } : {}),
        });
    }
    for (const call of calls) {
        events.push({ type: "tool_call", call });
    }
    if (response && deferTerminalResponse)
        events.push(response);
    return events;
}
function normalizeOpenAIResponseLifecycle(root) {
    const responseId = typeof root?.response?.id === "string"
        ? root.response.id
        : typeof root?.response_id === "string"
            ? root.response_id
            : undefined;
    const scope = openAIResponseScope(root);
    if (root?.type === "response.created") {
        return {
            type: "response",
            status: "started",
            ...(responseId ? { responseId } : {}),
            ...(scope ? { scope } : {}),
        };
    }
    const providerStatus = root?.response?.status;
    if (root?.type === "response.cancelled" || providerStatus === "cancelled") {
        return {
            type: "response",
            status: "cancelled",
            ...(responseId ? { responseId } : {}),
            ...(scope ? { scope } : {}),
        };
    }
    if (root?.type === "response.failed" ||
        providerStatus === "failed" ||
        providerStatus === "incomplete") {
        return {
            type: "response",
            status: "failed",
            ...(responseId ? { responseId } : {}),
            ...(scope ? { scope } : {}),
            error: "OpenAI Realtime response failed.",
        };
    }
    if (root?.type === "response.done" || providerStatus === "completed") {
        return {
            type: "response",
            status: "completed",
            ...(responseId ? { responseId } : {}),
            ...(scope ? { scope } : {}),
        };
    }
    return undefined;
}
export function buildOpenAIRealtimeAudioAppend(audio, inputFormat = "pcm16") {
    if (inputFormat === "pcm16") {
        return { type: "input_audio_buffer.append", audio: normalizePcm16Audio(audio, OPENAI_REALTIME_PCM_SAMPLE_RATE).data };
    }
    const actual = audio.mimeType.split(";")[0]?.trim().toLowerCase();
    const expected = inputFormat === "g711_ulaw" ? "audio/pcmu" : "audio/pcma";
    if (actual !== expected) {
        throw new Error(`OpenAI Realtime input format ${inputFormat} expects ${expected} audio.`);
    }
    return { type: "input_audio_buffer.append", audio: audio.data };
}
export function buildOpenAIResponseCancel(responseId, eventId) {
    return {
        type: "response.cancel",
        ...(eventId ? { event_id: eventId } : {}),
        ...(responseId ? { response_id: responseId } : {}),
    };
}
export function buildOpenAIConversationItemTruncate(truncate) {
    return {
        type: "conversation.item.truncate",
        item_id: truncate.itemId,
        content_index: truncate.contentIndex,
        audio_end_ms: Math.max(0, Math.round(truncate.audioEndMs)),
    };
}
export function buildOpenAISessionUpdate(config, systemInstruction, availableTools) {
    const tools = selectOpenAIHermesLiveTools(availableTools);
    return {
        type: "session.update",
        session: {
            type: "realtime",
            model: config.model,
            instructions: systemInstruction,
            output_modalities: ["audio"],
            audio: {
                input: {
                    format: openAiSessionAudioFormat(config.inputAudioFormat),
                    turn_detection: openAiTurnDetection(config.turnDetection),
                    ...(config.inputTranscriptionModel
                        ? {
                            transcription: {
                                model: config.inputTranscriptionModel,
                                ...(config.inputTranscriptionLanguage ? { language: config.inputTranscriptionLanguage } : {}),
                            },
                        }
                        : {}),
                },
                output: {
                    format: openAiSessionAudioFormat(config.outputAudioFormat),
                    voice: config.voice,
                },
            },
            ...(isOpenAIReasoningRealtimeModel(config.model)
                ? { reasoning: { effort: config.reasoningEffort }, parallel_tool_calls: false }
                : {}),
            tools,
            tool_choice: tools.length > 0 ? "auto" : "none",
        },
    };
}
function isOpenAIReasoningRealtimeModel(model) {
    return model.startsWith("gpt-realtime-2");
}
function parseOpenAIEvent(raw) {
    try {
        return JSON.parse(raw.toString("utf8"));
    }
    catch {
        return undefined;
    }
}
function extractOpenAIFunctionCalls(root) {
    const calls = [];
    if (root?.type === "response.function_call_arguments.done") {
        calls.push({ id: root.call_id, name: String(root.name ?? ""), args: normalizeArgs(root.arguments ?? {}) });
    }
    const outputItems = [];
    if (root?.type === "response.done"
        && root?.response?.status === "completed"
        && Array.isArray(root.response.output)) {
        outputItems.push(...root.response.output);
    }
    if (root?.type === "response.output_item.done" && root?.item) {
        outputItems.push(root.item);
    }
    for (const item of outputItems) {
        if (item.type === "function_call"
            && (item.status === undefined || item.status === "completed")) {
            calls.push({ id: item.call_id, name: String(item.name ?? ""), args: normalizeArgs(item.arguments ?? {}) });
        }
    }
    return calls.filter((call) => call.name.length > 0);
}
function toolCallFingerprint(call) {
    return `${call.name}\0${JSON.stringify(call.args)}`;
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
function buildRealtimeUrl(baseUrl, model) {
    const url = new URL(baseUrl);
    url.searchParams.set("model", model);
    return url.toString();
}
function openAiAudioMimeType(format, pcmSampleRate = OPENAI_REALTIME_PCM_SAMPLE_RATE) {
    if (format === "pcm16") {
        return `audio/pcm;rate=${pcmSampleRate}`;
    }
    return format === "g711_ulaw" ? "audio/pcmu;rate=8000" : "audio/pcma;rate=8000";
}
function openAiTurnDetection(turnDetection) {
    if (turnDetection === "disabled") {
        return null;
    }
    // VAD still commits turns and interrupts default-conversation output. The
    // adapter creates each response itself so a voice turn can be serialized
    // safely behind a response-scoped task announcement.
    return { type: turnDetection, create_response: false, interrupt_response: true };
}
function openAiSessionAudioFormat(format) {
    if (format === "pcm16") {
        return { type: "audio/pcm", rate: OPENAI_REALTIME_PCM_SAMPLE_RATE };
    }
    return format === "g711_ulaw" ? { type: "audio/pcmu" } : { type: "audio/pcma" };
}
//# sourceMappingURL=openai-realtime.adapter.js.map