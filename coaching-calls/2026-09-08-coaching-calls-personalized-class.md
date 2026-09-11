# Coaching Calls — Personalized Mini-Class

**Date:** September 8, 2026  
**Source:** Fathom recap email for “Coaching Calls” (149 minutes)  
**Fathom call:** https://fathom.video/calls/812573579?tab=summary  
**Note:** Tom joined late. The Fathom recap covered the meeting from the opening seconds, so the main material from before he joined is included below. This lesson is based on Fathom’s recap rather than a word-for-word transcript.

## The lesson: Build reliable systems, not agent theater

The most valuable idea from this call is simple: **use ordinary software for work that must happen the same way every time, and use language models where interpretation or creativity is genuinely needed.**

The speakers said purely agentic systems often waste tokens and require babysitting when asked to perform mechanical jobs such as connecting APIs, moving records, scheduling actions, or repeating fixed workflows. Their recommended alternative was a hybrid system:

- Deterministic code handles rules, states, retries, validation, duplicate prevention, scheduling, API calls, and consequential writes.
- LLMs handle classification, summarization, idea generation, drafting, and ambiguous language.
- A human approves sensitive or consequential actions until the system earns trust.

This is exactly the correct architecture for **Never Miss a Job**. Hermes can understand an inbound message, determine intent, extract useful details, draft a reply, and summarize the lead. It should not independently promise a price, change a booking, issue a refund, or keep retrying a customer-facing action without deterministic safeguards. The reliable workflow is the product; the model is one component inside it.

### What Tom probably missed near the beginning

The opening section began almost immediately:

- **0:08:** The hybrid AI strategy was introduced.
- **0:14:** The problem with purely agentic systems was framed as unreliability and constant babysitting.
- **0:55:** The speakers recommended code for the repeatable mechanical pipeline.
- **2:04:** They recommended strong LLMs for fuzzy or creative work.
- **28:00:** They returned to why this division produces a more stable and efficient system.

So the early lesson was not “build more agents.” It was **stop using agents where a dependable program would be better.**

## Mission Control: useful pattern, not proof of a business

At roughly **43:00**, the call discussed Pierpaolo’s “Mission Control”: a VPS running a general agent called Cesar, which delegates to specialized agents using models such as DeepSeek, GLM, and Kimi. The claimed benefits were specialization and lower token costs. Later examples included building a website quickly and maintaining a dashboard for personal metrics and system telemetry.

The useful pattern is a small control plane that knows:

1. what jobs exist,
2. which specialist owns each job,
3. which model is appropriate,
4. whether the job succeeded,
5. what needs human attention.

That resembles the Atlas-and-Charles arrangement already being developed. Atlas should remain the strategic conductor; Charles and narrowly scoped specialists should perform bounded work. But we should not multiply agents merely because an elaborate organization chart looks impressive. Every specialist must justify itself through better reliability, cost, speed, or quality.

A website built overnight is a demonstration of production speed—not evidence that customers want the offer, that the website converts, or that the underlying business works. For Tom’s new service, customer interviews and paid pilots remain more important than a sophisticated control center.

## Model routing and privacy

The call advocated using inexpensive models for specialized work and stronger models only where their reasoning is worth the cost. That is sensible, provided routing considers **data sensitivity**, not merely token price.

A practical hierarchy for Tom’s systems is:

- Local models for sensitive internal material when their quality is adequate.
- Trusted paid providers for difficult reasoning or high-value drafting.
- Low-cost external models only for public, non-sensitive material or sanitized inputs.
- No client personal data sent to a provider until its terms, retention, privacy, and processing boundaries are understood.

The call also made dramatic legal claims about Chinese models, GDPR violations, and possible criminal penalties. The Fathom recap does not substantiate those claims, so they should be treated as a warning to investigate—not as legal guidance. The defensible rule is simpler: know where client data goes, minimize it, obtain appropriate consent, and verify provider policy before use.

## The token-cost discussion: keep the principle, reject the gimmick

Near the end, the speakers discussed buying subscriptions directly from model providers and a supposed strategy of creating a new account each month to exploit partial-month token allocation.

The sound principle is to purchase access in a way that matches actual usage and preserves provider benefits. The account-rotation tactic is not a foundation for a serious operation: it may violate provider terms, creates administrative fragility, and can disappear without notice. A client service must have predictable, legitimate unit economics.

For Atlas, the better approach is the one already adopted: route routine jobs to free or inexpensive capacity, reserve the strongest subscription for high-value reasoning, monitor consumption, and avoid surprise overages.

## What this means for Tom now

### 1. Use Never Miss a Job as the first hybrid-system pilot
Build one narrow flow:

**missed call or web lead → capture → classify → draft response → approval or policy check → send → log → follow-up → outcome report**

Every arrow should have a deterministic owner. Hermes supplies understanding and language where needed.

### 2. Build a modest operator dashboard, not a grand Mission Control
The first dashboard only needs to show new leads, drafts awaiting approval, sends, failures, follow-ups due, and recovered-job outcomes. Add agent telemetry only when it solves an operational problem.

### 3. Prove the offer before expanding the agent team
Interview local HVAC, plumbing, and electrical owners. Run a few paid pilots. Measure response time, leads recovered, appointments created, and revenue attributed. Let real friction determine which specialists or integrations are worth building.

### 4. Keep privacy boundaries explicit
Before processing customer or Paw Prints client information, define consent, permitted data, provider routing, retention, deletion, review, and approval. Cheap inference is not cheap if it creates a trust or compliance problem.

### 5. Ignore token tricks that make the business brittle
Optimize honestly through routing, caching, fixed code, local models, batching, and provider selection. Do not design a customer service around account churn or loopholes.

## Bottom line

The call’s strongest lesson validates the direction already chosen: **language models should provide judgment and language; deterministic software should provide reliability and control.**

For Tom, the opportunity is not to imitate somebody else’s collection of agents. It is to take that architectural principle and turn it into one dependable, measurable service for local businesses. Start with Never Miss a Job, keep the first version narrow, prove that it recovers real revenue, and only then build the larger command center around what customers actually need.