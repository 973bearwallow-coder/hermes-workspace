#!/usr/bin/env python3
import base64
import html
import json
import os
import re
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

message_id = os.environ["GMAIL_MESSAGE_ID"]
token = Path(os.environ.get("GOOGLE_WORKSPACE_TOKEN_PATH", str(Path.home() / ".hermes/google_token_tom.json")))
creds = Credentials.from_authorized_user_file(str(token))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
service = build("gmail", "v1", credentials=creds)
message = service.users().messages().get(userId="me", id=message_id, format="full").execute()
texts = []

def decode(data):
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", "replace")

def walk(part):
    mime = part.get("mimeType", "")
    data = part.get("body", {}).get("data")
    if data and mime in {"text/plain", "text/html"}:
        text = decode(data)
        if mime == "text/html":
            text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
            text = re.sub(r"<[^>]+>", "", text)
            text = html.unescape(text)
        texts.append({"mime": mime, "text": text.strip()})
    for child in part.get("parts", []) or []:
        walk(child)

walk(message.get("payload", {}))
print(json.dumps({"id": message_id, "snippet": message.get("snippet", ""), "bodies": texts}, indent=2))
