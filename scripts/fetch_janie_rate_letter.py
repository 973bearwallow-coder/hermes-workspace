#!/usr/bin/env python3
import base64
import json
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

MESSAGE_ID = os.environ.get("GMAIL_MESSAGE_ID", "1a05aa9ab7bd9933")
TOKEN = Path(os.environ.get(
    "GOOGLE_WORKSPACE_TOKEN_PATH",
    str(Path.home() / ".hermes/google_token_tom.json"),
))
OUT = Path(os.environ.get(
    "GMAIL_ATTACHMENT_OUT",
    str(Path.home() / "hermes-workspace/inbox/janie-rate-adjustment"),
))
OUT.mkdir(parents=True, exist_ok=True)

creds = Credentials.from_authorized_user_file(str(TOKEN))
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
service = build("gmail", "v1", credentials=creds)
message = service.users().messages().get(userId="me", id=MESSAGE_ID, format="full").execute()

attachments = []
def walk(part):
    filename = part.get("filename", "")
    body = part.get("body", {})
    attachment_id = body.get("attachmentId")
    if filename and attachment_id:
        data = service.users().messages().attachments().get(
            userId="me", messageId=MESSAGE_ID, id=attachment_id
        ).execute()["data"]
        raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
        safe = Path(filename).name
        target = OUT / safe
        target.write_bytes(raw)
        attachments.append({"filename": safe, "mimeType": part.get("mimeType"), "size": len(raw), "path": str(target)})
    for child in part.get("parts", []) or []:
        walk(child)

walk(message.get("payload", {}))
print(json.dumps({"message_id": MESSAGE_ID, "attachments": attachments}, indent=2))
