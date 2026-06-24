# GitHub Audit: rai yanyahya/recall

**Date:** 2026-06-24
**Repo:** https://github.com/raiyanyahya/recall
**Stars:** ~440
**Author:** rai yanyahya
**License:** MIT

## Audit Results

### Red Flags: NONE
- **Telemetry:** NONE — explicitly documented as zero telemetry, zero network
- **Dangerous patterns:** `subprocess` only for git, hardened with `_GIT_HARDENING` flags (no fsmonitor, no external diff, no hooks, cat pager)
- **Network calls:** ZERO — entirely offline
- **Obfuscation:** NONE — clean, well-documented Python
- **eval/exec:** NONE

### Security Design
- Symlink-resistant file writes (O_NOFOLLOW)
- Path traversal protection (confined to cwd)
- Git hardening (neutralizes untrusted repo config)
- Session offset tracking with incremental reads
- Stdlib-only (no pip install, numpy optional for speed)

### Performance
- Summarizer: TextRank with TF-IDF, pure Python (numpy optional)
- Tested: captures sessions correctly, generates sensible context.md
- Compatible transcript format: `{"type":"user","message":{"content":"..."}}` (MCP-style)
- Note: Claude Code's own transcripts use `queue-operation` format which differs

### Verdict: 🟢 GREEN — Installed to skills/approved/recall
