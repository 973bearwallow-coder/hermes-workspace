#!/usr/bin/env python3
"""Quick Google Workspace CLI wrapper using saved OAuth token"""
import sys
import pickle
import os
from datetime import datetime, timedelta

TOKEN_FILE = '/home/tom/.hermes/google/token.pickle'

def get_creds():
    with open(TOKEN_FILE, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)
    return creds

def calendar():
    from googleapiclient.discovery import build
    service = build('calendar', 'v3', credentials=get_creds())
    now = datetime.utcnow().isoformat() + 'Z'
    events = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    for event in events.get('items', []):
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', '?'))
        summary = event.get('summary', 'No title')
        print(f"  {start}  {summary}")

def gmail():
    from googleapiclient.discovery import build
    service = build('gmail', 'v1', credentials=get_creds())
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
        subject = next((h['value'] for h in m.get('payload',{}).get('headers',[]) if h['name']=='Subject'), 'No subject')
        sender = next((h['value'] for h in m.get('payload',{}).get('headers',[]) if h['name']=='From'), 'Unknown')
        print(f"  {sender[:40]:40s}  {subject}")

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'calendar':
        print("📅 Upcoming events:")
        calendar()
    elif sys.argv[1] == 'gmail':
        print("📧 Recent emails:")
        gmail()
    else:
        print("Usage: gws-quick [calendar|gmail]")
