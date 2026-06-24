# Model Stack & Fallbacks — Detailed Notes
_Created: June 2026. Moved from MEMORY.md during weekly consolidation._

## Current Stack (as of June 14 2026)
| Role | Model | Notes |
|---|---|---|
| Atlas (primary) | openrouter/owl-alpha | 1M ctx. Do NOT switch without asking Tom. |
| Charles (OpenClaw) | ollama/qwen3:30b-a3b | Local, RTX 3090. |
| Heavy reasoning | deepseek/deepseek-v4-pro | Use when stuck on complex debugging. |
| Vision | nemotron-nano-12b-v2-vl:free | Via vision_analyze.py script. step-3.7-flash 404s. |
| SD (charles) | dreamshaper-8 (Lykon) | Preferred for TNDC. 2-3s/img on RTX 3090. |

## Fallback Chain
1. OWL-Alpha (daily)
2. DeepSeek V4 Pro (heavy reasoning)
3. Nemotron 3 Nano (second free fallback)

## Key Model Notes
- CLIP 77-token limit truncates long prompts — keep SD prompts under 65 tokens.
- Dream Shaper 8 handles "artistic nude / centerfold" aesthetic with tasteful results.
- Negative prompts: exclude cartoon, anime, illustrated, explicit terms.
- Charles local Ollama models: qwen2:72b, qwen3:30b-a3b, gemma4:31b, etc.

## Model Check History
- Jun 8 2026: owl-alpha confirmed best free model by context length (1,048,756 tokens).
- Jun 8 2026: Full model scout report at memory/model_scout_2026-06-08.md and model_check_2026-06-08.md.
