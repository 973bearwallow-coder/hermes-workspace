# AI Builders Guild — Coffee Hour + Guild Spark

**Date reviewed:** 2026-08-28  
**Sources:** Authenticated AI Builders Guild Skool archive via Kimi WebBridge; full Fathom summaries and transcripts for both 2026-08-28 recordings.

## Executive take

The Coffee Hour was idea-heavy and often speculative; the Guild Spark was more immediately useful. The strongest opportunity for Tom is the human-approved social intelligence/publishing workflow. The strongest research lead is the token/context-efficiency work around OpenViking and John Mackenzie's AIwatch method, but the quoted 97.2% waste-reduction claim is not yet trustworthy enough to act on. GrokBot appears useful as a benchmark candidate, not a replacement for Hermes.

## Coffee Hour — 2026-08-28

### What happened

- Members discussed GrokBot's inexpensive hosted VPS: claims included 8 vCPU/16 GB RAM around the $20 tier, 24/7 persistence, and higher tiers. Heavy users reported consuming most of their credits within a day, while others had much more headroom.
- John Mackenzie proposed using cheap persistent compute for deterministic scraping at large scale, then storing research cheaply in GitHub and promoting only the useful subset into a faster paid database.
- John's AIwatch/token-efficiency discussion centered on several independent "buckets" of waste: context, memory/file structure, harness behavior, routing, and order of operations. He compared his private method with OpenViking and claimed a possible 97.2% waste reduction and 86.3% cost reduction.
- Members discussed shared/contextual memory across multiple agents, Obsidian-backed files, Git-based memory, and the difference between a model's limits and the surrounding harness's limits.
- The Guild repository was populated with member skills; utility files were moved into a tools directory. The skills remain private for Guild members, with possible future free-versus-paid access.
- Other threads included SAM.gov-style opportunity discovery, BlackSnow/Security Pet monitoring ideas, LinkedIn optimization, GitHub's recent outage, and generating richer key-card summaries.

### Atlas's opinion

- **GrokBot:** promising as cheap experimental infrastructure, but the contradictory credit-burn reports are the key fact. We should not migrate Atlas/Hermes based on the headline VPS specs. Benchmark one identical workload for cost, wall time, output quality, persistence, exportability, and privacy.
- **Large-scale scraping/database construction:** the method is sound when the data is public and the schema is defined. GitHub is useful for versioned research artifacts, but it is not a substitute for a database at scale. We should use object/file storage plus a proper index rather than treating Git as a warehouse.
- **AIwatch/OpenViking:** highly relevant to Atlas because context, memory retrieval, repeated tool calls, and handoffs directly affect cost and reliability. However, the 97.2% figure is a self-reported projection derived by stacking assumptions; it is not a reproducible benchmark. The call itself acknowledged that AI frequently gets facts, memory, and context wrong. We should inspect the OpenViking code and benchmark on fixed Hermes tasks before accepting any percentage.
- **Guild skills:** potentially valuable, but every external skill should enter quarantine, be reviewed for network calls, credentials, shell execution, and broad filesystem writes, then be rebuilt minimally before use. This aligns with the existing Toolsmith protocol.
- **Memory discussion:** directionally correct. Files are not automatically good memory; retrieval quality, scope, freshness, provenance, and conflict resolution matter more than simply accumulating documents.

## Guild Spark — 2026-08-28

### What happened

- Members demonstrated and discussed the private Guild GitHub repository and potential workshops for Git, project roadmaps, and shared Guild skills.
- Several members reported that GrokBot could reuse or recreate agent rosters originally built in Hermes/Claude and that an orchestrator could create specialist agents on demand.
- Claude's built-in browser/remote-control capability was described as handling LinkedIn posting, discovering connections, Notion integration, and posting across WordPress, X, Facebook, Instagram, and LinkedIn.
- Keith described a practical social-content pipeline:
  1. research agents monitor Reddit, Facebook groups, and other sources;
  2. active topics are ranked using engagement;
  3. a publisher drafts posts;
  4. fact-check and compliance stages run;
  5. a human selects and approves each post;
  6. the blog is published first and social posts link back to it;
  7. a separate agent watches comments and drafts replies for human review.
- Participants discussed contract-review and compliance agents, including adapting a criminal-justice-law workflow to commercial agreements.
- CMS Security's EU/GDPR positioning and BSI-related compliance opportunity were discussed, along with ideas for using NotebookLM-style material to deepen research.

### Atlas's opinion

- **Social intelligence/publishing pipeline:** this is the best idea in either call for us. It matches our community-monitoring work and could be adapted to Paw Prints or another defined business lane. The human approval step is essential; no autonomous public posting.
- **Claude browser control:** useful evidence that browser-native agents are becoming practical, but it does not eliminate the need for our Kimi WebBridge/computer-use stack. We should compare reliability, quotas, mobile control, and recoverability before changing lanes.
- **Orchestrators that spawn agents:** useful only when responsibilities and acceptance tests are explicit. More agents do not automatically improve quality; they can multiply token cost, duplicated research, and contradictory outputs.
- **Contract/compliance agents:** valuable for issue spotting and first-pass organization, not final legal advice. Any real deployment needs citations, versioned source law, confidence labels, and human review.
- **CMS/BSI opportunity:** possibly real, but low priority unless Tom intends to sell into regulated EU markets. Research demand and procurement pathways before building anything.

## Recommended actions

1. **Pilot a human-approved social intelligence lane** for one business and one platform. Measure time saved, source quality, factual corrections, engagement, and conversion—not just impressions.
2. **Benchmark GrokBot against Hermes** on five identical tasks before paying for a higher tier or moving any production workload.
3. **Research OpenViking and AIwatch claims** with a fixed corpus and baseline metrics: tokens, cost, wall time, answer quality, retrieval accuracy, and failure recovery.
4. **Inspect the Guild skills repository** and selectively sanitize only the skills that solve a current problem.
5. **Do not prioritize the BSI/GDPR or broad SAM.gov ideas yet** unless a concrete customer, funding path, or near-term use case appears.

## Assignment check

No clear Tom-specific assignment was made in either transcript. All actions above are optional adaptations recommended by Atlas, not obligations from the Guild.
