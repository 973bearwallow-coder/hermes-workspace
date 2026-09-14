# OpenViking Evaluation

Source session: @session:default/voice_1788373511_fresh

## Summary
- OpenViking is an optional local sidecar, not Atlas's authoritative memory provider.
- Use it deliberately on document-retrieval and memory tasks.
- Compare results against the Hermes/Mnemosyne path before promoting it.
- Start with sanitized data and require source URIs.
- Do not change production memory unless evidence supports promotion.

## Additional candidate — Funes (2026-09-12)
- Hugging Face Funes is an Apache-2.0, local-first evidence-retrieval layer with explicit Hermes support.
- Evaluate only in quarantine/local-only mode; keep optional Hub synchronization disabled.
- Benchmark about 20 known historical decisions, including corrected and obsolete facts.
- Compare Hit@1, false-positive retrieval, provenance quality, latency, storage growth, and token use against Hermes session search, Mnemosyne, and OpenViking.
- Do not replace Mnemosyne; promote Funes only if the measured net benefit is clear.

## Note
This file tracks optional memory/retrieval sidecars so injected memory can stay compact.
