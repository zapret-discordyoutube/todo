#!/usr/bin/env python3
"""Пост в разметке `код`, [текст](url) и строк "> цитата" -> HTML, который Telegram Desktop вставляет с форматированием.

Строки подряд с префиксом "> " склеиваются в одну цитату <blockquote>: lib_ui
(ui/text/text_html_tags.cpp) переводит её при вставке в обычную цитату Telegram.
"""
import html, re, shutil, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read().rstrip()
# Пост не называет наш домен (решение владелицы от 30 октября 2026, pve-admin servers.md «Entry pages»): каждая ссылка на вики
# и git становится входной (страница на большой платформе ведёт на рабочее зеркало), заблокированное имя без ссылки — рабочим.
# Адрес входной страницы и его формат знает только служба zapret-links (~/zapret-links). Картинки идут отдельными аргументами и не трогаются.
if shutil.which('zapret-links'):
    fixed = subprocess.run(['zapret-links', 'rewrite', '--entry'], input=t, capture_output=True, text=True, check=True).stdout
    if fixed != t:
        print('ссылки на вики и git в посте заменены на входные (Apps Script сейчас, потом Cloud Storage); текст поста менять не нужно',
              file=sys.stderr)
        t = fixed
esc = lambda s: html.escape(s).replace('\n', '<br>')

def inline(s):
    out, last = [], 0
    for m in re.finditer(r'`([^`\n]+)`|\[([^\]\n]+)\]\((https?://[^)\s]+)\)', s):
        out.append(esc(s[last:m.start()]))
        out.append(f'<code>{html.escape(m[1])}</code>' if m[1] is not None
                   else f'<a href="{html.escape(m[3])}">{esc(m[2])}</a>')
        last = m.end()
    out.append(esc(s[last:]))
    return ''.join(out)

# Разбиваем на куски: обычный текст и цитаты (подряд идущие строки "> ...").
parts, buf, quote = [], [], False
for line in t.split('\n'):
    is_q = line.startswith('> ') or line == '>'
    if is_q != quote and buf:
        parts.append((quote, buf)); buf = []
    quote = is_q
    buf.append(line[2:] if line.startswith('> ') else ('' if line == '>' else line))
if buf:
    parts.append((quote, buf))
body = ''
for i, (q, lines) in enumerate(parts):
    chunk = inline('\n'.join(lines))
    body += f'<blockquote>{chunk}</blockquote>' if q else chunk
    if i < len(parts) - 1 and not q:
        body += '<br>'
# Необязательные аргументы: название страницы и картинки для поста в виде "Подпись|https://…".
title = sys.argv[3] if len(sys.argv) > 3 else 'Пост для Telegram'
pics = [a.split('|', 1) for a in sys.argv[4:] if '|' in a]
pics_html = ''
if pics:
    items = ''.join(f'<li><a href="{html.escape(u)}">{html.escape(n)}</a></li>' for n, u in pics)
    pics_html = f'<section id="pics"><h2>Картинки для поста</h2><ol>{items}</ol></section>'

# Страница без <!doctype>, <html>, <head>, <body>: так её требует Artifact (он сам оборачивает файл),
# а локально браузер открывает её и в таком виде. Один тёмный вид «как в Telegram», все цвета — токены.
page = f'''<title>{html.escape(title)}</title>
<style>
/* Раскладка: узкая колонка — панель с кнопкой, пузырь поста, под ним ссылки на картинки. */
:root{{--bg:#17212b;--bubble:#182533;--quote:#1e3043;--fg:#e6edf3;--muted:#8fa0b1;--link:#5eaff0;--code:#b79bff;--btn-fg:#0f1720;color-scheme:dark}}
body{{margin:0;padding-block:20px;padding-inline:16px;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"Segoe UI",Roboto,sans-serif}}
#bar,#post,#pics{{max-width:560px;margin-inline:auto}}
#bar{{margin-bottom:12px;user-select:none;display:flex;flex-wrap:wrap;gap:10px;align-items:center}}
#post{{background:var(--bubble);border-radius:12px;padding:12px 14px;overflow-wrap:anywhere}}
#post a,#pics a{{color:var(--link);text-decoration:none}} #post code{{font-family:Consolas,ui-monospace,monospace;color:var(--code)}}
#post blockquote{{margin:4px 0;padding:4px 10px;border-left:3px solid var(--link);background:var(--quote);border-radius:4px}}
button{{font:500 15px system-ui,sans-serif;border:0;border-radius:8px;padding:9px 16px;background:var(--link);color:var(--btn-fg);cursor:pointer}}
button:focus-visible,a:focus-visible{{outline:2px solid var(--fg);outline-offset:2px}}
#st{{color:var(--muted);font-size:14px;min-width:0}}
#pics{{margin-top:18px;color:var(--muted);font-size:14px;user-select:none}} #pics h2{{font-size:14px;font-weight:600;margin:0 0 6px;color:var(--fg)}} #pics ol{{margin:0;padding-left:20px}}
</style>
<div id="bar"><button id="b">Скопировать</button><span id="st">или выделите пост и нажмите Ctrl+C</span></div>
<div id="post">{body}</div>
{pics_html}
<script>
document.getElementById('b').onclick=async()=>{{
  const p=document.getElementById('post'), st=document.getElementById('st');
  try{{await navigator.clipboard.write([new ClipboardItem({{'text/html':new Blob([p.innerHTML],{{type:'text/html'}}),'text/plain':new Blob([p.innerText],{{type:'text/plain'}})}})]);st.textContent='Скопировано, вставляйте в Telegram через Ctrl+V';return;}}catch(e){{}}
  const r=document.createRange();r.selectNodeContents(p);const s=getSelection();s.removeAllRanges();s.addRange(r);
  let ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}
  st.textContent=ok?'Скопировано, вставляйте в Telegram через Ctrl+V':'Пост выделен, нажмите Ctrl+C';
}};
</script>
'''
open(dst, 'w', encoding='utf-8').write(page)
