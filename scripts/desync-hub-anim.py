#!/usr/bin/env python3
"""Анимированные схемы для хаба Zapret2/desync.md и соседних заметок.

Запуск: python3 scripts/desync-hub-anim.py [папка] [схема ...] — по умолчанию все
схемы в Zapret2/desync/attachments/desync-anim-hub-<имя>.svg.

Имя файла начинается с `desync-anim-`, поэтому плагин InlineAnimSvg сайта
встраивает схему в страницу как inline <svg>: она берёт цвета и шрифты темы
Quartz (--dark, --secondary, --codeFont…) и следует переключателю темы. В
<img> (Obsidian, зеркало, Forgejo) срабатывают запасные значения по
prefers-color-scheme. Все селекторы и keyframes — под корневым классом.

Каждая схема стоит рядом с тем объяснением, которое иллюстрирует, и цикл
анимации короткий: читатель видит механизм, не дочитывая абзац.
"""
import html
import math
import sys
from pathlib import Path

W = 960
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "Zapret2/desync/attachments"


def esc(s):
    return html.escape(str(s), quote=True)


class Fig:
    def __init__(self, name, H, T, title, desc):
        self.name, self.H, self.T = name, H, T
        self.id = "dsh-" + name
        self.title, self.desc = title, desc
        self.css, self.body, self.n = [], [], 0

    # ── имена классов ───────────────────────────────────────────────
    def c(self, names):
        return " ".join(f"{self.id}-{n}" for n in names.split())

    # ── анимация ────────────────────────────────────────────────────
    def kf(self, frames, tr=False):
        """frames: [(t, css-декларации)] → строка классов элемента."""
        self.n += 1
        cls = f"{self.id}-e{self.n}"
        name = f"{self.id}-k{self.n}"
        pts = {}
        for t, decl in frames:
            t = max(0.0, min(self.T, t))
            pts[round(t / self.T * 100, 3)] = decl
        pts.setdefault(0, pts[min(pts)])
        pts.setdefault(100, pts[max(pts)])
        body = "".join(f"{p}%{{{pts[p]}}}" for p in sorted(pts))
        self.css.append(f"@keyframes {name}{{{body}}}")
        self.css.append(f".{self.id} .{cls}{{animation-name:{name}}}")
        return f"a {cls}" + (" tr" if tr else "")

    def vis(self, t_in, t_out=None, dx=0, dy=0, fade=0.35):
        """Появление в t_in; если задан t_out — исчезновение (временный
        элемент), иначе держится до конца цикла (итоговое состояние)."""
        hid = f"opacity:0;transform:translate({dx}px,{dy}px)"
        shw = "opacity:1;transform:translate(0px,0px)"
        fr = [(0, hid), (t_in, hid), (t_in + fade, shw)]
        if t_out is not None:
            fr += [(t_out, shw), (t_out + 0.3, hid)]
            return self.kf(fr, tr=True)
        fr += [(self.T - 0.55, shw), (self.T - 0.15, hid)]
        return self.kf(fr)

    def go(self, pts, persist=True):
        """Движение. Элемент нарисован на итоговом месте; pts — смещения
        относительно него: [(t, dx, dy, opacity)]. Последняя точка — (·,0,0,1)
        для элемента, который остаётся; для временного он исчезает сам."""
        fr = [(t, f"opacity:{o};transform:translate({dx}px,{dy}px)") for t, dx, dy, o in pts]
        if persist:
            last = fr[-1][1]
            fr += [(self.T - 0.55, last), (self.T - 0.15, "opacity:0;transform:translate(0px,0px)")]
        return self.kf(fr, tr=not persist)

    def grow(self, t, dur=0.6, tr=False, until=None):
        """Рисование линии слева направо (dashoffset)."""
        hid, shw = "opacity:0;stroke-dashoffset:100", "opacity:1;stroke-dashoffset:0"
        fr = [(0, hid), (t, hid), (t + 0.01, "opacity:1;stroke-dashoffset:100"), (t + dur, shw)]
        if until is not None:
            fr += [(until, shw), (until + 0.3, hid)]
            tr = True
        else:
            fr += [(self.T - 0.55, shw), (self.T - 0.15, hid)]
        return self.kf(fr, tr=tr)

    # ── примитивы ───────────────────────────────────────────────────
    def add(self, s):
        self.body.append(s)

    def g(self, inner, anim=None):
        self.add(f'<g class="{anim}">{inner}</g>' if anim else inner)

    def rect(self, x, y, w, h, cls, rx=7):
        return f'<rect class="{self.c(cls)}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'

    def text(self, x, y, s, cls="t", anchor=None, tl=None):
        extra = f' text-anchor="{anchor}"' if anchor else ""
        if tl:
            extra += f' textLength="{tl}" lengthAdjust="spacingAndGlyphs"'
        return f'<text class="{self.c(cls)}" x="{x}" y="{y}"{extra}>{esc(s)}</text>'

    def line(self, x1, y1, x2, y2, cls):
        return f'<line class="{self.c(cls)}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'

    def head(self, x, y, ang, kind="f", s=5):
        ca, sa = math.cos(ang), math.sin(ang)
        bx, by = x - 10 * ca, y - 10 * sa
        p = [(x, y), (bx - s * sa, by + s * ca), (bx + s * sa, by - s * ca)]
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in p)
        return f'<polygon class="{self.c("hd-" + kind)}" points="{pts}"/>'

    def arrow(self, x1, y1, x2, y2, kind="f", t=None, dur=0.6, until=None, dash=False):
        """Стрелка; при t — рисуется с момента t."""
        ang = math.atan2(y2 - y1, x2 - x1)
        d = f"M{x1} {y1}L{x2} {y2}"
        cls = "ln-" + kind + (" dsh" if dash else "")
        if t is None:
            return (f'<path class="{self.c("sl-" + kind)}" d="{d}"/>' + self.head(x2, y2, ang, kind))
        shaft = f'<path class="{self.c(cls)} {self.grow(t, dur, until=until)}" pathLength="100" d="{d}"/>'
        tip = f'<g class="{self.vis(t + dur * 0.8, until, fade=0.2)}">{self.head(x2, y2, ang, kind)}</g>'
        return shaft + tip

    def chip(self, cx, cy, w, h, label, kind="bx", lcls="mk"):
        return (self.rect(cx - w / 2, cy - h / 2, w, h, "bxbg", rx=6)
                + self.rect(cx - w / 2, cy - h / 2, w, h, kind, rx=6)
                + self.text(cx, cy + 5, label, lcls + " c"))

    # ── стили ───────────────────────────────────────────────────────
    def style(self):
        i = self.id
        R = f".{i}"
        tokens = {
            "fg": ("--dark", "#2b2b2b", "#ebebec"),
            "fg2": ("--darkgray", "#4e4e4e", "#d4d4d4"),
            "mute": ("--gray", "#8a8a8a", "#8c8c8c"),
            "line": ("--lightgray", "#e5e5e5", "#393639"),
            "acc": ("--secondary", "#1f7fb5", "#b2e1ff"),
            "tint": ("--highlight", "rgba(178,225,255,.28)", "rgba(178,225,255,.12)"),
            "bg": ("--light", "#faf8f8", "#161618"),
        }
        light = ";".join(f"--{k}:var({v},{lt})" for k, (v, lt, dk) in tokens.items())
        dark = ";".join(f"--{k}:var({v},{dk})" for k, (v, lt, dk) in tokens.items())
        # «не прошло / отброшено» в теме сайта своего цвета нет
        light += ";--rej:#c4372b;--rejt:rgba(196,55,43,.10)"
        dark += ";--rej:#ff8f80;--rejt:rgba(255,143,128,.13)"
        mono = "var(--codeFont,'JetBrains Mono'),ui-monospace,'Cascadia Code',Consolas,monospace"
        sans = "var(--bodyFont,'Source Sans 3'),system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
        head = "var(--headerFont,Inter),system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
        halo = "paint-order:stroke;stroke:var(--bg);stroke-width:5px;stroke-linejoin:round"
        rules = [
            (R, light),
            (None, f"@media (prefers-color-scheme:dark){{{R}{{{dark}}}}}"),
            (f"{R} .{i}-bg", "fill:var(--bg)"),
            (f"{R} text", f"font-family:{sans};font-size:15px;fill:var(--fg2)"),
            (f"{R} .{i}-t", f"{halo}"),
            (f"{R} .{i}-tk", f"font-weight:600;fill:var(--fg);{halo}"),
            (f"{R} .{i}-m", f"font-family:{mono};font-size:14px;{halo}"),
            (f"{R} .{i}-mk", f"font-family:{mono};font-size:14px;font-weight:600;fill:var(--fg)"),
            (f"{R} .{i}-ml", f"font-family:{mono};font-size:18px;font-weight:600;fill:var(--fg)"),
            (f"{R} .{i}-cap", f"font-family:{head};font-size:11.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;fill:var(--mute)"),
            (f"{R} .{i}-sm", "font-size:13.5px"),
            (f"{R} .{i}-mu", "fill:var(--mute)"),
            (f"{R} .{i}-fg", "fill:var(--fg)"),
            (f"{R} .{i}-acc", "fill:var(--acc)"),
            (f"{R} .{i}-rej", "fill:var(--rej)"),
            (f"{R} .{i}-c", "text-anchor:middle"),
            (f"{R} .{i}-r", "text-anchor:end"),
            (f"{R} .{i}-bx", "fill:var(--bg);stroke:var(--line);stroke-width:1.4"),
            (f"{R} .{i}-bxa", "fill:var(--tint);stroke:var(--acc);stroke-width:1.4"),
            (f"{R} .{i}-bxr", "fill:var(--rejt);stroke:var(--rej);stroke-width:1.4"),
            (f"{R} .{i}-bxd", "fill:none;stroke:var(--mute);stroke-width:1.3;stroke-dasharray:3 3"),
            (f"{R} .{i}-bxn", "fill:none;stroke:none"),
            (f"{R} .{i}-lf", "fill:none;stroke:var(--line);stroke-width:1.2"),
            (f"{R} .{i}-lfd", "fill:none;stroke:var(--line);stroke-width:1.2;stroke-dasharray:4 5"),
            (f"{R} .{i}-lm", "fill:none;stroke:var(--mute);stroke-width:1.4"),
            (f"{R} .{i}-lmd", "fill:none;stroke:var(--mute);stroke-width:1.4;stroke-dasharray:4 5"),
            (f"{R} .{i}-lr", "fill:none;stroke:var(--rej);stroke-width:2"),
            (f"{R} .{i}-la", "fill:none;stroke:var(--acc);stroke-width:2"),
            (f"{R} .{i}-ln-a", "fill:none;stroke:var(--acc);stroke-width:2;stroke-dasharray:100"),
            (f"{R} .{i}-ln-f", "fill:none;stroke:var(--fg2);stroke-width:2;stroke-dasharray:100"),
            (f"{R} .{i}-ln-r", "fill:none;stroke:var(--rej);stroke-width:2;stroke-dasharray:100"),
            (f"{R} .{i}-sl-a", "fill:none;stroke:var(--acc);stroke-width:2"),
            (f"{R} .{i}-sl-f", "fill:none;stroke:var(--fg2);stroke-width:2"),
            (f"{R} .{i}-sl-r", "fill:none;stroke:var(--rej);stroke-width:2"),
            (f"{R} .{i}-bxbg", "fill:var(--bg);stroke:none"),
            (f"{R} .{i}-hd-a", "fill:var(--acc)"),
            (f"{R} .{i}-hd-f", "fill:var(--fg2)"),
            (f"{R} .{i}-hd-r", "fill:var(--rej)"),
            (f"{R} .{i}-dot", "fill:var(--acc)"),
            (f"{R} .{i}-ring", "fill:none;stroke:var(--acc);stroke-width:1.8"),
            (f"{R} .{i}-nd", "fill:var(--bg);stroke:var(--mute);stroke-width:1.5"),
            (f"{R} .{i}-ndr", "fill:var(--rejt);stroke:var(--rej);stroke-width:1.8"),
            (f"{R} .{i}-nda", "fill:var(--tint);stroke:var(--acc);stroke-width:1.8"),
            (f"{R} .a", f"animation-duration:{self.T}s;animation-timing-function:cubic-bezier(.3,.6,.25,1);animation-iteration-count:infinite;animation-fill-mode:both"),
            (None, f"@media (prefers-reduced-motion:reduce){{{R} .a{{animation:none}}{R} .tr{{display:none}}}}"),
            (f"figure.{i}-fig", "margin:1.6rem 0;overflow-x:auto"),
            (f"figure.{i}-fig>svg", "display:block;width:100%;min-width:680px;height:auto"),
        ]
        out = []
        for sel, decl in rules:
            out.append(decl if sel is None and decl.startswith("@") else f"{sel}{{{decl}}}")
        # .dsh-x-dsh — пунктир поверх ln-*: стоит после, чтобы перебить dasharray
        return "".join(out + self.css)

    def render(self):
        i = self.id
        self.css.append(f".{i} .{i}-dsh{{stroke-dasharray:5 5}}")
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" class="{i}" viewBox="0 0 {W} {self.H}" width="{W}" height="{self.H}" role="img" aria-labelledby="{i}-t {i}-d">',
            f'<title id="{i}-t">{esc(self.title)}</title>',
            f'<desc id="{i}-d">{esc(self.desc)}</desc>',
            f"<style>{self.style()}</style>",
            f'<rect class="{i}-bg" x="0" y="0" width="{W}" height="{self.H}"/>',
        ]
        out += self.body
        out.append("</svg>")
        return "\n".join(out) + "\n"


# ═══ 1. Путь пакета через цепочку инстансов ════════════════════════════
def fig_flow():
    f = Fig("flow", 350, 12.5, "Путь одного пакета через цепочку инстансов",
            "Пакет проходит перехват и разбор в ядре, фильтры профиля, первый инстанс fake и второй инстанс multisplit. "
            "Каждая функция отправляет свои пакеты в сеть сразу, а оригиналу возвращает вердикт: fake — PASS, multisplit — DROP. "
            "Итог по цепочке — DROP: оригинал выброшен, в сети уже фейк и три куска.")
    BW, STEP, X0, BY, BH = 150, 200, 6, 172, 72
    st = [("Ядро (C)", "перехват и разбор"), ("Фильтры", "наш ли это пакет?"), ("Инстанс 1", "fake"),
          ("Инстанс 2", "multisplit"), ("Вердикт", "итог по цепочке")]
    cx = [X0 + k * STEP + BW / 2 for k in range(5)]
    cy = BY + BH / 2
    visit = [(0.5, 2.1), (2.4, 3.6), (3.9, 5.1), (5.4, 6.6)]
    for k, (a, b) in enumerate(st):
        x = X0 + k * STEP
        f.add(f.rect(x, BY, BW, BH, "bx"))
        if k < 4:
            f.g(f.rect(x, BY, BW, BH, "bxa"), f.vis(visit[k][0], visit[k][1], fade=0.25))
        else:
            f.g(f.rect(x, BY, BW, BH, "bxr"), f.vis(7.0, fade=0.3))
        f.add(f.text(cx[k], BY + 30, a, "tk c"))
        f.add(f.text(cx[k], BY + 54, b, ("mu sm c" if k in (0, 1, 4) else "m mu c")))
        if k < 4:
            f.add(f.arrow(x + BW + 3, cy, x + STEP - 3, cy, "f"))
    # верхняя полоса «в сеть»
    f.add(f.text(2, 28, "в сеть: уходит сразу, не дожидаясь вердикта", "cap"))
    f.add(f.arrow(480, 78, 948, 78, "f"))
    f.add(f.text(948, 62, "к серверу", "mu sm r"))
    slots = [("фейк", 560, "bxd", 482), ("1", 650, "bxa", 683), ("2", 730, "bxa", 683), ("3", 810, "bxa", 683)]
    times = [4.0, 5.7, 5.95, 6.2]
    for (lab, x, kind, src), t in zip(slots, times):
        w = 64 if lab == "фейк" else 40
        f.g(f.chip(x, 78, w, 30, lab, kind, "mk"),
            f.go([(0, src - x, BY - 78, 0), (t, src - x, BY - 78, 0), (t + 0.2, src - x, BY - 78, 1), (t + 1.0, 0, 0, 1)]))
    # исходный пакет
    pk = f.chip(0, 0, 70, 30, "пакет", "bxa", "mk")
    f.g(pk,
        f.kf([(0, f"opacity:0;transform:translate(30px,{cy}px)"),
              (0.4, f"opacity:1;transform:translate({cx[0]}px,{cy}px)"),
              (1.9, f"opacity:1;transform:translate({cx[0]}px,{cy}px)"),
              (2.5, f"opacity:1;transform:translate({cx[1]}px,{cy}px)"),
              (3.5, f"opacity:1;transform:translate({cx[1]}px,{cy}px)"),
              (4.1, f"opacity:1;transform:translate({cx[2]}px,{cy}px)"),
              (5.0, f"opacity:1;transform:translate({cx[2]}px,{cy}px)"),
              (5.6, f"opacity:1;transform:translate({cx[3]}px,{cy}px)"),
              (6.1, f"opacity:1;transform:translate({cx[3]}px,{cy}px)"),
              (6.6, f"opacity:0;transform:translate({cx[3]}px,{cy}px)")], tr=True))
    # метки под блоками
    f.g(f.text(cx[1], BY + BH + 28, "совпал: передаём в инстансы", "acc sm c"), f.vis(3.0))
    f.g(f.text(cx[2], BY + BH + 28, "возвращает PASS", "mu c"), f.vis(4.8))
    f.g(f.text(cx[3], BY + BH + 28, "возвращает DROP", "rej tk c"), f.vis(6.2))
    f.g(f.text(cx[4] - 6, BY + BH + 28, "DROP сильнее PASS", "rej tk c sm"), f.vis(7.2))
    f.g(f.text(2, 308, "Фейк и три куска уже ушли в сеть: их отправили сами функции, пока работали.", "t"), f.vis(8.2))
    f.g(f.text(2, 334, "Оригинал выброшен: иначе сервер получил бы эти же данные второй раз.", "t"), f.vis(9.6))
    return f


# ═══ 2. Контракт: что в функцию, что из неё ═══════════════════════════
def fig_contract():
    f = Fig("contract", 500, 15, "Связь ядра на C и Lua-функции",
            "Ядро вызывает Lua-функцию, передавая таблицу desync с данными о пакете и потоке. Функция читает данные, "
            "через ctx просит ядро отправить сырые пакеты (они уходят в сеть сразу) и в конце возвращает вердикт для оригинала. "
            "Ядро сводит вердикты всех инстансов и решает судьбу оригинала.")
    cols = {"c": 160, "l": 480, "n": 800}
    heads = [("c", "Ядро nfqws2 (C)", "перехват, разбор, поток", 250), ("l", "Lua-инстанс", "fake(ctx, desync)", 250),
             ("n", "Сеть", "пакеты уходят адресату", 190)]
    for k, a, b, w in heads:
        x = cols[k]
        f.add(f.line(x, 74, x, 462, "lfd"))
        f.add(f.rect(x - w / 2, 14, w, 56, "bx"))
        f.add(f.text(x, 38, a, "tk c"))
        f.add(f.text(x, 58, b, "mu sm c" if k != "l" else "m mu c"))
    # 1. данные вниз в Lua
    f.g(f.text(320, 112, "вызов fake(ctx, desync)", "m fg c"), f.vis(0.8))
    f.add(f.arrow(cols["c"] + 4, 122, cols["l"] - 4, 122, "a", t=1.0))
    f.g(f.text(320, 148, "desync — данные о пакете и потоке", "acc sm c"), f.vis(1.6))
    # 2. работа внутри
    f.g(f.rect(350, 174, 260, 56, "bxa") + f.text(480, 198, "читает desync, делает копии", "tk c sm")
        + f.text(480, 218, "и меняет в них поля", "tk c sm"), f.vis(3.2))
    # 3. команда отправки
    f.g(f.text(320, 270, "ctx: отправь этот пакет (rawsend)", "m fg c"), f.vis(5.0))
    f.add(f.arrow(cols["l"] - 4, 280, cols["c"] + 4, 280, "f", t=5.2))
    f.g(f.text(320, 306, "команда ядру, ответа ждать не нужно", "mu sm c"), f.vis(5.8))
    f.add(f.arrow(cols["c"] + 4, 340, cols["n"] - 4, 340, "f", t=6.6, dur=1.0))
    f.g(f.text(480, 330, "пакет уходит в сеть сразу", "t c"), f.vis(7.0))
    f.g(f.chip(cols["n"], 372, 70, 28, "фейк", "bxd", "mk"),
        f.go([(0, -640, -32, 0), (6.8, -640, -32, 0), (7.0, -640, -32, 1), (7.9, 0, -32, 1), (8.3, 0, 0, 1)]))
    # 4. вердикт
    f.g(f.text(320, 404, "return VERDICT_PASS | MODIFY | DROP", "m fg c"), f.vis(9.6))
    f.add(f.arrow(cols["l"] - 4, 414, cols["c"] + 4, 414, "f", t=9.8))
    f.g(f.text(320, 438, "что сделать с оригиналом", "mu sm c"), f.vis(10.4))
    # 5. итог в ядре
    f.g(f.rect(40, 442, 250, 46, "bxa") + f.text(165, 462, "сводит вердикты всех", "tk c sm")
        + f.text(165, 480, "инстансов и решает судьбу", "tk c sm"), f.vis(11.6))
    # подписи направления
    f.g(f.text(950, 96, "данные — вниз, в Lua", "acc sm r"), f.vis(1.0))
    f.g(f.text(950, 118, "команды и вердикт — вверх, в C", "t sm r"), f.vis(5.0))
    return f


# ═══ 3. Вердикты: кто сильнее ═════════════════════════════════════════
def fig_verdict():
    f = Fig("verdict", 330, 13.8, "Как вердикты инстансов сводятся в один",
            "Три сценария. Все инстансы вернули PASS — оригинал уходит как есть. Один вернул MODIFY — уйдёт изменённый. "
            "Хоть один вернул DROP — оригинал выброшен, что бы ни вернули остальные. Приоритет: DROP сильнее MODIFY, MODIFY сильнее PASS.")
    scen = [
        (["PASS", "PASS", "PASS"], "PASS", "Все пропустили — оригинал уходит как есть."),
        (["PASS", "MODIFY", "PASS"], "MODIFY", "MODIFY сильнее PASS — уйдёт изменённый пакет."),
        (["PASS", "MODIFY", "DROP"], "DROP", "DROP сильнее всех: оригинал выброшен, что бы ни вернули соседи."),
    ]
    kind = {"PASS": "bx", "MODIFY": "bxa", "DROP": "bxr"}
    tcol = {"PASS": "mk", "MODIFY": "mk acc", "DROP": "mk rej"}
    f.add(f.text(2, 28, "вердикты инстансов профиля", "cap"))
    f.add(f.text(640, 28, "приоритет вердиктов", "cap"))
    # лестница
    base = 262
    bars = [("PASS", "пропустить", 640, 50), ("MODIFY", "изменить", 745, 100), ("DROP", "выбросить", 850, 150)]
    for name, gl, x, h in bars:
        f.add(f.rect(x, base - h, 90, h, "bx", rx=6))
        f.add(f.text(x + 45, base + 24, name, "mk c"))
        f.add(f.text(x + 45, base + 44, gl, "mu sm c"))
    f.add(f.text(640, 62, "чем выше, тем сильнее", "mu sm"))
    ys = [104, 154, 204]
    for s, (vs, res, note) in enumerate(scen):
        t0 = 0.3 + s * 4.5
        t1 = t0 + 4.3
        f.g(f.text(2, 62, f"случай {s + 1} из 3", "tk"), f.vis(t0, t1))
        for j, v in enumerate(vs):
            ta = t0 + 0.2 + 0.35 * j
            f.g(f.text(2, ys[j] + 6, f"инстанс {j + 1}", "t") + f.rect(130, ys[j] - 17, 104, 34, kind[v]) +
                f.text(182, ys[j] + 5, v, tcol[v] + " c"), f.vis(ta, t1))
            f.g(f.line(240, ys[j], 300, ys[j], "lm"), f.vis(ta + 0.2, t1))
        f.g(f.line(300, ys[0], 300, ys[2], "lm") + f.arrow(300, ys[1], 346, ys[1], "f"), f.vis(t0 + 1.5, t1))
        f.g(f.text(430, ys[1] - 40, "итог для оригинала", "cap c") +
            f.rect(354, ys[1] - 24, 152, 48, kind[res]) + f.text(430, ys[1] + 7, res, tcol[res] + " c"),
            f.vis(t0 + 1.8, t1))
        bx = {"PASS": 640, "MODIFY": 745, "DROP": 850}[res]
        h = {"PASS": 50, "MODIFY": 100, "DROP": 150}[res]
        f.g(f.rect(bx, base - h, 90, h, {"PASS": "bxa", "MODIFY": "bxa", "DROP": "bxr"}[res], rx=6), f.vis(t0 + 1.8, t1))
        f.g(f.text(2, 300, note, "t"), f.vis(t0 + 2.2, t1))
    return f


# ═══ 4. Карта функций ═════════════════════════════════════════════════
def fig_map():
    cols = ["лишний\nпакет", "режет\nданные", "обратный\nпорядок", "меняет или\nубирает оригинал", "начало\nсоединения"]
    groups = [
        ("Базовые", [("drop", "D"), ("send", "A"), ("pktmod", "D")]),
        ("HTTP", [("http_domcase", "D"), ("http_hostcase", "D"), ("http_methodeol", "D")]),
        ("Нарезка", [("multisplit", "B"), ("multidisorder", "BC"), ("tcpseg", "B")]),
        ("Fake", [("fake", "A"), ("fakedsplit", "AB"), ("fakeddisorder", "ABC"), ("hostfakesplit", "ABc")]),
        ("SYN", [("syndata", "AE"), ("synack", "AE"), ("synack_split", "BE")]),
        ("Окно", [("wsize", "DE"), ("wssize", "D")]),
        ("Прочее", [("rst", "A"), ("udplen", "D"), ("dht_dn", "D")]),
    ]
    RH, GG, Y0 = 27, 10, 78
    H = Y0 + sum(len(r) for _, r in groups) * RH + len(groups) * GG + 52
    f = Fig("map", H, 15, "Карта функций --lua-desync: что каждая делает с трафиком",
            "Матрица функций и действий: какие функции отправляют лишний пакет, режут данные, меняют порядок кусков, "
            "правят или убирают оригинал, работают с началом соединения.")
    cx = [350 + k * 130 for k in range(5)]
    for k, label in enumerate(cols):
        a, *b = label.split("\n")
        f.add(f.text(cx[k], 30, a, "cap c"))
        f.add(f.text(cx[k], 47, b[0], "cap c"))
    y = Y0
    t = 0.4
    for gi, (gname, rows) in enumerate(groups):
        gy = y
        f.add(f.line(2, y - 5, 950, y - 5, "lf"))
        f.g(f.text(2, y + 17, gname, "cap"), f.vis(t, fade=0.3))
        for name, marks in rows:
            inner = f.text(100, y + 18, name, "mk")
            for ch in marks:
                col = "ABCDE".index(ch.upper())
                if ch.isupper():
                    inner += f'<circle class="{f.c("dot")}" cx="{cx[col]}" cy="{y + 13}" r="6.5"/>'
                else:
                    inner += f'<circle class="{f.c("ring")}" cx="{cx[col]}" cy="{y + 13}" r="6"/>'
            f.g(inner, f.vis(t, dy=4, fade=0.3))
            y += RH
            t += 0.28
        y += GG
        t += 0.2
    f.add(f.line(2, y - 5, 950, y - 5, "lf"))
    ly = y + 22
    f.g(f'<circle class="{f.c("dot")}" cx="10" cy="{ly - 5}" r="6.5"/>' + f.text(26, ly, "основное действие функции", "t")
        + f'<circle class="{f.c("ring")}" cx="290" cy="{ly - 5}" r="6"/>' + f.text(306, ly, "только если включить параметром", "t"), f.vis(t))
    return f


# ═══ 5. Синтаксис --lua-desync ════════════════════════════════════════
def fig_syntax():
    f = Fig("syntax", 292, 13, "Как разобрать строку --lua-desync",
            "Строка --lua-desync=fake:blob=fake_default_tls:tcp_md5:ip_ttl=3 состоит из флага, имени функции и параметров через двоеточие. "
            "Параметр со значением пишется как имя=значение, параметр без значения — просто имя, это то же самое, что true.")
    cw = 10.8
    toks = [("--lua-desync=", "вызвать Lua-функцию", "acc", 0), ("fake", "имя функции", "fg", 1), ("blob=fake_default_tls", "параметр со значением", "fg", 2),
            ("tcp_md5", "флаг без значения = true", "fg", 0), ("ip_ttl=3", "параметр со значением", "fg", 1)]
    x = 22.0
    xs = []
    for k, (tk, _, _, _) in enumerate(toks):
        xs.append(x)
        x += len(tk) * cw
        if k > 0 and k < len(toks) - 1:
            pass
        if k >= 1 and k < len(toks) - 1:
            x += cw  # двоеточие
        elif k == 0:
            pass
    y = 64
    # двоеточия между токенами 1..4
    for k in range(1, len(toks) - 1):
        cxp = xs[k] + len(toks[k][0]) * cw
        f.add(f.text(cxp, y, ":", "ml mu", tl=cw))
    rows = [128, 176, 224]
    for k, (tk, label, col, row) in enumerate(toks):
        t = 1.0 + k * 2.1
        w = len(tk) * cw
        mid = xs[k] + w / 2
        f.g(f.text(xs[k], y, tk, "ml" + (" acc" if col == "acc" else ""), tl=w), f.vis(0.1, fade=0.2))
        f.g(f.rect(xs[k] - 2, y + 8, w + 4, 3, "bxa", rx=1.5), f.vis(t, fade=0.25))
        ly = rows[row]
        lx = 60 if k == 0 else mid
        f.g(f.line(lx, y + 14, lx, ly - 18, "lm"), f.vis(t + 0.1, fade=0.25))
        if k == 0:
            f.g(f.text(22, ly, label, "tk acc"), f.vis(t + 0.25, fade=0.3))
        else:
            f.g(f.text(mid, ly, label, "tk c"), f.vis(t + 0.25, fade=0.3))
    f.g(f.text(2, 276, "Инстансов может быть несколько: каждая строка --lua-desync — отдельный вызов, и идут они по порядку.", "mu"), f.vis(11.2))
    return f


# ═══ 6. Порядок инстансов ═════════════════════════════════════════════
def fig_order():
    f = Fig("order", 336, 13.5, "Порядок инстансов — это порядок отправки",
            "Если fake стоит перед multisplit, в сеть уходит сначала фейк, потом три куска настоящего запроса. "
            "Если наоборот, фейк уходит после кусков — настоящие данные к этому моменту уже ушли.")
    rows = [(118, ["фейк", "1", "2", "3"], "fake", "multisplit", 1.0,
             "DPI сначала видит фейк, потом куски настоящего запроса.", "acc"),
            (252, ["1", "2", "3", "фейк"], "multisplit", "fake", 6.6,
             "Фейк опоздал: настоящие куски уже ушли, и DPI их видел.", "rej")]
    f.add(f.text(262, 28, "время отправки", "cap"))
    f.add(f.arrow(262, 38, 948, 38, "f"))
    xs = [330, 470, 610, 750]
    for y, chips, a, b, t0, note, tone in rows:
        f.add(f.text(2, y - 10, "1. " + a, "mk"))
        f.add(f.text(2, y + 14, "2. " + b, "mk"))
        f.add(f.line(262, y + 2, 948, y + 2, "lfd"))
        for k, lab in enumerate(chips):
            fake = lab == "фейк"
            w = 100
            lbl = "фейк" if fake else f"кусок {lab}"
            kind = "bxd" if fake else "bxa"
            t = t0 + k * 0.9
            f.g(f.chip(xs[k], y + 2, w, 38, lbl, kind, "mk"),
                f.go([(0, -230, 0, 0), (t, -230, 0, 0), (t + 0.15, -230, 0, 1), (t + 0.9, 0, 0, 1)]))
        f.g(f.text(2, y + 62, note, "tk" if tone == "acc" else "tk rej"), f.vis(t0 + 4.1))
    return f


# ═══ 7. Обманки: где умирает фейк ═════════════════════════════════════
def fig_fooling():
    f = Fig("fooling", 548, 16, "Три способа сделать пакет, который читает DPI, но не принимает сервер",
            "Фейковый пакет идёт к серверу через DPI. Первый способ: ip_ttl или ip_autottl — TTL заканчивается в пути, до сервера пакет не доходит. "
            "Второй: badsum или tcp_md5 — пакет доходит, но сервер отбрасывает его из-за неверной контрольной суммы или подписи. "
            "Третий: tcp_seq или tcp_ack — сервер отбрасывает пакет, потому что номера не сходятся с состоянием соединения.")
    nodes = [70, 190, 310, 430, 550, 670, 880]       # клиент, 4 роутера (между 2 и 3 — DPI), сервер
    kinds = ["c", "r", "r", "d", "r", "r", "s"]
    lanes = [
        (100, "ip_ttl, ip_autottl", "TTL кончается в пути: до сервера пакет не доходит", 1.0),
        (252, "badsum, tcp_md5", "пакет доходит, сервер отбрасывает: сумма или подпись не сходятся", 5.4),
        (404, "tcp_seq, tcp_ack", "пакет доходит, сервер отбрасывает: номера не из этого соединения", 9.8),
    ]
    for li, (y, name, sub, s) in enumerate(lanes):
        f.add(f.text(2, y - 62, name, "mk"))
        f.add(f.text(2 + len(name) * 8.7 + 14, y - 62, sub, "mu"))
        last = 5 if li == 0 else 6
        f.add(f.line(nodes[0], y, nodes[last], y, "lm"))
        if li == 0:
            f.add(f.line(nodes[last], y, nodes[6], y, "lmd"))
        for k, x in enumerate(nodes):
            if kinds[k] == "d":
                f.add(f'<polygon class="{f.c("nd")}" points="{x - 20},{y} {x - 10},{y - 15} {x + 10},{y - 15} {x + 20},{y} {x + 10},{y + 15} {x - 10},{y + 15}"/>')
                f.add(f.text(x, y + 5, "DPI", "mk c sm"))
            elif kinds[k] == "c":
                f.add(f.rect(x - 24, y - 15, 48, 30, "nd", rx=5))
                f.add(f.text(x, y + 5, "клиент", "mk c sm"))
            elif kinds[k] == "s":
                f.add(f.rect(x - 28, y - 15, 56, 30, "nd", rx=5))
                f.add(f.text(x, y + 5, "сервер", "mk c sm"))
            else:
                f.add(f'<circle class="{f.c("nd")}" cx="{x}" cy="{y}" r="8"/>')
        tt = [s + d for d in (0, 0.9, 1.8, 2.7, 3.6, 4.5, 5.4)]
        end = 5 if li == 0 else 6
        fx = nodes[end]
        pts = [(0, nodes[0] - fx, 0, 0), (tt[0], nodes[0] - fx, 0, 0), (tt[0] + 0.2, nodes[0] - fx, 0, 1)]
        for k in range(1, end + 1):
            pts.append((tt[k] - 0.1 if k < end else tt[k], nodes[k] - fx, 0, 1))
        f.g(f.chip(fx, y - 30, 50, 24, "фейк", "bxd", "mk sm"),
            f.go(pts + [(tt[end] + 0.1, 0, 0, 1)]))
        # DPI разбирает
        f.g(f'<circle class="{f.c("ring")}" cx="{nodes[3]}" cy="{y}" r="28"/>', f.vis(tt[3] - 0.1, tt[3] + 1.4, fade=0.25))
        f.g(f.text(nodes[3], y + 40, "разобрал фейк", "acc sm c"), f.vis(tt[3], tt[3] + 4.2, fade=0.25))
        if li == 0:
            for k, v in zip(range(0, 5), (4, 3, 2, 1, 0)):
                col = "rej tk" if v == 0 else "tk"
                f.g(f.text(nodes[k], y + 36, f"TTL {v}", col + " c sm"), f.vis(tt[k] if k else tt[0] - 0.1, fade=0.2))
            f.g(f.chip(fx, y - 30, 76, 24, "фейк ✕", "bxr", "mk sm rej"), f.vis(tt[5] + 0.1, fade=0.2))
            f.g(f.text(fx, y + 62, "TTL = 0: выброшен в пути", "rej tk c sm"), f.vis(tt[5] + 0.2))
        else:
            f.g(f.chip(fx, y - 30, 76, 24, "фейк ✕", "bxr", "mk sm rej"), f.vis(tt[6] + 0.1, fade=0.2))
            msg = ["сервер отбросил:", "сумма или подпись неверны"] if li == 1 else ["сервер отбросил:", "номера не сходятся"]
            f.g(f.text(950, y + 48, msg[0], "rej tk r sm") + f.text(950, y + 66, msg[1], "rej sm r"), f.vis(tt[6] + 0.2))
    f.g(f.text(2, 540, "Во всех трёх случаях DPI фейк разбирает, а серверу он не достаётся или не принимается.", "t"), f.vis(14.4))
    return f


# ═══ 8. Маркеры позиций ═══════════════════════════════════════════════
def fig_markers():
    f = Fig("markers", 572, 22, "Маркеры позиций pos: где именно резать запрос",
            "Верхняя схема — HTTP-запрос по символам: маркеры method+2, host, sld, midsld, endsld и endhost указывают места разреза. "
            "Из pos=host,midsld,endhost запрос делится на четыре сегмента. Нижняя схема — TLS ClientHello без масштаба: "
            "маркеры extlen, sniext, host, midsld и endhost.")
    req = "GET / HTTP/1.1\r\nHost: www.youtube.com\r\n"
    chars = [("␍" if ch == "\r" else "␊" if ch == "\n" else ch) for ch in req]
    N, CW, X0, TY, TH = len(chars), 22, 51, 76, 30
    # ── HTTP
    f.add(f.text(2, 24, "HTTP-запрос по символам", "cap"))
    f.add(f.rect(X0, TY, N * CW, TH, "bx", rx=5))
    for k, ch in enumerate(chars):
        mu = "mu" if (k < 22 or k >= 37) else ""
        f.add(f.text(X0 + k * CW + CW / 2, TY + 20, ch, f"m c {mu}".strip()))
    f.add(f.rect(X0 + 22 * CW, TY, 15 * CW, TH, "bxa", rx=5))
    f.add(f.rect(X0 + 26 * CW, TY + TH + 3, 7 * CW, 4, "dot", rx=2))
    f.add(f.text(X0 + 29.5 * CW, TY - 8, "www.youtube.com", "mu sm c"))
    pins = [("method+2", 2, 168, "method+2 — метод и ещё 2 байта: GE|T"),
            ("host", 22, 168, "host — начало имени сайта, сразу после «Host: »"),
            ("sld", 26, 192, "sld — начало домена второго уровня (youtube)"),
            ("midsld", 29, 168, "midsld — середина домена второго уровня: you|tube"),
            ("endsld", 33, 192, "endsld — конец домена второго уровня"),
            ("endhost", 37, 168, "endhost — конец имени сайта")]
    for k, (name, pos, ly, cap) in enumerate(pins):
        t = 1.0 + k * 1.7
        x = X0 + pos * CW
        f.g(f.line(x, TY - 6, x, ly - 17, "la") + f.text(x, ly, name, "mk acc c"), f.vis(t, dy=-6))
        f.g(f.text(2, 230, cap, "tk"), f.vis(t + 0.1, t + 1.7, fade=0.25))
    f.g(f.text(2, 230, "pos=host,midsld,endhost — четыре сегмента", "tk"), f.vis(11.2))
    # результат: четыре сегмента с зазорами
    cuts = [0, 22, 29, 37, N]
    gap = 14
    for s in range(4):
        a, b = cuts[s], cuts[s + 1]
        sx = 30 + a * CW + s * gap
        w = (b - a) * CW
        t = 11.4 + s * 0.3
        inner = f.rect(sx, 256, w, TH, "bxa" if s == 1 or s == 2 else "bx", rx=5)
        for k in range(a, b):
            inner += f.text(sx + (k - a) * CW + CW / 2, 276, chars[k], "m c" + (" mu" if (k < 22 or k >= 37) else ""))
        inner += f.text(sx + w / 2, 306, f"сегмент {s + 1}", "mu sm c")
        f.g(inner, f.vis(t, dy=-14, fade=0.4))
    # ── TLS
    f.add(f.line(2, 338, 950, 338, "lf"))
    f.add(f.text(2, 366, "TLS ClientHello — схема без масштаба", "cap"))
    TY2, TH2 = 396, 34
    blocks = [("заголовки", 92, 0), ("версия, random, шифры …", 214, 0), ("длина", 60, 1), ("другие расширения", 150, 0),
              ("заг. SNI", 70, 1), ("www.youtube.com", 212, 2), ("остальное", 80, 0)]
    x = 30
    bpos = {}
    for k, (lab, w, hl) in enumerate(blocks):
        bpos[k] = (x, w)
        kind = "bxa" if hl else "bx"
        f.add(f.rect(x, TY2, w, TH2, kind, rx=5))
        f.add(f.text(x + w / 2, TY2 + 22, lab, ("mk" if hl else "mu") + " sm c" if hl != 2 else "mk sm c"))
        x += w + 4
    hx, hw = bpos[5]
    pins2 = [("extlen", bpos[2][0], 450, "extlen — где записана длина блока расширений"),
             ("sniext", bpos[4][0], 450, "sniext — начало расширения SNI, в нём лежит имя сайта"),
             ("host", hx, 450, "host — начало имени сайта внутри SNI"),
             ("midsld", hx + hw * 0.5, 474, "midsld — середина you|tube, как и в HTTP"),
             ("endhost", hx + hw, 450, "endhost — конец имени сайта")]
    for k, (name, px, ly, cap) in enumerate(pins2):
        t = 13.4 + k * 1.6
        f.g(f.line(px, TY2 - 6, px, ly - 17, "la") + f.text(px, ly, name, "mk acc c"), f.vis(t, dy=-6))
        f.g(f.text(2, 536, cap, "tk"), f.vis(t + 0.1, t + 1.6, fade=0.25))
    f.g(f.text(2, 536, "Маркеры привязаны к устройству запроса: одна и та же запись pos работает для HTTP и TLS.", "t"), f.vis(21.6 - 1.0) if False else f.vis(21.0))
    return f


# ═══ 9. seq и ack ═════════════════════════════════════════════════════
def fig_seqack():
    f = Fig("seqack", 452, 14, "badseq и badack меняют разные поля TCP",
            "Сверху: tcp_seq сдвигает номер последовательности — настоящий пакет попадает в окно приёма сервера и принимается, "
            "фейк со сдвигом на −10000 оказывается далеко за окном и отбрасывается. "
            "Снизу: tcp_ack сдвигает номер подтверждения на −66000 — подтверждение не сходится с тем, что отправлял сервер.")
    # панель 1: seq
    f.add(f.text(2, 26, "badseq: tcp_seq=-10000 сдвигает номер последовательности (seq)", "cap"))
    ly = 132
    f.add(f.line(40, ly, 920, ly, "lm"))
    f.add(f.text(920, ly + 28, "номера байтов потока →", "mu sm r"))
    f.add(f.rect(430, ly - 26, 290, 52, "bxa", rx=6))
    f.add(f.text(575, ly + 82, "окно приёма сервера: сюда пускают", "acc tk c sm"))
    f.g(f.chip(470, ly - 56, 190, 30, "настоящий: seq=1000", "bxa", "mk sm") + f.line(470, ly - 40, 470, ly - 6, "la"), f.go([(0, 0, -30, 0), (1.0, 0, -30, 0), (1.4, 0, -30, 1), (2.2, 0, 0, 1)]))
    f.g(f.text(470, ly + 50, "принят", "acc tk c sm"), f.vis(2.4))
    f.g(f.chip(150, ly - 56, 150, 30, "фейк: seq − 10000", "bxd", "mk sm") + f.line(150, ly - 40, 150, ly - 6, "lr"), f.go([(0, 0, -30, 0), (3.6, 0, -30, 0), (4.0, 0, -30, 1), (4.8, 0, 0, 1)]))
    f.g(f.text(150, ly + 30, "далеко за окном", "rej tk c sm") + f.text(150, ly + 50, "отброшен", "rej tk c sm"), f.vis(5.0))
    # панель 2: ack
    f.add(f.line(2, 236, 950, 236, "lf"))
    f.add(f.text(2, 266, "badack: tcp_ack=-66000 сдвигает номер подтверждения (ack)", "cap"))
    by = 330
    f.add(f.rect(300, by - 18, 400, 36, "bx", rx=6))
    f.add(f.text(500, by + 6, "что сервер отправил клиенту", "mu c"))
    f.g(f.line(700, by - 24, 700, by + 24, "la") + f.text(700, by - 34, "ack: «получил всё до сюда»", "acc tk c sm"), f.vis(6.4))
    f.g(f.text(700, by + 46, "нормальный ack", "acc sm c"), f.vis(6.6))
    f.g(f.line(130, by - 24, 130, by + 24, "lr") + f.text(130, by - 34, "ack − 66000", "rej tk c sm"), f.go([(0, 570, 0, 0), (8.4, 570, 0, 0), (8.6, 570, 0, 1), (10.0, 0, 0, 1)]))
    f.g(f.text(130, by + 46, "подтверждает то,", "rej sm c") + f.text(130, by + 63, "чего сервер не слал", "rej sm c"), f.vis(10.2))
    f.g(f.text(2, 438, "Это разные поля: badseq — seq, badack — ack. Для ack на Linux нужен ещё tcp_ts_up — схема в разделе ниже.", "t"), f.vis(11.6))
    return f


# ═══ 10. tcp_ts_up ════════════════════════════════════════════════════
def fig_tsup():
    f = Fig("tsup", 388, 14, "Зачем tcp_ts_up: Linux смотрит на первую опцию",
            "Linux отбрасывает пакет с плохим ack, только если опция timestamp стоит первой в списке TCP-опций. "
            "Без tcp_ts_up timestamp не первая, и пакет принимается. С tcp_ts_up она переносится на первое место, и пакет отбрасывается.")
    xs = [330, 470, 610, 750]
    labs = ["опция 1", "опция 2", "timestamp", "опция 4"]
    # без
    f.add(f.text(2, 28, "без tcp_ts_up", "cap"))
    f.add(f.text(2, 112, "TCP-опции", "t"))
    f.add(f.text(2, 132, "пакета с плохим ack", "t"))
    for k, x in enumerate(xs):
        ts = labs[k] == "timestamp"
        f.add(f.chip(x, 120, 120, 38, labs[k], "bxa" if ts else "bx", "mk sm" + (" acc" if ts else "")))
    f.g(f.text(xs[0], 70, "Linux смотрит сюда", "tk c sm") + f.arrow(xs[0], 76, xs[0], 98, "f"), f.vis(1.0))
    f.g(f.text(2, 190, "timestamp не первая → плохой ack не проверяется → пакет принят: обман не сработал", "rej tk"), f.vis(2.4))
    f.add(f.line(2, 214, 950, 214, "lf"))
    # с
    f.add(f.text(2, 244, "с tcp_ts_up", "cap"))
    f.add(f.text(2, 316, "TCP-опции", "t"))
    new_order = ["timestamp", "опция 1", "опция 2", "опция 4"]
    for lab in labs:
        ts = lab == "timestamp"
        old = xs[labs.index(lab)]
        new = xs[new_order.index(lab)]
        f.g(f.chip(new, 322, 120, 38, lab, "bxa" if ts else "bx", "mk sm" + (" acc" if ts else "")),
            f.go([(0, old - new, 0, 0), (5.0, old - new, 0, 0), (5.3, old - new, 0, 1), (7.0, old - new, 0, 1), (8.0, 0, 0, 1)]))
    f.g(f.text(xs[0], 272, "Linux смотрит сюда", "tk c sm") + f.arrow(xs[0], 278, xs[0], 300, "f"), f.vis(8.4))
    f.g(f.text(2, 376, "timestamp первая → ack проверяется → он плохой → пакет отброшен: обман сработал", "acc tk"), f.vis(9.4))
    return f


# ═══ 11. autottl ══════════════════════════════════════════════════════
def fig_autottl():
    f = Fig("autottl", 520, 18, "Как ip_autottl считает TTL фейка",
            "Из TTL ответа сервера (52) угадывается стартовое значение 64, число хопов до сервера равно 64 − 52 = 12. "
            "К нему прибавляется delta (−1), получается 11, результат зажимается в диапазон min–max. "
            "Фейк с TTL 11 умирает на 11-м хопе — на один раньше сервера, но после DPI.")
    S = 3.4
    ox = 36
    px = lambda v: ox + v * S
    f.add(f.text(2, 26, "1. TTL ответа сервера (SYN-ACK) → стартовое значение", "cap"))
    ay = 96
    f.add(f.line(px(0), ay, px(255), ay, "lm"))
    for lo, hi, st in ((32, 64, 64), (96, 128, 128), (223, 255, 255)):
        f.add(f.rect(px(lo), ay - 14, (hi - lo) * S, 28, "bxa", rx=4))
        f.add(f.text(px(hi), ay + 38, f"старт {st}", "mu sm c"))
    for v in (0, 64, 128, 255):
        f.add(f.line(px(v), ay - 8, px(v), ay + 8, "lm"))
        f.add(f.text(px(v), ay - 22, str(v), "mk c sm mu" if v else "mk c sm mu"))
    f.g(f.chip(px(52), ay, 56, 28, "52", "bx", "mk") + f.text(px(52), ay - 44, "пришёл с TTL 52", "tk c sm"),
        f.go([(0, 0, -40, 0), (1.0, 0, -40, 0), (1.4, 0, -40, 1), (2.2, 0, 0, 1)]))
    f.g(f.arrow(px(52) + 20, ay + 54, px(64), ay + 54, "a", t=3.2, dur=0.5) + f.text(px(64) + 6, ay + 78, "угадали: сервер стартовал с 64", "acc tk sm"), None)
    f.add(f.text(2, 196, "2. Считаем", "cap"))
    f.g(f.text(2, 226, "хопов до сервера = 64 − 52 = 12", "ml"), f.vis(4.4))
    f.g(f.text(2, 258, "TTL фейка = 12 + (−1) = 11", "ml") + f.text(420, 258, "← delta из ip_autottl=-1,3-20", "mu sm"), f.vis(6.0))
    f.g(f.text(2, 290, "рамки 3–20: 11 помещается → TTL = 11", "ml acc"), f.vis(7.6))
    f.add(f.line(2, 316, 950, 316, "lf"))
    f.add(f.text(2, 344, "3. Что это значит в пути", "cap"))
    by = 408
    n = 13
    sx0, sx1 = 60, 900
    xs = [sx0 + k * (sx1 - sx0) / 12 for k in range(n)]
    f.add(f.line(xs[0], by, xs[12], by, "lm"))
    for k, x in enumerate(xs):
        if k == 0:
            f.add(f.rect(x - 24, by - 15, 48, 30, "nd", rx=5) + f.text(x, by + 5, "клиент", "mk c sm"))
        elif k == 12:
            f.add(f.rect(x - 28, by - 15, 56, 30, "nd", rx=5) + f.text(x, by + 5, "сервер", "mk c sm"))
        elif k == 5:
            x2 = (xs[5] + xs[6]) / 2
            f.add(f'<circle class="{f.c("nd")}" cx="{x}" cy="{by}" r="7"/>')
            f.add(f'<polygon class="{f.c("nd")}" points="{x2 - 20},{by + 46} {x2 - 10},{by + 31} {x2 + 10},{by + 31} {x2 + 20},{by + 46} {x2 + 10},{by + 61} {x2 - 10},{by + 61}"/>')
            f.add(f.text(x2, by + 51, "DPI", "mk c sm"))
        else:
            f.add(f'<circle class="{f.c("nd")}" cx="{x}" cy="{by}" r="7"/>')
        if 0 < k < 12:
            f.add(f.text(x, by + 28, str(k), "mu sm c"))
    f.add(f.text(xs[12], by + 38, "12 хопов", "mu sm c"))
    f.g(f.chip(xs[11], by - 36, 64, 26, "TTL 11", "bxd", "mk sm"),
        f.go([(0, xs[0] - xs[11], 0, 0), (9.0, xs[0] - xs[11], 0, 0), (9.3, xs[0] - xs[11], 0, 1), (13.0, 0, 0, 1)]))
    f.g(f.chip(xs[11], by - 36, 90, 26, "TTL 0 ✕", "bxr", "mk sm rej"), f.vis(13.2, fade=0.2))
    f.g(f.text(xs[11], by - 66, "умер за хоп до сервера", "rej tk c sm"), f.vis(13.4))
    f.g(f.text(x2c(xs), by + 80, "DPI на пути успел его прочитать", "acc tk c sm"), f.vis(11.0))
    return f


# ═══ 12. Жизненный цикл: восемь стадий ════════════════════════════════
def fig_lifecycle():
    stages = [
        ("Транспорт", "пакет TCP? (у multisplit — только TCP)", "иначе: отключиться от потока"),
        ("Направление", "исходящий? противоположное не нужно", "иначе: отключиться от направления"),
        ("Аргументы", "обязательные аргументы на месте?", "иначе: выйти с ошибкой"),
        ("Данные", "что резать: blob → reasm_data → payload", "берётся первое, что есть"),
        ("Три гварда", "данные есть, направление и payload подходят?", "иначе: ничего не делать"),
        ("Replay", "это первый кусок запроса?", "не первый: дроп, данные уже ушли"),
        ("Техника", "маркеры, части, фейки, отправка в сеть", "у каждой функции своя"),
        ("Вердикт", "что сделать с оригиналом", "PASS · MODIFY · DROP"),
    ]
    RH, Y0 = 50, 64
    H = Y0 + 8 * RH + 30
    f = Fig("lifecycle", H, 13, "Восемь стадий desync-функции",
            "Любая desync-функция по очереди проходит восемь стадий: проверка транспорта, направления, аргументов, выбор данных, три гварда, "
            "развилка replay, собственно техника и вердикт. Отказ почти всегда происходит на одной из ранних стадий.")
    f.add(f.text(70, 30, "стадия и что она проверяет", "cap"))
    f.add(f.text(600, 30, "если не так", "cap"))
    for k, (name, what, no) in enumerate(stages):
        y = Y0 + k * RH
        t = 0.6 + k * 1.0
        last = k == 6
        f.add(f.line(2, y, 950, y, "lf"))
        f.g(f.rect(2, y + 2, 946, RH - 4, "bxa", rx=8), f.vis(t, t + 1.0, fade=0.25))
        f.add(f'<circle class="{f.c("nd")}" cx="30" cy="{y + RH / 2}" r="15"/>')
        f.g(f'<circle class="{f.c("nda")}" cx="30" cy="{y + RH / 2}" r="15"/>', f.vis(t, fade=0.25))
        f.add(f.text(30, y + RH / 2 + 5, str(k + 1), "mk c"))
        f.add(f.text(62, y + RH / 2 + 5, name, "tk" + (" acc" if last else "")))
        f.add(f.text(200, y + RH / 2 + 5, what, "t"))
        f.add(f.text(600, y + RH / 2 + 5, no, "mu sm"))
        if k in (0, 1, 2, 4, 5):
            f.g(f.text(578, y + RH / 2 + 5, "✕", "rej tk c"), f.vis(t + 0.1, t + 1.0, fade=0.2))
    f.add(f.line(2, Y0 + 8 * RH, 950, Y0 + 8 * RH, "lf"))
    f.g(f.text(2, Y0 + 8 * RH + 24, "Если техника «не работает», обычно пакет не дошёл до стадии 7: смотри, где функция остановилась.", "tk"), f.vis(9.4))
    return f


# ═══ 13. seqovl ═══════════════════════════════════════════════════════
def fig_seqovl():
    f = Fig("seqovl", 452, 15, "seqovl: лишние байты слева от окна приёма",
            "Без seqovl сегмент начинается с seq=1000 — именно с него сервер ждёт данные. С seqovl=10 слева дописано 10 байт паттерна, а seq сдвинут на 990. "
            "DPI читает сегмент целиком, вместе с паттерном; сервер выбрасывает байты левее 1000 как устаревшие и принимает реальную часть.")
    X_P, X_R, X_E = 250, 410, 800
    f.add(f.line(X_R, 40, X_R, 262, "lfd"))
    f.add(f.text(X_R, 30, "сервер ждёт seq=1000", "acc tk c sm"))
    # без seqovl
    ya, yb = 84, 190
    f.add(f.text(2, ya + 5, "без seqovl", "tk"))
    f.add(f.rect(X_R, ya - 20, X_E - X_R, 40, "bxa"))
    f.add(f.text((X_R + X_E) / 2, ya + 5, "реальная первая часть, seq=1000", "mk c sm"))
    f.g(f.text(X_E + 10, ya + 5, "принят", "acc tk sm"), f.vis(1.4))
    # с seqovl
    f.add(f.text(2, yb + 5, "seqovl=10", "tk"))
    f.add(f.rect(X_R, yb - 20, X_E - X_R, 40, "bxa"))
    f.add(f.text((X_R + X_E) / 2, yb + 5, "реальная первая часть", "mk c sm"))
    f.g(f.rect(X_P, yb - 20, X_R - X_P, 40, "bxd") + f.text((X_P + X_R) / 2, yb + 5, "паттерн, 10 байт", "mu c sm") +
        f.text(X_P, yb - 30, "seq=990", "mk sm"),
        f.go([(0, 60, 0, 0), (3.0, 60, 0, 0), (3.2, 60, 0, 0), (4.2, 0, 0, 1)]))
    f.g(f.text(X_E + 10, yb - 3, "один обычный", "mu sm") + f.text(X_E + 10, yb + 15, "TCP-сегмент", "mu sm"), f.vis(4.4))
    # кто что видит
    f.g(f.line(X_P, 266, X_E, 266, "la") + f.line(X_P, 260, X_P, 272, "la") + f.line(X_E, 260, X_E, 272, "la") +
        f.text((X_P + X_E) / 2, 292, "DPI читает сегмент целиком, от начала — и паттерн тоже", "acc tk c sm"), f.vis(6.0))
    f.g(f.line(X_P, 320, X_R, 320, "lr") + f.text((X_P + X_R) / 2, 344, "левее 1000: выброшено", "rej tk c sm"), f.vis(8.0))
    f.g(f.line(X_R, 320, X_E, 320, "la") + f.text((X_R + X_E) / 2, 344, "принято: сервер собрал нужные байты", "acc tk c sm"), f.vis(9.2))
    f.add(f.text(2, 320, "сервер", "tk"))
    f.add(f.text(2, 292, "DPI", "tk"))
    f.g(f.text(2, 410, "Заголовки не искажены, пакет выглядит честным — этим seqovl отличается от fooling.", "t"), f.vis(10.6))
    return f


# ═══ 14. Нарезка на сегменты ══════════════════════════════════════════
def fig_segments():
    f = Fig("segments", 372, 14, "multisplit: pos=100,300,450 делит 600 байт на четыре сегмента",
            "Данные длиной 600 байт режутся в позициях 100, 300 и 450 на четыре куска: 0–99, 100–299, 300–449, 450–599. "
            "Сегменты уходят по порядку, seq каждого равен смещению его первого байта.")
    X0, S = 150, 1.3
    px = lambda b: X0 + b * S
    f.add(f.text(2, 28, "данные запроса, 600 байт", "cap"))
    f.add(f.rect(px(0), 44, 600 * S, 34, "bx", rx=5))
    for b in (0, 100, 300, 450, 600):
        f.add(f.text(px(b), 100, str(b), "mu sm c"))
    cuts = [100, 300, 450]
    for k, b in enumerate(cuts):
        f.g(f.line(px(b), 36, px(b), 86, "la"), f.vis(0.8 + k * 0.5, fade=0.25))
    f.g(f.text(px(300), 128, "разрезы pos=100,300,450", "acc tk c sm"), f.vis(2.0))
    bounds = [0, 100, 300, 450, 600]
    f.add(f.text(2, 160, "порядок отправки", "cap"))
    for k in range(4):
        a, b = bounds[k], bounds[k + 1]
        y = 176 + k * 40
        t = 3.0 + k * 1.1
        f.g(f.rect(px(a) + 1, y, (b - a) * S - 2, 30, "bxa", rx=5) +
            f.text(px(a) + (b - a) * S / 2, y + 20, f"{b - a} байт", "mk c sm") +
            f.text(2, y + 20, f"сегмент {k + 1}", "tk sm") +
            f.text(86, y + 20, f"seq={a}", "m mu sm"),
            f.go([(0, 0, -150 + 0, 0), (t, 0, -34, 0), (t + 0.2, 0, -34, 1), (t + 0.9, 0, 0, 1)]))
    f.g(f.text(2, 356, "Сервер складывает сегменты по seq и получает исходные 600 байт без пропусков.", "tk"), f.vis(8.2))
    return f


# ═══ 15. MSS ══════════════════════════════════════════════════════════
def fig_mss():
    f = Fig("mss", 320, 13, "Автосегментация по MSS: кусок больше MSS режется сам",
            "Если кусок данных вместе с заголовками не помещается в MSS соединения, хелпер rawsend_payload_segmented дорезает его на под-сегменты "
            "и увеличивает seq на длину предыдущего. Fooling достаётся всем под-сегментам одинаково, ip_id считается для каждого отдельно.")
    X0, W_ = 40, 880
    f.add(f.text(2, 28, "кусок данных от функции", "cap"))
    f.add(f.rect(X0, 44, W_, 34, "bx", rx=5))
    f.add(f.text(X0 + W_ / 2, 66, "больше, чем влезает в один сегмент", "mu c sm"))
    mss = 300
    parts = [(X0, mss, "seq = s"), (X0 + mss, mss, "seq = s + MSS"), (X0 + 2 * mss, W_ - 2 * mss, "seq = s + 2·MSS")]
    for k in (1, 2):
        f.g(f.line(X0 + k * mss, 36, X0 + k * mss, 86, "la") + f.text(X0 + k * mss, 106, "MSS", "acc tk c sm"), f.vis(1.0 + k * 0.4, fade=0.25))
    f.add(f.text(2, 146, "что уходит в сеть", "cap"))
    for k, (x, w, lab) in enumerate(parts):
        y = 162
        t = 3.0 + k * 1.0
        f.g(f.rect(x + 1, y, w - 2, 34, "bxa", rx=5) + f.text(x + w / 2, y + 22, lab, "mk c sm") +
            f.text(x + w / 2, y + 58, "то же fooling", "mu sm c") + f.text(x + w / 2, y + 78, "свой ip_id", "mu sm c"),
            f.go([(0, 0, -40, 0), (t, 0, -40, 0), (t + 0.2, 0, -40, 1), (t + 0.8, 0, 0, 1)]))
    f.g(f.text(2, 300, "Думать о размере сегментов не нужно: MSS берётся из desync.tcp_mss.", "tk"), f.vis(7.0))
    return f


# ═══ 16. reasm и replay ═══════════════════════════════════════════════
def fig_reasm():
    f = Fig("reasm", 392, 15, "reasm: большой ClientHello приходит несколькими пакетами",
            "ClientHello не помещается в один TCP-сегмент и приходит тремя пакетами. nfqws2 придерживает их и собирает в reasm_data, затем перепроигрывает: "
            "на первой части функция режет и отправляет весь собранный буфер, а вторую и третью части выбрасывает — их содержимое уже ушло.")
    f.add(f.text(2, 28, "пришло из приложения", "cap"))
    xs = [60, 160, 260]
    for k in range(3):
        f.g(f.chip(xs[k] + 40, 62, 84, 32, f"часть {k + 1}", "bxa", "mk sm"),
            f.go([(0, -100, 0, 0), (0.5 + k * 0.8, -100, 0, 0), (0.6 + k * 0.8, -100, 0, 1), (1.4 + k * 0.8, 0, 0, 1)]))
    f.g(f.text(2, 112, "ядро придерживает пакеты и собирает запрос", "tk sm"), f.vis(3.2))
    f.g(f.rect(60, 128, 360, 40, "bxa") + f.text(240, 153, "reasm_data: запрос целиком", "mk c sm"), f.vis(3.6))
    f.add(f.text(2, 212, "перепроигрывание (replay)", "cap"))
    f.g(f.chip(100, 252, 100, 32, "часть 1", "bxa", "mk sm") + f.arrow(150, 252, 240, 252, "a") +
        f.rect(240, 226, 190, 52, "bxa") + f.text(335, 247, "функция режет весь", "mk c sm") + f.text(335, 267, "reasm_data", "mk c sm"), f.vis(5.4))
    for k in range(3):
        f.g(f.chip(500 + k * 100, 252, 80, 32, f"кусок {k + 1}", "bxa", "mk sm"),
            f.go([(0, -270 + k * 40, 0, 0), (7.0 + k * 0.5, -270 + k * 40, 0, 0), (7.1 + k * 0.5, -270 + k * 40, 0, 1), (7.9 + k * 0.5, 0, 0, 1)]))
    f.g(f.text(500, 306, "уходят в сеть сразу", "acc tk sm"), f.vis(8.8))
    f.g(f.chip(100, 340, 100, 32, "часть 2, 3", "bxr", "mk sm rej") + f.text(160, 345, "→ DROP: содержимое уже отправлено", "rej tk sm"), f.vis(10.2))
    return f


# ═══ 17. tls_mod ══════════════════════════════════════════════════════
def fig_tlsmod():
    f = Fig("tlsmod", 360, 20, "tls_mod: что меняется в фейковом ClientHello",
            "Опции tls_mod правят поля фейкового ClientHello перед отправкой: rnd делает случайными Random и Session ID, rndsni и sni= заменяют имя сайта, "
            "dupsid копирует Session ID из настоящего запроса, padencap раздувает padding extension под настоящий запрос.")
    blocks = [("заголовки", 100, "hdr"), ("Random 32 Б", 120, "rnd"), ("Session ID", 110, "sid"),
              ("другие расширения", 190, "ext"), ("SNI: имя сайта", 170, "sni"), ("padding", 100, "pad")]
    X0, Y, H_ = 30, 120, 44
    pos = {}
    x = X0
    for lab, w, key in blocks:
        pos[key] = (x, w)
        f.add(f.rect(x, Y, w, H_, "bx", rx=6) + f.text(x + w / 2, Y + 27, lab, "mk c sm" if key in ("rnd", "sid", "sni", "pad") else "mu c sm"))
        x += w + 4
    f.add(f.text(2, 28, "фейковый ClientHello", "cap"))
    scen = [
        (["rnd", "sid"], "rnd", "Random и Session ID заполнены случайными байтами"),
        (["sni"], "rndsni", "имя сайта в SNI заменено случайным доменом"),
        (["sni"], "sni=<домен>", "в SNI стоит ваш домен; длины внутри TLS пересчитаны"),
        (["sid"], "dupsid", "Session ID скопирован из настоящего запроса (после rnd)"),
        (["pad"], "padencap", "padding увеличен на длину настоящего запроса: он может выглядеть его частью"),
    ]
    for si, (keys, name, cap) in enumerate(scen):
        t0 = 0.4 + si * 3.8
        t1 = t0 + 3.6
        f.g(f.text(2, 70, f"tls_mod={name}", "ml acc"), f.vis(t0, t1))
        for key in keys:
            bx, bw = pos[key]
            f.g(f.rect(bx - 3, Y - 3, bw + 6, H_ + 6, "bxa", rx=8), f.vis(t0 + 0.3, t1, fade=0.3))
        f.g(f.text(2, 244, cap, "tk"), f.vis(t0 + 0.5, t1))
        if name == "dupsid":
            bx, bw = pos["sid"]
            f.g(f.rect(bx, 276, bw, 40, "bxa", rx=6) + f.text(bx + bw / 2, 301, "Session ID", "mk c sm") +
                f.text(X0, 292, "настоящий запрос", "mu sm") + f.arrow(bx + bw / 2, 272, bx + bw / 2, Y + H_ + 8, "a"), f.vis(t0 + 0.9, t1))
        if name == "padencap":
            bx, bw = pos["pad"]
            f.g(f.rect(bx + 6, 276, 190, 40, "bxa", rx=6) + f.text(bx + 101, 301, "настоящий запрос", "mk c sm") +
                f.arrow(bx + bw / 2, 272, bx + bw / 2, Y + H_ + 8, "a"), f.vis(t0 + 0.9, t1))
    f.g(f.text(2, 350, "Нет образца настоящего запроса (reasm_data) — tls_mod молча пропускается, и фейк уходит как есть.", "mu"), f.vis(0.2))
    return f


# ═══ 18. fakedsplit: шесть пакетов ════════════════════════════════════
def fig_fakedsplit6():
    f = Fig("fakedsplit6", 450, 16, "fakedsplit: каждая настоящая часть зажата между фейками",
            "fakedsplit отправляет до шести пакетов: фейк первой части, настоящая первая часть, повтор фейка, фейк второй части, настоящая вторая часть, повтор фейка. "
            "У трёх пакетов каждой тройки один и тот же seq, DPI не может понять, какой настоящий; сервер отбрасывает фейки и принимает настоящие части.")
    X1, X2, X3 = 250, 520, 770
    f.add(f.text(2, 28, "порядок отправки", "cap"))
    f.add(f.text(X1, 28, "1-я часть", "cap"))
    f.add(f.text(X2, 28, "2-я часть", "cap"))
    f.add(f.text(950, 28, "сервер", "cap r"))
    rows = [("фейк 1", "nofake1", 0, True), ("настоящая 1", "", 0, False), ("фейк 1, повтор", "nofake2", 0, True),
            ("фейк 2", "nofake3", 1, True), ("настоящая 2", "", 1, False), ("фейк 2, повтор", "nofake4", 1, True)]
    RH, Y0 = 46, 46
    for k, (lab, flag, part, fake) in enumerate(rows):
        y = Y0 + k * RH
        t = 0.6 + k * 1.0
        x = X1 if part == 0 else X2
        w = 250
        inner = f.text(2, y + 25, f"#{k + 1}", "mu") + f.text(34, y + 25, lab, "tk sm")
        if flag:
            inner += f.text(34, y + 41, flag, "m mu sm")
        inner += f.rect(x, y + 4, w, 32, "bxd" if fake else "bxa", rx=5)
        inner += f.text(x + w / 2, y + 25, "мусор X…X" if fake else "реальные данные", ("mu" if fake else "mk") + " c sm")
        inner += f.text(950, y + 25, "отброшен: fooling" if fake else "принят", ("mu" if fake else "acc tk") + " r sm")
        f.g(inner, f.vis(t, dx=-16))
    for part, (ra, rb, label) in enumerate([(0, 2, "тройка с одним seq"), (3, 5, "тройка с одним seq")]):
        y0 = Y0 + ra * RH + 2
        y1 = Y0 + rb * RH + RH - 2
        f.g(f.line(812, y0 + 4, 812, y1 - 4, "la") + f.line(806, y0 + 4, 812, y0 + 4, "la") + f.line(806, y1 - 4, 812, y1 - 4, "la"), f.vis(7.0 + part * 0.8))
    f.g(f.text(2, Y0 + 6 * RH + 28, "DPI видит две тройки «повторов» и не может понять, какой пакет в каждой настоящий.", "tk"), f.vis(8.6))
    f.g(f.text(2, Y0 + 6 * RH + 56, "Сервер выбрасывает фейки и склеивает настоящие части: получается исходный запрос.", "t"), f.vis(10.0))
    return f


def x2c(xs):
    return (xs[5] + xs[6]) / 2


FIGS = {"flow": fig_flow, "contract": fig_contract, "verdict": fig_verdict, "map": fig_map, "syntax": fig_syntax,
        "order": fig_order, "fooling": fig_fooling, "markers": fig_markers, "seqack": fig_seqack, "tsup": fig_tsup,
        "autottl": fig_autottl, "lifecycle": fig_lifecycle, "seqovl": fig_seqovl, "segments": fig_segments,
        "mss": fig_mss, "reasm": fig_reasm, "tlsmod": fig_tlsmod, "fakedsplit6": fig_fakedsplit6}


def main(argv):
    out = DEFAULT_OUT
    names = []
    for a in argv:
        if a in FIGS:
            names.append(a)
        else:
            out = Path(a)
    out.mkdir(parents=True, exist_ok=True)
    for name in names or list(FIGS):
        svg = FIGS[name]().render()
        (out / f"desync-anim-hub-{name}.svg").write_text(svg, encoding="utf-8")
        print(f"desync-anim-hub-{name}.svg  {len(svg) // 1024} КБ")


if __name__ == "__main__":
    main(sys.argv[1:])
