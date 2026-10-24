#!/usr/bin/env python3
"""Статистика читателей wiki2.zapret.moe по логу nginx, без счётчиков и cookie.

Лог /var/log/nginx/access.log общий с Forgejo и другими сайтами хоста, поэтому
берутся только запросы страниц вики (слаги из собранного сайта). Для каждого
читателя хранится не IP, а усечённый хеш sha256(соль + IP + User-Agent); соль
случайная и лежит в приватном state.json (0600). Публикуется только агрегат
(stats.json): числа по дням, топ статей, источники, платформы, часы.

Читатель считается человеком, если User-Agent не похож на бота и браузер в тот
же или предыдущий день запросил стили сайта (index.css, postscript.js), а за
день открыл не больше MAX_PAGES разных страниц. Это оценка, а не точный счёт:
скрейперы с настоящим браузером пройдут фильтр, а читатели, закрывшие JS и
CSS, отсеются.

Запуск: wiki-stats.py [--rebuild] — по таймеру wiki-stats.timer раз в 10 минут.
Первый запуск (или --rebuild) читает все сохранённые логи, включая .gz.
"""
import datetime as dt
import fcntl
import gzip
import hashlib
import ipaddress
import json
import os
import re
import secrets
import sys
import time
from urllib.parse import unquote_to_bytes, urlsplit

LOGDIR = "/var/log/nginx"
OUT = "/srv/wiki-stats"
PUBLIC = "/srv/wiki-quartz/public"
MSK = dt.timezone(dt.timedelta(hours=3))  # пояс меток времени в логе nginx
KEEP_DAYS = 95
MAX_PAGES = 80  # больше разных страниц за день — это обход сайта, а не чтение
MAX_VIEWS = 120  # больше просмотров за день — тоже робот (у 99% читателей меньше 40)
MAX_REPEAT = 30  # одна страница чаще 30 раз за день — перезагрузка по таймеру, не чтение
WINDOWS = (7, 30, 90)
TOP_N = 20
SPARK_DAYS = 14

MONTHS = {m.encode(): i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}

BOT = re.compile(
    r"bot|crawl|spider|slurp|scrap|fetch|python|curl|wget|go-http|okhttp|httpclient|libwww|"
    r"headless|axios|java/|aiohttp|requests|monitor|uptime|preview|facebookexternalhit|"
    r"clashmeta|clash|v2ray|happ/|hiddify|sing-box|shadowrocket|streisand|nekobox|"
    r"mihomo|flclash|compatible;|^-?$|Mozilla/5\.0 AppleWebKit|Lighthouse|Chrome-Lighthouse|"
    r"ahrefs|semrush|mj12|dataforseo|ia_archiver|archive\.org",
    re.I,
)
ASSETS = {b"/index.css", b"/postscript.js", b"/prescript.js"}

SECTIONS = {
    "Zapret": "Запрет GUI", "Zapret2": "Zapret 2", "DPI": "DPI и ТСПУ", "VLESS": "VLESS",
    "xray": "Xray", "Hysteria": "Hysteria", "amnezia-2-0": "AmneziaWG 2.0",
    "amnezia-3-0": "AmneziaWG 3.0", "sing-box": "sing-box", "Clash": "Clash",
    "protocols": "Протоколы", "tproxy": "TProxy", "subscriptions": "Подписки",
    "mtproxy": "MTProxy", "FIDO": "FIDO и ключи", "TOTP": "TOTP", "Mail": "Почта",
    "Payment": "Платежи", "virus": "Вирусы", "premium": "Zapret Premium", "nuc": "NUC",
    "root": "Root", "": "Разное",
}


def site_index():
    """canonical: слаг → заголовок; alias: путь заглушки → слаг (редирект Quartz)."""
    with open(f"{PUBLIC}/static/contentIndex.json", encoding="utf-8") as f:
        idx = json.load(f)
    titles = {k: v.get("title") or k.rsplit("/", 1)[-1] for k, v in idx.items()}
    # в contentIndex заголовок часто совпадает с именем файла; читателю нужен тот,
    # что виден на странице, — берём <title> из собранного HTML
    tag = re.compile(r"<title>([^<]+)</title>")
    for slug in titles:
        try:
            with open(f"{PUBLIC}/{slug}.html", encoding="utf-8") as f:
                m = tag.search(f.read(2500))
        except OSError:
            continue
        if m:
            titles[slug] = re.sub(r"\s+—\s+wiki\.zapret\.moe$", "", m.group(1)).strip()
    alias = {}
    stub = re.compile(r'http-equiv="refresh" content="0; url=\./([^"]+)"')
    for name in os.listdir(PUBLIC):
        if not name.endswith(".html") or name[:-5] in titles:
            continue
        try:
            with open(f"{PUBLIC}/{name}", encoding="utf-8") as f:
                m = stub.search(f.read(1500))
        except OSError:
            continue
        if m and m.group(1) in titles:
            alias[name[:-5]] = m.group(1)
    return titles, alias


def ext_referrer(ref: str):
    """Источник захода или None, если реферер пустой или это сама вики."""
    if not ref or ref == "-":
        return None
    if ref.startswith("android-app://"):
        pkg = ref[len("android-app://"):].split("/")[0].lower()
        return "Telegram" if ("telegram" in pkg or "ayugram" in pkg or "nekogram" in pkg) else "Другие сайты"
    host = (urlsplit(ref).hostname or "").lower()
    if not host or host == "wiki2.zapret.moe":
        return None
    if host in ("t.me", "telegram.me", "telegram.org", "web.telegram.org", "telegra.ph") or "telegram" in host:
        return "Telegram"
    if host.startswith(("yandex.", "www.yandex.")) or host in ("ya.ru", "dzen.ru") or host.endswith(".yandex.ru"):
        return "Яндекс"
    if "google." in host:
        return "Google"
    if host.endswith(("bing.com", "duckduckgo.com", "ecosia.org", "search.brave.com", "startpage.com", "yahoo.com", "baidu.com")):
        return "Другие поисковики"
    if host in ("git.zapret.moe", "github.com", "gitlab.com"):
        return "Git (Forgejo, GitHub)"
    if host == "publish.obsidian.md":
        return "Зеркало (Obsidian Publish)"
    if host.endswith(("4pda.to", "4pda.ru")):
        return "4PDA"
    return "Другие сайты"


def platform(ua: str):
    if "iPhone" in ua or "iPad" in ua:
        return "iOS"
    if "Android" in ua:
        return "Android"
    if "Windows" in ua:
        return "Windows"
    if "Macintosh" in ua:
        return "macOS"
    if "CrOS" in ua:
        return "ChromeOS"
    if "Linux" in ua or "X11" in ua:
        return "Linux"
    return "Другое"


def open_log(path):
    return gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb")


def log_files():
    """Сохранённые логи от старых к новым: access.log.N.gz … .2.gz, .1, access.log."""
    found = []
    for name in os.listdir(LOGDIR):
        m = re.fullmatch(r"access\.log(?:\.(\d+)(\.gz)?)?", name)
        if m:
            found.append((int(m.group(1)) if m.group(1) else 0, os.path.join(LOGDIR, name)))
    return [p for _, p in sorted(found, reverse=True)]


def ingest(fobj, state, titles, alias, skip=0):
    """Читает полные строки и возвращает число прочитанных байт."""
    if skip:
        fobj.seek(skip)
    salt = state["salt"].encode()
    days, assets = state["days"], state["assets"]
    consumed = skip
    slugb = {}  # кеш: сырой путь → (kind, значение)
    for raw in fobj:
        if not raw.endswith(b"\n"):
            break
        consumed += len(raw)
        p = raw.split(b'"')
        if len(p) < 6:
            continue
        req = p[1]
        if not req.startswith(b"GET /"):
            continue
        path = req.split(b" ", 2)[1].split(b"?", 1)[0]
        hit = slugb.get(path)
        if hit is None:
            if path in ASSETS:
                hit = ("asset", None)
            else:
                dec = unquote_to_bytes(path).decode("utf-8", "replace")
                s = "Zapret/home" if dec == "/" else dec.lstrip("/")
                if s in titles:
                    hit = ("page", s)
                elif s in alias:
                    hit = ("alias", alias[s])
                else:
                    hit = ("skip", None)
            if len(slugb) < 20000:
                slugb[path] = hit
        kind, slug = hit
        if kind == "skip":
            continue
        st = p[2].split(None, 1)[0]
        if st not in (b"200", b"304"):
            continue
        head = p[0]
        ip = head.split(b" ", 1)[0]
        try:
            if ipaddress.ip_address(ip.decode()).is_private:
                continue
        except ValueError:
            continue
        ts = head[head.index(b"[") + 1:head.index(b"]")]  # 19/Oct/2026:00:42:21 +0300
        d, mon, rest = ts.split(b"/", 2)
        year, hh = rest[:4], rest[5:7]
        day = f"{year.decode()}-{MONTHS[mon]:02d}-{d.decode()}"
        ua = p[5].decode("utf-8", "replace")
        h = hashlib.sha256(salt + ip + b"|" + p[5]).hexdigest()[:10]
        if kind == "asset":
            assets.setdefault(day, {})[h] = 1
            continue
        if BOT.search(ua):
            continue
        v = days.setdefault(day, {}).get(h)
        if v is None:
            v = days[day][h] = {"p": {}, "pl": platform(ua), "rf": "", "hr": 0}
        ref = ext_referrer(p[3].decode("utf-8", "replace"))
        if ref and not v["rf"]:
            v["rf"] = ref
        if kind == "alias":
            continue  # заглушка редиректа: просмотр засчитается на странице-цели
        v["p"][slug] = v["p"].get(slug, 0) + 1
        v["hr"] |= 1 << int(hh)
    return consumed


def update_state(state, titles, alias, rebuild):
    cur = os.path.join(LOGDIR, "access.log")
    cur_ino = os.stat(cur).st_ino
    cursor = None if rebuild else state.get("cursor")
    files = log_files()
    if cursor is None:
        for path in files[:-1]:
            with open_log(path) as f:
                ingest(f, state, titles, alias)
        with open(cur, "rb") as f:
            pos = ingest(f, state, titles, alias)
    elif cursor["ino"] == cur_ino:
        with open(cur, "rb") as f:
            pos = ingest(f, state, titles, alias, min(cursor["pos"], os.fstat(f.fileno()).st_size))
    else:
        # лог ротировали: дочитать старый (он стал access.log.1), затем новый с нуля
        prev = os.path.join(LOGDIR, "access.log.1")
        if os.path.exists(prev) and os.stat(prev).st_ino == cursor["ino"]:
            with open(prev, "rb") as f:
                ingest(f, state, titles, alias, cursor["pos"])
        with open(cur, "rb") as f:
            pos = ingest(f, state, titles, alias)
    state["cursor"] = {"ino": cur_ino, "pos": pos}


def human_visitors(state, day):
    """Читатели дня, прошедшие фильтр ботов: {хеш: запись}."""
    prev = (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()
    a = state["assets"]
    ok = {}
    for h, v in state["days"].get(day, {}).items():
        if not v["p"] or len(v["p"]) > MAX_PAGES or sum(v["p"].values()) > MAX_VIEWS or max(v["p"].values()) > MAX_REPEAT:
            continue
        if h in a.get(day, {}) or h in a.get(prev, {}):
            ok[h] = v
    return ok


def section(slug):
    top = slug.split("/")[0] if "/" in slug else ""
    return SECTIONS.get(top, top)


def article(slug):
    return slug != "Zapret/home" and not slug.endswith("/index")


def aggregate(state, titles, today):
    t0 = dt.date.fromisoformat(today)
    all_days = sorted(state["days"])
    humans = {d: human_visitors(state, d) for d in all_days}
    daily = []
    for d in all_days:
        views = sum(sum(v["p"].values()) for v in humans[d].values())
        daily.append({"d": d, "v": len(humans[d]), "w": views})
    daily = daily[-WINDOWS[-1]:]

    def span(n):
        return [(t0 - dt.timedelta(days=i)).isoformat() for i in range(n)]

    def window(n):
        ds = [d for d in span(n) if d in humans]
        vis, readers, views, secs, plats, srcs, heat = set(), {}, {}, {}, {}, {}, [[0] * 24 for _ in range(7)]
        visits, seen_days = 0, {}
        for d in ds:
            wd = dt.date.fromisoformat(d).weekday()
            for h, v in humans[d].items():
                vis.add(h)
                visits += 1
                seen_days.setdefault(h, set()).add(d)
                for s, c in v["p"].items():
                    readers.setdefault(s, set()).add(h)
                    views[s] = views.get(s, 0) + c
                for sec in {section(s) for s in v["p"] if article(s)}:
                    secs.setdefault(sec, set()).add(h)
                plats.setdefault(v["pl"], set()).add(h)
                srcs.setdefault(v["rf"] or "Прямой заход, закладки", set()).add(h)
                for hr in range(24):
                    if v["hr"] >> hr & 1:
                        heat[wd][hr] += 1
        arts = sorted((s for s in readers if article(s)), key=lambda s: (-len(readers[s]), -views[s], s))
        spark_days = span(SPARK_DAYS)[::-1]
        top = []
        for s in arts[:TOP_N]:
            sp = [sum(1 for v in humans.get(d, {}).values() if s in v["p"]) for d in spark_days]
            top.append({"s": s, "t": titles.get(s, s), "r": len(readers[s]), "w": views[s], "sp": sp})

        def rank(m, limit=None):
            rows = sorted(((k, len(v)) for k, v in m.items()), key=lambda kv: -kv[1])
            return [{"k": k, "v": v} for k, v in rows[:limit]]

        return {
            "visitors": len(vis),
            "views": sum(views.values()),
            "visits": visits,
            "returning": sum(1 for s in seen_days.values() if len(s) >= 2),
            "articles_read": len(arts),
            "top": top,
            "src": rank(srcs),
            "plat": rank(plats),
            "sec": rank(secs, 10),
            "heat": heat,
        }

    kpi = {}
    for key, d in (("today", today), ("yesterday", (t0 - dt.timedelta(days=1)).isoformat())):
        hv = humans.get(d, {})
        kpi[key] = {"v": len(hv), "w": sum(sum(v["p"].values()) for v in hv.values())}
    wins = {str(n): window(n) for n in WINDOWS}
    return {
        "generated": int(time.time()),
        "today": today,
        "since": all_days[0] if all_days else today,
        "span": len(all_days),
        "articles_total": sum(1 for s in titles if article(s)),
        "kpi": kpi,
        "daily": daily,
        "windows": wins,
    }


def write_atomic(path, data, mode):
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(data)
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def main():
    rebuild = "--rebuild" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    lock = open(f"{OUT}/.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    sp = f"{OUT}/state.json"
    state = {"salt": secrets.token_hex(16), "cursor": None, "days": {}, "assets": {}}
    if os.path.exists(sp) and not rebuild:
        with open(sp, encoding="utf-8") as f:
            state = json.load(f)
    elif os.path.exists(sp):
        with open(sp, encoding="utf-8") as f:
            state["salt"] = json.load(f)["salt"]  # соль сохраняем: хеши остаются сопоставимыми
    titles, alias = site_index()
    update_state(state, titles, alias, rebuild)
    today = dt.datetime.now(MSK).date().isoformat()
    cutoff = (dt.date.fromisoformat(today) - dt.timedelta(days=KEEP_DAYS)).isoformat()
    for k in ("days", "assets"):
        state[k] = {d: v for d, v in state[k].items() if d >= cutoff}
    write_atomic(sp, json.dumps(state, ensure_ascii=False, separators=(",", ":")), 0o600)
    write_atomic(f"{OUT}/stats.json", json.dumps(aggregate(state, titles, today), ensure_ascii=False, separators=(",", ":")), 0o644)


if __name__ == "__main__":
    main()
