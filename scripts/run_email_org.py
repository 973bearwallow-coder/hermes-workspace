#!/usr/bin/env python3
"""Quick email org scan - read inbox, classify, move, check retention, report."""
import subprocess, json, re, os, sys
from datetime import datetime, timedelta
from pathlib import Path

ACCOUNT = "toms gmail"
INBOX = "INBOX"
FOLDER_PREFIX = "CHARLES"

RETENTION = {
    "AI Profit Boardroom": 30, "AI Info": 14, "Accounts": 30,
    "Appointments": 30, "Atlas Communications": 30, "Cigars": 14,
    "Computer Systems": 30, "Divi": 14, "Family": 30, "Farm": 30,
    "Farm Equipment": 30, "Firearms": 14, "Guns": 14, "Misc": 14,
    "News": 7, "Promotions": 7, "Purchases": 30, "Recipes": 30,
    "Social": 7, "Tools": 7, "Work": 30,
}

CLASSIFICATION_RULES = [
    ("Appointments", ["appointment","schedule","meeting","calendar","book a","reserve","consultation","available","time slot","booking","calendly","acuity","square appointments","setmore","schedulicity"]),
    ("AI Profit Boardroom", ["tl;dv","tldv.io","skool.com","notifs.skool.com","ai profit boardroom","coaching call","meeting notes","multi-meeting ai report","uncover trends and insights"]),
    ("AI Info", ["hermes agent","redditmail.com","reddit.com","fireworks.ai","mem0.io","perplexity.ai","apify.com","chatgpt","chat gpt","openai","anthropic","claude","gemini","llm","ai agent","ai model"]),
    ("Atlas Communications", ["openclaw","charles health","atlas","atlastomsai","gateway down","gateway running","systemd"]),
    ("Family", ["suetorok","jane torok","carson","spencer","susan torok","caroline van wagoner","family"]),
    ("Accounts", ["security alert","verify your","verification code","password reset","new device","sign in code","authentication","two-factor","2fa","login","authorize","oauth","added to your account","google wallet","device verification","dashlane"]),
    ("Computer Systems", ["google one","google play","google cloud","google tips","google store","microsoft","apple","openrouter","notion","github","nvidia","mozilla"]),
    ("Cigars", ["famous cigars","cigar","humidor","drew estate"]),
    ("Firearms", ["palmetto state armory","brownells","opticsplanet","freedom gorilla","mountain valley auctions"]),
    ("Guns", ["ammo","ammunition","optic","scope","rifle","pistol","shotgun","firearm","gun","glock","sig sauer","smith & wesson","remington","winchester","federal","cci","hornady","berger","lapua","nightforce","vortex","leupold","trijicon","eotech","aimpoint","midwayusa","sportsman's","cabela's","bass pro","scheels","primary arms","geissele","daniel defense","hk","heckler","kac","knights armament","barrett","springfield","ruger","colt","beretta","cz usa","tikka","sako","weatherby","mossberg","benelli","sgammo","velocity ammo","ammo city","brownells deals"]),
    ("Farm", ["tractor","farm","agriculture","harvest","crop","livestock","tractor supply","rural king","fleet farm","orscheln","john deere","kubota","new holland","case ih","massey ferguson","agco","mower","plow","till","seed","fertilizer","feed store","co-op","grain","hay","bale","fence","gate","implement","meriwether farms"]),
    ("Farm Equipment", ["machinery trader","equipment auction","construction market"]),
    ("Tools", ["tool","harbor freight","home depot","lowe's","menards","northern tool","grizzly","woodcraft","rockler","lee valley","dewalt","milwaukee","makita","bosch","ridgid","craftsman","snap-on","mac tools","matco","gearwrench","proto","wright","channellock","irwin","klein","knipex","wera","wiha","drill","saw","grinder","impact","wrench","socket","circular saw","table saw","miter saw","band saw","router","planer","jointer","lathe","mill","press","vise"]),
    ("Divi", ["elegant themes","elegantthemes.com","divi 5","divi"]),
    ("News", ["news","breaking","report","update","china","market","stock","economy","trade","tariff","federal reserve","inflation","recession","gdp","unemployment","cpi","ppi","wall street","nasdaq","dow","s&p","ftse","nikkei","bloomberg","reuters","associated press","ap news","financial times","economist","barron's","marketwatch","cnbc","fox business","yahoo finance","google news","newsletter","daily briefing","morning brief","nextdoor local","trending on nextdoor","wall street journal","new york times","washington post"]),
    ("Promotions", ["sale","deal","discount","coupon","promo","promotion","save","clearance","special offer","limited time","flash sale","prime day","black friday","cyber monday","grocery","pharmacy","cvs","walgreens","rite aid","nike","adidas","under armour","reebok","wayfair","overstock","honey","swappa","amazon.com","amazon prime","amazon business","walmart","target","costco","bj's","lidl","kroger","safeway","best buy","samsung","wyze","sandisk","fogo de chao","is in demand","customer favorite","act now","interest is heating"]),
    ("Purchases", ["order confirmed","order shipped","your receipt","package was delivered","shipping confirmation","your order","purchase","invoice","payment received","refill ready","order delivered","delivered:","ebay - mark_k","members.ebay.com","reply.ebay.com","seller sent","counteroffer","payment method for best offer","confirm your email address","thanks for selecting","together computer","fidelity","ups package was delivered"]),
    ("Recipes", ["recipe","recipetineats","thewoksoflife","cozymeal","easy slow cooker","vegetable tian","salad dressing","coconut fish"]),
    ("Social", ["nextdoor","neighbor","trending on"]),
]

def run_hl(args, check=False, json_out=False):
    cmd = ["himalaya", "-o", "json"] + args
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0 and check:
        print(f"ERR: {r.stderr}", file=sys.stderr)
        return r
    if json_out:
        for line in r.stdout.split("\n"):
            line = line.strip()
            if line.startswith("[") or line.startswith("{"):
                r.stdout = line
                break
    return r

def classify(email_data, body=""):
    subj = (email_data.get("subject") or "").lower()
    sender_obj = email_data.get("from") or {}
    sender = (sender_obj.get("name") or "").lower()
    sender_email = (sender_obj.get("addr") or "").lower()
    body_p = body[:500].lower() if body else ""
    combined = f"{subj} {sender} {sender_email} {body_p}"
    for folder, keywords in CLASSIFICATION_RULES:
        for kw in keywords:
            if kw in combined:
                return folder
    return "Misc"

def move_email(email_id, folder):
    dest = f"{FOLDER_PREFIX}/{folder}"
    r = run_hl(["message", "move", "-f", INBOX, dest, str(email_id)])
    return r.returncode == 0

def list_folder(folder):
    r = run_hl(["envelope", "list", "-f", f"{FOLDER_PREFIX}/{folder}"], json_out=True)
    if r.returncode != 0 or not r.stdout.strip():
        return []
    try:
        return json.loads(r.stdout)
    except:
        return []

def delete_email(email_id, folder):
    r = run_hl(["message", "delete", "-f", f"{FOLDER_PREFIX}/{folder}", str(email_id)])
    return r.returncode == 0

def expunge(folder):
    run_hl(["folder", "expunge", "-f", f"{FOLDER_PREFIX}/{folder}"])

def apply_retention(folder):
    days = RETENTION.get(folder)
    if not days:
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    emails = list_folder(folder)
    deleted = 0
    for e in emails:
        ds = e.get("date") or e.get("internaldate", "")
        if not ds:
            continue
        try:
            ed = datetime.fromisoformat(ds)
            if ed.tzinfo:
                from datetime import timezone
                cu = cutoff.replace(tzinfo=timezone.utc)
            else:
                cu = cutoff
            if ed < cu:
                eid = e.get("id")
                if eid and delete_email(eid, folder):
                    deleted += 1
        except:
            pass
    return deleted

def notify_appointment(subject, sender):
    nf = Path.home() / ".hermes" / "cron" / "output" / "email_notification.txt"
    nf.parent.mkdir(parents=True, exist_ok=True)
    with open(nf, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] 📅 Appointment email: '{subject}' from {sender}. Add to Google Calendar?\n")

def main():
    print(f"=== Email Org: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print("\n📥 Reading inbox...")
    r = run_hl(["envelope", "list", "-f", INBOX, "-s", "500"], json_out=True)
    if r.returncode != 0 or not r.stdout.strip():
        print("   No emails or error reading inbox.")
        return
    try:
        emails = json.loads(r.stdout)
    except:
        print("   Failed to parse inbox listing.")
        return
    print(f"   Found {len(emails)} emails in INBOX")

    # Filter > 12 hours old
    cutoff = datetime.now() - timedelta(hours=12)
    old = []
    for e in emails:
        ds = e.get("date") or e.get("internaldate", "")
        if ds:
            try:
                ed = datetime.fromisoformat(ds)
                if ed.tzinfo:
                    from datetime import timezone
                    cu = cutoff.replace(tzinfo=timezone.utc)
                else:
                    cu = cutoff
                if ed < cu:
                    old.append(e)
            except:
                old.append(e)
        else:
            old.append(e)
    print(f"   {len(old)} emails > 12h old")

    moved = {}
    appointments = []
    skipped = 0
    for email in old:
        eid = email.get("id")
        subj = email.get("subject", "(no subject)")
        sender = email.get("from", {}).get("name") or email.get("from", {}).get("addr") or "Unknown"
        folder = classify(email)
        if move_email(eid, folder):
            moved[folder] = moved.get(folder, 0) + 1
            print(f"   → [{folder}] {subj[:60]} (from {sender[:30]})")
            if folder == "Appointments":
                appointments.append({"subject": subj, "sender": sender, "date": email.get("date", "")})
        else:
            print(f"   ✗ Failed: {subj[:60]}")
            skipped += 1

    # Retention
    print("\n🗑 Retention cleanup...")
    total_del = 0
    for folder, days in RETENTION.items():
        d = apply_retention(folder)
        if d > 0:
            print(f"   Deleted {d} from {folder} (>{days}d)")
            total_del += d
            expunge(folder)

    # Summary
    print(f"\n📊 Summary:")
    print(f"   Sorted: {sum(moved.values())}")
    for f, c in sorted(moved.items()):
        print(f"     {f}: {c}")
    print(f"   Skipped: {skipped}")
    print(f"   Deleted (retention): {total_del}")

    # Appointments
    if appointments:
        print(f"\n📅 Appointments: {len(appointments)}")
        for a in appointments:
            notify_appointment(a["subject"], a["sender"])
            print(f"   → {a['subject'][:60]} from {a['sender']}")

    print(f"\n✅ Done {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
