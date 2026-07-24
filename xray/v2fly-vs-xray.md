---
date: 2026-07-18
tags:
  - xray
  - v2ray
  - v2fly
  - архитектура
  - сравнение
aliases:
  - v2fly vs Xray
  - v2ray-core vs Xray-core
  - Чем отличается v2ray от xray
  - v2fly/v2ray-core
link: https://github.com/v2fly/v2ray-core
---

# ⚔️ v2fly/v2ray-core против XTLS/Xray-core: чем отличаются два ядра

> [!info] О чём заметка
> Сравнение двух прокси-ядер по исходному коду: **v2fly/v2ray-core** (продолжение оригинального V2Ray) и **XTLS/Xray-core** (форк, см. [[xray/project-x|Project X]]). Что у них общего от форка 2020 года и где они разошлись — по протоколам, транспортам, конфигу, зависимостям и модели управления. Про то, что это разные люди-авторы (RPRX vs Victoria/Darien Raymond), — в заметке [[xray/authors-v2ray-xray|Кто стоит за V2Ray и Xray]].

> [!warning] Источник данных
> Заметка составлена по прямому разбору исходников обоих репозиториев (снимок на 17–18 июля 2026: v2ray-core `v5.52.0`, Xray-core актуальный main) пятью независимыми проходами по коду и вебу. Пути к файлам и числа со временем поплывут — сверяйся с актуальными репозиториями.

## TL;DR

- **Xray — форк v2ray-core примерно 2020 года.** Это видно в коде: тела базовых файлов (например `core.go`) до сих пор почти идентичны, различается брендинг и версия. Их DI-модель, реестр протоколов и набор `features/` — общее наследие.
- **Одной строкой:** Xray — ужатое, «заточенное под обход блокировок» ядро v2ray плюс собственные антидетект-технологии; v2ray — то же наследие, но развитое в расширяемую платформу.
- **Эксклюзивы Xray:** [[xray/reality|REALITY]], [[xray/xtls-vision|XTLS-Vision]] (`flow=xtls-rprx-vision`), VLESS encryption (пост-квантовое), XHTTP (splithttp), рабочий XUDP. Ничего из этого в v2ray нет вообще.
- **Эксклюзивы v2ray:** вторая схема конфига JSONv5 и protobuf-JSON форматы, транспорты QUIC / HTTP-2 / DTLS / domain socket, протоколы Hysteria2 и vlite, платформенные приложения (подписки, REST API, менеджер инстансов, WebRTC).
- **Лицензии разные:** v2ray — MIT, Xray — MPL-2.0. Кросс-импортов между кодовыми базами нет — они полностью развязаны.
- **Управление:** v2fly — «community edition» с несколькими мейнтейнерами (ведущий — неанонимный Xiaokang Wang / Shelikhoo); Xray центрирован на одном авторе RPRX. Оба проекта живы в 2026 году.

## Общий предок: Xray — это форк v2ray

Начать надо с того, что это **не два независимых проекта, а родитель и его форк**. В отличие от пары [[sing-box/protocols-origin|sing-box и Xray]] (которые написаны с нуля и не делят кода), Xray буквально отпочковался от v2ray-core в ноябре 2020 года — README Xray прямо говорит «Xray-core v1.0.0 was forked from v2fly-core».

Родство видно в коде до сих пор. Тело пакета `core` почти идентично: `diff` файла `core.go` в обоих репозиториях показывает, что различаются лишь брендинг («V2Ray» → «Xray»), схема нумерации версий и ASCII-арт в комментарии — сама логика одна. Общими остались: механизм загрузчиков конфига (`RegisterConfigLoader`), DI-реестр протоколов (`common.RegisterConfig` / `CreateObject`), весь набор `features/` (dns, inbound, outbound, policy, routing, stats) и базовые приложения `app/` (router, dns, dispatcher, proxyman, observatory и даже одинаковый `observatory/burst`).

Проще говоря: если снять с обоих ядер «фирменные» фичи, под ними обнаружится один и тот же скелет 2020 года. Разошлись именно верхние слои — конфиг, набор протоколов и транспортов, философия развития.

## Полная родословная: Shadowsocks → V2Ray → v2fly → Xray

Здесь важно не путать два **разных** типа «наследования», которые в цепочке смешаны:

- **Идейный преемник** — новый код, написанный с нуля и лишь вдохновлённый предшественником (общего кода нет).
- **Code-fork** — прямое ответвление кодовой базы (общий код есть).

Разберём цепочку по звеньям:

1. **Shadowsocks** (2012, автор под ником clowwindy) — первый массовый инструмент обхода GFW. В августе 2015 clowwindy сообщил, что к нему пришла полиция и потребовала прекратить разработку и удалить код с GitHub (знаменитое прощальное сообщение в issue [shadowsocks-iOS #124](https://github.com/shadowsocks/shadowsocks-iOS/issues/124)). Сам Shadowsocks при этом не умер — репозитории заранее перенесли в организацию, права раздали участникам. Как и остальные в этой цепочке, clowwindy — псевдоним, настоящие имя и пол не раскрыты (англоязычная Wikipedia намеренно использует нейтральное «they»); встречающийся в прессе «he» — допущение пересказчиков, а не самоидентификация.
2. **V2Ray / Project V** (первый релиз — 18 сентября 2015, автор под псевдонимом [[xray/authors-v2ray-xray|Victoria/Darien Raymond]]) — появился буквально через месяц после ухода clowwindy, как более мощная и модульная альтернатива. **Это НЕ форк кода Shadowsocks:** у оригинального репозитория [v2ray/v2ray-core](https://github.com/v2ray/v2ray-core) нет метки «forked from», и он принёс собственный новый протокол **VMess**. Связь с Shadowsocks — **идейная** (ответ на ту же задачу в тот же момент), а не кодовая. Project V — «зонтичный» проект, V2Ray — его ядро.
3. **v2fly/v2ray-core** (2019–2020, сообщество) — после исчезновения оригинального автора (см. [[xray/authors-v2ray-xray|заметку об авторах]]) сообщество создало каноническое продолжение. **Это уже code-fork/continuation** оригинального v2ray-core — общий код.
4. **XTLS/Xray-core** (ноябрь 2020, RPRX) — **прямой code-fork** v2fly-core. README Xray прямо указывает точку ответвления: «Xray-core v1.0.0 was forked from v2fly-core **9a03cc5**». Повод для форка — лицензионный: команда v2fly сочла лицензию XTLS несовместимой и удалила XTLS из v2ray-core (версия 4.33.0), в ответ RPRX увёл разработку в свой Project X.

Диаграмма (пунктир — идейная связь, стрелка — code-fork):

```
Shadowsocks (2012, clowwindy)
   ┆  идейный преемник (новый код, протокол VMess; НЕ форк)
   ▼
V2Ray / Project V (2015, Victoria/Darien Raymond)  — написан с нуля
   │  code-fork / continuation (после исчезновения автора, 2019)
   ▼
v2fly/v2ray-core (2020, сообщество)  — сегодня это «V2Ray»
   │  code-fork от коммита 9a03cc5 (лицензионный спор об XTLS, ноя. 2020)
   ▼
XTLS/Xray-core / Project X (2020, RPRX)  — VLESS, XTLS-Vision, REALITY, XHTTP
```

Итог для вашего вопроса «V2Ray — это форк?»: **сам V2Ray — не форк, а самостоятельный проект** (идейный наследник Shadowsocks). Форками являются v2fly (от оригинального v2ray-core) и Xray (от v2fly-core). Отсюда и вся общая кодовая база, разобранная ниже.

## Протоколы и транспорты: кто на чём сфокусировался

Это самое наглядное различие. Базовый набор общий (VMess, VLESS, Trojan, Shadowsocks, Shadowsocks-2022, SOCKS, HTTP, WireGuard, freedom, dokodemo; транспорты TCP, WebSocket, gRPC, mKCP, HTTPUpgrade, TLS с ECH). А дальше приоритеты расходятся.

| Возможность | v2ray-core | Xray-core |
|---|---|---|
| [[xray/reality\|REALITY]] (маскировка под чужой сайт) | ❌ нет вообще | ✅ `transport/internet/reality` |
| [[xray/xtls-vision\|XTLS-Vision]] (`xtls-rprx-vision`) | ❌ (поле `flow` в proto есть, логики нет) | ✅ `proxy/vless/encoding` |
| VLESS encryption (пост-квантовое) | ❌ | ✅ `proxy/vless/encryption` |
| XHTTP / splithttp (транспорт через CDN) | ❌ | ✅ `transport/internet/splithttp` |
| XUDP (рабочий пакет) | ❌ (только в тесте) | ✅ `common/xudp` |
| Фрагментация/обфускация (finalmask) | ❌ | ✅ `transport/internet/finalmask` |
| QUIC (транспорт) | ✅ `transport/internet/quic` | ❌ |
| HTTP/2 (h2) транспорт | ✅ `transport/internet/http` | ❌ |
| DTLS, domain socket, tlsmirror | ✅ | ❌ |
| Hysteria | ✅ Hysteria **2** (`proxy/hysteria2`) | ✅ Hysteria **1** (`proxy/hysteria`) |
| vlite | ✅ `proxy/vlite` | ❌ |
| tun (проксирование через TUN) | ❌ | ✅ `proxy/tun` |

Обратите внимание на строку Hysteria: у ядер она **разных версий** (v2ray — Hysteria2, Xray — Hysteria1), то есть это не «одно и то же».

Вывод по этому срезу: **весь фирменный антицензурный стек XTLS — REALITY, Vision, VLESS encryption, XHTTP, XUDP — существует только в Xray**. v2ray, наоборот, шире по «классическим» и универсальным транспортам (QUIC, HTTP/2, DTLS, доменные сокеты) и несёт собственные протоколы Hysteria2 и vlite.

## Конфигурация: v2ray-платформа против ужатого Xray

Оба ядра в рантайме protobuf-first (JSON из конфига компилируется в protobuf-сообщения) и оба умеют читать JSON/TOML/YAML. Но в области конфига v2ray ушёл заметно дальше:

- **v2ray** держит **две схемы конфига**: классическую (v4) и новую **JSONv5** (`infra/conf/v5cfg`, расширения `.v5.json`), плюс protobuf-JSON форматы (`jsonpb`, `v2jsonpb`) и CLI-конвертер между всеми форматами. Отсюда и объём protobuf-схемы: **110 .proto**-файлов против 78 у Xray.
- **Xray** оставил **одну классическую схему** (наследник v4) плоским набором файлов `infra/conf/*.go`, а TOML/YAML — тонкие обёртки, конвертирующие в тот же JSON. Никаких v5/jsonpb.

То же расхождение в приложениях `app/`. v2ray нарастил «платформенные» подсистемы: подписки (`subscription`), REST API (`restfulapi`), менеджер инстансов (`instman`), постоянное хранилище, browser forwarder, WebRTC. Xray, наоборот, ядро оставил тоньше (убрал эти приложения и часть реестра расширений), но добавил своё: подсистему метрик (`app/metrics`) и geodata как компонент.

Проще говоря: **v2ray развивается как расширяемая платформа общего назначения, Xray — как узкоспециализированный инструмент обхода блокировок.** Одна и та же кодовая база 2020 года, две разные стратегии.

## Зависимости и лицензии

| | v2ray-core | Xray-core |
|---|---|---|
| Лицензия | **MIT** | **MPL-2.0** |
| Модуль | `github.com/v2fly/v2ray-core/v5` | `github.com/xtls/xray-core` |
| uTLS (маскировка TLS-почерка) | `refraction-networking/utls` | `refraction-networking/utls` (**тот же форк**) |
| quic-go | официальный `quic-go/quic-go` + `apernet/quic-go` (для Hysteria2) | только `apernet/quic-go` |
| REALITY-библиотека | — | `github.com/xtls/reality` |
| Пост-квантовая крипта | — | `cloudflare/circl` (для VLESS encryption) |
| WebRTC-стек (pion) | полный (`webrtc/v4`, `ice/v4`…) | почти нет |

Важные наблюдения: uTLS у обоих — **один и тот же форк** `refraction-networking/utls` (в отличие от sing-box, который использует форк MetaCubeX). REALITY и пост-квантовое шифрование тянут за собой отдельные зависимости, которых у v2ray нет в принципе. И главное — **кросс-импортов между кодовыми базами нет**: ни одного боевого `import` из `xtls/*` в v2ray и из `v2fly/*` в Xray (только текстовые ссылки в комментариях тестов). Родственные по происхождению, сегодня они полностью развязаны.

## Модель управления: сообщество против одного лидера

Различаются и способы управления проектами — хотя тут важно быть аккуратным с формулировками.

**v2fly** — организация-сообщество (основана 15 апреля 2019 года), самоопределение — «community-driven edition of V2Ray». Релизы подписывает коллективный ключ «V2Fly Developers», у проекта несколько мейнтейнеров. Фактический ведущий релиз-инженер — **Xiaokang Wang** (ник Shelikhoo), и это, в отличие от анонимного оригинального автора, **публичная неанонимная фигура**: по собственным данным профиля — Дублин, магистратура Trinity College Dublin; соавтор академических работ USENIX Security 2023 (о детекте полностью зашифрованного трафика GFW) и 2024 (Tor Snowflake), выступает под настоящим именем.

**Xray** — форк «Project X», центрированный на одном разработчике [[xray/authors-v2ray-xray|RPRX]] (создателе XTLS/REALITY). Проект движется его видением.

> [!note] Оговорка про «сообщество vs один автор»
> Ни у v2fly, ни у Xray в репозитории нет формального документа governance (файлов GOVERNANCE/MAINTAINERS/CODEOWNERS не найдено ни там, ни там). Поэтому противопоставление «коллективное управление v2fly ↔ один лидер Xray» — это обоснованная **интерпретация** по косвенным признакам (самоописание «community-driven», коллективные подписи-ключи у v2fly против проекта, центрированного на RPRX, у Xray), а не цитата из устава. RPRX как единоличный лидер Xray — общеизвестный факт, но в README это не кодифицировано.

## Оба проекта живы

Важно, что это **не «оригинал и заброшенный форк»**, а два параллельно развивающихся ядра. v2ray-core на июль 2026 активно релизится (последняя версия `v5.52.0` от 7 июля 2026, каденс — примерно раз в 2–4 недели, коммиты в master ежедневно). Xray-core тоже активно развивается (см. [[xray/project-x|Project X]]). Выбор между ними — это выбор между узкоспециализированным антицензурным инструментом (Xray с REALITY/Vision) и более широкой расширяемой платформой (v2ray), а не между живым и мёртвым.

## 📚 См. также

- [[xray/project-x|Project X (Xray-core)]] — история форка, ключевые технологии Xray, роль RPRX
- [[xray/authors-v2ray-xray|Кто стоит за V2Ray и Xray]] — авторы обоих проектов, разбор мифов о личности
- [[xray/reality|REALITY]] и [[xray/xtls-vision|XTLS-Vision]] — фирменные технологии Xray, которых нет в v2ray
- [[xray/vless|Протокол VLESS]] — базовый протокол, общий для обоих (но encryption/vision — только в Xray)
- [[sing-box/protocols-origin|Откуда код протоколов в sing-box]] — для сравнения: там пара ядер БЕЗ общего кода, здесь — родитель и форк

### Источники
- 🔗 исходники ядер: [github.com/v2fly/v2ray-core](https://github.com/v2fly/v2ray-core) · [github.com/XTLS/Xray-core](https://github.com/XTLS/Xray-core) · [оригинальный github.com/v2ray/v2ray-core](https://github.com/v2ray/v2ray-core) (без метки «forked from»)
- 🔗 родословная — Shadowsocks: [github.com/shadowsocks](https://github.com/shadowsocks) · [прощальный issue clowwindy #124](https://github.com/shadowsocks/shadowsocks-iOS/issues/124) · [Wikipedia: Shadowsocks](https://en.wikipedia.org/wiki/Shadowsocks) · [China Digital Times, авг. 2015](https://chinadigitaltimes.net/2015/08/circumvention-tool-deleted-after-police-visit-developer/)
- 🔗 V2Ray/Project V: [Wikipedia: V2Ray](https://en.wikipedia.org/wiki/V2Ray)
- 🔗 раскол v2fly ↔ Xray: [разбор сообщества v2fly discussions #688](https://github.com/v2fly/v2ray-core/discussions/688) · лицензионный спор [XTLS/Go #9](https://github.com/XTLS/Go/issues/9) · предложение убрать XTLS [v2ray-core #2789](https://github.com/v2ray/v2ray-core/issues/2789)
- 🔗 нынешний мейнтейнер v2fly: [github.com/xiaokangwang](https://github.com/xiaokangwang) (Shelikhoo) · [профиль спикера USENIX Security 2023](https://www.usenix.org/conference/usenixsecurity23/speaker-or-organizer/xiaokang-wang-v2ray-project)
- 🔗 релизы: [v2ray-core releases](https://github.com/v2fly/v2ray-core/releases) · [Xray-core releases](https://github.com/XTLS/Xray-core/releases)

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование и скачивание всего репозитория одним zip-архивом доступны на GitHub: [исходник этой заметки](https://github.com/youtubediscord/todo/blob/main/xray/v2fly-vs-xray.md) · [весь репозиторий](https://github.com/youtubediscord/todo/tree/main).
