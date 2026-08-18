import { randomUUID } from "node:crypto";
import { requireLiveTaskNotification, } from "../../../application/live-gateway/ports/realtime-model.port.js";
export class MockLiveAdapter {
    async connect(params) {
        queueMicrotask(() => {
            params.callbacks.onOpen?.();
            params.callbacks.onEvent({
                type: "text",
                text: "Mock live mode is connected. Type a message to route it through Hermes.",
            });
        });
        return new MockLiveSession(params.callbacks);
    }
}
class MockLiveSession {
    callbacks;
    constructor(callbacks) {
        this.callbacks = callbacks;
    }
    async sendRealtimeAudio(_audio) {
        this.callbacks.onEvent({
            type: "text",
            text: "Mock live mode does not transcribe audio. Use the text box to test the Hermes bridge.",
        });
    }
    async sendText(text) {
        this.callbacks.onEvent({ type: "response", status: "started" });
        this.callbacks.onEvent({
            type: "tool_call",
            call: {
                id: `mock_${randomUUID()}`,
                name: "start_background_task",
                args: {
                    message: text,
                    title: text.replace(/\s+/gu, " ").trim().slice(0, 120),
                    execution_mode: "exclusive",
                    resource_keys: ["workspace:default"],
                },
            },
        });
    }
    async sendAudioStreamEnd() {
        return false;
    }
    async cancelResponse() {
        return false;
    }
    async sendToolResponse(_call, response) {
        const output = typeof response.message === "string"
            ? response.message
            : typeof response.output === "string"
                ? response.output
                : "Hermes Live updated the background task.";
        this.callbacks.onEvent({ type: "text", text: output });
        this.callbacks.onEvent({ type: "response", status: "completed" });
    }
    async sendTaskNotification(notification) {
        const { announcement } = requireLiveTaskNotification(notification);
        this.callbacks.onEvent({ type: "response", status: "started" });
        this.callbacks.onEvent({ type: "text", text: announcement, speaker: "assistant", final: true });
        this.callbacks.onEvent({ type: "response", status: "completed" });
    }
    async close() { }
}
//# sourceMappingURL=mock-live.adapter.js.map