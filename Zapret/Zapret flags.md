---
description: "Полный справочник флагов nfqws v72.2: --dpi-desync, fooling, hostlist, ipset, позиции split и готовые профили для HTTPS, HTTP, TCP и UDP."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/Zapret/Zapret-flags](https://wiki.zapret.moe/Zapret/Zapret-flags)


```bash
@<config_file>|$<config_file>                             ; читать конфигурацию из файла. опция должна быть первой. остальные опции игнорируются.

--debug=0|1                                               ; 1=выводить отладочные сообщения
--dry-run                                                 ; проверить опции командной строки и выйти. код 0 - успешная проверка.
--version                                                 ; вывести версию и выйти
--comment                                                 ; любой текст (игнорируется)
--daemon                                                  ; демонизировать прогу
--pidfile=<file>                                          ; сохранить PID в файл
--user=<username>                                         ; менять uid процесса
--uid=uid[:gid]                                           ; менять uid процесса
--qnum=N                                                  ; номер очереди N
--bind-fix4                                               ; пытаться решить проблему неверного выбора исходящего интерфейса для сгенерированных ipv4 пакетов
--bind-fix6                                               ; пытаться решить проблему неверного выбора исходящего интерфейса для сгенерированных ipv6 пакетов
--ctrack-timeouts=S:E:F[:U]                               ; таймауты внутреннего conntrack в состояниях SYN, ESTABLISHED, FIN, таймаут udp. по умолчанию 60:300:60:60
--ctrack-disable=[0|1]                                    ; 1 или остутствие аргумента отключает conntrack
--ipcache-lifetime=<int>                                  ; время жизни записей кэша IP в секундах. 0 - без ограничений.
--ipcache-hostname=[0|1]                                  ; 1 или отсутствие аргумента включают кэширование имен хостов для применения в стратегиях нулевой фазы
--wsize=<winsize>[:<scale_factor>]                        ; менять tcp window size на указанный размер в SYN,ACK. если не задан scale_factor, то он не меняется (устарело !)
--wssize=<winsize>[:<scale_factor>]                       ; менять tcp window size на указанный размер в исходящих пакетах. scale_factor по умолчанию 0. (см. conntrack !)
--wssize-cutoff=[n|d|s]N                                  ; изменять server window size в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру меньше N
--wssize-forced-cutoff=0|1                                ; 1(default)=автоматически отключать wssize в случае обнаружения известного протокола
--synack-split=[syn|synack|acksyn]                        ; выполнить tcp split handshake. вместо SYN,ACK отсылать только SYN, SYN+ACK или ACK+SYN
--orig-ttl=<int>                                          ; модифицировать TTL оригинального пакета
--orig-ttl6=<int>                                         ; модифицировать ipv6 hop limit оригинальных пакетов.  если не указано, используется значение --orig-ttl
--orig-autottl=[<delta>[:<min>[-<max>]]|-]                ; режим auto ttl для ipv4 и ipv6. по умолчанию: +5:3-64. "0:0-0" или "-" отключает функцию
--orig-autottl6=[<delta>[:<min>[-<max>]]|-]               ; переопределение предыдущего параметра для ipv6
--orig-tcp-flags-set=<int|0xHEX|flaglist>                 ; устанавливать указанные tcp флаги (flags |= value). число , либо список через запятую : FIN,SYN,RST,PSH,ACK,URG,ECE,CWR,AE,R1,R2,R3
--orig-tcp-flags-unset=<int|0xHEX|flaglist>               ; удалять указанные tcp флаги (flags &= ~value)
--orig-mod-start=[n|d|s]N                                 ; применять orig-mod только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру больше или равно N
--orig-mod-cutoff=[n|d|s]N                                ; применять orig-mod только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру меньше N
--dup=<int>                                               ; высылать N дубликатов до оригинала
--dup-replace=[0|1]                                       ; 1 или отсутствие аргумента блокирует отправку оригинала. отправляются только дубликаты.
--dup-ttl=<int>                                           ; модифицировать TTL дубликатов
--dup-ttl6=<int>                                          ; модифицировать ipv6 hop limit дубликатов. если не указано, используется значение --dup-ttl
--dup-autottl=[<delta>[:<min>[-<max>]]|-]                 ; режим auto ttl для ipv4 и ipv6. по умолчанию: +1:3-64. "0:0-0" или "-" отключает функцию
--dup-autottl6=[<delta>[:<min>[-<max>]]|-]                ; переопределение предыдущего параметра для ipv6
--dup-tcp-flags-set=<int|0xHEX|flaglist>                  ; устанавливать указанные tcp флаги (flags |= value). число , либо список через запятую : FIN,SYN,RST,PSH,ACK,URG,ECE,CWR,AE,R1,R2,R3
--dup-tcp-flags-unset=<int|0xHEX|flaglist>                ; удалять указанные tcp флаги (flags &= ~value)
--dup-fooling=<fooling>                                   ; дополнительные методики как сделать, чтобы дубликат не дошел до сервера. none md5sig badseq badsum datanoack ts hopbyhop hopbyhop2
--dup-ts-increment=<int|0xHEX>                            ; инкремент TSval для ts. по умолчанию -600000
--dup-badseq-increment=<int|0xHEX>                        ; инкремент sequence number для badseq. по умолчанию -10000
--dup-badack-increment=<int|0xHEX>                        ; инкремент ack sequence number для badseq. по умолчанию -66000
--dup-ip-id=same|zero|seq|rnd                             ; режим назначения ip_id для пакетов dup
--dup-start=[n|d|s]N                                      ; применять dup только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру больше или равно N
--dup-cutoff=[n|d|s]N                                     ; применять dup только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру меньше N
--hostcase                                                ; менять регистр заголовка "Host:" по умолчанию на "host:".
--hostnospace                                             ; убрать пробел после "Host:" и переместить его в конец значения "User-Agent:" для сохранения длины пакета
--methodeol                                               ; добавить перевод строки в unix стиле ('\n') перед методом и убрать пробел из Host: : "GET / ... Host: domain.com" => "\nGET  / ... Host:domain.com"
--hostspell=HoST                                          ; точное написание заголовка Host (можно "HOST" или "HoSt"). автоматом включает --hostcase
--domcase                                                 ; домен после Host: сделать таким : TeSt.cOm
--ip-id=seq|seqgroup|rnd|zero                             ; режим назначения ip_id для генерированных пакетов
--dpi-desync=[<mode0>,]<mode>[,<mode2]                    ; атака по десинхронизации DPI. mode : synack syndata fake fakeknown rst rstack hopbyhop destopt ipfrag1 multisplit multidisorder fakedsplit hostfakesplit fakeddisorder ipfrag2 udplen tamper
--dpi-desync-fwmark=<int|0xHEX>                           ; бит fwmark для пометки десинхронизирующих пакетов, чтобы они повторно не падали в очередь. default = 0x40000000
--dpi-desync-ttl=<int>                                    ; установить ttl для десинхронизирующих пакетов
--dpi-desync-ttl6=<int>                                   ; установить ipv6 hop limit для десинхронизирующих пакетов. если не указано, используется значение --dpi-desync-ttl
--dpi-desync-autottl=[<delta>[:<min>[-<max>]]|-]          ; режим auto ttl для ipv4 и ipv6. по умолчанию: 1:3-20. "0:0-0" или "-" отключает функцию
--dpi-desync-autottl6=[<delta>[:<min>[-<max>]]|-]         ; переопределение предыдущего параметра для ipv6
--dpi-desync-tcp-flags-set=<int|0xHEX|flaglist>           ; устанавливать указанные tcp флаги (flags |= value). число , либо список через запятую : FIN,SYN,RST,PSH,ACK,URG,ECE,CWR,AE,R1,R2,R3
--dpi-desync-tcp-flags-unset=<int|0xHEX|flaglist>         ; удалять указанные tcp флаги (flags &= ~value)
--dpi-desync-fooling=<fooling>                            ; дополнительные методики как сделать, чтобы фейковый пакет не дошел до сервера. none md5sig badseq badsum datanoack ts hopbyhop hopbyhop2
--dpi-desync-repeats=<N>                                  ; посылать каждый генерируемый в nfqws пакет N раз (не влияет на остальные пакеты)
--dpi-desync-skip-nosni=0|1                               ; 1(default)=не применять dpi desync для запросов без hostname в SNI, в частности для ESNI
--dpi-desync-split-pos=N|-N|marker+N|marker-N             ; список через запятую маркеров для tcp сегментации в режимах split и disorder
--dpi-desync-split-seqovl=N|-N|marker+N|marker-N          ; единичный маркер, определяющий величину перекрытия sequence в режимах split и disorder. для split поддерживается только положительное число.
--dpi-desync-split-seqovl-pattern=[+ofs]@<filename>|0xHEX ; чем заполнять фейковую часть overlap
--dpi-desync-fakedsplit-pattern=[+ofs]@<filename>|0xHEX   ; чем заполнять фейки в fakedsplit/fakeddisorder
--dpi-desync-fakedsplit-mod=mod[,mod]                     ; может быть none, altorder=0|1|2|3 + 0|8|16
--dpi-desync-hostfakesplit-midhost=marker+N|marker-N      ; маркер дополнительного разреза сегмента с оригинальным хостом. должен попадать в пределы хоста.
--dpi-desync-hostfakesplit-mod=mod[,mod]                  ; может быть none, host=<hostname>, altorder=0|1
--dpi-desync-ts-increment=<int|0xHEX>                     ; инкремент TSval для ts. по умолчанию -600000
--dpi-desync-badseq-increment=<int|0xHEX>                 ; инкремент sequence number для badseq. по умолчанию -10000
--dpi-desync-badack-increment=<int|0xHEX>                 ; инкремент ack sequence number для badseq. по умолчанию -66000
--dpi-desync-any-protocol=0|1                             ; 0(default)=работать только по http request и tls clienthello  1=по всем непустым пакетам данных
--dpi-desync-fake-tcp-mod=mod[,mod]                       ; список через запятую режимов runtime модификации tcp фейков (любых) : none, seq
--dpi-desync-fake-http=[+ofs]@<filename>|0xHEX	          ; файл, содержащий фейковый http запрос для dpi-desync=fake, на замену стандартному www.iana.org
--dpi-desync-fake-tls=[+ofs]@<filename>|0xHEX|![+offset]  ; файл, содержащий фейковый tls clienthello для dpi-desync=fake, на замену стандартному. '!' = стандартный фейк
--dpi-desync-fake-tls-mod=mod[,mod]                       ; список через запятую режимов runtime модификации фейков : none,rnd,rndsni,sni=<sni>,dupsid,padencap
--dpi-desync-fake-unknown=[+ofs]@<filename>|0xHEX         ; файл, содержащий фейковый пейлоад неизвестного протокола для dpi-desync=fake, на замену стандартным нулям 256 байт
--dpi-desync-fake-syndata=[+ofs]@<filename>|0xHEX         ; файл, содержащий фейковый пейлоад пакета SYN для режима десинхронизации syndata
--dpi-desync-fake-quic=[+ofs]@<filename>|0xHEX            ; файл, содержащий фейковый QUIC Initial
--dpi-desync-fake-wireguard=[+ofs]@<filename>|0xHEX       ; файл, содержащий фейковый wireguard handshake initiation
--dpi-desync-fake-dht=[+ofs]@<filename>|0xHEX             ; файл, содержащий фейковый пейлоад DHT протокола для dpi-desync=fake, на замену стандартным нулям 64 байт
--dpi-desync-fake-discord=[+ofs]@<filename>|0xHEX         ; файл, содержащий фейковый пейлоад Discord протокола нахождения IP адреса для голосовых чатов для dpi-desync=fake, на замену стандартным нулям 64 байт
--dpi-desync-fake-stun=[+ofs]@<filename>|0xHEX            ; файл, содержащий фейковый пейлоад STUN протокола для dpi-desync=fake, на замену стандартным нулям 64 байт
--dpi-desync-fake-unknown-udp=[+ofs]@<filename>|0xHEX     ; файл, содержащий фейковый пейлоад неизвестного udp протокола для dpi-desync=fake, на замену стандартным нулям 64 байт
--dpi-desync-udplen-increment=<int>                       ; на сколько увеличивать длину udp пейлоада в режиме udplen
--dpi-desync-udplen-pattern=[+ofs]@<filename>|0xHEX       ; чем добивать udp пакет в режиме udplen. по умолчанию - нули
--dpi-desync-start=[n|d|s]N                               ; применять dpi desync только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру больше или равно N
--dpi-desync-cutoff=[n|d|s]N                              ; применять dpi desync только в исходящих пакетах (n), пакетах данных (d), относительных sequence (s) по номеру меньше N
--hostlist=<filename>                                     ; действовать только над доменами, входящими в список из filename. поддомены автоматически учитываются, если хост не начинается с '^'.
                                                          ; в файле должен быть хост на каждой строке.
                                                          ; список читается при старте и хранится в памяти в виде иерархической структуры для быстрого поиска.
                                                          ; при изменении времени модификации файла он перечитывается автоматически по необходимости
                                                          ; список может быть запакован в gzip. формат автоматически распознается и разжимается
                                                          ; списков может быть множество. пустой общий лист = его отсутствие
                                                          ; хосты извлекаются из Host: хедера обычных http запросов и из SNI в TLS ClientHello.
--hostlist-domains=<domain_list>                          ; фиксированный список доменов через зяпятую. можно использовать # в начале для комментирования отдельных доменов.
--hostlist-exclude=<filename>                             ; не применять дурение к доменам из листа. может быть множество листов. схема аналогична include листам.
--hostlist-exclude-domains=<domain_list>                  ; фиксированный список доменов через зяпятую. можно использовать # в начале для комментирования отдельных доменов.
--hostlist-auto=<filename>                                ; обнаруживать автоматически блокировки и заполнять автоматический hostlist (требует перенаправления входящего трафика)
--hostlist-auto-fail-threshold=<int>                      ; сколько раз нужно обнаружить ситуацию, похожую на блокировку, чтобы добавить хост в лист (по умолчанию: 3)
--hostlist-auto-fail-time=<int>                           ; все эти ситуации должны быть в пределах указанного количества секунд (по умолчанию: 60)
--hostlist-auto-retrans-threshold=<int>                   ; сколько ретрансмиссий запроса считать блокировкой (по умолчанию: 3)
--hostlist-auto-debug=<logfile>                           ; лог положительных решений по autohostlist. позволяет разобраться почему там появляются хосты.
--new                                                     ; начало новой стратегии (новый профиль)
--skip                                                    ; не использовать этот профиль . полезно для временной деактивации профиля без удаления параметров.
--filter-l3=ipv4|ipv6                                     ; фильтр версии ip для текущей стратегии
--filter-tcp=[~]port1[-port2]|*                           ; фильтр портов tcp для текущей стратегии. ~ означает инверсию. установка фильтра tcp и неустановка фильтра udp запрещает udp. поддерживается список через запятую.
--filter-udp=[~]port1[-port2]|*                           ; фильтр портов udp для текущей стратегии. ~ означает инверсию. установка фильтра udp и неустановка фильтра tcp запрещает tcp. поддерживается список через запятую.
--filter-l7=<proto>                                       ; фильтр протокола L6-L7. поддерживается несколько значений через запятую. proto : http tls quic wireguard dht discord stun unknown
--filter-ssid=ssid1[,ssid2,ssid3,...]                     ; фильтр по имени wifi сети (только для linux)
--ipset=<filename>                                        ; включающий ip list. на каждой строчке ip или cidr ipv4 или ipv6. поддерживается множество листов и gzip. перечитка автоматическая.
--ipset-ip=<ip_list>                                      ; фиксированный список подсетей через запятую. можно использовать # в начале для комментирования отдельных подсетей.
--ipset-exclude=<filename>                                ; исключающий ip list. на каждой строчке ip или cidr ipv4 или ipv6. поддерживается множество листов и gzip. перечитка автоматическая.
--ipset-exclude-ip=<ip_list>                              ; фиксированный список подсетей через запятую. можно использовать # в начале для комментирования отдельных подсетей.
```

# 📚 Справочник параметров nfqws v72.2

## 🔧 Базовые параметры

### Конфигурация и управление
```bash
@<file> | $<file>         # Загрузить конфиг из файла (должно быть первым)
--debug=0|1               # Отладочные сообщения
--dry-run                 # Проверить параметры и выйти
--version                 # Показать версию
--comment                 # Комментарий (игнорируется)
--daemon                  # Запустить как демон
--pidfile=<file>          # Файл PID
--user=<username>         # Сменить пользователя
--uid=uid[:gid]           # Сменить UID:GID
--qnum=N                  # Номер NFQUEUE
```

### Системные настройки
```bash
--bind-fix4               # Фикс выбора интерфейса IPv4
--bind-fix6               # Фикс выбора интерфейса IPv6
--ctrack-timeouts=S:E:F[:U]  # Таймауты conntrack (по умолч: 60:300:60:60)
--ctrack-disable=[0|1]    # Отключить conntrack
--ipcache-lifetime=<int>  # Время жизни IP-кэша (сек), 0=∞
--ipcache-hostname=[0|1]  # Кэшировать имена хостов
```

---

## 🎯 Модификация оригинальных пакетов (orig)

```bash
--orig-ttl=<int>                              # TTL для IPv4
--orig-ttl6=<int>                             # Hop limit для IPv6
--orig-autottl=[<delta>[:<min>[-<max>]]|-]    # AutoTTL IPv4/6 (дефолт: +5:3-64)
--orig-autottl6=[...]                         # AutoTTL только для IPv6
--orig-tcp-flags-set=<flags> 🆕               # Установить TCP флаги
--orig-tcp-flags-unset=<flags> 🆕             # Снять TCP флаги
--orig-mod-start=[n|d|s]N                     # Начать модификацию с пакета N
--orig-mod-cutoff=[n|d|s]N                    # Прекратить модификацию после пакета N
```

---

## 👥 Дубликаты пакетов (dup)

```bash
--dup=<int>                                   # Количество дубликатов
--dup-replace=[0|1]                           # Отправлять только дубликаты (блокировать оригинал)
--dup-ttl=<int>                               # TTL для дубликатов
--dup-ttl6=<int>                              # Hop limit для дубликатов IPv6
--dup-autottl=[<delta>[:<min>[-<max>]]|-]     # AutoTTL (дефолт: +1:3-64)
--dup-autottl6=[...]                          # AutoTTL для IPv6
--dup-tcp-flags-set=<flags> 🆕                # Установить TCP флаги
--dup-tcp-flags-unset=<flags> 🆕              # Снять TCP флаги
--dup-fooling=<method>                        # Метод "обмана": md5sig, badseq, badsum, datanoack, ts, hopbyhop, hopbyhop2
--dup-ts-increment=<int>                      # Инкремент TSval (дефолт: -600000)
--dup-badseq-increment=<int>                  # Инкремент SEQ (дефолт: -10000)
--dup-badack-increment=<int>                  # Инкремент ACK (дефолт: -66000)
--dup-ip-id=same|zero|seq|rnd 🆕              # Режим назначения IP_ID
--dup-start=[n|d|s]N                          # Начать с пакета N
--dup-cutoff=[n|d|s]N                         # Прекратить после пакета N
```

---

## 🛡️ DPI Desync (основные параметры)

### Режимы десинхронизации
```bash
--dpi-desync=[mode0,]mode[,mode2]
```
**Режимы TCP:** `synack`, `syndata`, `fake`, `fakeknown`, `rst`, `rstack`, `multisplit`, `multidisorder`, `fakedsplit`, `hostfakesplit`, `fakeddisorder`, `ipfrag1`, `ipfrag2`, `hopbyhop`, `destopt`

**Режимы UDP:** `udplen`, `tamper`

### TTL и автоматика
```bash
--dpi-desync-ttl=<int>                        # TTL для десинхронизирующих пакетов
--dpi-desync-ttl6=<int>                       # Hop limit IPv6
--dpi-desync-autottl=[<delta>[:<min>[-<max>]]|-]  # AutoTTL (дефолт: 1:3-20)
--dpi-desync-autottl6=[...]                   # AutoTTL для IPv6
--dpi-desync-tcp-flags-set=<flags> 🆕         # Установить TCP флаги
--dpi-desync-tcp-flags-unset=<flags> 🆕       # Снять TCP флаги
```

### Методы "обмана" фейков
```bash
--dpi-desync-fooling=<method>                 # none, md5sig, badseq, badsum, datanoack, ts, hopbyhop, hopbyhop2
--dpi-desync-repeats=<N>                      # Повторять каждый фейк N раз
--dpi-desync-skip-nosni=0|1                   # Пропускать ESNI (дефолт: 1)
```

### TCP сегментация
```bash
--dpi-desync-split-pos=N|-N|marker+N|marker-N         # Позиции разреза
--dpi-desync-split-seqovl=N|-N|marker+N|marker-N      # Величина sequence overlap
--dpi-desync-split-seqovl-pattern=[+ofs]@file|0xHEX   # Чем заполнять overlap
```

**Маркеры:** `method`, `host`, `endhost`, `sld`, `endsld`, `midsld`, `sniext`

### Модификации для split режимов
```bash
--dpi-desync-fakedsplit-pattern=[+ofs]@file|0xHEX     # Паттерн фейков
--dpi-desync-fakedsplit-mod=mod[,mod]                 # altorder=0-3 + 0|8|16
--dpi-desync-hostfakesplit-midhost=marker±N           # Доп. разрез в хосте
--dpi-desync-hostfakesplit-mod=mod[,mod]              # host=<hostname>, altorder=0|1
```

### Инкременты для fooling
```bash
--dpi-desync-ts-increment=<int>               # TSval (дефолт: -600000)
--dpi-desync-badseq-increment=<int>           # SEQ (дефолт: -10000)
--dpi-desync-badack-increment=<int>           # ACK (дефолт: -66000)
```

### Протоколы и фейки
```bash
--dpi-desync-any-protocol=0|1                 # 1=работать со всеми протоколами
--dpi-desync-fake-tcp-mod=mod[,mod]           # seq
```

#### Фейковые пейлоады
```bash
--dpi-desync-fake-http=[+ofs]@file|0xHEX
--dpi-desync-fake-tls=[+ofs]@file|0xHEX|![+ofs]
--dpi-desync-fake-tls-mod=mod[,mod]           # none, rnd, rndsni, sni=<sni>, dupsid, padencap
--dpi-desync-fake-unknown=[+ofs]@file|0xHEX
--dpi-desync-fake-syndata=[+ofs]@file|0xHEX
--dpi-desync-fake-quic=[+ofs]@file|0xHEX
--dpi-desync-fake-wireguard=[+ofs]@file|0xHEX
--dpi-desync-fake-dht=[+ofs]@file|0xHEX
--dpi-desync-fake-discord=[+ofs]@file|0xHEX
--dpi-desync-fake-stun=[+ofs]@file|0xHEX
--dpi-desync-fake-unknown-udp=[+ofs]@file|0xHEX
```

### UDP специфичное
```bash
--dpi-desync-udplen-increment=<int>           # Увеличение длины UDP
--dpi-desync-udplen-pattern=[+ofs]@file|0xHEX # Чем добивать пакет
```

### Ограничители применения
```bash
--dpi-desync-start=[n|d|s]N                   # Начать с пакета N
--dpi-desync-cutoff=[n|d|s]N                  # Прекратить после пакета N
--dpi-desync-fwmark=<int|0xHEX>               # Метка fwmark (дефолт: 0x40000000)
```

---

## 🌐 Модификации HTTP/TLS заголовков

```bash
--hostcase                    # "Host:" → "host:"
--hostnospace                 # Убрать пробел после "Host:"
--methodeol                   # Добавить \n перед методом
--hostspell=HoST              # Точное написание "Host"
--domcase                     # Домен: example.com → ExAmPlE.cOm
```

---

## 📊 Window Size

```bash
--wsize=<size>[:<scale>]              # В SYN,ACK (устарело!)
--wssize=<size>[:<scale>]             # В исходящих пакетах
--wssize-cutoff=[n|d|s]N              # Прекратить изменение после пакета N
--wssize-forced-cutoff=0|1 🆕         # 1=авто-отключение при HTTP/TLS (дефолт)
```

Почему `--wssize` стоит применять только как крайнюю меру (нет фильтрации по хостлистам и l7, замедление всех соединений на отфильтрованных портах) — в [[Zapret/wssize|отдельной заметке]].

---

## 🎭 Режим назначения IP_ID

```bash
--ip-id=seq|seqgroup|rnd|zero         # Для всех генерируемых пакетов
--dup-ip-id=same|zero|seq|rnd 🆕      # Для дубликатов (дефолт: same)
```

---

## 📋 Фильтрация и листы

### Хост-листы
```bash
--hostlist=<file>                     # Включающий список доменов
--hostlist-domains=<domain,domain>    # Фикс. список доменов
--hostlist-exclude=<file>             # Исключающий список
--hostlist-exclude-domains=<list>     # Фикс. список исключений
```

### Автоматический hostlist
```bash
--hostlist-auto=<file>                        # Автообнаружение блокировок
--hostlist-auto-fail-threshold=<int>          # Порог срабатывания (дефолт: 3)
--hostlist-auto-fail-time=<int>               # Временное окно (дефолт: 60 сек)
--hostlist-auto-retrans-threshold=<int>       # Порог ретрансмиссий (дефолт: 3)
--hostlist-auto-debug=<logfile>               # Лог решений
```

### IP-листы
```bash
--ipset=<file>                        # Включающий IP/CIDR список
--ipset-ip=<ip,ip,cidr>               # Фикс. список подсетей
--ipset-exclude=<file>                # Исключающий список
--ipset-exclude-ip=<list>             # Фикс. список исключений
```

---

## 🔀 Профили и фильтры

### Управление профилями
```bash
--new                                 # Начать новый профиль
--skip                                # Пропустить профиль
```

### Фильтры
```bash
--filter-l3=ipv4|ipv6                 # По версии IP
--filter-tcp=[~]port[-port]|*         # По TCP портам
--filter-udp=[~]port[-port]|*         # По UDP портам
--filter-l7=<proto>                   # По протоколу L7: http, tls, quic, wireguard, dht, discord, stun, unknown
--filter-ssid=ssid1,ssid2             # По WiFi SSID (только Linux)
```

---

## 🆕 Новое в [[Zapret v72.2]]

1. **`--wssize-forced-cutoff=0|1`** - контроль авто-отключения wssize
2. **Манипуляция TCP флагами:**
   - `--orig-tcp-flags-set/unset`
   - `--dup-tcp-flags-set/unset`
   - `--dpi-desync-tcp-flags-set/unset`
   - Формат: число, 0xHEX или список: `FIN,SYN,RST,PSH,ACK,URG,ECE,CWR,AE,R1,R2,R3`
3. **`--dup-ip-id=same|zero|seq|rnd`** - режим IP_ID для дубликатов

---

## 💡 Подсказки

### Форматы параметров:
- `[n|d|s]N` - n=номер пакета, d=пакет данных, s=sequence number
- `marker±N` - относительная позиция от маркера
- `[+ofs]@file|0xHEX` - данные из файла со смещением или hex-строка
- `#` в начале домена/IP - комментарий (игнорируется)

### TCP флаги (12 бит):
- Стандартные: FIN, SYN, RST, PSH, ACK, URG, ECE, CWR
- Reserved: **AE** (Accurate ECN), **R1, R2, R3**

# 🔀 Разделение параметров nfqws по типам трафика

## 🔐 HTTPS (TLS over TCP, порт 443)

### Основные режимы десинхронизации
```bash
--dpi-desync=fake,split              # Фейковый TLS ClientHello + сегментация
--dpi-desync=fakedsplit              # Замешивание фейков и оригинала
--dpi-desync=multisplit              # Нарезка на несколько сегментов
--dpi-desync=multidisorder           # Нарезка + обратный порядок
--dpi-desync=hostfakesplit           # Фейк только на имени хоста (SNI)
```

### Позиции разреза (специфичные для TLS)
```bash
--dpi-desync-split-pos=sni           # Разрез в начале SNI extension
--dpi-desync-split-pos=sniext        # Разрез в начале данных SNI
--dpi-desync-split-pos=host          # Разрез в начале hostname в SNI
--dpi-desync-split-pos=midsld        # Разрез в середине домена 2-го уровня
--dpi-desync-split-pos=sld           # Разрез в начале SLD
```

### Фейковые пейлоады для TLS
```bash
--dpi-desync-fake-tls=@tls_clienthello.bin       # Кастомный TLS ClientHello
--dpi-desync-fake-tls=!                          # Стандартный фейк
--dpi-desync-fake-tls=0xHEX                      # Hex-данные

# Модификации TLS фейков
--dpi-desync-fake-tls-mod=rnd                    # Рандомизировать random и session_id
--dpi-desync-fake-tls-mod=rndsni                 # Случайный SNI
--dpi-desync-fake-tls-mod=dupsid                 # Копировать session_id из оригинала
--dpi-desync-fake-tls-mod=sni=google.com         # Заменить SNI
--dpi-desync-fake-tls-mod=padencap               # Инкапсулировать в padding extension
--dpi-desync-fake-tls-mod=rnd,dupsid,rndsni      # Комбинация (по умолч.)
```

### Фильтры для HTTPS
```bash
--filter-tcp=443                                  # Только порт 443
--filter-l7=tls                                   # Только TLS протокол
--dpi-desync-skip-nosni=1                         # Пропускать ESNI (по умолч.)
```

### Типичные конфигурации для HTTPS
```bash
# Вариант 1: Простой split на SNI
--filter-tcp=443 --dpi-desync=split --dpi-desync-split-pos=sniext

# Вариант 2: Фейк + split с TTL
--filter-tcp=443 --dpi-desync=fake,split \
--dpi-desync-fooling=badsum --dpi-desync-split-pos=midsld

# Вариант 3: AutoTTL фейк
--filter-tcp=443 --dpi-desync=fake,multisplit \
--dpi-desync-autottl=2 --dpi-desync-split-pos=sniext,midsld

# Вариант 4: Disorder с кастомным SNI
--filter-tcp=443 --dpi-desync=fake,multidisorder \
--dpi-desync-fake-tls-mod=sni=ya.ru --dpi-desync-split-pos=midsld
```

---

## 🌐 HTTP (plain HTTP over TCP, порт 80)

### Основные режимы
```bash
--dpi-desync=split                    # Простая сегментация
--dpi-desync=multisplit               # Множественная нарезка
--dpi-desync=fake,split               # Фейк + сегментация
--dpi-desync=hostfakesplit            # Фейк на Host: заголовке
```

### Позиции разреза (специфичные для HTTP)
```bash
--dpi-desync-split-pos=method         # В начале метода (GET, POST)
--dpi-desync-split-pos=method+2       # После "GET" -> "GE|T /"
--dpi-desync-split-pos=host           # В начале значения Host:
--dpi-desync-split-pos=midsld         # В середине домена
--dpi-desync-split-pos=3              # После 3-го байта: "GET| /"
```

### Модификация HTTP заголовков
```bash
--hostcase                            # "Host:" → "host:"
--hostspell=HoSt                      # Точное написание
--hostnospace                         # Убрать пробел после Host:
--domcase                             # example.com → ExAmPlE.cOm
--methodeol                           # \n перед методом
```

### Фейковые пейлоады для HTTP
```bash
--dpi-desync-fake-http=@fake_request.txt         # Кастомный HTTP запрос
--dpi-desync-fake-http=0x474554202F20485454...   # Hex-данные
# По умолчанию: GET / HTTP/1.1\r\nHost: www.iana.org\r\n\r\n
```

### Фильтры для HTTP
```bash
--filter-tcp=80                       # Только порт 80
--filter-l7=http                      # Только HTTP протокол
```

### Типичные конфигурации для HTTP
```bash
# Вариант 1: Split после метода
--filter-tcp=80 --dpi-desync=split --dpi-desync-split-pos=method+2

# Вариант 2: Смена регистра + split
--filter-tcp=80 --hostcase --dpi-desync=split --dpi-desync-split-pos=host

# Вариант 3: Фейк с TTL
--filter-tcp=80 --dpi-desync=fake,split \
--dpi-desync-ttl=4 --dpi-desync-split-pos=midsld

# Вариант 4: Модификация заголовков
--filter-tcp=80 --hostcase --domcase --methodeol
```

---

## 🔌 TCP (прочий TCP трафик)

### Когда применяется
```bash
--dpi-desync-any-protocol=1           # Работать со ВСЕМИ TCP пакетами
```

⚠️ **Внимание:** Без этого флага desync работает только с HTTP/TLS!

### Подходящие режимы для любого TCP
```bash
--dpi-desync=syndata                  # Данные в SYN пакете
--dpi-desync=synack                   # Модификация handshake
--dpi-desync=multisplit               # Универсальная сегментация
--dpi-desync=fake,split               # Фейк + split
```

### Позиции разреза (универсальные)
```bash
--dpi-desync-split-pos=1              # После 1-го байта
--dpi-desync-split-pos=2              # После 2-го байта
--dpi-desync-split-pos=-1             # Последний байт
--dpi-desync-split-pos=10,20,30       # Множественные позиции
```

### Фейковые пейлоады для неизвестных протоколов
```bash
--dpi-desync-fake-unknown=@payload.bin           # Кастомный пейлоад
--dpi-desync-fake-unknown=0x0000...              # Hex (256 байт по умолч.)
```

### Sequence overlap (для любого TCP)
```bash
--dpi-desync-split-seqovl=10                     # Перекрытие на 10 байт
--dpi-desync-split-seqovl-pattern=0x41414141     # Чем заполнять overlap
```

### Фильтры для прочего TCP
```bash
--filter-tcp=*                        # Все TCP порты
--filter-tcp=~80,443                  # Все КРОМЕ 80 и 443
--filter-tcp=22,3389                  # Конкретные порты (SSH, RDP)
--filter-l7=unknown                   # Неизвестные протоколы
```

### Типичные конфигурации для TCP
```bash
# Вариант 1: SSH, VPN через TCP
--filter-tcp=22 --dpi-desync=split --dpi-desync-split-pos=2 \
--dpi-desync-any-protocol=1

# Вариант 2: Все TCP кроме HTTP/HTTPS
--filter-tcp=~80,443 --dpi-desync=fake,split \
--dpi-desync-any-protocol=1 --dpi-desync-split-pos=1

# Вариант 3: SYN data для быстрых соединений
--filter-tcp=* --dpi-desync=syndata \
--dpi-desync-fake-syndata=@payload.bin
```

---

## 📡 UDP

### Режимы десинхронизации для UDP
```bash
--dpi-desync=udplen                   # Увеличить длину UDP пакета
--dpi-desync=tamper                   # Испортить пакет
--dpi-desync=fake                     # Фейковый UDP пакет
--dpi-desync=ipfrag2                  # IP фрагментация
```

### UDP длина (udplen)
```bash
--dpi-desync-udplen-increment=2       # Увеличить длину на 2 байта
--dpi-desync-udplen-pattern=0x0000    # Чем добивать (по умолч. нули)
```

### Фейковые пейлоады для UDP протоколов
```bash
# QUIC (HTTP/3)
--dpi-desync-fake-quic=@quic_initial.bin
--filter-l7=quic
--filter-udp=443

# WireGuard VPN
--dpi-desync-fake-wireguard=@wg_handshake.bin
--filter-l7=wireguard
--filter-udp=51820

# DHT (torrents)
--dpi-desync-fake-dht=@dht_payload.bin
--filter-l7=dht

# Discord голосовой чат
--dpi-desync-fake-discord=@discord_payload.bin
--filter-l7=discord

# STUN (WebRTC, VoIP)
--dpi-desync-fake-stun=@stun_payload.bin
--filter-l7=stun

# Неизвестный UDP
--dpi-desync-fake-unknown-udp=@payload.bin
--filter-l7=unknown
```

### Фильтры для UDP
```bash
--filter-udp=443                      # QUIC (HTTP/3)
--filter-udp=53                       # DNS
--filter-udp=51820                    # WireGuard
--filter-udp=*                        # Все UDP
--filter-l7=quic,wireguard,stun       # Несколько протоколов
```

### Типичные конфигурации для UDP
```bash
# Вариант 1: QUIC (YouTube, Google)
--filter-udp=443 --filter-l7=quic \
--dpi-desync=fake --dpi-desync-repeats=6 \
--dpi-desync-fake-quic=@quic_initial.bin

# Вариант 2: WireGuard VPN
--filter-udp=51820 --filter-l7=wireguard \
--dpi-desync=fake,udplen \
--dpi-desync-udplen-increment=2

# Вариант 3: Все UDP с увеличением длины
--filter-udp=* --dpi-desync=udplen \
--dpi-desync-udplen-increment=1

# Вариант 4: DNS через UDP
--filter-udp=53 --dpi-desync=fake \
--dpi-desync-ttl=1
```

---

## 📊 Сравнительная таблица

| Параметр | HTTPS | HTTP | TCP | UDP |
|----------|-------|------|-----|-----|
| **Основной порт** | 443 | 80 | * | * |
| **Фильтр L7** | `tls` | `http` | `unknown` | `quic`, `wireguard`, etc. |
| **Лучший режим** | `fake,split` | `split` | `syndata` | `fake,udplen` |
| **Маркеры split** | `sniext`, `midsld` | `method+2`, `host` | Числа | - |
| **Фейки** | `--fake-tls` | `--fake-http` | `--fake-unknown` | `--fake-quic`, etc. |
| **Модификации** | `--fake-tls-mod` | `--hostcase` | - | `--udplen-increment` |
| **any-protocol** | Не нужен | Не нужен | **Обязателен!** | - |

---

## 🎯 Готовые профили (многопрофильная конфигурация)

### Полная конфигурация для всех типов трафика
```bash
# Профиль 1: HTTPS
--filter-tcp=443 --filter-l7=tls \
--dpi-desync=fake,multisplit \
--dpi-desync-split-pos=sniext,midsld \
--dpi-desync-fooling=badsum \
--dpi-desync-fake-tls-mod=rnd,dupsid

# Профиль 2: HTTP
--new \
--filter-tcp=80 --filter-l7=http \
--hostcase --domcase \
--dpi-desync=split \
--dpi-desync-split-pos=method+2

# Профиль 3: QUIC (YouTube)
--new \
--filter-udp=443 --filter-l7=quic \
--dpi-desync=fake \
--dpi-desync-repeats=6

# Профиль 4: Прочий TCP
--new \
--filter-tcp=~80,443 \
--dpi-desync=split \
--dpi-desync-split-pos=2 \
--dpi-desync-any-protocol=1

# Профиль 5: WireGuard
--new \
--filter-udp=51820 --filter-l7=wireguard \
--dpi-desync=fake,udplen \
--dpi-desync-udplen-increment=2
```

---

## 💡 Ключевые отличия

### HTTPS vs HTTP
- **HTTPS**: Работает с бинарным TLS, нужны `sni*` маркеры, `--fake-tls-mod`
- **HTTP**: Работает с текстом, можно менять регистр (`--hostcase`), маркеры `method`, `host`

### TCP vs UDP  
- **TCP**: Sequence numbers, сегментация, syn/ack манипуляции
- **UDP**: Без состояния, `udplen`, специфичные фейки для протоколов

### Известные vs неизвестные протоколы
- **HTTP/TLS**: Автоопределение, маркеры работают
- **Прочие**: Нужен `--dpi-desync-any-protocol=1`, только числовые позиции split