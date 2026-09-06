from pathlib import Path
import json

base = Path('/home/tom/hermes-workspace/memory/coaching-digests')
old_digest = base / '2026-08-05-to-2026-09-04.md'
new_digest = base / '2026-08-05-to-2026-09-05.md'
state_path = Path('/home/tom/.hermes/data/coaching_review_state.json')

text = old_digest.read_text()

new_session = '''### 2026-09-05 — tl;dv locked Guild Spark reminder
Source: tl;dv email `80919`; meeting `6a9b5448eb8ad70013668457`.

- **Status:** Locked reminder only; the tl;dv app page hides action items and decisions behind the free-summary limit.
- **Topics:** Guild Spark session title only, recording access, locked AI notes, sign-in-gated app page.
- **Key takeaways:** **Do not infer work from the title alone**; **wait for a public share or pasted transcript before extracting decisions**; **treat the meeting ID as the durable reference**.
- **Tom lens:** keep the meeting ID for later follow-up; use the same evidence-first approach if the transcript surfaces; avoid inventing assignments from the title.
- **Tom-specific assignments:** none identified.

'''
text = text.replace('# Coaching and Community Digest — 2026-08-05 through 2026-09-04', '# Coaching and Community Digest — 2026-08-05 through 2026-09-05', 1)
text = text.replace('- This file extends the prior rolling digest (`2026-08-05-to-2026-09-03.md`) with the newest 2026-09-04 tl;dv weekly action-item report and the 2026-09-03 Boardroom Fathom recap.',
                    '- This file extends the prior rolling digest (`2026-08-05-to-2026-09-04.md`) with the newest 2026-09-05 tl;dv locked Guild Spark reminder and the 2026-09-04 tl;dv weekly action-item report.')
text = text.replace('### 2026-09-04 — tl;dv weekly action-item report', new_session + '### 2026-09-04 — tl;dv weekly action-item report', 1)
text = text.replace('- The newest transcript-backed source in this review window is the Boardroom Fathom recap for 2026-09-03 (`Fathom email 80896` / meeting `807598429`).',
                    '- The newest transcript-backed source in this review window remains the Boardroom Fathom recap for 2026-09-03 (`Fathom email 80896` / meeting `807598429`).')
text = text.replace('- No new local coaching archive files were created after 2026-09-03.',
                    '- No new local coaching archive files were created after 2026-09-03.\n- The 2026-09-05 tl;dv reminder remains locked, so no assignments or decisions were recovered from it.')
text = text.replace('- Track the September 3 Boardroom recap and the Sep 4 tl;dv weekly report for any follow-on public share or transcript.',
                    '- Track the September 3 Boardroom recap, the Sep 4 tl;dv weekly report, and the Sep 5 Guild Spark reminder for any follow-on public share or transcript.')
text = text.replace('4. Watch for any follow-on clarification from the Sep 4 tl;dv weekly report, especially around migration format and Hermes desktop-app testing.\n',
                    '4. Watch for any follow-on clarification from the Sep 4 tl;dv weekly report, especially around migration format and Hermes desktop-app testing.\n5. Watch the Sep 5 Guild Spark reminder for a public transcript/share before attempting to infer work items.\n')

new_digest.write_text(text)

state = json.loads(state_path.read_text())
state['last_reviewed'] = '2026-09-05'
state['window_end'] = '2026-09-05'
state['latest_digest'] = str(new_digest)
state['last_successful_transcript_date'] = '2026-09-03'
state['status'] = '2026-09-05 review found a locked tl;dv Guild Spark reminder plus the Sep 4 tl;dv weekly action-item report and the Sep 3 Boardroom Fathom recap; no Tom-specific assignments were identified. The tl;dv app page remains sign-in gated, so no extra decisions could be extracted there.'
state['new_session_items'] = [
    {
        'source': 'tl;dv',
        'group': 'AI Builders Guild',
        'type': 'locked reminder',
        'date': '2026-09-05',
        'id': '80919',
        'meeting_id': '6a9b5448eb8ad70013668457',
        'status': 'free AI summary limit reached; action items and decisions locked; app page sign-in gated',
    },
    {
        'source': 'tl;dv',
        'group': 'AI Profit Boardroom / AI Builders Guild',
        'type': 'weekly action-item report',
        'date': '2026-09-04',
        'id': '80890',
        'meeting_ids': ['6a9596c650b9e1001322f0a6', '6a96e8402007190014dfc922'],
        'status': 'weekly report; action items only; covers Aug 31 and Sep 1 coaching calls',
    },
    {
        'source': 'Fathom',
        'group': 'AI Profit Boardroom',
        'type': 'recap',
        'date': '2026-09-04',
        'id': '80896',
        'meeting_id': '807598429',
        'status': 'transcript-backed recap and action items for the Sep 3 coaching call',
    },
    {
        'source': 'tl;dv',
        'group': 'AI Builders Guild',
        'type': 'locked reminder',
        'date': '2026-09-03',
        'id': '80831',
        'meeting_id': '6a98b1495fab4f0013736634',
        'status': 'free AI summary limit reached; action items and decisions locked; app page sign-in gated',
    },
]
state['source_notes'] = [
    {
        'source': 'tl;dv',
        'group': 'AI Builders Guild',
        'type': 'locked reminder',
        'date': '2026-09-05',
        'email_id': '80919',
        'meeting_id': '6a9b5448eb8ad70013668457',
        'status': 'action items and decisions hidden by free-summary limit; app page sign-in gated',
    },
    {
        'source': 'tl;dv',
        'group': 'AI Profit Boardroom / AI Builders Guild',
        'type': 'weekly action-item report',
        'date': '2026-09-04',
        'email_id': '80890',
        'meeting_ids': ['6a9596c650b9e1001322f0a6', '6a96e8402007190014dfc922'],
        'status': 'action items only; covers Aug 31 and Sep 1 coaching calls',
    },
    {
        'source': 'Fathom',
        'group': 'AI Profit Boardroom',
        'type': 'recap',
        'date': '2026-09-04',
        'email_id': '80896',
        'meeting_id': '807598429',
        'status': 'transcript-backed recap and action items for the Sep 3 coaching call',
    },
    {
        'source': 'tl;dv',
        'group': 'AI Builders Guild',
        'type': 'locked reminder',
        'date': '2026-09-03',
        'email_id': '80831',
        'meeting_id': '6a98b1495fab4f0013736634',
        'status': 'AI notes locked; public transcript/share not yet available; app page sign-in gated',
    },
]
state_path.write_text(json.dumps(state, indent=2) + '\n')

print('UPDATED_DIGEST', new_digest)
print('UPDATED_STATE', state_path)
print('DIGEST_LINES', len(text.splitlines()))
print('NEW_SESSION_ITEMS', len(state['new_session_items']))
print('SOURCE_NOTES', len(state['source_notes']))
