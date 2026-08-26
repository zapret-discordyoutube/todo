---
date: 2026-08-20
tags:
  - xray
  - vless
  - reality
  - proxy
  - обзор-раздела
aliases:
  - Xray раздел
  - Xray-core обзор
  - VLESS REALITY XTLS что это
  - Иксрей прокси
description: "Раздел о Project X и ядре Xray-core: протоколы VLESS, XTLS/Vision, REALITY и XHTTP — от истории проекта до подключения клиентов и маршрутизации."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/xray/xray](https://wiki.zapret.moe/xray/xray)

# 🛰️ Xray, VLESS и REALITY — раздел

> [!info] О чём раздел
> Раздел о **Project X**: ядре **Xray-core** и его протоколах — VLESS, XTLS/Vision, REALITY, XHTTP, — на которых сегодня работает большинство прокси-серверов для обхода блокировок. От истории проекта до побайтового устройства каждого слоя.

## Как читать раздел

**Знакомство — что это и откуда:**

- [[xray/project-x|Project X (Xray-core): что за проект и откуда взялся]] — обзорная точка входа.
- [[xray/authors-v2ray-xray|Кто стоит за V2Ray и Xray]] — Victoria Raymond, Darien Raymond и RPRX: разбор частого вопроса про авторов.
- [[xray/v2fly-vs-xray|v2fly/v2ray-core против XTLS/Xray-core]] — чем отличаются два ядра, сравнение по исходному коду.

**Протоколы и слои:**

- [[xray/vless|Протокол VLESS]] — устройство и возможности транспортного протокола.
- [[xray/vless-stack-map|Слои VLESS-стека]] — кто за что отвечает: `type`, `security`, `flow`, `encryption` и сам протокол — пять разных слоёв одной ссылки.
- [[xray/xtls-vision|XTLS и Vision]] — что это и чем отличается от VLESS и REALITY.
- [[xray/reality|REALITY]] — как прокси прикрывается настоящим чужим сайтом вместо своего TLS-сертификата.
- [[xray/vless-encryption|VLESS Encryption]] — собственное постквантовое шифрование протокола (с сентября 2025).
- [[xray/xhttp|XHTTP]] — транспорт, притворяющийся обычным веб-трафиком (бывший SplitHTTP).

**Практика:**

- [[xray/clients-and-routing|Клиенты и маршрутизация: как подключиться к VLESS-серверу]] — для пользователя без опыта, с телефона и компьютера.
- [[xray/routing|Маршрутизация в Xray]] — как трафик распределяется по outbound на сервере и в клиенте.

## 📚 См. также

- [[VLESS/dpi-tls-june-2026|Как DPI «замораживает» VLESS+REALITY]] — взгляд со стороны цензора
- [[sing-box/sing-box|Раздел sing-box]] — соседняя платформа, реализующая те же протоколы

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/xray/xray.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
