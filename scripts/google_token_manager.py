#!/usr/bin/env python3
"""
Persistent Google OAuth token manager.
Stores tokens as JSON (not pickle) and auto-refreshes.
Run this before any Google API call to ensure fresh tokens.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configuration: map account names to token files and client secrets
ACCOUNTS = {
    'personal': {
        'token_file': '/home/tom/.hermes/google/token.json',
        'client_secret': '/home/tom/Downloads/atlas google info/client_secret_6585546189-qf7e2fpe47hd4jqmlb7rtldoocoq5hbh.apps.googleusercontent.com.json',
        'scopes': [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/drive.readonly',
        ],
    },
    'atlas': {
        'token_file': '/home/tom/.hermes/google/atlas_token.json',
        'client_secret': '/home/tom/Downloads/atlas google info/client_secret_6585546189-qf7e2fpe47hd4jqmlb7rtldoocoq5hbh.apps.googleusercontent.com.json',
        'scopes': [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/contacts.readonly',
        ],
    },
}

def load_token(token_file):
    """Load token from JSON file."""
    if os.path.exists(token_file):
        with open(token_file) as f:
            return json.load(f)
    return None

def save_token(token_file, creds):
    """Save token as JSON."""
    token_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes,
        'expiry': creds.expiry.isoformat() if creds.expiry else None,
    }
    os.makedirs(os.path.dirname(token_file), exist_ok=True)
    with open(token_file, 'w') as f:
        json.dump(token_data, f, indent=2)
    os.chmod(token_file, 0o600)  # Only owner can read

def refresh_if_needed(account_name):
    """Check token and refresh if needed. Returns fresh credentials."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    
    config = ACCOUNTS[account_name]
    token_file = config['token_file']
    
    token_data = load_token(token_file)
    
    if token_data:
        creds = Credentials(
            token=token_data['token'],
            refresh_token=token_data['refresh_token'],
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes'],
        )
        if token_data.get('expiry'):
            creds.expiry = datetime.fromisoformat(token_data['expiry'])
        
        # Refresh if expired
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                save_token(token_file, creds)
                print(f"[{account_name}] Token refreshed successfully.")
            except Exception as e:
                print(f"[{account_name}] Refresh failed: {e}")
                print(f"[{account_name}] Re-auth required!")
                creds = None
        else:
            print(f"[{account_name}] Token still valid until {creds.expiry}")
        
        return creds
    else:
        print(f"[{account_name}] No token found. Re-auth required!")
        return None

def force_reauth(account_name):
    """Force a new OAuth flow."""
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    config = ACCOUNTS[account_name]
    
    print(f"[{account_name}] Starting OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(
        config['client_secret'], config['scopes']
    )
    creds = flow.run_local_server(port=0)
    save_token(config['token_file'], creds)
    print(f"[{account_name}] Auth complete. Token saved.")
    return creds

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: google_token_manager.py <account> [refresh|reauth|status]")
        print("Accounts: personal, atlas")
        sys.exit(1)
    
    account = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else 'refresh'
    
    if account not in ACCOUNTS:
        print(f"Unknown account: {account}. Choose from: {list(ACCOUNTS.keys())}")
        sys.exit(1)
    
    if action == 'status':
        creds = refresh_if_needed(account)
        if creds:
            print(f"  Valid: {creds.valid}")
            print(f"  Expired: {creds.expired}")
            print(f"  Expiry: {creds.expiry}")
            print(f"  Has refresh_token: {creds.refresh_token is not None}")
        else:
            print("  No valid token.")
    elif action == 'refresh':
        creds = refresh_if_needed(account)
        if not creds:
            force_reauth(account)
    elif action == 'reauth':
        force_reauth(account)
    else:
        print(f"Unknown action: {action}")
