---
tags:
link:
aliases:
img:
description: "Пути установки Zapret 2 GUI на Windows: папки ZapretTwo в ProgramData, ветки реестра HKCU для stable и dev, удаление через unins000.exe."
---

> [!mirror] Резервное зеркало
> Актуальная версия этой страницы — на основной вики: [wiki.zapret.moe/Zapret/path](https://wiki.zapret.moe/Zapret/path)

# Пути установки Zapret 2 GUI
## Stable ветка
- Путь установочных файлов в проводнике — `C:\ProgramData\ZapretTwo`
- Путь реестра — `Компьютер\HKEY_CURRENT_USER\SOFTWARE\Zapret2Reg`

## Dev ветка
- Путь установочных файлов в проводнике — `C:\ProgramData\ZapretTwoDev`
- Путь реестра — `Компьютер\HKEY_CURRENT_USER\SOFTWARE\Zapret2DevReg

Чтобы удалить программу запустите `unins000.exe` файл по пути `C:\ProgramData\ZapretTwo\unins000.exe` для stable и `C:\ProgramData\ZapretTwoDev\unins000.exe` для dev.

Чтобы очистить реестр запустите через `win + x` -> `Windows PowerShell (администратор)` -> `reg delete "HKCU\SOFTWARE\Zapret2Reg" /f` для stable и `reg delete "HKCU\SOFTWARE\Zapret2DevReg" /f` для dev