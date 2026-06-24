#!/usr/bin/env python3
"""
Atlas Unified Memory Search
Combines three memory layers into ONE search:
  1. SEMANTIC (vault + session chunks, via embedding cosine similarity)
  2. KEYWORD (vault files, via BM25-like token overlap)
  3. SESSION FTS5 (exact phrase match in conversation transcripts)

Usage:
  python3 atlas_unified_search.py "query"           # all layers combined
  python3 atlas_unified_search.py "query" --top 10   # more results
  python3 atlas_unified_search.py --rebuild          # rebuild vault+session index
  python3 atlas_unified_search.py --stats            # combined stats
"""

import sys, os, json, hashlib, re, time, urllib.request, sqlite3

# ── Config ──────────────────────────────────────────────────────────────────
HOME = "/home/tom"
VAULT_DIRS = [
    f"{HOME}/hermes-workspace/memory",
    f"{HOME}/Documents/ObsidianVault",
]
SEARCH_DB = f"{HOME}/hermes-workspace/memory/.search_index.db"
STATE_DB = f"{HOME}/.hermes/state.db"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

SKIP_DIRS = {'.obsidian', '.git', '__pycache__', 'node_modules', '.venv', 'venv'}
SKIP_FILES = {'QUICK_REFERENCE.md'}
DAILY_NOISE_THRESHOLD = 7 * 86400
RECENCY_HALF_LIFE = 30 * 86400

# Layer weights for final combined score
W_SEMANTIC = 0.35
W_KEYWORD  = 0.25
W_FTS5     = 0.40  # exact matches get highest weight

# ── Helpers ─────────────────────────────────────────────────────────────────
def tokenize(text):
    return [w for w in re.split(r'[^a-z0-9]+', text.lower()) if len(w) > 2]

def cosine_similarity(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    ma = sum(x*x for x in a)**0.5
    mb = sum(x*x for x in b)**0.5
    return dot/(ma*mb) if ma and mb else 0.0

def keyword_score(q_tokens, text_tokens):
    if not q_tokens: return 0.0
    ts = set(text_tokens)
    return sum(1 for t in q_tokens if t in ts) / len(q_tokens)

def recency_boost(mtime):
    age = time.time() - mtime
    return 2 ** (-age / RECENCY_HALF_LIFE)

def get_embedding(text):
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:2048]}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/embeddings", data=body,
                                  headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())["embedding"]

def chunk_text(text, size=400, overlap=80):
    sections = re.split(r'\n(?=#{1,3} |\n---|\n[-*] |\n\d+\. )', text)
    chunks, cur = [], ""
    for s in sections:
        s = s.strip()
        if not s: continue
        if len(cur) + len(s) < size:
            cur += "\n" + s
        else:
            if cur.strip(): chunks.append(cur.strip())
            cur = s
    if cur.strip(): chunks.append(cur.strip())
    if not chunks and text.strip(): chunks = [text.strip()]
    return chunks

# ── Rebuild ─────────────────────────────────────────────────────────────────
def scan_vault():
    files = []
    for vault_dir in VAULT_DIRS:
        for root, dirs, fnames in os.walk(vault_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in fnames:
                if not fn.endswith('.md') or fn in SKIP_FILES: continue
                p = os.path.join(root, fn)
                try:
                    st = os.stat(p)
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    if content.strip():
                        files.append((p, content, st.st_mtime))
                except: pass
    return files

def rebuild_index():
    print("Building unified search index...")
    files = scan_vault()
    print(f"  Vault: {len(files)} files")

    if os.path.exists(SEARCH_DB):
        os.remove(SEARCH_DB)

    conn = sqlite3.connect(SEARCH_DB)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""CREATE TABLE chunks (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,   -- 'vault' or 'session'
        file_path TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        embedding BLOB NOT NULL,
        mtime REAL NOT NULL,
        is_noise INTEGER DEFAULT 0
    )""")
    conn.execute("CREATE INDEX idx_source ON chunks(source)")

    total, errors = 0, 0

    # Index vault
    for fp, content, mtime in files:
        # Determine which vault dir this file belongs to for relative path
        vault_base = VAULT_DIRS[0]
        for vd in VAULT_DIRS:
            if fp.startswith(vd):
                vault_base = vd
                break
        rel = os.path.relpath(fp, vault_base)
        noise = 1 if (re.match(r'Daily/\d{4}-\d{2}-\d{2}\.md', rel) and time.time()-mtime > DAILY_NOISE_THRESHOLD) else 0
        for i, chunk in enumerate(chunk_text(content)):
            cid = hashlib.md5(f"v:{rel}:{i}:{chunk[:60]}".encode()).hexdigest()
            try:
                emb = json.dumps(get_embedding(chunk)).encode()
                conn.execute("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?,?,?)",
                    (cid, "vault", rel, chunk, emb, mtime, noise))
                total += 1
            except Exception as e:
                errors += 1

    # Index sessions (last 15 to keep rebuild fast)
    if os.path.exists(STATE_DB):
        try:
            state = sqlite3.connect(STATE_DB)
            state.row_factory = sqlite3.Row
            sessions = state.execute(
                "SELECT s.id, s.title, s.started_at FROM sessions s WHERE s.title IS NOT NULL ORDER BY s.started_at DESC LIMIT 15"
            ).fetchall()
            print(f"  Sessions: {len(sessions)}")
            sess_count = 0

            for sess in sessions:
                sid = sess["id"]
                title = sess["title"] or "Untitled"
                started = sess["started_at"] or time.time()
                msgs = state.execute("SELECT role, content FROM messages WHERE session_id=? ORDER BY id", (sid,))
                exchange, q_buf, a_buf = [], None, []
                for m in msgs:
                    role = m["role"]
                    content = (m["content"] or "").strip()
                    if not content or role == "system": continue
                    if len(content) > 2000: content = content[:2000] + "..."
                    if role == "user":
                        if q_buf and a_buf:
                            exchange.append((q_buf, " ".join(a_buf)))
                        q_buf, a_buf = content, []
                    elif role == "assistant" and q_buf is not None:
                        a_buf.append(content)
                if q_buf and a_buf:
                    exchange.append((q_buf, " ".join(a_buf)))

                for i, (q, a) in enumerate(exchange):
                    chunk = f"Q: {q}\nA: {a}"
                    if len(chunk) > 3000: chunk = chunk[:3000]
                    cid = hashlib.md5(f"s:{sid}:{i}:{chunk[:60]}".encode()).hexdigest()
                    fp2 = f"sessions/{sid[:12]}/{title[:50]}"
                    try:
                        emb = json.dumps(get_embedding(chunk[:1024])).encode()
                        conn.execute("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?,?,?)",
                            (cid, "session", fp2, chunk, emb, started, 0))
                        total += 1
                        sess_count += 1
                    except Exception as e:
                        errors += 1
            state.close()
            print(f"  Session chunks indexed: {sess_count}")
        except Exception as e:
            print(f"  Session indexing error: {e}")

    conn.commit()
    conn.close()
    print(f"  Total indexed: {total} chunks ({errors} errors)")
    return total

# ── FTS5 session search ─────────────────────────────────────────────────────
def search_fts5(query, top_k=5):
    """Exact phrase/conversation search via FTS5."""
    if not os.path.exists(STATE_DB):
        return []
    try:
        state = sqlite3.connect(STATE_DB)
        # Search messages FTS
        rows = state.execute("""
            SELECT s.title, m.content, m.session_id, rank
            FROM messages_fts fts
            JOIN messages m ON m.id = fts.rowid
            JOIN sessions s ON s.id = m.session_id
            WHERE messages_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, top_k)).fetchall()
        state.close()
        results = []
        for title, content, sid, rank in rows:
            # Normalize rank (lower is better in FTS5) to 0-1 score
            score = 1.0 / (1.0 + abs(rank)) if rank else 0.5
            preview = content[:400].replace('\n',' ').strip() if content else ""
            results.append((score, f"sessions/{sid[:18]}/{title[:50]}", preview, "fts5"))
        return results
    except Exception as e:
        return []

# ── Vault semantic+keyword search ───────────────────────────────────────────
def search_vault_layers(query, q_emb, q_tokens, top_k=10):
    """Search vault DB with semantic + keyword scoring."""
    if not os.path.exists(SEARCH_DB):
        return []
    conn = sqlite3.connect(SEARCH_DB)
    rows = conn.execute("SELECT source, file_path, chunk_text, embedding, mtime, is_noise FROM chunks").fetchall()
    conn.close()

    results = []
    seen_paths = {}

    for source, fp, chunk, emb_bytes, mtime, is_noise in rows:
        emb = json.loads(emb_bytes.decode())
        toks = tokenize(chunk)

        sem = cosine_similarity(q_emb, emb)
        kw = keyword_score(q_tokens, toks)

        score = W_SEMANTIC * sem + W_KEYWORD * kw
        score *= (1.0 + recency_boost(mtime))
        if is_noise: score *= 0.3

        key = f"{source}:{fp}"
        if key not in seen_paths or score > seen_paths[key]:
            seen_paths[key] = score
            results.append((score, fp, chunk[:350], source))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:top_k]

# ── Unified search ──────────────────────────────────────────────────────────
def unified_search(query, top_k=8):
    q_emb = get_embedding(query)
    q_tokens = tokenize(query)

    # Layer 1+2: Vault semantic + keyword
    vault_results = search_vault_layers(query, q_emb, q_tokens, top_k=top_k)

    # Layer 3: FTS5 exact match
    fts_results = search_fts5(query, top_k=3)
    # Re-weight FTS5 results
    fts_weighted = [(s * W_FTS5 / max(W_SEMANTIC, W_KEYWORD), fp, preview, "fts5")
                    for s, fp, preview, _ in fts_results]

    # Merge: vault first, then FTS5 results appended
    combined = vault_results + fts_weighted
    combined.sort(key=lambda x: x[0], reverse=True)

    # Deduplicate by path
    seen, final = set(), []
    for score, fp, preview, src in combined:
        key = f"{src}:{fp}"
        if key not in seen:
            seen.add(key)
            final.append((score, fp, preview, src))
        if len(final) >= top_k:
            break
    return final

# ── Stats ───────────────────────────────────────────────────────────────────
def show_stats():
    print("=== Atlas Unified Memory Search ===\n")
    if os.path.exists(SEARCH_DB):
        conn = sqlite3.connect(SEARCH_DB)
        total = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        vault = conn.execute("SELECT COUNT(*) FROM chunks WHERE source='vault'").fetchone()[0]
        sessions = conn.execute("SELECT COUNT(*) FROM chunks WHERE source='session'").fetchone()[0]
        files = conn.execute("SELECT COUNT(DISTINCT file_path) FROM chunks").fetchone()[0]
        sz = os.path.getsize(SEARCH_DB)
        conn.close()
        print(f"  Semantic+Keyword Index:")
        print(f"    Chunks:   {total} (vault: {vault}, sessions: {sessions})")
        print(f"    Files:    {files}")
        print(f"    Size:     {sz/1024/1024:.1f} MB")
    if os.path.exists(STATE_DB):
        state = sqlite3.connect(STATE_DB)
        msgs = state.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        sess = state.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        state.close()
        print(f"  FTS5 Index:")
        print(f"    Messages: {msgs}")
        print(f"    Sessions: {sess}")
    print(f"  Weights: semantic={W_SEMANTIC}, keyword={W_KEYWORD}, fts5={W_FTS5}")

# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    if "--stats" in args:
        show_stats()
        sys.exit(0)

    do_rebuild = "--rebuild" in args
    if do_rebuild:
        args.remove("--rebuild")

    top_k = 8
    if "--top" in args:
        idx = args.index("--top")
        top_k = int(args[idx+1])
        args = args[:idx] + args[idx+2:]

    query = " ".join(args) if args else None

    if do_rebuild:
        rebuild_index()

    if not query:
        print("Provide a query or --rebuild.")
        sys.exit(1)

    results = unified_search(query, top_k=top_k)
    if not results:
        print(f"No results for: \"{query}\"")
    else:
        print(f"\n🔍 Atlas Unified Search: \"{query}\" ({len(results)} results)\n")
        for i, (score, fp, preview, src) in enumerate(results, 1):
            src_label = {"vault": "📁 VAULT", "session": "💬 SESSION", "fts5": "⚡ FTS5"}.get(src, src)
            print(f"── {i}. {src_label} | {fp} (score: {score:.3f}) ──")
            print(f"   {str(preview)[:300]}")
            print()
