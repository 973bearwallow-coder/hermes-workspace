"""Read the OpenRouter API key from Hermes config WITHOUT hardcoding it."""
import os, re

def get_key():
    cfg = "/home/tom/.hermes/config.yaml"
    txt = open(cfg).read()
    # find the openrouter block's api_key: sk-...
    m = re.search(r"openrouter:\s*\n\s*api_key:\s*(sk-[^\s]+)", txt)
    if m:
        return m.group(1)
    # fallback: any sk- under providers
    m = re.search(r"api_key:\s*(sk-[A-Za-z0-9]+)", txt)
    return m.group(1) if m else None

if __name__ == "__main__":
    k = get_key()
    print("KEY_FOUND" if k else "KEY_MISSING", (k[:6] + "...") if k else "")
