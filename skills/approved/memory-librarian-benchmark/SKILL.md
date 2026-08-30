---
name: memory-librarian-benchmark
description: Run the sanitized fixed Mnemosyne retrieval, provenance, and profile-isolation benchmark.
---

# Memory Librarian Benchmark

Run `/home/tom/hermes-workspace/scripts/memorylibrarian_benchmark.py` with the Hermes agent Python environment. Pass only when the JSON reports `passed: true`, full recall, full provenance coverage, zero false positives, and `isolation_passed: true`.

The benchmark uses two temporary, distinct databases and synthetic facts only. It must clean up automatically and must never ingest production memories, credentials, private history, or another user's profile. Keep prior dated JSON reports for trend comparison only when they contain sanitized benchmark data.

This benchmark validates the provider library and isolation invariant. Separately check `hermes memory status`; do not claim the running gateway uses the profile-isolated configuration if live status reports otherwise. Never restart the gateway without fresh, specific authorization.