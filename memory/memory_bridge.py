"""Shared memory bridge: links Atlas (Hermes) with all subbots + the voice app.

Single source of truth:
  - Subbots/apps READ the ATLAS CONTEXT section (injected into their prompts).
  - Everyone APPENDS to the SUBBOT LOG section.
  - Atlas periodically distills SUBBOT LOG into MEMORY.md.

Usage (subbots / voice app):
    sys.path.insert(0, "/home/tom/hermes-workspace/memory")
    from memory_bridge import get_shared_context, log_subbot
    ctx = get_shared_context(1500)                # inject into your system prompt
    log_subbot("voice-app", "Q: ... | A: ...")    # persist what you learned
"""
import os
import datetime

SHARED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SHARED.md")


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def get_shared_context(max_chars=1500):
    """Return the ATLAS CONTEXT section (everything before SUBBOT LOG)."""
    try:
        txt = open(SHARED_FILE).read()
    except FileNotFoundError:
        return ""
    if "## SUBBOT LOG" in txt:
        txt = txt.split("## SUBBOT LOG")[0]
    txt = txt.replace("## ATLAS CONTEXT", "").strip()
    if len(txt) > max_chars:
        txt = txt[-max_chars:]
    return txt


def log_subbot(source, text):
    """Append a timestamped line to the SUBBOT LOG section."""
    entry = f"\n- [{_now()}][{source}] {text}"
    try:
        content = open(SHARED_FILE).read()
    except FileNotFoundError:
        content = "# Shared Memory Bridge\n\n## ATLAS CONTEXT\n\n## SUBBOT LOG\n"
    if "## SUBBOT LOG" not in content:
        content += "\n## SUBBOT LOG\n"
    content = content.rstrip() + entry + "\n"
    open(SHARED_FILE, "w").write(content)
    return entry


def distill_to_memory():
    """(Manual, run by Atlas) return SUBBOT LOG lines for folding into MEMORY.md."""
    try:
        txt = open(SHARED_FILE).read()
        return txt.split("## SUBBOT LOG", 1)[1].strip() if "## SUBBOT LOG" in txt else ""
    except FileNotFoundError:
        return ""
