#!/usr/bin/env python3
"""
Index session transcripts into the search DB.
Extracts key exchanges (user questions + assistant answers) from recent sessions
and adds them to the semantic search index.
"""

import sys, os, json, hashlib, time, urllib.request, sqlite3, re

DB_PATH = "/home/tom/hermes-workspace/memory/.search_index.db"
STATE_DB = "/home/tom/.hermes/state.db"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
MAX_SESSIONS = 20  # index last N sessions
CHUNK_SIZE = 500

def get_embedding(text):
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:2048]}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/embeddings", data=body,
                                  headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return resp["embedding"]

def extract_exchanges(session_id, messages):
    """Extract meaningful Q&A exchanges from a session."""
    exchanges = []
    current_q = None
    current_a = []

    for msg in messages:
        role = msg["role"]
        content = msg.get("content", "")

        # Skip tool calls, system messages
        if role == "system" or not content:
            continue
        # Truncate very long content
        if len(content) > 2000:
            content = content[:2000] + "..."

        if role == "user":
            # Save previous exchange
            if current_q and current_a:
                exchanges.append((current_q, " ".join(current_a)))
            current_q = content
            current_a = []
        elif role == "assistant" and current_q:
            current_a.append(content)

    # Don't forget last exchange
    if current_q and current_a:
        exchanges.append((current_q, " ".join(current_a)))

    return exchanges

def index_sessions():
    """Index recent session transcripts into the search DB."""
    if not os.path.exists(DB_PATH):
        print("No search DB found. Run memory_search.py --rebuild first.")
        return

    state = sqlite3.connect(STATE_DB)
    state.row_factory = sqlite3.Row
    search = sqlite3.connect(DB_PATH)

    # Get recent sessions with titles
    sessions = state.execute("""
        SELECT s.id, s.title, s.started_at, s.model
        FROM sessions s
        WHERE s.title IS NOT NULL AND s.title != ''
        ORDER BY s.started_at DESC
        LIMIT ?
    """, (MAX_SESSIONS,)).fetchall()

    print(f"Indexing {len(sessions)} recent sessions...")

    total_exchanges = 0
    errors = 0
    t0 = time.time()

    for sess in sessions:
        sid = sess["id"]
        title = sess["title"] or "Untitled"
        created = sess["started_at"] or time.time()
        model = sess["model"] or "unknown"

        # Get messages
        messages = state.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
            (sid,)
        ).fetchall()
        messages = [{"role": m["role"], "content": m["content"]} for m in messages]

        exchanges = extract_exchanges(sid, messages)

        for i, (q, a) in enumerate(exchanges):
            # Create a chunk from the exchange
            chunk = f"Q: {q}\nA: {a}"
            if len(chunk) > 3000:
                chunk = chunk[:3000]

            chunk_id = hashlib.md5(f"session:{sid}:{i}".encode()).hexdigest()
            file_path = f"sessions/{sid[:12]}/{title[:50]}"

            try:
                emb = get_embedding(chunk[:1024])  # embed first part
                emb_bytes = json.dumps(emb).encode()
                search.execute(
                    "INSERT OR REPLACE INTO chunks (id, file_path, chunk_text, embedding, mtime, indexed_at, is_noise) VALUES (?,?,?,?,?,?,?)",
                    (chunk_id, file_path, chunk, emb_bytes, created, time.time(), 0)
                )
                total_exchanges += 1
            except Exception as e:
                errors += 1
                print(f"  ERROR: {e}")

        if total_exchanges % 20 == 0:
            print(f"  ... {total_exchanges} exchanges indexed", flush=True)

    search.commit()
    search.close()
    state.close()

    elapsed = time.time() - t0
    print(f"Indexed {total_exchanges} exchanges from {len(sessions)} sessions in {elapsed:.1f}s ({errors} errors)")

if __name__ == "__main__":
    index_sessions()
