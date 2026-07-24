#!/usr/bin/env bash
# Публикация в Obsidian Publish всего, что изменилось, КРОМЕ закрытых разделов.
# Заметки исключаются свойством `publish: false` во frontmatter, но на вложения
# (png и прочие ассеты) оно не действует — поэтому папки из EXCLUDE фильтруются здесь.
set -uo pipefail

OBS="${OBSIDIAN_CLI:-$HOME/.local/bin/obsidian}"
VAULT="${OBSIDIAN_VAULT:-Privacy}"
EXCLUDE_RE='^VPS/'          # закрытые разделы: их вложения не публикуем никогда

queue=$("$OBS" vault="$VAULT" publish:status </dev/null 2>&1)
if [ "$queue" = "No changes." ]; then
  echo "Нечего публиковать."; exit 0
fi

published=0; skipped=0
while IFS=$'\t' read -r state path; do
  [ -n "${path:-}" ] || continue
  if printf '%s' "$path" | grep -qE "$EXCLUDE_RE"; then
    echo "пропуск (закрытый раздел): $path"; skipped=$((skipped+1)); continue
  fi
  out=$("$OBS" vault="$VAULT" publish:add path="$path" </dev/null 2>&1 | tail -1)
  echo "$state → $path: $out"; published=$((published+1))
done <<< "$queue"

echo "Опубликовано: $published, пропущено: $skipped"
"$OBS" vault="$VAULT" publish:status </dev/null 2>&1 | tail -3
