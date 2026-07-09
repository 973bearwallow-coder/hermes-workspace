#!/bin/bash
set -euo pipefail

HERMES_CONFIG="${HOME}/.hermes/config.yaml"

get_config_value() {
    local key_path=$1
    grep -E "^\s*${key_path}:\s*" "${HERMES_CONFIG}" | \
        sed -E "s/^[[:space:]]*${key_path}:\s*\"?([^\"#]+)\"?.*$/\1/" | \
        tr -d '[:space:]'
}

echo "=== Current Vision Model ==="
get_config_value 'auxiliary.vision.model'

echo "=== GPU VRAM Status ==="
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu,utilization.memory --format=csv,noheader

echo "=== Ollama Process Status ==="
ps aux | grep -E "(ollama|llama)" | grep -v grep || echo "No ollama/llama processes found"