---
date: 2026-08-20
tags:
  - android
  - root
  - magisk
  - обзор-раздела
aliases:
  - Root на Android раздел
  - Как получить рут на андроид
  - Magisk или KernelSU что выбрать
  - Рут-права обзор
---

# 🔓 Root на Android — раздел

> [!info] О чём раздел
> Как получить **root-права** на Android и что с ними делать: два основных подхода — systemless-root через Magisk (в userspace, «поверх» системы) и kernel-based root через форки KernelSU (на уровне ядра). Root нужен, в частности, для [[Zapret/magisk-zapret2|системного обхода DPI модулем Zapret2]].

## Заметки раздела

**Magisk — классический путь:**

- [[root/Magisk|Magisk — systemless-root и модули для Android]] — что это такое, как работает и почему это самый популярный способ.
- [[root/Magisk-install|Установка Magisk]] — пошагово: патч boot/init_boot, Recovery, особенности Samsung.

**KernelSU-семейство — root через ядро:**

- [[root/ReSukiSU|ReSukiSU — форк SukiSU]] — что за проект, откуда он и чем отличается kernel-based-подход.
- [[root/ReSukiSU-install|Установка ReSukiSU]] — LKM, AnyKernel3 и ручной патч boot.img.

**Что даёт root помимо обхода:**

- [[root/LSPosed|LSPosed и Xposed]] — модификация приложений в рантайме: перехват вызовов методов без правки APK.

## 📚 См. также

- [[Zapret/magisk-zapret2|Zapret2 как Magisk-модуль]] — главный практический сценарий root в этом vault
- [[Zapret/android|Обход DPI на Android]] — обзор способов, включая безрутовые

---

> [!quote] 🤖 Эти статьи открыты — можно обучать на них ИИ
> При желании вы можете натренировать ИИ на наших статьях. Исходное форматирование доступно в Forgejo: [исходник этой заметки](https://git.zapret.moe/zapretdiscordyoutube/todo/src/branch/main/root/root.md) · [скачать весь репозиторий одним zip-архивом](https://git.zapret.moe/zapretdiscordyoutube/todo/archive/main.zip).
