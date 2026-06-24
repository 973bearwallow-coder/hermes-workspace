---
name: kimi-webbridge
category: devops
description: "Use Kimi WebBridge daemon (port 10086) to control the local Chrome browser on charles for web scraping, navigation, and interaction. Primary browser automation tool — replaces xdotool+OCR."
---

# Kimi WebBridge — Browser Automation on charles

The Kimi WebBridge daemon runs on charles at `http://127.0.0.1:10086`. It controls the local Chrome browser via an HTTP API. This is the **primary method** for web scraping and browser automation — far superior to xdotool+OCR.

## Quick Reference

```bash
# All commands go to:
POST http://127.0.0.1:10086/command
Content-Type: application/json
Body: {"action": "...", "args": {...}, "session": "unique-name"}
```

## Actions

| Action | Args | Description |
|--------|------|-------------|
| `navigate` | `url`, `newTab` (bool), `group_title` | Navigate to URL |
| `snapshot` | — | Get accessibility tree with element refs |
| `click` | `selector` ("@eN" or CSS) | Click element |
| `fill` | `selector`, `value` | Fill input field |
| `evaluate` | `code` (JS string) | Execute JavaScript |
| `screenshot` | `path` | Save screenshot to file |
| `list_tabs` | — | List open Chrome tabs |
| `close_session` | — | Close session tabs |

## Python Helper

For anything beyond simple curl, use a Python helper:

```python
import subprocess, json

WEBADDR = "http://127.0.0.1:10086/command"

def wb(session, action, **kwargs):
    payload = {"action": action, "args": kwargs, "session": session}
    cmd = ["curl", "-s", "-X", "POST", WEBADDR,
           "-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout)

def js(session, code):
    r = wb(session, "evaluate", code=code)
    return r.get("data", {}).get("value", "")
```

## Common Patterns

### Navigate and read page
```python
wb("mytask", "navigate", url="https://example.com", newTab=True)
time.sleep(5)
text = js("mytask", "document.body.innerText")
```

### Click element from snapshot
```python
# Get snapshot to find ref
snap = wb("mytask", "snapshot")
# Parse tree to find element ref (e.g., "@e21")
wb("mytask", "click", selector="@e21")
time.sleep(2)
```

### Extract all links
```python
val = js("mytask", """
JSON.stringify(Array.from(document.querySelectorAll('a'))
  .filter(a => a.href.length > 20 && a.innerText.trim().length > 2)
  .map(a => ({text: a.innerText.trim().substring(0,100), href: a.href})))
""")
links = json.loads(val) if isinstance(val, str) else []
```

### Scroll and re-read
```python
js("mytask", "window.scrollBy(0, 3000)")
time.sleep(3)
text = js("mytask", "document.body.innerText")
```

### Navigate to specific post/page directly
```python
# For SPAs, navigate directly to the URL if known
wb("mytask", "navigate", url="https://www.skool.com/ai-profit-lab-7462/slug-here", newTab=False)
time.sleep(5)
```

## Session Management

- Use unique session names per task: `"boardroom"`, `"skool-scrape"`, `"research-xyz"`
- `newTab: true` opens a fresh tab; `newTab: false` reuses the session tab
- Always include `group_title` to organize tabs in Chrome
- Close sessions when done: `wb("mytask", "close_session")`

## Chrome Login State

Chrome on charles is logged into:
- **Skool** (ai-profit-lab-7462): `973bearwallow@gmail.com`
- **Google Meet**: `973bearwallow@gmail.com`
- **Gmail**: `973bearwallow@gmail.com`

No re-authentication needed for these sites.

## Snapshot Tree Structure

The snapshot returns a nested accessibility tree. Key patterns:
- `{'role': 'button', 'name': 'Click me', 'ref': '@e5'}` → clickable button
- `{'role': 'link', 'name': 'Post Title', 'ref': '@e12'}` → clickable link
- `{'role': 'textbox', 'name': 'Search', 'ref': '@e3'}` → input field
- `{'role': 'StaticText', 'name': 'plain text'}` → non-interactive text

Use refs for reliable clicking: `wb("s", "click", selector="@e12")`

## Evaluate JS — Common Patterns

```python
# Get clean page text (PREFERRED over OCR)
text = js("s", "document.body.innerText")

# Get specific element text
text = js("s", "document.querySelector('.post-content').innerText")

# Click element by text match
js("s", "Array.from(document.querySelectorAll('a')).filter(a => a.textContent.includes('Memory Systems locally'))[0].click()")

# Get all text from specific container
text = js("s", "document.querySelector('[class*=\"post\"]').innerText")
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 403 on WebSocket | Use HTTP POST, not WebSocket |
| `extension_connected: false` | Click Kimi WebBridge extension icon in Chrome toolbar |
| Session not found | Create with `navigate` + `newTab: true` first |
| Stale refs | Take fresh `snapshot` before each `click` |
| Page not loading | Increase `time.sleep()` after `navigate` |
| SPA not rendering | Wait longer (7-10s) or scroll to trigger lazy load |

## xdotool Fallback

For non-browser desktop GUI automation (e.g., clicking OS dialogs, window management):
```bash
DISPLAY=:1 xdotool mousemove X Y click 1
DISPLAY=:1 xdotool type "text"
DISPLAY=:1 xdotool key Return
```

## Key Rule

**Always prefer Kimi WebBridge over xdotool+OCR for browser tasks.** The WebBridge gives direct DOM access — clean text, reliable element selection, no coordinate hunting.
