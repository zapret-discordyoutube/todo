---
name: publish-deeplink-404-2026-11-05
description: "Obsidian Publish mirror /zapret/<path> redirected to /404 on 2026-11-05 although site, files and subscription were fine; how it was diagnosed"
metadata:
  node_type: memory
  type: project
  originSessionId: 76e4f65d-9ab5-4d50-a6dd-bbf38f6deb10
  modified: 2026-11-05T21:21:28.033Z
---

On 2026-11-05 every direct request to `publish.obsidian.md/zapret/<path>` (even nonexistent paths) answered 301 → `/404`, while bare `/zapret` loaded the SPA and in-app navigation worked. Other Publish sites (`/hub/...`) returned 200 for deep links.

Checked and healthy: `publish:site`, `publish:list total` (1042), the server index at `publish-01.obsidian.md/cache/<siteId>`, `apiOptions()`, account API `publish/list` and `api/site` (one site, id matches `.obsidian/publish.json`), and the owner's screenshot of the Publish plan (Active, renews 2027-10-07). Re-binding the slug via `publish.obsidian.md/api/slug` did nothing. The owner concluded it is a bug on Obsidian's side.

**Why:** a 404 on the mirror looks like the subscription-expiry failure in the `vault-note` skill, but here the site, files and plan were all intact, so recreating the site would have been wrong.

**How to apply:** if the mirror 404s, first compare deep link vs bare `/zapret`, check `publish:site` and the account API; recreate the site only when `publish/list` returns no sites. Do not run `publish:add changed` blindly: the working tree holds untracked `gptimage/` and drafts. Task file: `~/.agent-todo/Privacy/2026-11-05-publish-mirror-deeplink-404.md`. See [[vault-push-and-shared-dirs]].

Update 2026-11-19: still 404 after 13 days; support ticket #155692 got only the auto-reply, and support's first answer was "check your local settings". Three independent networks (this host, the owner's browser, the US2-7 server with its own IP and no VPN) all get the same `301 -> /404`, and the same site under another slug (`zapretwiki`, tested for ~30 s, then reverted) answered 200 on deep links, so the fault follows the slug `zapret`, not local settings. The four files that failed `publish:add` with `Failed to fetch` published fine on a later retry (transient, not an attachment). Deploy flow since 2026-11-07: push to Forgejo, then the wiki container's `wiki-autopull` (every minute) and `wiki-rebuild.path` rebuild the wiki; the Publish CLI (headless Obsidian) still runs on this host.
