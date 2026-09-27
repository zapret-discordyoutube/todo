---
title: Zapret 2 (Запрет GUI) — обход блокировок Discord и YouTube
tags:
link:
aliases:
  - index
  - Запрет ГУИ
  - Zapret GUI
  - Скачать Запрет
  - Запрет 2 обход блокировок
  - Обход блокировки Дискорда и Ютуба
img:
description: "Zapret 2 (Запрет GUI) — бесплатный обход блокировок Discord и YouTube на Windows: скачивание, настройка, 200+ стратегий, FAQ и помощь сообщества."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/Zapret/home](https://wiki.zapret.moe/Zapret/home)

**Zapret Wiki** — открытая база знаний по [[Zapret2|Zapret 2]] и Запрет GUI, одному из самых популярных GUI-лаунчеров для обхода блокировок YouTube и Discord, а также по всему, что с ним связано, и вообще по обходу блокировок в интернете (*особенно в рунете*). Мы собрали и продолжаем собирать свыше 200 стратегий обхода блокировок для Discord и YouTube.

## С чего начать

- [[download|Как скачать и установить]] — пять способов скачать Запрет GUI для Windows 10+: Telegram-канал, бот, релизы в Forgejo и сборка из исходников.
- [[Zapret/about|Что это такое]] — VPN, Tor и обход DPI простыми словами: чем они отличаются и что будет при изоляции рунета.
- [[guide|Как настроить под себя]] — гайд для новичков: выбор пресета, перебор стратегий и тонкая подстройка.
- [[faq|FAQ — частые вопросы]] — как добавить сайт в hostlist, почему не работают YouTube и Discord, чем мешают AdGuard и Яндекс DNS.
- [[zapret_not_working|Не работает!]] — типы блокировок, конфликты с антивирусом и VPN, что проверить по шагам.
- [[🐳 Win 7 и 8|Windows 7 и 8]] — консольные версии с bat-стратегиями вместо GUI и ручной автозапуск.
- [[virus|О вирусах]] — почему антивирусы ругаются на Zapret и WinDivert и как отличить подделку.
- [[Манифест Zapret|Манифест Zapret]] — доступ к информации как базовое право, открытый код и независимость.
- [[changelog-21.0.0-dev-june-2026|Changelog 21.0.0]] — что нового в dev-сборках Запрет GUI 21.0.0.
- [[premium|Поддержать проект]] — Zapret Premium и Zapret VPN: подписка, на которую живёт проект.

## Что умеет Запрет GUI

Программа даёт широкие возможности для автоматического запуска как GUI, так и отдельных `bat`-стратегий (*в режимах Запрет 1 и [[Zapret2|Запрет 2]]*), а также для тонкой настройки любой её части: например, списками доменов для всех стратегий можно управлять прямо из GUI.

- Обходит блокировки YouTube и Discord через ядро `winws.exe`, а также ядро `winws2.exe` — подробнее про [[youtube|блокировку YouTube]].
- Быстро переключается между режимами Запрет 1 и Запрет 2.
- Открывает ChatGPT, Google Gemini, Notion и другие ресурсы, недоступные из России, через файл `hosts`.
- Запускает оркестратор — автоматический перебор стратегий в режиме live.
- Прописывает свои DNS-серверы против подмены DNS провайдером.
- Блокирует установку национального мессенджера `Max`.

![[Pasted image 20260714003302.png|Окно Запрет GUI: статус обхода, пресеты и настройки программы]]

> [!TIP]
> Относитесь к программе как к аптечке. По умолчанию Вам доступен стандартный набор возможностей, но Вы можете попробовать другие лекарства, которые кому-то помогают сильнее, у кого-то не вызывают аллергию, у кого-то вызывают аллергию (_но это не значит что препарат опасен, он просто Вам не подходит_) а кому-то бесполезны и ничего не делают. Вы также можете добавлять свои лекарства в эту аптечку.

## Если ни одна стратегия не подошла

- [[Blockcheck|Blockcheck]] — автоперебор всех стратегий, когда сайт не открывается ни с одной стоковой.
- [[Создание своей категории|Как собрать свои адреса]] — домены, IP и порты для игр, приложений и сайтов.
- [[profile|Что такое профиль]] — чем профиль отличается от пресета и как фильтры выбирают трафик.
- [[youtube|Блокировка YouTube]] — три области обхода: сайт, QUIC и GoogleVideo в плеере.

## Сообщество и поддержка

Есть вопросы? Задайте их [в Forgejo](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/issues/new), в [группе помощи в Telegram](https://telegram.me/youtubenotwork) или [в Discord](https://discord.gg/kkcBDG2uws) — отвечают живые люди. Вы можете помочь вики, если запишетесь в [[Волонтёры|волонтёры]], или написать статью сами: сделайте форк [репозитория вики](https://git.zapret.moe/zapretdiscordyoutube/todo) и пришлите пулл-реквест.

- [Основной канал в Telegram](https://telegram.me/bypassblock) — новости и свежие сборки Zapret.
- [VPN-канал в Telegram](https://telegram.me/vpndiscordyooutube) — всё про наш VPN.
- [Личный канал nerdpapers](https://t.me/nerdpapers) — канал автора проекта.
- [YouTube-канал](https://www.youtube.com/channel/UCyEOuaB8EUwn1aU8a73_EWQ/) — видео и разборы.
- [Сообщество в Discord](https://discord.com/invite/kkcBDG2uws) — общий чат проекта.
- [Вопросы и баги в Forgejo](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/issues/new/choose) — задача не потеряется в чате.
- [Поддержать донатом](https://telegram.me/zapretvpns_bot) — через Telegram-бота проекта.
- [Канал изменений вики](https://telegram.me/approundmap) — уведомления обо всех правках статей.

## Проект в цифрах

Запрет GUI разрабатывается открыто на собственном Git-сервере [git.zapret.moe](https://git.zapret.moe/): там [исходники](https://git.zapret.moe/zapretdiscordyoutube/zapretgui), [релизы](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/releases), [задачи](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/issues), [проверки в Actions](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/actions) и [история коммитов](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/commits/branch/main). Лицензия — [MIT](https://git.zapret.moe/zapretdiscordyoutube/zapretgui/src/branch/main/docs/LICENSE), а к каждому релизу прилагается SHA256.

<p align="center">
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/stars"><img alt="Звёзды в Forgejo" src="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/badges/stars.svg"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/releases"><img alt="Последний релиз в Forgejo" src="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/badges/release.svg"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/issues"><img alt="Открытые задачи в Forgejo" src="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/badges/issues.svg"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/actions"><img alt="Проверка исходников в Forgejo Actions" src="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/actions/workflows/source-guards.yml/badge.svg"></a>
</p>

<p align="center">
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/releases"><img alt="Загрузки последнего релиза" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgit.zapret.moe%2Fapi%2Fv1%2Frepos%2Fzapretdiscordyoutube%2Fzapretgui%2Freleases%3Flimit%3D1&query=%24%5B0%5D.assets%5B0%5D.download_count&label=%D0%B7%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B8%20%D1%80%D0%B5%D0%BB%D0%B8%D0%B7%D0%B0&color=45cfff"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/commits/branch/main"><img alt="Последний коммит" src="https://img.shields.io/gitea/last-commit/zapretdiscordyoutube/zapretgui?gitea_url=https%3A%2F%2Fgit.zapret.moe&label=последний%20коммит&color=2e7bff"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/src/branch/main/docs/LICENSE"><img alt="Лицензия MIT" src="https://img.shields.io/badge/лицензия-MIT-45cfff"></a>
  <img alt="Python 3" src="https://img.shields.io/badge/python-3-3776AB?logo=python&logoColor=white">
  <img alt="Windows 10 и 11" src="https://img.shields.io/badge/windows-10%20%C2%B7%2011-2e7bff">
  <a href="https://git.zapret.moe/"><img alt="Свой Git-сервер" src="https://img.shields.io/badge/self--hosted-git.zapret.moe-a980ff?logo=forgejo&logoColor=white"></a>
  <a href="https://git.zapret.moe/zapretdiscordyoutube/zapretgui/releases"><img alt="SHA256 в каждом релизе" src="https://img.shields.io/badge/sha256-в%20каждом%20релизе-2ea043"></a>
</p>

## Вики дружит с ИИ

Все статьи открыты — их можно скармливать ИИ-ассистентам и обучать на них модели:

- у каждой страницы есть кнопка **«🤖 Скопировать как Markdown»** (под датой), а исходник доступен по адресу страницы с расширением `.md` — например, [Zapret2/guide.md](https://wiki.zapret.moe/Zapret2/guide.md);
- [llms.txt](https://wiki.zapret.moe/llms.txt) — каталог всех статей вики со ссылками на Markdown-исходники (стандарт [llmstxt.org](https://llmstxt.org) для ИИ-краулеров);
- [llms-full.txt](https://wiki.zapret.moe/llms-full.txt) — вся вики одним файлом (~5 МБ), удобно загрузить в контекст модели целиком;
- [zip всего репозитория](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip) — исходники со всей историей в [Forgejo](https://git.zapret.moe/zapretdiscordyoutube/todo).

## Другие полезные сервисы и VPN

Подборка сервисов и VPN для обхода блокировок собрана в репозитории [CensorNet на GitHub](https://github.com/awesome-windows11/CensorNet).

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/Zapret/home.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
