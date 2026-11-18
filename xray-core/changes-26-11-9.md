---
date: 2026-11-18
tags:
  - xray
  - xray-core
  - changelog
  - миграция
  - vless
aliases:
  - Что нового в Xray-core 26.11.9
  - Xray-core 26.11.9 изменения
  - Чем Xray 26.11.9 отличается от 26.3.27
  - Что сломалось в конфиге Xray после обновления
  - Xray-core changelog 2026
description: "Разница между Xray-core 26.11.9 и предыдущей стабильной 26.3.27: что убрали, что стало обязательным, новые транспорты, Finalmask, TUN, Lua и безопасность."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [pyzluhgrnw.osjcpjzipyb.click/xray-core/changes-26-11-9](https://pyzluhgrnw.osjcpjzipyb.click/xray-core/changes-26-11-9)

# 🆕 Что нового в Xray-core 26.11.9: разница с предыдущей стабильной 26.3.27

> [!info] О чём заметка
> Сравнение официального ядра [Xray-core](https://github.com/XTLS/Xray-core) версии 26.11.9 (9 ноября 2026) с предыдущей стабильной версией 26.3.27 (27 марта 2026): что в конфигурации перестало работать, что поведение изменило молча, и что добавилось. Устройство самих компонентов — в [[xray-core/components|каталоге компонентов]]; история проекта — в [[xray/project-x|Project X]].

> [!warning] Откуда взяты данные
> Официальные заметки к релизу 26.11.9 почти пусты: [в них только две ссылки](https://github.com/XTLS/Xray-core/releases/tag/v26.11.9) (транспорт XDRIVE и отпечаток Chrome 155). Автор проекта в заметках к [релизу 26.10.21](https://github.com/XTLS/Xray-core/releases/tag/v26.10.21) прямо написал, что полное описание накопленных за полгода изменений отложено. Поэтому список ниже восстановлен по истории коммитов между тегами [v26.3.27](https://github.com/XTLS/Xray-core/releases/tag/v26.3.27) и v26.11.9 (388 коммитов) и по коду самих тегов. Названия параметров проверены в коде, а мотивы изменений в сообщениях коммитов не всегда объяснены, так что там, где они не названы, текст их не додумывает. Перед обновлением боевого сервера проверьте конфигурацию командой `xray run -test`.

## TL;DR

- «Предыдущая стабильная» здесь — 26.3.27. После неё GitHub 13 раз выпускал версии с пометкой pre-release (от 26.4.13 до 26.9.30), а следующей стабильной стала только 26.10.21, поэтому разница накопилась за полгода и разом.
- Самое важное для сервера: VLESS и Trojan **без шифрования к публичному адресу больше не принимаются**, Mux по умолчанию получает **128** потоков вместо 8, MPTCP **выключен**, а встроенный корневой список сертификатов заменил системный.
- Из конфигураций уходят: корневой `reverse` (замена — обратный прокси VLESS), режимы без шифрования у VMess и Shadowsocks, заголовки mKCP `dns`, `dtls`, `srtp`, `utp`, `wechat`, `wireguard` (замена — маска `mkcp-legacy`), `blockDelay`.
- Новое: транспорт **XDRIVE** (хранилище как канал), протокол и транспорт **MASQUE**, пять новых масок Finalmask, скрипты **Lua** в маршрутизации и DNS, модуль **geodata** с автообновлением, собственный TCP/IP-стек вместо gVisor.
- После тега 26.11.9 в `main` уже есть ломающие правки (например, `finalRules` → `firewall`), которых в этом релизе нет.

## Какая версия считается стабильной

На странице релизов GitHub у каждой версии есть пометка: стабильная или pre-release. Проект выпускает много версий подряд, и обычный пользователь получает только те, что помечены стабильными. Вот как выглядит последний год по этим пометкам: 26.2.6 → 26.3.27 (стабильные) → 13 pre-release от 26.4.13 до 26.9.30 → 26.10.21 → 26.10.31 → 26.11.9 (стабильные).

Две из трёх последних стабильных версий вышли как срочные исправления безопасности. Версия [26.10.21](https://github.com/XTLS/Xray-core/releases/tag/v26.10.21) убрала из встроенного списка корневых сертификатов три записи: поводом [названо вскрытие закрытых ключей нескольких индийских промежуточных сертификатов](https://github.com/XTLS/Xray-core/pull/7212), ключи которых оказались слишком простыми. Она собрана на Go 1.27.3, чтобы такие сертификаты отфильтровывались, даже если список в операционной системе не обновлён; версии 26.10.10 и 26.10.17 автор отозвал. Версия [26.10.31](https://github.com/XTLS/Xray-core/releases/tag/v26.10.31) закрыла опасность MPTCP на Linux (версия 26.10.29 тоже отозвана). Версия 26.11.9 — первая после них с обычным набором изменений.

## Что может сломать старый конфиг

Таблица собрана по сообщениям коммитов и проверена по коду тега 26.11.9. В столбце «Дата» указан день попадания изменения в основную ветку: в релиз оно вошло со следующей по времени версией.

| Что изменилось | Дата | Что делать |
|---|---|---|
| Исходящий `vless` без TLS, REALITY или `encryption` и исходящий `trojan` без TLS отклоняются, если адрес сервера не частный IP и не частный домен ([PR #6303](https://github.com/XTLS/Xray-core/pull/6303)) | 7 июля | включить `security: tls` или `reality`, либо задать `encryption` (ключи — `xray vlessenc`) |
| У VMess и Shadowsocks убраны режимы без шифрования: `none`, `zero`, `plain` (тот же PR) | 7 июля | выбрать настоящий шифр |
| Корневой блок `reverse` не принимается, [ядро подсказывает перейти на VLESS Reverse Proxy](https://github.com/XTLS/Xray-core/commit/cd4d0baacd53e35dee78ed38bfd145a9408d4398) | 25 апреля | перенести настройку в поле `reverse` пользователя VLESS |
| Mux: значения `concurrency` от 0 до 128 поднимаются до **128** (раньше пустое значение означало 8); значения выше 128 сохраняются; число соединений на один мультиплексор ограничено 1024 | 6 ноября | уменьшить число потоков в этой версии нельзя; отрицательное `concurrency` отключает мультиплексор |
| MPTCP по умолчанию выключен для всех слушающих сокетов ([PR #7291](https://github.com/XTLS/Xray-core/pull/7291)) | 31 октября | если MPTCP нужен, включить `sockopt.tcpMptcp`; о причинах — [[xray/mptcp-linux-kernel-rce-cve-2026-98432\|CVE-2026-98432]] |
| Клиентский TLS доверяет встроенному списку корневых сертификатов, а не системному ([PR #7105](https://github.com/XTLS/Xray-core/pull/7105)) | 10 октября | если вы подключаетесь к серверу с корпоративным или самоподписанным сертификатом, задайте его в настройках TLS явно |
| Серверы XHTTP, WebSocket, HTTPUpgrade и gRPC учитывают заголовок `X-Forwarded-For` только от адресов из `sockopt.trustedXForwardedFor` ([PR #6309](https://github.com/XTLS/Xray-core/pull/6309)) | 19 июня | если сервер стоит за CDN или nginx, перечислите их адреса |
| Входящие `clients` и `accounts` называются `users`; для VLESS старое `clients` ядро читает по-прежнему ([PR #6083](https://github.com/XTLS/Xray-core/pull/6083)) | 7 мая | переименовать при ближайшей правке |
| Поле транспорта `network` называется `method`; оба имени читаются ([PR #6426](https://github.com/XTLS/Xray-core/pull/6426)) | 7 июля | переименовать при ближайшей правке |
| Входящий `tunnel`: `address`, `port`, `network` стали `rewriteAddress`, `rewritePort`, `allowedNetwork`; старые имена читаются ([PR #6084](https://github.com/XTLS/Xray-core/pull/6084)) | 7 мая | переименовать при ближайшей правке |
| Исходящий `dns`: действие `reject` заменено на `return` (`rCode` по умолчанию 0) ([PR #6214](https://github.com/XTLS/Xray-core/pull/6214)) | 1 июня | заменить в правилах |
| Исходящий `freedom`: в `finalRules` поле `blockDelay` переименовано в `delay`, добавлен `logLevel` ([PR #7329](https://github.com/XTLS/Xray-core/pull/7329)); `fragment` и `noises` помечены к переносу в Finalmask ([PR #7242](https://github.com/XTLS/Xray-core/pull/7242)) | 4 ноября, 29 октября | заменить `blockDelay` на `delay`; со временем перенести `fragment` и `noises` в маски |
| WireGuard (исходящий): убраны режим `local` у `remoteDNS` и `domainStrategy` ([PR #6771](https://github.com/XTLS/Xray-core/pull/6771)) | 21 сентября | убрать из конфигурации |
| Заголовки mKCP `dns`, `dtls`, `srtp`, `utp`, `wechat`, `wireguard` заменены маской `mkcp-legacy` ([PR #6201](https://github.com/XTLS/Xray-core/pull/6201)) | 29 мая | перейти на маску Finalmask |
| TLS: убран параметр `echForceQuery` (ECH теперь применяется всегда, если настроен) ([PR #6032](https://github.com/XTLS/Xray-core/pull/6032)); удалены ещё несколько устаревших полей ([PR #6226](https://github.com/XTLS/Xray-core/pull/6226)) | 2 мая, 3 июня | убрать |
| XHTTP: параметры `session*` переименованы в `sessionID*` и добавлены `sessionIDTable`, `sessionIDLength` ([PR #6258](https://github.com/XTLS/Xray-core/pull/6258)); у клиента по умолчанию `maxConnections` теперь 3 (27 июня вместо прежнего `maxConcurrency: 1` задали `maxConnections: 6`, 28 июля снизили до 3; оба выпуска были пре-релизами, в стабильных версиях значение 3 с 26.10.21) | 9 июня, 28 июля | сверить, если вы полагались на значение по умолчанию |
| Для Go нужна версия 1.27 (`go.mod`: было 1.26) | 8 сентября | актуально только для самостоятельной сборки |

Обратите внимание на строку про Mux: она не вызывает ошибку, поведение меняется молча. Клиент с `mux.concurrency: 8` теперь складывает в одно соединение до 128 потоков, и причина возможного падения скорости из журнала не видна. В релизе 26.11.9 это действует для всех транспортов; в `main` уже есть правка, ограничивающая значение 128 транспортом XDRIVE.

Отдельно про REALITY: значение по умолчанию `minClientVer: 26.3.27` действовало только в пре-релизах. Его [добавили 11 июля](https://github.com/XTLS/Xray-core/commit/af7eb68028732a8ee3c0e5d6ab2b8a657bb2e770) (тогда сервер переставал принимать клиентов старше 26.3.27), а [8 сентября отключили](https://github.com/XTLS/Xray-core/commit/47cfe9994a6b39b1f673ba35e62b091bcce15a71) при обновлении библиотеки REALITY: в коде осталась закомментированная строка. В стабильных версиях 26.10.21, 26.10.31 и 26.11.9 порога по умолчанию нет, он включается только если задать `minClientVer` в конфиге самому.

## Новые компоненты

### Транспорты и протоколы

**XDRIVE** — транспорт, в котором клиент и сервер обмениваются данными не напрямую, а через общее хранилище. Он появился в сентябре ([PR #5645](https://github.com/XTLS/Xray-core/pull/5645), бэкенд Google Drive и шаблонный бэкенд — [PR #6748](https://github.com/XTLS/Xray-core/pull/6748)) и к ноябрю получил бэкенд S3 ([PR #7231](https://github.com/XTLS/Xray-core/pull/7231)), поддержку HTTP/3 ([PR #7187](https://github.com/XTLS/Xray-core/pull/7187)) и серию оптимизаций, о которых говорится [в заметках 26.11.9](https://github.com/XTLS/Xray-core/pull/7352). С 17 октября он требует VLESS с `encryption` и включённый `mux` ([PR #7182](https://github.com/XTLS/Xray-core/pull/7182)).

**MASQUE** — туннель IP по стандарту IETF CONNECT-IP (RFC 9484): исходящий и транспорт добавлены 24 сентября ([PR #6807](https://github.com/XTLS/Xray-core/pull/6807)), входящий — 27 сентября ([PR #6844](https://github.com/XTLS/Xray-core/pull/6844)), позже поддержка HTTP/2 ([PR #6810](https://github.com/XTLS/Xray-core/pull/6810)), WARP ([PR #6878](https://github.com/XTLS/Xray-core/pull/6878)) и XMUX ([PR #7121](https://github.com/XTLS/Xray-core/pull/7121)).

**Hysteria** обновлена с 2.8.2 ([PR #6041](https://github.com/XTLS/Xray-core/pull/6041)) до официальной 2.12.2 ([PR #6565](https://github.com/XTLS/Xray-core/pull/6565)); входящий Hysteria теперь понимает `vlessRoute` в маршрутизации ([PR #6375](https://github.com/XTLS/Xray-core/pull/6375)).

**WireGuard** (входящий) получил управление пирами на лету ([PR #6360](https://github.com/XTLS/Xray-core/pull/6360)), у исходящего появился `remoteDNS` с учётом TTL ([PR #6620](https://github.com/XTLS/Xray-core/pull/6620)).

**Shadowsocks 2022** переписан без зависимостей от библиотек sing ([PR #6831](https://github.com/XTLS/Xray-core/pull/6831)); **SOCKS5** строже следует RFC 1928 в UDP ASSOCIATE ([PR #6149](https://github.com/XTLS/Xray-core/pull/6149)); у **blackhole** можно задать собственный ответ ([PR #6713](https://github.com/XTLS/Xray-core/pull/6713)); у **dns**-исходящего появились правила по типу записи и домену ([PR #5981](https://github.com/XTLS/Xray-core/pull/5981)); у **loopback** — `sniffing` ([PR #6326](https://github.com/XTLS/Xray-core/pull/6326)).

### Finalmask

За полгода Finalmask из набора отдельных приёмов превратился в общий слой. Новые маски: `realm` ([PR #6137](https://github.com/XTLS/Xray-core/pull/6137)), `udphop` ([PR #6327](https://github.com/XTLS/Xray-core/pull/6327)), `xmc` ([PR #6210](https://github.com/XTLS/Xray-core/pull/6210)), `filter` ([PR #7206](https://github.com/XTLS/Xray-core/pull/7206)) и `mkcp-legacy`. У `header-custom` появились программируемые шаблоны рукопожатия ([PR #5920](https://github.com/XTLS/Xray-core/pull/5920)), у `fragment` — `lengths` и `delays` ([PR #6334](https://github.com/XTLS/Xray-core/pull/6334)), у `xdns` — поддержка DoH и список резолверов, а `noise` умеет выполнять Lua-скрипт ([PR #7124](https://github.com/XTLS/Xray-core/pull/7124)). Транспорты теперь строятся поверх диалера и слушателя Finalmask ([PR #6754](https://github.com/XTLS/Xray-core/pull/6754)). Сами маски разобраны в [[xray-core/components|каталоге компонентов]].

### TUN и собственный сетевой стек

Входящий `tun` существовал и в 26.3.27, но с тех пор вырос: получил поддержку Windows ([PR #5887](https://github.com/XTLS/Xray-core/pull/5887)) и FreeBSD ([PR #5891](https://github.com/XTLS/Xray-core/pull/5891)), параметры `autoSystemRoutingTable` и `autoOutboundsInterface` для Linux и macOS ([PR #6366](https://github.com/XTLS/Xray-core/pull/6366)), счётчики трафика ([PR #6349](https://github.com/XTLS/Xray-core/pull/6349)) и на Windows защиту от утечек вне туннеля (`autoSystemWfpBlockLeak`). В октябре ядро перестало зависеть от gVisor: TUN ([PR #7130](https://github.com/XTLS/Xray-core/pull/7130)), WireGuard и MASQUE ([PR #7156](https://github.com/XTLS/Xray-core/pull/7156)) используют встроенный облегчённый TCP/IP-стек.

### Маршрутизация, DNS и geodata

**Lua** — скрипты для правил маршрутизации и DNS ([PR #6823](https://github.com/XTLS/Xray-core/pull/6823)), с 16 октября в песочнице с белым списком функций, а inline-скрипты временно отключены ([PR #7136](https://github.com/XTLS/Xray-core/pull/7136)). **Geodata** вынесена в отдельный модуль с обновлением по расписанию и горячей заменой файлов ([PR #5992](https://github.com/XTLS/Xray-core/pull/5992)), с ограничениями на размер, расширения и частоту загрузки ([PR #7267](https://github.com/XTLS/Xray-core/pull/7267)) и разбором сжатых файлов `.dat.gz` ([PR #7334](https://github.com/XTLS/Xray-core/pull/7334)). Сборки ядра на GitHub теперь берут встроенные списки [из репозитория XTLS/Xray-rules-dat](https://github.com/XTLS/Xray-core/pull/7185). В правилах появилось условие `localOS` ([PR #6553](https://github.com/XTLS/Xray-core/pull/6553)), условие `process` научилось работать на macOS, а на Android — с UID. Sniffing получил `ipsExcluded` ([PR #5929](https://github.com/XTLS/Xray-core/pull/5929)), `geosite:` в `domainsExcluded` ([PR #5927](https://github.com/XTLS/Xray-core/pull/5927)) и поддержку QUICv2 ([PR #6695](https://github.com/XTLS/Xray-core/pull/6695)). Балансировщик `leastload` наконец реализовал заявленный параметр `tolerance` ([PR #6156](https://github.com/XTLS/Xray-core/pull/6156)). У FakeDNS пул IPv6 по умолчанию стал `2001:2::/48` ([PR #6815](https://github.com/XTLS/Xray-core/pull/6815)).

### XHTTP и безопасность соединения

В XHTTP серверы получили `h2Params` ([PR #7295](https://github.com/XTLS/Xray-core/pull/7295)) и возможность принимать `OPTIONS` как метод загрузки ([PR #7290](https://github.com/XTLS/Xray-core/pull/7290)), клиент стал по умолчанию открывать меньше параллельных соединений. Разбор самого транспорта — в [[xray/xhttp|заметке про XHTTP]]. В XTLS Vision исправлена совместимость с Go 1.27.3 ([PR #7176](https://github.com/XTLS/Xray-core/pull/7176)) и убрано лишнее закрывающее уведомление внешнего TLS после перехода на прямое копирование ([PR #6834](https://github.com/XTLS/Xray-core/pull/6834)). Соответствие флага `flow` и других полей протоколу — в [[xray/xtls-vision|XTLS Vision]].

### API, команды, конфигурация

В API появился запрос статистики пользователей `GetUsersStats` ([PR #5776](https://github.com/XTLS/Xray-core/pull/5776)), `xray api adu` научился работать с Hysteria ([PR #6847](https://github.com/XTLS/Xray-core/pull/6847)). Новые подкоманды — `xray base64` ([PR #7132](https://github.com/XTLS/Xray-core/pull/7132)) и `xray lua sign` для подписи скриптов. В корне конфигурации появился блок `env` ([PR #6400](https://github.com/XTLS/Xray-core/pull/6400)), а переменная `XRAY_JSON_STRICT=true` включает строгий разбор JSON ([PR #6053](https://github.com/XTLS/Xray-core/pull/6053)).

## Что уже есть в `main`, но не вошло в 26.11.9

Тег 26.11.9 поставлен 9 ноября. С того времени в ветку `main` вошли правки, которых в релизе нет: [`finalRules` переименован в `firewall`, добавлен `reply`, исходящие `block` и `blackhole` объединены, `proxyProtocol` перенесён](https://github.com/XTLS/Xray-core/commit/7daa8e4b6adb3a7098b43b192fd3175d8612a884) (18 ноября); маска `xmc` перешла на «родное» дополнение кадров, и это ломающее изменение ([PR #7402](https://github.com/XTLS/Xray-core/pull/7402)); поведение Mux 128 ограничено транспортом XDRIVE ([PR #7375](https://github.com/XTLS/Xray-core/pull/7375)). Если сервер собран из `main`, а не из релиза, сверяйтесь с исходниками именно этой ветки.

## Источники

- [Исходный код Xray-core](https://github.com/XTLS/Xray-core)
- [Xray-core v26.11.9, заметки к релизу на GitHub](https://github.com/XTLS/Xray-core/releases/tag/v26.11.9)
- [Xray-core v26.10.21, заметки к релизу на GitHub](https://github.com/XTLS/Xray-core/releases/tag/v26.10.21)
- [Xray-core v26.3.27, заметки к релизу на GitHub](https://github.com/XTLS/Xray-core/releases/tag/v26.3.27)
- [PR #7212 — TLS client: Update built-in RootCAs to remove newly low-credit certs](https://github.com/XTLS/Xray-core/pull/7212)
- [Xray-core v26.10.31, заметки к релизу на GitHub](https://github.com/XTLS/Xray-core/releases/tag/v26.10.31)
- [PR #6303 — Xray-core: Forbid unencrypted outbounds on public Internet for VLESS and Trojan; Remove "none/zero/plain" for VMess and Shadowsocks](https://github.com/XTLS/Xray-core/pull/6303)
- [Коммит cd4d0baac в Xray-core](https://github.com/XTLS/Xray-core/commit/cd4d0baacd53e35dee78ed38bfd145a9408d4398)
- [PR #7291 — DefaultListener: Disable MPTCP by default](https://github.com/XTLS/Xray-core/pull/7291)
- [PR #7105 — TLS client: Use Xray-core's built-in RootCAs by default (avoids maliciously injected CA in the OS)](https://github.com/XTLS/Xray-core/pull/7105)
- [PR #6309 — XHTTP & WS & HU & gRPC servers: Require `sockopt.trustedXForwardedFor`](https://github.com/XTLS/Xray-core/pull/6309)
- [PR #6083 — Config: Rename inbounds' `clients`/`accounts` to `users`](https://github.com/XTLS/Xray-core/pull/6083)
- [PR #6426 — infra/conf/transport_internet.go: Split into multiple files; Rename `network` to `method`](https://github.com/XTLS/Xray-core/pull/6426)
- [PR #6084 — Config: Rename `network`/`address`/`port` in Tunnel inbound and DNS outbound](https://github.com/XTLS/Xray-core/pull/6084)
- [PR #6214 — DNS outbound: Replace "reject" with "return" (`rCode` is 0 by default)](https://github.com/XTLS/Xray-core/pull/6214)
- [PR #7329 — Direct/Freedom outbound's `finalRules`: Add `logLevel`; `blockDelay`->`delay`; Apply default safe policy on MASQUE as well](https://github.com/XTLS/Xray-core/pull/7329)
- [PR #7242 — Direct/Freedom outbound: Warn about migrating `fragment` and `noises` to Finalmask](https://github.com/XTLS/Xray-core/pull/7242)
- [PR #6771 — WireGuard outbound: Remove `remoteDNS`' "local" mode and `domainStrategy`](https://github.com/XTLS/Xray-core/pull/6771)
- [PR #6201 — Finalmask: Add mkcp-legacy (UDP) to replace mkcp-* and legacy header-*](https://github.com/XTLS/Xray-core/pull/6201)
- [PR #6032 — TLS ECH: Remove `echForceQuery` (ECH is forced now if configured)](https://github.com/XTLS/Xray-core/pull/6032)
- [PR #6226 — TLS config: Remove some deprecated fields](https://github.com/XTLS/Xray-core/pull/6226)
- [PR #6258 — XHTTP transport: Add `sessionIDTable` and `sessionIDLength`; Rename `session*` to `sessionID*`](https://github.com/XTLS/Xray-core/pull/6258)
- [PR #5645 — XDRIVE transport: The universal remote-storage/any-service-based proxy, ignoring IP whitelists](https://github.com/XTLS/Xray-core/pull/5645)
- [PR #6748 — XDRIVE transport: Add the Google Drive and "template" backend](https://github.com/XTLS/Xray-core/pull/6748)
- [PR #7231 — XDRIVE transport: Add "s3" storage backend](https://github.com/XTLS/Xray-core/pull/7231)
- [PR #7187 — XDRIVE transport: Support h3 (Chrome CH by default) and XMUX as well; Send Chrome HTTP headers (User-Agent, etc.) by default](https://github.com/XTLS/Xray-core/pull/7187)
- [PR #7352 — XDRIVE transport: Release notes & more optimizations for the Google Drive backend](https://github.com/XTLS/Xray-core/pull/7352)
- [PR #7182 — XDRIVE transport: Require VLESS Multiplex+Encryption; "Google Drive"->"google-drive"](https://github.com/XTLS/Xray-core/pull/7182)
- [PR #6807 — Proxy: Add MASQUE outbound & transport (IETF CONNECT-IP, RFC 9484)](https://github.com/XTLS/Xray-core/pull/6807)
- [PR #6844 — Proxy: Add MASQUE inbound (IETF CONNECT-IP server, RFC 9484)](https://github.com/XTLS/Xray-core/pull/6844)
- [PR #6810 — MASQUE client: Support HTTP/2 (Extended CONNECT, RFC 8441)](https://github.com/XTLS/Xray-core/pull/6810)
- [PR #6878 — MASQUE client: Support WARP](https://github.com/XTLS/Xray-core/pull/6878)
- [PR #7121 — MASQUE client: Support XMUX (`"maxConnections": 1` by default); Use Chrome's User-Agent by default](https://github.com/XTLS/Xray-core/pull/7121)
- [PR #6041 — Hysteria: Upgrade to official v2.8.2](https://github.com/XTLS/Xray-core/pull/6041)
- [PR #6565 — Hysteria: Upgrade to official v2.12.2](https://github.com/XTLS/Xray-core/pull/6565)
- [PR #6375 — Hysteria inbound: Support `routing`'s `vlessRoute` as well](https://github.com/XTLS/Xray-core/pull/6375)
- [PR #6360 — WireGuard inbound: Support dynamic peer management](https://github.com/XTLS/Xray-core/pull/6360)
- [PR #6620 — WireGuard outbound: Add `remoteDNS` & honor TTL](https://github.com/XTLS/Xray-core/pull/6620)
- [PR #6831 — SS2022 proxy: Refactor to remove sing* dependencies](https://github.com/XTLS/Xray-core/pull/6831)
- [PR #6149 — Socks5 server: More standard UDP ASSOCIATE (RFC 1928)](https://github.com/XTLS/Xray-core/pull/6149)
- [PR #6713 — Blackhole outbound: Add customizable response data support](https://github.com/XTLS/Xray-core/pull/6713)
- [PR #5981 — DNS outbound: Add `rules` (matches `qtype` and `domain`, then `action`)](https://github.com/XTLS/Xray-core/pull/5981)
- [PR #6326 — Loopback outbound: Add `sniffing`](https://github.com/XTLS/Xray-core/pull/6326)
- [PR #6137 — Finalmask: Add Realm (UDP hole punching in Hysteria v2.9.1)](https://github.com/XTLS/Xray-core/pull/6137)
- [PR #6327 — Finalmask: Make "udpHop" a new UDP mask](https://github.com/XTLS/Xray-core/pull/6327)
- [PR #6210 — Finalmask: Add XMC (TCP, Minecraft)](https://github.com/XTLS/Xray-core/pull/6210)
- [PR #7206 — Finalmask: Add `filter` for inbound (TCP & UDP, source IP filtering)](https://github.com/XTLS/Xray-core/pull/7206)
- [PR #5920 — header-custom finalmask: Add programmable handshake templates and runtime core](https://github.com/XTLS/Xray-core/pull/5920)
- [PR #6334 — Fragment finalmask: Add `lengths` and `delays`](https://github.com/XTLS/Xray-core/pull/6334)
- [PR #7124 — Noise finalmask: Support Lua `script` as well (on main branch: inline scripts were disabled for now; sandbox-only for now)](https://github.com/XTLS/Xray-core/pull/7124)
- [PR #6754 — Transport: Refactor to be based on Finalmask's dialer & listener](https://github.com/XTLS/Xray-core/pull/6754)
- [PR #5887 — TUN inbound: Add `gateway`, `dns`, `autoSystemRoutingTable`, `autoOutboundsInterface` for Windows](https://github.com/XTLS/Xray-core/pull/5887)
- [PR #5891 — TUN inbound: Add FreeBSD support](https://github.com/XTLS/Xray-core/pull/5891)
- [PR #6366 — TUN inbound: Support `autoSystemRoutingTable` and `autoOutboundsInterface` on macOS and Linux as well](https://github.com/XTLS/Xray-core/pull/6366)
- [PR #6349 — TUN inbound: Add traffic counters; Metrics: Rely on instance](https://github.com/XTLS/Xray-core/pull/6349)
- [PR #7130 — TUN inbound: Use Xray-core's built-in lightweight TCP/IP stack instead of gVisor](https://github.com/XTLS/Xray-core/pull/7130)
- [PR #7156 — WireGuard, MASQUE proxies: Use Xray-core's built-in lightweight TCP/IP stack instead of gVisor as well](https://github.com/XTLS/Xray-core/pull/7156)
- [PR #6823 — Xray-core: Add Lua `script` for `dns` and `routing`](https://github.com/XTLS/Xray-core/pull/6823)
- [PR #7136 — Lua: Sandbox by default (whitelisted functions); Disable inline scripts for now; Add more checks for security reasons](https://github.com/XTLS/Xray-core/pull/7136)
- [PR #5992 — Geodata: Support automatically updating .dat files and hot reloading](https://github.com/XTLS/Xray-core/pull/5992)
- [PR #7267 — Geodata: Limit download size, file extensions, and update frequency](https://github.com/XTLS/Xray-core/pull/7267)
- [PR #7334 — Geodata: Download `.dat.gz` when the URL belongs to XTLS/Xray-rules-dat](https://github.com/XTLS/Xray-core/pull/7334)
- [PR #7185 — GitHub Actions: Switch geodata to XTLS/Xray-rules-dat](https://github.com/XTLS/Xray-core/pull/7185)
- [PR #6553 — Routing: Add `localOS` that directly matches `runtime.GOOS`](https://github.com/XTLS/Xray-core/pull/6553)
- [PR #5929 — Sniffing: Add `ipsExcluded` (supports IP, CIDR, "geoip:", "ext:")](https://github.com/XTLS/Xray-core/pull/5929)
- [PR #5927 — Sniffing: `domainsExcluded` supports "geosite:"](https://github.com/XTLS/Xray-core/pull/5927)
- [PR #6695 — Sniffing: Support QUICv2](https://github.com/XTLS/Xray-core/pull/6695)
- [PR #6156 — leastLoad balancer: Implement missing `tolerance`](https://github.com/XTLS/Xray-core/pull/6156)
- [PR #6815 — FakeDNS: Change default FakeIPv6Pool to 2001:2::/48](https://github.com/XTLS/Xray-core/pull/6815)
- [PR #7295 — XHTTP server: Add `h2Params`](https://github.com/XTLS/Xray-core/pull/7295)
- [PR #7290 — XHTTP server: Accept OPTIONS as `uplinkHTTPMethod`](https://github.com/XTLS/Xray-core/pull/7290)
- [PR #7176 — XTLS Vision: Compatible with Go 1.27.3+](https://github.com/XTLS/Xray-core/pull/7176)
- [PR #6834 — XTLS Vision: Suppress outer CloseNotify after switching to direct copy](https://github.com/XTLS/Xray-core/pull/6834)
- [PR #5776 — API & Commands: Add GetUsersStatsRequest(); Improve `api statsonlineiplist`](https://github.com/XTLS/Xray-core/pull/5776)
- [PR #6847 — API: `xray api adu` supports Hysteria](https://github.com/XTLS/Xray-core/pull/6847)
- [PR #7132 — Lua: Support inline scripts; Add `./xray base64 encode/decode [-gzip]` command](https://github.com/XTLS/Xray-core/pull/7132)
- [PR #6400 — Root config: Add `env` config](https://github.com/XTLS/Xray-core/pull/6400)
- [PR #6053 — Config: Support env `XRAY_JSON_STRICT=true`](https://github.com/XTLS/Xray-core/pull/6053)
- [Коммит 7daa8e4b6 в Xray-core](https://github.com/XTLS/Xray-core/commit/7daa8e4b6adb3a7098b43b192fd3175d8612a884)
- [PR #7402 — XMC finalmask: Switch to native frame padding (breaking); `delay` supports range (receiver waits at least minimal ms)](https://github.com/XTLS/Xray-core/pull/7402)
- [PR #7375 — VLESS Multiplex (mux.cool): Raise maxConcurrency to 128 only for XDRIVE](https://github.com/XTLS/Xray-core/pull/7375)

- [Коммит af7eb68 в Xray-core: REALITY, значение minClientVer по умолчанию](https://github.com/XTLS/Xray-core/commit/af7eb68028732a8ee3c0e5d6ab2b8a657bb2e770)
- [Коммит 47cfe99 в Xray-core: обновление REALITY, порог отключён](https://github.com/XTLS/Xray-core/commit/47cfe9994a6b39b1f673ba35e62b091bcce15a71)

## 📚 См. также

- [[xray-core/xray-core|Документация Xray-core 26.11.9]] — оглавление раздела
- [[xray-core/components|Компоненты Xray-core]] — из чего состоит ядро и как называется каждая часть в конфиге
- [[xray/project-x|Project X (Xray-core)]] — история проекта
- [[xray/mptcp-linux-kernel-rce-cve-2026-98432|CVE-2026-98432]] — почему MPTCP выключен
- [[xray/vless|Протокол VLESS]] и [[xray/vless-encryption|VLESS Encryption]] — как включить шифрование, которого теперь требует ядро
- [[xray/xhttp|XHTTP]] — главный транспорт после очистки старых

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование и скачивание всего репозитория одним zip-архивом доступны в Forgejo: [исходник этой заметки](https://tficguhwsu.osjcpjzipyb.click/zapretdiscordyoutube/todo/src/branch/main/xray-core/changes-26-11-9.md) · [весь репозиторий](https://tficguhwsu.osjcpjzipyb.click/zapretdiscordyoutube/todo/src/branch/main).
