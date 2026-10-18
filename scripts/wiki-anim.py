#!/usr/bin/env python3
"""Анимированные схемы для разделов вики вне Zapret2/desync.

Запуск: python3 scripts/wiki-anim.py [схема ...] — по умолчанию все.
Схема попадает в attachments своего раздела как wiki-anim-<имя>.svg; плагин
InlineAnimSvg сайта встраивает её inline и красит темой Quartz (см.
scripts/desync-hub-anim.py — там же класс Fig и все приёмы анимации).
"""
import importlib.util
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("hub", ROOT / "scripts" / "desync-hub-anim.py")
hub = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hub)
Fig = hub.Fig


def wrapped(f, x, y, txt, cls, width=88, lh=22):
    """Текст в несколько строк: SVG сам строки не переносит."""
    return "".join(f.text(x, y + k * lh, ln, cls) for k, ln in enumerate(textwrap.wrap(txt, width)))


# ═══ Z2: путь пакета через nfqws2 ═════════════════════════════════════
def fig_z2_pipeline():
    f = Fig("z2-pipeline", 470, 17, "Путь пакета через nfqws2",
            "Пакет проходит перехват в ядре ОС, диссекцию, conntrack, определение типа пейлоада, при необходимости сборку reasm, выбор профиля, "
            "цепочку Lua-инстансов и сведение вердиктов, после чего уходит, изменяется или выбрасывается. Cutoff отключает инстанс от потока.")
    BW, BH, X0, STEP = 170, 86, 5, 195
    row1 = [("Перехват", "в ядре ОС, ранняя", "фильтрация"), ("Диссекция", "пакет → поля ip, tcp,", "udp, payload"),
            ("conntrack", "привязка к потоку:", "направление, счётчики"), ("Тип пейлоада", "TLS ClientHello,", "HTTP, QUIC…"),
            ("reasm / decrypt", "запрос из нескольких", "пакетов собираем")]
    row2 = [("Профиль", "первый совпавший", "по фильтрам; кэш"), ("Инстансы Lua", "--lua-desync строго", "по порядку"),
            ("Вердикты", "PASS · MODIFY · DROP:", "сильнейший побеждает"), ("Итог", "отправить, изменить", "или выбросить")]
    Y1, Y2 = 58, 236
    cx = [X0 + k * STEP + BW / 2 for k in range(5)]
    f.add(f.text(2, 30, "1. разбор пакета", "cap"))
    f.add(f.text(104, 208, "2. решение", "cap"))

    def box(x, y, title, a, b, n, visit):
        f.add(f.rect(x, y, BW, BH, "bx"))
        f.g(f.rect(x, y, BW, BH, "bxa"), f.vis(visit[0], visit[1], fade=0.25))
        f.add(f.text(x + 12, y + 20, str(n), "mu sm"))
        f.add(f.text(x + BW / 2, y + 36, title, "tk c"))
        f.add(f.text(x + BW / 2, y + 58, a, "mu sm c"))
        f.add(f.text(x + BW / 2, y + 75, b, "mu sm c"))

    t = 0.5
    visits = []
    for k in range(9):
        visits.append((t, t + 1.3))
        t += 1.35
    n = 0
    for k, (title, a, b) in enumerate(row1):
        box(X0 + k * STEP, Y1, title, a, b, k, visits[k])
        if k < 4:
            f.add(f.arrow(X0 + k * STEP + BW + 3, Y1 + BH / 2, X0 + (k + 1) * STEP - 3, Y1 + BH / 2, "f"))
    for k, (title, a, b) in enumerate(row2):
        box(X0 + k * STEP, Y2, title, a, b, k + 5, visits[5 + k])
        if k < 3:
            f.add(f.arrow(X0 + k * STEP + BW + 3, Y2 + BH / 2, X0 + (k + 1) * STEP - 3, Y2 + BH / 2, "f"))
    # колено между рядами
    ex = X0 + 4 * STEP + BW / 2
    sx = X0 + BW / 2
    f.add(f'<path class="{f.c("sl-f")}" d="M{ex} {Y1 + BH + 3}V{Y1 + BH + 28}H{sx}V{Y2 - 5}"/>')
    f.add(f.head(sx, Y2 - 3, 1.5708, "f"))
    # cutoff
    f.add(f.rect(X0 + STEP, Y2 + BH + 36, 290, 74, "bxd"))
    f.add(f.text(X0 + STEP + 12, Y2 + BH + 58, "Cutoff", "tk sm"))
    f.add(f.text(X0 + STEP + 12, Y2 + BH + 77, "инстанс отключается от потока:", "mu sm"))
    f.add(f.text(X0 + STEP + 12, Y2 + BH + 94, "лишние пакеты в Lua не идут", "mu sm"))
    f.add(f.arrow(cx[1], Y2 + BH + 3, cx[1], Y2 + BH + 33, "f", ))
    # пакет
    cy1, cy2 = Y1 + BH / 2, Y2 + BH / 2
    pts = []
    for k in range(5):
        pts.append((visits[k][0] + 0.15, cx[k], cy1))
        pts.append((visits[k][1] - 0.2, cx[k], cy1))
    pts.append((visits[4][1] + 0.2, cx[4], Y1 + BH + 28))
    pts.append((visits[4][1] + 0.5, cx[0], Y1 + BH + 28))
    for k in range(4):
        pts.append((visits[5 + k][0] + 0.15, cx[k], cy2))
        pts.append((visits[5 + k][1] - 0.2, cx[k], cy2))
    fr = [(0, f"opacity:0;transform:translate({pts[0][1]}px,{pts[0][2]}px)")]
    for tt, x, y in pts:
        fr.append((tt, f"opacity:1;transform:translate({x}px,{y}px)"))
    last = pts[-1]
    fr.append((last[0] + 0.5, f"opacity:0;transform:translate({last[1]}px,{last[2]}px)"))
    f.g(f.chip(0, 0, 66, 28, "пакет", "bxa", "mk sm"), f.kf(fr, tr=True))
    f.g(f.text(2, 456, "Путь короткий, но почти любой отказ техники случается на одной из ранних стадий — до вызова Lua.", "tk"), f.vis(14.4))
    return f


# ═══ Z2: как выбирается профиль ═══════════════════════════════════════
def fig_z2_profilepick():
    f = Fig("z2-profilepick", 470, 17, "Как движок выбирает профиль: сверху вниз, первый совпавший",
            "Для нового соединения движок проверяет профили сверху вниз и отдаёт соединение первому, у которого совпали все фильтры. "
            "Если не подошёл ни один, соединение достаётся скрытому профилю no_action, который ничего не делает. Выбор кэшируется в conntrack.")
    rows = [("Профиль 1", "Исключения (pass)", "--hostlist=ru-sites.txt"),
            ("Профиль 2", "youtube.com", "--filter-tcp=443  --hostlist=youtube.txt"),
            ("Профиль 3", "Весь TLS", "--filter-tcp=443  --filter-l7=tls"),
            ("№ 0", "no_action (скрытый)", "фильтров нет — совпадает со всем")]
    Y0, RH = 96, 62
    X1, X2 = 2, 560
    f.add(f.text(X1, 30, "профили пресета, пример", "cap"))
    f.add(f.text(X2 + 30, 30, "новое соединение", "cap"))
    for k, (a, b, c) in enumerate(rows):
        y = Y0 + k * RH
        dashed = k == 3
        f.add(f.rect(X1, y, 520, 50, "bxd" if dashed else "bx"))
        f.add(f.text(X1 + 14, y + 22, a, "mu sm"))
        f.add(f.text(X1 + 108, y + 22, b, "tk sm"))
        f.add(f.text(X1 + 14, y + 41, c, "m mu sm"))
    f.add(f.text(X1, Y0 + 4 * RH + 10, "поиск идёт строго по порядку: первое совпадение побеждает, остальные профили не смотрят", "mu sm"))
    scen = [("rutube.ru:443", [0], 0, "достаётся профилю 1: остальные не проверяются"),
            ("youtube.com:443", [1], 1, "профиль 1 не подошёл, профиль 2 подошёл — стоп"),
            ("example.org:443", [2], 2, "профили 1 и 2 не подошли, профиль 3 подошёл — стоп"),
            ("UDP 3478", [], 3, "не подошёл ни один: действий нет, соединение идёт как есть")]
    for si, (name, ok, win, cap) in enumerate(scen):
        t0 = 0.5 + si * 4.0
        t1 = t0 + 3.8
        f.g(f.chip(X2 + 120, 56, 180, 32, name, "bxa", "mk sm"), f.vis(t0, t1))
        for k in range(win + 1):
            y = Y0 + k * RH
            tk = t0 + 0.5 + k * 0.7
            if k < win:
                f.g(f.text(X1 + 540, y + 31, "✕ не подошёл", "rej tk sm"), f.vis(tk, t1, fade=0.2))
            else:
                f.g(f.rect(X1, y, 520, 50, "bxa" if k < 3 else "bx") + f.text(X1 + 540, y + 31, "✓ совпал", "acc tk sm"), f.vis(tk, t1, fade=0.2))
        f.g(f.text(2, 356, cap, "tk"), f.vis(t0 + 1.2 + win * 0.7, t1))
    f.g(wrapped(f, 2, 392, "Выбор запоминается в conntrack и пересматривается не больше двух раз: когда распознан протокол и когда найдено имя сайта.", "t", 88), f.vis(0.2))
    f.g(f.text(2, 456, "Внутри профиля фильтры объединяются через И, значения внутри одного фильтра — через ИЛИ.", "mu sm"), f.vis(0.2))
    return f


# ═══ Z2: circular ═════════════════════════════════════════════════════
def fig_z2_circular():
    f = Fig("z2-circular", 486, 17, "circular: стратегия сменяется после неудачи",
            "Оркестратор circular выполняет только инстансы текущей стратегии. После fails неудач переходит к следующей по формуле (N % total) + 1, "
            "а на стратегии с флагом final ротация останавливается. Состояние хранится для каждого хоста в таблице autostate.")
    strat = [("strategy=1", "multisplit:pos=2"), ("strategy=2", "fake:blob=fake_default_http"), ("strategy=3 · final", "multidisorder:pos=host")]
    X = [20, 345, 670]
    W_, Y, H_ = 270, 120, 86
    f.add(f.text(2, 30, "circular:fails=1:time=300:retrans=3:nld=2", "mk"))
    for k, (a, b) in enumerate(strat):
        f.add(f.rect(X[k], Y, W_, H_, "bx"))
        f.add(f.text(X[k] + 14, Y + 28, a, "tk sm"))
        f.add(f.text(X[k] + 14, Y + 56, "--lua-desync=", "m mu sm"))
        f.add(f.text(X[k] + 14, Y + 74, b, "m sm"))
        win = [(0.4, 5.0), (5.0, 10.0), (10.0, None)][k]
        f.g(f.rect(X[k], Y, W_, H_, "bxa"), f.vis(win[0], win[1], fade=0.3) if win[1] else f.vis(win[0], fade=0.3))
        f.g(f.text(X[k] + W_ - 14, Y - 12, "активна", "acc tk sm r"), f.vis(win[0], win[1], fade=0.3) if win[1] else f.vis(win[0], fade=0.3))
    # переходы
    for k in (0, 1):
        t = 3.0 + k * 5.0
        x1, x2 = X[k] + W_ + 2, X[k + 1] - 2
        f.add(f.arrow(x1, Y + H_ / 2, x2, Y + H_ / 2, "f", t=t + 0.6, dur=0.5, until=None))
        f.g(f.chip((x1 + x2) / 2, Y - 34, 66, 26, "неудача", "bxr", "mk sm rej"), f.vis(t, t + 2.2, fade=0.2))
    f.g(f.text(X[0] + W_ / 2 + 80, Y + H_ + 44, "неудач ≥ fails → следующая:  (N % total) + 1", "m fg sm"), f.vis(3.4, 6.6))
    f.g(f.text(X[0] + W_ / 2 + 80, Y + H_ + 44, "неудач ≥ fails → следующая:  (N % total) + 1", "m fg sm"), f.vis(8.4, 11.6))
    # final
    f.g(f.text(X[2] + W_ / 2, Y + H_ + 36, "final: ротация остановлена", "rej tk c sm"), f.vis(11.4))
    f.g(f'<path class="{f.c("lmd")}" d="M{X[2] + W_ / 2} {Y + H_ + 8}V{Y + H_ + 24}"/>', f.vis(11.0))
    # справочные строки
    notes = [("неудача", "3 ретрансмиссии подряд (retrans=3)"),
             ("ключ хоста", "домен 2-го уровня, например google.com (nld=2)"),
             ("сброс счётчика", "если последняя неудача старше 300 с (time=300)"),
             ("память", "по каждому хосту, в таблице autostate: переживает отдельные соединения")]
    f.add(f.line(2, 296, 950, 296, "lf"))
    for k, (a, b) in enumerate(notes):
        y = 324 + k * 30
        f.g(f.text(2, y, a, "cap") + f.text(180, y, b, "t"), f.vis(0.6 + k * 0.4))
    f.g(wrapped(f, 2, 450, "На каждом пакете выполняются только инстансы с номером текущей стратегии; несколько инстансов одной стратегии идут по порядку.", "mu sm", 98, 19), f.vis(0.2))
    return f


# ═══ Z2: анатомия профиля ═════════════════════════════════════════════
def fig_z2_profile():
    f = Fig("z2-profile", 410, 16, "Анатомия профиля: три роли флагов",
            "Флаги профиля делятся на три роли. Фильтры профиля решают, какие соединения ему достаются; если не совпали — проверяется следующий профиль. "
            "Внутрипрофильные условия решают, к каким пакетам применять стратегию; если не подошли — пакет остаётся в этом профиле, но стратегия его пропускает. "
            "Стратегия — это вызовы --lua-desync по порядку.")
    lines = [("--name=youtube.com (интерфейс)", None, "подпись в GUI и логах, на трафик не влияет"),
             ("--filter-tcp=80,443", 0, None), ("--hostlist=lists/youtube.txt", 0, None),
             ("--out-range=-d8", 1, None), ("--payload=tls_client_hello", 1, None),
             ("--lua-desync=multisplit:pos=1,host+2,…:seqovl=1", 2, None)]
    Y0, LH = 46, 44
    for k, (code, layer, note) in enumerate(lines):
        y = Y0 + k * LH
        f.g(f.text(24, y + 26, code, "m fg"), f.vis(0.3 + k * 0.35, fade=0.25))
        if note:
            f.g(f.text(430, y + 26, note, "mu sm"), f.vis(0.5, fade=0.25))
    layers = [(1, 2, "1. Какие соединения достаются", "не совпало — проверяется следующий профиль", "acc"),
              (3, 4, "2. К каким пакетам применять", "не подошло — пакет остаётся в профиле, стратегия его пропускает", "acc"),
              (5, 5, "3. Что делать", "вызовы по порядку", "acc")]
    for k, (a, b, title, cons, col) in enumerate(layers):
        ya, yb = Y0 + a * LH + 4, Y0 + b * LH + LH - 6
        t = 3.2 + k * 2.4
        x = 420 if k != 1 else 420
        f.g(f.rect(2, ya - 2, 410 if k < 2 else 548, yb - ya + 4, "bxa", rx=8), f.vis(t, fade=0.3))
        f.g(f.line(414 if k < 2 else 560, ya + 2, 414 if k < 2 else 560, yb - 2, "la") +
            f.text(430 if k < 2 else 575, (ya + yb) / 2 - 2, title, "tk sm") +
            wrapped(f, 430 if k < 2 else 575, (ya + yb) / 2 + 18, cons, "mu sm", 46, 18), f.vis(t + 0.2, fade=0.3))
    f.g(wrapped(f, 2, 372, "Условия второй группы в выбор профиля не участвуют: они действуют на идущие после них --lua-desync внутри уже выбранного профиля.", "mu sm", 98, 19), f.vis(10.6))
    return f


# ═══ Z2: out-range, счётчики n и d ════════════════════════════════════
def fig_z2_outrange():
    f = Fig("z2-outrange", 504, 16, "Как считаются пакеты в --out-range: n и d",
            "Счётчик n считает все пакеты нужного направления, счётчик d — только пакеты с данными. SYN и пустой ACK дают d=0, ClientHello — d=1. "
            "--out-range считает только исходящие пакеты, --in-range — только входящие. Ниже — какие d попадают под -d10, d1-d10, d1<d10 и d5-.")
    f.add(f.text(2, 28, "исходящие (--out-range)", "cap"))
    f.add(f.text(520, 28, "входящие (--in-range)", "cap"))
    out = [("SYN", "n=1  d=0", False), ("ACK, пустой", "n=2  d=0", False), ("ClientHello / HTTP", "n=3  d=1", True)]
    for k, (a, b, data) in enumerate(out):
        y = 56 + k * 44
        t = 0.6 + k * 1.1
        f.g(f.rect(2, y, 250, 34, "bxa" if data else "bx", rx=6) + f.text(14, y + 22, a, "tk sm") +
            f.text(250, y + 22, b, "m mu sm r"), f.go([(0, -30, 0, 0), (t, -30, 0, 0), (t + 0.2, -30, 0, 1), (t + 0.8, 0, 0, 1)]))
    f.g(f.rect(520, 56, 250, 34, "bx", rx=6) + f.text(532, 78, "SYN-ACK", "tk sm") + f.text(768, 78, "n=1  d=0", "m mu sm r"),
        f.go([(0, 30, 0, 0), (2.0, 30, 0, 0), (2.2, 30, 0, 1), (2.8, 0, 0, 1)]))
    f.g(f.text(520, 126, "для --out-range не считается:", "mu sm") + f.text(520, 146, "это входящий пакет", "mu sm"), f.vis(3.2))
    f.g(f.text(2, 214, "data-пакет (d) — тот, где есть данные приложения; пустые ACK, FIN и RST d не получают.", "t"), f.vis(4.2))
    # линейка d
    f.add(f.line(2, 250, 950, 250, "lf"))
    f.add(f.text(2, 278, "какие data-пакеты попадают в диапазон", "cap"))
    X0, CW = 170, 56
    for d in range(1, 13):
        f.add(f.text(X0 + (d - 1) * CW + CW / 2, 308, f"d{d}", "mu sm c"))
    rng = [("-d10", 1, 10, "от начала до d10"), ("d1-d10", 1, 10, "с d1 по d10 включительно"),
           ("d1<d10", 1, 9, "с d1 по d9, d10 не входит"), ("d5-", 5, 12, "с d5 и до конца")]
    for k, (name, a, b, cap) in enumerate(rng):
        y = 322 + k * 34
        t = 5.4 + k * 1.2
        f.g(f.text(2, y + 20, name, "mk"), f.vis(t, fade=0.2))
        f.g(f.rect(X0 + (a - 1) * CW + 2, y, (b - a + 1) * CW - 4, 26, "bxa", rx=5) +
            (f.text(X0 + b * CW + 6, y + 18, "…", "mu sm") if name == "d5-" else ""),
            f.go([(0, -20, 0, 0), (t, -20, 0, 0), (t + 0.15, -20, 0, 1), (t + 0.7, 0, 0, 1)]))
    f.g(f.text(2, 488, "winws2 по умолчанию не перехватывает пустые ACK (--wf-tcp-empty=0): n «перескакивает», и условия по n сдвигаются.", "mu sm"), f.vis(10.8))
    return f


# ═══ Z2: зачем fake должен умереть ════════════════════════════════════
def fig_z2_fakedies():
    f = Fig("z2-fakedies", 424, 17, "У фейка две аудитории с противоположными требованиями",
            "Для DPI фейк должен выглядеть настоящим: его нужно успеть разобрать как TLS, HTTP или QUIC. Для сервера он должен быть плохим и умереть. "
            "Fooling — ровно такая порча, которая убивает фейк до сервера, но не мешает DPI. Если фейк дошёл до сервера живым, поток развалится.")
    nodes = {"c": 70, "d": 470, "s": 880}
    lanes = [(110, "фейк с fooling", True), (270, "фейк без fooling", False)]
    for y, name, dies in lanes:
        f.add(f.text(2, y - 56, name, "tk"))
        f.add(f.line(nodes["c"], y, nodes["s"], y, "lm"))
        f.add(f.rect(nodes["c"] - 24, y - 15, 48, 30, "nd", rx=5) + f.text(nodes["c"], y + 5, "клиент", "mk c sm"))
        f.add(f'<polygon class="{f.c("nd")}" points="{nodes["d"] - 20},{y} {nodes["d"] - 10},{y - 15} {nodes["d"] + 10},{y - 15} {nodes["d"] + 20},{y} {nodes["d"] + 10},{y + 15} {nodes["d"] - 10},{y + 15}"/>')
        f.add(f.text(nodes["d"], y + 5, "DPI", "mk c sm"))
        f.add(f.rect(nodes["s"] - 28, y - 15, 56, 30, "nd", rx=5) + f.text(nodes["s"], y + 5, "сервер", "mk c sm"))
    # линия 1: фейк умирает
    t0 = 0.8
    f.g(f.chip(nodes["s"] - 70, 80, 56, 24, "фейк", "bxd", "mk sm"),
        f.go([(0, nodes["c"] - nodes["s"] + 70, 0, 0), (t0, nodes["c"] - nodes["s"] + 70, 0, 0), (t0 + 0.2, nodes["c"] - nodes["s"] + 70, 0, 1),
              (t0 + 2.2, nodes["d"] - nodes["s"] + 70, 0, 1), (t0 + 4.0, 0, 0, 1)]))
    f.g(f'<circle class="{f.c("ring")}" cx="{nodes["d"]}" cy="110" r="28"/>', f.vis(t0 + 2.0, t0 + 3.6, fade=0.25))
    f.g(f.text(nodes["d"], 156, "разобрал: безобидный SNI", "acc tk c sm"), f.vis(t0 + 2.2, fade=0.25))
    f.g(f.chip(nodes["s"] - 70, 80, 76, 24, "фейк ✕", "bxr", "mk sm rej"), f.vis(t0 + 4.2, fade=0.2))
    f.g(f.text(950, 156, "до сервера не доходит или отброшен", "rej tk r sm"), f.vis(t0 + 4.4))
    # линия 2: фейк жив
    t1 = 7.2
    f.g(f.chip(nodes["s"] - 70, 240, 56, 24, "фейк", "bxd", "mk sm"),
        f.go([(0, nodes["c"] - nodes["s"] + 70, 0, 0), (t1, nodes["c"] - nodes["s"] + 70, 0, 0), (t1 + 0.2, nodes["c"] - nodes["s"] + 70, 0, 1),
              (t1 + 2.2, nodes["d"] - nodes["s"] + 70, 0, 1), (t1 + 4.0, 0, 0, 1)]))
    f.g(f.text(950, 296, "сервер принял фейк как часть потока", "rej tk r sm"), f.vis(t1 + 4.2))
    f.g(f.chip(nodes["s"] - 70, 330, 90, 24, "настоящий", "bxa", "mk sm"), f.go([(0, -300, 0, 0), (t1 + 5.0, -300, 0, 0), (t1 + 5.2, -300, 0, 1), (t1 + 6.4, 0, 0, 1)]))
    f.g(f.text(950, 372, "TLS или HTTP развалился", "rej tk r sm"), f.vis(t1 + 6.6))
    f.g(f.text(2, 404, "Поэтому «фейк не дошёл до сервера» — не побочный эффект, а обязательное условие.", "tk"), f.vis(14.2))
    return f


# ═══ Z2: ловушка F5 ═══════════════════════════════════════════════════
def fig_z2_f5():
    f = Fig("z2-f5", 452, 16, "Почему F5 не показывает новую стратегию",
            "После смены стратегии F5 шлёт запрос по уже открытому keep-alive соединению, нового SYN нет. Дурение работает только при установке соединения, "
            "а ТСПУ помнит старое соединение как плохое. Чтобы браузер открыл новое соединение, нужны Ctrl+F5, новая вкладка, режим инкогнито или перезапуск браузера.")
    steps = ["Меняю стратегию на рабочую", "Жму F5", "Браузер шлёт запрос по уже открытому соединению: нового SYN нет",
             "Новая стратегия работает только при установке соединения — здесь не применяется",
             "ТСПУ помнит это соединение как плохое и продолжает блокировать", "Сайт «не открывается», хотя стратегия уже рабочая"]
    X, W_, RH = 2, 520, 56
    f.add(f.text(X, 28, "что происходит", "cap"))
    for k, txt in enumerate(steps):
        y = 44 + k * 62
        last = k == len(steps) - 1
        t = 0.5 + k * 1.3
        lines = textwrap.wrap(txt, 50)
        cls = "rej tk sm" if last else "tk sm"
        inner = f.rect(X, y, W_, RH, "bxr" if last else "bx")
        inner += f'<circle class="{f.c("nd")}" cx="{X + 20}" cy="{y + RH / 2}" r="12"/>' + f.text(X + 20, y + RH / 2 + 5, str(k + 1), "mk c sm")
        base = y + RH / 2 + 5 - 10 * (len(lines) - 1)
        for j, ln in enumerate(lines):
            inner += f.text(X + 42, base + j * 19, ln, cls)
        f.g(inner, f.vis(t, dy=8))
    f.add(f.text(580, 28, "как получить новое соединение", "cap"))
    ladder = [("Ctrl+F5", "чаще, но без гарантии", 1), ("Новая вкладка", "лучше — закрыв старую", 2),
              ("Инкогнито", "отдельный контекст и пустой кэш", 3), ("Закрыть браузер совсем", "самое надёжное", 4)]
    for k, (a, b, lvl) in enumerate(ladder):
        y = 48 + k * 74
        t = 4.4 + k * 1.2
        f.g(f.rect(580, y, 60 + lvl * 62, 48, "bxa", rx=6) + f.text(594, y + 21, a, "tk sm") + f.text(594, y + 40, b, "mu sm"),
            f.go([(0, -40, 0, 0), (t, -40, 0, 0), (t + 0.2, -40, 0, 1), (t + 0.8, 0, 0, 1)]))
    f.g(f.text(580, 362, "чем длиннее полоса, тем надёжнее способ", "mu sm"), f.vis(9.4))
    f.g(f.text(2, 436, "Для приложений (Discord, игры) то же правило: закрыть целиком, вплоть до трея.", "mu"), f.vis(10.4))
    return f


# ═══ DPI: три условия триггера ТСПУ ═══════════════════════════════════
def fig_dpi_gates():
    f = Fig("dpi-gates", 486, 18, "Блокировка включается, только если совпали все три условия",
            "ТСПУ оценивает ClientHello по трём косвенным признакам: маршрут, TLS-отпечаток, поведение. Если совпали все три — заморозка всех TLS-соединений к узлу на 120 секунд. "
            "Достаточно сломать любое одно условие: другой отпечаток (Firefox), HTTP/2 вместо лавины соединений или сайт вне подозрительной подсети.")
    gates = [("1. Маршрут", "IP в подсети или AS дата-центра под анализом", "увести сайт из такой подсети"),
             ("2. Отпечаток", "JA3/JA4: Chrome, Safari, iOS под фильтром", "другой отпечаток: Firefox, Edge"),
             ("3. Поведение", "больше 3 TLS-сессий к одному SNI за 60 с, пауза меньше 20–50 мс", "HTTP/2: одно соединение вместо лавины")]
    GX, GW, GY, GH = [176, 392, 608], 190, 96, 64
    f.add(f.text(2, 28, "соединение с ClientHello", "cap"))
    for k, (a, b, fix) in enumerate(gates):
        x = GX[k]
        f.add(f.rect(x, GY, GW, GH, "bx"))
        f.add(f.text(x + GW / 2, GY + 38, a, "tk c"))
        f.add(wrapped(f, x + 6, GY + GH + 28, b, "mu sm", 23, 18))
        f.add(f.text(x + 6, GY + GH + 112, "как сломать условие:", "cap"))
        f.add(wrapped(f, x + 6, GY + GH + 136, fix, "acc tk sm", 23, 18))
        if k < 2:
            f.add(f.arrow(x + GW + 3, GY + GH / 2, GX[k + 1] - 3, GY + GH / 2, "f"))
    f.add(f.arrow(GX[2] + GW + 3, GY + GH / 2, 818, GY + GH / 2, "f"))
    f.add(f.arrow(142, GY + GH / 2, GX[0] - 3, GY + GH / 2, "f"))
    scen = [("Chrome", [True, True, True], 0.4, 8.6, False), ("Firefox", [True, False, True], 9.0, 17.2, True)]
    for name, cond, t0, t1, ok in scen:
        cy = GY + GH / 2
        f.g(f.chip(78, cy, 110, 32, name, "bxa", "mk sm"), f.vis(t0, t1, fade=0.2))
        last = 3
        for k in range(3):
            tk = t0 + 0.9 + k * 1.5
            lab, cls = ("да", "rej tk c") if cond[k] else ("нет", "acc tk c")
            f.g(f.text(GX[k] + GW / 2, GY - 10, lab, cls), f.vis(tk, t1, fade=0.2))
            if cond[k]:
                f.g(f.rect(GX[k], GY, GW, GH, "bxr"), f.vis(tk, t1, fade=0.2))
            else:
                f.g(f.rect(GX[k], GY, GW, GH, "bxa"), f.vis(tk, t1, fade=0.2))
                last = k
                break
        te = t0 + 0.9 + (3 if all(cond) else last + 1) * 1.5
        if all(cond):
            f.g(f.rect(818, GY - 24, 140, GH + 48, "bxr") + f.text(888, GY + 12, "заморозка", "rej tk c sm") +
                f.text(888, GY + 34, "всех TLS к узлу", "rej sm c") + f.text(888, GY + 54, "на 120 секунд", "rej sm c"), f.vis(te, t1, fade=0.3))
        else:
            f.g(f.rect(818, GY - 24, 140, GH + 48, "bxa") + f.text(888, GY + 12, "условие не", "acc tk c sm") +
                f.text(888, GY + 34, "выполнено —", "acc tk c sm") + f.text(888, GY + 54, "трафик идёт", "acc tk c sm"), f.vis(te, t1, fade=0.3))
    f.add(f.line(2, 352, 950, 352, "lf"))
    f.g(f.text(2, 384, "Двойная ловушка: если во время заморозки сменить отпечаток, ТСПУ добавляет штраф — 600 секунд.", "tk sm"), f.vis(0.2))
    f.g(wrapped(f, 2, 416, "Сайт не в реестре запрещённых: ломается только сетевое взаимодействие, а чинится это легальной настройкой.", "mu sm", 98, 19), f.vis(0.2))
    return f


# ═══ DPI: HTTP/1.1 против HTTP/2 ══════════════════════════════════════
def fig_dpi_http2():
    f = Fig("dpi-http2", 400, 14, "HTTP/2 сворачивает лавину рукопожатий в одно",
            "HTTP/1.1 открывает от 6 до примерно 30 параллельных TCP-соединений, в каждом свой TLS-хендшейк: лимит около трёх за 60 секунд превышен, "
            "ТСПУ замораживает узел на 120 секунд. HTTP/2 мультиплексирует всё в одно соединение с одним хендшейком, лимит не превышен.")
    f.add(f.text(2, 28, "HTTP/1.1", "cap"))
    f.add(f.text(490, 28, "HTTP/2", "cap"))
    f.add(f.rect(2, 52, 90, 220, "bx") + f.text(47, 168, "браузер", "mk c sm"))
    f.add(f.rect(400, 52, 80, 220, "bx") + f.text(440, 168, "сайт", "mk c sm"))
    for k in range(6):
        y = 66 + k * 38
        t = 0.8 + k * 0.35
        f.g(f.line(94, y, 398, y, "lm") + f.chip(180, y, 70, 24, "TLS", "bxa", "mk sm"), f.go([(0, -60, 0, 0), (t, -60, 0, 0), (t + 0.2, -60, 0, 1), (t + 0.7, 0, 0, 1)]))
    f.g(f.text(2, 300, "от 6 до ~30 соединений, у каждого свой TLS-хендшейк", "t"), f.vis(1.0))
    f.g(f.rect(2, 316, 478, 54, "bxr") + f.text(14, 340, "больше 3 хендшейков за 60 с →", "rej tk sm") + f.text(14, 360, "заморозка узла на 120 секунд", "rej tk sm"), f.vis(3.4))
    f.add(f.rect(490, 52, 90, 220, "bx") + f.text(535, 168, "браузер", "mk c sm"))
    f.add(f.rect(870, 52, 88, 220, "bx") + f.text(914, 168, "сайт", "mk c sm"))
    f.add(f.line(582, 162, 868, 162, "lm"))
    f.g(f.chip(660, 162, 70, 24, "TLS", "bxa", "mk sm"), f.go([(0, -60, 0, 0), (0.8, -60, 0, 0), (1.0, -60, 0, 1), (1.6, 0, 0, 1)]))
    for k in range(10):
        y = 150 + (k % 2) * 24 - 12
        t = 2.0 + k * 0.25
        f.g(f'<circle class="{f.c("dot")}" cx="{720 + k * 14}" cy="{162 + ((k * 7) % 3 - 1) * 5}" r="3.5"/>', f.go([(0, -60, 0, 0), (t, -60, 0, 0), (t + 0.15, -60, 0, 1), (t + 0.5, 0, 0, 1)]))
    f.g(wrapped(f, 490, 300, "одно TCP-соединение, ровно один хендшейк, внутри сотни запросов одновременно", "t", 46, 22), f.vis(1.4))
    f.g(f.rect(490, 346, 468, 30, "bxa") + f.text(502, 366, "лимит не превышен — трафик легитимен", "acc tk sm"), f.vis(4.2))
    return f


# ═══ DPI: июнь 2026, таймлайн ═════════════════════════════════════════
def fig_dpi_june_timeline():
    f = Fig("dpi-june", 400, 12, "Июньские сбои 2026: от жалоб до заявлений хостеров за шесть дней",
            "4–5 июня первые массовые жалобы, 6 июня обновление настроек ТСПУ, 7 июня технический разбор eByeBots, 9 июня закупка ДЦОА на 1,31 млрд рублей, "
            "9–10 июня Selectel, Beget и Timeweb подтверждают сбои.")
    X0, DX, AY = 70, 130, 200
    f.add(f.line(X0 - 30, AY, X0 + DX * 6 + 40, AY, "lm"))
    for d in range(4, 11):
        x = X0 + (d - 4) * DX
        f.add(f.line(x, AY - 6, x, AY + 6, "lm"))
        f.add(f.text(x, AY + 28, f"{d} июня", "mu sm c"))
    ev = [(4.5, "4–5 июня", "первые массовые жалобы на недоступность сайтов", -1, False),
          (6, "6 июня", "обновление настроек ТСПУ — точка отсчёта сбоев", 1, True),
          (7, "7 июня", "eByeBots публикует технический разбор", -1, False),
          (9, "9 июня", "ДЦОА закупает на 1,31 млрд ₽ ≥154 сервера для ТСПУ", 1, False),
          (9.7, "9–10 июня", "Selectel, Beget и Timeweb подтверждают сбои", -1, False)]
    for k, (d, title, text, side, key) in enumerate(ev):
        x = X0 + (d - 4) * DX
        t = 0.6 + k * 1.6
        y0 = AY - 24 if side < 0 else AY + 50
        cardy = 40 if side < 0 else AY + 70
        if k == 4:
            cardy = 110
        inner = f'<circle class="{f.c("nda" if not key else "ndr")}" cx="{x}" cy="{AY}" r="8"/>'
        cw = 200
        cx0 = max(2, min(x - cw / 2, 958 - cw))
        ty = cardy
        inner += f.line(x, AY - 8 if side < 0 else AY + 8, x, (ty + 78) if side < 0 else ty, "lm")
        inner += f.rect(cx0, ty, cw, 78, "bxr" if key else "bx")
        inner += f.text(cx0 + 12, ty + 24, title, "rej tk sm" if key else "tk sm")
        for j, ln in enumerate(textwrap.wrap(text, 25)):
            inner += f.text(cx0 + 12, ty + 46 + j * 18, ln, "mu sm")
        f.g(inner, f.vis(t, dy=-6 if side < 0 else 6))
    return f


# ═══ Premium: привязка устройства ═════════════════════════════════════
def fig_premium_bind():
    f = Fig("premium-bind", 568, 20, "Привязка Zapret Premium: код из программы — в бот",
            "Пользователь покупает тариф в боте, создаёт в Zapret GUI код из 8 символов, отправляет его боту; программа каждые несколько секунд спрашивает сервер "
            "и после привязки показывает Premium. Бот отвечает одним из пяти сообщений.")
    LX = {"u": 120, "g": 350, "b": 580}
    for k, (a, b) in {"u": ("Ты", "в Telegram"), "g": ("Zapret GUI", "страница «Донат»"), "b": ("Бот и сервер", "@zapretvpns_bot")}.items():
        x = LX[k]
        f.add(f.line(x, 66, x, 540, "lfd"))
        f.add(f.rect(x - 90, 12, 180, 50, "bx"))
        f.add(f.text(x, 34, a, "tk c"))
        f.add(f.text(x, 52, b, "mu sm c"))
    f.g(f.text(LX["u"] + 8, 100, "1. купить любой тариф", "t sm") + f.arrow(LX["u"] + 4, 110, LX["b"] - 4, 110, "f"), f.vis(0.8))
    f.g(f.text(LX["u"] + 8, 170, "2. «Создать код»", "t sm") + f.arrow(LX["u"] + 4, 180, LX["g"] - 4, 180, "f") +
        f.rect(LX["g"] - 110, 196, 220, 62, "bxa") + f.text(LX["g"], 218, "код из 8 символов,", "mk c sm") + f.text(LX["g"], 238, "действует 10 минут", "mk c sm"), f.vis(2.6))
    f.g(f.text(LX["u"] + 8, 306, "3. отправить код боту", "t sm") + f.arrow(LX["u"] + 4, 316, LX["b"] - 4, 316, "f"), f.vis(5.2))
    outs = [("✅ Устройство привязано", "acc"), ("❌ Код не найден или истёк", "rej"), ("ℹ️ Код уже использован", "mu"),
            ("⚠️ Лимит устройств: 5", "rej"), ("🔒 Нет активной подписки", "rej")]
    f.g(f.text(700, 78, "ответ бота — один из пяти", "cap"), f.vis(6.0))
    for k, (txt, col) in enumerate(outs):
        y = 94 + k * 40
        f.g(f.rect(700, y, 258, 32, "bxa" if k == 0 else "bx", rx=6) + f.text(710, y + 21, txt, ("acc tk sm" if k == 0 else "sm")), f.vis(6.3 + k * 0.4, dx=12))
    f.g(f.text(LX["g"] + 8, 380, "4. раз в несколько секунд:", "t sm") + f.text(LX["g"] + 8, 398, "«код пришёл?»", "t sm") + f.arrow(LX["g"] + 4, 408, LX["b"] - 4, 408, "f"), f.vis(9.2))
    f.g(f.arrow(LX["b"] - 4, 440, LX["g"] + 4, 440, "a", ) + f.text(LX["g"] + 8, 432, "привязка есть", "acc tk sm"), f.vis(11.4))
    f.g(f.rect(LX["g"] - 170, 460, 340, 70, "bxa") + f.text(LX["g"], 484, "«Привязка: есть», FREE → Premium", "tk c sm") +
        f.text(LX["g"], 504, "дальше сверка раз в несколько часов,", "mu sm c") + f.text(LX["g"], 522, "офлайн статус помнится до 7 дней", "mu sm c"), f.vis(13.0))
    return f


# ═══ Zapret: wssize ═══════════════════════════════════════════════════
def fig_wssize():
    f = Fig("wssize", 430, 14, "wssize срабатывает до того, как известен сайт",
            "wssize вмешивается во время TCP-рукопожатия, когда данных приложения ещё нет и неизвестны SNI и протокол. Поэтому хостлисты и l7-фильтр к нему не применимы, "
            "доступна лишь фильтрация по IP и портам. Обычные стратегии работают позже, на первом сообщении с данными.")
    pk = [("SYN", "→", 100), ("SYN-ACK", "←", 250), ("ACK", "→", 400), ("ClientHello (виден SNI)", "→", 640)]
    f.add(f.text(2, 28, "время жизни TCP-соединения", "cap"))
    f.add(f.arrow(2, 90, 950, 90, "f"))
    for k, (name, d, x) in enumerate(pk):
        t = 0.6 + k * 0.9
        w = 230 if k == 3 else 90
        f.g(f.chip(x, 90, w, 34, name, "bxa" if k == 3 else "bx", "mk sm"), f.go([(0, -30, 0, 0), (t, -30, 0, 0), (t + 0.2, -30, 0, 1), (t + 0.8, 0, 0, 1)]))
    f.g(f.line(18, 134, 450, 134, "la") + f.line(18, 128, 18, 140, "la") + f.line(450, 128, 450, 140, "la") +
        f.text(234, 162, "рукопожатие: данных приложения ещё нет", "acc tk c sm") + f.text(234, 182, "здесь работает wssize", "acc tk c sm"), f.vis(4.2))
    f.g(f.line(520, 134, 760, 134, "lm") + f.line(520, 128, 520, 140, "lm") + f.line(760, 128, 760, 140, "lm") +
        f.text(640, 162, "первое сообщение с данными:", "tk c sm") + f.text(640, 182, "SNI и протокол известны", "tk c sm") + f.text(640, 202, "здесь работают обычные стратегии", "mu c sm"), f.vis(5.6))
    f.add(f.line(2, 228, 950, 228, "lf"))
    f.add(f.text(2, 256, "поэтому у wssize нет", "cap"))
    lim = [("хостлистов", "SNI в рукопожатии ещё не передан"), ("l7-фильтра", "протокол опознаётся позже"), ("точной цели", "бьёт по всем под фильтром")]
    for k, (a, b) in enumerate(lim):
        x = 2 + k * 318
        f.g(f.rect(x, 270, 306, 68, "bxr") + f.text(x + 12, 296, a, "rej tk sm") + f.text(x + 12, 318, b, "mu sm"), f.vis(7.2 + k * 0.8, dy=8))
    f.g(wrapped(f, 2, 372, "Сервер из-за подмены окна шлёт ответ крошечными порциями: DPI без пересборки потока не видит его целиком, но замедляются все такие соединения.", "t sm", 98, 20), f.vis(10.4))
    return f


# ═══ Zapret: DoH, два случая ══════════════════════════════════════════
def fig_doh():
    f = Fig("doh", 458, 14, "Поможет ли zapret с заблокированным DoH",
            "Если DoH-сервер блокируют по имени (SNI виден в начале соединения), zapret поможет: домен резолвера добавляют в хостлист. "
            "Если блокируют по адресу или порту, соединение даже не начинается, и zapret бессилен: нужен другой адрес резолвера.")
    f.add(f.rect(300, 12, 360, 54, "bxa") + f.text(480, 38, "Как заблокирован DoH-сервер?", "tk c") + f.text(480, 56, "случаев два, действия противоположны", "mu sm c"))
    cases = [(20, "по имени", "SNI dns.google виден в начале HTTPS-соединения", "zapret поможет", "домен резолвера — в хостлист, дальше подбор стратегии", "acc"),
             (500, "по адресу", "соединение к IP или порту (например, 8.8.8.8) не проходит", "zapret бессилен", "портить нечего: соединение не начинается; другой адрес (8.8.4.4) или другой резолвер", "rej")]
    for k, (x, a, b, c, d, col) in enumerate(cases):
        t = 1.0 + k * 3.2
        f.g(f.arrow(480, 70, x + 220, 110, "f"), f.vis(t, fade=0.2))
        f.g(f.rect(x, 114, 440, 76, "bx") + f.text(x + 14, 140, "Случай " + str(k + 1) + ": " + a, "tk sm") +
            wrapped(f, x + 14, 160, b, "mu sm", 50, 17), f.vis(t + 0.4))
        f.g(f.arrow(x + 220, 192, x + 220, 220, "a" if col == "acc" else "r"), f.vis(t + 1.2, fade=0.2))
        f.g(f.rect(x, 224, 440, 92, "bxa" if col == "acc" else "bxr") + f.text(x + 14, 252, c, ("acc" if col == "acc" else "rej") + " tk") +
            wrapped(f, x + 14, 276, d, "sm", 44, 19), f.vis(t + 1.5))
    f.add(f.line(2, 338, 950, 338, "lf"))
    f.add(f.text(2, 364, "как понять, какой случай у вас", "cap"))
    chk = ["сменить адрес резолвера (8.8.4.4 вместо 8.8.8.8): заработало — случай 2", "недоступен по любому адресу, обычные сайты открываются — похоже на случай 1",
           "ничего не помогло — включить DoH внутри VPN или прокси-туннеля"]
    for k, c in enumerate(chk):
        f.g(f.text(2, 390 + k * 24, f"{k + 1}.  " + c, "t sm"), f.vis(8.0 + k * 1.2))
    return f


# ═══ MTProto: шесть слоёв детекции ════════════════════════════════════
def fig_mtproto_layers():
    f = Fig("mtproto-layers", 522, 14, "Шесть слоёв, которыми ТСПУ ищет MTProto",
            "Каскад методов детекции: сигнатуры, TLS-отпечаток, проверка IP и ASN, активные пробы, поведенческий анализ, ML. Каждый следующий слой дороже по вычислениям. "
            "От активных проб telemt и mtg защищают, официальный MTProxy нет; от поведенческого анализа адресует mtg Doppelganger.")
    rows = [("Сигнатуры", "первые 16–32 байта сверяются с базой; голый MTProto ловится мгновенно"),
            ("TLS-отпечаток", "JA3/JA4: своя TLS-библиотека (Go, Rust) даёт хэш, отличный от браузера"),
            ("IP и ASN", "SNI говорит «iCloud», а IP принадлежит Hetzner — аномалия"),
            ("Активные пробы", "ТСПУ сам подключается к серверу; ответ не по домену — блокировка"),
            ("Поведение", "размеры пакетов, тайминги, направление: у туннеля нетипичный профиль"),
            ("ИИ и ML", "нейросети по метаданным; бюджет 2,27 млрд ₽, утверждён в декабре 2025")]
    Y0, RH = 40, 74
    f.add(f.text(2, 26, "слой и что он проверяет", "cap"))
    f.add(f.text(600, 26, "кто защищает", "cap"))
    for k, (a, b) in enumerate(rows):
        y = Y0 + k * RH
        t = 0.5 + k * 1.3
        w = 20 + k * 6
        inner = f.line(2, y, 950, y, "lf")
        inner += f'<circle class="{f.c("nd")}" cx="22" cy="{y + RH / 2}" r="14"/>' + f.text(22, y + RH / 2 + 5, str(k + 1), "mk c sm")
        inner += f.text(48, y + 24, a, "tk sm")
        for j, ln in enumerate(textwrap.wrap(b, 52)):
            inner += f.text(48, y + 44 + j * 16, ln, "mu sm")
        f.g(inner, f.vis(t, dy=8))
        f.g(f.rect(2, y + RH - 7, 40 + k * 100, 4, "dot", rx=2), f.go([(0, -30, 0, 0), (t, -30, 0, 0), (t + 0.2, -30, 0, 1), (t + 0.9, 0, 0, 1)]))
    def side(row, lines, t):
        y = Y0 + row * RH + 12
        inner = "".join(f.text(600, y + 14 + j * 18, ln, cls) for j, (ln, cls) in enumerate(lines))
        f.g(inner, f.vis(t, dx=10))
    side(3, [("telemt: TCP Splice → реальный сайт", "acc tk sm"), ("mtg: Domain Fronting → такой же ответ", "acc tk sm"), ("официальный MTProxy: не защищает", "rej tk sm")], 5.0)
    side(4, [("mtg Doppelganger: имитирует", "acc tk sm"), ("паттерны настоящего сайта", "acc tk sm")], 6.5)
    f.g(f.text(2, 508, "Каждый следующий слой дороже по вычислениям, поэтому дешёвые признаки проверяются первыми.", "mu sm"), f.vis(9.0))
    return f


# ═══ MTProto: хронология ══════════════════════════════════════════════
def fig_mtproto_timeline():
    f = Fig("mtproto-timeline", 468, 14, "Хронология: от блокировки звонков к приватному FakeTLS",
            "Август 2025 блокировка звонков Telegram и WhatsApp, сентябрь 2025 блокировка VMess, декабрь 2025 закон об установке ТСПУ на трансграничные каналы, "
            "январь 2026 замедление медиа Telegram до 128 КБ/с, 17 февраля 2026 массовые сбои VLESS+Reality, 1 марта 2026 контроль над магистральным трафиком, "
            "март 2026 MTProxy с FakeTLS на приватных серверах работает.")
    ev = [("Август 2025", "РКН заблокировал звонки в Telegram и WhatsApp", 0), ("Сентябрь 2025", "VMess заблокирован в РФ", 0),
          ("Декабрь 2025", "закон об обязательной установке ТСПУ на все трансграничные каналы", 0),
          ("Январь 2026", "медиа в Telegram замедлено до 128 КБ/с", 0),
          ("17 февраля 2026", "массовые сбои VLESS+Reality: порог 16 КБ, блокировка IP на 10 минут", 1),
          ("1 марта 2026", "РКН получил контроль над магистральным трафиком", 0),
          ("Март 2026", "MTProxy с FakeTLS на приватных серверах работает", 2)]
    X = 176
    f.add(f.line(X, 20, X, 448, "lm"))
    for k, (d, txt, key) in enumerate(ev):
        y = 40 + k * 58
        t = 0.5 + k * 1.5
        col = {0: "tk sm", 1: "rej tk sm", 2: "acc tk sm"}[key]
        node = {0: "nd", 1: "ndr", 2: "nda"}[key]
        inner = f.text(X - 18, y + 5, d, col + " r") + f'<circle class="{f.c(node)}" cx="{X}" cy="{y}" r="9"/>'
        inner += f.rect(X + 24, y - 20, 700, 40, {0: "bx", 1: "bxr", 2: "bxa"}[key], rx=8)
        inner += f.text(X + 38, y + 5, txt, "sm" if key == 0 else col)
        f.g(inner, f.vis(t, dy=8))
    return f


# ═══ MTProto: статус протоколов ═══════════════════════════════════════
def fig_mtproto_status():
    f = Fig("mtproto-status", 520, 14, "Что блокируют, а что ещё работает (март 2026)",
            "Заблокированы OpenVPN, WireGuard, Shadowsocks, Trojan и VMess; массовые сбои у VLESS+TCP/TLS; VLESS+Reality детектируется поведенческим анализом; "
            "MTProto ванильный замедляется, публичный FakeTLS блокируется за часы или дни; работают приватный FakeTLS с telemt или mtg и SSH-туннели. Статусы на март 2026.")
    rows = [("OpenVPN, WireGuard", "заблокированы", "r"), ("Shadowsocks", "заблокирован с сентября 2024", "r"), ("Trojan", "заблокирован с августа 2025", "r"),
            ("VMess", "заблокирован с сентября 2025", "r"), ("VLESS + TCP/TLS", "массовые сбои с 17 февраля 2026", "r"),
            ("VLESS + Reality", "частично: ловится поведенческим анализом", "m"), ("VLESS + XHTTP", "рекомендуется как следующий шаг", "a"),
            ("MTProto ванильный", "замедляется", "m"), ("MTProto FakeTLS, публичный", "блокируется за часы или дни", "r"),
            ("MTProto FakeTLS, приватный", "работает при правильной настройке", "a"), ("SSH-туннели", "работают", "a")]
    f.add(f.text(2, 26, "протокол", "cap"))
    f.add(f.text(330, 26, "статус", "cap"))
    for k, (a, b, c) in enumerate(rows):
        y = 40 + k * 40
        t = 0.4 + k * 0.9
        kind = {"r": "bxr", "m": "bx", "a": "bxa"}[c]
        col = {"r": "rej tk sm", "m": "tk sm", "a": "acc tk sm"}[c]
        f.g(f.rect(2, y, 320, 32, "bx", rx=6) + f.text(14, y + 21, a, "tk sm") + f.rect(330, y, 628, 32, kind, rx=6) + f.text(344, y + 21, b, col), f.vis(t, dx=-10))
    f.g(f.text(2, 500, "Статус на март 2026; сейчас октябрь 2026, поэтому актуальность проверяйте по свежим заметкам.", "mu sm"), f.vis(10.0))
    return f


# ═══ MTProxy: где живёт задержка ══════════════════════════════════════
def fig_mtproxy_latency():
    f = Fig("mtproxy-latency", 506, 14, "Сеть не добавляет задержки: на одном релее цифры одинаковы",
            "Время в миллисекундах для трёх отрезков соединения: tcp до релея, faketls — ответ релея, respq — путь через релей до Telegram и обратно. "
            "Релей B даёт почти те же цифры в фильтрованной и в чистой сети: фильтрация задержки не добавляет. «За релеем» — примерно respq минус tcp.")
    data = [("релей A, фильтрованная сеть", 70, 71, 94, 24), ("релей B, фильтрованная сеть", 17, 9, 55, 38), ("релей B, чистая сеть", 11, 11, 56, 45)]
    X0, S = 250, 5.0
    f.add(f.text(2, 28, "миллисекунды", "cap"))
    f.add(f.text(X0 + 560, 28, "за релеем", "cap"))
    names = [("tcp", "до релея"), ("faketls", "ответ релея"), ("respq", "через релей к Telegram и назад")]
    for g, (label, tcp, ftls, respq, behind) in enumerate(data):
        y0 = 78 + g * 126
        t = 0.6 + g * 3.4
        f.g(f.text(2, y0 - 6, label, "tk sm"), f.vis(t, fade=0.25))
        vals = [tcp, ftls, respq]
        for k, v in enumerate(vals):
            y = y0 + 8 + k * 30
            cls = "bxa" if k == 2 else "bx"
            f.g(f.rect(X0, y, v * S, 24, cls, rx=5) + f.text(X0 + v * S + 8, y + 18, f"{v}", "mk sm") + f.text(X0 - 8, y + 18, names[k][0], "mu sm r"),
                f.go([(0, -30, 0, 0), (t + 0.3 + k * 0.4, -30, 0, 0), (t + 0.5 + k * 0.4, -30, 0, 1), (t + 1.1 + k * 0.4, 0, 0, 1)]))
        f.g(f.rect(X0 + 560, y0 + 4, 110, 84, "bxa") + f.text(X0 + 615, y0 + 44, f"≈ {behind}", "acc tk c") + f.text(X0 + 615, y0 + 64, "мс", "mu sm c"), f.vis(t + 1.8))
    f.g(wrapped(f, 2, 468, "Релеи различаются вдвое по суммарному времени (55 против 94 мс), но по разным причинам: один дальше от Telegram, другой дальше от клиента.", "mu sm", 98, 19), f.vis(11.4))
    return f


# ═══ tproxy: жизненный цикл потока ════════════════════════════════════
def fig_tproxy_lifecycle():
    f = Fig("tproxy-lifecycle", 506, 15, "Жизнь одного потока в tproxy: OPEN, DATA, CLOSE",
            "Клиент открывает поток кадром OPEN, реле открывает TCP-соединение к бэкенду. DATA идёт в обе стороны в рамках кредита. CLOSE закрывает поток; "
            "подтверждения у OPEN нет, данные можно слать сразу. Неудача дозвона закрывает только этот поток, сессия продолжает работать.")
    LX = {"c": 130, "r": 470, "b": 810}
    for k, (a, b) in {"c": ("Клиент", "приложение"), "r": ("Реле", "tproxy"), "b": ("Бэкенд", "TCP-сервис")}.items():
        x = LX[k]
        f.add(f.line(x, 66, x, 440, "lfd"))
        f.add(f.rect(x - 90, 12, 180, 50, "bx"))
        f.add(f.text(x, 34, a, "tk c"))
        f.add(f.text(x, 52, b, "mu sm c"))
    steps = [(100, "c", "r", "OPEN s=17", "a", None), (126, "r", "b", None, "f", "реле открывает TCP к бэкенду"),
             (196, "c", "r", "DATA s=17", "a", "ограничено кредитом"), (246, "r", "b", "DATA", "f", "запись в сокет бэкенда"),
             (306, "b", "r", None, "f", "чтение бэкенда"), (330, "r", "c", "DATA s=17", "a", None),
             (394, "c", "r", "CLOSE s=17", "r", "обрыв: данные в очереди отбрасываются"), (420, "r", "b", None, "f", "закрытие соединения")]
    for k, (y, a, b, lab, kind, note) in enumerate(steps):
        t = 0.6 + k * 1.5
        x1, x2 = LX[a] + (4 if LX[b] > LX[a] else -4), LX[b] - (4 if LX[b] > LX[a] else 4)
        if lab:
            f.g(f.text((LX[a] + LX[b]) / 2, y - 8, lab, "mk c sm"), f.vis(t))
        f.add(f.arrow(x1, y, x2, y, kind, t=t, dur=0.5))
        if note:
            f.g(f.text((LX[a] + LX[b]) / 2, y + 20, note, "mu sm c"), f.vis(t + 0.4))
    f.g(wrapped(f, 2, 462, "У OPEN нет подтверждения: DATA можно слать сразу. Неудача дозвона закрывает только этот поток, сессия продолжает работать.", "mu sm", 98, 19), f.vis(13.0))
    return f


# ═══ XHTTP: три режима ════════════════════════════════════════════════
def fig_xhttp_modes():
    f = Fig("xhttp-modes", 410, 14, "XHTTP: как разложены аплинк и даунлинк в трёх режимах",
            "packet-up: аплинк нарезан на много коротких POST с номером seq, даунлинк — отдельный длинный GET. stream-up: один длинный POST вверх и отдельный GET вниз. "
            "stream-one: аплинк и даунлинк в одном HTTP-обмене. Общий sessionId склеивает запросы в один туннель.")
    modes = [("packet-up", "через CDN, HTTP/1.1"), ("stream-up", "раздельные каналы up и down"), ("stream-one", "REALITY напрямую, h2 или h3")]
    for k, (name, good) in enumerate(modes):
        x = 2 + k * 320
        t = 0.6 + k * 3.4
        f.add(f.text(x, 28, name, "mk"))
        f.add(f.rect(x, 44, 70, 170, "bx") + f.text(x + 35, 134, "клиент", "mk c sm"))
        f.add(f.rect(x + 226, 44, 70, 170, "bx") + f.text(x + 261, 134, "сервер", "mk c sm"))
        if k == 0:
            for j in range(4):
                y = 66 + j * 22
                f.g(f.arrow(x + 74, y, x + 222, y, "a") + f.text(x + 148, y - 5, f"POST seq={j + 1}", "m sm c" if False else "mu sm c"), f.vis(t + 0.6 + j * 0.5, fade=0.2))
            f.g(f.arrow(x + 222, 176, x + 74, 176, "f") + f.text(x + 148, 168, "один длинный GET", "mu sm c"), f.vis(t + 3.0))
        elif k == 1:
            f.g(f.arrow(x + 74, 80, x + 222, 80, "a") + f.text(x + 148, 70, "одно длинное тело POST", "mu sm c"), f.vis(t + 0.6))
            f.g(f.arrow(x + 222, 176, x + 74, 176, "f") + f.text(x + 148, 168, "отдельный GET", "mu sm c"), f.vis(t + 1.8))
        else:
            f.g(f.arrow(x + 74, 100, x + 222, 100, "a") + f.text(x + 148, 90, "тело запроса", "mu sm c"), f.vis(t + 0.6))
            f.g(f.arrow(x + 222, 150, x + 74, 150, "f") + f.text(x + 148, 142, "тело ответа", "mu sm c"), f.vis(t + 1.4))
        f.g(f.rect(x, 232, 296, 36, "bxa", rx=6) + f.text(x + 148, 255, good, "tk c sm"), f.vis(t + 2.4))
    f.add(f.line(2, 296, 950, 296, "lf"))
    f.g(wrapped(f, 2, 326, "Сессию на сервере склеивает общий sessionId: GET даунлинка и все POST аплинка с одним sessionId относятся к одному туннелю.", "t sm", 98, 20), f.vis(11.0))
    return f


FIGS = {
    "z2-pipeline": (fig_z2_pipeline, "Zapret2/attachments"),
    "z2-profilepick": (fig_z2_profilepick, "Zapret2/attachments"),
    "z2-circular": (fig_z2_circular, "Zapret2/attachments"),
    "z2-profile": (fig_z2_profile, "Zapret2/attachments"),
    "z2-outrange": (fig_z2_outrange, "Zapret2/attachments"),
    "z2-fakedies": (fig_z2_fakedies, "Zapret2/attachments"),
    "z2-f5": (fig_z2_f5, "Zapret2/attachments"),
    "dpi-gates": (fig_dpi_gates, "DPI/attachments"),
    "dpi-http2": (fig_dpi_http2, "DPI/attachments"),
    "dpi-june": (fig_dpi_june_timeline, "DPI/attachments"),
    "premium-bind": (fig_premium_bind, "premium/attachments"),
    "wssize": (fig_wssize, "Zapret/attachments"),
    "doh": (fig_doh, "Zapret/attachments"),
    "mtproto-layers": (fig_mtproto_layers, "Zapret/attachments"),
    "mtproto-timeline": (fig_mtproto_timeline, "Zapret/attachments"),
    "mtproto-status": (fig_mtproto_status, "Zapret/attachments"),
    "mtproxy-latency": (fig_mtproxy_latency, "mtproxy/attachments"),
    "tproxy-lifecycle": (fig_tproxy_lifecycle, "tproxy/attachments"),
    "xhttp-modes": (fig_xhttp_modes, "xray/attachments"),
}


def main(argv):
    out_override = None
    names = []
    for a in argv:
        if a in FIGS:
            names.append(a)
        else:
            out_override = Path(a)
    for name in names or list(FIGS):
        fn, folder = FIGS[name]
        out = out_override or ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        svg = fn().render()
        (out / f"wiki-anim-{name}.svg").write_text(svg, encoding="utf-8")
        print(f"wiki-anim-{name}.svg  {len(svg) // 1024} КБ")


if __name__ == "__main__":
    main(sys.argv[1:])
