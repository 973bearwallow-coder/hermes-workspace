# GitHub Audit: tsouth89/conduit

**Date:** 2026-06-24
**Repo:** https://github.com/tsouth89/conduit
**Stars:** ~24
**Author:** tsouth89 (Tyler South Forge AI)
**License:** MIT

## Audit Results

### Red Flags: NONE
- **Telemetry:** NONE — "no Conduit server, account, or telemetry, nothing phones home"
- **Dangerous patterns:** NONE
- **Network:** Only between gateway and configured MCP servers
- **Secrets:** OS keychain (not plaintext config)
- **OAuth:** PKCE, CSRF state, loopback redirect, RFC 8707

### Security Design (excellent)
- Local-only gateway, no listening ports
- Tool governance (per-tool enable/disable, destructive-tool deny-list)
- Audit log of all tool calls
- Minimal attack surface
- Responsible disclosure process

### Verdict: 🟢 GREEN — Not yet installed as it requires Tauri desktop app / Rust gateway build. 
Will revisit when we have active MCP servers to collapse.
