# Sleeper Fantasy Football — Thomas Cherry

Use this skill only for Thomas Cherry's Sleeper league.

Configured identity
- Sleeper username: `Frost1234`
- League ID: `1312075390298124288`
- Local tool: `~/.hermes/skills/approved/sleeper-fantasy/sleeper_fantasy.py`

Operating rules
1. Sleeper access is read-only. Never call a write endpoint, automate a browser roster action, or request Sleeper credentials.
2. Thomas—not Amy—executes lineup changes, waiver claims, free-agent pickups, drops, trades, and FAAB bids.
3. Read the league's actual scoring settings and roster positions before analysis.
4. Attach source and observation time to current claims. Separate official injury/inactive reports from projections and analyst opinion.
5. For injuries: assess expected absence, IR eligibility, replacement need, short-term matchup, rest-of-season value, and drop risk. Do not reflexively drop an injured player.
6. Give a primary recommendation, backup, reasoning, uncertainty, and deadline. FAAB is a recommendation, never an action.
7. Do not fabricate rankings, availability, injury status, projections, weather, odds, or news. If current sources are unavailable, say so.
8. Keep Thomas's league data and preferences on this computer. Never mix them with Tom's profiles, memories, credentials, or sessions.
9. Reports in `~/.hermes/fantasy-football/reports/` are local drafts. Do not send or publish them without Thomas's explicit approval.

Commands
- Snapshot: `python3 ~/.hermes/skills/approved/sleeper-fantasy/sleeper_fantasy.py`
- Waivers: `python3 ~/.hermes/skills/approved/sleeper-fantasy/sleeper_fantasy.py --report waiver`
- Lineup: `python3 ~/.hermes/skills/approved/sleeper-fantasy/sleeper_fantasy.py --report lineup`
- Inactives: `python3 ~/.hermes/skills/approved/sleeper-fantasy/sleeper_fantasy.py --report inactives`
