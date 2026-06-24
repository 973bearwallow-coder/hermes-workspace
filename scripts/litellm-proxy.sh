#!/bin/bash
# Start litellm proxy that routes Anthropic API requests to OpenRouter
# This lets Claude Code (which only talks Anthropic API) use OpenRouter models

# Read OpenRouter API key from Hermes config
OPENROUTER_API_KEY=*** -c "
import yaml
with open('/home/tom/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
for provider in config.get('providers', {}).values():
    if 'openrouter' in str(provider.get('base_url', '')):
        print(provider.get('api_key', ''))
        break
" 2>/dev/null)

export OPENROUTER_API_KEY

# Start litellm with OpenRouter as the backend
exec litellm \
  --model openrouter/owl-alpha \
  --api_base https://openrouter.ai/api/v1 \
  --api_key "$OPENROUTER_API_KEY" \
  --port 4000 \
  --host 127.0.0.1 \
  --drop_params \
  --num_retries 2
