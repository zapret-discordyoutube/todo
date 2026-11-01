#!/usr/bin/env python3
"""Рендер HTML-диаграммы в PNG через headless Chromium.

    render.py chart.html out.png [--width 1200] [--height auto|675] [--scale 2]

Что делает:
  1. Проверяет, что в системе есть шрифт Inter Variable; если нет, ставит его
     из assets/fonts скилла в ~/.local/share/fonts.
  2. Первым проходом меряет реальный размер страницы. При --height auto
     холст подгоняется под содержимое; при фиксированной высоте печатает
     предупреждение, если содержимое не влезает и низ обрежется.
  3. Снимает PNG с --force-device-scale-factor (по умолчанию ×2: CSS 1200 px
     -> файл 2400 px).
  4. Рядом кладёт превью шириной 400 px (<out>.tg400.png) — так картинку
     видят в ленте Telegram на телефоне. Превью в vault не копировать.
  5. Заблокированные имена сайтов (старые имена вики и git и любое
     следующее с флагом blocked в реестрах хоста) в подписях заменяет на рабочие
     через zapret-links и предупреждает: впечатанное в пиксели имя потом
     никакой заменой текста не исправить.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_SRC = os.path.join(SKILL, "assets", "fonts", "InterVariable.ttf")
FONT_DIR = os.path.expanduser("~/.local/share/fonts/inter")

MEASURE = """<script>
addEventListener('load', () => document.fonts.ready.then(() => {
  const e = document.documentElement, b = document.body;
  let w = Math.max(e.scrollWidth, b.scrollWidth), h = Math.max(e.scrollHeight, b.scrollHeight), ink = 0;
  // Содержимое SVG с overflow: visible не растягивает scroll-размеры — меряем элементы.
  for (const el of document.querySelectorAll('svg *')) {
    const r = el.getBoundingClientRect();
    if (r.width || r.height) {
      w = Math.max(w, r.right + scrollX); h = Math.max(h, r.bottom + scrollY);
      ink = Math.max(ink, r.right + scrollX);
    }
  }
  const field = b.getBoundingClientRect().right - parseFloat(getComputedStyle(b).paddingRight);
  // Первым в font-family у всего видимого текста должен стоять "Inter Variable":
  // имя Inter и system-ui (дефолт Observable Plot) на хосте молча дают DejaVu или serif.
  const bad = new Set();
  for (const el of document.body.querySelectorAll('*')) {
    if (['SCRIPT', 'STYLE'].includes(el.tagName)) continue;
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const ff = getComputedStyle(el).fontFamily;
    if (!/^["']?Inter Variable/.test(ff) && !/mono/i.test(ff)) bad.add(ff);
  }
  e.setAttribute('data-render-fonts', encodeURIComponent([...bad].join(' | ')));
  e.setAttribute('data-render-size', Math.ceil(w) + 'x' + Math.ceil(h));
  e.setAttribute('data-render-field', Math.ceil(ink) + 'x' + Math.floor(field));
}));
</script>"""


def find_chrome():
    pats = [
        "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell",
        "~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome",
    ]
    for p in pats:
        hits = sorted(glob.glob(os.path.expanduser(p)))
        if hits:
            return hits[-1]
    for name in ("chromium", "chromium-browser", "google-chrome"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("Chromium не найден: ни в ~/.cache/ms-playwright, ни в PATH")


def ensure_inter():
    out = subprocess.run(["fc-list", ":family=Inter Variable"], capture_output=True, text=True).stdout
    if out.strip():
        return
    os.makedirs(FONT_DIR, exist_ok=True)
    shutil.copy(FONT_SRC, FONT_DIR)
    subprocess.run(["fc-cache", "-f", FONT_DIR], check=True, capture_output=True)
    print(f"Inter Variable установлен в {FONT_DIR}", file=sys.stderr)


def chrome(bin_, args):
    base = [bin_, "--no-sandbox", "--hide-scrollbars", "--disable-gpu",
            "--virtual-time-budget=10000"]
    r = subprocess.run(base + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Chromium завершился с ошибкой:\n{r.stderr[-2000:]}")
    return r.stdout


def measure(bin_, html, width, height):
    with open(html, encoding="utf-8") as f:
        src = f.read()
    src = src.replace("</body>", MEASURE + "</body>", 1) if "</body>" in src else src + MEASURE
    # Копия рядом с оригиналом, чтобы работали относительные пути к файлам.
    fd, tmp = tempfile.mkstemp(suffix=".html", dir=os.path.dirname(html))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(src)
        dom = chrome(bin_, [f"--window-size={width},{height}", "--dump-dom", "file://" + tmp])
    finally:
        os.unlink(tmp)
    m = re.search(r'data-render-size="(\d+)x(\d+)"', dom)
    f = re.search(r'data-render-field="(\d+)x(\d+)"', dom)
    if not m or not f:
        sys.exit("Не удалось измерить страницу: скрипт замера не отработал (ошибка JS в странице?)")
    fonts = re.search(r'data-render-fonts="([^"]*)"', dom)
    if fonts and fonts.group(1):
        from urllib.parse import unquote
        print(f"ВНИМАНИЕ: текст не в Inter Variable, font-family: {unquote(fonts.group(1))}", file=sys.stderr)
    ink, field = int(f.group(1)), int(f.group(2))
    if ink > field:
        print(f"ВНИМАНИЕ: элементы SVG заходят на правое поле ({ink} > {field} CSS px)", file=sys.stderr)
    return int(m.group(1)), int(m.group(2))


def with_site_names(html):
    """Путь к HTML для рендера: исходник или его копия рядом, где заблокированные имена
    сайтов заменены на рабочие (служба zapret-links). Второе значение — удалить ли копию."""
    tool = shutil.which("zapret-links")
    if not tool:
        return html, False
    with open(html, encoding="utf-8") as f:
        src = f.read()
    fixed = subprocess.run([tool, "rewrite"], input=src, capture_output=True, text=True, check=True).stdout
    if fixed == src:
        return html, False
    found = subprocess.run([tool, "check", html], capture_output=True, text=True).stdout
    print("ВНИМАНИЕ: в HTML заблокированное имя сайта, на картинке оно заменено на рабочее "
          f"({subprocess.run([tool, 'link', 'wiki'], capture_output=True, text=True).stdout.strip()}, "
          f"{subprocess.run([tool, 'link', 'git'], capture_output=True, text=True).stdout.strip()}). "
          "Поправь исходник: zapret-links rewrite " + html + "\n" + found, file=sys.stderr)
    fd, tmp = tempfile.mkstemp(suffix=".html", dir=os.path.dirname(html))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(fixed)
    return tmp, True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1200, help="ширина холста в CSS px")
    ap.add_argument("--height", default="auto", help="высота в CSS px или auto (по содержимому)")
    ap.add_argument("--scale", type=float, default=2, help="device scale factor")
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    bin_ = find_chrome()
    ensure_inter()
    html, tmp_html = with_site_names(os.path.abspath(a.html))
    try:
        render(a, bin_, html, out)
    finally:
        if tmp_html:
            os.unlink(html)


def render(a, bin_, html, out):
    # scrollHeight не бывает меньше окна, поэтому для auto меряем в низком окне.
    probe_h = 100 if a.height == "auto" else int(a.height)
    cw, ch = measure(bin_, html, a.width, probe_h)
    if cw > a.width:
        print(f"ВНИМАНИЕ: содержимое шире холста ({cw} > {a.width} CSS px), правый край обрежется", file=sys.stderr)
    if a.height == "auto":
        h = ch
    else:
        h = int(a.height)
        if ch > h:
            print(f"ВНИМАНИЕ: содержимое выше холста ({ch} > {h} CSS px), низ обрежется", file=sys.stderr)

    chrome(bin_, [f"--window-size={a.width},{h}", f"--force-device-scale-factor={a.scale:g}",
                  f"--screenshot={out}", "file://" + html])

    img = Image.open(out)
    prev = os.path.splitext(out)[0] + ".tg400.png"
    img.resize((400, round(img.height * 400 / img.width)), Image.LANCZOS).save(prev)
    print(f"{out}: {img.width}×{img.height} px (CSS {a.width}×{h}, ×{a.scale:g})")
    print(f"{prev}: превью 400 px, как в ленте Telegram")


if __name__ == "__main__":
    main()
