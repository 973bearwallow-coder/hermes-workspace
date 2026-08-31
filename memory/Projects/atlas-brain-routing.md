# Atlas Brain Routing

- Primary model: DeepSeek V4 Flash.
- Fallback model: hy3.
- Avoid Gemini unless there is a clear emergency-quality reason.
- Voicebox at `http://127.0.0.1:17493` is the default local TTS/STT/voice-cloning path.
- Vision uses local `llama3.2-vision:11b` via the Ollama API directly.
- Kimi WebBridge at `http://localhost:10086` is the browser fallback when automation is blocked.
- "the farm" means West Augusta, Virginia.
