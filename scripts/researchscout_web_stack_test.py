#!/usr/bin/env python3
import json, subprocess, sys, urllib.request

results = []
def run(name, cmd):
    p = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    results.append({'tool': name, 'ok': p.returncode == 0, 'stdout': p.stdout.strip()[-500:], 'stderr': p.stderr.strip()[-500:]})

with urllib.request.urlopen('https://example.com/', timeout=30) as r:
    body = r.read().decode('utf-8', 'replace')
results.append({'tool':'direct_http', 'ok': 'Example Domain' in body})

run('scrapling', ['/home/tom/hermes-workspace/venvs/scrapling-research/bin/python', '-c',
    "from scrapling.fetchers import Fetcher; p=Fetcher.get('https://example.com', timeout=30000); assert p.css('h1::text').get().strip()=='Example Domain'; print('ok')"])
run('playwright', [sys.executable, '-c',
    "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); q=b.new_page(); q.set_content('<h1>browser-ok</h1>'); assert q.locator('h1').inner_text()=='browser-ok'; b.close(); p.stop(); print('ok')"])
run('scrapy', ['/home/tom/hermes-workspace/venvs/scraping/bin/python3', '-c', "import scrapy; print(scrapy.__version__)"])
run('crawlee', ['node', '/home/tom/hermes-workspace/tools/crawlee-research/smoke.mjs'])
run('kimi_status', ['/home/tom/.kimi-webbridge/bin/kimi-webbridge', 'status'])

print(json.dumps(results, indent=2))
if not all(x['ok'] for x in results): raise SystemExit(1)