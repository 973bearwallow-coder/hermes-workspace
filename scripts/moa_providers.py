#!/usr/bin/env python3
"""
moa_providers.py — Unified model caller for Atlas MoA Router.
Routes a chat call to the correct provider endpoint based on the catalog
model entry's `home_provider` / `api_style`. Local-first by design.

Providers supported:
  local_ollama  -> http://localhost:11434/v1          (OpenAI-compat, no key)
  openrouter    -> https://openrouter.ai/api/v1        (OpenAI-compat, key)
  github        -> https://models.inference.ai.azure.com/v1 (OpenAI-compat, PAT)
  nvidia        -> https://integrate.api.nvidia.com/v1 (OpenAI-compat, key)
  nous          -> https://api.nousresearch.com/v1     (OpenAI-compat, key)
  groq          -> https://api.groq.com/openai/v1      (OpenAI-compat, key)
  mistral       -> https://api.mistral.ai/v1           (OpenAI-compat, key)
  openai        -> https://api.openai.com/v1           (OpenAI-compat, key) [PREMIUM]
  huggingface   -> https://api-inference.huggingface.co/models/{id} (custom, token)
  anthropic     -> https://api.anthropic.com/v1/messages (native, key) [PREMIUM]
  replicate     -> https://api.replicate.com/v1/models/{owner}/{name}/predictions (native, token)

All keys read via get_provider_key (never printed).
"""
import json, time, urllib.request, urllib.error
import get_provider_key as pk

OPENAI_COMPAT = {
    "local_ollama": "http://localhost:11434/v1/chat/completions",
    "openrouter":   "https://openrouter.ai/api/v1/chat/completions",
    "github":       "https://models.inference.ai.azure.com/v1/chat/completions",
    "nvidia":       "https://integrate.api.nvidia.com/v1/chat/completions",
    "nous":         "https://nousresearch.com/v1/chat/completions",
    "groq":         "https://api.groq.com/openai/v1/chat/completions",
    "mistral":      "https://api.mistral.ai/v1/chat/completions",
    "openai":       "https://api.openai.com/v1/chat/completions",
    "cloudflare":   "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/chat/completions",
    "agnes":       "https://apihub.agnes-ai.com/v1/chat/completions",
    "cerebras":     "https://api.cerebras.ai/v1/chat/completions",
    "deepseek":     "https://api.deepseek.com/v1/chat/completions",
    "nebius":       "https://api.studio.nebius.com/v1/chat/completions",
    "chutes":       "https://api.chutes.ai/v1/chats",  # base; _chutes_call builds full path
}
PREMIUM = {"anthropic", "openai"}

# Groq blocks the default Python UA at the Cloudflare layer (HTTP 403/1010).
# A browser UA passes. OpenAI-compat providers that are picky get this UA.
_BROWSER_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
_UA_FOR = {"groq", "cerebras", "deepseek", "nebius"}  # providers that need the browser UA

def _get_key(provider):
    """Key from secrets; falls back to Hermes config.yaml for groq."""
    k = pk.get_key(provider)
    if k:
        return k
    if provider == "groq":
        import re
        try:
            cfg = open("/home/tom/.hermes/config.yaml").read()
            m = re.search(r"groq:\s*\n\s*api_key:\s*(\S+)", cfg)
            if m:
                return m.group(1)
        except Exception:
            pass
    return ""

def _post(url, body, headers, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def _openai_call(url, key, provider, model_id, prompt, sys_prompt, max_tokens, timeout=120):
    body = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
    }
    # Local Ollama Qwen3 is a reasoning model that leaves `content` empty and
    # only fills `reasoning`. For normal chat/voice use we want the answer in
    # `content`, so disable thinking for local qwen3 (cloud reasoning models like
    # hy3 keep thinking on — the MoA aggregator benefits from it).
    if provider == "local_ollama" and "qwen3" in model_id.lower():
        body["think"] = False
    headers = {"Content-Type": "application/json"}
    if provider in _UA_FOR:
        headers.update(_BROWSER_UA)
    else:
        headers["User-Agent"] = "atlas-moa/1.0"
    if key:
        headers["Authorization"] = f"Bearer {key}"
    data = _post(url, body, headers, timeout)
    msg = data["choices"][0]["message"]
    text = msg.get("content")
    if not text:  # reasoning models (gpt-oss, deepseek-r1, owl, hy3) put output in "reasoning"
        text = msg.get("reasoning") or msg.get("reasoning_content") or ""
    usage = data.get("usage", {})
    return text, usage

def _anthropic_call(model_id, prompt, sys_prompt, max_tokens, key, timeout=120):
    # map catalog id -> anthropic model name
    body = {
        "model": model_id.split("/")[-1] if "/" in model_id else model_id,
        "max_tokens": max_tokens,
        "system": sys_prompt,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "User-Agent": "atlas-moa/1.0",
    }
    data = _post("https://api.anthropic.com/v1/messages", body, headers, timeout)
    text = "".join(c.get("text", "") for c in data.get("content", []))
    usage = data.get("usage", {})
    return text, usage

def _hf_call(model_id, prompt, sys_prompt, max_tokens, key, timeout=150):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    # HF serverless is NOT OpenAI-compat; use text-generation style
    body = {
        "inputs": f"{sys_prompt}\n\n{prompt}",
        "parameters": {"max_new_tokens": max_tokens, "return_full_text": False},
    }
    headers = {"Content-Type": "application/json", "User-Agent": "atlas-moa/1.0"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    data = _post(url, body, headers, timeout)
    # response: list[{"generated_text": "..."}]
    if isinstance(data, list) and data:
        return data[0].get("generated_text", ""), {}
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"], {}
    return str(data), {}

def _replicate_call(model_id, prompt, sys_prompt, max_tokens, key, timeout=200):
    # model_id like "owner/name"; use synchronous Prefer: wait
    owner, name = model_id.split("/")[:2] if "/" in model_id else ("", model_id)
    url = f"https://api.replicate.com/v1/models/{owner}/{name}/predictions"
    body = {"input": {"prompt": f"{sys_prompt}\n\n{prompt}", "max_new_tokens": max_tokens}}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
        "Prefer": "wait",  # block until done
        "User-Agent": "atlas-moa/1.0",
    }
    data = _post(url, body, headers, timeout)
    out = data.get("output")
    if isinstance(out, list):
        return "\n".join(str(o) for o in out), {}
    return str(out or ""), {}

def _gemini_call(model_id, prompt, sys_prompt, max_tokens, key, timeout=120):
    # Gemini uses the native Generative Language API (not OpenAI-compat)
    mid = model_id.split("/", 1)[-1] if "/" in model_id else model_id
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{mid}:generateContent?key={key}"
    # Gemini reasoning models eat the token budget on thoughts; disable thinking
    # for normal chat/voice use so we get a real answer in content.parts.
    body = {
        "contents": [{"role": "user", "parts": [{"text": f"{sys_prompt}\n\n{prompt}"}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "thinkingConfig": {"thinkingBudget": 0}},
    }
    headers = {"Content-Type": "application/json", "User-Agent": "atlas-moa/1.0"}
    data = _post(url, body, headers, timeout)
    try:
        parts = data["candidates"][0]["content"].get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
    except (KeyError, IndexError):
        text = ""
    if not text:  # fallback: try reasoning/thought summary
        text = data.get("candidates", [{}])[0].get("finishReason", "")
    usage = data.get("usageMetadata", {})
    return text, usage

def _chutes_call(model_slug, prompt, sys_prompt, max_tokens, key, timeout=120):
    # Chutes deploys models as user "chutes" (apps). Generate endpoint:
    # POST https://api.chutes.ai/v1/chats/{username}/{slug}/api/generate
    user, slug = (model_slug.split("/", 1) + [""])[:2] if "/" in model_slug else ("chutes", model_slug)
    url = f"https://api.chutes.ai/v1/chats/{user}/{slug}/api/generate"
    body = {"messages": [{"role": "system", "content": sys_prompt},
                          {"role": "user", "content": prompt}], "max_tokens": max_tokens}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    data = _post(url, body, headers, timeout)
    # response: {"text": "...", ...} or {"outputs": [...]}
    if isinstance(data, dict):
        text = data.get("text") or data.get("output") or ""
        if isinstance(text, list):
            text = "\n".join(str(x) for x in text)
    else:
        text = str(data)
    return text, {}

def call_model(model_entry, prompt, sys_prompt="You are a helpful assistant.", max_tokens=500, timeout=180):
    """Route a call by the catalog model's home_provider. Returns (text, usage)."""
    provider = model_entry.get("home_provider", "openrouter")
    mid = model_entry["id"]
    try:
        if provider in OPENAI_COMPAT:
            key = _get_key(provider) or (pk.get_key("openrouter") if provider == "openrouter" else "")
            call_mid = mid.split("/", 1)[-1] if provider != "openrouter" else mid
            url = OPENAI_COMPAT[provider]
            if provider == "cloudflare":
                acct = pk.get_key("cloudflare_account_id") or ""
                if not acct:
                    return "(Cloudflare account_id missing — add cloudflare_account_id to secrets)", {}
                url = url.format(account_id=acct)
            return _openai_call(url, key, provider, call_mid, prompt, sys_prompt, max_tokens, timeout)
        if provider == "anthropic":
            ak = pk.get_key("anthropic")
            if not ak:
                return "(Anthropic key not set)", {}
            return _anthropic_call(mid, prompt, sys_prompt, max_tokens, ak, timeout)
        if provider == "huggingface":
            return _hf_call(mid, prompt, sys_prompt, max_tokens, pk.get_key("huggingface"), timeout)
        if provider == "replicate":
            return _replicate_call(mid, prompt, sys_prompt, max_tokens, pk.get_key("replicate"), timeout)
        if provider == "gemini":
            gk = pk.get_key("gemini")
            if not gk:
                return "(Gemini key not set)", {}
            return _gemini_call(mid, prompt, sys_prompt, max_tokens, gk, timeout)
        if provider == "chutes":
            ck = pk.get_key("chutes")
            if not ck:
                return "(Chutes key not set)", {}
            return _chutes_call(mid, prompt, sys_prompt, max_tokens, ck, timeout)
        # fallback: treat as openrouter
        return _openai_call(OPENAI_COMPAT["openrouter"], pk.get_key("openrouter"), "openrouter", mid, prompt, sys_prompt, max_tokens, timeout)
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:160]
        if provider == "anthropic" and "authentication_error" in msg:
            return "(Anthropic 401: key invalid — re-paste anthropic key in secrets)", {}
        return f"(HTTP {e.code}: {msg})", {}
    except Exception as e:
        return f"(ERR {type(e).__name__}: {e})", {}

def configured_providers():
    return pk.list_configured()
