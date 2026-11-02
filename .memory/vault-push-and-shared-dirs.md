---
name: vault-push-and-shared-dirs
description: "This session user (ccw-ton08) can't push the vault or share /tmp/claude-1001 with codex-pve; how to work around"
metadata:
  node_type: memory
  type: reference
  originSessionId: ec38a60f-14bd-45d9-b1b4-a1ab127d4ef3
  modified: 2026-10-24T20:13:30.266Z
---

- Session runs as `ccw-ton08`; the vault's `origin` (ssh://…<forgejo-host>) rejects this user. Push works as `sudo -u codex-pve -H git push origin main` (codex-pve has an HTTP insteadOf + credential helper to <forgejo-host>:3000). Obsidian Publish CLI also only as codex-pve: `sudo -u codex-pve -H /home/codex-pve/.local/bin/obsidian vault=Privacy …` — inside a `while read` loop add `</dev/null` or sudo eats stdin.
- The task-file dir `/home/codex-pve/.agent-todo/` is codex-pve-only: read/write via `sudo -u codex-pve`.
- `/tmp/claude-1001` gets its ACL mask reset to 700, so codex-pve loses access to the scratchpad mid-session; for files codex-pve must read (e.g. running render.py/Chromium as codex-pve) use `/var/tmp/zapret-site-patch` (ACL for both users).
- Chart rendering: codex-pve has Chromium `chromium_headless_shell-1243`; ccw-ton08 has only the older 1194 build (`chrome-linux/headless_shell` layout). Since 2026-11-02 render.py also looks for that layout, so it renders as ccw-ton08 too; before that it fell back to `/usr/bin/chromium` and failed with "Missing X server or $DISPLAY".

Related: [[wiki-domain-wiki2]]
