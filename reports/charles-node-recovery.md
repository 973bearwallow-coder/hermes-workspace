# Charles OpenClaw node recovery

Date: 2026-09-13 EDT
Host: `Charles`
Outcome: **Recovered**

## Fault

`openclaw-node.service` repeatedly exited with `listeners.add is not a function` while `openclaw-gateway.service`, its `http://127.0.0.1:18789/health` endpoint, and `hermes-gateway.service` remained healthy.

The production node executable is OpenClaw `2026.5.27` (`/home/tom/.npm-global/lib/node_modules/openclaw`). Its agent-event singleton uses `Symbol.for("openclaw.agentEvents.state")` with `listeners: new Set()` and registers through `.add()`.

Three auto-loaded production plugins had nested `openclaw` peer symlinks pointing into an isolated testbed install:

- `@openclaw/google-meet/node_modules/openclaw`
- `@openclaw/googlechat/node_modules/openclaw`
- `@openclaw/whatsapp/node_modules/openclaw`

All resolved to `/home/tom/hermes-live-testbed/sandboxes/openclaw-official-2026.9.4/node_modules/openclaw`. OpenClaw `2026.9.4` initializes the same process-global symbol with `listeners: new Map()` plus `runListeners`, `nextListenerId`, `listenerRevision`, `auditListeners`, and lifecycle fields. Runtime instrumentation confirmed the crashing 5.27 node saw that 9.4-shaped state and a `Map`; its 5.27 listener helper then called `.add()`, causing the exception.

## Repair

Repointed only the three auto-loaded plugins' nested peer symlinks to the matching production OpenClaw package:

`/home/tom/.npm-global/lib/node_modules/openclaw`

No package upgrade, configuration rewrite, gateway restart, Hermes restart, account/SSH/boot change, or sandbox-file modification was performed. Temporary runtime instrumentation was removed; no `DEBUG-charles-node-agent-events` marker remains in the production bundle.

Rollback for each link is to restore its former target:

`/home/tom/hermes-live-testbed/sandboxes/openclaw-official-2026.9.4/node_modules/openclaw`

## Verification

At 22:35:19 EDT the repaired node started. After more than one minute:

- `openclaw-node.service`: `active/running`, PID `3675547`, `NRestarts=0`, `Result=success`
- Node journal since repair: no exception or restart
- Gateway log at 22:35:24: `device pairing auto-approved ... role=node`, proving the node reached and authenticated to the live gateway
- Gateway health: `{"ok":true,"status":"live"}`
- `openclaw-gateway.service`: active
- `hermes-gateway.service`: active

## Remaining issues / follow-up

- `plugins.allow` is empty, so non-bundled plugins auto-load. This warning predates the repair; no config rewrite was made under the minimal-repair constraint.
- An unused/unconfigured `@openclaw/discord` package still has a peer symlink to the 2026.9.4 sandbox. It was not among the plugins discovered by the node and was intentionally left untouched. If Discord is later enabled, align or remove that package first.
- `openclaw nodes status` is blocked by pre-existing schema validation errors (`meta`, `agents`, and `talk.realtime`) in the newer config when parsed by the 2026.5.27 CLI. I did not run the suggested destructive `doctor --fix`. Service stability and the gateway's live node-pairing event provide the connection verification instead.
- The unit description says v2026.5.7 while the invoked package reports 2026.5.27; this label is stale but operationally harmless and was not changed.
