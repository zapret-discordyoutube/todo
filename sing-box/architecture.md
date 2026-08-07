---
date: 2026-07-17
tags:
  - sing-box
  - архитектура
  - go
  - proxy
aliases:
  - Архитектура sing-box-extended
  - sing-box-extended internals
link: https://github.com/shtorm-7/sing-box-extended
---

# 🏗️ Архитектура sing-box-extended: как форк устроен изнутри

> [!info] О чём заметка
> Разбор исходного кода [sing-box-extended](https://github.com/shtorm-7/sing-box-extended) — форка прокси-платформы sing-box с десятками дополнительных протоколов и функций. Что это за проект и зачем он нужен — в обзорной заметке [[sing-box/sing-box-extended|sing-box-extended]]; здесь — только внутреннее устройство: ядро, registry-паттерн, реализация протоколов, лимитеры, DNS и подсистема управления «manager + node + панель».

> [!warning] Источник данных
> Заметка составлена по разбору исходников ветки `extended` (снимок на 17 июля 2026, релиз `v1.13.14-extended-2.5.1`) пятью независимыми проходами по коду. Пути файлов и номера строк со временем поплывут — сверяйся с актуальным репозиторием. Выводы о поведении кода сделаны чтением, без запуска и динамической проверки.

## TL;DR

- Форк сохраняет module path `github.com/sagernet/sing-box` и не выделяет свой код в отдельный namespace: новые протоколы добавлены прямо в `protocol/`, новые сервисы — в `service/`, а зависимости SagerNet подменены через 9 `replace`-директив в `go.mod` на форки автора (`shtorm-7/sing`, `shtorm-7/wireguard-go` и др.).
- Ядро — конструктор `box.New()`: реестры типов (registry-паттерн) лежат в контексте, конфиг-JSON парсится по полю `type` через эти же реестры, «тяжёлые» фичи отсекаются build-tag-ами `with_*` (масштаб — 1052 Go-файла).
- Протоколы поделены на свои реализации (OpenVPN, Sudoku, Snell, TrustTunnel, VLESS encryption, Bond, Failover) и обёртки над библиотеками (Mieru → `enfein/mieru`, MTProxy → форк `mtg-multi`, MASQUE → `connect-ip-go`, DNSCrypt → форк `ameshkov/dnscrypt`).
- Лимитеры — это outbound-обёртки со встроенным собственным роутером; Failover умеет прозрачно восстанавливать TCP-сессии после разрыва, Bond режет поток на куски по долям между несколькими каналами.
- Подсистема управления: центральный сервис `manager` (SQLite/PostgreSQL) раздаёт пользователей и лимиты узлам по gRPC-стриму (узел сам подключается к менеджеру — удобно за NAT), пользователи вживляются в работающие inbound-ы без перезапуска; админ-панель — React SPA, встроенная в бинарник через `go:embed`.
- Слабые места по части безопасности: секреты пользователей в БД менеджера хранятся открытым текстом, аутентификация всех API — один статический ключ.

## Ядро: Box, менеджеры и registry-паттерн

Вся программа собирается вокруг структуры `Box` (файл `box.go` в корне). `box.New(options)` создаёт набор менеджеров — по одному на каждую категорию сущностей конфига: `inbound.Manager` (входящие слушатели), `outbound.Manager` (исходящие подключения), `endpoint.Manager` (двусторонние туннели вроде WireGuard), `provider.Manager` (подписки), `service.Manager` (сервисы), `dns.TransportManager` и `dns.Router`, `route.Router` с `route.NetworkManager` и `route.ConnectionManager`. Жизненный цикл многофазный: `PreStart → Start → PostStart`, закрытие — в обратном порядке.

Расширяемость построена на **registry-паттерне**. Для каждой категории существует реестр (`adapter/inbound/registry.go` и аналоги): generic-функция `Register[Options any](registry, type, constructor)` кладёт в две map конструктор объекта и конструктор его структуры опций. Реестры создаются декларативно в одном месте — `include/registry.go` — и кладутся в контекст как DI-контейнер (типизированный сервис-локатор из библиотеки `sagernet/sing/service`).

Парсинг конфига опирается на те же реестры. JSON-объект inbound/outbound/service несёт поле `type`; кастомный `UnmarshalJSONContext` (например в `option/inbound.go`) достаёт из контекста реестр опций, по строке типа создаёт пустую структуру нужных опций и домаршаливает в неё остаток JSON. Добавить новый протокол = написать пакет в `protocol/`, структуру опций в `option/` и одну строку регистрации в `include/registry.go`.

Проще говоря: ядро ничего не знает о конкретных протоколах — оно знает только слово «тип» и таблицу «тип → конструктор». Поэтому форку не пришлось переписывать ядро, чтобы добавить полтора десятка протоколов: он просто дописал таблицу.

Опциональные фичи отсекаются **build-tag-ами**: парные файлы `include/<фича>.go` (`//go:build with_<фича>`) и `include/<фича>_stub.go` — заглушка возвращает ошибку «rebuild with -tags with_...». Под тегами живут `with_masque`, `with_openvpn`, `with_snell`, `with_sudoku`, `with_mtproxy`, `with_trusttunnel`, `with_wireguard` (включая WARP), `with_manager`, `with_admin_panel` и другие; Mieru, SSH, VPN, Bond, Failover вкомпилированы всегда.

## Как форк наслаивается на upstream

Отдельного «слоя форка» в дереве исходников нет — код добавлен прямо в структуру upstream (module path остался `github.com/sagernet/sing-box`). Extended-код распознаётся по трём признакам:

1. **Новые пакеты в `protocol/`**: `bond`, `failover`, `mieru`, `mtproxy`, `openvpn`, `snell`, `sudoku`, `trusttunnel`, `warp`, `masque`, `limiter/*`.
2. **Новые пакеты в `service/`**: `manager`, `manager_api`, `node`, `node_manager_api`, `admin_panel` и другие (в upstream из сервисов есть только `resolved` и `ssmapi`).
3. **`go.mod`**: 9 `replace`-директив подменяют зависимости на форки автора с суффиксом `-extended-*`. Ключевые: `sagernet/sing` → `shtorm-7/sing` (базовая библиотека всего стека), `sagernet/wireguard-go` → `shtorm-7/wireguard-go` (там живёт обфускация [[amnezia-2-0/reference|Amnezia 2.0]]), `ameshkov/dnscrypt` → `shtorm-7/dnscrypt`, `dolonet/mtg-multi` → `shtorm-7/mtg-multi` (MTProto), `Diniboy1123/connect-ip-go` → `shtorm-7/connect-ip-go` (MASQUE), `sagernet/sing-mux`, `sagernet/sing-vmess`, `sagernet/tailscale`.

> [!note] Следствие для безопасности
> Часть криптографии и сетевого кода живёт не в этом репозитории, а в форках библиотек автора — исправления из соответствующих upstream-библиотек попадают туда только после ручного перебазирования. Это главный практический смысл «отставания» форка, разобранного в [[sing-box/sing-box-extended|обзорной заметке]] (раздел «Отстаёт ли форк от оригинала»).

Масштаб: 1052 Go-файла, Go 1.26. Крупнейшие пакеты — `option/` (71 файл), `route/rule/` (45), `include/` (37), `experimental/libbox/` (35, мобильная обёртка gomobile).

## Протоколы: что своё, а что обёртка

Сводка по реализации протоколов, добавленных форком (подробно о том, что каждый протокол делает, — в [[sing-box/sing-box-extended|обзорной заметке]]):

| Протокол | Путь | Реализация | Роль |
|---|---|---|---|
| WARP | `protocol/warp/` | Своя обвязка Cloudflare API + WireGuard через `shtorm-7/wireguard-go` | endpoint |
| MASQUE | `protocol/masque/` | Обёртка над `connect-ip-go` (CONNECT-IP поверх HTTP/3) | outbound |
| MTProxy | `protocol/mtproxy/` | Обёртка над `mtg-multi` (форк mtg) | только inbound (сервер) |
| Mieru | `protocol/mieru/` | Обёртка над официальным `enfein/mieru/v3` | inbound + outbound |
| OpenVPN | `protocol/openvpn/` + `transport/openvpn/` | Своя (control/data-каналы, tls-auth/tls-crypt/tls-crypt-v2); извне только LZO | outbound |
| TrustTunnel | `protocol/trusttunnel/` | Своя, поверх QUIC/HTTP3 и HTTP/2 | inbound + outbound |
| Sudoku | `protocol/sudoku/` | Своя (собственная крипта, обфускация, мультиплекс, HTTP-маска) | inbound + outbound |
| Snell | `protocol/snell/` | Своя (v4, shadow-AEAD, obfs через simple-obfs) | inbound + outbound |
| SSH-расширения | `protocol/ssh/` | Поверх `x/crypto/ssh`: CA-сертификаты и fallback-сервер | inbound + outbound |
| VPN | `protocol/vpn/` | Своя (туннель с кадрированием поверх любого TCP-канала) | endpoint (client + server) |
| Bond | `protocol/bond/` | Своя (см. ниже) | inbound + outbound |
| Failover | `protocol/failover/` | Своя (см. ниже) | inbound + outbound |

Заимствования из соседних экосистем портированы, а не подключены модулями: транспорт mKCP (`transport/v2raykcp/`) — порт из v2ray-core, [[xray/xhttp|XHTTP]] (`transport/v2rayxhttp/`) — порт из Xray-core вместе со вспомогательным слоем `common/xray/*` (buf, pipe, crypto). Шифрование [[xray/vless|VLESS]] (`protocol/vless/encryption/`) — собственная реализация в стиле Xray на стандартной криптографии Go, включая пост-квантовый ML-KEM (`crypto/mlkem`) поверх X25519.

Параметры [[amnezia-2-0/reference|Amnezia 2.0]] (`jc`, `jmin/jmax`, `s1/s2`, `h1–h4`, `i1–i3`) sing-box лишь прокидывает в IPC-конфиг WireGuard — сам движок junk-пакетов и подменённых заголовков реализован в форке `shtorm-7/wireguard-go`. Опции доступны и для обычного WireGuard-endpoint, и для WARP.

## Группы outbound: Fallback, Failover, Bond

Три механизма отказоустойчивости устроены принципиально по-разному:

- **Fallback** (`protocol/group/fallback.go`) — простая группа над тегами существующих outbound-ов: перебор по порядку, неудачные попадают в чёрный список на `blacklist_timeout` (по умолчанию 1 минута). Работает с любыми серверами, серверная поддержка не нужна.
- **Failover** (`protocol/failover/`) — полноценный клиент-серверный протокол с **восстановлением сессий**. Клиент нумерует кадры и держит кольцевой буфер последних 10 записанных; при разрыве канала он поднимает соединение через следующий outbound (стратегии `sequential`/`cycle`), шлёт `CommandReconnect` с UUID сессии, сервер находит живую сессию по UUID, стороны синхронизируют индексы и переотправляют недошедшие кадры — TCP-сессия приложения переживает смену транспорта прозрачно. Требует failover-inbound на своём сервере.
- **Bond** (`protocol/bond/`) — агрегация каналов: один логический поток режется на куски пропорционально долям `download_ratio`/`upload_ratio` (сумма долей обязана равняться 100) и размазывается по нескольким физическим соединениям с общим UUID; сервер склеивает куски обратно. Конфигом можно, например, пустить весь download через один канал, а upload через другой (`examples/bond/client_split.json`).

Штатные группы `selector`/`urltest` расширены интеграцией с провайдерами (поля `providers`, `use_all_providers`, фильтры `include`/`exclude`) — группа автоматически подхватывает все outbound-ы из подписок. **Unified Delay** реализован в `common/urltest/`: при включённом `experimental.unified_delay` URL-тест делает второй HTTP-запрос и меряет задержку по нему, исключая время установления соединения и TLS-рукопожатия (как в Clash).

## Providers и Link Parser

Провайдеры (`provider/`) бывают трёх типов: `inline` (outbound-ы прямо в конфиге), `local` (файл на диске, перечитывается по fswatch) и `remote` (URL с `update_interval`, ETag-кэшированием, разбором заголовка `subscription-userinfo` и загрузкой через указанный `download_detour`). Распарсенные подписки кэшируются через `cachefile`, поэтому после рестарта outbound-ы восстанавливаются до первого похода в сеть; встроенный health-check гоняет URL-тест по узлам подписки.

Парсер подписок (`parser/`) пробует по очереди четыре формата: sing-box JSON → Clash YAML → SIP008 → список share-ссылок (plain или base64). Link Parser (`parser/link/`) разбирает схемы `vless://`, `vmess://`, `ss://`, `trojan://`, `tuic://`, `hysteria://`, `hy2://`/`hysteria2://` и превращает их в структуры `option.Outbound` — включая маппинг query-параметров VLESS-ссылки в транспорт, uTLS-fingerprint, REALITY (`pbk`/`sid`) и `flow=xtls-rprx-vision`.

Собственной документации по фичам форка нет: mkdocs-сайт в `docs/` — неизменённая документация upstream. Роль документации играют README и подробные комментарии внутри JSON-файлов каталога `examples/` (26 подкаталогов примеров).

## Лимитеры: outbound-обёртки со своим роутером

Четыре лимитера (`protocol/limiter/{bandwidth,traffic,connection,rate}/`) реализованы не как хук в общем роутере, а как **специальные outbound-ы**, которые оборачивают дальнейший путь трафика. Внутри каждый лимитер поднимает собственный вложенный `route.Router` со своими полями `rules`/`final` — ради этого форк сделал роутер переиспользуемым (`route.NewRouter(...)` + `Initialize(...)`). Лимитеры можно выстраивать в цепочку: трафик проходит сквозь несколько обёрток до реального outbound-а.

Механика по типам: **bandwidth** троттлит `Read`/`Write` через token bucket (`x/time/rate`), опционально с честным взвешенным распределением полосы (WFQ) по ключам `user`/`source_ip`/`hwid`/`mux`/`protocol`/`destination`; **traffic** считает байты и рвёт соединение при исчерпании квоты; **connection** берёт счётчик-«лок» перед dial-ом и обрубает лишние соединения; **rate** ограничивает частоту новых соединений (библиотека `gorl`).

Уровень применения задаёт поле `strategy`: `global` (на весь outbound), `connection` (на соединение — по id, IP источника, HWID или mux-сессии), `users` (per-user по списку в конфиге), `manager` (per-user, список приходит динамически от центрального менеджера) и `bypass`. Счётчики трафика — единственное персистентное состояние: узел раз в 5 секунд отправляет дельту менеджеру, тот пишет её в поле `raw_used` таблицы `traffic_limiters` своей БД.

## DNS-расширения

К штатным DNS-транспортам sing-box (udp/tcp/tls/https/h3/quic/local/hosts/fakeip/dhcp/tailscale) форк добавляет два:

- **SDNS/DNSCrypt** (`dns/transport/sdns.go`) — обёртка над библиотекой `ameshkov/dnscrypt/v2` (в сборке — форк `shtorm-7/dnscrypt`); сервер задаётся DNS-стемпом `sdns://`, поддерживаются и DNSCrypt-, и DoH-стемпы.
- **Fallback** (`dns/transport/fallback/`) — агрегатор над списком других DNS-серверов с двумя стратегиями: `parallel` (запрос во все сразу, побеждает первый успешный ответ) и `sequential` (перебор до первого успеха; значение по умолчанию).

## Подсистема управления: manager, node, панель

Самое крупное отличие от upstream — распределённая система управления парком серверов, реализованная пятью типами сервисов: `manager`, `manager-api`, `node-manager-api`, `node`, `admin-panel`. Топология из примера `examples/admin_panel-manager-node/`: центральный хост запускает `manager` + `manager-api` + `node-manager-api` (сервер) + `admin-panel`; каждый VPN-узел — `node` + `node-manager-api` в режиме `client`.

**Manager** (`service/manager/`) — центральный сервис с реляционной БД (SQLite или PostgreSQL, миграции через `golang-migrate`). Хранит пользователей, узлы, лимитеры и «squads» — группы, через которые всё связывается: пользователь, узел и лимитер применяются вместе, если состоят в общем squad.

**Manager API** (`service/manager_api/`) — внешний API для панели и автоматизации: REST на go-chi (префикс `/manager/v1`, CRUD по squads/users/nodes/лимитерам, Swagger UI) и зеркальный gRPC. Аутентификация — статический ключ `api_key` (Bearer-токен, сравнение constant-time).

**Node Manager API** (`service/node_manager_api/`) — отдельный gRPC-протокол связи узла с менеджером. Направление соединения — **от узла к менеджеру** (узлам за NAT не нужны входящие порты): узел вызывает `AddNode(uuid)` и получает долгоживущий server-stream, по которому менеджер пушит полные снапшоты и точечные дельты пользователей и лимитов; при обрыве узел переподключается каждые 5 секунд. Обратные unary-вызовы от узла — `AcquireLock`/`RefreshLock`/`ReleaseLock` (глобальный лимит соединений пользователя сразу на всех узлах) и `AddTrafficUsage` (учёт общей квоты трафика).

**Node** (`service/node/`) — сторона узла: принимает обновления и **вживляет пользователей в работающие inbound-ы без перезапуска**, вызывая `UpdateUsers` у живого инстанса протокола (поддержаны vless, vmess, trojan, tuic, hysteria/hysteria2, shadowsocks, mtproxy, naive, socks, http, anytls, trusttunnel, ssh). Лимитеры со `strategy: "manager"` он связывает с приходящими от менеджера правилами.

**Admin Panel** (`service/admin_panel/`) — SPA на React 18 + TypeScript + Vite + Material UI (страницы: дашборд с графиками, squads, узлы, пользователи, четыре вида лимитеров). Собранный `dist/` закоммичен и встраивается в бинарник через `//go:embed` — Node.js при сборке Go не нужен. Go-сервис панели лишь раздаёт статику; все запросы SPA шлёт напрямую в manager-api, ключ API пользователь вводит на странице логина (хранится в localStorage браузера).

Отдельный от всего этого `daemon/` — локальный gRPC-сервис управления самим запущенным инстансом (стоп/релоад, подписки на логи/соединения, выбор outbound, системный прокси) — аналог [[Clash/01-clash-core|Clash API]] для GUI-клиентов, не связанный с manager-подсистемой.

> [!warning] Замечания по безопасности подсистемы управления
> По состоянию кода на июль 2026: (1) секреты пользователей — UUID, пароли, ключи — хранятся в БД менеджера открытым текстом; (2) аутентификация manager-api и node-manager-api — один статический `api_key` на всех клиентов, без ролей и ротации; (3) панель хранит этот ключ в localStorage браузера. Для продакшн-развёртывания это означает: БД и API-ключ нужно защищать как главный секрет всей инфраструктуры, API — закрывать TLS и firewall-ом, панель — не выставлять в открытый интернет.

## 📚 См. также

- [[sing-box/sing-box-extended|sing-box-extended — обзор]] — что это за форк, список возможностей, отставание от upstream, риски
- [[sing-box/protocols-origin|Откуда код протоколов]] — своя реализация или копия Xray: сравнение ядер sing-box и Xray-core по исходникам
- [[sing-box/hardcoded-defaults|Хардкод-константы и дефолты]] — порты, таймауты и магические числа из `constant/` и кода фич
- [[xray/project-x|Project X / Xray-core]] — соседняя экосистема, из которой форк портировал XHTTP и VLESS encryption
- [[xray/xhttp|XHTTP]] — устройство транспорта, порт которого лежит в `transport/v2rayxhttp/`
- [[xray/vless|Протокол VLESS]] — протокол, чьё шифрование и flow реализованы в `protocol/vless/`
- [[amnezia-2-0/reference|Amnezia 2.0]] — параметры обфускации WireGuard, которые форк прокидывает в свой `wireguard-go`
- [[mtproxy/mtproto-zig|MTProto-прокси]] — протокол, серверную часть которого форк подключает через `mtg-multi`
- [[Hysteria/00-overview|Hysteria]] — протокол, чьи share-ссылки понимает Link Parser
- 🔗 [github.com/shtorm-7/sing-box-extended](https://github.com/shtorm-7/sing-box-extended) — исходники
- 🔗 [каталог examples](https://github.com/shtorm-7/sing-box-extended/tree/extended/examples) — фактическая документация фич форка

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование и скачивание всего репозитория одним zip-архивом доступны на GitHub: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/sing-box/architecture.md) · [весь репозиторий](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main).
