#!/bin/bash
# Start litellm proxy on :4000 that translates Anthropic API → OpenRouter
# This lets Claude Code (Anthropic-only) use any OpenRouter model

# Source the key from .env securely
if [ -f /home/tom/.hermes/.env ]; then
    export OPENROUTER_API_KEY=*** -E '/OPENROUTER_API_KEY/{n;p;q}' /home/tom/.hermes/.env | head -1 | sed 's/"//g')
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "ERROR: No OpenRouter key found" >&2
    exit 1
fi

exec /home/tom/.hermes/hermes-agent/venv/bin/litellm \
  --config /home/tom/hermes-workspace/scripts/litellm-config.yaml \
  --port 4000 \
  --host 127.0.0.1
