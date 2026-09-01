# Coaching Call Intelligence — 2026-08-31

## Source and evidence

- Fathom recap forwarded by Tom to Atlas: Gmail message `1a058feed0a350fb`.
- Meeting: **Coaching Calls**, August 31, 2026, 182 minutes.
- Fathom call: [summary and recording](https://fathom.video/calls/802852562?tab=summary).
- Evidence limitation: this digest is based on Fathom's emailed recap, not a downloaded full transcript. Product names and performance claims remain attributed to the speakers until independently verified.

## Executive summary

The strongest recurring lesson was to separate **strategy from execution**: use a high-level reasoning conversation to clarify the goal, architecture, constraints, and migration plan, then hand a precise implementation brief to the coding agent. The call also highlighted using inexpensive remote CPU capacity for deterministic batch work, applying an independent audit pass to AI-generated code, and how a non-developer built multiple working products with AI tools.

## Key takeaways

1. **Strategize before coding.** Jeff Wurfel recommended using Claude Chat to define the goal and generate a strong implementation prompt before sending work to Claude Code. This was presented as especially useful for migrations and other complex projects. [Fathom timestamp](https://fathom.video/calls/802852562?tab=summary&timestamp=1294.0)
2. **Independent AI-code auditing is worth pursuing.** Jeff is developing a process to audit AI-generated code and remove unused sections. [Fathom timestamp](https://fathom.video/calls/802852562?tab=summary&timestamp=926.0)
3. **Offload deterministic batch work when it is genuinely cheaper.** John Mackenzie reported using a "GrokBot VPS" with 8 CPUs and 16 GB RAM for scraping and data enrichment, while keeping higher-level strategy in Claude. The claimed economics were substantial, but neither the product identity nor the resource/cost terms could be corroborated in a public web search, so this is an investigation lead—not a verified recommendation. [Fathom timestamp](https://fathom.video/calls/802852562?tab=summary&timestamp=3257.0)
4. **AI can let non-developers ship practical field tools.** Patrick Thomas reportedly built five websites and a construction-estimating companion app with job creation, photo/voice notes, GPS, and XML export. This validates the value of tightly scoped companion apps tied to an existing workflow. [Fathom timestamp](https://fathom.video/calls/802852562?tab=summary&timestamp=1980.0)
5. **Usage-based builder credits can become expensive.** The recap quotes roughly $7 per GrokBuild build after included tokens were exhausted. This supports Tom's preference for sustained-use subscriptions or local tools over quota-limited production dependencies. [Fathom timestamp](https://fathom.video/calls/802852562?tab=summary&timestamp=1860.0)

## Tom / Atlas relevance

- **Keep Atlas as strategist and Charles as executor.** For complex builds, Atlas should produce the architecture, acceptance criteria, risks, and test plan before Charles changes code.
- **Keep independent review in the loop.** Code-producing agents should not be their own final judge; use a second model or reviewer for dead code, security, regressions, and requirement coverage.
- **Do not move sensitive work to an unverified VPS.** If the reported service is identified, benchmark it only with public/synthetic data first. Confirm terms, persistence, network exposure, and true sustained cost before adoption.
- **Potential Paw Prints pattern:** a narrow mobile field companion for photos, voice notes, GPS, customer/job records, and export could be valuable—but only after the current workflow is mapped and the business need is confirmed.

## Action items from the call

- John Mackenzie: create a template/class for cost-effective VPS compute.
- Ernest Mockus: use Claude.ai to plan an AgenticOS migration.
- Jeff Wurfel: present the AI code-auditing solution later in the week.
- Kickoff team: wait for Julie's combined CKO/SKO schedule update.
- **Tom-specific assignments:** none identified in the Fathom recap.

## Atlas determination

**Adopt now:** strategy-first implementation briefs and independent code review.

**Investigate, do not adopt yet:** the reported "GrokBot VPS." Public searches returned no corroborating result for that exact product/resource claim, so its identity, security, limits, and economics remain unknown.

**No immediate build recommended:** a Paw Prints field companion app is a useful pattern, but it should follow workflow discovery rather than start from the technology demo.
