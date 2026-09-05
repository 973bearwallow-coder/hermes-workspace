# Camera Dog Monitor

Local-only dog detection for authenticated RTSP cameras. The first registered camera is `living_room`.

- No continuous video recording.
- Only bounded dog crops and compact event metadata are retained.
- Event files are private (`0600`); directories are private (`0700`).
- Telegram alerts remain disabled pending notifier and live acceptance.
- The RTSP URL is loaded from a protected environment file and never stored in project configuration.

## Status

Inspect `/home/tom/.local/state/camera-dog-monitor/health.json`. A successful live check reports `status: ok`, `frame_received: true`, and the mapped camera/location.
