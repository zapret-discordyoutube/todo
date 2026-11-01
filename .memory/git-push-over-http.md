---
name: git-push-over-http
description: Forgejo SSH is disabled since 2026-10-20; every repo pushes over HTTP via a global url rewrite and a credential helper
metadata:
  type: project
---

Forgejo SSH has been off since 2026-10-20 (another session set `DISABLE_SSH` when the sites moved behind Cloudflare). The user explicitly allowed whatever it takes to push and release, so on 2026-10-20 I set up a permanent path: `~/.gitconfig` rewrites `ssh://git@<forgejo-host> (internal Forgejo address, see `~/pve-admin/servers.md`):22/`, `git@<forgejo-host>:` and `ssh://git@<old git name>:2222/` to `http://<forgejo-host>:3000/`, and `credential.http://<forgejo-host>:3000.helper` points at `~/.config/forgejo/git-credential-forgejo-local`, which reads `~/.config/forgejo/claude-admin-token` (user loop-uh, admin) without printing it.

**Why:** the old helper `git-credential-zastogram` uses `release-token`, which has no write scope on zapretgui, so pushes returned 403.

**How to apply:** plain `git push` works in zapretgui, private_zapretgui, the Privacy vault and zapret-dns. Never re-enable SSH, never put a token into a remote URL or a log. The Dev release goes through the `CodexZapretRelease` task on win10; see [[publish-finished-articles-without-asking]] for the vault push rule.
