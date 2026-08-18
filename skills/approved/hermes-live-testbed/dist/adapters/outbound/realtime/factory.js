import { GeminiLiveAdapter } from "./gemini-live.adapter.js";
import { HuggingFaceRealtimeAdapter } from "./huggingface-realtime.adapter.js";
import { MockLiveAdapter } from "./mock-live.adapter.js";
import { OpenAIRealtimeAdapter } from "./openai-realtime.adapter.js";
export function createLiveModelAdapter(config) {
    switch (config.realtime.provider) {
        case "local":
            return new HuggingFaceRealtimeAdapter(config.local, config.server.providerReadyTimeoutMs);
        case "mock":
            return new MockLiveAdapter();
        case "openai":
            return new OpenAIRealtimeAdapter(config.openai, config.server.providerReadyTimeoutMs);
        case "gemini":
            return new GeminiLiveAdapter(config.gemini);
    }
}
//# sourceMappingURL=factory.js.map