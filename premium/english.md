---
date: 2026-10-16
tags:
  - zapret-vpn
  - инструкция
  - english
aliases:
  - Zapret VPN in English
  - English guide Zapret VPN
  - How to connect Zapret VPN
description: "Zapret VPN guide in English: the bot @zapretvpns_bot is in Russian, so this page names every button you need, translates it and walks you from payment to a working VPN."
---

> [!mirror] Backup mirror
> The main version of this page is on the wiki: [wiki.zapret.moe/premium/english](https://wiki.zapret.moe/premium/english)

# 🇬🇧 Zapret VPN in English

> [!info] In short
> Zapret VPN is a personal VPN that works in Russia. You buy it in the Telegram bot [@zapretvpns_bot](https://t.me/zapretvpns_bot), get **one link**, paste it into a VPN app once — and the app gets all your servers from it. The bot is in Russian, so below every button is quoted exactly as it appears in the bot, with a translation in brackets.

## The whole path in four steps

| Step | Where | What to tap | What you get |
|---|---|---|---|
| 1. Top up the balance | bot | «💳 Подписка и баланс» (Plan and balance) → «💰 Пополнить» (Top up) → amount → pay | money on your bot balance |
| 2. Buy a plan | bot | «🛒 Купить / продлить» (Buy / renew) → plan → period → confirm | an active plan |
| 3. Get your link | bot | «🚀 Подключить устройство» (Connect a device) → «🌐 Весь интернет (VPN)» (Whole internet) → your device → the subscription button | a link `https://…` |
| 4. Turn on the VPN | app | add the link as a subscription, pick a server, connect | a working VPN |

If you don't know which plan to take — take **💎 Vless MAX** (199 ₽ a month): it has 15 servers instead of 2 and all Telegram proxies.

## Step 1. Top up the balance

1. Open [@zapretvpns_bot](https://t.me/zapretvpns_bot) and tap «Запустить» (Start).
2. Tap **«💳 Подписка и баланс»** (Plan and balance), then **«💰 Пополнить»** (Top up).
3. Choose an amount or type it in digits, for example `199`.
4. Tap the payment button, open the link it gives and pay with SBP (Russia's fast payment system) in your bank app.
5. Come back to the bot: the money arrives by itself within seconds. If nothing changed after a minute, tap «🔄 Проверить оплату» (Check payment).

## Step 2. Buy a plan

1. On the same screen tap **«🛒 Купить / продлить»** (Buy / renew).
2. Choose a plan — **💎 Vless MAX** if unsure — then the period.
3. Confirm. The bot answers «✅ Подписка успешно оформлена!» (Plan activated) and shows the next step.

## Step 3. Get your link

1. In the main menu tap the green button **«🚀 Подключить устройство»** (Connect a device).
2. Tap **«🌐 Весь интернет (VPN)»** (Whole internet). («✈️ Только Telegram» means Telegram only — a proxy inside Telegram.)
3. Choose your device. The bot names the app to install and gives one button for your link:

| Your device | Install | Tap in the bot |
|---|---|---|
| 🤖 Android | [ZapretKVN](https://git.zapret.moe/zapretkvn/ZapretKVN-android/releases/latest), file `…-arm64-v8a.apk` | «🔗 Получить Xray-подписку» (Get Xray subscription) |
| 🍏 iPhone, iPad | [Clash Mi](https://clashmi.app/download) | «🧭 Получить Mihomo-подписку» (Get Mihomo subscription) |
| 🪟 Windows | [Zapret KVN](https://git.zapret.moe/zapretkvn/zapret-kvn) | «🔗 Получить Xray-подписку» (Get Xray subscription) |
| 💻 Mac, Linux | [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) | «🧭 Получить Mihomo-подписку» (Get Mihomo subscription) |

4. The bot shows a card with your link `https://…`. **Tap the link — Telegram copies it.**

> [!warning] The link is personal
> Anyone with your link can use your VPN. Do not post it in chats or show it on screenshots. If it leaked, open the subscription card → «⋯ Ещё» (More) → «♻️ Сменить ссылку» (Change link).

## Step 4. Turn on the VPN

1. Open the app and add the link as a subscription: in ZapretKVN for Android «Серверы» → «Ссылка» → paste; in Zapret KVN for Windows — add a subscription by link; in Clash apps — «Profiles» → add by URL.
2. If the server list is empty, refresh the subscription.
3. Pick a server and press the big connect button. Android and iPhone ask for VPN permission the first time — allow it.
4. Check: open YouTube or a site that does not open without a VPN.

On Windows, Zapret KVN has two modes. **«VPN (TUN)»** sends the whole computer through the VPN — choose it if unsure. **«Прокси»** (Proxy) covers only programs that use the system proxy.

## Telegram

Our Telegram client [ZaStoGram](https://t.me/zastogram) (Android and Windows) bypasses the Telegram block by itself, without a VPN. With the VPN on, the regular Telegram works too.

## Help

| Need | Where |
|---|---|
| ask a question | in the bot: «💬 Поддержка» (Support) → «🎫 Создать тикет» (Create ticket) — available on any plan |
| direct contacts of the support team | «💬 Поддержка» → «Поддержка Premium» — from 🚀 MasterVless Plus, included in 💎 Vless MAX |
| is a server down | [status.zapret.moe](https://status.zapret.moe) — live status of every server |
| more details | the full guide in Russian: [[Zapret/premium\|Zapret VPN: how to buy and connect]] (your browser can translate it) |

---

> [!quote] 🤖 These articles are open — you may train AI on them
> The source is available on Forgejo: [this note's source](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/premium/english.md) · [the whole repository as one zip](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
