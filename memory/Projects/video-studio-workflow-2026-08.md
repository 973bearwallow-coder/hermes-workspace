# Video Studio Workflow — August 2026

## Durable decisions from recent sessions
- Treat video generation as an isolated artifact-producing workflow; do not modify production Hermes, Amy/Voicebox, or Paw Prints source files.
- Preserve every original video/audio asset and version generated renders.
- For moving faces, reject fixed face-box lip-sync or text-prompted expression changes when they cause identity drift. Prefer frame-by-frame face tracking, low-strength edits, temporal smoothing, and full-clip playback review.
- A recent Wan smile attempt was rejected after direct visual review found grotesque/uncanny expression drift. Qwen3-VL's “stable” assessment was insufficient; human playback review remains authoritative.
- Expected deliverable: verified MP4 plus settings/manifest and explicit defect notes.

## Open direction
Use a controlled face-tracked mouth/cheek expression workflow for the woman-smiling request rather than another blind Wan text-prompt attempt.
