#!/usr/bin/env python3
"""
Atlas Unified Memory Search
Searches both the Obsidian vault (semantic) and session transcripts (keyword).

Usage:
  python3 atlas_search.py "query here"
  python3 atlas_search.py "query here" --vault-only
  python3 atlas_search.py "query here" --sessions-only
  python3 atlas_search.py --rebuild          # rebuild vault index
  python3 atlas_search.py --stats            # show index stats
"""

import sys, os, json, re, subprocess

VAULT_DIR = "/home/tom/hermes-workspace/memory"
SCRIPT_DIR = "/home/tom/hermes-workspace/scripts"

def search_vault(query, top_k=5):
    """Search the vault using semantic index."""
    result = subprocess.run(
        [sys.executable, f"{SCRIPT_DIR}/memory_search.py", query],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()

def search_sessions(query, limit=3):
    """Search session transcripts using Hermes session_search (FTS5)."""
    # We can't call session_search from Python - it's a Hermes tool
    # But we can check if there's a CLI or use the DB directly
    # For now, return a placeholder telling the agent to use session_search
    return None

def show_stats():
    """Show vault index stats."""
    result = subprocess.run(
        [sys.executable, f"{SCRIPT_DIR}/memory_search.py", "--stats"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        sys.exit(0)
    
    if "--stats" in args:
        show_stats()
        sys.exit(0)
    
    if "--rebuild" in args:
        subprocess.run([sys.executable, f"{SCRIPT_DIR}/memory_search.py", "--rebuild"])
        query_args = [a for a in args if a != "--rebuild"]
        if not query_args:
            sys.exit(0)
        args = query_args
    
    vault_only = "--vault-only" in args
    sessions_only = "--sessions-only" in args
    query = " ".join(a for a in args if not a.startswith("--"))
    
    if not query:
        print("Provide a search query.")
        sys.exit(1)
    
    print(f"🔍 Atlas Memory Search: \"{query}\n")
    
    if not sessions_only:
        print("═══ VAULT (Semantic) ═══")
        vault_results = search_vault(query)
        print(vault_results)
    
    if not vault_only:
        print("\n═══ SESSIONS (Keyword) ═══")
        print("Use session_search tool for FTS5 keyword search across past conversations.")
        print(f"  session_search(query=\"{query}\", limit=3)")
