---
publish: false
---

# AGENTS.md — правила работы с этим репозиторием

Это Obsidian-хранилище проекта ZapretKVN (приватность, обход DPI и цензуры). Его Git-репозиторий хранится в Forgejo: `zapretdiscordyoutube/todo` на `git.zapret.moe`; материалы публикуются на сайт `https://wiki.zapret.moe` (self-hosted Quartz 4, живёт на этом же хосте в `/srv/wiki-quartz`). Публикация привязана к Git: **каждый локальный коммит в vault автоматически пересобирает сайт** (systemd-юнит `wiki-rebuild.path` следит за `.git/logs/HEAD` и запускает `wiki-rebuild.service`). Отдельного шага «опубликовать» больше нет.

## Git-процесс: коммитим прямо в `main`

**Ветки и pull request'ы не используются.** Готовые правки коммитятся напрямую в `main` и пушатся — это решение владельца репозитория (25 июля 2026), принятое взамен прежней схемы «ветка → PR → merge».

Почему так: репозиторий ведёт один человек, ревьюить PR некому, а Forgejo Actions здесь запускают проверку на `push` в `main` (см. ниже). PR не давал дополнительного ревью, а только добавлял лишний шаг.

Порядок работы:

- `git fetch origin` перед началом, чтобы не разойтись с remote;
- добавлять в staging **только подтверждённые файлы**, не `git add -A` вслепую;
- `git diff --check` перед коммитом;
- осмысленное сообщение коммита на русском: первая строка — суть, дальше абзац с деталями;
- `git push` в `main`.

Не коммитить: `.obsidian/`, `.agents/`, `.claude/` и прочие служебные каталоги (часть из них уже в `.gitignore`).

## Forgejo Actions

На каждый `push` в `main` срабатывает workflow `.forgejo/workflows/content-check.yml`. Он получает текущий commit и его непосредственного родителя, чтобы проверять именно новая правка, а не всю историю хранилища. Workflow проверяет:

- что в последнем опубликованном commit нет проблем с пробелами и концами строк через `git diff --check HEAD^ HEAD`;
- что корневой `index.html` существует и не пуст.

Публикацию на сайт этот workflow не выполняет — сайт собирается локальным systemd-юнитом, см. ниже.

## Публикация на сайт (wiki.zapret.moe)

Сайт — статический, собирается Quartz 4 прямо из этого vault (`npx quartz build -d /home/codex-pve/Privacy` в `/srv/wiki-quartz`). Запускать руками ничего не нужно: **любой коммит в vault триггерит пересборку** через `wiki-rebuild.path`. Принудительная пересборка без коммита: `sudo systemctl start wiki-rebuild.service` или `/usr/local/bin/wiki-rebuild`.

URL заметки = путь в vault со слагами Quartz (пробелы → `-`, кириллица сохраняется): `Zapret/home.md` → `https://wiki.zapret.moe/Zapret/home`. Главная `/` — это alias `index` в frontmatter `Zapret/home.md`.

**Как исключить файл из публикации:** добавить в его frontmatter `publish: false` — фильтр `RemoveNoPublish` в Quartz не пропустит такую заметку на сайт, при этом она остаётся в Git. Так исключён сам `AGENTS.md`.

**Закрытые разделы.** Папки `VPS/`, `scripts/`, `.obsidian/`, `.claude/`, `.agents/`, `.forgejo/` и корневые `index.html`, `AGENTS.md` вырезаются на уровне `ignorePatterns` в `/srv/wiki-quartz/quartz.config.ts` — в сборку не попадают ни заметки, ни вложения из них. В `VPS/` лежат IP, пароли и детали инфраструктуры — новые закрытые папки добавлять именно в `ignorePatterns`, а не полагаться только на `publish: false` (frontmatter не защищает вложения).

**При переименовании заметки** старый путь исчезает с сайта сам при следующей пересборке; чтобы старые внешние ссылки не ломались, можно добавить старый слаг в `aliases:` frontmatter — Quartz сделает редирект.

**Историческая справка:** до 20 августа 2026 сайт жил на Obsidian Publish (`publish.obsidian.md/zapret`) и публиковался через `scripts/publish-safe.sh` и Obsidian CLI (`publish:add`). Подписка закончилась, скрипт устарел и оставлен только как история; команды `publish:*` больше не используются.

## Проверка перед публикацией

Вместо ручных grep-скриптов используйте встроенные проверки CLI:

```bash
"$HOME/.local/bin/obsidian" vault="Privacy" unresolved counts   # битые [[wikilinks]] по всему хранилищу
"$HOME/.local/bin/obsidian" vault="Privacy" orphans             # заметки без входящих ссылок (сироты)
"$HOME/.local/bin/obsidian" vault="Privacy" links path=…        # исходящие ссылки конкретной заметки
"$HOME/.local/bin/obsidian" vault="Privacy" backlinks path=…    # кто ссылается на заметку
```

После добавления новой заметки `unresolved` не должен приобретать новых записей из-за неё, а сама заметка не должна оставаться в `orphans` — если осталась, не хватает ссылки из соседней заметки или из обзора раздела.

## Заметки

Правила написания заметок вынесены в скилл **`vault-note`** (`.claude/skills/vault-note/SKILL.md`) — он обязателен при создании, правке и публикации любой `.md` в этом хранилище: самодостаточность, атомарность, frontmatter, callout-ы, `[[wikilinks]]`, Forgejo-футер, запрет ручных переносов прозы.

Отдельное правило: **`Zapret/home.md` не трогать** — навигацию на главной ведёт владелец вручную.
