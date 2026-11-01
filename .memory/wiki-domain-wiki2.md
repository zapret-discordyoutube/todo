---
name: wiki-domain-wiki2
description: Old wiki/git names on zapret.moe are blocked in Russia; working names come only from zapret-links; never run rewrite over history notes
metadata:
  node_type: memory
  type: project
  originSessionId: ec38a60f-14bd-45d9-b1b4-a1ab127d4ef3
  modified: 2026-10-24T20:13:24.965Z
---

Since 2026-10-24 the original wiki and git names on zapret.moe (the ones without a digit) are blocked in Russia by SNI. Since 2026-10-30 readers get mirrors with random names, and Telegram posts link through an entry page instead of our domain. The current scheme is in `Privacy/AGENTS.md` («Публикация на сайт») and in the `zapret-links` service (`~/zapret-links`: `link`, `rewrite`, `check`); the vault pre-commit hook rejects blocked names in added lines (AGENTS.md excluded).

**Why:** any working name can be blocked next; hard-coded names had to be replaced by hand each time.
**How to apply:** never write a mirror name from memory, take it from `zapret-links link wiki|git`. On a new block run `zapret-links rewrite` over vault `.md` in one commit and re-render images with the name baked into pixels. Don't run `rewrite` over history and memory notes: it mangles "X is blocked → use Y" prose; reword such notes without the literal blocked name instead. See [[vault-push-and-shared-dirs]].
