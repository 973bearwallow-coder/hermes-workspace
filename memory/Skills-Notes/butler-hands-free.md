# Butler Hands-Free Rules

- Wake word for hands-free mode: `Atlas`.
- Mic stays live until hard cap or explicit push-to-talk release.
- Idle timeout re-arms the wake word; it does not release the mic.
- On self-signed HTTPS, use Chrome for mic/getUserMedia flows; Firefox blocks the mic path.
- Any actual send/create/edit/delete/write must route through Atlas/Hermes for approval.
