#!/usr/bin/env python3
"""Extract summaries from Guild Archive Fathom recordings."""
import json, subprocess, time, re, os
from datetime import datetime

OUTPUT_DIR = "/home/tom/hermes-workspace/coaching-calls"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# All 39 Fathom URLs from the Guild Archive
fathom_urls = [
    "https://fathom.video/share/2gKCyvyABhW6Yqa5rgXaa19tZDw3gB4h",
    "https://fathom.video/share/N2qouJC5GLoS-CpXT2km9bvPo6JzM9VW",
    "https://fathom.video/share/kdmsPTYSGDyk_1x75hxKcjEwX9_Mta36",
    "https://fathom.video/share/x2RhsmeN7acscxF6er7X4arqne5RJc4r",
    "https://fathom.video/share/s_HqZwYGQKxsTZ7xdsbxSaFHZe8fVeD7",
    "https://fathom.video/share/Vem_DzvYnkYyemzobgysr5ZepHHCXbVz",
    "https://fathom.video/share/uqqzccQRu72qs2AU1L8CiguCHWSCi8ux",
    "https://fathom.video/share/_BVdG_4__H6aDYsNBNviRa1sFiiiQ9ss",
    "https://fathom.video/share/pzTy5JcQMLyJhxpiwPGSsgunz6QDFHKN",
    "https://fathom.video/share/Z9Vs6UR6aa1S9-9WcLztMsD_-XS6xBcc",
    "https://fathom.video/share/tQdZfbYKGU_muUrWS9zjWpEDPefE4wnB",
    "https://fathom.video/share/YmEE4XqzwnxBnYAsZ93tQp_Z-shXt-Tc",
    "https://fathom.video/share/ESsDMSZNC6aggfKsKacaS-8cgd_WJNRn",
    "https://fathom.video/share/G37SKy_YVHBZxfg6zP7DrQxxQQ1rfYH2",
    "https://fathom.video/share/j6FHpstdpZFJi7VGCvgBj8HXtTDxvDWw",
]

def kimi(method, session="fathom_batch", **kwargs):
    """Call Kimi WebBridge."""
    payload = {"action": method, "args": kwargs, "session": session}
    cmd = ["curl", "-s", "-X", "POST", "http://127.0.0.1:10086/command",
           "-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return json.loads(result.stdout)
    except:
        return {"ok": False, "error": result.stdout}

results = []
for url in fathom_urls:
    share_id = url.split("/")[-1]
    print(f"\n{'='*60}")
    print(f"Processing: {share_id}")
    
    # Navigate
    resp = kimi("navigate", url=url, newTab=True, group_title=f"Fathom {share_id}")
    if not resp.get("data",{}).get("success"):
        print(f"  Navigate failed: {resp}")
        continue
    
    time.sleep(10)  # Wait for JS rendering
    
    # Get page content
    resp = kimi("evaluate", code="document.body.innerText", session="fathom_batch")
    text = resp.get("data",{}).get("value","")
    
    # Get title
    resp2 = kimi("evaluate", code="document.title", session="fathom_batch")
    title = resp2.get("data",{}).get("value","")
    
    # Get URL
    resp3 = kimi("evaluate", code="window.location.href", session="fathom_batch")
    current_url = resp3.get("data",{}).get("value","")
    
    info = {
        "share_id": share_id,
        "title": title,
        "url": current_url,
        "text": text[:3000] if text else "",
        "timestamp": datetime.now().isoformat(),
    }
    results.append(info)
    
    print(f"  Title: {title}")
    print(f"  Text length: {len(text)}")
    if text:
        print(f"  Preview: {text[:200]}")
    
    # Close tab to free resources
    kimi("navigate", url="about:blank", session="fathom_batch")
    time.sleep(2)

# Save results
output = {"processed_at": datetime.now().isoformat(), "recordings": results}
with open(f"{OUTPUT_DIR}/guild_archive_summaries.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n\n✅ Processed {len(results)} recordings")
print(f"Results saved to {OUTPUT_DIR}/guild_archive_summaries.json")