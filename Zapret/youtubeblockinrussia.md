---
tags:
link:
aliases:
img:
description: "Как обойти блокировку YouTube в Zapret: за что отвечают области YouTube TCP, YouTube QUIC и GoogleVideo и какую включать, если видео не грузятся."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/Zapret/youtubeblockinrussia](https://wiki.zapret.moe/Zapret/youtubeblockinrussia)

# Как обойти блокировку YouTube
По умолчанию в запрете включено 3 области для обхода Ютуба:

![[Pasted image 20260101185946.png]]

- `Youtube TCP` — обходит основной сайт (интерфейс https://www.youtube.com)
- `YouTube QUIC` — обходит блокировку по протоколу QUIC (обычно включен в браузере Edge, но часто выключен, особенно для пользователей из под РФ)
- `GoogleVideo` — обходит блокировку непосредственно CDN-серверов YouTube (сервера типа https://rr2---sn-aigl6nze.googlevideo.com), они отвечают за загрузку непосредственно самого контента. Эта вкладка полезна когда сам сайт ютуба работает, а видео внутри видеоплеера не загружаются.