# Carson Hermes Bot Setup Plan — Linux Mint

## Goal
Set up a fully-capable Hermes bot for Carson on his Linux Mint machine. Minimize what Carson has to do manually — Atlas does the heavy lifting via SSH.

## Pre-Trip Prep (Atlas Does This Before the Trip)

### 1. Generate SSH Key Pair
- Create a dedicated key for Carson's machine
- Prepare a script that copies the public key to Carson's machine
- Test SSH connectivity

### 2. Automated Install Script
Create a single script Carson can run with one command:
```bash
curl -sSL https://hermes-agent.nousresearch.com/install.sh | bash
```
Or a local script that:
- Installs system dependencies (python3.11, git, curl, ffmpeg, etc.)
- Creates a Python venv
- Installs hermes-agent
- Runs initial setup wizard non-interactively
- Configures Telegram bot token
- Sets up basic skills

### 3. Prepare Config Templates
- Pre-configured `config.yaml` with model provider settings
- Telegram bot token placeholder
- Google OAuth client_secret.json (if Carson has a Google account)
- Starter pack of useful skills

### 4. Carson's One-Page Cheat Sheet
Simple instructions for Carson:
- How to talk to his bot on Telegram
- How to restart the service if needed
- How to check status
- Who to call (you) if something breaks

## Day-Of Setup (Atlas Does Everything via SSH)

### Phase 1: Initial Access (5 min)
1. SSH into Carson's machine
2. Verify OS version and installed packages
3. Copy SSH key for passwordless access going forward

### Phase 2: Base Install (15 min)
1. Run automated install script
2. Verify hermes-agent is installed and running
3. Configure as systemd service for auto-start

### Phase 3: Telegram Setup (10 min)
1. Help Carson create a Telegram bot via BotFather (he does this part)
2. Configure the bot token in Hermes
3. Test basic chat with Carson's bot

### Phase 4: Google Integration (15 min)
1. Set up Google Cloud project (or reuse existing)
2. Configure OAuth consent screen
3. Run auth flow for Gmail/Calendar/Drive
4. Test email and calendar access

### Phase 5: Useful Skills & Features (15 min)
1. Install commonly useful skills
2. Set up basic cron jobs (daily briefing, etc.)
3. Configure email sending from his bot's account

### Phase 6: Handoff (10 min)
1. Show Carson the Telegram bot working
2. Walk him through the cheat sheet
3. Leave the cheat sheet on his Desktop
4. Verify he can restart the service himself

## Key Principles
- **Carson does as little as possible** — ideally just: create Telegram bot, approve OAuth, and chat
- **Atlas does everything else** via SSH
- **Keep it simple** — don't over-engineer. Core chat + email is enough for day 1
- **Document everything** so Carson isn't stuck if something breaks

## Questions for Carson (Before the Trip)
1. What's his machine's hostname or IP address?
2. What's his Linux Mint username?
3. Does he have a Google account for the bot? (or should we create one?)
4. What's his main use case? (personal assistant, business, dev work?)
5. Does he have a Telegram account already?
