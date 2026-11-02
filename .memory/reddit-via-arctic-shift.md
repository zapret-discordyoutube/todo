---
name: reddit-via-arctic-shift
description: Reddit returns 403 to curl/WebFetch from this host; read posts and comments with exact UTC times via the Arctic Shift API
metadata:
  type: reference
---

Reddit (`www`, `old`, `api.reddit.com`, `.json`) answers 403 to curl from this host, WebFetch refuses reddit.com, and redlib mirrors are rate-limited or dead (checked 2026-11-02). The Arctic Shift archive works without a key and gives exact `created_utc`, score and permalinks:

- post: `https://arctic-shift.photon-reddit.com/api/posts/ids?ids=<post id>`
- all comments of a post: `.../api/comments/search?link_id=<post id>&limit=100`
- posts of an author in a subreddit: `.../api/posts/search?subreddit=<name>&author=<user>&limit=10`
- comment permalinks: `.../api/comments/ids?ids=<id>,<id>`; in articles link as `https://www.reddit.com/r/<sub>/comments/<post id>/comment/<comment id>/`

**Why:** on 2026-11-02 this gave the timeline for [[article-deliverables]] of `DPI/rkn-ai-vpn-ban-fake-november-2026.md`: the author admitted the error 4 minutes after posting, 9 hours before Telegram channels ran the story. Screenshots show only "11 h ago".

**How to apply:** when tracing a rumor to Reddit or quoting Reddit comments, take times and texts from Arctic Shift and convert UTC to Moscow time (+3).
