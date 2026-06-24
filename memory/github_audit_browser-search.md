# GitHub Audit: Johell1NS/browser-search

**Date:** 2026-06-24
**Repo:** https://github.com/Johell1NS/browser-search
**Stars:** ~153
**Author:** Johell1NS
**License:** MIT (confirmed in repo)

## Audit Results

### Red Flags: NONE
- **Telemetry:** NONE — search goes direct to Bing/Google/etc via SearXNG
- **Dangerous patterns:** NONE — only curl/HTTP requests to local services
- **Network calls:** Only to configured SearXNG/Camofox/CloakBrowser
- **Obfuscation:** NONE

### Components
- SearXNG: Self-hosted metasearch (Google, Bing, DuckDuckGo, etc.)
- Camofox: Anti-bot browser (Playwright stealth)
- CloakBrowser: NPM package for Cloudflare/Akamai bypass

### Tested
- SearXNG running successfully on Charles port 8081
- JSON format working, news categories working
- Results match expected quality

### Verdict: 🟢 GREEN — Installed to skills/approved/browser-search, SearXNG deployed
