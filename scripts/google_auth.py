#!/usr/bin/env python3
"""Google OAuth re-auth for gmail/calendar/drive using existing client_secret.json"""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = '/home/tom/Downloads/atlas google info/client_secret_6585546189-qf7e2fpe47hd4jqmlb7rtldoocoq5hbh.apps.googleusercontent.com.json'
TOKEN_FILE = '/home/tom/.hermes/google/token.pickle'

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]

os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

print("Starting OAuth flow...")
print("A browser window should open. Log in with 973bearwallow@gmail.com and approve the scopes.")
print()

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

with open(TOKEN_FILE, 'wb') as f:
    pickle.dump(credentials, f)

print(f"\n✅ Auth successful!")
print(f"   Token saved to: {TOKEN_FILE}")
print(f"   Client ID: {credentials.client_id}")
print(f"   Scopes: {credentials.scopes}")
print(f"   Expiry: {credentials.expiry}")
