#!/usr/bin/env python3
"""Генератор анимированных SVG-схем техник дурения DPI (Zapret2/desync/attachments/desync-anim-*.svg).

Сцена как в заставке главной wiki.zapret.moe: «ваш ПК → ТСПУ → сервер».
Пакеты едут слева направо в порядке отправки; на ТСПУ появляется то, что
увидел DPI, на сервере — то, что он собрал. Анимация — CSS внутри SVG
(transform/opacity), один цикл на все элементы, работает в <img>.
"""
import html
import sys
from pathlib import Path

W, H = 960, 672
LANE_Y = 292
PC = (30, 150)          # x-границы блока «ваш ПК»
SRV = (810, 930)        # x-границы блока «сервер»
GATE_X = 480
TRAVEL = 2.2            # примерное время пути от ПК до сервера
SPEED = 250.0           # px/с — скорость всех пакетов
GAP = 0.85              # пауза между отправками
FS_PK = 21              # кегль подписи пакета
CH = 0.62               # ширина моноширинного символа в em

C = {
    "bg": "#0b1020", "line": "#1f2a48", "ink": "#e8edff", "dim": "#8d99bd",
    "mut": "#7d8bb0", "red": "#ff3b5c", "grn": "#37e39a", "amb": "#ffb020",
    "cy": "#4fd1ff", "vio": "#9b7bff", "pink": "#ff6fa3", "pk": "#0e1630",
}
PART_COL = {1: C["cy"], 2: C["vio"], 3: C["amb"], 4: C["pink"]}
CIRC = {1: "①", 2: "②", 3: "③", 4: "④"}


def esc(s):
    return html.escape(s, quote=True)


def tw(text, fs):
    return len(text) * fs * CH


class Svg:
    def __init__(self, spec):
        self.s = spec
        self.css = []
        self.body = []
        self.n = 0
        self.T = 1.0

    # ── анимации ────────────────────────────────────────────────────
    def kf(self, frames, cls="a"):
        """frames: [(t, {'o':op, 'x':px, 'y':px})]; возвращает атрибуты."""
        self.n += 1
        name = f"k{self.n}"
        pts = {}
        for t, st in frames:
            t = max(0.0, min(self.T, t))
            pts[round(t / self.T * 100, 3)] = st
        if 0 not in pts:
            first = pts[min(pts)]
            pts[0] = dict(first)
        if 100 not in pts:
            pts[100] = dict(pts[max(pts)])
        rules = []
        for p in sorted(pts):
            st = pts[p]
            decl = []
            if "o" in st:
                decl.append(f"opacity:{st['o']}")
            if "x" in st:
                decl.append(f"transform:translate({st['x']:.1f}px,{st.get('y', 0):.1f}px)")
            rules.append(f"{p}%{{{';'.join(decl)}}}")
        self.css.append(f"@keyframes {name}{{{''.join(rules)}}}")
        return f'class="{cls}" style="animation-name:{name}"'

    def show_at(self, t, cls="a fin"):
        """Появиться в t и держаться до конца цикла."""
        return self.kf([(0, {"o": 0}), (t, {"o": 0}), (t + 0.3, {"o": 1}),
                        (self.T - 0.7, {"o": 1}), (self.T - 0.25, {"o": 0})], cls)

    def pulses(self, times, peak=0.95, cls="a pk"):
        fr = [(0, {"o": 0})]
        for t in sorted(times):
            fr += [(t - 0.06, {"o": 0}), (t + 0.06, {"o": peak}), (t + 0.5, {"o": 0})]
        return self.kf(fr, cls)

    # ── рисование ───────────────────────────────────────────────────
    def add(self, s):
        self.body.append(s)

    def label(self, spans, x, y, fs, anchor="middle"):
        out = [f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" text-anchor="{anchor}" class="mono">']
        for text, col in spans:
            fill = f' fill="{col}"' if col else ""
            out.append(f"<tspan{fill}>{esc(text)}</tspan>")
        out.append("</text>")
        return "".join(out)

    def box(self, w, h, kind, col, dash=False):
        stroke = C["mut"] if kind == "fake" else col
        d = ' stroke-dasharray="7 6"' if dash or kind == "fake" else ""
        fill = "#161a2a" if kind == "fake" else C["pk"]
        return (f'<rect x="{-w / 2:.1f}" y="{-h / 2:.1f}" width="{w:.1f}" height="{h}" rx="11" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="2.4"{d}/>')

    def build(self):
        s = self.s
        ev = s["events"]
        # ширина и путь каждого пакета; скорость у всех одна, иначе широкий догонит узкий
        for e in ev:
            e.setdefault("kind", "real")
            text = "".join(x for x, _ in e["label"])
            e["w"] = max(tw(text, FS_PK) + 30, 70)
            if e.get("dir") == "back":
                e["x0"] = SRV[0] - e["w"] / 2 - 8
                e["x1"] = PC[1] + e["w"] / 2 + 8
            else:
                e["x0"] = PC[1] + e["w"] / 2 + 8
                e["x1"] = SRV[0] - e["w"] / 2 - 8
            e["tr"] = abs(e["x1"] - e["x0"]) / SPEED
        # расписание: следующий стартует, когда предыдущий освободил место
        t = 0.6
        for i, e in enumerate(ev):
            e["t0"] = t + e.get("delay", 0)
            nxt = ev[i + 1]["w"] if i + 1 < len(ev) else 0
            t = e["t0"] + max(e.get("gap", GAP), (nxt + 36) / SPEED)
        gate_times, fake_hits = [], []
        for e in ev:
            e["tg"] = e["t0"] + abs(GATE_X - e["x0"]) / SPEED
            e["ta"] = e["t0"] + e["tr"]
            if e["kind"] != "dropped" and e.get("dir") != "back" and not e.get("nodpi"):
                gate_times.append(e["tg"])
            if e["kind"] == "fake":
                fake_hits.append(e["ta"])
        last = max(e["t0"] + (1.6 if e["kind"] == "dropped" else e["tr"]) for e in ev)
        self.T = round(last + s.get("hold", 3.6), 2)
        self.gate_times = gate_times
        self.fake_hits = fake_hits
        self.dpi_done = max(gate_times) + 0.35
        self.srv_done = max(e["ta"] for e in ev if e["kind"] != "dropped") + 0.35

        self.scene()
        self.payload_bar()
        self.panels()
        for e in ev:
            self.packet(e)
        return self.render()

    def scene(self):
        s = self.s
        a = self.add
        a(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26" fill="{C["bg"]}" stroke="{C["line"]}" stroke-width="2"/>')
        a(f'<text x="36" y="58" class="mono" font-size="30" font-weight="700" fill="{C["cy"]}">{esc(s["name"])}</text>')
        a(f'<text x="{36 + tw(s["name"], 30) + 18:.0f}" y="57" class="sans" font-size="19" fill="{C["dim"]}">{esc(s["subtitle"])}</text>')
        a(f'<text x="36" y="90" class="mono" font-size="15" fill="{C["mut"]}">{esc(s["cmd"])}</text>')
        # дорожка
        a(f'<line x1="{PC[1]}" y1="{LANE_Y}" x2="{SRV[0]}" y2="{LANE_Y}" stroke="rgba(151,166,201,.4)" stroke-width="2" stroke-dasharray="6 10"/>')
        for (x0, x1), lab, sub in ((PC, "ваш ПК", "Zapret 2"), (SRV, "сервер", s.get("server", "youtube.com"))):
            cx = (x0 + x1) / 2
            a(f'<rect x="{x0}" y="{LANE_Y - 44}" width="{x1 - x0}" height="88" rx="16" fill="#111a33" stroke="#2d3b66" stroke-width="2"/>')
            a(f'<text x="{cx}" y="{LANE_Y - 4}" class="sans" font-size="20" font-weight="700" fill="{C["ink"]}" text-anchor="middle">{lab}</text>')
            a(f'<text x="{cx}" y="{LANE_Y + 24}" class="mono" font-size="14" fill="{C["dim"]}" text-anchor="middle">{esc(sub)}</text>')
        # ТСПУ
        gy0, gy1 = LANE_Y - 66, LANE_Y + 66
        a(f'<text x="{GATE_X}" y="{gy0 - 12}" class="sans" font-size="21" font-weight="800" letter-spacing="2" fill="{C["red"]}" text-anchor="middle">ТСПУ</text>')
        a(f'<rect x="{GATE_X - 14}" y="{gy0}" width="28" height="{gy1 - gy0}" rx="8" fill="rgba(255,59,92,.14)" stroke="{C["red"]}" stroke-width="2"/>')
        a(f'<g {self.pulses(self.gate_times)}><rect x="{GATE_X - 14}" y="{gy0}" width="28" height="{gy1 - gy0}" rx="8" fill="rgba(255,176,32,.55)" stroke="{C["amb"]}" stroke-width="5"/></g>')
        # сервер отбрасывает фейк
        if self.fake_hits and s.get("fake_flash", True):
            cx = (SRV[0] + SRV[1]) / 2
            a(f'<g {self.pulses(self.fake_hits)}><rect x="{SRV[0]}" y="{LANE_Y - 44}" width="{SRV[1] - SRV[0]}" height="88" rx="16" fill="rgba(255,59,92,.18)" stroke="{C["red"]}" stroke-width="4"/>'
              f'<text x="{cx}" y="{LANE_Y - 56}" class="sans" font-size="18" font-weight="700" fill="{C["red"]}" text-anchor="middle">✕ фейк</text></g>')
        # легенда
        leg = s.get("legend")
        if leg:
            a(f'<text x="36" y="{LANE_Y + 92}" class="sans" font-size="15" fill="{C["dim"]}">{esc(leg)}</text>')

    def payload_bar(self):
        s = self.s
        a = self.add
        parts = s["parts"]
        y, h = 118, 40
        a(f'<text x="36" y="{y + 26}" class="sans" font-size="16" fill="{C["dim"]}">{esc(s.get("bar_title", "что отправляет браузер:"))}</text>')
        x = 36 + len(s.get("bar_title", "что отправляет браузер:")) * 16 * 0.6 + 14
        avail = W - 36 - x
        ws = [tw(p["text"], 17) + 26 for p in parts]
        k = min(1.0, avail / sum(ws))
        for p, w in zip(parts, ws):
            w *= k
            col = PART_COL.get(p.get("n"), C["dim"])
            a(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="6" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-width="1.6"/>')
            a(self.label([(p["text"], C["ink"])], x + w / 2, y + 26, 17))
            x += w
            if p.get("cut"):
                a(f'<line x1="{x:.1f}" y1="{y - 8}" x2="{x:.1f}" y2="{y + h + 8}" stroke="{C["red"]}" stroke-width="2.4" stroke-dasharray="4 3"/>')
                a(f'<text x="{x:.1f}" y="{y + h + 22}" class="mono" font-size="13" fill="{C["red"]}" text-anchor="middle">{esc(p["cut"])}</text>')
            if p.get("pkt_edge"):
                a(f'<line x1="{x:.1f}" y1="{y - 4}" x2="{x:.1f}" y2="{y + h + 4}" stroke="{C["ink"]}" stroke-width="3"/>')

    def panels(self):
        s = self.s
        a = self.add
        y0, y1 = 420, 652
        for x0, x1, title, col in ((30, 470, "что видит ТСПУ", C["red"]), (490, 930, "что собирает сервер", C["grn"])):
            a(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="18" fill="#0f1730" stroke="#243056" stroke-width="1.6"/>')
            a(f'<text x="{x0 + 20}" y="{y0 + 32}" class="sans" font-size="18" font-weight="700" fill="{col}">{title}</text>')
        # чипы DPI
        x, y = 50, y0 + 52
        for e in self.s["events"]:
            if e["kind"] == "dropped" or e.get("dir") == "back" or e.get("nodpi"):
                continue
            chip = e.get("chip", e["label"])
            text = "".join(t for t, _ in chip)
            w = tw(text, 18) + 22
            if x + w > 452:
                x, y = 50, y + 50
            kind = "fake" if (e["kind"] == "fake" and not s.get("dpi_blind")) else "real"
            col = C["ink"] if s.get("dpi_blind") else PART_COL.get(e.get("part"), C["ink"])
            a(f'<g {self.show_at(e["tg"])}><g transform="translate({x + w / 2:.1f},{y + 20})">{self.box(w, 40, kind, col)}{self.label(chip, 0, 7, 18)}</g></g>')
            x += w + 10
        vy = y + 76
        for i, line in enumerate(s["dpi_verdict"]):
            col = C["amb"] if i == 0 else C["ink"]
            a(f'<g {self.show_at(self.dpi_done + 0.2 * i)}><text x="50" y="{vy + i * 27}" class="sans" font-size="18" font-weight="{700 if i == 0 else 400}" fill="{col}">{esc(line)}</text></g>')
        # слоты сервера
        slots = s.get("slots", [])
        x, y = 510, y0 + 52
        for sl in slots:
            text = sl["text"]
            w = tw(text, 18) + 24
            col = PART_COL.get(sl.get("n"), C["grn"])
            a(f'<g transform="translate({x + w / 2:.1f},{y + 20})"><rect x="{-w / 2:.1f}" y="-20" width="{w:.1f}" height="40" rx="10" fill="none" stroke="#33406a" stroke-width="1.6" stroke-dasharray="4 4"/></g>')
            t_fill = min(e["ta"] for e in s["events"] if e.get("fills") == sl["n"])
            a(f'<g {self.show_at(t_fill)}><g transform="translate({x + w / 2:.1f},{y + 20})">{self.box(w, 40, "real", col)}{self.label([(text, C["ink"])], 0, 7, 18)}</g></g>')
            x += w + 8
        ny = y + 80
        for i, (t_key, line, col) in enumerate(self.srv_notes()):
            a(f'<g {self.show_at(t_key)}><text x="510" y="{ny + i * 27}" class="sans" font-size="17" fill="{col}">{esc(line)}</text></g>')
        a(f'<g {self.show_at(self.srv_done + 0.3)}><text x="510" y="{y1 - 24}" class="sans" font-size="20" font-weight="700" fill="{C["grn"]}">{esc(s["result"])}</text></g>')

    def srv_notes(self):
        out = []
        for n in self.s.get("srv_notes", []):
            t_key = n.get("t")
            if t_key == "fake":
                t_key = min(self.fake_hits)
            elif isinstance(t_key, int):
                t_key = self.s["events"][t_key]["ta"]
            out.append((t_key, n["text"], n.get("col", C["dim"])))
        return out

    def packet(self, e):
        a = self.add
        w, h = e["w"], 46
        col = PART_COL.get(e.get("part"), C["ink"])
        inner = self.box(w, h, e["kind"] if e["kind"] != "dropped" else "real", col) + self.label(e["label"], 0, 7, FS_PK)
        t0, x0, x1 = e["t0"], e["x0"], e["x1"]
        y = LANE_Y
        if e["kind"] == "dropped":
            fr = [(0, {"o": 0, "x": x0, "y": y}), (t0, {"o": 0, "x": x0, "y": y}),
                  (t0 + 0.25, {"o": 1, "x": x0, "y": y}), (t0 + 1.2, {"o": 1, "x": x0, "y": y}),
                  (t0 + 1.5, {"o": 0, "x": x0, "y": y + 26})]
            strike = (f'<g {self.kf([(0, {"o": 0}), (t0 + 0.55, {"o": 0}), (t0 + 0.7, {"o": 1}), (t0 + 1.5, {"o": 1}), (t0 + 1.6, {"o": 0})], "a")}>'
                      f'<line x1="{-w / 2 - 6:.1f}" y1="-26" x2="{w / 2 + 6:.1f}" y2="26" stroke="{C["red"]}" stroke-width="5"/>'
                      f'<text x="0" y="-34" class="sans" font-size="17" font-weight="700" fill="{C["red"]}" text-anchor="middle">{esc(e.get("drop_note", "drop"))}</text></g>')
            a(f'<g {self.kf(fr, "a pk")}>{inner}{strike}</g>')
            return
        ta = e["ta"]
        def at(t):
            return x0 + (x1 - x0) * (t - t0) / e["tr"]
        fr = [(0, {"o": 0, "x": x0, "y": y}), (t0, {"o": 0, "x": x0, "y": y}),
              (t0 + 0.2, {"o": 1, "x": at(t0 + 0.2), "y": y}), (ta, {"o": 1, "x": x1, "y": y})]
        if e["kind"] == "fake":
            fr += [(ta + 0.35, {"o": 0, "x": x1, "y": y + 30})]
        else:
            fr += [(ta + 0.3, {"o": 0, "x": x1 + (12 if e.get("dir") != "back" else -12), "y": y})]
        a(f'<g {self.kf(fr, "a pk")}>{inner}</g>')

    def render(self):
        s = self.s
        style = (
            ".mono{font-family:ui-monospace,'JetBrains Mono','Cascadia Code','SF Mono',Consolas,'DejaVu Sans Mono',monospace}"
            ".sans{font-family:Onest,Inter,system-ui,-apple-system,'Segoe UI',Roboto,'Noto Sans','DejaVu Sans',sans-serif}"
            f".a{{animation-duration:{self.T}s;animation-timing-function:linear;animation-iteration-count:infinite;animation-fill-mode:both}}"
            "@media (prefers-reduced-motion:reduce){.a{animation:none!important}.pk{display:none}}"
        )
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
            f'<title id="t">{esc(s["title"])}</title>',
            f'<desc id="d">{esc(s["desc"])}</desc>',
            "<style>" + style + "".join(self.css) + "</style>",
        ]
        out += self.body
        out.append("</svg>")
        return "\n".join(out) + "\n"


def P(text, n, cut=None, **kw):
    d = {"text": text, "n": n}
    if cut:
        d["cut"] = cut
    d.update(kw)
    return d


def pk(text, part=None, kind="real", chip=None, fills=None, **kw):
    col = PART_COL.get(part, C["ink"])
    lab = [(CIRC[part] + " ", col), (text, C["ink"] if kind != "fake" else C["mut"])] if part else [(text, C["ink"] if kind != "fake" else C["mut"])]
    e = {"label": kw.pop("label", lab), "part": part, "kind": kind, "fills": fills}
    if chip is not None:
        e["chip"] = chip
    e.update(kw)
    return e


def chipc(part, fake=False, text=None):
    col = C["mut"] if fake else PART_COL.get(part, C["ink"])
    return [(text or CIRC[part], col)]


LEG_FAKE = "сплошная рамка — настоящие данные · пунктир — фейк, который сервер отбросит"
LEG_REAL = "каждый пакет — настоящий кусок того же ClientHello, фейков нет"

SPECS = {}

SPECS["multisplit"] = dict(
    name="multisplit", subtitle="режем по порядку",
    cmd="--payload=tls_client_hello --lua-desync=multisplit:pos=1,midsld",
    parts=[P("16", 1, cut="pos=1"), P("03 01 … SNI you", 2, cut="midsld"), P("tube.com …", 3)],
    events=[pk("16", 1, chip=chipc(1), fills=1), pk("… you", 2, chip=chipc(2, text="② …you"), fills=2),
            pk("tube.com …", 3, chip=chipc(3, text="③ tube.com…"), fills=3)],
    slots=[{"text": "16", "n": 1}, {"text": "… you", "n": 2}, {"text": "tube.com …", "n": 3}],
    dpi_verdict=["имя youtube.com разрезано", "между пакетами — сигнатура", "не нашлась, соединение идёт"],
    result="собрано: … youtube.com … ✓",
    legend=LEG_REAL,
    title="multisplit: ClientHello разрезан на три TCP-сегмента",
    desc="Анимация: Zapret 2 режет TLS ClientHello по позициям 1 и midsld на три сегмента и отправляет их по порядку. ТСПУ видит имя youtube.com разрезанным между пакетами и не находит сигнатуру, сервер собирает поток целиком.",
)


M = C["mut"]
RED = C["red"]
AMB = C["amb"]
INK = C["ink"]


def fk(text, part=None, chip=None, **kw):
    """Фейк: пунктирная рамка, серый текст."""
    return pk(text, part, kind="fake", chip=chip, **kw)


# ── fake ───────────────────────────────────────────────────────────
SPECS["fake"] = dict(
    name="fake", subtitle="сначала подсунуть подделку",
    cmd="--payload=tls_client_hello --lua-desync=fake:blob=fake_default_tls:tcp_md5",
    parts=[P("ClientHello · SNI youtube.com", 1)],
    events=[fk("фейк · SNI www.w3.org", label=[("фейк · SNI www.w3.org", M)], chip=[("SNI www.w3.org", M)]),
            pk("SNI youtube.com", 1, chip=[("SNI youtube.com", C["cy"])], fills=1)],
    slots=[{"text": "ClientHello · youtube.com", "n": 1}],
    dpi_verdict=["первым прочитал фейк с www.w3.org", "и мог решить, что поток разрешён —", "настоящий пакет идёт следом"],
    srv_notes=[{"t": "fake", "text": "фейк: неверная подпись tcp_md5", "col": RED},
               {"t": "fake", "text": "→ отброшен, настоящий принят", "col": RED}],
    result="собрано: только настоящий ✓",
    legend=LEG_FAKE,
    title="fake: поддельный ClientHello перед настоящим",
    desc="Анимация: перед настоящим ClientHello с именем youtube.com Zapret 2 отправляет фейк с именем www.w3.org и испорченной подписью tcp_md5. ТСПУ читает фейк первым, сервер его отбрасывает и принимает только настоящий пакет.",
)

# ── multidisorder ──────────────────────────────────────────────────
SPECS["multidisorder"] = dict(
    name="multidisorder", subtitle="режем и шлём с конца",
    cmd="--payload=tls_client_hello --lua-desync=multidisorder:pos=midsld",
    parts=[P("16 03 01 … SNI you", 1, cut="midsld"), P("tube.com …", 2)],
    events=[pk("tube.com …", 2, chip=chipc(2, text="② tube.com…"), fills=2),
            pk("16 03 01 … you", 1, chip=chipc(1, text="① …you"), fills=1)],
    slots=[{"text": "16 03 01 … you", "n": 1}, {"text": "tube.com …", "n": 2}],
    dpi_verdict=["конец пришёл раньше начала,", "а поток задом наперёд DPI", "обычно не пересобирает"],
    srv_notes=[{"t": 0, "text": "② пришёл первым — ждёт в буфере", "col": C["dim"]},
               {"t": 1, "text": "① встал перед ним по номеру seq", "col": C["dim"]}],
    result="собрано: … youtube.com … ✓",
    legend="части настоящие, но уходят в обратном порядке: сначала ②, потом ①",
    title="multidisorder: части ClientHello в обратном порядке",
    desc="Анимация: Zapret 2 режет ClientHello по позиции midsld на две части и отправляет сначала вторую, потом первую. ТСПУ получает поток задом наперёд, сервер расставляет части по номерам и собирает ClientHello целиком.",
)

# ── multidisorder_legacy ───────────────────────────────────────────
SPECS["multidisorder_legacy"] = dict(
    name="multidisorder_legacy", subtitle="с конца, но внутри пакета",
    cmd="--lua-desync=multidisorder_legacy:pos=200,600   (ClientHello 800 байт = пакеты A 500 + B 300)",
    bar_title="ClientHello в двух пакетах:",
    parts=[P("A1 0–199", 1, cut="200"), P("A2 200–499", 2, pkt_edge=True), P("B1 500–599", 3, cut="600"), P("B2 600–799", 4)],
    events=[pk("A2", 2, chip=chipc(2, text="② A2"), fills=2), pk("A1", 1, chip=chipc(1, text="① A1"), fills=1),
            pk("B2", 4, chip=chipc(4, text="④ B2"), fills=4), pk("B1", 3, chip=chipc(3, text="③ B1"), fills=3)],
    slots=[{"text": "A1", "n": 1}, {"text": "A2", "n": 2}, {"text": "B1", "n": 3}, {"text": "B2", "n": 4}],
    dpi_verdict=["в каждом пакете конец", "пришёл раньше начала,", "а A по-прежнему раньше B"],
    srv_notes=[{"t": 3, "text": "границы пакетов A и B сохранены", "col": C["dim"]}],
    result="собрано: A1 A2 B1 B2 ✓",
    legend="обратный порядок — только внутри каждого исходного пакета (A, затем B)",
    title="multidisorder_legacy: обратный порядок внутри каждого пакета",
    desc="Анимация: ClientHello занимает два пакета A и B. multidisorder_legacy режет каждый пакет отдельно и отправляет части задом наперёд внутри пакета: A2, A1, затем B2, B1. Сервер собирает A1 A2 B1 B2.",
)

# ── fakedsplit / fakeddisorder ─────────────────────────────────────
GARB = "▒▒▒▒▒▒"
def _faked(order):
    ev = []
    for part in order:
        real_text = "16 03 01 … you" if part == 1 else "tube.com …"
        ev += [fk(GARB, part, chip=chipc(part, text=CIRC[part])),
               pk(real_text, part, chip=chipc(part, text=CIRC[part]), fills=part),
               fk(GARB, part, chip=chipc(part, text=CIRC[part]))]
    return ev

_FD_COMMON = dict(
    parts=[P("16 03 01 … SNI you", 1, cut="midsld"), P("tube.com …", 2)],
    slots=[{"text": "16 03 01 … you", "n": 1}, {"text": "tube.com …", "n": 2}],
    dpi_blind=True,
    srv_notes=[{"t": "fake", "text": "фейки: неверный ACK (tcp_ack=-66000)", "col": RED},
               {"t": "fake", "text": "→ отброшены, настоящие части приняты", "col": RED}],
    result="собрано: … youtube.com … ✓",
    legend=LEG_FAKE,
)
SPECS["fakedsplit"] = dict(
    _FD_COMMON, name="fakedsplit", subtitle="каждая часть в окружении фейков",
    cmd="--payload=tls_client_hello --lua-desync=fakedsplit:pos=midsld:tcp_ack=-66000:tcp_ts_up",
    events=_faked([1, 2]),
    dpi_verdict=["каждая часть пришла трижды", "с одним и тем же seq — какая", "копия настоящая, не понять"],
    title="fakedsplit: части ClientHello вперемешку с фейками",
    desc="Анимация: Zapret 2 режет ClientHello по midsld на две части и окружает каждую фейком того же размера и с тем же seq: фейк, часть 1, фейк, фейк, часть 2, фейк. ТСПУ видит по три копии каждой части, сервер отбрасывает фейки по неверному ACK.",
)
SPECS["fakeddisorder"] = dict(
    _FD_COMMON, name="fakeddisorder", subtitle="фейки + обратный порядок",
    cmd="--payload=tls_client_hello --lua-desync=fakeddisorder:pos=midsld:tcp_ack=-66000:tcp_ts_up",
    events=_faked([2, 1]),
    dpi_verdict=["по три копии каждой части,", "да ещё конец раньше начала —", "DPI не знает, что собирать"],
    title="fakeddisorder: фейки и обратный порядок частей",
    desc="Анимация: Zapret 2 режет ClientHello по midsld на две части и отправляет сначала вторую, потом первую, окружая каждую фейками с тем же seq. ТСПУ видит копии задом наперёд, сервер отбрасывает фейки и собирает ClientHello.",
)

# ── hostfakesplit ──────────────────────────────────────────────────
SPECS["hostfakesplit"] = dict(
    name="hostfakesplit", subtitle="режем точно по имени сайта",
    cmd="--payload=tls_client_hello --lua-desync=hostfakesplit:tcp_md5",
    parts=[P("16 03 01 … SNI", 1, cut="host"), P("youtube.com", 2, cut="endhost"), P("…", 3)],
    events=[pk("… SNI", 1, chip=[("… SNI", INK)], fills=1),
            fk("u9a7bk2.org", label=[("u9a7bk2.org", M)], chip=[("u9a7bk2.org", INK)]),
            pk("youtube.com", 2, chip=[("youtube.com", INK)], fills=2),
            fk("u9a7bk2.org", label=[("u9a7bk2.org", M)], chip=[("u9a7bk2.org", INK)]),
            pk("…", 3, chip=[("…", INK)], fills=3)],
    dpi_blind=True,
    slots=[{"text": "… SNI", "n": 1}, {"text": "youtube.com", "n": 2}, {"text": "…", "n": 3}],
    dpi_verdict=["на месте имени — три кандидата", "одной длины: какой настоящий?"],
    srv_notes=[{"t": "fake", "text": "фейки: неверная подпись tcp_md5", "col": RED},
               {"t": "fake", "text": "→ отброшены, имя собрано верно", "col": RED}],
    result="собрано: … youtube.com … ✓",
    legend=LEG_FAKE,
    title="hostfakesplit: имя сайта в окружении фейковых имён",
    desc="Анимация: Zapret 2 режет ClientHello по границам имени youtube.com и отправляет перед и после него фейковое имя u9a7bk2.org той же длины. ТСПУ видит несколько имён на одном месте потока, сервер отбрасывает фейки по неверной подписи tcp_md5.",
)

# ── tcpseg ─────────────────────────────────────────────────────────
SPECS["tcpseg"] = dict(
    name="tcpseg", subtitle="сегмент с лишним байтом спереди",
    cmd="--lua-desync=tcpseg:pos=0,-1:seqovl=1 --lua-desync=drop",
    parts=[P("16 03 01 … SNI youtube.com …", 1)],
    events=[pk("16 03 01 … youtube.com", 1, kind="dropped", drop_note="drop: оригинал не уйдёт", gap=1.7),
            pk("", 1, label=[("▒", AMB), (" 16 03 01 … youtube.com", INK)], chip=[("▒", AMB), (" 16 03 01 …", INK)], fills=1)],
    slots=[{"text": "16 03 01 … youtube.com", "n": 1}],
    dpi_verdict=["поток начинается с лишнего", "байта ▒ — разбор ClientHello", "может сбиться"],
    srv_notes=[{"t": 1, "text": "▒ лежит левее окна TCP → отрезан", "col": AMB}],
    result="собрано: ClientHello целиком ✓",
    legend="▒ — байт seqovl: seq сдвинут на 1 назад, сервер его отрежет",
    title="tcpseg: ClientHello одним сегментом с seqovl",
    desc="Анимация: второй инстанс drop выбрасывает оригинальный пакет, а tcpseg отправляет вместо него тот же ClientHello с одним лишним байтом спереди (seqovl=1). ТСПУ видит поток, начинающийся с мусора, сервер отрезает байт левее окна TCP.",
)

# ── oob ────────────────────────────────────────────────────────────
SPECS["oob"] = dict(
    name="oob", subtitle="байт «срочных данных» в имени",
    cmd="--in-range=-s1 --lua-desync=oob:urp=midsld",
    parts=[P("16 03 01 … SNI you", 1, cut="▮ сюда (urp=midsld)"), P("tube.com …", 1)],
    events=[pk("", None, label=[("SYN · seq−1", INK)], chip=[("SYN", INK)], gap=TRAVEL + 0.2),
            pk("", 1, label=[("… you", INK), ("▮", RED), ("tube.com … URG", INK)], chip=[("you", INK), ("▮", RED), ("tube.com", INK)], fills=1)],
    slots=[{"text": "… youtube.com …", "n": 1}],
    dpi_verdict=["в имени лишний байт:", "you▮tube.com — не youtube.com,", "сигнатура не совпала"],
    srv_notes=[{"t": 0, "text": "SYN: seq на 1 меньше — место под байт", "col": C["dim"]},
               {"t": 1, "text": "▮ помечен URG — вынут из потока", "col": RED}],
    result="собрано: youtube.com ✓",
    legend="▮ — байт Out-of-Band: флаг URG велит стеку сервера вынуть его из данных",
    title="oob: байт срочных данных внутри имени сайта",
    desc="Анимация: oob сдвигает seq в SYN на единицу, а затем вставляет в середину имени youtube.com байт срочных данных с флагом URG. ТСПУ видит испорченное имя, TCP-стек сервера вынимает этот байт и получает исходный ClientHello.",
)

# ── syndata ────────────────────────────────────────────────────────
SPECS["syndata"] = dict(
    name="syndata", subtitle="данные прямо в SYN",
    cmd="--lua-desync=syndata:blob=fake_default_tls",
    server="youtube.com",
    bar_title="первый пакет соединения:",
    fake_flash=False,
    parts=[P("SYN", None), P("+ фейковый ClientHello из blob", None)],
    events=[fk("", label=[("SYN + ", INK), ("фейк www.w3.org", M)], chip=[("SYN + www.w3.org", M)], gap=TRAVEL + 0.2),
            pk("", None, label=[("SYN-ACK", INK)], dir="back", nodpi=True, gap=TRAVEL + 0.2),
            pk("SNI youtube.com", 1, chip=[("SNI youtube.com", C["cy"])], fills=1)],
    slots=[{"text": "ClientHello · youtube.com", "n": 1}],
    dpi_verdict=["мог принять данные из SYN", "за начало потока — и уже не", "искать имя в настоящем"],
    srv_notes=[{"t": 0, "text": "SYN принят, данные из него", "col": C["dim"]},
               {"t": 0, "text": "большинство стеков отбрасывает", "col": C["dim"]}],
    result="соединение установлено ✓",
    legend="пунктир — фейковые данные, приклеенные к первому пакету соединения (SYN)",
    title="syndata: фейковые данные в SYN-пакете",
    desc="Анимация: syndata добавляет в первый пакет соединения SYN фейковый ClientHello с именем www.w3.org. Сервер отвечает SYN-ACK и отбрасывает данные из SYN, а ТСПУ может принять их за начало потока. Затем уходит настоящий ClientHello.",
)


def main():
    """python3 scripts/desync-anim.py [папка] [техника ...] — по умолчанию все в Zapret2/desync/attachments."""
    root = Path(__file__).resolve().parent.parent
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "Zapret2/desync/attachments"
    out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[2:] or list(SPECS)
    for n in names:
        svg = Svg(SPECS[n]).build()
        p = out / f"desync-anim-{n}.svg"
        p.write_text(svg, encoding="utf-8")
        print(p, len(svg))


if __name__ == "__main__":
    main()
