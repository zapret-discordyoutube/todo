#!/usr/bin/env python3
"""Анимированные схемы техник дурения DPI: карта потока «время × seq».

Запуск: python3 scripts/desync-anim.py [папка] [техника ...] — по умолчанию все
техники в Zapret2/desync/attachments/desync-anim-*.svg.

Строка — пакет в порядке отправки, подписанный как в статьях
(`#1 FAKE1 seq=0 len=14`). По горизонтали — место пакета в TCP-потоке,
в ячейках — его байты (фейковые, как в статьях, — X). Под картой —
буфер сервера в тех же колонках: принятые куски встают на свои места.

Цвета и шрифты — переменные темы Quartz (--dark, --secondary, --codeFont…):
на wiki.zapret.moe SVG встраивается в страницу и следует теме сайта, а в
<img> (Obsidian, зеркало, Forgejo) срабатывают запасные значения по
prefers-color-scheme. Все селекторы и keyframes — под корневым классом.
"""
import html
import sys
from pathlib import Path

W = 960
CW = 22            # ширина ячейки по умолчанию (spec["cw"] переопределяет)
CH = 26            # высота ячейки
ROW = 36           # шаг строк
LBL_X = 0          # колонка подписи пакета
SRV_X = 826        # колонка сервера (x левого края)
MAP_X = 240        # левый край карты потока
STEP = 1.05        # секунд между пакетами


def esc(s):
    return html.escape(str(s), quote=True)


class Diagram:
    def __init__(self, spec):
        self.s = spec
        self.id = "dsa-" + spec["name"].replace("_", "-")
        self.css = []
        self.body = []
        self.n = 0

    # ── анимация ────────────────────────────────────────────────────
    def anim(self, frames):
        """frames: [(t, css-декларации)] → имя класса элемента."""
        self.n += 1
        cls = f"{self.id}-e{self.n}"
        name = f"{self.id}-k{self.n}"
        pts = {}
        for t, decl in frames:
            t = max(0.0, min(self.T, t))
            pts[round(t / self.T * 100, 3)] = decl
        if 0 not in pts:
            pts[0] = pts[min(pts)]
        if 100 not in pts:
            pts[100] = pts[max(pts)]
        body = "".join(f"{p}%{{{pts[p]}}}" for p in sorted(pts))
        self.css.append(f"@keyframes {name}{{{body}}}")
        self.css.append(f".{self.id} .{cls}{{animation-name:{name}}}")
        return f"a {cls}"

    def appear(self, t, extra_end=None, dx=0):
        """Появление в t (с лёгким сдвигом по x), держится до конца цикла."""
        hid = "opacity:0" + (f";transform:translateX({dx}px)" if dx else "")
        shown = "opacity:1" + (";transform:translateX(0px)" if dx else "")
        fr = [(0, hid), (t, hid), (t + 0.35, shown)]
        if extra_end:
            fr += extra_end
        fr += [(self.T - 0.55, fr[-1][1]), (self.T - 0.15, hid)]
        return self.anim(fr)

    # ── геометрия ───────────────────────────────────────────────────
    def cx(self, pos):
        return self.MX + pos * self.cw

    def build(self):
        s = self.s
        rows = s["rows"]
        tape = s["tape"]
        self.N = len(tape)
        self.cw = s.get("cw", CW)
        self.neg = s.get("neg", 0)                   # ячеек левее seq=0 (seqovl)
        self.MX = MAP_X + self.neg * self.cw         # x колонки seq=0
        self.BN = s.get("buf_len", self.N)           # длина буфера сервера
        span = (self.N + self.neg) * self.cw
        assert MAP_X + span <= SRV_X - 12, (s["name"], MAP_X + span)
        for i, r in enumerate(rows):
            r["t"] = 0.5 + i * STEP
        last = rows[-1]["t"]
        self.t_done = last + 0.9
        self.T = round(last + s.get("hold", 4.8), 2)

        y = 0
        y = self.header(y)
        y0 = y
        for i, r in enumerate(rows):
            self.row(r, y0 + i * ROW)
        y = y0 + len(rows) * ROW
        # разрезы — пунктир через все строки
        for pos, lab in s.get("cuts", []):
            x = self.cx(pos)
            self.add(f'<line class="{self.id}-cut" x1="{x}" y1="{y0 - 30}" x2="{x}" y2="{y + 8}"/>')
        if self.neg:
            x = self.cx(0)
            self.add(f'<line class="{self.id}-win" x1="{x}" y1="{y0 - 30}" x2="{x}" y2="{y + 52}"/>')
        y = self.buffer(y + 16)
        y = self.notes(y + 6)
        self.H = y + 6
        return self.render()

    def add(self, s):
        self.body.append(s)

    def header(self, y):
        s, i = self.s, self.id
        a = self.add
        a(f'<text class="{i}-cap" x="{LBL_X}" y="{y + 14}">пакет в порядке отправки</text>')
        a(f'<text class="{i}-cap" x="{self.cx(0)}" y="{y + 14}">место в потоке (seq) →</text>')
        a(f'<text class="{i}-cap" x="{SRV_X}" y="{y + 14}">сервер</text>')
        # линейка: подписи позиций и скобка над именем сайта
        ry = y + 44
        a(f'<line class="{i}-rule" x1="{self.cx(-self.neg)}" y1="{ry}" x2="{self.cx(self.N)}" y2="{ry}"/>')
        marks = {0: "0", self.N: str(s.get("len", self.N))}
        if self.neg:
            marks[-self.neg] = f"−{self.neg}"
        for pos, lab in s.get("cuts", []) + s.get("marks", []):
            marks[pos] = lab
        for pos, lab in sorted(marks.items()):
            x = self.cx(pos)
            a(f'<line class="{i}-rule" x1="{x}" y1="{ry - 5}" x2="{x}" y2="{ry}"/>')
            anchor = ("end" if self.neg else "start") if pos == -self.neg else ("end" if pos == self.N else "middle")
            a(f'<text class="{i}-tick" x="{x}" y="{ry - 9}" text-anchor="{anchor}">{esc(lab)}</text>')
        if s.get("name_span"):
            h0, h1 = s["name_span"]
            x0, x1 = self.cx(h0) + 2, self.cx(h1) - 2
            a(f'<path class="{i}-brace" d="M{x0} {ry + 10}v-4H{x1}v4"/>')
        return ry + 26

    def cells(self, pos, chars, cls, y, name=None):
        """Кусок потока: одна рамка, внутри байты с шагом ячейки.
        Байты имени сайта — основным цветом, служебные — приглушённо."""
        i = self.id
        x0 = self.cx(pos)
        out = [f'<rect class="{i}-{cls}" x="{x0 + 1}" y="{y}" width="{len(chars) * self.cw - 2}" height="{CH}" rx="4"/>']
        h0, h1 = name or self.s.get("name_span") or (0, 0)
        for k, ch in enumerate(chars):
            if cls == "fk":
                c = "ch-fk"
            elif h0 <= pos + k < h1 and ch not in "·X":
                c = "ch"
            else:
                c = "ch-mu"
            out.append(f'<text class="{i}-{c}" x="{self.cx(pos + k) + self.cw / 2}" y="{y + 18}">{esc(ch)}</text>')
        return "".join(out)

    def row(self, r, y):
        i, t = self.id, r["t"]
        a = self.add
        kind = r.get("kind", "real")
        lab = r["label"]
        # подпись: «#1  FAKE1  seq=0  len=14» — как в таблицах статей
        a(f'<g class="{self.appear(t)}"><text class="{i}-lbl" x="{LBL_X}" y="{y + 18}">'
          f'<tspan class="{i}-no">{esc(r["no"])}</tspan> '
          f'<tspan class="{i}-{"kfk" if kind == "fake" else "k"}">{esc(lab)}</tspan>'
          f'<tspan class="{i}-meta"> {esc(r.get("meta", ""))}</tspan></text></g>')
        if r.get("range") is not None:
            p0 = r["range"][0]
            chars = r.get("chars")
            if chars is None:
                chars = self.s["tape"][r["range"][0]:r["range"][1]] if kind != "fake" else "X" * (r["range"][1] - r["range"][0])
            r["range"] = (p0, p0 + len(chars))
            cls = "fk" if kind == "fake" else ("dim" if kind == "dropped" else "rl")
            x0, x1 = self.cx(p0), self.cx(p0 + len(chars))
            gone = r.get("rejected") or kind == "dropped"
            dimmed = [(t + 0.9, "opacity:.55;transform:translateX(0px)")] if gone else None
            a(f'<g class="{self.appear(t, dimmed, dx=-14)}">{self.cells(p0, chars, cls, y)}'
              f'{self.extra_cells(r, y)}</g>')
            if gone:
                # отброшенный или выброшенный пакет перечёркивается
                a(f'<line class="{i}-strike {self.anim([(0, "transform:scaleX(0)"), (t + 0.7, "transform:scaleX(0)"), (t + 1.0, "transform:scaleX(1)"), (self.T - 0.55, "transform:scaleX(1);opacity:1"), (self.T - 0.15, "transform:scaleX(1);opacity:0")])}" '
                  f'x1="{x0 - 3}" y1="{y + CH / 2}" x2="{x1 + 3}" y2="{y + CH / 2}"/>')
        elif r.get("arrow"):
            a(f'<g class="{self.appear(t, dx=-14)}"><text class="{i}-arrow" x="{self.cx(0)}" y="{y + 18}">{esc(r["arrow"])}</text></g>')
        srv = r.get("server", "")
        if srv:
            cls = "srv-no" if r.get("rejected") or kind == "dropped" else "srv"
            a(f'<g class="{self.appear(t + 0.55)}"><text class="{i}-{cls}" x="{SRV_X}" y="{y + 18}">{esc(srv)}</text></g>')

    def extra_cells(self, r, y):
        """Особые ячейки внутри пакета (байт OOB, байт seqovl) — акцентом."""
        out = []
        for pos in r.get("mark", []):
            x = self.cx(pos)
            out.append(f'<rect class="{self.id}-mk" x="{x + 2}" y="{y + 1}" width="{self.cw - 4}" height="{CH - 2}" rx="3"/>')
        return "".join(out)

    def buffer(self, y):
        s, i = self.s, self.id
        a = self.add
        a(f'<line class="{i}-sep" x1="0" y1="{y - 8}" x2="{W}" y2="{y - 8}"/>')
        a(f'<text class="{i}-lbl" x="{LBL_X}" y="{y + 28}"><tspan class="{i}-k">буфер сервера</tspan></text>')
        by = y + 10
        # пустые места буфера
        a(f'<rect class="{i}-slot" x="{self.cx(0) + 1}" y="{by}" width="{self.BN * self.cw - 2}" height="{CH}" rx="4"/>')
        btape = s.get("buf_tape", s["tape"])
        bname = s.get("buf_name", s.get("name_span"))
        for r in s["rows"]:
            fill = r.get("fills")
            if not fill:
                continue
            # fills: (от, до) по буферу или [(от, до, сдвиг_в_ячейках), …] — кусок
            # въезжает со сдвигом и встаёт на место (так байт OOB «вынимается»)
            parts = [fill + (0,)] if isinstance(fill, tuple) else fill
            for f0, f1, sh in parts:
                t = r["t"] + 0.55
                cells = self.cells(f0, btape[f0:f1], "rl", by, name=bname)
                if sh:
                    d = sh * self.cw
                    cls = self.anim([(0, f"opacity:0;transform:translateX({d}px)"), (t, f"opacity:0;transform:translateX({d}px)"),
                                     (t + 0.35, f"opacity:1;transform:translateX({d}px)"), (t + 0.9, f"opacity:1;transform:translateX({d}px)"),
                                     (t + 1.4, "opacity:1;transform:translateX(0px)"), (self.T - 0.55, "opacity:1;transform:translateX(0px)"),
                                     (self.T - 0.15, "opacity:0;transform:translateX(0px)")])
                else:
                    cls = self.appear(t)
                a(f'<g class="{cls}">{cells}</g>')
        if bname:
            h0, h1 = bname
            a(f'<line class="{i}-uline {self.anim([(0, "transform:scaleX(0)"), (self.t_done, "transform:scaleX(0)"), (self.t_done + 0.6, "transform:scaleX(1)"), (self.T - 0.55, "transform:scaleX(1);opacity:1"), (self.T - 0.15, "transform:scaleX(1);opacity:0")])}" '
              f'x1="{self.cx(h0) + 1}" y1="{by + CH + 5}" x2="{self.cx(h1) - 1}" y2="{by + CH + 5}"/>')
        res = s.get("result")
        if res:
            a(f'<g class="{self.appear(self.t_done + 0.4)}"><text class="{i}-srv" x="{SRV_X}" y="{by + 18}">{esc(res)}</text></g>')
        return by + CH + 14

    def notes(self, y):
        i = self.id
        for k, (who, text) in enumerate(self.s.get("notes", [])):
            yy = y + 18 + k * 22
            self.add(f'<g class="{self.appear(self.t_done + 0.7 + 0.25 * k)}"><text class="{i}-note" x="{LBL_X}" y="{yy}">'
                     f'<tspan class="{i}-who">{esc(who)}</tspan> {esc(text)}</text></g>')
        return y + 18 + len(self.s.get("notes", [])) * 22

    # ── вывод ───────────────────────────────────────────────────────
    def style(self):
        i = self.id
        R = f".{i}"
        # (переменная темы, светлый запас, тёмный запас)
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
        mono = "var(--codeFont,'JetBrains Mono'),ui-monospace,'Cascadia Code',Consolas,monospace"
        sans = "var(--bodyFont,'Source Sans 3'),system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
        head = "var(--headerFont,Inter),system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
        rules = [
            f"{R}{{{light}}}",
            f"@media (prefers-color-scheme:dark){{{R}{{{dark}}}}}",
            f"{R} .{i}-bg{{fill:var(--bg)}}",
            f"{R} text{{font-family:{mono};font-size:13.5px;fill:var(--fg2)}}",
            f"{R} .{i}-cap{{font-family:{head};font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;fill:var(--mute)}}",
            f"{R} .{i}-tick{{font-size:11px;fill:var(--mute)}}",
            f"{R} .{i}-rule{{stroke:var(--mute);stroke-width:1}}",
            f"{R} .{i}-brace{{fill:none;stroke:var(--acc);stroke-width:1.3}}",
            f"{R} .{i}-cut{{stroke:var(--acc);stroke-width:1;stroke-dasharray:3 4;opacity:.55}}",
            f"{R} .{i}-win{{stroke:var(--fg2);stroke-width:1.4}}",
            f"{R} .{i}-sep{{stroke:var(--line);stroke-width:1}}",
            f"{R} .{i}-no{{fill:var(--mute)}}",
            f"{R} .{i}-k{{fill:var(--fg);font-weight:600}}",
            f"{R} .{i}-kfk{{fill:var(--mute);font-weight:600}}",
            f"{R} .{i}-meta{{fill:var(--mute)}}",
            f"{R} .{i}-arrow{{font-family:{sans};font-size:14px;fill:var(--fg2)}}",
            f"{R} .{i}-rl{{fill:var(--tint);stroke:var(--acc);stroke-width:1}}",
            f"{R} .{i}-fk{{fill:none;stroke:var(--mute);stroke-width:1;stroke-dasharray:2 2}}",
            f"{R} .{i}-dim{{fill:none;stroke:var(--line);stroke-width:1}}",
            f"{R} .{i}-mk{{fill:none;stroke:var(--fg);stroke-width:1.8}}",
            f"{R} .{i}-slot{{fill:none;stroke:var(--line);stroke-width:1;stroke-dasharray:3 3}}",
            f"{R} .{i}-ch{{font-size:14px;fill:var(--fg);text-anchor:middle}}",
            f"{R} .{i}-ch-fk{{font-size:14px;fill:var(--mute);text-anchor:middle}}",
            f"{R} .{i}-ch-mu{{font-size:14px;fill:var(--mute);text-anchor:middle}}",
            f"{R} .{i}-strike{{stroke:var(--fg2);stroke-width:1.4;transform-box:fill-box;transform-origin:left center}}",
            f"{R} .{i}-uline{{stroke:var(--acc);stroke-width:2;transform-box:fill-box;transform-origin:left center}}",
            f"{R} .{i}-srv{{font-family:{sans};font-size:14px;fill:var(--fg)}}",
            f"{R} .{i}-srv-no{{font-family:{sans};font-size:14px;fill:var(--mute)}}",
            f"{R} .{i}-note{{font-family:{sans};font-size:14.5px;fill:var(--fg2)}}",
            f"{R} .{i}-who{{font-family:{head};font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;fill:var(--acc)}}",
            f"{R} .a{{animation-duration:{self.T}s;animation-timing-function:cubic-bezier(.3,.6,.25,1);animation-iteration-count:infinite;animation-fill-mode:both}}",
            f"@media (prefers-reduced-motion:reduce){{{R} .a{{animation:none}}}}",
            # обёртка при встраивании в страницу
            f"figure.{i}-fig{{margin:1.6rem 0;overflow-x:auto}}",
            f"figure.{i}-fig>svg{{display:block;width:100%;min-width:680px;height:auto}}",
        ]
        return "".join(rules + self.css)

    def render(self):
        s, i = self.s, self.id
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" class="{i}" viewBox="0 0 {W} {self.H}" width="{W}" height="{self.H}" role="img" aria-labelledby="{i}-t {i}-d">',
            f'<title id="{i}-t">{esc(s["title"])}</title>',
            f'<desc id="{i}-d">{esc(s["desc"])}</desc>',
            f"<style>{self.style()}</style>",
            f'<rect class="{i}-bg" x="0" y="0" width="{W}" height="{self.H}"/>',
        ]
        out += self.body
        out.append("</svg>")
        return "\n".join(out) + "\n"


# ── общий ClientHello: 26 байт в ASCII-виде, имя с 11-й позиции ─────
TAPE = "···········youtube.com····"
NAME = (11, 22)
MIDSLD = 14          # середина «youtube»: you|tube
SPECS = {}


def R(no, label, meta, rng, kind="real", **kw):
    d = {"no": f"#{no}" if isinstance(no, int) else no, "label": label, "meta": meta, "range": rng, "kind": kind}
    d.update(kw)
    return d


def A(no, label, meta, arrow, **kw):
    """Строка без данных (SYN, SYN-ACK)."""
    d = {"no": f"#{no}", "label": label, "meta": meta, "range": None, "arrow": arrow, "kind": "real"}
    d.update(kw)
    return d


SPECS["fake"] = dict(
    name="fake", tape=TAPE, name_span=NAME, len=26,
    rows=[
        R(1, "FAKE", "seq=0  blob", (0, 26), "fake", chars="···········www.w3.org·····", rejected=True, server="отброшен: md5"),
        R(2, "ORIG", "seq=0  len=26", (0, 26), server="принят", fills=(0, 26)),
    ],
    result="поток собран",
    notes=[("DPI", "первым читает ClientHello с www.w3.org; если решение принято по нему, настоящий пакет уже не проверяется"),
           ("сервер", "фейк отбрасывает по неверной подписи TCP MD5 (tcp_md5), принимает оригинал")],
    title="fake: фейковый ClientHello перед оригиналом",
    desc="Карта потока для fake с blob=fake_default_tls и tcp_md5: сначала уходит фейковый ClientHello с именем www.w3.org на тех же позициях потока, затем оригинал с youtube.com. Сервер отбрасывает фейк по неверной подписи TCP MD5 и принимает оригинал.",
)

SPECS["multisplit"] = dict(
    name="multisplit", tape=TAPE, name_span=NAME, len=26,
    cuts=[(1, "1"), (MIDSLD, "midsld")],
    rows=[
        R(1, "PART1", "seq=0  len=1", (0, 1), server="принят", fills=(0, 1)),
        R(2, "PART2", "seq=1  len=13", (1, 14), server="принят", fills=(1, 14)),
        R(3, "PART3", "seq=14 len=12", (14, 26), server="принят", fills=(14, 26)),
    ],
    result="поток собран",
    notes=[("DPI", "имя разрезано между #2 и #3: целиком youtube.com нет ни в одном пакете"),
           ("сервер", "складывает сегменты по seq и получает исходный ClientHello")],
    title="multisplit: три сегмента по порядку",
    desc="Карта потока для multisplit с pos=1,midsld: ClientHello уходит тремя сегментами по порядку — 1 байт, байты до середины имени, остаток. Имя youtube.com разрезано между вторым и третьим сегментом, сервер собирает поток по seq.",
)

SPECS["multidisorder"] = dict(
    name="multidisorder", tape=TAPE, name_span=NAME, len=26,
    cuts=[(MIDSLD, "midsld")],
    rows=[
        R(1, "PART2", "seq=14 len=12", (14, 26), server="ждёт в буфере", fills=(14, 26)),
        R(2, "PART1", "seq=0  len=14", (0, 14), server="принят", fills=(0, 14)),
    ],
    result="поток собран",
    notes=[("DPI", "конец запроса приходит раньше начала; без пересборки потока имени целиком не видно"),
           ("сервер", "держит #1 в буфере и ставит #2 перед ним по seq")],
    title="multidisorder: части в обратном порядке",
    desc="Карта потока для multidisorder с pos=midsld: сначала уходит вторая часть ClientHello (seq=14), затем первая (seq=0). Сервер держит вторую часть в буфере и собирает поток по seq.",
)

L_TAPE = "············youtube.com·········"      # 32 ячейки по 25 байт = 800 байт
SPECS["multidisorder_legacy"] = dict(
    name="multidisorder_legacy", tape=L_TAPE, name_span=(12, 23), len=800, cw=17,
    cuts=[(8, "200"), (24, "600")], marks=[(20, "A|B 500")],
    rows=[
        R(1, "A2", "seq=200 len=300", (8, 20), server="ждёт в буфере", fills=(8, 20)),
        R(2, "A1", "seq=0   len=200", (0, 8), server="принят", fills=(0, 8)),
        R(3, "B2", "seq=600 len=200", (24, 32), server="ждёт в буфере", fills=(24, 32)),
        R(4, "B1", "seq=500 len=100", (20, 24), server="принят", fills=(20, 24)),
    ],
    result="поток собран",
    notes=[("DPI", "ClientHello из двух пакетов A и B: задом наперёд части идут только внутри пакета, A по-прежнему раньше B"),
           ("сервер", "собирает 0–800 по seq; новый multidisorder развернул бы весь поток: 600–800, 200–600, 0–200")],
    title="multidisorder_legacy: обратный порядок внутри каждого пакета",
    desc="Карта потока для multidisorder_legacy с pos=200,600: ClientHello длиной 800 байт пришёл от ядра двумя пакетами, A (0–499) и B (500–799). Каждый пакет режется отдельно и уходит задом наперёд: A2, A1, затем B2, B1.",
)


def _faked(order):
    rows, no = [], 1
    for part in order:
        rng = (0, MIDSLD) if part == 1 else (MIDSLD, 26)
        meta = f"seq={rng[0]:<2} len={rng[1] - rng[0]}"
        for lab, kind in ((f"FAKE{part}", "fake"), (f"REAL{part}", "real"), (f"FAKE{part}", "fake")):
            if kind == "fake":
                rows.append(R(no, lab, meta, rng, "fake", rejected=True, server="отброшен: ack"))
            else:
                rows.append(R(no, lab, meta, rng, server="принят", fills=rng))
            no += 1
    return rows


_FD = dict(tape=TAPE, name_span=NAME, len=26, cuts=[(MIDSLD, "midsld")], result="поток собран")

SPECS["fakedsplit"] = dict(
    _FD, name="fakedsplit", rows=_faked([1, 2]),
    notes=[("DPI", "три сегмента с seq=0 и три с seq=14: какая копия в каждой тройке настоящая, по пакетам не видно"),
           ("сервер", "фейки отбрасывает по неверному ACK (tcp_ack=-66000), из REAL1 и REAL2 собирает исходный поток")],
    title="fakedsplit: порядок отправки и сборка на сервере",
    desc="Карта потока для fakedsplit с pos=midsld: шесть сегментов в порядке отправки — FAKE1, REAL1, FAKE1, FAKE2, REAL2, FAKE2. Фейки лежат на тех же позициях потока, что и настоящие части, и заполнены мусором X. Сервер отбрасывает фейки по неверному ACK и собирает ClientHello из двух настоящих частей.",
)

SPECS["fakeddisorder"] = dict(
    _FD, name="fakeddisorder", rows=_faked([2, 1]),
    notes=[("DPI", "по три копии каждой части, и конец запроса приходит раньше начала"),
           ("сервер", "фейки отбрасывает по неверному ACK (tcp_ack=-66000), REAL2 держит в буфере до прихода REAL1")],
    title="fakeddisorder: фейки и обратный порядок частей",
    desc="Карта потока для fakeddisorder с pos=midsld: сначала вторая часть ClientHello в окружении фейков (FAKE2, REAL2, FAKE2), затем первая (FAKE1, REAL1, FAKE1). Сервер отбрасывает фейки по неверному ACK и собирает поток по seq.",
)

SPECS["hostfakesplit"] = dict(
    name="hostfakesplit", tape=TAPE, name_span=NAME, len=26,
    cuts=[(11, "host"), (22, "endhost")],
    rows=[
        R(1, "BEFORE", "seq=0  len=11", (0, 11), server="принят", fills=(0, 11)),
        R(2, "FAKE", "seq=11 len=11", (11, 22), "fake", chars="u9a7bk2.org", rejected=True, server="отброшен: md5"),
        R(3, "HOST", "seq=11 len=11", (11, 22), server="принят", fills=(11, 22)),
        R(4, "FAKE", "seq=11 len=11", (11, 22), "fake", chars="u9a7bk2.org", rejected=True, server="отброшен: md5"),
        R(5, "AFTER", "seq=22 len=4", (22, 26), server="принят", fills=(22, 26)),
    ],
    result="поток собран",
    notes=[("DPI", "на месте имени три сегмента одной длины с одним seq: u9a7bk2.org, youtube.com, u9a7bk2.org"),
           ("сервер", "фейковые имена отбрасывает по неверной подписи TCP MD5 (tcp_md5)")],
    title="hostfakesplit: имя сайта между фейковыми именами",
    desc="Карта потока для hostfakesplit с tcp_md5: ClientHello режется по границам имени, настоящее имя youtube.com уходит между двумя фейковыми именами u9a7bk2.org той же длины и с тем же seq. Сервер отбрасывает фейки по неверной подписи TCP MD5.",
)

SPECS["tcpseg"] = dict(
    name="tcpseg", tape=TAPE, name_span=NAME, len=26, neg=1, cw=21,
    rows=[
        R("–", "ORIG", "seq=0  len=26", (0, 26), "dropped", server="drop: не ушёл"),
        R(1, "SEG", "seq=-1 len=27", (-1, 26), chars="X" + TAPE, mark=[-1], server="байт −1 отрезан", fills=(0, 26)),
    ],
    result="поток собран",
    notes=[("DPI", "поток начинается на байт раньше, и первый байт — мусор: разбор ClientHello может сбиться"),
           ("сервер", "байт левее окна приёма отрезает, остальное принимает; оригинал выбросил инстанс drop")],
    title="tcpseg: ClientHello одним сегментом с seqovl",
    desc="Карта потока для tcpseg с pos=0,-1 и seqovl=1 в связке с drop: оригинальный пакет выбрасывается, вместо него уходит сегмент с seq=-1 и одним байтом мусора спереди. Сервер отрезает байт левее окна приёма и принимает ClientHello целиком.",
)

O_TAPE = TAPE[:MIDSLD] + "·" + TAPE[MIDSLD:]     # байт OOB посреди имени
SPECS["oob"] = dict(
    name="oob", tape=O_TAPE, name_span=(11, 23), len=27, cw=21,
    cuts=[(MIDSLD, "urp=midsld")],
    buf_tape=TAPE, buf_len=26, buf_name=NAME,
    rows=[
        A(1, "SYN", "seq−1", "SYN с номером на 1 меньше: место под лишний байт", server="принят"),
        R(2, "DATA", "URG len=27", (0, 27), mark=[MIDSLD], server="байт URG вынут",
          fills=[(0, MIDSLD, 0), (MIDSLD, 26, 1)]),
    ],
    result="поток собран",
    notes=[("DPI", "в имени лишний байт: you·tube.com не совпадает с youtube.com"),
           ("сервер", "байт с флагом URG вынимает из потока как срочные данные, имя смыкается")],
    title="oob: байт срочных данных внутри имени сайта",
    desc="Карта потока для oob с urp=midsld: сначала SYN с номером последовательности на единицу меньше, затем ClientHello с байтом срочных данных (флаг URG) посреди имени youtube.com. TCP-стек сервера вынимает этот байт, и имя смыкается.",
)

SPECS["syndata"] = dict(
    name="syndata", tape=TAPE, name_span=NAME, len=26,
    rows=[
        R(1, "SYN+DATA", "blob", (0, 26), "fake", chars="···········www.w3.org·····", rejected=True, server="SYN принят"),
        A(2, "SYN-ACK", "← сервер", "ответ сервера, данные из SYN не подтверждены"),
        R(3, "ORIG", "seq=0  len=26", (0, 26), server="принят", fills=(0, 26)),
    ],
    result="поток собран",
    notes=[("DPI", "первые данные потока пришли в SYN; если DPI счёл их ClientHello, настоящий может не проверяться"),
           ("сервер", "данные из SYN большинство TCP-стеков игнорирует и ждёт их заново после рукопожатия")],
    title="syndata: фейковый ClientHello в SYN-пакете",
    desc="Карта потока для syndata с blob=fake_default_tls: к SYN приклеен фейковый ClientHello с именем www.w3.org на тех же позициях потока. Сервер отвечает SYN-ACK, данные из SYN игнорирует, после рукопожатия принимает настоящий ClientHello.",
)


def main():
    root = Path(__file__).resolve().parent.parent
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "Zapret2/desync/attachments"
    out.mkdir(parents=True, exist_ok=True)
    for n in sys.argv[2:] or list(SPECS):
        svg = Diagram(SPECS[n]).build()
        p = out / f"desync-anim-{n}.svg"
        p.write_text(svg, encoding="utf-8")
        print(p, len(svg))


if __name__ == "__main__":
    main()
