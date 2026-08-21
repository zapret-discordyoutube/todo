---
date: 2026-08-20
tags:
  - mtproxy
  - telegram
  - faketls
  - обзор-раздела
aliases:
  - MTProxy раздел
  - Прокси для Телеграма обзор
  - FakeTLS что это
  - МТПрокси не работает
---

# ✈️ MTProxy и Telegram-транспорты — раздел

> [!info] О чём раздел
> Всё о прокси для Telegram: **MTProxy** (прокси, гоняющий телеграмный протокол MTProto), маскировка **FakeTLS**, детекция со стороны ТСПУ и способы её пережить — как на сервере, так и на клиенте. Плюс альтернативный транспорт WSS (MTProto внутри WebSocket).

## Заметки раздела

**База и сервер:**

- [[mtproxy/mtproto-zig|MTProxy и mtproto.zig: что это и как пережить ТСПУ]] — вводная простым языком: что такое MTProxy, что такое FakeTLS, по каким признакам его ловит DPI.
- [[mtproxy/mtproto-zig-setup|Настройка MTProxy на mtproto.zig]] — практический runbook с объяснением каждого слоя защиты.
- [[mtproxy/faketls-relay-diagnosis|Релей или клиент: диагностика]] — когда рабочий ключ не подключается в стороннем клиенте.

**Клиентская сторона — TLS-почерк:**

- [[mtproxy/ja4-sni-client-side|Кто может менять JA4/SNI и почему обход — клиентский]] — архитектурный факт, определяющий всю борьбу с новой детекцией MTProto.
- [[mtproxy/tdlib-obf-client-side-stealth|tdlib-obf — TDLib с маскировкой под браузер]] — форк библиотеки для клиентов Telegram.
- [[mtproxy/tsrman-tg-android-faketls|tsrman/tg — форк Telegram для Android со сменой JA4]] — то же для официального Android-приложения.

**WSS-транспорт:**

- [[mtproxy/telegram-wss-transport|WSS для Telegram: MTProto внутри WebSocket]] — как устроен транспорт через веб-релеи Telegram.
- [[mtproxy/telegram-wss-limits|Ограничения WSS]] — что не работает и почему: датацентры, оговорки, границы применимости.

**WEB-прокси — новый тип прокси (август 2026):**

- [[tproxy/tproxy|WEB-прокси Telegram: трафик внутри обычного сайта]] — четвёртый тип прокси в Telegram: соединения открывает встроенный браузер приложения, а не сам мессенджер. Обзор для тех, кто видит это впервые.
- [[tproxy/tproxy-protocol|Как устроен WEB-прокси изнутри]] — техническая часть: вывод пропуска, формат кадров, кредитные окна, четыре режима доставки.
- [[tproxy/tproxy-server-setup|Установка tproxy-server]] — развёртывание своего сервера, включая интеграцию за уже работающий nginx.
- [[tproxy/tproxy-in-bot|Выдача WEB-прокси из Telegram-бота]] — раздача доступа пользователям и почему автоматическая выдача упирается в перезапуск службы.

## 📚 См. также

- [[DPI/DPI|Раздел DPI]] — как ТСПУ вообще анализирует соединения
- 🔗 [zastogram/ZaStoGram](https://git.zapret.moe/zastogram/ZaStoGram) — Telegram-клиент проекта: исходники Android-форка с WSS-транспортом и готовые сборки в релизах

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/mtproxy/mtproxy.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
