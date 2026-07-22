#!/usr/bin/env python3
"""
get_provider_key.py — Safe provider-key reader for Atlas MoA Router.
Reads /home/tom/.hermes/secrets/provider_keys.json (chmod 600, gitignored).
NEVER prints raw values. Returns the key or empty string if unset.
"""
import json, os, re

SECRETS = "/home/tom/.hermes/secrets/provider_keys.json"
CONFIG = "/home/tom/.hermes/config.yaml"

# provider name -> json key
ALIASES = {
    "github": "github_pat", "github_models": "github_pat", "gh": "github_pat",
    "hf": "huggingface", "huggingface": "huggingface",
    "nous": "nous", "nousresearch": "nous",
    "nvidia": "nvidia", "nim": "nvidia",
    "replicate": "replicate",
    "anthropic": "anthropic", "claude": "anthropic",
    "openai": "openai", "gpt": "openai",
    "cloudflare": "cloudflare", "cf": "cloudflare",
    "cloudflare_account_id": "cloudflare_account_id",
    "agnes": "agnes", "cerebras": "cerebras", "deepseek": "deepseek", "gemini": "gemini",
    "chutes": "chutes", "nebius": "nebius",
    "openrouter": "openrouter",
    "groq": "groq",
}

# providers whose key may live in Hermes config.yaml if not in secrets
CONFIG_FALLBACK = {"openrouter", "groq"}

def _load_secrets():
    try:
        with open(SECRETS) as f:
            return json.load(f)
    except Exception:
        return {}

def _config_key(provider):
    try:
        cfg = open(CONFIG).read()
        if provider == "openrouter":
            m = re.search(r"openrouter:\s*\n\s*api_key:\s*(\S+)", cfg)
            return m.group(1) if m else ""
        if provider == "groq":
            m = re.search(r"groq:\s*\n\s*api_key:\s*(\S+)", cfg)
            return m.group(1) if m else ""
    except Exception:
        pass
    return ""

def get_key(provider):
    """Return API key for provider (by alias) or '' if missing.
    Falls back to Hermes config.yaml for openrouter/groq."""
    key = ALIASES.get(provider.lower().strip())
    if not key:
        return ""
    data = _load_secrets()
    val = data.get(key, "") or ""
    if val:
        return val
    if provider in CONFIG_FALLBACK:
        return _config_key(provider)
    return ""

def is_configured(provider):
    return bool(get_key(provider))

def list_configured():
    """Return provider aliases that have a non-empty key (no values)."""
    data = _load_secrets()
    out = [k for k, v in data.items() if v and not k.startswith("_")]
    if _config_key("openrouter"):
        out.append("openrouter (from config)")
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        p = sys.argv[1]
        print(f"{p}: {'CONFIGURED' if is_configured(p) else 'missing'}")
    else:
        print("configured providers:", list_configured())
