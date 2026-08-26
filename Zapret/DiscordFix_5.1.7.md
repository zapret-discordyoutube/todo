---
tags:
aliases:
img:
description: "Bat-файл DiscordFix 5.1.7 для Zapret под Билайн, Ростелеком и Инфолинк: параметры winws.exe и варианты стратегий syndata, split2, disorder2."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/Zapret/DiscordFix_5.1.7](https://wiki.zapret.moe/Zapret/DiscordFix_5.1.7)

DiscordFix (для Билайн, Ростелеком, Инфолинк).bat
```bash
@echo off
chcp 65001 >nul
:: 65001 - UTF-8

cd /d "%~dp0..\"
set BIN=%~dp0..\bin\

set LIST_TITLE=ZAPRET: Discord Fix Beeline-Rostelekom-Infolink
set LIST_PATH=%~dp0..\lists\list-discord.txt
set DISCORD_IPSET_PATH=%~dp0..\lists\ipset-discord.txt

start "%LIST_TITLE%" /min "%BIN%winws.exe" --wf-udp=50000-50100 ^
--filter-udp=50000-50100 --ipset="%DISCORD_IPSET_PATH%" --dpi-desync=fake --dpi-desync-any-protocol --dpi-desync-cutoff=d3 --dpi-desync-repeats=6 ^
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,split2
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,split2 --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,disorder2
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,disorder2 --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata --wssize 1:6
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin --wssize 1:6
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,split2 --wssize 1:6
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,split2 --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin --wssize 1:6
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,disorder2 --wssize 1:6
--wf-l3=ipv4 --wf-tcp=443 --dpi-desync=syndata,disorder2 --dpi-desync-fake-syndata=/cygdrive/c/zapret-win-bundle-master/blockcheck/zapret/files/fake/tls_clienthello_iana_org.bin --wssize 1:6
```

