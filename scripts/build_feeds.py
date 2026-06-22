#!/usr/bin/env python3
"""Génère les flux RSS du site (idempotent).

- /feed.xml            : journal FR (depuis journal/index.html, 20 dernières entrées)
- /veille-ia/feed.xml  : veille IA (depuis veille-ia/feed.json, 50 derniers items)

Usage : python3 scripts/build_feeds.py   (depuis la racine du repo ou ailleurs)
"""
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "knowledge-hub"
BASE = "https://hl-consulting.tech/knowledge-hub"

ENTRY_RE = re.compile(
    r'<li class="entry"[^>]*>.*?<time datetime="(?P<date>[\d-]+)">.*?'
    r'<a href="(?P<href>[^"]+)">(?P<title>.*?)</a>.*?'
    r'<p class="entry__excerpt">(?P<excerpt>.*?)</p>',
    re.S,
)


def rfc822(iso_date: str) -> str:
    d = datetime.strptime(iso_date, "%Y-%m-%d").replace(hour=8, tzinfo=timezone.utc)
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


def rss(title: str, link: str, description: str, items: list) -> str:
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "<channel>",
        f"<title>{html.escape(title)}</title>",
        f"<link>{link}</link>",
        f"<description>{html.escape(description)}</description>",
        "<language>fr</language>",
        f'<atom:link href="{link.rstrip("/")}/feed.xml" rel="self" type="application/rss+xml"/>',
    ]
    for it in items:
        out += [
            "<item>",
            f"<title>{html.escape(it['title'])}</title>",
            f"<link>{it['link']}</link>",
            f"<guid isPermaLink=\"{'true' if it.get('permalink', True) else 'false'}\">{it['guid']}</guid>",
            f"<pubDate>{rfc822(it['date'])}</pubDate>",
            f"<description>{html.escape(it['description'])}</description>",
            "</item>",
        ]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def build_journal_feed() -> None:
    src = (ROOT / "journal" / "index.html").read_text(encoding="utf-8")
    items = []
    for m in ENTRY_RE.finditer(src):
        url = f"{BASE}/journal/{m['href']}"
        items.append({
            "title": html.unescape(re.sub(r"<[^>]+>", "", m["title"])),
            "link": url,
            "guid": url,
            "date": m["date"],
            "description": html.unescape(re.sub(r"<[^>]+>", "", m["excerpt"])),
        })
    items = items[:20]
    xml = rss(
        "Journal — Hugo Lahutte",
        f"{BASE}/",
        "Sessions documentées : comment Hugo Lahutte construit avec Claude (Odoo, Shopify, agents, méthode).",
        items,
    )
    (ROOT / "feed.xml").write_text(xml, encoding="utf-8")
    print(f"feed.xml : {len(items)} entrées journal")


def build_veille_feed() -> None:
    data = json.loads((ROOT / "veille-ia" / "feed.json").read_text(encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("items", [])
    rows = [e for e in rows if e.get("date")]
    rows.sort(key=lambda e: e["date"], reverse=True)
    items = []
    for e in rows[:50]:
        link = e.get("tweet_url") or f"{BASE}/veille-ia/"
        items.append({
            "title": e.get("titre_fr", ""),
            "link": link,
            "guid": f"{BASE}/veille-ia/#{e['date']}-{abs(hash(e.get('titre_fr', ''))) % 10**8}",
            "permalink": False,
            "date": e["date"],
            "description": e.get("resume_fr", ""),
        })
    xml = rss(
        "Veille IA — Hugo Lahutte",
        f"{BASE}/veille-ia/",
        "Veille IA quotidienne curatée : modèles, agents, outils — angle marchands & PME.",
        items,
    )
    (ROOT / "veille-ia" / "feed.xml").write_text(xml, encoding="utf-8")
    print(f"veille-ia/feed.xml : {len(items)} items veille")


if __name__ == "__main__":
    build_journal_feed()
    build_veille_feed()
