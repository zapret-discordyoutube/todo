#!/usr/bin/env python3
"""Общие построители схем для wiki-anim.py: цепочка, стек, диаграмма последовательности,
сравнение двух вариантов, раскладка полей. Схема описывается данными; текст берётся из
заметки, которую схема заменяет. Используется через build(hub, wrapped)."""
import textwrap


def build(hub, wrapped):
    Fig = hub.Fig
    figs = {}

    def reg(name, folder):
        def deco(fn):
            figs[name] = (fn, folder)
            return fn
        return deco

    def wrap(txt, n):
        return textwrap.wrap(txt, n) or [""]

    # ── цепочка блоков ──────────────────────────────────────────────
    def chain(name, title, desc, items, folder, edges=None, vertical=False, accent=(), warn=(), foot=None, lw=430):
        n = len(items)
        edges = edges or {}
        T = n * 1.3 + 3.5
        if not vertical:
            gap = 36
            bw = (956 - (n - 1) * gap) / n
            f = Fig(name, 200 + (28 if edges else 0) + (34 if foot else 0), T, title, desc)
            cpl = max(10, int(bw / 8.6))
            for k, (a, b) in enumerate(items):
                x = 2 + k * (bw + gap)
                kind = "bxr" if k in warn else ("bxa" if k in accent else "bx")
                t = 0.4 + k * 1.2
                inner = f.rect(x, 20, bw, 130, kind, rx=8)
                lines = wrap(a, cpl)
                for j, ln in enumerate(lines):
                    inner += f.text(x + bw / 2, 46 + j * 19, ln, ("rej tk sm c" if k in warn else "tk sm c"))
                base = 46 + len(lines) * 19 + 6
                for j, ln in enumerate(wrap(b, cpl + 2)[:4]):
                    inner += f.text(x + bw / 2, base + j * 17, ln, "mu sm c")
                f.g(inner, f.vis(t, dy=8, fade=0.3))
                if k < n - 1:
                    f.g(f.arrow(x + bw + 4, 85, x + bw + gap - 4, 85, "f"), f.vis(t + 0.4, fade=0.2))
                    if k in edges:
                        f.g(wrapped(f, x + bw + gap / 2 - 60, 176, edges[k], "mu sm", 16, 17), f.vis(t + 0.5, fade=0.2))
            if foot:
                f.g(wrapped(f, 2, f.H - 16, foot, "tk sm", 98, 18), f.vis(T - 2.2))
            return f
        rh, gap = 54, 24
        H = 14 + n * (rh + gap) + (30 if foot else 0)
        f = Fig(name, H, T, title, desc)
        for k, (a, b) in enumerate(items):
            y = 10 + k * (rh + gap)
            kind = "bxr" if k in warn else ("bxa" if k in accent else "bx")
            t = 0.4 + k * 1.2
            inner = f.rect(2, y, lw, rh, kind, rx=8)
            lines = wrap(a, int((lw - 20) / 8.8))
            top = y + rh / 2 + 5 - 9 * (len(lines) - 1)
            inner += "".join(f.text(16, top + j * 18, ln, ("rej tk sm" if k in warn else "tk sm")) for j, ln in enumerate(lines))
            if b:
                bl = wrap(b, int((950 - lw - 24) / 9.3))
                btop = y + rh / 2 + 5 - 9 * (len(bl) - 1)
                inner += "".join(f.text(lw + 24, btop + j * 18, ln, "mu sm") for j, ln in enumerate(bl))
            f.g(inner, f.vis(t, dx=-10, fade=0.3))
            if k < n - 1:
                f.g(f.arrow(lw / 2, y + rh + 2, lw / 2, y + rh + gap - 2, "f"), f.vis(t + 0.4, fade=0.2))
        if foot:
            f.g(wrapped(f, 2, H - 8, foot, "tk sm", 98, 18), f.vis(T - 2.0))
        return f

    # ── стек инкапсуляции ───────────────────────────────────────────
    def stack(name, title, desc, layers, folder, foot=None, accent=()):
        n = len(layers)
        T = n * 1.3 + 3.5
        LH = 54
        H = 20 + n * LH + 24 + (30 if foot else 0)
        f = Fig(name, H, T, title, desc)
        for k, (a, b) in enumerate(layers):
            x, y = 2 + k * 26, 14 + k * LH
            w = 520 - k * 52
            h = (n - k) * LH - 6 + 4
            kind = "bxa" if k in accent else "bx"
            t = 0.4 + k * 1.2
            f.g(f.rect(x, y, w, h, kind, rx=8) + f.text(x + 14, y + 26, a, "tk sm"), f.vis(t, fade=0.3))
            f.g(wrapped(f, 560, y + 24, b, "mu sm", 46, 18), f.vis(t + 0.2, dx=8, fade=0.3))
        if foot:
            f.g(wrapped(f, 2, H - 10, foot, "tk sm", 98, 18), f.vis(T - 2.0))
        return f

    # ── диаграмма последовательности ────────────────────────────────
    def seq(name, title, desc, actors, steps, folder, foot=None, aw=190):
        n = len(actors)
        xs = [aw / 2 + 2 + k * ((956 - aw) / (n - 1)) for k in range(n)] if n > 1 else [480]
        T = len(steps) * 1.5 + 3.5
        RH = 72
        H = 84 + len(steps) * RH + (36 if foot else 14)
        f = Fig(name, H, T, title, desc)
        for k, (a, b) in enumerate(actors):
            x = xs[k]
            f.add(f.line(x, 66, x, H - (36 if foot else 14), "lfd"))
            f.add(f.rect(x - aw / 2, 8, aw, 54, "bx"))
            f.add(f.text(x, 32, a, "tk c sm"))
            f.add(f.text(x, 50, b, "mu sm c"))
        for j, (src, dst, lab, sub, kind) in enumerate(steps):
            y = 100 + j * RH
            t = 0.5 + j * 1.5
            x1, x2 = xs[src], xs[dst]
            d = 1 if x2 > x1 else -1
            if lab:
                f.g(f.text((x1 + x2) / 2, y - 8, lab, "mk sm c"), f.vis(t))
            f.add(f.arrow(x1 + 4 * d, y, x2 - 4 * d, y, kind, t=t, dur=0.5))
            if sub:
                f.g(wrapped(f, min(x1, x2) + 8, y + 20, sub, "mu sm", int(abs(x2 - x1) / 8.2), 17), f.vis(t + 0.5))
        if foot:
            f.g(wrapped(f, 2, H - 10, foot, "tk sm", 98, 18), f.vis(T - 2.2))
        return f

    # ── сравнение двух вариантов ────────────────────────────────────
    def compare(name, title, desc, left, right, folder, foot=None, lk="bxr", rk="bxa"):
        T = 12
        rows = max(len(left[1]), len(right[1]))
        H = 70 + rows * 40 + (34 if foot else 20)
        f = Fig(name, H, T, title, desc)
        for side, (head, lines), kind, x in ((0, left, lk, 2), (1, right, rk, 490)):
            t0 = 0.5 + side * 3.0
            col = "rej" if kind == "bxr" else "acc"
            f.g(f.rect(x, 8, 466, H - 8 - (34 if foot else 12), kind, rx=10) + f.text(x + 16, 38, head, col + " tk"), f.vis(t0, fade=0.3))
            for k, ln in enumerate(lines):
                f.g(wrapped(f, x + 16, 74 + k * 40, ln, "sm", 52, 17), f.vis(t0 + 0.5 + k * 0.5, fade=0.25))
        if foot:
            f.g(wrapped(f, 2, H - 8, foot, "tk sm", 98, 18), f.vis(T - 2.5))
        return f

    # ── раскладка полей ─────────────────────────────────────────────
    def fields(name, title, desc, rows, folder, foot=None, W=900, minw=26):
        """rows: [(заголовок, [(метка, размер, пояснение или '')], итог)]; размер в байтах, ширина пропорциональна."""
        RH = 164
        T = len(rows) * 3.0 + 3.0
        H = 16 + len(rows) * RH + (34 if foot else 8)
        f = Fig(name, H, T, title, desc)
        for r, (head, flds, total) in enumerate(rows):
            flds = [tuple(x) + ("",) * (3 - len(x)) for x in flds]
            y = 18 + r * RH
            t0 = 0.4 + r * 3.0
            f.g(f.text(2, y + 4, head, "tk sm") + (f.text(950, y + 4, total, "mk acc sm r") if total else ""), f.vis(t0, fade=0.3))
            nom = [(s[0] if isinstance(s, tuple) else s) for _, s, _ in flds]
            tot = sum(max(v, 0.0001) for v in nom)
            ws = [max(minw, v / tot * W) for v in nom]
            k = sum(ws) / W
            ws = [w / k for w in ws]
            x = 30
            for j, ((lab, size, note), w) in enumerate(zip(flds, ws)):
                t = t0 + 0.2 + j * 0.25
                cls = "bxa" if j % 2 == 0 else "bx"
                inner = f.rect(x, y + 16, w - 2, 34, cls, rx=4) + f.text(x + w / 2 - 1, y + 38, (size[1] if isinstance(size, tuple) else (str(int(size)) if size == int(size) and size else "")), "mk c sm")
                ly = y + 68 + (j % 3) * 28
                half = len(lab) * 4.6
                lx = min(max(x + w / 2, half + 2), 958 - half)
                inner += f.line(x + w / 2, y + 50, x + w / 2, ly - 14, "lm")
                inner += f.text(lx, ly, lab, "tk sm c")
                f.g(inner, f.go([(0, -14, 0, 0), (t, -14, 0, 0), (t + 0.15, -14, 0, 1), (t + 0.5, 0, 0, 1)]))
                x += w
        if foot:
            f.g(wrapped(f, 2, H - 10, foot, "mu sm", 98, 18), f.vis(T - 2.0))
        return f

    return figs, dict(chain=chain, stack=stack, seq=seq, compare=compare, fields=fields, reg=reg)
