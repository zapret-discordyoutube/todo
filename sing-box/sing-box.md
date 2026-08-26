---
date: 2026-08-20
tags:
  - sing-box
  - proxy
  - обзор-раздела
aliases:
  - sing-box раздел
  - sing-box-extended обзор
  - синг-бокс что это
description: "Раздел о прокси-платформе sing-box и форке sing-box-extended: обзор форка, архитектура, происхождение кода протоколов и хардкод-константы."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/sing-box/sing-box](https://wiki.zapret.moe/sing-box/sing-box)

# 📦 sing-box и sing-box-extended — раздел

> [!info] О чём раздел
> Заметки об универсальной прокси-платформе **sing-box** и её форке **sing-box-extended** (от разработчика shtorm-7) с десятками дополнительных протоколов. Разбор ведётся по исходному коду — от обзора форка до устройства wire-протоколов.

## Заметки раздела

Порядок — от знакомства к глубоким деталям:

- [[sing-box/sing-box-extended|sing-box-extended — форк с расширенными функциями]] — обзор: что добавлено относительно upstream sing-box и зачем.
- [[sing-box/architecture|Архитектура sing-box-extended]] — как форк устроен изнутри.
- [[sing-box/protocols-origin|Откуда в sing-box код протоколов]] — своя реализация или копия Xray: есть ли вообще разница.
- [[sing-box/wire-protocol-explained|Что такое «wire-протокол»]] — объяснение с нуля: почему один протокол реализуют дважды и что такое формат «на проводе».
- [[sing-box/hardcoded-defaults|Хардкод-константы и дефолты]] — справочник значений, зашитых в исходники: порты, таймауты, размеры буферов.

## 📚 См. также

- [[xray/xray|Раздел Xray]] — соседнее прокси-ядро, у которого sing-box перенимает протоколы
- [[Clash/00-overview|Раздел Clash]] — клиентская маршрутизация, где sing-box часто работает сервером

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/sing-box/sing-box.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
