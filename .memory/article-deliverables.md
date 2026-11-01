---
name: article-deliverables
description: "Every new vault article = article + Telegram post + cover prompt; publish right away, set the cover when she sends it; ✔ DONE only after the cover"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c655fef4-7ed0-4895-af65-85b257e77724
  modified: 2026-10-24T22:57:12.262Z
---

User decision of 2026-10-24: every new article comes with a Telegram post (code block + Artifact page, per vault-note) and a cover prompt (Zapret-tan / RKN-tan, see [[gptimage-prompts]]), both produced without being asked. The article is published right away (commit, push, mirror) without the cover (decision of 2026-10-31, replaced the 2026-10-24 "cover first"); the owner generates the cover herself and sends it to the chat.

Until the cover arrives, the task stays open: no `✔ DONE`, and the task file has an item "You: generate the cover from the prompt and send it". When it arrives, put it as the article header (vault-image: embed + `image:` frontmatter), save a copy next to the prompt in `gptimage/`, then commit, push and upload to the Obsidian Publish mirror.

**Why:** the user wants every article to ship as a complete set with its own cover, and generating the image is done by her, not by Claude.

**How to apply:** publish without waiting, add `image:` and the header embed in a separate commit when the cover arrives; "finished" (✔ DONE) means the cover is in place. No timer is needed for the wait, because the user's message wakes the session. Written into AGENTS.md («Обложки статей»), the vault-note and vault-image skills.
