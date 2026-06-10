#!/usr/bin/env python3
"""Injecte un rendu HTML statique de la veille IA dans les pages veille (idempotent).

Pourquoi : la page rend feed.json côté client, or les crawlers IA (GPTBot,
ClaudeBot, PerplexityBot…) n'exécutent pas le JavaScript. Ce script écrit les
derniers items en HTML statique dans <div id="veille-feed">, entre marqueurs ;
le JS de la page écrase ce contenu au chargement chez les visiteurs.

À relancer après chaque mise à jour de veille-ia/feed.json :
    python3 scripts/build_veille_static.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK_START = "<!-- veille-static:start (généré par scripts/build_veille_static.py) -->"
MARK_END = "<!-- veille-static:end -->"
DAYS = 10  # nombre de jours de veille rendus en statique

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def score(e: dict) -> float:
    if isinstance(e.get("score"), (int, float)):
        return e["score"]
    if isinstance(e.get("importance"), (int, float)):
        return e["importance"]
    return min(len(e.get("tags", [])), 3) + min(len(e.get("resume_fr", "")) / 200, 2)


def render_static() -> str:
    data = json.loads((ROOT / "veille-ia" / "feed.json").read_text(encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("items", [])
    rows = [e for e in rows if e.get("date")]
    rows.sort(key=lambda e: e["date"], reverse=True)

    days: dict[str, list] = {}
    for e in rows:
        days.setdefault(e["date"], []).append(e)

    out = []
    for date in sorted(days, reverse=True)[:DAYS]:
        items = sorted(days[date], key=score, reverse=True)
        n = len(items)
        out.append('<section class="veille-dayblock">')
        out.append(
            f'<div class="veille-day"><time datetime="{date}">{fr_date(date)}</time>'
            f'<span class="veille-day__count">{n} annonce{"s" if n > 1 else ""}</span></div>'
        )
        for e in items:
            tags = "".join(
                f'<span class="tag">{html.escape(t)}</span>' for t in e.get("tags", [])
            )
            src = (
                f' <a class="veille-src" href="{html.escape(e["tweet_url"])}" target="_blank"'
                f' rel="noopener">Voir l\'original sur X →</a>'
                if e.get("tweet_url") else ""
            )
            out.append(
                '<article class="veille-item">'
                f'<h3 class="veille-title">{html.escape(e.get("titre_fr", ""))}</h3>'
                f'<p class="veille-resume">{html.escape(e.get("resume_fr", ""))}{src}</p>'
                + (f'<div class="tags veille-tags">{tags}</div>' if tags else "")
                + "</article>"
            )
        out.append("</section>")
    return "\n".join(out)


def inject(page: Path, static_html: str) -> None:
    src = page.read_text(encoding="utf-8")
    block = f"{MARK_START}\n{static_html}\n{MARK_END}"
    if MARK_START in src:
        new = re.sub(
            re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
            lambda _: block, src, flags=re.S,
        )
    else:
        new = src.replace(
            '<div id="veille-feed" class="veille-feed"></div>',
            f'<div id="veille-feed" class="veille-feed">\n{block}\n</div>',
            1,
        )
        if new == src:
            raise SystemExit(f"{page} : point d'injection introuvable")
    page.write_text(new, encoding="utf-8")
    print(f"{page.relative_to(ROOT)} : rendu statique injecté ({DAYS} jours)")


if __name__ == "__main__":
    static_html = render_static()
    inject(ROOT / "veille-ia" / "index.html", static_html)
    inject(ROOT / "en" / "veille-ia" / "index.html", static_html)
