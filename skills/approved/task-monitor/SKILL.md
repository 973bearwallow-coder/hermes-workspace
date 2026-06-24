# Task Monitor Skill

## Purpose
For any long-running task (>5 min), set up a watchdog sub-bot that:
1. Checks progress at regular intervals
2. **Validates output quality** — not just counting files but spot-checking content
3. **Self-checks** — the watchdog itself verifies its own reports are accurate
4. Alerts Tom if stalled or quality drops
5. Auto-restarts if possible

## When to Use
- Batch processing (transcription, downloads, data processing)
- Multi-step workflows with >3 steps
- Any background task that takes >5 minutes
- Cron jobs that run for extended periods

## Protocol

### 1. At Task Start
Create a progress marker file:
```
echo "STARTED: $(date)" > ~/task_name/progress.log
echo "TOTAL: N items" >> ~/task_name/progress.log
```

### 2. Create a Watchdog Cron (Sub-Bot)
```
Schedule: every 15m (or appropriate interval)
```

The watchdog is a **sub-bot** — it runs independently, checks progress, and delivers reports to Tom. It should be self-contained and self-checking.

### 3. Quality Checks (Critical)
Don't just count files — verify:
- **Non-empty**: Output files have content (>0 bytes)
- **Correct format**: Expected structure (headers, timestamps, etc.)
- **No error patterns**: No "ERROR", "Traceback", repeated garbage
- **Spot-check**: Read first/last few lines of latest output — does it look real?
- **Self-check**: The watchdog should verify its own counts by re-checking, not just trusting the last report

### 4. Watchdog Self-Verification
The watchdog should:
- Re-count files each run (don't assume last count was accurate)
- Spot-check at least 1 output file per run for content quality
- Compare current progress to last report — flag if numbers don't add up
- If it detects its own previous report was wrong, say so and correct it

### 5. Progress Report Format
```
📊 [Task Name] Monitor
Status: RUNNING | STALLED | COMPLETE
Progress: X / N (XX%)
Rate: ~Y items/min
ETA: ~Z minutes
Quality: ✅ OK | ⚠️ ISSUE (describe)
Last activity: [timestamp]
```

### 6. Completion
When task finishes:
- Report final stats to Tom
- Remove the watchdog cron
- Archive progress log

## Example Watchdog Prompt Template
```
You are a watchdog for [TASK_NAME]. Check status and quality.

1. Process running: [check command]
2. Progress: [count command — re-count, don't trust previous reports]
3. Quality: [spot-check command — read actual file content]
4. Log tail: [log location]
5. Self-check: Compare your count to the last report. If different, explain why.

Report: Status, progress %, rate, quality check, any issues.
If stalled (no process + not complete): [restart command].
If complete: report final stats.
Keep it concise — 5-8 lines max.
```

## Key Rules
- **Always** set up monitoring before starting a long task
- **Never** fire-and-forget a batch job
- **Quality > quantity** — 10 good outputs beat 100 garbage ones
- **Self-checking** — watchdog verifies its own accuracy each run
- **Report rate** — every 15 min for tasks <2 hours, every 30 min for longer
- **Auto-restart** — if safe to do so, watchdog should restart stalled tasks
- **Clean up** — remove watchdog cron when task completes
