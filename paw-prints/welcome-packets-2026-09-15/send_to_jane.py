from email.message import EmailMessage
from email.policy import SMTP
from pathlib import Path
import mimetypes
import subprocess

sender = "Atlas <atlastomsai@gmail.com>"
recipient = "Jane Torok <ttorok@verizon.net>"
subject = "Re: refresh layout for Paw Prints welcome packets"
thread_id = "<1608218433.298720.1789323732536@mail.yahoo.com>"

base = Path("/home/tom/hermes-workspace/paw-prints/welcome-packets-2026-09-15/final")
attachments = [
    (base / "Paw Prints-Welcome packet - Professional Refresh.docx", "Paw Prints Welcome Packet - Professional Refresh.docx"),
    (base / "Paw Prints-Welcome packet - Professional Refresh.pdf", "Paw Prints Welcome Packet - Professional Refresh.pdf"),
    (base / "Paw Prints-Welcome packet with Pet Lodging - Professional Refresh.docx", "Paw Prints Welcome Packet with Pet Lodging - Professional Refresh.docx"),
    (base / "Paw Prints-Welcome packet with Pet Lodging - Professional Refresh.pdf", "Paw Prints Welcome Packet with Pet Lodging - Professional Refresh.pdf"),
    (base / "Paw Prints Welcome Packet - Optional Page 1-2 Suggestions.pdf", "Paw Prints Welcome Packet - Review Notes and Optional Suggestions.pdf"),
]

for path, _ in attachments:
    if not path.is_file() or path.stat().st_size == 0:
        raise FileNotFoundError(f"Missing or empty attachment: {path}")

msg = EmailMessage(policy=SMTP)
msg["From"] = sender
msg["To"] = recipient
msg["Subject"] = subject
msg["In-Reply-To"] = thread_id
msg["References"] = thread_id
msg.set_content("""Hi Jane,

Tom asked me to send you the refreshed Paw Prints welcome packets so you can choose what you like and refine them with me.

I attached both packet versions in editable Word format and review-ready PDF format. I kept your supplied contractual wording, rates, policies, signatures, and page structure unchanged while giving the forms a more consistent professional treatment based on the newer Rates & Services page.

I also attached a short review memo with optional wording suggestions for pages 1–2 and a few source-document items that need your confirmation—particularly the Standard packet's Service Agreement page and the different rates shown in the two packet versions.

Please reply with:
- which packet or design treatment you prefer;
- any colors, spacing, wording, or form areas you want adjusted;
- which Service Agreement pages belong in the Standard packet; and
- whether the Pet Lodging packet should keep its older rate sheet or use the newer rates.

You can be as specific or informal as you like. I can refine the selected version with you from there.

Best,
Atlas
""")

for path, display_name in attachments:
    mime, _ = mimetypes.guess_type(display_name)
    maintype, subtype = (mime or "application/octet-stream").split("/", 1)
    msg.add_attachment(path.read_bytes(), maintype=maintype, subtype=subtype, filename=display_name)

result = subprocess.run(
    ["himalaya", "message", "send", "--account", "atlas_mail"],
    input=msg.as_bytes(),
    check=False,
    timeout=240,
    capture_output=True,
)
print(result.stdout.decode("utf-8", "replace"))
print(result.stderr.decode("utf-8", "replace"))
raise SystemExit(result.returncode)
