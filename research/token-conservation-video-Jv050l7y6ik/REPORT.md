# Token-conservation tools from YouTube Jv050l7y6ik

**Reviewed:** 2026-09-13T15:35:11-04:00  
**Video:** [“10 Repos conserve your token usage”](https://www.youtube.com/watch?v=Jv050l7y6ik&t=279s)  
**Focus:** linked **4:39**, inside the PXPipe section  
**Scope:** read-only review. Nothing was installed, configured, or executed from the candidate repositories.

## Bottom line

Do **not** put any of these repositories in Astra’s primary Sol path yet. The best immediate savings come from Hermes’s existing micro-compaction plus stricter output discipline. The strongest external candidates are **Headroom** for reversible local tool-output compression and **Graphify** for advisory, local code navigation; both still require controlled, isolated A/B tests. **Context Mode** is a secondary experiment if its generic MCP mode can be made useful without host-specific hooks. **Ponytail** is worth a coding-only trial, never a global reasoning rule.

The linked 4:39 tool, **PXPipe, should be skipped** for Astra: the video tester reports that accuracy “was not quite there” at 4:56–5:22, while the upstream README explicitly says it is lossy and reports poor exact-identifier recall on some models.

**No external tool receives `adopt` status.** Zero degradation cannot be promised without a controlled benchmark on Tom’s real Sol/Astra workload.

## Repository identification: 11 actual GitHub URLs

The YouTube description exposes **11 exact GitHub repository URLs**. The video title says “10 Repos” and the spoken walkthrough covers **10**; `codebase-memory-mcp` is an additional description link not named in the transcript.

1. https://github.com/tashfeenahmed/freellmapi
2. https://github.com/aerovato/magic-compact
3. https://github.com/headroomlabs-ai/headroom
4. https://github.com/teamchong/pxpipe
5. https://github.com/jia-gao/leanctx
6. https://github.com/ooples/token-optimizer-mcp
7. https://github.com/mksglu/context-mode
8. https://github.com/DietrichGebert/ponytail
9. https://github.com/Graphify-Labs/graphify
10. https://github.com/diegosouzapw/OmniRoute
11. https://github.com/DeusData/codebase-memory-mcp — description-only; not spoken

No repository was inferred from a product name. The count and exact URLs come from the expanded YouTube description captured in [`youtube-description-links.json`](./youtube-description-links.json).

## Recommendations

| Repository | Status | Astra/Hermes finding | Accuracy/context risk | Privacy/latency | Fixed-subscription net benefit |
|---|---|---|---|---|---|
| **FreeLLMAPI** | **SKIP** | Provider aggregator/router, not primarily a context-saving layer. OpenAI-compatible and claims Codex support, but would route work away from the selected Sol subscription path. | Model substitution/failover is the main risk; capability and behavior can change between providers. | Router and key DB are local, but prompts still go to whichever external provider is selected. Extra gateway/failover latency. | No direct Codex OAuth bill saving. Free quotas could add capacity, but at a likely quality-consistency cost. |
| **Magic Compact** | **SKIP** | Claude Code/OpenCode plugin; no verified Hermes adapter. Development is paused for Operator Memory. Hermes already has native micro-compaction. | README calls the conversation shape “lossless,” but aggressive tool pruning still removes information from the active prompt until explicitly recovered. Host mismatch dominates. | Local disk; low runtime overhead claimed. | Duplicates current Hermes behavior without a supported integration. |
| **Headroom** | **TEST** | Best direct candidate. Local proxy/library/MCP; upstream lists Codex and reversible retrieval. No Hermes-specific adapter was verified, and ChatGPT/Codex OAuth passthrough is not documented strongly enough to assume. | Compression can omit details, but originals are cached locally and retrievable. Reversible mode should be mandatory; output-style reduction should stay off during first test. | README says compression is local and benchmarks sub-ms compression on repetitive payloads. Proxy adds another local component. | Valuable for context headroom and rate-limit/session longevity, not direct API-dollar savings. Test whether it preserves the existing Codex OAuth rail exactly. |
| **PXPipe** | **SKIP** | At 4:39 it converts dense text/history to images for vision-capable models. Proxy supports OpenAI Responses/Codex routes, but this is a poor fit for precision coding. | Upstream explicitly: “It is lossy”; exact hex/identifier recall can be poor. Video independently reports accuracy failures. | Local rendering, then image data still goes to the provider; image processing raises model dependence and likely latency. | Token count can fall, but fixed subscription and accuracy loss make the net benefit negative for Astra. |
| **LeanCtx** | **SKIP** for primary path | SDK wrapper for application code, not a transparent Hermes integration. Local LLMLingua mode requires roughly 1.2 GB of model weights. | Upstream’s full N=503 result admits **−1.8 percentage points overall**, with **−17.6 pp** on one short bucket and **−11.5 pp** on single-document QA. | Local by default; reported 47 ms p50 on GPU for its sidecar, but CPU timeouts affect savings. | Documented quality loss is unacceptable when dollars are not metered per token. |
| **Token Optimizer MCP** | **SKIP** for now | Large MCP/hooks/knowledge-graph system; overlaps Hermes tooling, compaction, and memory. Default assist mode is safer than enforcement, but integration surface is large. | Its README reports assist roughly matching control, while enforce was worse/slower and 1.471× control cost per task. | Claims no telemetry and local state. More hooks, storage, and MCP calls add complexity/latency. | Possible repeated-read savings, but poor marginal value versus existing Hermes facilities. Security source confirms the legacy hook installer automatically marks the current Claude workspace trusted. |
| **Context Mode** | **TEST** second | Strong mechanism: raw outputs stay in local SQLite/FTS5 and the model gets selected results. No prose-style enforcement. Upstream documents Codex and OpenClaw, not a Hermes-specific adapter; generic MCP should be tested without automatic hooks first. | Retrieval can miss relevant rows; raw originals remain local. Do not allow it to block native tools during the first trial. | Local database; query/index overhead instead of large prompt transfer. | Potentially useful for Tom’s verbose logs and web/tool dumps. Benefit is context capacity, not subscription cost. Competes with Headroom; test one at a time. |
| **Ponytail** | **TEST**, coding only | Upstream now documents a Hermes plugin. It encourages reuse and smaller diffs rather than compressing prompts. | Benchmark says tokens were 78% of baseline and safety stayed intact on its small coding suite, but the README warns a terse reasoning model can spend *more* thinking tokens (GPT-5.5 did). Could under-build. | Local instructions/hooks; negligible network privacy impact and modest hook latency. | Can reduce code/tool churn, but could constrain Sol reasoning. Never enable globally; test on over-building-prone implementation tasks only. |
| **Graphify** | **TEST** on large codebases | Explicit Hermes installer; deterministic local tree-sitter graph for code. Use soft/advisory mode, never strict replacement for source reads. | Graph answers are abstractions and may omit source detail. Require source verification before edits or conclusions. | Code parsing stays local; docs/media call a model only if separately configured. Indexing has upfront latency, queries should reduce repeated scans. | Useful when repeated `search/read` dominates a large repo. Little benefit on small repos or non-code tasks. |
| **OmniRoute** | **SKIP** for Astra primary | Already installed locally as **3.8.46**, but not referenced by Hermes config and no process was running. It is primarily a provider gateway; upstream also claims RTK/Caveman compression and Codex OAuth support. | Automatic routing/fallback can silently replace Sol with a weaker/different model. Compression adds another transformation layer. | Local gateway, but provider-selected traffic leaves for those providers; substantial feature/attack surface and proxy latency. | The direct Codex OAuth subscription already shows $0 metered API cost. Routing does not save that bill. If ever revisited, benchmark compression alone with routing pinned to the exact same Sol endpoint/model. |
| **Codebase Memory MCP** | **TEST alternative**, not alongside Graphify | Additional description link. Upstream documents Hermes `pre_llm_call` augmentation and local tree-sitter/LSP graph. Consider only as an alternative to Graphify. | Upstream preprint claims 83% answer quality and 10× fewer tokens—not a no-loss result. Graph output must remain advisory. | Claims 100% local and sub-ms queries after indexing; native binary reads code and writes agent config, so source/release trust needs separate review. | Potential gain on very large codebases, but duplicating Graphify/other memory systems would increase tools and context rather than conserve it. |

## Video claims versus verified findings

- **FreeLLMAPI (0:12–1:10):** video says it stacks free provider tiers and switches automatically. README verifies an OpenAI-compatible local router, provider failover, encrypted local keys, and a provider catalog. This is capacity routing, not preservation of Sol quality.
- **Magic Compact (1:12–2:30):** video calls it lossless and notes development paused. README verifies both the lossless/retrieval design claim and the pause in favor of Operator Memory; supported hosts are Claude Code/OpenCode.
- **Headroom (2:32–3:45):** video reports a file compressed to roughly 37% and “great results.” README verifies local, reversible compression, Codex support, workload-dependent savings, and very low compressor overhead claims. It does **not** establish transparent compatibility with Hermes’s current `openai-codex`/ChatGPT OAuth route.
- **PXPipe (4:13–5:32; linked point 4:39):** video says it renders context as pictures and warns of accuracy errors/hallucinations. README independently admits it is lossy and publishes exact-recall failures. This directly violates the performance-preservation requirement.
- **LeanCtx (5:34–6:43):** video reports roughly 52% saving and worries that words may be removed incorrectly. README’s stronger benchmark is more cautious: blended savings are lower and accuracy drops overall and sharply in some buckets.
- **Token Optimizer MCP (6:47–8:07):** video says it remembers prior work and warns installation turns off a Claude trust prompt. Source review narrows this: `install-hooks.sh`/`.ps1` sets `hasTrustDialogAccepted=true` for the **current workspace**. It is not evidence that every trust control is globally disabled, but it is still an automatic security-state mutation.
- **Context Mode (8:12–9:25):** video claims mid-90s to 98% reduction by indexing raw tool output locally. README verifies the 315 KB→5.4 KB benchmark claim, SQLite/FTS5 session storage, and local retrieval design; it remains upstream-authored benchmark evidence.
- **Ponytail (9:28–10:34):** video says it makes agents write less code/use what exists. README’s corrected agentic benchmark reports 22% fewer tokens on average, not a universal huge reduction, and explicitly warns some reasoning models can consume more thinking tokens.
- **Graphify (10:37–12:00):** video calls it a code knowledge graph built without model tokens. README verifies local deterministic AST graph construction for code; docs/media semantic passes can use a model if configured. The video’s “over 100,000 stars” is not evidence of accuracy.
- **OmniRoute (12:03–13:17):** video describes free/paid routing plus RTK compression. README verifies gateway, subscription/OAuth, flat-rate accounting, and compression claims. For Astra, changing models/providers is a quality change, not harmless token conservation.
- **Codebase Memory MCP:** exact repository is in the description, but it has no spoken timestamp. Upstream claims local indexing, Hermes support, and large token reductions; those are not independently replicated here.

## Current local overlap

- Hermes config currently has `compression.threshold_tokens: 80000` and micro-compaction enabled. Its documented micro-compaction already removes stale heavy tool results and superseded assistant turns before full compaction.
- Hermes tool wrappers already support the safest pattern these projects exploit: save full oversized output to disk, return only targeted excerpts, then use `read_file` pagination/search for retrieval.
- Current execution uses `openai-codex` with Sol delegation. This is a fixed ChatGPT/Codex subscription rail; fewer tokens may improve context capacity, responsiveness, and quota headroom, but do **not** automatically reduce a separately billed API invoice.
- Candidate binary check: only `omniroute` was found; package version 3.8.46. `rtk`, Headroom, Magic Compact, PXPipe, LeanCtx, Context Mode, Ponytail, Graphify, FreeLLMAPI, and Codebase Memory MCP were not found under the tested executable/module names.
- The saved process check found no running OmniRoute process. Hermes config did not reference `omniroute` or localhost port 20128.
- Memory/session searches did not reveal a prior tool-by-tool evaluation of these exact repositories, so this report is the durable local research record.

## Actionable shortlist

### Adopt now — no new software

1. Keep Hermes micro-compaction as the safety net; do **not** lower the 80k threshold merely to chase token counts without an A/B test.
2. For verbose terminal/web results, save the full artifact and return only counts, errors, and decision-relevant excerpts.
3. Search before reading; paginate narrow ranges; batch independent lookups; deduplicate and count in code.
4. After a skill is loaded, retain only its operative rules in working context; reload the full skill only after compaction or when a missing detail matters.
5. Give Sol/Astra full raw context for exact identifiers, security decisions, final diffs, and uncertain evidence. Compress repetitive logs and bulk JSON first—not instructions, user constraints, or reasoning-critical evidence.

### Controlled tests, in this order

1. **Headroom** — local + reversible mode; exact same Sol model/OAuth endpoint; output-style rewriting off.
2. **Graphify** — one large codebase; soft advisory mode; require source reads before edits. Compare with **Codebase Memory MCP** only as a separate alternative, never simultaneously.
3. **Context Mode** — MCP-only, no enforcement/hooks initially; compare against Headroom on log/JSON-heavy workflows.
4. **Ponytail** — coding-only, explicit activation; compare completed tests, diff correctness, thinking/input/output tokens, and latency.

### Benchmark acceptance gate

Use paired baseline/tool runs on representative Astra workloads: large log diagnosis, multi-file coding, security-sensitive exact identifiers, long research synthesis, and compaction recovery. Keep provider, Sol model, task text, workspace snapshot, and effort fixed. Record task success/tests, exact-detail recall, critical omissions, tool calls, context/input/output tokens where observable, wall latency, and retrieval expansions. Reject a tool on any new critical failure or material quality loss; only then compare context savings. Averages must not hide a failed security or identifier task.

## Mini lesson for Tom

The high-value distinction is **lossless offloading vs. lossy rewriting**. Tom’s largest avoidable waste is repeated full skill text, giant tool logs, broad file reads, and replayed context—not Sol’s reasoning. Let Astra keep reasoning quality and exact constraints; move bulky raw artifacts to files and retrieve small cited slices. A fixed Codex subscription changes the objective from “cheaper tokens” to **more useful work before context/quota limits, with no material quality regression**. Tool count itself has a cost: every new MCP schema, routing instruction, hook, and recovery workflow consumes context and adds failure modes.

## Sources and evidence artifacts

Primary video evidence:
- [`transcript.txt`](./transcript.txt) — required plain-text transcript fetch
- [`transcript-with-timestamps.txt`](./transcript-with-timestamps.txt) — normalized timestamped transcript
- [`youtube-description-links.json`](./youtube-description-links.json) — exact expanded-description GitHub URLs and count

Upstream evidence (GitHub metadata and README text fetched read-only; repository code was not run):
- [`upstream-repo-evidence.json`](./upstream-repo-evidence.json)
- [`upstream-evidence-summary.txt`](./upstream-evidence-summary.txt)
- [`compatibility-evidence.txt`](./compatibility-evidence.txt)
- [`token-optimizer-security-source-evidence.txt`](./token-optimizer-security-source-evidence.txt)

Local evidence:
- [`local-tool-checks.json`](./local-tool-checks.json)
- [`omniroute-process-check.json`](./omniroute-process-check.json)
- Hermes micro-compaction documentation: `/home/tom/.hermes/hermes-agent/docs/micro-compaction.md`
- Active configuration evidence: `/home/tom/.hermes/config.yaml` (only relevant non-secret fields were inspected)

Upstream source links are the 11 exact repository URLs listed above; claims attributed to a README remain maintainer claims unless explicitly identified as independently reproduced.