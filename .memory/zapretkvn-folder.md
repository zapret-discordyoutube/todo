---
name: zapretkvn-folder
description: Всё про приложение Zapret KVN лежит в vault в папке ZapretKVN/; что там, что владелица хочет от статьи (обзор для новичков, лёгкая реклама бота), и что не трогать
metadata:
  type: project
---

С 2026-11-04 материалы о приложении Zapret KVN живут в папке `ZapretKVN/`: обзор `ZapretKVN.md`, статья `zapret-kvn-windows.md` (обзор «Zapret KVN и Zapret 2 GUI: что это, чем отличаются, что выбрать»), `android.md` (переехал из `premium/android.md`, старый путь оставлен алиасом) и `attachments/` со скриншотами `kvn-*` и диаграммами.

**Why:** владелица велела создать папку и перенести туда всё про приложение. Сначала я понял «отключение KVN и GUI» буквально и написал про крестик, трей и выход. Она поправила: «disabling» было сбоем перевода, нужен подробный обзор для новичков, что такое Zapret KVN и что такое Zapret 2 GUI и чем они отличаются, без инструкций «как включить или выключить». «GUI» значит Zapret 2 GUI, отдельную программу. Статья слегка рекламная: в ней есть раздел про Telegram-бот @zapretvpns_bot.

**How to apply:** адрес `ZapretKVN/zapret-kvn-windows` менять нельзя: на него ведёт ссылка «Подробнее в статье» в обучении Zapret KVN 0.8.61+. Новые материалы про KVN кладите в `ZapretKVN/` и добавляйте в обзор. Ссылки пишите как `[[ZapretKVN/android]]`. Факты о программах берите из README обеих (Zapret 2 GUI 21.1.7.228, Zapret KVN 0.8.60) и из обучения в `xray_fluent/ui/tour/steps.py`. Цены бота дают с отсылкой на гайд `Zapret/premium`, они меняются. См. [[article-deliverables]] и [[gptimage-prompts]].
