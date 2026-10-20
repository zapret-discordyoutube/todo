---
date: 2026-10-15
tags:
  - zapret-vpn
  - клиенты
  - инструкция
aliases:
  - Приложения для Zapret VPN
  - Чем открыть подписку Zapret
  - Какое приложение скачать для VPN
  - v2rayNG Happ FlClash Clash Mi AmneziaVPN
  - AWG 3.0 или AWG 2.0
description: "Какое приложение поставить для Zapret VPN на Android, iPhone, Windows, Mac, Linux и роутер, какую ссылку взять в боте и как её добавить; AWG 3.0 против AWG 2.0; Telegram через ZaStoGram."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/premium/apps](https://wiki.zapret.moe/premium/apps)

# 📲 Приложения для Zapret VPN: что поставить и какую ссылку взять

> [!info] О чём заметка
> Бот [@zapretvpns_bot](https://telegram.me/zapretvpns_bot) не требует какого-то одного приложения: подписку можно открыть в любом подходящем. Здесь — какое приложение подходит для вашего устройства, какую ссылку для него взять в боте и куда её вставить. Если вы на Android и только начинаете — проще всего [[premium/android|пошаговая инструкция для ZapretKVN]].

> [!tip] Простыми словами
> VPN работает внутри приложения, а ссылка из бота говорит приложению, к каким серверам подключаться. Найдите в таблице своё устройство, поставьте приложение из первой строки и возьмите в боте ту ссылку, что указана рядом. Не уверены — нажмите в боте «🚀 Подключить устройство»: он сам назовёт приложение и даст нужную ссылку.

## TL;DR

- **Android:** ZapretKVN + Xray-подписка. Запасные: v2rayNG, Happ (Xray-подписка), FlClash (Mihomo-подписка).
- **iPhone и iPad:** Clash Mi + Mihomo-подписка. Запасные: Happ, V2RayTun (Xray-подписка), WireGuard.
- **Windows:** Zapret KVN + Xray-подписка. Запасные: v2rayN, Happ (Xray-подписка), Clash Verge Rev (Mihomo-подписка).
- **macOS и Linux:** Clash Verge Rev + Mihomo-подписка. Запасные: Happ, v2rayN, Throne.
- **Ничего не подключается:** AWG 3.0 в AmneziaVPN 5.0.0.5 или новее. AWG 2.0 — прошлое поколение, оставлен для старых приложений и роутеров.
- **Telegram:** наш клиент [ZaStoGram](https://t.me/zastogram) (Android и Windows) — работает даже без VPN.

---

## Сначала — какую ссылку брать в боте

Протокол — стандарт интернета, а не часть Android или iPhone: любой из них открывает весь интернет, включая YouTube и Discord, на любой системе, где есть приложение с его поддержкой. От системы зависит только выбор приложения.

Все ссылки входят в один тариф: советуем 💎 Vless MAX (199 ₽ в месяц), самый дешёвый с VPN — ⚡ MasterVless (99 ₽). Приложение умеет читать не каждую, поэтому сначала выберите приложение, а потом ссылку под него.

| Что взять в боте | Что внутри | Какие приложения читают |
|---|---|---|
| 🔗 **Xray-подписка** | все ваши серверы VLESS одной ссылкой | ZapretKVN, Zapret KVN, v2rayNG, v2rayN, Happ, V2RayTun, V2Box |
| ⚡ **Hysteria 2-подписка** | серверы Hysteria 2 — весь интернет, быстрее на плохой сети и в играх | ZapretKVN, Zapret KVN, v2rayN 7.24.9+, Throne, Husi |
| 🧭 **Mihomo-подписка** | VLESS и Hysteria 2 вместе, российские сайты напрямую; работает на всех системах, не только на iPhone | Clash Mi, FlClash, Clash Verge Rev, Clash Meta for Android |
| 🛡 **WireGuard-конфиг** | один сервер, файл `.conf` | WireGuard, AmneziaVPN, WG Tunnel, роутеры |
| 🗝 **AWG 3.0-конфиг** | WireGuard с сильной маскировкой, файл `.conf` | AmneziaVPN 5.0.0.5+, Throne 1.2.2+, клиенты на ядре Mihomo 1.19.30+ |
| 🔐 **AWG 2.0-конфиг** | прошлое поколение маскировки | AmneziaVPN, AmneziaWG, WG Tunnel, роутеры с AmneziaWG |

Подписка (`https://…`) обновляется: новые серверы приходят по той же ссылке. Конфиг (файл `.conf`) — это один сервер, и обновлять его нужно вручную.

Где это в боте: подписки — «🚀 Подключить устройство» или «🌐 VPN, WireGuard и Telegram» → нужный протокол; конфиги — «🌐 VPN, WireGuard и Telegram» → WireGuard, AWG 3.0 или AWG 2.0 → сервер со значком ➕: бот создаст ключ и пришлёт файл.

## Как скопировать ссылку из бота

В карточке подписки **нажмите на адрес** — Telegram скопирует его. Если бот открыт на компьютере, а подписку добавляете в телефон, нажмите «📲 QR-код» и отсканируйте код приложением на телефоне. Конфиг `.conf` бот присылает файлом: сохраните его («⋮» → «Сохранить в загрузки») и откройте в приложении.

---

## Android

| Приложение | Ссылка из бота | Как добавить |
|---|---|---|
| ⭐ [ZapretKVN](https://git.zapret.moe/zapretkvn/ZapretKVN-android/releases/latest) — наш клиент | Xray- и Hysteria 2-подписка | «Серверы» → «Ссылка» → вставить → «Загрузить preview» → «Один профиль-группа». [[premium/android\|Пошагово со скриншотами]] |
| [v2rayNG](https://github.com/2dust/v2rayNG/releases/latest) | Xray-подписка | меню ☰ → группы подписок → «+» → вставить адрес в поле URL → сохранить; на главном экране «⋮» → обновить подписку; включение — круглая кнопка внизу справа |
| [Happ](https://play.google.com/store/apps/details?id=com.happproxy) (есть в Google Play) | Xray-подписка | «+» в правом верхнем углу → вставка из буфера обмена; включение — большая кнопка |
| [FlClash](https://github.com/chen08209/FlClash) | Mihomo-подписка | «Профили» → «+» → по URL → вставить; затем кнопка запуска на главной |
| [Clash Mi](https://clashmi.app/download) | Mihomo-подписка | добавить профиль по ссылке, выбрать его, включить |
| [AmneziaVPN](https://amnezia.org/downloads) | AWG 3.0- или WireGuard-конфиг | «+» → из файла → выбрать сохранённый `.conf` |
| [WG Tunnel](https://www.wgtunnel.com/) | WireGuard- или AWG 2.0-конфиг | «+» → импорт из файла |

Названия пунктов в чужих приложениях меняются от версии к версии; ищите «Подписки», «Профили», «Add subscription», «+».

> [!tip] Если работает YouTube, а Telegram нет
> В ZapretKVN через VPN идут только отмеченные приложения, а Telegram-копия в «Двойных приложениях» Xiaomi или «Защищённой папке» Samsung не видит VPN вовсе. Разбор и решение — в [[premium/android#Один Telegram работает, а второй нет|инструкции для Android]].

## iPhone и iPad

| Приложение | Ссылка из бота | Как добавить |
|---|---|---|
| ⭐ [Clash Mi](https://clashmi.app/download) | Mihomo-подписка | добавить профиль по ссылке → выбрать → включить; iOS спросит разрешение на VPN-конфигурацию — разрешите |
| [Happ](https://apps.apple.com/us/app/happ-proxy-utility/id6504287215) / [Happ Plus](https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973) | Xray-подписка | «+» → вставка из буфера обмена → большая кнопка включения |
| [V2RayTun](https://apps.apple.com/us/app/v2raytun/id6476628951) | Xray-подписка | «+» → импорт из буфера обмена |
| [AmneziaVPN](https://amnezia.org/downloads) | AWG 3.0- или WireGuard-конфиг | «+» → из файла (файл из Telegram: «Поделиться» → AmneziaVPN) |
| [WireGuard](https://apps.apple.com/app/wireguard/id1441195209) | WireGuard-конфиг | «+» → «Создать из файла или архива» |

В App Store России часть VPN-приложений недоступна; тогда их ставят с Apple ID другой страны. ZapretKVN и ZaStoGram для iPhone нет.

## Windows

| Приложение | Ссылка из бота | Как добавить |
|---|---|---|
| ⭐ [Zapret KVN](https://git.zapret.moe/zapretkvn/zapret-kvn) — наш клиент | Xray- и Hysteria 2-подписка | добавить подписку по ссылке, выбрать сервер, включить |
| [v2rayN](https://github.com/2dust/v2rayN/releases/latest) | Xray- или Hysteria 2-подписка | «Подписки» → «Настройки подписок» → «Добавить» → URL; затем «Обновить подписки». [[premium/v2rayn\|Подробно со скриншотами]] |
| [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) | Mihomo-подписка | «Профили» → вставить ссылку → «Импорт»; включить системный прокси или TUN |
| [Happ](https://github.com/Happ-proxy/happ-desktop/releases/latest) | Xray-подписка | «+» → из буфера обмена |
| [AmneziaVPN](https://amnezia.org/downloads) | AWG 3.0- или WireGuard-конфиг | «+» → из файла |

**Режим «Прокси» или «VPN (TUN)».** В «VPN (TUN)» через сервер идёт весь компьютер, в «Прокси» — только программы, которые берут прокси. Не знаете, что выбрать, — берите TUN; подробно — [[Zapret/premium#Zapret KVN на Windows: «Прокси» или «VPN (TUN)»|чем они отличаются]].

**Адрес прокси ZapretKVN** — на «Панели», в карточке «Режим работы»: в режиме «Прокси» при подключении там строка `SOCKS5: 127.0.0.1:1390 · HTTP: 127.0.0.1:1391`. Его вписывают в программы, которые идут мимо сервера. Telegram подключается кнопкой «Добавить в Telegram» рядом с этой строкой (с версии 0.8.35) — [[Zapret/premium#Telegram и ZapretKVN на Windows в режиме «Прокси»|подробно]]; а ещё проще держать Telegram в [ZaStoGram](https://t.me/zastogram), которому VPN не нужен.

**Какие сервисы открываются через сервер.** После теста скорости в карточке сервера ZapretKVN на Windows появляется строка «Через этот узел» со значками по сервисам: YouTube, Discord, Telegram, Instagram, Facebook, X, WhatsApp, Spotify, ChatGPT, Twitch и LinkedIn. Галочка значит, что сервис отвечает быстро; предупреждение — что ответы идут с паузами, медленно или открывается не каждый адрес сервиса; крестик — что через этот сервер сервис не открывается. Под строкой словами названо, что именно не так, и время проверки. Так видно, что сервер «живой» и быстрый, но, например, YouTube через него замирает, и можно выбрать другой.

**Windows спрашивает: частная или общедоступная сеть?** Приложение, которое пускает через VPN весь компьютер (ZapretKVN, AmneziaVPN, v2rayN в режиме TUN), создаёт в Windows свой сетевой адаптер, и Windows спрашивает, что это за сеть. Выберите **«Общедоступная сеть»** или оставьте как есть: на работу VPN выбор не влияет. «Частная» нужна только для домашней сети, где компьютеры видят друг друга и делятся файлами и принтерами; для VPN это лишнее.

Discord без VPN на весь компьютер — в заметке [[premium/discord|Discord через прокси]]. Бесплатный обход YouTube и Discord без всякого VPN — программа [[Zapret/download|Zapret GUI]].

## macOS и Linux

| Приложение | Ссылка из бота | Как добавить |
|---|---|---|
| ⭐ [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) | Mihomo-подписка | «Профили» → вставить ссылку → «Импорт» |
| [Happ](https://apps.apple.com/us/app/happ-proxy-utility/id6504287215?platform=mac) | Xray-подписка | «+» → из буфера обмена |
| [V2Box](https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690?platform=mac) (macOS) | Xray-подписка | добавить подписку по ссылке |
| [Throne](https://github.com/throneproj/Throne/releases/latest) | Hysteria 2-подписка, AWG 3.0 | добавить группу подписки по URL |
| [AmneziaVPN](https://amnezia.org/downloads) | AWG 3.0- или WireGuard-конфиг | «+» → из файла |

## Роутер

| Прошивка | Что взять в боте |
|---|---|
| с WireGuard (Keenetic, OpenWrt, MikroTik и др.) | WireGuard-конфиг |
| с AmneziaWG | AWG 2.0-конфиг; AWG 3.0 — если прошивка уже знает третье поколение |

На роутер берите отдельный конфиг, а не подписку: прошивки подписки не читают. Каждому устройству — свой конфиг: один и тот же файл на двух устройствах сразу работать не будет.

---

## AWG 3.0 или AWG 2.0

AmneziaWG (AWG) — это WireGuard с маскировкой: к обычным пакетам добавляется «шум», чтобы фильтр провайдера не узнал протокол.

| | AWG 2.0 | AWG 3.0 |
|---|---|---|
| Поколение | прошлое, сентябрь 2025 года | текущее, вышло 24 июля 2026 года |
| Маскировка | мусорные пакеты, случайные заголовки и дополнение пакетов до случайной длины | то же плюс шифрование заголовков пакетов — узнать труднее |
| Приложения | почти все клиенты AmneziaWG и многие роутеры | AmneziaVPN 5.0.0.5+, Throne 1.2.2+, ядро Mihomo 1.19.30+ |
| Когда брать | старое приложение или роутер, который не знает 3.0 | **всегда, когда приложение его поддерживает** |

**А как же AWG 3.1?** 3.1 — не отдельный протокол, а обновление внутри третьего поколения (12 августа 2026 года): формат пакетов тот же, добавлены необязательные настройки. Наши серверы AWG 3.0 уже собраны на коде линии 3.1, поэтому в боте это называется «AWG 3.0», и обновлять приложение ради «3.1» не нужно. Подробно — в разделе [[amnezia-3-0/amnezia-3-0|AmneziaWG 3.0]].

AWG 2.0 в боте остаётся, чтобы не отрезать тех, у кого старое приложение или роутер. Если начинаете с нуля — берите AWG 3.0.

## Telegram: ZaStoGram

Для Telegram советуем наш клиент [ZaStoGram](https://t.me/zastogram) — это Telegram с вашими чатами и аккаунтами, в который встроен обход блокировки через официальные веб-шлюзы Telegram (WSS). Он работает в большинстве сетей **без VPN**, а прокси из бота (MTProxy, TeleMT) работают в нём стабильнее всего.

| Платформа | Где скачать |
|---|---|
| Android | канал [@zastogram](https://t.me/zastogram) или [страница выпусков](https://git.zapret.moe/zastogram/ZaStoGram/releases/latest), файл `ZaStoGram-standalone-arm64-v8a.apk` |
| Windows | канал [@zastogram](https://t.me/zastogram) или [страница выпусков ZaStoGram Desktop](https://git.zapret.moe/zastogram/ZaStoGram_desktop/releases/latest), файл `ZaStoGram-x64.exe` |

ZaStoGram ставится рядом с обычным Telegram. В одном приложении можно держать до трёх аккаунтов (с Telegram Premium — до пяти), поэтому клоны Telegram не нужны. Голосовые звонки идут мимо WSS, напрямую: если они не соединяются, поможет VPN или пакетный обход zapret. WSS и прокси из бота одновременно не работают: при включённом прокси WSS приостанавливается, а после его выключения ZaStoGram сам возвращается на WSS.

## Источники

- Списки совместимых приложений — тексты бота [@zapretvpns_bot](https://telegram.me/zapretvpns_bot) на 15 октября 2026 года (карточки подписок, меню AWG 3.0, мастер подключения).
- Версии AmneziaWG — разделы вики [[amnezia-2-0/amnezia-2-0|AmneziaWG 2.0]] и [[amnezia-3-0/amnezia-3-0|AmneziaWG 3.0]]; версия модуля на серверах — исходники компонента `awg-core` проекта.
- [ZaStoGram](https://git.zapret.moe/zastogram/ZaStoGram) и [ZaStoGram Desktop](https://git.zapret.moe/zastogram/ZaStoGram_desktop) — исходный код и выпуски.

## 📚 См. также

- [[premium/glossary|📘 Что есть что]] — коротко обо всём и словарь терминов.
- [[premium/guides|📚 Все инструкции Zapret VPN]] — оглавление всех статей.
- [[premium/android|VPN на Android: ZapretKVN по шагам]] — со скриншотами каждого экрана.
- [[Zapret/premium|Zapret VPN и Zapret Premium: гайд для новичка]] — тарифы, оплата, выбор протокола.
- [[premium/v2rayn|v2rayN и режим прокси]] — подробная настройка на Windows.
- [[Clash/03-first-run|Первый запуск Clash/mihomo]] — как устроены клиенты на ядре Mihomo.

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/premium/apps.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
