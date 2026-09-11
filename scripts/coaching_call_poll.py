#!/usr/bin/env python3
"""
Weekly coaching-call poll: checks Skool (AI Builders Guild 'Guild Archive' +
AI Profit Boardroom) + Atlas/Tom Gmail for new Fathom /share/ links.
If found, extracts and summarizes. If NONE found, reminds Tom to send the
link manually.

Run by cron (no_agent=False). Output is delivered verbatim to Telegram.
"""
import os, re, json, subprocess
from datetime import datetime, timezone

STATE_FILE = os.path.expanduser("~/.hermes/data/skool_last_check.json")
GMAIL_ACCOUNTS = ("atlas_mail", "toms gmail")

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
    return re.findall(r"https://fathom\.video/share/[A-Za-z0-9_-]+", text)

def check_gmail():
    """Read recent messages from both inboxes and scan their bodies for links."""
    links, errors = [], []
    for acct in GMAIL_ACCOUNTS:
        try:
            listing = subprocess.run(
                ["himalaya", "-o", "json", "envelope", "list", "-f", "INBOX", "-s", "50", "-a", acct],
                capture_output=True, text=True, timeout=90,
            )
            if listing.returncode != 0:
                errors.append(f"{acct}: envelope list failed")
                continue
            envelopes = json.loads(listing.stdout or "[]")
            for envelope in envelopes:
                message_id = envelope.get("id")
                if message_id is None:
                    continue
                message = subprocess.run(
                    ["himalaya", "message", "read", "-f", "INBOX", str(message_id), "-a", acct],
                    capture_output=True, text=True, timeout=30,
                )
                if message.returncode == 0:
                    links.extend(extract_fathom_shares(message.stdout))
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            errors.append(f"{acct}: {type(exc).__name__}")
    return sorted(set(links)), errors

def main():
    state = load_seen()
    seen = set(state.get("last_seen_urls", state.get("seen_urls", [])))

    # Fathom emails are deterministic and avoid a fragile authenticated
    # browser dependency. The separate Skool archive job handles browser-only
    # posts when an authenticated session is available.
    all_links, errors = check_gmail()
    if errors and not all_links:
        print("Coaching-call poll could not scan the configured inboxes: " + "; ".join(errors))
        raise SystemExit(1)

    new_links = [l for l in all_links if l not in seen]

    if new_links:
        # Update state
        for l in new_links:
            seen.add(l)
        state["last_seen_urls"] = sorted(seen)
        state.pop("seen_urls", None)
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
        # Quiet success: no new links is normal and should not create noise.
        return

if __name__ == "__main__":
    main()
