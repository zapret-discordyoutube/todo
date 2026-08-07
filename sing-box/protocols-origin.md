---
date: 2026-07-18
tags:
  - sing-box
  - xray
  - архитектура
  - протоколы
aliases:
  - Откуда код протоколов в sing-box
  - sing-box vs Xray-core
  - происхождение протоколов sing-box
link: https://github.com/shtorm-7/sing-box-extended
---

# 🧬 Откуда в sing-box код протоколов: своя реализация или копия Xray

> [!info] О чём заметка
> Ответ на вопрос «sing-box просто вшивает чужие протоколы статичными файлами, или пишет их сам — и есть ли вообще разница между ядрами sing-box и Xray-core?». Разбор сделан по исходникам [[sing-box/sing-box-extended|sing-box-extended]] (включающего весь upstream sing-box) с прямым сравнением против Xray-core. Внутреннее устройство самого форка — в [[sing-box/architecture|разборе архитектуры]]. Если незнакомы с самой идеей «двух независимых реализаций одного протокола» — начните с вводной заметки [[sing-box/wire-protocol-explained|Что такое wire-протокол]].

## TL;DR

- **sing-box и Xray-core — два независимых ядра без единой общей строчки прокси-кода**: прямых импортов друг из друга ноль в обе стороны; Xray-core — форк v2ray-core, sing-box написан с нуля на экосистеме библиотек `sagernet/sing`. Что вообще значит «две независимые реализации одного протокола» — в [[sing-box/wire-protocol-explained|отдельной вводной заметке]].
- Совместимость по VLESS/Trojan/VMess/REALITY между ними — результат **двойной реализации одних и тех же wire-спецификаций** (одинаковые байты на проводе, разный код), а не общего кода.
- Ответ на «просто вшиты статичные файлы?» — **в основном нет, но есть исключения**: VLESS encryption и слой `common/xray/*` — действительно почти дословные копии из Xray-core; wire-формат Hysteria2 скопирован байт-в-байт из apernet/hysteria. Всё остальное (VLESS-заголовок, Vision, REALITY, VMess, Shadowsocks, Trojan, TUIC) — самостоятельные реимплементации.
- Чужой код входит в sing-box тремя путями: собственные библиотеки SagerNet (`sing-vmess`, `sing-quic`, …), форки сторонних проектов через go.mod (~13 штук: quic-go, wireguard-go, gvisor, uTLS и др.) и точечные in-tree порты (слой `common/xray`, mKCP, kTLS из Go stdlib).

> [!warning] Источник данных
> Выводы получены пятью независимыми проходами по исходникам (июль 2026): ветка `extended` форка sing-box-extended, Xray-core, библиотеки `sing-vmess`, `sing-quic`, `sing-shadowsocks2`, `sing-shadowtls`, официальный `apernet/hysteria` — включая прямые diff-сравнения файлов. Часть выводов относится к форку (например, uTLS от MetaCubeX) и может отличаться от upstream sing-box; это отмечено в тексте.

## Два ядра — две родословные

Распространённое представление «sing-box и Xray — примерно одно и то же» неверно на уровне кода. [[xray/project-x|Xray-core]] — форк v2ray-core и несёт его наследие: конфиг protobuf-first (78 `.proto`-файлов; JSON из пользовательского конфига конвертируется в protobuf-сообщения слоем `infra/conf/`), глобальный реестр протоколов на reflection (`common.RegisterConfig` из `init()`), собственный слой буферов `common/buf` с MultiBuffer.

sing-box написан с нуля автором nekohasekai (SagerNet) поверх собственной базовой библиотеки `sagernet/sing`: конфиг — чистый JSON, маппящийся в типизированные Go-структуры без protobuf; протоколы регистрируются в явных generic-реестрах (подробно — в [[sing-box/architecture|разборе архитектуры]]); буферы — из библиотеки `sing`. Grep по всем исходникам не находит ни одного импорта `github.com/xtls/*` или `github.com/v2fly/*` в sing-box — и ни одного импорта `sagernet/sing-box` в Xray.

Проще говоря: это два разных дома, построенных по разным чертежам, у которых совпадают только дверные замки — чтобы подходили одни и те же ключи-протоколы. Даже общие низкоуровневые зависимости разведены по разным форкам: uTLS у sing-box-extended — форк MetaCubeX (`metacubex/utls`; в upstream sing-box — форк `sagernet/utls`), у Xray — оригинальный `refraction-networking/utls`; quic-go у sing-box — `sagernet/quic-go`, у Xray — `apernet/quic-go` (оба — независимые форки одного `quic-go/quic-go`).

## Как достигается совместимость: спецификация, а не копипаста

Основной механизм — **независимая реализация того же байтового формата**. Библиотеки SagerNet реализуют те же константы, порядок полей и криптопримитивы, что и «родные» проекты, но собственным кодом под свои абстракции. README библиотек прямо декларируют цель: «100% compatible with v2ray-core» (sing-vmess), «Go implementation of shadow-tls» (sing-shadowtls) — совместимость по формату, не заимствование исходников.

| Протокол | Где реализация | Происхождение |
|---|---|---|
| VLESS (wire-заголовок) | библиотека `sing-vmess/vless` | Независимая реимплементация; формат совпадает с Xray (UUID, addons, flow), код — нет |
| XTLS-Vision | `sing-vmess/vless/vision.go` | Реимплементация с дословным переносом констант Xray (chunk 8192, пороги паддинга 900/500/256, 5-байтовый заголовок) — иначе байтовой совместимости не было бы |
| REALITY | клиент в дереве sing-box (`common/tls/reality_client.go`), сервер в форке uTLS | Независимая реализация; библиотека `xtls/reality`, которую использует Xray, не подключена вовсе |
| VMess | библиотека `sing-vmess` | Независимая реимплементация SagerNet |
| Shadowsocks | библиотеки `sing-shadowsocks`/`sing-shadowsocks2` | Независимая реимплементация (включая Shadowsocks-2022) |
| Trojan | в дереве, `transport/trojan/` | Независимая реимплементация (те же константы формата: SHA224-hex пароля, CRLF, команды 1/3) |
| Hysteria v1, TUIC | библиотека `sing-quic` | Независимые реимплементации SagerNet |
| Hysteria2 | библиотека `sing-quic/hysteria2` | **Гибрид**: файлы wire-формата скопированы из apernet/hysteria байт-в-байт, транспорт/obfs/congestion переписаны (см. ниже) |
| SOCKS, HTTP | библиотека `sing` | Своя реализация открытых RFC-протоколов |
| NaiveProxy | `protocol/naive/` | Сервер — обычный HTTP/2+HTTP/3 на Go; клиент (только в форке) — обёртка над Chromium Cronet |

## Где код всё-таки скопирован

Проходы по коду нашли три заметных места, где ответ «вшито статичными файлами» — правда:

1. **VLESS encryption** (`protocol/vless/encryption/` — пост-квантовое шифрование ML-KEM + X25519). Прямой diff против `xray-core/proxy/vless/encryption/` показывает почти построчное совпадение: изменены только import-пути, обёртки ошибок и добавлено несколько методов интеграции; логика хендшейка, 0-RTT, паддинга и XorConn совпадает дословно. Это честный вендоринг кода Xray.
2. **`common/xray/*`** — «подложка» для пункта 1: дословно скопированные внутренние пакеты Xray-core (`buf`, `net`, `signal`, `crypto`, `pipe` и др.) с переименованным namespace — в файлах даже сохранились doc-маркеры `xray:api:beta`. Скопированы, чтобы не тянуть весь Xray-core как зависимость.
3. **Wire-формат Hysteria2**: файлы определений протокола (`internal/protocol/http.go`, `padding.go` — заголовки `Hysteria-*`, путь `/auth`, статус-код 233) в `sing-quic` идентичны apernet/hysteria вплоть до пустого diff. При этом транспорт, сессии, obfuscation Salamander и congestion control Brutal переписаны под стек sing (с теми же алгоритмическими константами — например, `minAckRate=0.8`).

К этой же категории «порт чужого кода в дерево» относятся транспорты: mKCP (`transport/v2raykcp/` — порт из v2ray-core, в коде остались ссылки «mirrors v2ray-core's kcp»), [[xray/xhttp|XHTTP]] (`transport/v2rayxhttp/`), simple-obfs и SIP003 (из shadowsocks-экосистемы), kTLS (порт `crypto/tls` из Go stdlib, копирайты The Go Authors), JA3-парсер (Open Systems AG).

> [!note] Каталоги `transport/v2ray*` — это название семейства, а не признак копии
> WebSocket/gRPC/HTTPUpgrade-транспорты в sing-box лежат в каталогах с префиксом `v2ray*` (`v2raywebsocket`, `v2raygrpc`…), потому что «V2Ray transport» — устоявшееся имя семейства транспортов, совместимость с которым нужна клиентам. Сами реализации там в основном собственные, на библиотеках sing (с точечными исключениями вроде mKCP и заимствованных файлов gRPC-credentials).

## Итоговая картина: три пути чужого кода

1. **Собственные библиотеки SagerNet** (та же команда, что и ядро): `sing`, `sing-vmess`, `sing-quic`, `sing-shadowsocks(2)`, `sing-shadowtls`, `sing-mux`, `sing-tun`. Это не «чужой» код — это ядро, разнесённое по модулям.
2. **Форки сторонних проектов через go.mod** (~13 в sing-box-extended): `quic-go`, `wireguard-go` (от zx2c4), `gvisor` (Google), `tailscale`, uTLS, `smux`, `bbolt` и др. — плюс в форке shtorm-7 поверх них ещё 9 собственных развилок (см. [[sing-box/architecture|архитектуру]]).
3. **In-tree порты** — то самое «вшито статичными файлами», но точечно: слой `common/xray` + VLESS encryption (из Xray), mKCP (из v2ray), wire-константы Hysteria2 (из apernet), kTLS и `container/list` (из Go), JA3.

Вывод одной фразой: **sing-box не «пишет все протоколы с нуля» и не «вшивает чужое ядро» — он реализует чужие wire-спецификации самостоятельно в 80–90% случаев (оценка по числу протоколов из таблицы выше), а копирует файлы дословно лишь там, где протокол слишком свежий или сложный, чтобы переписывать (пост-квантовый VLESS encryption), либо где нужна гарантированная байтовая идентичность формата (Hysteria2). И разница между ядрами sing-box и Xray-core фундаментальная — общий у них только протокол на проводе.**

## 📚 См. также

- [[sing-box/wire-protocol-explained|Что такое wire-протокол]] — вводная про совместимость по проводу и двойную реализацию, фундамент этой заметки
- [[sing-box/sing-box-extended|sing-box-extended — обзор]] — что за форк и его возможности
- [[sing-box/architecture|Архитектура sing-box-extended]] — ядро, реестры, лимитеры, manager-подсистема, карта форков зависимостей
- [[sing-box/hardcoded-defaults|Хардкод-константы и дефолты]] — порты, таймауты и магические числа из исходников
- [[xray/project-x|Project X / Xray-core]] — родословная и экосистема Xray
- [[xray/vless|Протокол VLESS]] и [[xray/xtls-vision|XTLS и Vision]] — сами протоколы, о чьих реализациях идёт речь
- [[xray/reality|REALITY]] — протокол, реализованный в обоих ядрах независимо
- [[Hysteria/00-overview|Hysteria]] — официальная реализация apernet, с которой sing-box совместим
- 🔗 [github.com/SagerNet/sing-box](https://github.com/SagerNet/sing-box) — оригинальный sing-box
- 🔗 [github.com/XTLS/Xray-core](https://github.com/XTLS/Xray-core) — Xray-core

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование и скачивание всего репозитория одним zip-архивом доступны на GitHub: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/sing-box/protocols-origin.md) · [весь репозиторий](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main).
