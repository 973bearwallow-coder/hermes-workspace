#!/usr/bin/env python3
"""
Memory Sync — Sync memory tool entries to Obsidian vault.

Called after memory tool saves to ensure Obsidian vault stays in sync.
Also handles mem0 long-term storage.

Usage:
  python3 memory_sync.py --sync-file <vault_path> --content <content> --category <category>
  python3 memory_sync.py --search <query>
"""

import sys, os, json, hashlib, time, argparse, sqlite3

HOME = "/home/tom"
OBSIDIAN_VAULT = f"{HOME}/Documents/ObsidianVault"
WORKSPACE_MEMORY = f"{HOME}/hermes-workspace/memory"
SEARCH_DB = f"{WORKSPACE_MEMORY}/.search_index.db"

# Category → Obsidian subfolder mapping
CATEGORY_MAP = {
    "user": "Areas/People",
    "memory": "Areas/Technology",
    "daily": "Daily",
    "business": "Business",
    "projects": "Projects",
    "people": "People",
    "tools": "Tools/skills-Notes",
    "meeting": "Meeting-Notes",
    "coaching": "Business/Coaching",
    "default": "Areas/Technology",
}

def get_obsidian_path(category):
    """Determine which Obsidian subfolder to save to."""
    cat_lower = category.lower() if category else ""
    for key, folder in CATEGORY_MAP.items():
        if key in cat_lower:
            return os.path.join(OBSIDIAN_VAULT, folder)
    return os.path.join(OBSIDIAN_VAULT, CATEGORY_MAP["default"])


def sanitize_filename(text, max_len=60):
    """Create a filesystem-safe filename from text."""
    safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in text)
    safe = safe.strip().replace(" ", "_")
    return safe[:max_len]


def sync_to_obsidian(content, category=None, title=None, date_str=None):
    """
    Save content to the Obsidian vault in the appropriate subfolder.
    Creates or appends to the daily note, or creates a new note if topic-specific.
    """
    if not date_str:
        date_str = time.strftime("%Y-%m-%d")

    folder = get_obsidian_path(category)
    os.makedirs(folder, exist_ok=True)

    if category and category.lower() in ("daily", "journal"):
        # Append to daily note
        filepath = os.path.join(folder, f"{date_str}.md")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n\n## {time.strftime('%H:%M')} — {title or category}\n\n{content}\n")
        print(f"✅ Appended to daily note: {filepath}")
    else:
        # Create a topic-specific note
        slug = sanitize_filename(title or "memory-sync")
        filepath = os.path.join(folder, f"{slug}.md")
        if os.path.exists(filepath):
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(f"\n\n## {date_str} — Update\n\n{content}\n")
            print(f"✅ Appended to: {filepath}")
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title or slug}\n\n*{date_str}*\n\n{content}\n")
            print(f"✅ Created: {filepath}")

    return filepath


def rebuild_search_index():
    """Rebuild the unified search index to include new Obsidian files."""
    os.system(f"python3 {HOME}/hermes-workspace/scripts/atlas_unified_search.py --rebuild")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync memory to Obsidian vault")
    parser.add_argument("--sync-file", help="Content to sync (or read from stdin)")
    parser.add_argument("--content", help="Content string to sync")
    parser.add_argument("--category", help="Category for folder mapping")
    parser.add_argument("--title", help="Title for the note")
    parser.add_argument("--date", help="Date string (YYYY-MM-DD)")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild search index after sync")
    args = parser.parse_args()

    content = args.content
    if not content and not args.sync_file:
        content = sys.stdin.read().strip()

    if content:
        filepath = sync_to_obsidian(
            content,
            category=args.category,
            title=args.title,
            date_str=args.date,
        )
        if args.rebuild:
            rebuild_search_index()
    else:
        print("No content to sync.")
        sys.exit(1)
