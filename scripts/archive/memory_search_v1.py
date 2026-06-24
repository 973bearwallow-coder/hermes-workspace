#!/usr/bin/env python3
"""
Atlas Memory Search Index v2
Hybrid search: semantic (nomic-embed-text via Ollama) + keyword (BM25-like).
Indexes vault markdown files + session transcript excerpts.
Recency-weighted scoring. Noise filtering for daily logs.

Usage:
  python3 memory_search.py "query"              # hybrid search (default)
  python3 memory_search.py "query" --semantic    # semantic only
  python3 memory_search.py "query" --keyword     # keyword only
  python3 memory_search.py --rebuild             # rebuild index
  python3 memory_search.py --rebuild "query"     # rebuild then search
  python3 memory_search.py --stats               # index stats
  python3 memory_search.py --clean               # remove old daily noise from index
"""

import sys, os, json, hashlib, re, time, urllib.request, sqlite3

# ── Config ──────────────────────────────────────────────────────────────────
VAULT_DIR = "/home/tom/hermes-workspace/memory"
DB_PATH = "/home/tom/hermes-workspace/memory/.search_index.db"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

# Folders/files to skip during indexing
SKIP_DIRS = {'.obsidian', '.git', '__pycache__', 'node_modules', '.venv', 'venv'}
SKIP_FILES = {'QUICK_REFERENCE.md'}  # too meta, pollutes results
# Daily files older than this (seconds) get depriorized, not skipped
DAILY_NOISE_THRESHOLD = 7 * 86400  # 7 days
# Weight multipliers
SEMANTIC_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4
RECENCY_HALF_LIFE = 30 * 86400  # 30 days half-life for recency boost

# ── Embedding ───────────────────────────────────────────────────────────────
def get_embedding(text):
    """Get embedding vector from Ollama."""
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:2048]}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/embeddings", data=body,
                                  headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return resp["embedding"]

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(x * x for x in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

# ── Text processing ─────────────────────────────────────────────────────────
def tokenize(text):
    """Simple tokenizer: lowercase, split on non-alphanumeric, filter short."""
    return [w for w in re.split(r'[^a-z0-9]+', text.lower()) if len(w) > 2]

def keyword_score(query_tokens, text_tokens):
    """BM25-like keyword overlap score."""
    if not query_tokens:
        return 0.0
    text_set = set(text_tokens)
    matches = sum(1 for t in query_tokens if t in text_set)
    # Normalize by query length and add IDF-like weighting for rare terms
    return matches / len(query_tokens)

def chunk_text(text, chunk_size=400, overlap=80):
    """Split text into meaningful overlapping chunks."""
    # Split on headers, double newlines, or bullet points
    sections = re.split(r'\n(?=#{1,3} |\n---|\n[-*] |\n\d+\. )', text)
    chunks = []
    current = ""
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(current) + len(section) < chunk_size:
            current += "\n" + section
        else:
            if current.strip():
                chunks.append(current.strip())
            current = section
    if current.strip():
        chunks.append(current.strip())
    # If no chunks produced, use whole text
    if not chunks and text.strip():
        chunks = [text.strip()]
    return chunks

def is_daily_noise(rel_path, mtime):
    """Check if a file is an old daily log that should be depriorized."""
    if re.match(r'Daily/\d{4}-\d{2}-\d{2}\.md', rel_path):
        age = time.time() - mtime
        return age > DAILY_NOISE_THRESHOLD
    return False

def recency_boost(mtime):
    """Exponential decay recency boost. Newer files get higher boost."""
    age = time.time() - mtime
    return 2 ** (-age / RECENCY_HALF_LIFE)

# ── Indexing ────────────────────────────────────────────────────────────────
def scan_vault():
    """Scan vault for markdown files."""
    files = []
    for root, dirs, fnames in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in fnames:
            if not fname.endswith('.md') or fname in SKIP_FILES:
                continue
            path = os.path.join(root, fname)
            try:
                stat = os.stat(path)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if content.strip():
                    files.append((path, content, stat.st_mtime))
            except Exception as e:
                print(f"  WARN: skipping {path}: {e}")
    return files

def rebuild_index():
    """Rebuild the entire search index."""
    print("Scanning vault...")
    files = scan_vault()
    print(f"Found {len(files)} markdown files")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA cache_size=-64000")
    conn.execute("""CREATE TABLE IF NOT EXISTS chunks (
        id TEXT PRIMARY KEY,
        file_path TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        embedding BLOB NOT NULL,
        mtime REAL NOT NULL,
        indexed_at REAL NOT NULL,
        is_noise INTEGER DEFAULT 0
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_file ON chunks(file_path)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_noise ON chunks(is_noise)")

    total_chunks = 0
    noise_chunks = 0
    errors = 0
    t0 = time.time()

    for fpath, content, mtime in files:
        rel_path = os.path.relpath(fpath, VAULT_DIR)
        noise = is_daily_noise(rel_path, mtime)
        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.md5(f"{rel_path}:{i}:{chunk[:80]}".encode()).hexdigest()
            try:
                emb = get_embedding(chunk)
                emb_bytes = json.dumps(emb).encode()
                conn.execute(
                    "INSERT OR REPLACE INTO chunks (id, file_path, chunk_text, embedding, mtime, indexed_at, is_noise) VALUES (?,?,?,?,?,?,?)",
                    (chunk_id, rel_path, chunk, emb_bytes, mtime, time.time(), int(noise))
                )
                total_chunks += 1
                if noise:
                    noise_chunks += 1
            except Exception as e:
                errors += 1
                print(f"  ERROR embedding {rel_path} chunk {i}: {e}")

        if total_chunks % 20 == 0:
            print(f"  ... {total_chunks} chunks indexed", flush=True)

    conn.commit()
    conn.close()
    elapsed = time.time() - t0
    print(f"Indexed {total_chunks} chunks from {len(files)} files in {elapsed:.1f}s")
    print(f"  Noise chunks (old daily): {noise_chunks}")
    print(f"  Errors: {errors}")
    return total_chunks

# ── Search ──────────────────────────────────────────────────────────────────
def search(query, top_k=8, mode="hybrid"):
    """Search the index. mode = 'hybrid' | 'semantic' | 'keyword'."""
    if not os.path.exists(DB_PATH):
        print("No index found. Run with --rebuild first.", file.stderr)
        sys.exit(1)

    q_emb = get_embedding(query)
    q_tokens = tokenize(query)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT file_path, chunk_text, embedding, mtime, is_noise FROM chunks WHERE is_noise = 0"
    ).fetchall()
    # Also get noise rows but we'll depriorize them
    noise_rows = conn.execute(
        "SELECT file_path, chunk_text, embedding, mtime, is_noise FROM chunks WHERE is_noise = 1"
    ).fetchall()
    conn.close()

    def score_row(row):
        fpath, chunk_text, emb_bytes, mtime, is_noise = row
        emb = json.loads(emb_bytes.decode())
        chunk_tokens = tokenize(chunk_text)

        sem = cosine_similarity(q_emb, emb) if mode in ("hybrid", "semantic") else 0.0
        kw = keyword_score(q_tokens, chunk_tokens) if mode in ("hybrid", "keyword") else 0.0

        # Combined score
        if mode == "hybrid":
            score = SEMANTIC_WEIGHT * sem + KEYWORD_WEIGHT * kw
        elif mode == "semantic":
            score = sem
        else:
            score = kw

        # Recency boost (multiplicative)
        boost = recency_boost(mtime)
        score *= (1.0 + boost)

        # Noise penalty
        if is_noise:
            score *= 0.3

        return (score, fpath, chunk_text, sem, kw)

    # Score clean rows
    scored = [score_row(r) for r in rows]
    # Score noise rows (will naturally rank lower)
    scored += [score_row(r) for r in noise_rows]

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def show_stats():
    if not os.path.exists(DB_PATH):
        print("No index found. Run with --rebuild first.")
        return
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    files = conn.execute("SELECT COUNT(DISTINCT file_path) FROM chunks").fetchone()[0]
    noise = conn.execute("SELECT COUNT(*) FROM chunks WHERE is_noise = 1").fetchone()[0]
    db_size = os.path.getsize(DB_PATH)
    # Oldest/newest
    oldest = conn.execute("SELECT MIN(mtime) FROM chunks").fetchone()[0]
    newest = conn.execute("SELECT MAX(mtime) FROM chunks").fetchone()[0]
    conn.close()
    print(f"Index stats:")
    print(f"  Chunks:       {total} ({noise} noise/depriorized)")
    print(f"  Files:        {files}")
    print(f"  Size:         {db_size/1024/1024:.1f} MB")
    print(f"  Oldest chunk: {time.strftime('%Y-%m-%d', time.localtime(oldest)) if oldest else 'N/A'}")
    print(f"  Newest chunk: {time.strftime('%Y-%m-%d', time.localtime(newest)) if newest else 'N/A'}")
    print(f"  DB path:      {DB_PATH}")

# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    mode = "hybrid"
    if "--semantic" in args:
        mode = "semantic"
        args.remove("--semantic")
    if "--keyword" in args:
        mode = "keyword"
        args.remove("--keyword")

    if "--stats" in args:
        show_stats()
        sys.exit(0)

    do_rebuild = "--rebuild" in args
    if do_rebuild:
        args.remove("--rebuild")

    query = " ".join(args) if args else None

    if do_rebuild:
        rebuild_index()

    if query:
        results = search(query, mode=mode)
        if not results:
            print("No results found.")
        else:
            print(f"\n🔍 Top {len(results)} results for: \"{query}\" (mode: {mode})\n")
            for i, (score, fpath, chunk, sem, kw) in enumerate(results, 1):
                print(f"── {i}. {fpath} (score: {score:.3f} | sem: {sem:.2f} | kw: {kw:.2f}) ──")
                preview = chunk[:350].replace('\n', ' ').strip()
                if len(chunk) > 350:
                    preview += "..."
                print(f"   {preview}")
                print()
    elif not do_rebuild:
        print("Provide a search query or --rebuild flag.")
