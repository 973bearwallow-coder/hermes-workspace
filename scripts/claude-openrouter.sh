#!/bin/bash
# claude-openrouter — Run Claude Code using OpenRouter instead of Anthropic
# Usage: claude-openrouter [claude-code-args...]
#
# This sets the ANTHROPIC_API_KEY to our OpenRouter key and configures
# the base URL so Claude Code routes through OpenRouter.

# Read OpenRouter API key from Hermes config
OPENROUTER_API_KEY=$(python3 -c "
import yaml
with open('/home/tom/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
for provider in config.get('providers', {}).values():
    if 'openrouter' in str(provider.get('base_url', '')):
        print(provider.get('api_key', ''))
        break
" 2>/dev/null)

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "ERROR: Could not find OpenRouter API key in config" >&2
    exit 1
fi

export ANTHROPIC_API_KEY="$OPENROUTER_API_KEY"

# Run Claude Code with all passed arguments
exec claude "$@"
