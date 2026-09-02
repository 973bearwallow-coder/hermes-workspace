# Portal Authentication vs Discord Live Voice — Second Pass

Date: 2026-09-01
Host: charles
Scope: Non-destructive verification of the currently installed Hermes Agent, its Nous Portal authentication state, Discord configuration/readiness, authorization boundaries, and local voice pipeline.

## Executive result

The two surfaces are not presently interchangeable authentication mechanisms.

- **Nous Portal OAuth** authenticates Hermes to Nous subscription services (models and managed Tool Gateway).
- **Discord authorization** independently authenticates a Discord user by Discord user/role allowlists and then carries voice utterances through the same post-auth gateway boundary.
- A recognized voice or a Discord account must not inherit Portal/subscription authority by itself.

The installed implementation's internal Discord voice and authorization paths pass their focused tests. A live Discord session could not be exercised because this host has no configured Discord token, allowed users, guild, or home channel. A live authenticated Portal UI/session could not be exercised because Hermes is not logged into Nous Portal.

## Verified current state

### Nous Portal

Commands run:

- `hermes auth status nous`
- `hermes portal info`
- `hermes portal tools`

Observed:

- Nous Portal status: **not logged in**.
- Subscription and managed Tool Gateway status therefore cannot be queried.
- The browser reached the Portal landing page, but the user session was not authenticated.
- A legacy `NOUS_API_KEY` variable exists in the gateway environment, but that is not equivalent to the current Hermes Portal OAuth session.

### Discord

Observed from active gateway state and environment-name checks:

- Discord platform not configured in the active gateway.
- No Discord bot token configured.
- No Discord allowed-user list configured.
- No Discord guild/home-channel identifiers configured.
- The currently running gateway is therefore incapable of joining a live Discord voice channel.

Runtime prerequisites verified in the Hermes venv:

- `discord.py 2.7.1` installed.
- PyNaCl voice support installed.
- System Opus library loads successfully when explicitly requested.
- ffmpeg and the local STT/TTS path are available.

## Tests executed

### Discord voice flow

Focused files:

- `tests/gateway/test_discord_voice_mixer.py`
- `tests/gateway/test_discord_race_polish.py`
- `tests/gateway/test_voice_command.py`
- `tests/integration/test_voice_channel_flow.py`

Result: **87 passed, 34 deselected, 4 warnings**.

The warnings are unawaited-coroutine warnings in mocked concurrency/voice tests. They do not fail the suite, but they are worth cleaning up before treating the suite as warning-free.

### Discord authorization boundary

Focused files:

- `tests/gateway/test_discord_platform_events.py`
- `tests/gateway/test_discord_slash_auth.py`
- `tests/gateway/test_discord_component_auth.py`
- `tests/gateway/test_discord_bot_auth_bypass.py`
- `tests/gateway/test_platform_authz_scope.py`
- `tests/gateway/test_unauthorized_dm_behavior.py`

Result: **83 passed**.

This verifies the implemented boundaries for unauthorized Discord events, slash commands, components, bot-message bypass handling, platform-scoped authorization, and unauthorized DMs.

### Local speech round trip

Generated locally through Edge TTS:

> Atlas voice pipeline second pass verification.

Transcribed with local faster-whisper (`base`, CPU/int8):

> Atlas Voice Pipeline 2nd Pass Verification

Result: **successful semantic round trip**. This proves the host's core speech generation and recognition path works independently of Portal authentication and Discord transport.

## Behavioral comparison

| Concern | Nous Portal | Discord Live Voice |
|---|---|---|
| Identity being authenticated | Hermes installation/subscription session | Discord member ID and/or role |
| Current state | Logged out | Not configured |
| Voice transport | Portal/web speech UI, separate from Hermes gateway transport | Discord voice channel via bot connection |
| Authorization source | Portal OAuth/subscription | `DISCORD_ALLOWED_USERS`, role allowlists, gateway auth boundary |
| Session continuity | Hermes provider/tool credentials | Gateway conversation source bound to guild/channel/user |
| Safe default | No subscription tools while logged out | No live voice access while unconfigured |
| Primary failure mode now | Missing Portal OAuth session | Missing bot token, allowlist, guild/channel setup |

## Decision

The second pass supports a **two-layer architecture**:

1. **Transport identity**: Discord proves which Discord member supplied the utterance.
2. **Capability authorization**: Hermes separately decides which actions that identity may perform.

Portal authentication should remain a provider/subscription credential and must not automatically elevate Discord callers. Discord live voice should initially be restricted to Tom's numeric Discord user ID, a specific guild/channel, and non-sensitive capabilities. Sensitive actions should retain their existing confirmation rules.

## What remains for a true live A/B run

A live external comparison requires account/credential operations that were deliberately not guessed or bypassed:

1. Log Hermes into Nous Portal with Tom's Portal account.
2. Create/select a Discord bot, enable required intents, and install it into the intended server.
3. Configure the bot token without exposing it in logs.
4. Configure Tom's numeric Discord user ID, guild ID, and voice channel ID.
5. Run authorized-user, unauthorized-user, reconnect, stale-session, and attempted-sensitive-action scenarios.

Until those steps are completed, the software paths are verified but the external account-to-account live transport is not.
