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
  - Zapret VPN bot English buttons
description: "Zapret VPN guide in English: the bot @zapretvpns_bot speaks English; this page names every button you need and walks you from payment to a working VPN."
---

> [!mirror] Backup mirror
> The main version of this page is on the wiki: [wiki.zapret.moe/premium/english](https://wiki.zapret.moe/premium/english)

# 🇬🇧 Zapret VPN in English

> [!info] In short
> Zapret VPN is a personal VPN that works in Russia. You buy it in the Telegram bot [@zapretvpns_bot](https://telegram.me/zapretvpns_bot), get **one link**, paste it into a VPN app once — and the app gets all your servers from it. The bot speaks English: below every button is quoted as the English bot shows it, with the Russian name in brackets in case your bot is in Russian.

**Bot language.** The bot picks its language from your Telegram language by itself: if Telegram is in English, the bot answers in English. To choose it manually, send /language or open «⚙️ Settings» («⚙️ Настройки») → «🌐 Язык / Language». A few rare screens, such as the privacy policy, are still in Russian only.

## The whole path in four steps

| Step | Where | What to tap | What you get |
|---|---|---|---|
| 1. Top up the balance | bot | «💳 Plan and balance» → «💰 Top up» → amount → pay | money on your bot balance |
| 2. Buy a plan | bot | «🛒 Buy / renew» → plan → period → confirm | an active plan |
| 3. Get your link | bot | «🚀 Connect a device» → «🌐 Whole internet (VPN)» → your device → the subscription button | a link `https://…` |
| 4. Turn on the VPN | app | add the link as a subscription, pick a server, connect | a working VPN |

If you don't know which plan to take — take **💎 Vless MAX** (199 ₽ a month): it has 15 servers instead of 2 and all Telegram proxies.

## Step 1. Top up the balance

1. Open [@zapretvpns_bot](https://telegram.me/zapretvpns_bot) and tap «Start».
2. Tap **«💳 Plan and balance»** («💳 Подписка и баланс»), then **«💰 Top up»** («💰 Пополнить»).
3. Choose an amount or type it in digits, for example `199`.
4. Tap the payment button, open the link it gives and pay with SBP (Russia's fast payment system) in your bank app.
5. Come back to the bot: the money arrives by itself within seconds. If nothing changed after a minute, tap «🔄 Check payment» («🔄 Проверить оплату»): the card switches to «🔄 Checking the payment…» and a few seconds later shows the answer in the same card — paid, still processing or not paid. The bot sends a separate message once the money is credited.

## Step 2. Buy a plan

1. On the same screen tap **«🛒 Buy / renew»** («🛒 Купить / продлить»).
2. Choose a plan — **💎 Vless MAX** if unsure — then the period.
3. Confirm. The bot answers «✅ Subscription successfully purchased!» («✅ Подписка успешно оформлена!») and shows the next step.

## Step 3. Get your link

1. In the main menu tap the green button **«🚀 Connect a device»** («🚀 Подключить устройство»).
2. Tap **«🌐 Whole internet (VPN)»** («🌐 Весь интернет (VPN)»). «✈️ Telegram only» («✈️ Только Telegram») gives a proxy inside Telegram instead.
3. Choose your device. The bot names the app to install and gives one button for your link:

| Your device | Install | Tap in the bot |
|---|---|---|
| 🤖 Android | [ZapretKVN](https://git.zapret.moe/zapretkvn/ZapretKVN-android/releases/latest), file `…-arm64-v8a.apk` | «🔗 Get Xray subscription» («🔗 Получить Xray-подписку») |
| 🍏 iPhone / iPad | [Clash Mi](https://clashmi.app/download) | «🧭 Get Mihomo subscription» («🧭 Получить Mihomo-подписку») |
| 🪟 Windows | [Zapret KVN](https://git.zapret.moe/zapretkvn/zapret-kvn) | «🔗 Get Xray subscription» |
| 💻 macOS / Linux | [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) | «🧭 Get Mihomo subscription» |

4. The bot shows a card with your link `https://…`. **Tap the link — Telegram copies it.**

> [!warning] The link is personal
> Anyone with your link can use your VPN. Do not post it in chats or show it on screenshots. If it leaked, open the subscription card → «⋯ More» («⋯ Ещё») → «♻️ Change link» («♻️ Сменить ссылку»).

## Step 4. Turn on the VPN

1. Open the app and add the link as a subscription: in ZapretKVN for Android «Серверы» → «Ссылка» → paste; in Zapret KVN for Windows — add a subscription by link; in Clash apps — «Profiles» → add by URL.
2. If the server list is empty, refresh the subscription. An empty list explains itself: its entries say what to do, for example «⚠️ No keys yet — open the bot».
3. Pick a server and press the big connect button. Android and iPhone ask for VPN permission the first time — allow it.
4. Check: open YouTube or a site that does not open without a VPN.

In Mihomo apps (Clash Mi, Clash Verge Rev) the choice is in the group «🌐 VPnBot»: «🛡 Stable» keeps the first working server, «⚡ By latency» picks the fastest one, «👆 Manual choice» is any server from the list. If your bot is in Russian, these groups have Russian names.

On Windows, Zapret KVN has two modes. **«VPN (TUN)»** sends the whole computer through the VPN — choose it if unsure. **«Прокси»** (Proxy) covers only programs that use the system proxy.

## Personal account website

Your plan, balance, payments and subscription links with QR codes can also be viewed in a browser at [lk.zapret.moe](https://lk.zapret.moe). It is handy on a computer: point your phone's camera or app scanner at the QR code instead of copying the link. The site is in Russian. You can top up your balance there (10 to 10,000 ₽, via Pally or Antilopay): the page waits for the bill and then shows a «Перейти к оплате» (Go to payment) button. Payment opens in a new tab, and the account tab itself shows «Оплата получена» (payment received) once the money arrives; Pally opens the bot in that second tab after payment — you can close it. You can also buy or extend a plan from your balance there: on «📋 Все тарифы» (all plans) each period your balance covers has a «Купить» (Buy) button, and the site offers the same merge-or-separate choice as the bot. Auto-renewal can be turned on or off there too, and with several subscriptions you choose which one renews. Plan upgrades are on the «⬆️ Повысить тариф» (upgrade) page: the remaining days count towards the new plan and the difference comes from your balance. Mihomo device slots can be added, have their link changed, have their servers and protocols chosen or be switched off on the «🧭 Mihomo-подписка» page. The «🔗 Xray-подписка» page turns on the single VLESS/VMess/Trojan subscription: the site picks the recommended servers, prepares keys on them, refreshes itself while showing «готово N из M» (N of M ready) and then shows the link with a QR code — the same link the bot shows. Under the link, «Сменить ссылку» (change link) issues a new one on the page and the old one stops working (the bot's card goes stale — reopen the section in the bot), «Выключить ссылку» (switch off) closes it, and «Удалить подписку» (delete) removes it together with all your Xray keys on the servers, as in the bot. «Состав подписки» (composition) is the same choice as in the bot — the recommended set (with regions and number of nodes), existing keys only, chosen servers or all available ones; the site shows what you will get before applying, and the link address stays the same. From that page, «Ключи по серверам» (keys by server) issues a single VLESS/VMess/Trojan key on one server, like the bot's server list: pick a server and a connection variant (✅ — you already have a key, ➕ — none, «рекомендуем» — recommended), press «Получить ключ» (get key), and the page refreshes itself and shows the key with a QR code; the key is visible in the bot too, and nothing is sent to Telegram. A key can be moved to another variant of the server there («Перенести на другой вариант», like 🔄 in the bot: the old key stops working, the new one appears on that variant's page), renamed («Переименовать ключ», up to 20 characters, shown in the app and the bot) or deleted («Удалить ключ»). The «🔐 AWG 2.0», «🗝 AWG 3.0» and «🛡 WireGuard» pages work like those sections of the bot: pick a device slot, then a server, press «Получить ключ» (get key), and the page refreshes itself and offers the .conf file for AmneziaVPN («⬇️ Скачать …conf») and its QR code; nothing is sent to Telegram, and the key is visible in the bot too. A broken AWG key can be repaired («🛠 Восстановить ключ») and any key deleted there; a WireGuard key is repaired, and the whole-slot archive built, in the bot. The «📡 MTProxy личный» (personal MTProxy) and «⚡ MTProxy Zig» pages work like those sections of the bot: pick a server, press «Получить ключ» (get key), and the page refreshes itself and shows a «🔗 Подключить прокси» (connect proxy) button, the link and its QR code; nothing is sent to Telegram, the key is visible in the bot too, and it can be deleted there. If a server moved to a new backend and the key has to be replaced, the site asks you to get it in the bot, which sends the new key as a message. The «🌀 WARP» page works like the bot's WARP section: pick a device slot (✅ — a config is there, ➕ — none), then «⚙️ Настройки по умолчанию» (default settings) or one of the bot's quick scenarios (💡 — recommended for your plan, 🔒 — not in your plan); the page refreshes itself and shows the config: the .conf file for AmneziaWG or WireGuard («📄 Скачать …conf»), its QR code and its text — the same config the bot would send as a file, and nothing is sent to Telegram. A new config is a new WARP account; the page shows the latest one. Fine tuning (endpoint, DNS, MTU, masking, NAT64), WARP+, Clash Ultimate and the NAT64 pack stay in the bot. The «🆘 Поддержка» (support) page lists your tickets and opens a new one with the same questions as the bot (bug, idea, refund, partnership or question); a ticket's page shows the whole conversation with support, a reply box, «✅ Вопрос решён» (resolved) and «↩️ Вернуть в работу» (reopen). Support replies appear on the page and also arrive as a Telegram message; if you blocked the bot, the reply is still on the page. Files and screenshots are attached in the bot for now. The «⚡ Hysteria 2-подписка» page turns on the single Hysteria 2 subscription: the site creates keys on all available servers, refreshes itself, and once the keys are ready «Показать ссылку здесь» (show the link here) puts the link and its QR code on the page — the same link the bot shows; the link can be changed, switched off, or the subscription deleted with its Hysteria 2 keys there too, and «Состав подписки» (composition) offers the same server choice as the bot. From that page, «🔑 Ключи по серверам» (keys by server) gives a single Hysteria 2 key on one server, like the bot's server list: ✅ — you have a key, ➕ — none; «Получить ключ» (get key) puts the key and its QR code on the page, nothing is sent to Telegram, and «Удалить ключ» (delete key) removes it; deleting all keys at once stays in the bot. Automatic top-ups can be switched off on the «🔁 Автопополнения» (auto top-ups) page; setting them up stays in the bot. The «🚀 Подключить устройство» (connect a device) page is the same setup wizard as in the bot; its «Получить…» buttons open the bot right on that subscription or config. The «📋 Все тарифы» (all plans) and «🎁 Рефералы» (referrals) pages show the same plans with prices and your referral link and bonuses as the bot. The «🏳 Белые списки» (whitelists) page lists the shared Telegram proxies for whitelist blocking: the ones your plan includes have a connect button, the link and a QR code. A one-time donation to the project is on the «💝 Донат» (donate) page. The section buttons at the top of the page marked ↗ (VPN, Telegram proxies, Zapret Premium) open the bot right on that screen.

There is no password; you sign in from the bot:

1. In the bot open «💳 Plan and balance» and tap «🌐 Personal account» («🌐 Личный кабинет»).
2. Tap «Open my account» («Открыть кабинет») on the device where you want to see the account.
3. On the site press «Войти» (Sign in).

The sign-in link works once, for 5 minutes. Do not forward it: whoever opens it first gets into your account. If someone else saw the link or your open account, tap «🚪 Sign out everywhere» («🚪 Закрыть все входы») on the same bot card, then change your subscription links.

## Telegram

Our Telegram client [ZaStoGram](https://t.me/zastogram) (Android and Windows) bypasses the Telegram block by itself, without a VPN. With the VPN on, the regular Telegram works too.

## Help

| Need | Where |
|---|---|
| ask a question | in the bot: «💬 Support» («💬 Поддержка») → «🎫 Create ticket» («🎫 Создать тикет») — available on any plan |
| direct contacts of the support team (Premium support) | «💬 Support» → «💬 Go to the group» or the support agent's button — from 🚀 MasterVless Plus, included in 💎 Vless MAX |
| is a server down | [status.zapret.moe](https://status.zapret.moe) — live status of every server |
| more details | the full guide in Russian: [[Zapret/premium\|Zapret VPN: how to buy and connect]] (your browser can translate it) |

---

> [!quote] 🤖 These articles are open — you may train AI on them
> The source is available on Forgejo: [this note's source](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/premium/english.md) · [the whole repository as one zip](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
