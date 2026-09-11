# GPT-6 Astra — Atlas Use Policy

Updated: 2026-09-08

## Decision

Use GPT-6 Astra proactively for the hardest and highest-value work, with dynamic routing against the live subscription allowance. Target roughly 80–90% of each weekly allowance instead of conserving capacity that will expire. Keep Sol/Terra/Luna for routine work so Astra capacity remains available when its stronger judgment matters.

## Why

- OpenAI describes Astra as its most capable model for complex reasoning, coding, computer use, research, and document creation.
- Official API specifications: 1,050,000-token context, 128,000-token maximum output, text/image input, tool use, structured outputs, skills, MCP, computer use, hosted shell, and reasoning effort from low through max.
- ARC Prize measured a major jump on ARC-AGI-3, including 99.9% with OpenAI's provider adapter, but explicitly states that this is not proof of AGI.
- Independent Artificial Analysis ranks Astra among the frontier leaders, but not unambiguously first on every real-world benchmark. It is slower and expensive at maximum reasoning.

## Best Atlas uses

1. Architecture and strategic decisions with multiple interacting constraints.
2. Difficult debugging after ordinary diagnosis stalls.
3. Independent final review of consequential code, automation, security, or data migrations.
4. Large-context synthesis across long transcripts, documents, and project history.
5. Deep research synthesis after Research Scout gathers primary evidence.
6. Novel planning where the system must infer rules, build a world model, and adapt.
7. High-value opportunity analysis: turn community/coaching material into decisions, experiments, and business opportunities.

## Poor uses

- Greetings, ordinary questions, routine summaries, simple lookups, status checks, scheduled monitoring, commodity coding, or voice conversation.
- First-pass web collection; use cheaper tools/models to gather evidence, then Astra to synthesize only when the decision merits it.
- Unverified autonomous consequential actions. Atlas/Hermes retains tool authority and verification.

## Routing policy

- Default: GPT-5.6 Sol/Luna or suitable local/free tools.
- Escalate to Astra when at least one applies:
  - A wrong answer would be expensive or hard to reverse.
  - The task spans several systems or more context than ordinary models handle reliably.
  - Two credible approaches conflict and a higher-quality adjudication is valuable.
  - Normal diagnosis has failed once and the next step requires novel reasoning.
  - Tom explicitly asks for Astra, maximum brainpower, or an independent frontier review.
- Reasoning effort:
  - `high`: normal Astra escalation.
  - `xhigh`: difficult architecture/research adjudication.
  - `max`: rare benchmark-class or exceptionally consequential work.
- Require cited evidence for current facts and execution verification for actions.
- Track whether Astra materially improved the result; do not retain it for a task class if it fails to earn its cost/latency.

## Cost and capacity guardrails

Tom's $100 subscription is a fixed Pro 5x allowance, not a $100 API-metered wallet. Included Codex use stops or falls back at the plan's rolling limits; it does not create an extra token bill unless separately purchased credits or an API key is deliberately used.

OpenAI's current estimates for Pro 5x are 25–225 local Astra messages versus 50–500 Sol messages per five-hour period. Credit/token accounting prices Astra at 2.5x Sol. Exact consumption varies with context, reasoning, tools, caching, and output length.

Local rate-limit history inspected on 2026-09-08 showed weekly peaks of approximately 67% for the week ending August 29 and 17% for the next observed cycle; the new cycle was near 2%. Historical capacity was therefore being left unused.

Dynamic policy:

- Aim for 80–90% weekly utilization, retaining 10–20% as a reserve for urgent work and measurement uncertainty.
- At under 50% halfway through a weekly cycle, broaden Astra use to deep synthesis, architecture, important code review, business opportunity analysis, and stubborn debugging.
- At under 65% with less than two days before reset, use Astra for worthwhile backlog reviews and improvements because unused allowance expires.
- At 75–90%, return to strict high-value escalation.
- Above 90%, reserve Astra for explicit requests or decisions where its advantage is likely consequential; use Sol/Terra/Luna otherwise.
- Never purchase credits or switch to API-billed use without Tom's explicit approval.

Official API list price remains $10/M uncached input tokens, $1/M cached input, and $50/M output. Inputs above 272K tokens receive higher rates. API billing is separate from included subscription usage.

## Verified local access

On 2026-09-08, Codex CLI was upgraded from 0.144.6 to 0.153.4. A read-only authenticated probe using model `gpt-6-astra` returned exactly `ASTRA_ACCESS_OK`. No Hermes default model or gateway configuration was changed.

## AGI judgment

Astra is a serious frontier jump and likely much better at long-horizon agentic work. It is not established AGI. ARC Prize explicitly says saturating ARC-AGI-3 is not proof of AGI because the benchmark remains bounded, deterministic, and closed-ended. Treat “AGI” as an attention-grabbing interpretation, not a settled technical conclusion.

## Sources

- OpenAI announcement: https://openai.com/index/gpt-6-astra/
- OpenAI model documentation: https://developers.openai.com/api/docs/models/gpt-6-astra
- ARC Prize evaluation: https://arcprize.org/blog/astra
- Independent Artificial Analysis: https://artificialanalysis.ai/models/gpt-6-astra
