#!/usr/bin/env python3
import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

path = os.path.expanduser('/home/tom/.hermes/google_token.json')
creds = Credentials.from_authorized_user_file(path)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
msg = build('gmail', 'v1', credentials=creds).users().messages().get(
    userId='me', id='1a05ae86d051b3f6', format='metadata',
    metadataHeaders=['From','To','Subject']
).execute()
headers = {h['name'].lower(): h['value'] for h in msg.get('payload',{}).get('headers',[])}
print(json.dumps({'labelIds': msg.get('labelIds', []), **headers}, indent=2))
