#!/usr/bin/env python3
"""Описания схем, заменяющих ASCII-блоки в заметках вне Zapret2/desync.
Подключается из wiki-anim.py: register(FIGS, hub, wrapped, B), где B — построители
chain, stack, seq, compare, fields из wiki-anim-more.py."""


def register(FIGS, hub, wrapped, B):
    Fig = hub.Fig
    chain, stack, seq, compare, fields = B["chain"], B["stack"], B["seq"], B["compare"], B["fields"]

    def add(name, folder, fn):
        FIGS[name] = (fn, folder)

    # ═══ AmneziaWG 2.0 ═══════════════════════════════════════════════
    add("awg-messages", "amnezia-2-0/attachments", lambda: fields(
        "awg-messages", "Четыре сообщения AmneziaWG: размеры полей по масштабу",
        "Handshake Initiation 148 байт, Handshake Response 92 байта, Cookie Reply 64 байта и Transport от 16 байт. Ширина поля пропорциональна его размеру в байтах; "
        "первое поле каждого сообщения — тип, в котором стоит магический заголовок H1, H2, H3 или H4.",
        [("Handshake Initiation", [("Type · H1", 4, ""), ("Sender", 4, ""), ("Ephemeral", 32, ""), ("Static: 32 + тег 16", 48, ""),
                                  ("Timestamp: 12 + тег 16", 28, ""), ("MAC1", 16, ""), ("MAC2", 16, "")], "148 байт"),
         ("Handshake Response", [("Type · H2", 4, ""), ("Sender", 4, ""), ("Receiver", 4, ""), ("Ephemeral", 32, ""), ("Empty: тег", 16, ""),
                                 ("MAC1", 16, ""), ("MAC2", 16, "")], "92 байта"),
         ("Cookie Reply", [("Type · H3", 4, ""), ("Receiver", 4, ""), ("Nonce", 24, ""), ("Cookie: 16 + тег 16", 32, "")], "64 байта"),
         ("Transport", [("Type · H4", 4, ""), ("Receiver", 4, ""), ("Counter", 8, ""), ("Ciphertext + тег Poly1305 16", (60, "переменный"), "")], "от 16 байт")],
        "amnezia-2-0/attachments", foot="Числа внутри полей — размер в байтах. Перед сообщением может стоять S1, S2, S3 или S4 случайных байт."))

    def awg_handshake():
        f = Fig("awg-handshake", 452, 16, "Что уходит в сеть при handshake и передаче данных в AmneziaWG 2.0",
                "Init: сигнатурные пакеты i1–i5, затем Jc мусорных пакетов, затем сообщение Init с префиксом S1; всё одним вызовом SendBuffers. "
                "Response: префикс S2 и 92 байта. Cookie Reply под нагрузкой: S3 и 64 байта. Transport: S4, заголовок 16 байт, шифртекст и тег; у keepalive S4 не применяется.")
        rows = [("Init", "каждые ~2 минуты", [("i1", 44), ("i2", 44), ("i3", 44), ("i4", 44), ("i5", 44), ("Junk × Jc", 110), ("S1 random", 90), ("Init · 148 Б", 120)], "всё одним вызовом peer.SendBuffers"),
                ("Response", "ответ на Init", [("S2 random", 100), ("Response · 92 Б", 150)], "i1–i5 и junk с Response не отправляются"),
                ("Cookie Reply", "под нагрузкой", [("S3 random", 100), ("Cookie · 64 Б", 140)], "уходит напрямую, не через peer queue"),
                ("Transport", "данные", [("S4 random", 100), ("заголовок 16 Б", 150), ("шифртекст", 170), ("тег 16 Б", 90)], "у keepalive S4 не применяется")]
        for r, (name, sub, chips, note) in enumerate(rows):
            y = 20 + r * 102
            t0 = 0.4 + r * 3.4
            f.g(f.text(2, y + 18, name, "tk") + f.text(2, y + 38, sub, "mu sm"), f.vis(t0, fade=0.3))
            x = 160
            for k, (lab, w) in enumerate(chips):
                t = t0 + 0.3 + k * 0.3
                kind = "bxd" if ("random" in lab or lab.startswith("Junk") or lab.startswith("i")) else "bxa"
                f.g(f.chip(x + w / 2, y + 28, w - 6, 40, lab, kind, "mk sm"), f.go([(0, -16, 0, 0), (t, -16, 0, 0), (t + 0.15, -16, 0, 1), (t + 0.5, 0, 0, 1)]))
                x += w
            f.g(f.text(160, y + 72, note, "mu sm"), f.vis(t0 + 1.8, fade=0.3))
        f.g(f.text(2, 436, "Пунктирные блоки — маскировка (случайные байты и мусор), сплошные — настоящие сообщения WireGuard.", "mu sm"), f.vis(13.6))
        return f
    add("awg-handshake", "amnezia-2-0/attachments", awg_handshake)

    add("awg2-wire", "amnezia-2-0/attachments", lambda: fields(
        "awg2-wire", "Transport-пакет AmneziaWG 2.0 на проводе",
        "Пакет состоит из S4 случайных байт, заголовка WireGuard Transport в 16 байт (H4, получатель, nonce), зашифрованной нагрузки с выравниванием и тега Poly1305 16 байт.",
        [("Итоговый пакет", [("S4 random", (50, "S4")), ("H4 + recv + nonce: заголовок", (16, "16")), ("encrypted(payload + выравнивание)", (60, "перем.")), ("Poly1305", (16, "16"))], "S4 + 16 + payload + 16")],
        "amnezia-2-0/attachments", foot="Заголовок записывается в LittleEndian; сдвиг на S4 байт делается, только если пакет не keepalive."))

    add("awg3-wire", "amnezia-3-0/attachments", lambda: fields(
        "awg3-wire", "Пакеты AmneziaWG 3.0 на проводе: nonce и псевдослучайность",
        "В 3.0 пакет открывается 12 байтами nonce, остаток префикса S случайный, а заголовок и сообщение зашифрованы ChaCha20: на проводе сплошная псевдослучайность. "
        "Размер Init всегда S1 + 148 байт для данной конфигурации.",
        [("Transport", [("nonce", (12, "12")), ("остаток S4 (S4−12)", (30, "S4−12")), ("заголовок, ChaCha20: тип · получатель · счётчик", (16, "16")), ("шифртекст + content padding", (60, "перем.")), ("Poly1305", (16, "16"))], ""),
         ("Init", [("nonce", (12, "12")), ("остаток S1 (S1−12)", (30, "S1−12")), ("148 Б сообщения, зашифровано целиком", (110, "148"))], "S1 + 148 байт")],
        "amnezia-3-0/attachments"))

    # ═══ Локальный трекинг и SOCKS5 ═══════════════════════════════════
    def loopback():
        f = Fig("loopback", 320, 11, "127.0.0.1 общий для всех процессов устройства",
                "Яндекс, шпионское приложение и браузер обращаются к одному и тому же 127.0.0.1. Этот адрес общий для всех процессов, не маршрутизируется через VPN или TUN, "
                "не изолирован между профилями и не требует специальных разрешений.")
        apps = [("Приложение A", "Яндекс"), ("Приложение B", "шпион"), ("Браузер", "Chrome")]
        for k, (a, b) in enumerate(apps):
            x = 40 + k * 300
            t = 0.4 + k * 0.7
            f.g(f.rect(x, 20, 220, 62, "bxr" if k == 1 else "bx", rx=8) + f.text(x + 110, 48, a, ("rej tk c sm" if k == 1 else "tk c sm")) + f.text(x + 110, 68, b, "mu sm c") +
                f.arrow(x + 110, 86, x + 110, 124, "r" if k == 1 else "f"), f.vis(t, dy=-8))
        f.g(f.rect(20, 128, 920, 120, "bxa", rx=10) + f.text(480, 156, "127.0.0.1 (loopback)", "tk c") +
            f.text(60, 190, "общий для всех процессов устройства", "t sm") + f.text(60, 214, "не маршрутизируется через VPN или TUN", "t sm") +
            f.text(500, 190, "не изолирован между профилями", "t sm") + f.text(500, 214, "не требует специальных разрешений", "t sm"), f.vis(3.0))
        f.g(f.text(2, 284, "Любое приложение может постучаться на порт другого приложения и получить ответ.", "tk sm"), f.vis(5.0))
        return f
    add("loopback", "attachments", loopback)

    add("yandex-metrica", "attachments", lambda: seq(
        "yandex-metrica", "Яндекс.Метрика: браузер узнаёт идентификаторы у приложения по localhost",
        "JavaScript Яндекс.Метрики в браузере обращается по HTTP на локальные порты 29009 и 30102 (HTTPS — 29010 и 30103), где слушает SDK Метрики в нативном приложении Яндекса. "
        "Приложение отвечает 200 OK с AAID и зашифрованными ID, а браузер отправляет их на mc.yango.com.",
        [("Браузер", "Яндекс.Метрика JS"), ("Приложение Яндекса", "SDK Метрики слушает порты"), ("mc.yango.com", "сервер Яндекса")],
        [(0, 1, "HTTP на localhost", "порты 29009, 30102 (HTTP) и 29010, 30103 (HTTPS)", "a"),
         (1, 0, "200 OK + идентификаторы", "AAID и зашифрованные ID", "r"),
         (0, 2, "отправляет ID", "связка веб-сессии с идентификатором устройства", "r")],
        "attachments", aw=210))

    add("meta-pixel", "attachments", lambda: seq(
        "meta-pixel", "Meta Pixel: веб-сессия связывается с устройством и аккаунтом через localhost",
        "Meta Pixel в браузере кладёт значение cookie _fbp в поле ice-ufrag (SDP Munging) и шлёт STUN-запрос на порты 12580–12585 фонового сервиса Facebook или Instagram. "
        "Приложение получает _fbp и отправляет в graph.facebook.com GraphQL-запрос с _fbp, Device ID и Facebook Account ID; сам браузер шлёт _fbp на facebook.com/tr.",
        [("Браузер", "Meta Pixel JS"), ("Facebook / Instagram", "фоновый сервис в приложении"), ("Серверы Meta", "серверы facebook.com")],
        [(0, 1, "WebRTC STUN: ice-ufrag = _fbp", "SDP Munging; TCP 12387, 12388; UDP 12580–12585 (STUN), 12586–12591 (TURN)", "a"),
         (0, 2, "_fbp + URL, событие, метаданные", "браузер шлёт на facebook.com/tr", "f"),
         (1, 2, "GraphQL: _fbp + Device ID + Account ID", "graph.facebook.com/graphql", "r")],
        "attachments", foot="Итог: веб-сессия, устройство и аккаунт Facebook оказываются связаны.", aw=220))

    add("socks5-spy", "attachments", lambda: chain(
        "socks5-spy", "Как шпионский модуль получает выходной IP через открытый SOCKS5",
        "Модуль в приложении сканирует порты localhost, находит SOCKS5 без аутентификации на 127.0.0.1:10808, проводит handshake с методом 0x00, открывает CONNECT на ifconfig.me:80 "
        "и получает ответ с выходным IP VPN-сервера.",
        [("Шпионский модуль в приложении", "Яндекс, WB, Ozon, государственное приложение"),
         ("127.0.0.1:10808", "1. сканирование портов localhost занимает секунды; xray-core inbound, SOCKS5 без аутентификации"),
         ("xray-core outbound", "2. SOCKS5 handshake: method 0x00, NO AUTH. 3. CONNECT ifconfig.me:80"),
         ("VPN-сервер → ifconfig.me", "ответ: «185.xxx.xxx.xxx»"),
         ("Шпион получает выходной IP", "4. выходной адрес VPN раскрыт")],
        "attachments", vertical=True, warn=(4,)))

    def socks5_bypass():
        f = Fig("socks5-bypass", 330, 14, "Шпион идёт мимо VpnService, поэтому per-app split tunneling не помогает",
                "Обычное приложение проходит VpnService, tun2socks и SOCKS5 xray до VPN-сервера и интернета. Шпион обращается прямо на 127.0.0.1:10808 минуя VpnService, "
                "поэтому исключение приложений из туннеля его не останавливает.")
        steps = [("Приложение", "обычное"), ("VpnService", "Android, TUN"), ("tun2socks", "TUN → SOCKS"), ("SOCKS5 xray", "localhost:10808"), ("VPN-сервер", "VLESS/Trojan/SS"), ("Интернет", "freedom")]
        W = 134
        f.add(f.text(2, 26, "обычный путь трафика", "cap"))
        for k, (a, b) in enumerate(steps):
            x = 2 + k * (W + 30)
            t = 0.4 + k * 0.7
            kind = "bxa" if k == 3 else "bx"
            f.g(f.rect(x, 40, W, 70, kind, rx=8) + f.text(x + W / 2, 70, a, "tk c sm") + f.text(x + W / 2, 92, b, "mu sm c") + (f.arrow(x + W + 4, 75, x + W + 26, 75, "f") if k < 5 else ""), f.vis(t, dy=8))
        x3 = 2 + 3 * (W + 30) + W / 2
        f.add(f.text(2, 168, "путь шпиона", "cap"))
        f.g(f.rect(2, 184, W, 70, "bxr", rx=8) + f.text(2 + W / 2, 214, "Шпион", "rej tk c sm") + f.text(2 + W / 2, 236, "приложение", "mu sm c"), f.vis(6.0, dy=8))
        f.g(f'<path class="{f.c("sl-r")}" d="M{2 + W + 4} 219H{x3}V{114}"/>' + f.head(x3, 114, -1.5708, "r") + f.text(300, 210, "прямо на 127.0.0.1:10808, минуя VpnService", "rej tk sm"), f.vis(7.0))
        f.g(f.text(2, 312, "Исключение приложений из VPN на уровне VpnService шпиона не останавливает: он ходит на localhost.", "tk sm"), f.vis(10.0))
        return f
    add("socks5-bypass", "attachments", socks5_bypass)

    add("grpc-chain", "attachments", lambda: chain(
        "grpc-chain", "Цепочка атаки через открытый gRPC API прокси-ядра",
        "Шпион сканирует порты, находит gRPC API без авторизации, через ReflectionService узнаёт список методов, через HandlerService выгружает конфиг outbound и получает ключ шифрования, "
        "IP сервера и SNI; вместе со второй уязвимостью конфигурации это позволяет расшифровать трафик.",
        [("Шпион", "сканирует порты"), ("gRPC API", "без аутентификации"), ("ReflectionService", "список методов"), ("HandlerService", "дамп outbound-конфига"),
         ("Ключ, IP сервера, SNI", "+ вторая уязвимость → расшифровка трафика")],
        "attachments", warn=(4,)))

    add("uid-isolation", "attachments", lambda: compare(
        "uid-isolation", "Пароль на localhost защищён изоляцией процессов Android",
        "VPN-клиент с UID 10150 подключается к 127.0.0.1:10808 с паролем открытым текстом, но данные видит только ядро и этот UID. Шпион с UID 10200 может сделать connect к порту, "
        "но ему нужен пароль, а читать чужой сокет он не может.",
        ("VPN-клиент (UID 10150)", ["TCP → 127.0.0.1:10808", "«user=abc pass=xyz» — открытым текстом", "ядро: только UID 10150 видит эти данные"]),
        ("Шпион (UID 10200)", ["connect() к :10808 проходит, но нужен пароль — отказ", "read() чужого сокета невозможен"]),
        "attachments", lk="bxa", rk="bxr"))

    add("android-localhost", "attachments", lambda: compare(
        "android-localhost", "Без root блокировщики не видят localhost",
        "Приложение A обращается на 127.0.0.1:10808 к xray или sing-box: это localhost, он не проходит через VPN API. NetGuard и RethinkDNS как VPN перехватывают только реальные интерфейсы "
        "eth0, wlan0 и rmnet0, поэтому трафик приложения B к google.com они видят, а локальные обращения нет.",
        ("Приложение A → 127.0.0.1:10808", ["это localhost: не проходит через VPN API", "блокировщики локальный трафик не видят"]),
        ("Приложение B → google.com", ["VPN перехватывает: eth0, wlan0, rmnet0", "NetGuard и RethinkDNS видят только реальные интерфейсы"]),
        "attachments", lk="bxr", rk="bxa"))

    add("own-socks5", "attachments", lambda: compare(
        "own-socks5", "Где включать пароль, если вы не владелец подписки",
        "Сервер VLESS Reality принадлежит владельцу подписки, и вы его не контролируете. Локальный SOCKS5 inbound на localhost:10808 находится на вашем устройстве: именно там вы меняете настройку auth: password.",
        ("Сервер (владелец подписки)", ["VLESS Reality inbound", "вы его не контролируете"]),
        ("Ваше устройство (вы контролируете)", ["xray outbound (VLESS) — туннель к серверу", "SOCKS5 inbound localhost:10808 — ваш", "auth: password — менять здесь"]),
        "attachments", lk="bx", rk="bxa"))

    # ═══ DPI и протоколы ══════════════════════════════════════════════
    add("olcrtc-chain", "DPI/attachments", lambda: chain(
        "olcrtc-chain", "Как olcrtc прячет трафик в звонок WebRTC",
        "Приложение отправляет трафик в SOCKS5 на 127.0.0.1:8808, клиент olcrtc cnc передаёт его через WebRTC и SFU-сервис вроде Jitsi, Телемоста или WbStream на сервер olcrtc srv, который выходит в интернет.",
        [("Приложение", ""), ("SOCKS5", "127.0.0.1:8808"), ("olcrtc cnc", "клиент"), ("WebRTC / SFU", "Jitsi, Телемост, WbStream"), ("olcrtc srv", "сервер"), ("Интернет", "")],
        "DPI/attachments", accent=(3,)))

    add("telegram-wss-stack", "mtproxy/attachments", lambda: stack(
        "telegram-wss-stack", "Из каких слоёв состоит соединение Telegram по WebSocket",
        "Соединение открывается на TCP 443 к адресу релея, поверх идёт настоящий TLS с именем сервера kwsN.web.telegram.org, затем HTTP/1.1 Upgrade до WebSocket, бинарные кадры, "
        "obfuscated2 с шифром AES-256-CTR и внутри MTProto с шифрованием ключом авторизации.",
        [("TCP :443", "соединение с адресом релея"), ("TLS 1.2+", "настоящий TLS, имя сервера kwsN.web.telegram.org"), ("HTTP/1.1 Upgrade", "GET /apiws → 101 Switching Protocols"),
         ("кадры WebSocket", "бинарные, каждый замаскирован клиентом"), ("obfuscated2", "64-байтный заголовок и шифр AES-256-CTR"), ("MTProto", "шифрование клиент ↔ Telegram ключом авторизации")],
        "mtproxy/attachments"))

    add("vless-encryption-layers", "xray/attachments", lambda: chain(
        "vless-encryption-layers", "VLESS Encryption — ещё один слой поверх открытого соединения",
        "Приложение со своим TLS до сайта передаёт данные протоколу VLESS (версия, UUID, адрес назначения), затем идёт новый слой VLESS Encryption, который шифрует всё, что выше, "
        "потом транспорт и слой безопасности.",
        [("приложение", "браузер, его собственный TLS до сайта"), ("протокол VLESS", "версия, UUID, адрес назначения"), ("VLESS Encryption", "новый слой: шифрует всё, что выше"),
         ("транспорт", "RAW TCP, XHTTP, WebSocket, gRPC, mKCP"), ("слой безопасности", "TLS, REALITY или none")],
        "xray/attachments", vertical=True, accent=(2,)))

    add("xray-lineage", "xray/attachments", lambda: chain(
        "xray-lineage", "От Shadowsocks до Xray: родословная",
        "Shadowsocks 2012 года стал идейным предшественником V2Ray 2015 года, который написан с нуля. После исчезновения автора V2Ray продолжило сообщество как v2fly в 2020, "
        "а в ноябре 2020 из-за лицензионного спора об XTLS от коммита 9a03cc5 отделился Xray-core с VLESS, XTLS-Vision, REALITY и XHTTP.",
        [("Shadowsocks", "2012, clowwindy"), ("V2Ray / Project V", "2015, написан с нуля"), ("v2fly/v2ray-core", "2020, сообщество; сегодня это «V2Ray»"), ("XTLS/Xray-core", "2020, RPRX; VLESS, Vision, REALITY, XHTTP")],
        "xray/attachments", edges={0: "идейный преемник, не форк", 1: "форк кода, 2019", 2: "форк от 9a03cc5, ноябрь 2020"}, accent=(3,)))

    add("vless-flow-chain", "xray/attachments", lambda: chain(
        "vless-flow-chain", "Почему «без flow лучше»: цепочка причин",
        "Цель — уменьшить число внешних TLS-соединений к серверу. Это делает Mux.Cool, но он несовместим с Vision, поэтому flow приходится оставить пустым. "
        "Соединений становится меньше, и фильтр по их количеству не срабатывает.",
        [("цель", "уменьшить число внешних TLS-соединений к серверу"), ("Mux.Cool", "классический мультиплексор протокола"), ("несовместим с Vision", "TCP-поток внутри mux рвёт mux-соединение"),
         ("flow пустой", "приходится выставить пустым"), ("соединений меньше", "фильтр по их количеству не срабатывает")],
        "xray/attachments", vertical=True, accent=(4,)))

    add("dpi-funnel", "DPI/attachments", lambda: chain(
        "dpi-funnel", "Анализ трафика идёт воронкой: чем дальше, тем дороже",
        "DPI проверяет поток по ступеням: первые пакеты дают отпечаток ОС, первые байты — протокольный маркер, ClientHello — JA3 и JA4, далее сертификат, метаанализ потока и после 16 КБ "
        "поведенческий ML-классификатор. Итог — пропустить, RST, drop или throttle.",
        [("пакеты 1–5 (TCP/IP)", "TTL, TCP-опции (MSS/WS/SACK/TS) → отпечаток ОС"), ("байты 0–5 (сигнатура)", "протокольный маркер: 16 03 01… / SSH-2.0- / …"),
         ("байты 6–300 (TLS hello)", "ClientHello → JA3 / JA4, фингерпринт клиента"), ("байты 300–3000", "сертификат: CT-логи, ASN, CN/SAN ↔ SNI; в TLS 1.3 он шифруется, остаются SNI и ASN"),
         ("байты 3000–16000", "метаанализ потока: размеры, тайминги, соотношение in/out, длительность"), ("после 16 КБ", "поведенческий ML-классификатор"),
         ("вердикт", "пропустить, RST, drop или throttle")],
        "DPI/attachments", vertical=True, accent=(6,), lw=300))

    add("faketls-handshake", "Zapret/attachments", lambda: seq(
        "faketls-handshake", "FakeTLS handshake в MTProxy: клиент и сервер изображают обычный TLS",
        "Клиент отправляет фейковый TLS ClientHello на 517 байт с SNI из секрета и HMAC-SHA256 в поле Random. Сервер отвечает фейковым ServerHello и ChangeCipherSpec, копируя размер ответа реального сертификата. "
        "Дальше идут записи Application Data с зашифрованным MTProto до 16408 байт.",
        [("Клиент", "Telegram"), ("Сервер", "MTProxy")],
        [(0, 1, "Фейковый TLS ClientHello, 517 байт", "SNI — домен из секрета (например, google.com); Random содержит HMAC-SHA256 для проверки секрета", "a"),
         (1, 0, "Фейковый ServerHello + ChangeCipherSpec", "имитирует ответ реального TLS-сервера; размер ответа копирует настоящий сертификат домена", "f"),
         (0, 1, "Application Data, тип 0x17", "внутри зашифрованный MTProto; максимальный размер записи 16408 байт", "a")],
        "Zapret/attachments", aw=180))

    add("zig-wire", "mtproxy/attachments", lambda: seq(
        "zig-wire", "Что происходит на проводе: карта защит mtproto.zig",
        "ClientHello несёт почерк клиента, ТСПУ снимает отпечаток, сервер тоже пишет его в лог. ServerHello сервер дробит desync. Затем идёт 64-байтный MTProto-хендшейк, и если соединение живо, сервер проксирует его в DC.",
        [("Клиент", "Telegram"), ("ТСПУ", "наблюдатель"), ("Сервер", "mtproto.zig")],
        [(0, 1, "ClientHello (почерк!)", "ТСПУ снимает фингерпринт; здесь же и блокировка", "r"),
         (1, 2, "ClientHello", "сервер снимает fp в лог", "f"),
         (2, 0, "ServerHello, дроблёный desync", "защиты: mask, desync, drs", "a"),
         (0, 2, "64-байтный MTProto-хендшейк", "если соединение живо: proxy → DC", "a")],
        "mtproxy/attachments", aw=170))

    add("ja4-sni-order", "mtproxy/attachments", lambda: chain(
        "ja4-sni-order", "Почему JA4 и SNI меняются только на стороне клиента",
        "Telegram сам генерирует ClientHello с JA4 и SNI, цензор видит этот почерк, и только после этого пакет приходит на сервер-прокси, который ничего изменить уже не может.",
        [("Telegram", "генерирует ClientHello: JA4 + SNI"), ("Цензор", "видит почерк"), ("Сервер-прокси", "пакет приходит уже после цензора")],
        "mtproxy/attachments", warn=(1,)))

    add("ja4-parts", "DPI/attachments", lambda: fields(
        "ja4-parts", "Как читается JA4: t13d1516h2",
        "t — транспорт TCP, 13 — версия TLS 1.3, d — SNI присутствует, 15 — число шифров, 16 — число расширений, h2 — ALPN HTTP/2.",
        [("t13d1516h2", [("транспорт: TCP", (10, "t")), ("версия TLS: 1.3", (14, "13")), ("SNI есть (d = domain)", (10, "d")), ("шифров: 15", (14, "15")), ("расширений: 16", (14, "16")), ("ALPN: http/2", (14, "h2"))], "")],
        "DPI/attachments", W=640))

    def nginx_split():
        f = Fig("nginx-split", 330, 10, "nginx stream разводит трафик по SNI: сайт отдельно, MTProto отдельно",
                "Порт 443 принимает nginx stream или haproxy на уровне L4 с ssl_preread. Если SNI равен example.com, соединение уходит на настоящий HTTPS-сайт на 127.0.0.1:8443; "
                "если SNI пустой или неизвестный (iOS, Android, Desktop), на MTProto Proxy с FakeTLS на 127.0.0.1:2443.")
        f.add(f.rect(280, 8, 400, 66, "bxa") + f.text(480, 34, "порт 443 → nginx stream / haproxy", "tk c") + f.text(480, 56, "L4 TCP: ssl_preread / inspect", "mu sm c"))
        for k, (x, sni, sub, dest, d2, kind) in enumerate([(30, "SNI = example.com", "", "127.0.0.1:8443", "Nginx HTTPS: реальный сайт", "bx"),
                                                         (500, "SNI пустой или неизвестный", "iOS, Android, Desktop", "127.0.0.1:2443", "MTProto Proxy (FakeTLS)", "bxa")]):
            t = 1.0 + k * 2.2
            f.g(f.arrow(480, 78, x + 210, 130, "f"), f.vis(t, fade=0.2))
            f.g(f.rect(x, 134, 420, 58, "bx", rx=8) + f.text(x + 14, 160, sni, "tk sm") + f.text(x + 14, 180, sub, "mu sm"), f.vis(t + 0.3))
            f.g(f.arrow(x + 210, 196, x + 210, 226, "a" if k else "f"), f.vis(t + 0.8, fade=0.2))
            f.g(f.rect(x, 230, 420, 62, kind, rx=8) + f.text(x + 14, 256, dest, "mk sm") + f.text(x + 14, 278, d2, "tk sm"), f.vis(t + 1.1))
        return f
    add("nginx-split", "Zapret/attachments", nginx_split)

    add("asn-match", "Zapret/attachments", lambda: compare(
        "asn-match", "SNI и IP сервера должны принадлежать одному ASN",
        "Плохо: VPS в сети Hetzner (AS24940), а SNI указывает на www.google.com (AS15169): ASN не совпадают, это подозрительно. Хорошо: SNI на другом сайте в Hetzner (AS24940): один ASN выглядит как обычный shared hosting.",
        ("Плохо", ["VPS IP: 167.235.x.x (Hetzner, AS24940)", "SNI: www.google.com (AS15169)", "ASN не совпадают — подозрительно"]),
        ("Хорошо", ["VPS IP: 167.235.x.x (Hetzner, AS24940)", "SNI: some-site.de (тоже Hetzner, AS24940)", "один ASN — нормально, shared hosting"]),
        "Zapret/attachments"))

    add("bot-apply", "Zapret/attachments", lambda: compare(
        "bot-apply", "Как бот меняет секреты прокси: сейчас и в цели",
        "Сейчас бот по SSH дописывает секрет в secrets.conf и перезапускает mtproxy. Цель — отправлять HTTP POST на /v1/users, и telemt применяет пользователя на лету без перезапуска.",
        ("Сейчас", ["Бот → SSH", "echo secret >> secrets.conf", "systemctl restart mtproxy"]),
        ("Цель", ["Бот → HTTP POST /v1/users", "telemt применяет на лету", "перезапуск не нужен"]),
        "Zapret/attachments"))

    add("wf-pipeline", "Zapret2/attachments", lambda: chain(
        "wf-pipeline", "Порядок фильтрации: сначала WinDivert, потом фильтры nfqws",
        "Все пакеты сетевого стека сначала проходят фильтр WinDivert --wf-* на уровне драйвера: остальные идут мимо nfqws напрямую в сеть. Захваченные пакеты проходят фильтры nfqws по портам, IP и доменам, и к ним применяются desync-действия.",
        [("Сетевой стек", "все пакеты"), ("1. WinDivert-фильтр --wf-*", "уровень драйвера; остальные пакеты идут мимо nfqws напрямую в сеть"),
         ("2. --filter-tcp/udp", "фильтр по портам"), ("3. --ipset", "фильтр по IP"), ("4. --hostlist", "фильтр по доменам (из payload)"), ("5. desync actions", "применение обхода DPI")],
        "Zapret2/attachments", vertical=True, accent=(5,)))

    def mtproto_conntrack():
        f = Fig("mtproto-conntrack", 330, 14, "Как распознаётся MTProto: протокол запоминается, тип пакета нет",
                "Первые три пакета TCP не несут данных. Первый пакет с данными даёт payload mtproto_initial и протокол MTProto. Последующие пакеты выглядят как зашифрованный мусор, payload у них unknown, "
                "но протокол потока MTProto уже сохранён в conntrack.")
        pk = [("SYN", "empty", "bx"), ("SYN+ACK", "empty", "bx"), ("ACK", "empty", "bx"), ("DATA #1", "mtproto_initial", "bxa"), ("DATA #2", "unknown", "bx"), ("DATA #3", "unknown", "bx")]
        f.add(f.arrow(2, 40, 950, 40, "f"))
        f.add(f.text(2, 28, "время", "cap"))
        for k, (a, b, kind) in enumerate(pk):
            x = 76 + k * 150
            t = 0.5 + k * 1.0
            f.g(f.chip(x, 90, 110, 40, a, kind, "mk sm") + f.text(x, 134, "payload=", "mu sm c") + f.text(x, 154, b, "tk sm c" if b != "empty" else "mu sm c"), f.go([(0, -20, 0, 0), (t, -20, 0, 0), (t + 0.15, -20, 0, 1), (t + 0.5, 0, 0, 1)]))
        f.g(f.line(76 + 3 * 150 - 60, 176, 76 + 3 * 150 - 60, 196, "la") + f.text(76 + 3 * 150, 196, "proto = mtproto: определён и сохранён", "acc tk sm") +
            f.text(76 + 3 * 150, 218, "seq_last − seq0 = 1", "m mu sm"), f.vis(6.2))
        f.g(f.text(76 + 4 * 150 - 60, 250, "payload = unknown,", "rej tk sm") + f.text(76 + 4 * 150 - 60, 270, "proto = mtproto (сохранён)", "mu sm") + f.text(76 + 4 * 150 - 60, 290, "seq_last − seq0 > 1", "m mu sm"), f.vis(8.0))
        f.g(f.text(2, 316, "Поэтому desync нужен именно на пакете mtproto_initial: дальше он выглядит как мусор.", "tk sm"), f.vis(10.0))
        return f
    add("mtproto-conntrack", "Zapret2/attachments", mtproto_conntrack)

    add("mtproto-l7-cache", "Zapret2/attachments", lambda: compare(
        "mtproto-l7-cache", "Conntrack запоминает протокол: на втором пакете детекция не нужна",
        "На первом пакете mtproto_initial conntrack-запись по ip:port имеет l7proto UNKNOWN, срабатывает IsMTProto() и сохраняется l7proto = MTPROTO. На втором пакете, зашифрованном мусоре, l7proto уже MTPROTO, детекция не нужна.",
        ("Пакет 1 (mtproto_initial)", ["conntrack lookup по (ip:port)", "ctrack->l7proto = UNKNOWN", "детекция: IsMTProto() = true", "сохранение: ctrack->l7proto = MTPROTO"]),
        ("Пакет 2 (зашифрованный мусор)", ["conntrack lookup по (ip:port)", "ctrack->l7proto = MTPROTO — уже!", "детекция не нужна", "l7proto = MTPROTO"]),
        "Zapret2/attachments", lk="bx", rk="bxa"))

    add("dpi-tls-gates", "VLESS/attachments", lambda: chain(
        "dpi-tls-gates", "Правило срабатывает, только если выполнены все три условия",
        "TLS-соединение попадает под заморозку на 120 секунд, если подсеть сервера в списке, фингерпринт подозрительный и к одному SNI больше трёх соединений за короткое время. Достаточно разорвать любое одно звено.",
        [("подсеть в списке?", "Selectel, Яндекс.Облако…"), ("фингерпринт подозрительный?", "Chrome, Safari, iOS"), (">3 соединений на SNI", "интервал меньше ~350–400 мс, за 60 с"), ("заморозка", "120 секунд")],
        "VLESS/attachments", edges={0: "И", 1: "И", 2: "→"}, warn=(3,), foot="Разорвите любое одно звено — правило на вас не сработает."))

    add("tls-in-tls", "VLESS/attachments", lambda: stack(
        "tls-in-tls", "«TLS в TLS»: два вложенных соединения",
        "Внешний TLS или REALITY-туннель идёт от вас к вашему VPS, а внутри него идёт внутренний TLS от браузера до google.com; эта вложенность и называется TLS в TLS.",
        [("внешний TLS / REALITY-туннель", "вы ↔ ваш VPS"), ("внутренний TLS", "браузер ↔ google.com: это и есть «TLS в TLS»")],
        "VLESS/attachments", accent=(1,)))

    def mux():
        f = Fig("mux", 250, 9, "Mux: одно внешнее TLS-соединение несёт несколько подпотоков",
                "Внутри одного внешнего TLS-соединения идут подпотоки к разным сайтам, у каждого внутри свой TLS. Снаружи цензор видит только одно соединение.")
        f.add(f.rect(2, 10, 940, 220, "bxa", rx=12) + f.text(18, 38, "ОДНО внешнее TLS-соединение", "tk"))
        for k, s in enumerate(["подпоток 1 → сайт A", "подпоток 2 → сайт B", "подпоток 3 → сайт C"]):
            y = 64 + k * 54
            f.g(f.rect(40, y, 560, 40, "bx", rx=8) + f.text(56, y + 25, s, "tk sm") + f.text(620, y + 25, "внутри свой TLS", "mu sm"), f.vis(0.6 + k * 0.9, dx=-10))
        return f
    add("mux", "VLESS/attachments", mux)
