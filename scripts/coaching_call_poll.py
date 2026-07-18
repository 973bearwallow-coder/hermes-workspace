#!/usr/bin/env python3
"""
Weekly coaching-call poll: checks Skool (AI Builders Guild 'Guild Archive' +
AI Profit Boardroom) + Atlas/Tom Gmail for new Fathom /share/ links.
If found, extracts and summarizes. If NONE found, reminds Tom to send the
link manually.

Run by cron (no_agent=False). Output is delivered verbatim to Telegram.
"""
import os, re, json, subprocess, sys
from datetime import datetime, timezone

STATE_FILE = os.path.expanduser("~/.hermes/data/skool_last_check.json")
GMAIL_ACCOUNT = "atlastomsai@gmail.com"  # Atlas token reads Atlas inbox

def load_seen():
    try:
        return json.load(open(STATE_FILE))
    except Exception:
        return {"seen_urls": [], "last_run": None}

def save_seen(data):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(data, open(STATE_FILE, "w"), indent=2)

def extract_fathom_shares(text):
    """Find all fathom.video/share/... links in text."""
    return re.findall(r"https://fathom\.video/share/[A-Za-z0-9]+", text)

def check_gmail():
    """Use himalaya to pull recent Atlas + Tom inboxes, scan for Fathom share links."""
    links = []
    for acct in ["atlas_mail", "toms gmail"]:
        try:
            out = subprocess.run(
                ["himalaya", "mail", "list", "--mailbox", "INBOX", "--max", "50", "--account", acct],
                capture_output=True, text=True, timeout=90
            )
            if out.returncode == 0:
                links += extract_fathom_shares(out.stdout)
        except Exception:
            pass
    return links

def check_skool():
    """
    Poll AI Builders Guild 'Guild Archive' course for new Fathom /share/ links.
    Requires browser auth (flaky) — best-effort only; Gmail + manual link are primary.
    Returns list of fathom share URLs found.
    """
    try:
        from hermes_tools import browser_navigate, browser_console
    except Exception:
        return []
    try:
        browser_navigate("https://www.skool.com/ai-builders-guild-9932/classroom/50af6e4d")
        # extract fathom links from DOM
        res = browser_console('''var links = Array.from(document.querySelectorAll('a')).map(a=>a.href).filter(h=>h.includes('fathom.video/share')); JSON.stringify(links);''')
        import json as _json
        try:
            return _json.loads(res.get('result', '[]'))
        except Exception:
            return []
    except Exception:
        return []

def main():
    state = load_seen()
    seen = set(state.get("seen_urls", []))

    # Collect from Gmail (primary) + Skool (secondary/manual)
    gmail_links = check_gmail()
    skool_links = check_skool()
    all_links = sorted(set(gmail_links + skool_links))

    new_links = [l for l in all_links if l not in seen]

    if new_links:
        # Update state
        for l in new_links:
            seen.add(l)
        state["seen_urls"] = list(seen)
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_seen(state)

        lines = [f"🎙️ **New Fathom coaching calls found ({len(new_links)}):**\n"]
        for l in new_links:
            lines.append(f"- {l}")
        lines.append("\nAtlas: I'll process these now — extracting determinations per the coaching-call workflow.")
        print("\n".join(lines))
    else:
        # Nothing found — remind Tom
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_seen(state)
        print("⚠️ **No new Fathom coaching-call links found** in Atlas Gmail or Skool this week.\n\n"
              "Tom — if a call happened and you have the /share/ link, send it to me and I'll extract the intelligence.\n"
              "(Fathom notifications may have gone to your 973bearwallow@gmail.com inbox instead — if so, forward or paste the link.)")

if __name__ == "__main__":
    main()
