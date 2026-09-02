import json
import urllib.request
from pathlib import Path

env = {}
for line in Path('/home/tom/.hermes/.env').read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, v = line.split('=', 1)
    env[k] = v.strip().strip('"').strip("'")

token = env['TELEGRAM_BOT_TOKEN']
chat = env['TELEGRAM_HOME_CHANNEL']
text = '📅 Appointment email: "\\"Coaching Calls\\" meeting notes and AI answers are ready ✅" from tl;dv Team\nAdd this to your Google Calendar? (yes/no)'
payload = json.dumps({'chat_id': chat, 'text': text}).encode()
req = urllib.request.Request(
    f'https://api.telegram.org/bot{token}/sendMessage',
    data=payload,
    headers={'Content-Type': 'application/json'},
)
resp = urllib.request.urlopen(req, timeout=30).read().decode()
print(resp)
