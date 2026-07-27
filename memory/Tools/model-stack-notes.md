# Model Stack & Fallbacks — Detailed Notes
_Created: June 2026. Moved from MEMORY.md during weekly consolidation._

## Current Stack (as of 2026-07-26)
| Role | Model | Notes |
|---|---|---|
| Atlas (primary) | `deepseek/deepseek-v4-flash` | Primary brain; keep this unless a real regression justifies change. |
| Fallback | `tencent/hy3` | Default fallback; Tom explicitly prefers this over Gemini. |
| Vision | `llama3.2-vision:11b` | Local Ollama vision model; use the direct API path when needed. |
| Charles / OpenClaw | `ollama/qwen2.5:7b` | Local Charles-side model from the standing protocols. |

## Fallback / Promotion Rules
1. Use the free current brain first.
2. Fall back to hy3 if needed.
3. Do not promote a new or paid model without practical evidence.
4. Stay off Gemini 2.5 Flash unless Tom explicitly overrides.

## Key Model Notes
- Keep prompts tight; avoid unnecessary context when testing stack changes.
- Prefer live health checks over assumptions.
- Record any model switch or fallback change in the project notes before changing memory.

## Model Check History
- Jun 8 2026: owl-alpha was previously the preferred free model by context length.
- Jul 2026: current Atlas brain stabilized on DeepSeek V4 Flash, with hy3 as fallback.
