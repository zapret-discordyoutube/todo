---
name: wiki-stats-architecture
description: Как устроена статистика читателей на главной вики (журнал nginx → агрегат → компонент Quartz)
metadata:
  type: project
---

Статистика читателей на главной (запрос 2026-10-19): `scripts/wiki-stats.py` в vault читает общий журнал nginx (он общий с Forgejo, без поля host — вики узнаётся по слагам из `public/static/contentIndex.json`), отсеивает ботов, пишет `/srv/wiki-stats/stats.json` (публичный агрегат) и приватный `state.json` (хеши IP+UA с солью). Таймер `wiki-stats.timer` раз в 10 минут; nginx отдаёт `/_stats.json`; блок рисует компонент `HomeStats` в `/srv/wiki-quartz` (подключён в `quartz.layout.ts`, `Zapret/home.md` не тронут). Часовой пояс журнала +03:00, хост сам в EDT.

**Why:** главная не редактируется агентом, а цифры нужно обновлять без коммитов и пересборки сайта.
**How to apply:** менять метрики — в `wiki-stats.py`, вид — в `HomeStats`/`homestats.*`; журнал хранится 14 дней, дальше история копится только в `state.json`. См. [[visuals-inline-not-ascii]] про общий стиль схем.
