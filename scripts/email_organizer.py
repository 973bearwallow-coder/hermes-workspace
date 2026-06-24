#!/usr/bin/env python3
"""
Daily email organization script for Tom's Gmail (973bearwallow@gmail.com).
Uses Himalaya CLI to read, classify, and move emails.

Process:
1. Read emails from INBOX (page size 500)
2. Filter to emails > 12 hours old
3. Classify each email into a folder based on sender/subject/content
4. Move to appropriate folder
5. Apply retention rules (delete old emails from folders)
6. For appointment emails, notify Tom via Telegram

Folder retention rules:
- Appointments: keep 1 month (ask Tom before adding to Google Calendar)
- Farm: delete after 1 month
- Guns: keep 2 weeks
- News: keep 1 week
- Promotions: keep 1 week
- Tools: keep 1 week
"""

import subprocess
import json
import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
ACCOUNT = "toms gmail"
INBOX = "INBOX"
FOLDER_PREFIX = "CHARLES"
TELEGRAM_CHAT_ID = "7602246023"

# Folder retention in days
RETENTION = {
    "AI Profit Boardroom": 30,
    "AI Info": 14,
    "Accounts": 30,
    "Appointments": 30,
    "Atlas Communications": 30,
    "Cigars": 14,
    "Computer Systems": 30,
    "Divi": 14,
    "Family": 30,
    "Farm": 30,
    "Farm Equipment": 30,
    "Firearms": 14,
    "Guns": 14,
    "Misc": 14,
    "News": 7,
    "Promotions": 7,
    "Purchases": 30,
    "Recipes": 30,
    "Social": 7,
    "Tools": 7,
    "Work": 30,
}

# Classification rules: (folder_name, keywords)
# Order matters — first match wins
CLASSIFICATION_RULES = [
    # --- Appointments & scheduling ---
    ("Appointments", [
        "appointment", "schedule", "meeting", "calendar", "book a", "reserve",
        "consultation", "available", "time slot", "booking", "calendly",
        "acuity", "square appointments", "setmore", "schedulicity",
    ]),

    # --- AI Profit Boardroom (coaching calls, Skool, tl;dv) ---
    ("AI Profit Boardroom", [
        "tl;dv", "tldv.io", "skool.com", "notifs.skool.com",
        "ai profit boardroom", "coaching call", "meeting notes",
        "multi-meeting ai report", "uncover trends and insights",
    ]),

    # --- AI Info (Reddit Hermes/AI blogs, AI news) ---
    ("AI Info", [
        "hermes agent", "redditmail.com", "reddit.com",
        "fireworks.ai", "mem0.io", "perplexity.ai", "apify.com",
        "chatgpt", "chat gpt", "openai", "anthropic", "claude",
        "gemini", "llm", "ai agent", "ai model",
    ]),

    # --- Atlas Communications (OpenClaw/Atlas alerts) ---
    ("Atlas Communications", [
        "openclaw", "charles health", "atlas", "atlastomsai",
        "gateway down", "gateway running", "systemd",
    ]),

    # --- Family ---
    ("Family", [
        "suetorok", "jane torok", "carson", "spencer", "susan torok",
        "caroline van wagoner", "family",
    ]),

    # --- Accounts (security alerts, verification, auth) ---
    ("Accounts", [
        "security alert", "verify your", "verification code", "password reset",
        "new device", "sign in code", "authentication", "two-factor", "2fa",
        "login", "authorize", "oauth", "added to your account",
        "google wallet", "device verification", "dashlane",
    ]),

    # --- Computer Systems (Google services, cloud, software) ---
    ("Computer Systems", [
        "google one", "google play", "google cloud", "google tips",
        "google store", "microsoft", "apple", "openrouter",
        "notion", "github", "nvidia", "mozilla",
    ]),

    # --- Cigars ---
    ("Cigars", [
        "famous cigars", "cigar", "humidor", "drew estate",
    ]),

    # --- Firearms (gun dealers, not ammo) ---
    ("Firearms", [
        "palmetto state armory", "brownells", "opticsplanet",
        "freedom gorilla", "mountain valley auctions",
    ]),

    # --- Guns (ammo, accessories) ---
    ("Guns", [
        "ammo", "ammunition", "optic", "scope", "rifle", "pistol", "shotgun",
        "firearm", "gun", "glock", "sig sauer", "smith & wesson", "remington",
        "winchester", "federal", "cci", "hornady", "berger", "lapua",
        "nightforce", "vortex", "leupold", "trijicon", "eotech", "aimpoint",
        "midwayusa", "sportsman's", "cabela's", "bass pro", "scheels",
        "primary arms", "geissele", "daniel defense", "hk", "heckler",
        "kac", "knights armament", "barrett", "springfield", "ruger", "colt",
        "beretta", "cz usa", "tikka", "sako", "weatherby", "mossberg",
        "benelli", "sgammo", "velocity ammo", "ammo city", "brownells deals",
    ]),

    # --- Farm ---
    ("Farm", [
        "tractor", "farm", "agriculture", "harvest", "crop", "livestock",
        "tractor supply", "rural king", "fleet farm", "orscheln", "john deere",
        "kubota", "new holland", "case ih", "massey ferguson", "agco",
        "mower", "plow", "till", "seed", "fertilizer", "feed store",
        "co-op", "grain", "hay", "bale", "fence", "gate", "implement",
        "meriwether farms",
    ]),

    # --- Farm Equipment ---
    ("Farm Equipment", [
        "machinery trader", "equipment auction", "construction market",
    ]),

    # --- Tools ---
    ("Tools", [
        "tool", "harbor freight", "home depot", "lowe's", "menards",
        "northern tool", "grizzly", "woodcraft", "rockler", "lee valley",
        "dewalt", "milwaukee", "makita", "bosch", "ridgid", "craftsman",
        "snap-on", "mac tools", "matco", "gearwrench", "proto", "wright",
        "channellock", "irwin", "klein", "knipex", "wera", "wiha",
        "drill", "saw", "grinder", "impact", "wrench", "socket",
        "circular saw", "table saw", "miter saw", "band saw", "router",
        "planer", "jointer", "lathe", "mill", "press", "vise",
    ]),

    # --- Divi / Elegant Themes ---
    ("Divi", [
        "elegant themes", "elegantthemes.com", "divi 5", "divi",
    ]),

    # --- News ---
    ("News", [
        "news", "breaking", "report", "update", "china", "market", "stock",
        "economy", "trade", "tariff", "federal reserve", "inflation",
        "recession", "gdp", "unemployment", "cpi", "ppi",
        "wall street", "nasdaq", "dow", "s&p", "ftse", "nikkei",
        "bloomberg", "reuters", "associated press", "ap news",
        "financial times", "economist", "barron's", "marketwatch",
        "cnbc", "fox business", "yahoo finance", "google news",
        "newsletter", "daily briefing", "morning brief",
        "nextdoor local", "trending on nextdoor",
        "wall street journal", "new york times", "washington post",
    ]),

    # --- Promotions ---
    ("Promotions", [
        "sale", "deal", "discount", "coupon", "promo", "promotion",
        "save", "clearance", "special offer", "limited time", "flash sale",
        "prime day", "black friday", "cyber monday",
        "grocery", "pharmacy", "cvs", "walgreens", "rite aid",
        "nike", "adidas", "under armour", "reebok",
        "wayfair", "overstock", "honey", "swappa",
        "amazon.com", "amazon prime", "amazon business",
        "walmart", "target", "costco", "bj's", "lidl", "kroger", "safeway",
        "best buy", "samsung", "wyze", "sandisk", "fogo de chao",
        "is in demand", "customer favorite", "act now", "interest is heating",
    ]),

    # --- Purchases (actual orders, receipts, shipping) ---
    ("Purchases", [
        "order confirmed", "order shipped", "your receipt",
        "package was delivered", "shipping confirmation", "your order",
        "purchase", "invoice", "payment received", "refill ready",
        "order delivered", "delivered:",
        "ebay - mark_k", "members.ebay.com", "reply.ebay.com",
        "seller sent", "counteroffer", "payment method for best offer",
        "confirm your email address", "thanks for selecting",
        "together computer", "fidelity", "ups package was delivered",
    ]),

    # --- Recipes ---
    ("Recipes", [
        "recipe", "recipetineats", "thewoksoflife", "cozymeal",
        "easy slow cooker", "vegetable tian", "salad dressing",
        "coconut fish",
    ]),

    # --- Social (Nextdoor, Reddit non-AI, Skool social) ---
    ("Social", [
        "nextdoor", "neighbor", "trending on",
    ]),
]


def run_himalaya(args, check=True, json_output=False):
    """Run himalaya CLI command and return output."""
    cmd = ["himalaya", "-o", "json"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        if check:
            print(f"Himalaya error: {result.stderr}", file=sys.stderr)
        return result
    if json_output:
        # Filter out WARN lines and extract JSON
        stdout = result.stdout
        for line in stdout.split('\n'):
            line = line.strip()
            if line.startswith('[') or line.startswith('{'):
                result.stdout = line
                break
    return result


def list_inbox_emails():
    """List all emails in INBOX."""
    result = run_himalaya(["envelope", "list", "-f", INBOX, "-s", "500"], check=False, json_output=True)
    if result.returncode != 0 or not result.stdout.strip():
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Failed to parse envelope list: {result.stdout[:200]}", file=sys.stderr)
        return []


def read_email(id):
    """Read a specific email by ID."""
    result = run_himalaya(["message", "read", "-f", INBOX, str(id)], check=False)
    if result.returncode != 0:
        return None
    return result.stdout


def move_email(id, folder):
    """Move email to a folder."""
    dest = f"{FOLDER_PREFIX}/{folder}"
    result = run_himalaya(["message", "move", "-f", INBOX, dest, str(id)], check=False)
    return result.returncode == 0


def delete_email(id, folder):
    """Delete email from a folder (move to trash)."""
    result = run_himalaya(["message", "delete", "-f", folder, str(id)], check=False)
    return result.returncode == 0


def expunge_folder(folder):
    """Expunge deleted messages from a folder."""
    result = run_himalaya(["folder", "expunge", "-f", folder], check=False)
    return result.returncode == 0


def list_folder_emails(folder):
    """List all emails in a folder."""
    result = run_himalaya(["envelope", "list", "-f", f"{FOLDER_PREFIX}/{folder}"], check=False, json_output=True)
    if result.returncode != 0 or not result.stdout.strip():
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []


def classify_email(email_data, email_body=""):
    """Classify an email into a folder based on rules."""
    subject = (email_data.get("subject") or "").lower()
    sender_obj = email_data.get("from") or {}
    sender = (sender_obj.get("name") or "").lower()
    sender_email = (sender_obj.get("addr") or "").lower()
    body_preview = email_body[:500].lower() if email_body else ""
    
    combined = f"{subject} {sender} {sender_email} {body_preview}"
    
    for folder, keywords in CLASSIFICATION_RULES:
        for keyword in keywords:
            if keyword in combined:
                return folder
    
    return None  # No classification match


def apply_retention(folder):
    """Delete emails older than retention period from a folder."""
    retention_days = RETENTION.get(folder)
    if not retention_days:
        return 0
    
    cutoff = datetime.now() - timedelta(days=retention_days)
    emails = list_folder_emails(folder)
    deleted = 0
    
    for email in emails:
        date_str = email.get("date") or email.get("internaldate", "")
        if not date_str:
            continue
        
        try:
            # Himalaya returns ISO format: "2026-06-14 17:12+00:00"
            email_date = datetime.fromisoformat(date_str)
            # Make cutoff timezone-aware if email has tz info
            if email_date.tzinfo is not None:
                from datetime import timezone
                cutoff_aware = cutoff.replace(tzinfo=timezone.utc)
            else:
                cutoff_aware = cutoff
            
            if email_date < cutoff_aware:
                email_id = email.get("id")
                if email_id and delete_email(email_id, f"{FOLDER_PREFIX}/{folder}"):
                    deleted += 1
        except Exception as e:
            print(f"Error processing email date {date_str}: {e}", file=sys.stderr)
    
    return deleted


def is_appointment_email(email_data, email_body=""):
    """Check if email is an appointment/scheduling related email."""
    subject = (email_data.get("subject") or "").lower()
    sender = (email_data.get("from") or {}).get("name", "").lower()
    combined = f"{subject} {sender}"
    
    appointment_keywords = [
        "appointment", "schedule", "meeting", "calendar", "book",
        "consultation", "available", "time slot", "booking", "calendly",
        "acuity", "square appointments", "setmore",
    ]
    
    return any(kw in combined for kw in appointment_keywords)


def send_telegram_notification(message):
    """Write appointment notification to a file that the cron agent can pick up."""
    notification_file = Path.home() / ".hermes" / "cron" / "output" / "email_appointments.txt"
    notification_file.parent.mkdir(parents=True, exist_ok=True)
    with open(notification_file, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {message}\n")


def main():
    print(f"=== Email Organization Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Step 1: Get inbox emails
    print("\n📥 Reading inbox...")
    emails = list_inbox_emails()
    print(f"   Found {len(emails)} emails in INBOX")
    
    if not emails:
        print("   No emails to process.")
        return
    
    # Step 2: Filter emails older than 12 hours
    cutoff_time = datetime.now() - timedelta(hours=12)
    old_emails = []
    for email in emails:
        date_str = email.get("date") or email.get("internaldate", "")
        if date_str:
            try:
                email_date = datetime.fromisoformat(date_str)
                if email_date.tzinfo is not None:
                    from datetime import timezone
                    cutoff_aware = cutoff_time.replace(tzinfo=timezone.utc)
                else:
                    cutoff_aware = cutoff_time
                if email_date < cutoff_aware:
                    old_emails.append(email)
            except Exception:
                old_emails.append(email)  # If we can't parse date, include it
        else:
            old_emails.append(email)
    
    print(f"   {len(old_emails)} emails are > 12 hours old (ready to sort)")
    
    # Step 3: Classify and move emails
    moved = {}
    appointments = []
    skipped = 0
    
    for email in old_emails:
        email_id = email.get("id")
        subject = email.get("subject", "(no subject)")
        sender = email.get("from", {}).get("name") or email.get("from", {}).get("addr") or "Unknown"
        
        # Classify
        folder = classify_email(email)
        
        # Catch-all: anything unmatched goes to Misc
        if not folder:
            folder = "Misc"
        
        if move_email(email_id, folder):
            moved[folder] = moved.get(folder, 0) + 1
            print(f"   → [{folder}] {subject[:50]} (from {sender[:30]})")
            
            # Track appointments for notification
            if folder == "Appointments":
                appointments.append({
                    "subject": subject,
                    "sender": sender,
                    "date": email.get("date", ""),
                })
        else:
            print(f"   ✗ Failed to move: {subject[:50]}")
            skipped += 1
    
    # Step 4: Apply retention rules
    print("\n🗑 Applying retention rules...")
    total_deleted = 0
    for folder, days in RETENTION.items():
        deleted = apply_retention(folder)
        if deleted > 0:
            print(f"   Deleted {deleted} emails from {folder} (>{days} days old)")
            total_deleted += deleted
            expunge_folder(f"{FOLDER_PREFIX}/{folder}")
    
    # Step 5: Report
    print(f"\n📊 Summary:")
    print(f"   Emails sorted: {sum(moved.values())}")
    for folder, count in moved.items():
        print(f"     {folder}: {count}")
    print(f"   Emails skipped (no match): {skipped}")
    print(f"   Emails deleted (retention): {total_deleted}")
    
    # Step 6: Notify about appointments
    if appointments:
        print(f"\n📅 Appointment emails found: {len(appointments)}")
        for appt in appointments:
            msg = f"📅 Appointment email: '{appt['subject']}' from {appt['sender']}. Add to Google Calendar?"
            send_telegram_notification(msg)
            print(f"   → {msg}")
    
    print(f"\n✅ Done at {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
