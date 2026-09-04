#!/bin/bash
# codex-health-return.sh
# Deterministic no-agent watchdog: when OpenAI's Codex backend recovers,
# flip the Hermes default model back from deepseek flash to gpt-5.6-sol.
# Emits [SILENT] when nothing changes (healthy stays healthy / codex still down).
set -u
LOG=/home/tom/hermes-workspace/logs/codex-return.log
mkdir -p "$(dirname "$LOG")"

AUTH=/home/tom/.hermes/auth.json
CFG=/home/tom/.hermes/config.yaml

# --- Resolve current default model ---
CUR=$(grep -A4 '^model:' "$CFG" | grep 'default:' | head -1 | awk '{print $2}')
echo "$(date -Is) cur=${CUR:-<none>}" >> "$LOG"

# Only act if we are NOT already on codex
if [[ "$CUR" == "gpt-5.6-sol" ]]; then
  echo "$(date -Is) already on codex, nothing to do" >> "$LOG"
  echo "[SILENT]"
  exit 0
fi

# --- Load access token (redacted in logs) ---
TOK=$(python3 -c "
import json,sys
d=json.load(open('$AUTH'))
e=d['credential_pool']['openai-codex'][0]
sys.stdout.write(e.get('access_token',''))
")
if [[ -z "$TOK" ]]; then
  echo "$(date -Is) no codex token available" >> "$LOG"
  echo "[SILENT]"
  exit 0
fi

# --- Probe the real endpoint (/responses) ---
# streams a trivial prompt; success = HTTP 2xx
CODE=$(curl -s -o /tmp/codex_probe.json -w '%{http_code}' --max-time 25 \
  -X POST 'https://chatgpt.com/backend-api/codex/responses' \
  -H "Authorization: Bearer $TOK" \
  -H 'Content-Type: application/json' \
  -H 'OpenAI-Beta: codex-v1' \
  -d '{"model":"gpt-5.6-sol","input":[{"role":"user","content":"ping"}],"store":false,"stream":true}')
echo "$(date -Is) probe_http=$CODE" >> "$LOG"

# 2xx = healthy -> switch back. 404/5xx/503 = still down -> silent.
if [[ "$CODE" == "2"* ]]; then
  echo "$(date -Is) CODECX HEALTHY -> switching default back to gpt-5.6-sol" >> "$LOG"
  # backup config
  cp "$CFG" "${CFG}.pre-codex-return-$(date +%Y%m%dT%H%M%S%Z)"
  python3 - "$CFG" <<'PYEOF'
import sys, re
p=sys.argv[1]
s=open(p).read()
s=re.sub(r'(^model:\n(\s+)default:)(.*)$',
         lambda m: m.group(1)+' gpt-5.6-sol', s, count=1, flags=re.M)
s=re.sub(r'(^model:\n(?:\s+[^\n]*\n){1})(\s+provider:)(.*)$',
         lambda m: m.group(1)+m.group(2)+' openai-codex', s, count=1, flags=re.M)
s=re.sub(r'(^model:\n(?:\s+[^\n]*\n){2})(\s+base_url:).*$',
         lambda m: m.group(1)+m.group(2)+' https://chatgpt.com/backend-api/codex', s, count=1, flags=re.M)
open(p,'w').write(s)
PYEOF
  # gateaway restart from external process
  systemctl --user restart hermes-gateway.service
  echo "$(date -Is) gateway restarted, switched to gpt-5.6-sol" >> "$LOG"
  echo "Codex backend recovered. Switched Hermes default model back to gpt-5.6-sol."
else
  echo "$(date -Is) codex still down (http=$CODE), staying on $CUR" >> "$LOG"
  echo "[SILENT]"
fi