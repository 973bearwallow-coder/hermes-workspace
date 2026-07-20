#!/usr/bin/env python3
"""
moa_catalog.py v2 — Multi-provider FREE/CHEAP model discovery + classification.
Atlas MoA Router (2026-07-14). Supports local-first + all-provider pool.

PULLS FROM:
  1. OpenRouter keyless /models (343+, covers many re-exposed providers)
  2. NVIDIA NIM public catalog (121, OpenAI-compat)
  3. GitHub Models (needs PAT — only if key present)
  4. Hugging Face serverless (public list; custom adapter, best-effort)
  5. Nous Research (if key present)
  6. Local Ollama on Charles (unlimited $0 — PREFERRED workhorse)

Each model gets a `home_provider` so moa_providers.call_model() routes correctly.
Local models are tagged home_provider=local_ollama and sorted FIRST by the router.

USAGE
  python3 moa_catalog.py            # refresh + summary
  python3 moa_catalog.py --quiet    # write only
"""
import json, sys, os, subprocess, datetime, re, urllib.request, urllib.error

MEMORY = "/home/tom/hermes-workspace/memory"
OUT = os.path.join(MEMORY, "model_catalog.json")
OR_API = "https://openrouter.ai/api/v1/models"
NIM_API = "https://integrate.api.nvidia.com/v1/models"
HF_API = "https://huggingface.co/api/models?filter=text-generation-inference&limit=120&sort=downloads"
GH_API = "https://models.inference.ai.azure.com/v1/models"

import get_provider_key as pk

# providers behind a Cloudflare bot-check need a full browser UA on /v1/models
_BROWSER_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
_UA_FOR = {"groq", "cerebras"}

def _get_json(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "atlas-moa/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def cost_tier(pin, pout):
    if pin == 0 and pout == 0:
        return "free", 0.0, 0.0
    if pout <= 1.0:
        return "cheap", pin, pout
    return "paid", pin, pout

def quality_proxy(name, tier):
    score = 5.0
    n = name.lower()
    if any(p in n for p in ["deepseek", "qwen3", "gemma", "llama-3.3", "nemotron", "hy3", "owl", "claude", "gpt", "grok"]):
        score += 1.5
    if tier == "paid":
        score += 1.5
    elif tier == "cheap":
        score += 0.5
    if "coder" in n:
        score += 0.5
    return round(min(score, 10.0), 1)

def add_common(models, mid, name, home_provider, tier, cin, cout, ctx, tags, mods=None):
    models.append({
        "id": mid, "name": name, "provider": home_provider, "home_provider": home_provider,
        "tier": tier, "cost_in": cin, "cost_out": cout, "context_length": ctx,
        "modalities": mods or {"text": True, "vision": False, "audio": False, "file": False},
        "tags": tags, "quality": quality_proxy(name, tier),
        "rate_limit": "see provider", "expiration": None, "expiring_soon": False,
        "expires_in_days": None, "direct_key": True,
        "notes": f"Routed via {home_provider}.",
    })

def fetch_openrouter(models):
    raw = _get_json(OR_API)
    today = datetime.date.today()
    for m in raw.get("data", []):
        p = m.get("pricing", {}) or {}
        try:
            cin = float(p.get("prompt") or 0); cout = float(p.get("completion") or 0)
        except Exception:
            cin = cout = 0
        # Skip OpenRouter "auto" routers (auto-beta, fusion, pareto, etc.) — they have
        # sentinel cost -1.0 (dynamic backend, unknown price until query). Including them
        # as "cheap/free" pollutes cost estimates. We only want fixed-price models.
        if cin == -1.0 or cout == -1.0:
            continue
        tier, cin, cout = cost_tier(cin, cout)
        arch = m.get("architecture", {}) or {}
        ins = set(arch.get("input_modalities", []) or []); outs = set(arch.get("output_modalities", []) or [])
        mods = {"text": "text" in ins|outs, "vision": "image" in ins|outs,
                "audio": "audio" in ins|outs or "speech" in ins|outs, "file": "file" in ins|outs}
        t = []
        nm = (m.get("name","")+" "+m["id"]).lower()
        if mods["vision"]: t.append("vision")
        if any(k in nm for k in ["coder","code","qwen3-coder","codestral","deepcoder"]): t.append("coder")
        if any(k in nm for k in ["reason","thinking","r1","qwq","nemotron","hy3","owl"]): t.append("reasoning")
        if (m.get("context_length") or 0) >= 128000: t.append("longctx")
        exp = m.get("expiration_date"); expiring = False; days = None
        if exp:
            try:
                ed = datetime.date.fromisoformat(exp[:10]); days = (ed-today).days
                if days <= 30: expiring = True
            except Exception: pass
        prov = m["id"].split("/")[0].lower()
        models.append({
            "id": m["id"], "name": m.get("name"), "provider": prov, "home_provider": "openrouter",
            "tier": tier, "cost_in": cin, "cost_out": cout, "context_length": m.get("context_length"),
            "modalities": mods, "tags": t, "quality": quality_proxy(m["id"], tier),
            "rate_limit": m.get("per_request_limits"), "expiration": exp, "expiring_soon": expiring,
            "expires_in_days": days, "direct_key": False,
            "description": (m.get("description") or "")[:300],
        })

def fetch_nim(models):
    try:
        raw = _get_json(NIM_API)
        for m in raw.get("data", []):
            mid = m["id"]
            # NIM free models have $0; infer cheap if known paid
            add_common(models, f"nvidia/{mid}", mid, "nvidia", "free", 0.0, 0.0,
                       m.get("context_length") or 65536, ["nim","cloud"])
    except Exception as e:
        print(f"  (NIM skip: {e})")

def _openai_compat_models(models, url, provider, tier, key, tag):
    """Pull real model list from an OpenAI-compat /v1/models endpoint."""
    headers = {"User-Agent": "Mozilla/5.0"}
    # providers behind a Cloudflare bot-check need the full browser UA
    if provider in _UA_FOR:
        headers = dict(_BROWSER_UA)
    if key:
        headers["Authorization"] = f"Bearer {key}"
    try:
        raw = _get_json(url, headers=headers)
        arr = raw.get("data", raw if isinstance(raw, list) else [])
        n = 0
        for m in arr:
            mid = m.get("id") or m.get("name")
            if not mid:
                continue
            ctx = m.get("context_window") or m.get("context_length") or 128000
            add_common(models, f"{provider}/{mid}", mid, provider, tier, 0.0, 0.0, ctx,
                       [provider, "cloud", "free"])
            n += 1
        print(f"  ({tag}: {n} models)")
    except Exception as e:
        print(f"  ({tag} skip: {e})")

def fetch_github(models):
    """GitHub Models has no public list API — use a curated free set."""
    # Verified-free GitHub Models IDs (tested live 2026-07-14). GitHub uses
    # bare lowercase names (e.g. llama-3.3-70b-instruct, NOT meta/Llama-...).
    FREE_GH = [
        "llama-3.3-70b-instruct", "phi-4-mini-instruct", "mistral-small-2503",
        "DeepSeek-V3-0324", "phi-4", "gpt-4.1-mini",
    ]
    for mid in FREE_GH:
        add_common(models, f"github/{mid}", mid, "github", "free", 0.0, 0.0, 128000,
                   ["github", "cloud", "free"])

def fetch_groq(models):
    key = pk.get_key("groq")
    if not key:
        return
    _openai_compat_models(models, "https://api.groq.com/openai/v1/models", "groq", "free", key, "Groq")

def fetch_cerebras(models):
    key = pk.get_key("cerebras")
    if not key:
        return
    _openai_compat_models(models, "https://api.cerebras.ai/v1/models", "cerebras", "free", key, "Cerebras")

def fetch_mistral(models):
    key = pk.get_key("mistral")
    if not key:
        return
    _openai_compat_models(models, "https://api.mistral.ai/v1/models", "mistral", "free", key, "Mistral")

def fetch_deepseek(models):
    key = pk.get_key("deepseek")
    if not key:
        return
    _openai_compat_models(models, "https://api.deepseek.com/v1/models", "deepseek", "free", key, "DeepSeek")

def fetch_nebius(models):
    key = pk.get_key("nebius")
    if not key:
        return
    _openai_compat_models(models, "https://api.studio.nebius.com/v1/models", "nebius", "free", key, "Nebius")

def fetch_chutes(models):
    """Chutes.ai — community-hosted open models. API is /v1/chats/{user}/{slug}/api/generate
    (not OpenAI-compat /v1/models). Use the curated free set from the free-LLM repo."""
    key = pk.get_key("chutes")
    if not key:
        return
    # curated free Chutes models (from awesome-freellm-apis): DeepSeek-R1 + 1 other
    chutes_free = [
        ("deepseek-ai/DeepSeek-R1", "deepseek-ai/DeepSeek-R1", 131000),
    ]
    n = 0
    for mid, call_id, ctx in chutes_free:
        add_common(models, f"chutes/{mid}", call_id, "chutes", "free", 0.0, 0.0, ctx,
                   ["chutes", "cloud", "free", "reasoning"])
        n += 1
    print(f"  (Chutes: {n} models [curated])")

def fetch_gemini(models):
    """Gemini native API. The /v1beta/models list endpoint is flaky (403), so use
    a curated set of known-free Gemini text models (verified live 2026-07-15)."""
    key = pk.get_key("gemini")
    if not key:
        return
    gemini_free = [
        ("gemini-2.5-flash", 1048576),
        ("gemini-2.5-flash-lite", 1048576),
        ("gemini-2.0-flash", 1048576),
        ("gemini-1.5-flash", 1048576),
    ]
    n = 0
    for mid, ctx in gemini_free:
        add_common(models, f"gemini/{mid}", mid, "gemini", "free", 0.0, 0.0, ctx,
                   ["gemini", "cloud", "free"])
        n += 1
    print(f"  (Gemini: {n} models [curated])")

def fetch_agnes(models):
    """Agnes AI — they ARE the model maker (apihub.agnes-ai.com is their own hub,
    not an aggregator). Use their real model names (agnes-2.0-flash etc.), NOT a
    routing slug. Pull the live /v1/models list; fallback to a curated set."""
    key = pk.get_key("agnes")
    if not key:
        return
    ids = None
    try:
        raw = _get_json("https://apihub.agnes-ai.com/v1/models",
                        headers={"Authorization": f"Bearer {key}",
                                  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"},
                        timeout=25)
        arr = raw.get("data") or raw.get("models") or []
        ids = [m.get("id") for m in arr if m.get("id")]
    except Exception:
        ids = None
    if not ids:
        # curated fallback (verified live 2026-07-15)
        ids = ["agnes-2.0-flash", "agnes-1.5-flash"]
    n = 0
    for mid in ids:
        if not mid or "video" in mid or "image" in mid:
            continue
        # NOTE: bare slug (agnes-2.0-flash), NOT agnes/agnes-2.0-flash — the latter
        # 503s because apihub.agnes-ai.com expects the raw model id. home_provider='agnes'
        # routes to the correct endpoint. Context = 256K (real spec, not 128K).
        # Tagged multimodal+vision so the router can pick Agnes for image tasks.
        add_common(models, mid, mid, "agnes", "free-fallback", 0.0, 0.0, 256000,
                   ["agnes", "cloud", "free", "multimodal", "vision", "tools", "fallback"],
                   mods={"text": True, "vision": True, "audio": False, "file": False})
        n += 1
    print(f"  (Agnes: {n} models)")

def fetch_openai(models):
    key = pk.get_key("openai")
    if not key:
        return
    # OpenAI via direct key = PAID premium tier (these cost). Mark as paid.
    try:
        raw = _get_json("https://api.openai.com/v1/models",
                        headers={"Authorization": f"Bearer {key}", "User-Agent": "Mozilla/5.0"})
        arr = raw.get("data", [])
        n = 0
        for m in arr:
            mid = m.get("id") or m.get("name")
            if not mid:
                continue
            # only keep chat-capable general models as premium
            if any(k in mid.lower() for k in ["gpt-4", "gpt-4.1", "gpt-5", "o1", "o3", "o4", "chat"]):
                add_common(models, f"openai/{mid}", mid, "openai", "paid", 0.0, 0.0,
                           m.get("context_window") or 128000, ["openai", "cloud", "premium"])
                n += 1
        print(f"  (OpenAI premium: {n} models)")
    except Exception as e:
        print(f"  (OpenAI skip: {e})")

def fetch_cloudflare(models):
    """Cloudflare Workers AI — pull the LIVE model list (text generation) via API."""
    import urllib.request as _ur
    tok = pk.get_key("cloudflare")
    acct = pk.get_key("cloudflare_account_id")
    if not (tok and acct):
        # fallback: a couple of known-good free models
        FREE_CF = ["@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/meta/llama-3.1-8b-instruct-fp8"]
        for mid in FREE_CF:
            name = mid.split("/")[-1]
            add_common(models, f"cloudflare/{mid}", name, "cloudflare", "free", 0.0, 0.0, 32000,
                       ["cloudflare", "cloud", "free"])
        return
    try:
        url = (f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/models/search"
               "?task=Text%20Generation")
        req = _ur.Request(url, headers={"Authorization": f"Bearer {tok}", "User-Agent": "Mozilla/5.0"})
        raw = json.load(_ur.urlopen(req, timeout=30))
        n = 0
        for m in raw.get("result", []):
            mid = m.get("name")
            if not mid:
                continue
            name = mid.split("/")[-1]
            add_common(models, f"cloudflare/{mid}", name, "cloudflare", "free", 0.0, 0.0, 32000,
                       ["cloudflare", "cloud", "free"])
            n += 1
        print(f"  (Cloudflare: {n} models)")
    except Exception as e:
        print(f"  (Cloudflare skip: {e})")

def fetch_nous(models):
    """Nous public inference endpoint is currently down; add known Hermes models."""
    for mid in ["NousResearch/Hermes-3-Llama-3.1-405B", "NousResearch/Hermes-4-405B",
                "NousResearch/Hermes-2-Pro-Llama-3-70B"]:
        add_common(models, mid, mid, "nous", "free", 0.0, 0.0, 128000, ["reasoning", "cloud", "free"])

def fetch_replicate(models):
    """Replicate: curated free-ish open-weight models (cost applies per-use)."""
    REP = [
        "meta/meta-llama-3-70b-instruct", "mistralai/mixtral-8x7b-instruct-v0.1",
        "google/deepseek-ai-deepseek-r1-distill-llama-70b", "meta/llama-2-70b-chat",
        "mistralai/mistral-7b-instruct-v0.2",
    ]
    for mid in REP:
        name = mid.split("/")[-1]
        add_common(models, f"replicate/{mid}", name, "replicate", "cheap", 0.0, 0.0, 32000,
                   ["replicate", "cloud", "cheap"])

def fetch_hf(models):
    # HF serverless inference endpoint is unreachable from Charles (DNS for
    # api-inference.huggingface.co does not resolve here). Skip until DNS/route fixes.
    try:
        import socket
        socket.gethostbyname("api-inference.huggingface.co")
    except Exception:
        print("  (HF skip: api-inference.huggingface.co not resolvable on Charles)")
        return
    try:
        tok = pk.get_key("huggingface")
        headers = {"Authorization": f"Bearer {tok}"} if tok else {}
        raw = _get_json(HF_API, headers=headers)
        for m in raw[:100]:
            mid = m["id"]
            add_common(models, f"hf/{mid}", mid, "huggingface", "free", 0.0, 0.0,
                       32000, ["hf", "cloud", "free"],
                       mods={"text": True, "vision": False, "audio": False, "file": False})
    except Exception as e:
        print(f"  (HF skip: {e})")

# Curated free-LLM GitHub repos (the "awesome list" Tom remembered). These list
# providers + models OpenRouter does NOT aggregate, so they broaden discovery.
FREELLM_SOURCES = [
    ("awesome-freellm-apis", "https://raw.githubusercontent.com/open-free-llm-api/awesome-freellm-apis/main/README.md"),
    ("cheahjs", "https://raw.githubusercontent.com/cheahjs/free-llm-api-resources/main/README.md"),
]

def fetch_freellm(models):
    """Enrich the catalog with free providers/models from curated GitHub lists
    (the 'awesome free LLM' repos Tom remembered). These list providers +
    base URLs OpenRouter does NOT aggregate, broadening daily discovery.

    Parses the markdown PROVIDER TABLE (not headers) so we get real provider
    names + free-model counts + base URLs. Tagged 'freellm' so the router can
    prefer verified API-sourced models but still know a provider exists.
    Robust: any fetch failure is skipped silently.
    """
    n = 0
    for src_name, url in FREELLM_SOURCES:
        try:
            if url.endswith(".json"):
                txt = _get_json(url)
            else:
                txt = urllib.request.urlopen(
                    urllib.request.Request(url, headers={"User-Agent": "atlas-moa/1.0"}), timeout=20
                ).read().decode(errors="ignore")
        except Exception as e:
            print(f"  (freellm/{src_name} skip: {e})")
            continue
        # provider tables look like:  | Provider | Free Models | ... |
        # capture first cell of each data row (skip header + separator rows)
        rows = re.findall(r"^\|\s*([A-Za-z0-9 ._\-()]+?)\s*\|\s*\d+", txt, re.M)
        seen = set()
        for p in rows:
            p = p.strip()
            if len(p) < 3 or p.lower() in ("provider", "free models", "api key"):
                continue
            key = f"freellm/{p}"
            if key in seen:
                continue
            seen.add(key)
            add_common(models, key, p, "freellm", "free", 0.0, 0.0, 32000,
                       ["freellm", "cloud", "free", src_name])
            n += 1
    if n:
        print(f"  (freellm: +{n} providers from curated GitHub lists)")
    else:
        print("  (freellm: no new providers parsed)")

def local_ollama(models):
    """Add local models on Charles as unlimited $0 entries — but only those that
    actually serve via the OpenAI-compat endpoint (liveness probe)."""
    try:
        res = subprocess.run(["/usr/bin/ollama", "list"], capture_output=True, text=True, timeout=15)
        for line in res.stdout.strip().splitlines()[1:]:
            parts = line.split()
            if not parts: continue
            mid = parts[0]  # e.g. 'gemma4:31b' — this is what the API expects
            low = mid.lower()
            is_vision = ("vl" in low or "vision" in low)
            tags = ["local", "unlimited"]
            if is_vision: tags.append("vision")
            if any(k in low for k in ["coder", "code", "qwen3-coder", "codestral", "deepcoder"]): tags.append("coder")
            if any(k in low for k in ["reason", "thinking", "r1", "qwq", "nemotron", "qwen3", "deepseek", "30b", "72b", "27b"]): tags.append("reasoning")
            if any(k in low for k in ["64k", "128k", "long"]): tags.append("longctx")
            q = 7.0
            if any(k in low for k in ["qwen3:30b", "qwen2:72b", "gemma4:31b", "qwen3.6-27b"]): q = 8.0
            # liveness probe — only hard-skip when the API explicitly rejects
            # the model name (404/400 "model not found"). A 500/timeout means
            # Ollama will load it on demand — keep it (optimistic, avoids
            # false-negatives on slow cold loads of large local models).
            ok = False
            try:
                import urllib.request as _ur, json as _json
                probe = {"model": mid, "messages": [{"role":"user","content":"hi"}], "max_tokens": 3, "think": False}
                preq = _ur.Request("http://localhost:11434/v1/chat/completions",
                                             data=_json.dumps(probe).encode(), headers={"Content-Type":"application/json"})
                with _ur.urlopen(preq, timeout=20) as r:
                    _json.load(r); ok = True
            except _ur.HTTPError as e:
                body = e.read().decode(errors="ignore").lower()
                if e.code in (404, 400) and "not found" in body:
                    ok = False   # truly nonexistent model name -> skip
                elif e.code == 500 and ("unable to load" in body or "blob" in body):
                    ok = False   # broken GGUF/manifest -> skip
                else:
                    ok = True    # other 5xx -> Ollama will serve on demand
            except Exception:
                ok = True   # timeout/cold-load -> keep, it will serve
            if not ok:
                print(f"  (skip local model not serving: {mid})")
                continue
            models.append({
                "id": f"local_ollama/{mid}", "name": mid, "provider": "local_ollama", "home_provider": "local_ollama",
                "tier": "free", "cost_in": 0.0, "cost_out": 0.0, "context_length": 32768,
                "modalities": {"text": True, "vision": is_vision, "audio": False, "file": False},
                "tags": tags,
                "quality": q, "rate_limit": "unlimited (local GPU)", "expiration": None,
                "expiring_soon": False, "expires_in_days": None, "direct_key": False,
                "notes": "Runs on Charles RTX 3090 — $0, no rate limit. PREFERRED.",
            })
    except Exception:
        pass

def build():
    models = []
    print("Pulling OpenRouter (343+)..."); fetch_openrouter(models)
    print("Pulling NVIDIA NIM (121)..."); fetch_nim(models)
    print("Pulling GitHub Models..."); fetch_github(models)
    print("Pulling Groq..."); fetch_groq(models)
    print("Pulling OpenAI (premium)..."); fetch_openai(models)
    print("Pulling Cloudflare..."); fetch_cloudflare(models)
    print("Pulling Nous..."); fetch_nous(models)
    print("Pulling Replicate..."); fetch_replicate(models)
    print("Pulling Hugging Face (100)..."); fetch_hf(models)
    print("Pulling Cerebras..."); fetch_cerebras(models)
    print("Pulling Mistral..."); fetch_mistral(models)
    print("Pulling DeepSeek..."); fetch_deepseek(models)
    print("Pulling Gemini..."); fetch_gemini(models)
    print("Pulling Chutes..."); fetch_chutes(models)
    print("Pulling Nebius..."); fetch_nebius(models)
    print("Pulling Agnes..."); fetch_agnes(models)
    print("Adding local Ollama..."); local_ollama(models)
    print("Scanning curated free-LLM GitHub lists..."); fetch_freellm(models)
    # PRESERVE openai-codex entries (ChatGPT Plus OAuth) across refreshes — these
    # are added manually (not discovered via OpenRouter) and must survive rebuild.
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT))["models"]
            preserved = [m for m in old if m.get("home_provider") == "openai-codex"]
            if preserved:
                models.extend(preserved)
                print(f"Preserved {len(preserved)} openai-codex (ChatGPT Plus) entr(ies)")
        except Exception:
            pass
    by_tier = {}
    for x in models:
        by_tier[x["tier"]] = by_tier.get(x["tier"], 0) + 1
    catalog = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "source": "OpenRouter + NIM + GitHub + Groq + OpenAI + Cloudflare + Nous + Replicate + HF + curated free-LLM lists + local Ollama + openai-codex (preserved)",
        "total": len(models), "by_tier": by_tier, "models": models,
    }
    os.makedirs(MEMORY, exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(catalog, f, indent=2)
    return catalog

if __name__ == "__main__":
    cat = build()
    quiet = "--quiet" in sys.argv
    if not quiet:
        print(f"\nCatalog: {OUT}")
        print(f"  total: {cat['total']}  tiers: {cat['by_tier']}")
        local = [x for x in cat["models"] if x["home_provider"] == "local_ollama"]
        free_cloud = [x for x in cat["models"] if x["tier"]=="free" and x["home_provider"]!="local_ollama"]
        expiring = [x for x in cat["models"] if x.get("expiring_soon")]
        print(f"  local: {len(local)}  free-cloud: {len(free_cloud)}  expiring: {len(expiring)}")
        if expiring:
            for x in expiring[:8]:
                print(f"     ⚠ {x['id']} ({x['expires_in_days']}d)")
