---
date: 2026-06-02
tags: [tools, browser, web, kimi]
aliases: [Kimi WebBridge, WebBridge API]
---

# Kimi WebBridge API

**Endpoint:** `http://localhost:10086`
**Protocol:** HTTP POST to `/command` with JSON body

## Session
- Use `session` param to persist tabs across calls (e.g., `boardroom`, `pawprints`)
- New session = new clean state. Reuse session to keep tabs.

## Actions

### navigate
```json
{"action": "navigate", "args": {"url": "https://example.com"}, "session": "boardroom"}
```
Returns: `{tab_id, url}`

### snapshot  
```json
{"action": "list_tabs", "session": "boardroom"}
```
Then use tab ID for targeted snapshot. Returns accessibility tree with `@e` refs for click/fill.

### click
```json
{"action": "click", "args": {"ref": "@e37"}, "session": "boardroom"}
```

### fill
```json
{"action": "fill", "args": {"ref": "@e37", "text": "hello"}, "session": "boardroom"}
```

### evaluate (JS execution)
```json
{"action": "evaluate", "args": {"expression": "document.body.innerText"}, "session": "boardroom"}
```
Returns clean text — NO OCR needed. This is the killer feature.

### screenshot
```json
{"action": "screenshot", "args": {"full_page": false, "ref": null}, "session": "boardroom"}
```

### list_tabs
```json
{"action": "list_tabs", "session": "boardroom"}
```

### close_session
```json
{"action": "close_session", "session": "boardroom"}
```

## Python Helper
Use python3 for complex multi-step interactions (avoids curl escaping issues):
```python
import urllib.request, json
def wb(action, args=None, session="boardroom"):
    body = json.dumps({"action": action, "args": args or {}, "session": session}).encode()
    req = urllib.request.Request("http://127.0.0.1:10086/command", data=body, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())
```

## Logged-in Sites (charles Chrome)
- Skool (ai-profit-lab-7462)
- Google Meet (973bearwallow@gmail.com)
- Gmail
- Google Calendar

## See Also
- [[skills/kimi-webbridge-integration/SKILL.md]]
- [[Tools/Skool-Community-Scraping]]
