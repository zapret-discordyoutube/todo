---
name: no-real-ips-in-public-repos
description: "Реальные адреса хостов (pve, фасад, egress) не записывать ни в один публичный репозиторий — только в закрытый ~/pve-admin/servers.md"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d1d838aa-66b9-436d-a242-7d88282186a5
  modified: 2026-10-17T12:03:13.101Z
---

Реальные IP серверов проекта (основной pve, его второй адрес для YouTube, узлы egress) нельзя писать в публичные репозитории — ни в код, ни в тесты, ни в AGENTS.md, ни в сообщения коммитов. В публичных местах — заглушки вида `<IP_ДЛЯ_YOUTUBE>` или документационные адреса (203.0.113.x; если нужен глобальный адрес — чужой, например 8.8.4.4). Настоящие значения — только в закрытом `~/pve-admin/servers.md`.

**Why:** сайты zapret.moe спрятаны за фасадом (адрес — в `~/pve-admin/servers.md`), чтобы жалобы шли его хостеру; 17.10.2026 публичный `yt-dlp-gui` (Forgejo + GitHub) прямо называл адрес хоста в AGENTS.md, и историю пришлось переписывать filter-repo и force-push. Публичны в том числе хранилище вики `zapretdiscordyoutube/todo` и `zapretgui`.

**How to apply:** перед коммитом в публичный репозиторий проверять дифф на IPv4-литералы; в тестах брать чужие адреса. Связано: [[publish-finished-articles-without-asking]].
