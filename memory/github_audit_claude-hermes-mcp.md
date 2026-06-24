# GitHub Audit: claude-hermes-mcp
- **Date:** 2026-06-10
- **Repo:** https://github.com/mlennie/claude-hermes-mcp
- **Version:** 0.4.0
- **Stars:** N/A (mlennie org)
- **License:** Apache-2.0

## Verdict: 🟢 Green (but not compatible with our setup)

## Summary
Well-structured MCP bridge that lets MCP clients (Claude Desktop, Codex, Cursor) delegate tasks to a local Hermes Agent via an OAuth 2.1-secured API.

## Red Flags
None found.

## Why Not Compatible
The bridge expects Hermes to expose an OpenAI-compatible API at a local port (default `http://127.0.0.1:8642/v1/chat/completions`). Our setup uses OpenClaw's gateway on port 18789 with a web UI, not a standalone Hermes API server. The `api_server` toolset isn't enabled in our Hermes config.

## What Was Done
- Installed in venv at `/home/tom/hermes-workspace/venves/hermes-mcp/`
- Sanitized copy at `skills/approved/hermes-mcp-bridge/`
- Generated OAuth credentials (stored temporarily, then shredded)

## Future Path
If we ever enable the Hermes `api_server` toolset, this bridge could be configured to connect Claude Desktop to our Hermes Agent. For now, the existing Telegram → Hermes flow covers this use case.
