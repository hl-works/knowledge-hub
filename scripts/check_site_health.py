#!/usr/bin/env python3
"""Check de cohérence du site (lecture seule, exit 1 si dérive).

Vérifie que les compteurs et index restent synchronisés avec les fichiers :
- journal/*.html  vs  search-index*.json (entrées Journal, URLs existantes)
- compteur "## Journal (NN …)" dans llms.txt / en/llms.txt
- compteur "NN sessions" dans les <title> des index journal
- fallback <b id="stat-sessions">NN</b> des deux homes
- chaque entrée journal présente dans sitemap.xml
- appariement FR/EN du journal

Usage : python3 scripts/check_site_health.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def journal_slugs(d: Path) -> set[str]:
    return {f.stem for f in d.glob("*.html") if f.name not in ("index.html", "_template.html")}


def indexed_slugs(index_file: Path) -> set[str]:
    data = json.loads(index_file.read_text(encoding="utf-8"))
    slugs = set()
    for e in data:
        if e.get("kind") == "Journal" and not e["url"].rstrip("/").endswith("journal"):
            slugs.add(e["url"].rstrip("/").split("/")[-1].removesuffix(".html"))
    return slugs


def expect_count(path: Path, pattern: str, expected: int, label: str) -> None:
    m = re.search(pattern, path.read_text(encoding="utf-8"))
    if not m:
        err(f"{label} : motif introuvable dans {path.name}")
    elif int(m.group(1)) != expected:
        err(f"{label} : {m.group(1)} au lieu de {expected} ({path.relative_to(ROOT)})")


fr = journal_slugs(ROOT / "journal")
en = journal_slugs(ROOT / "en" / "journal")
n = len(fr)

# Appariement FR/EN
if fr != en:
    if fr - en:
        err(f"journal : pages FR sans jumelle EN : {sorted(fr - en)}")
    if en - fr:
        err(f"journal : pages EN orphelines : {sorted(en - fr)}")

# search-index FR/EN
for index_file, disk in ((ROOT / "search-index.json", fr), (ROOT / "search-index.en.json", en)):
    idx = indexed_slugs(index_file)
    if idx != disk:
        if disk - idx:
            err(f"{index_file.name} : entrées manquantes : {sorted(disk - idx)}")
        if idx - disk:
            err(f"{index_file.name} : URLs sans fichier sur disque : {sorted(idx - disk)}")

# Compteurs llms.txt
expect_count(ROOT / "llms.txt", r"## Journal \((\d+) entrées\)", n, "llms.txt")
expect_count(ROOT / "en" / "llms.txt", r"## Journal \((\d+) entries\)", len(en), "en/llms.txt")

# Compteurs statiques (titres, og, lead, placeholders, fallbacks JS)
expect_count(ROOT / "journal" / "index.html", r"<title>[^<]*?(\d+) sessions", n, "titre journal FR")
expect_count(ROOT / "journal" / "index.html", r'og:description" content="(\d+) sessions', n, "og journal FR")
expect_count(ROOT / "journal" / "index.html", r'class="lead">(\d+) sessions', n, "lead journal FR")
expect_count(ROOT / "en" / "journal" / "index.html", r"<title>[^<]*?(\d+) documented", len(en), "titre journal EN")
expect_count(ROOT / "en" / "journal" / "index.html", r'og:description" content="(\d+) sessions', len(en), "og journal EN")
expect_count(ROOT / "en" / "journal" / "index.html", r'class="lead">(\d+) working', len(en), "lead journal EN")
expect_count(ROOT / "index.html", r'id="stat-sessions">(\d+)<', n, "fallback stat home FR")
expect_count(ROOT / "index.html", r"Rechercher dans les (\d+) sessions", n, "placeholder home FR")
expect_count(ROOT / "index.html", r'id="journal-count-link"[^>]*>(\d+) entrées', n, "count-link home FR")
expect_count(ROOT / "en" / "index.html", r'id="stat-sessions">(\d+)<', len(en), "fallback stat home EN")
expect_count(ROOT / "en" / "index.html", r"Search across (\d+) sessions", len(en), "placeholder home EN")
expect_count(ROOT / "en" / "index.html", r'id="journal-count-link"[^>]*>(\d+) entries', len(en), "count-link home EN")

# Sitemap : chaque entrée journal FR doit y figurer
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
missing = sorted(s for s in fr if f"/journal/{s}.html" not in sitemap)
if missing:
    err(f"sitemap.xml : entrées journal absentes : {missing}")

# Nombre d'items dans journal/index.html
li_count = len(re.findall(r'<li class="entry"', (ROOT / "journal" / "index.html").read_text(encoding="utf-8")))
if li_count != n:
    err(f"journal/index.html : {li_count} <li class=\"entry\"> pour {n} fichiers")

if ERRORS:
    print(f"❌ {len(ERRORS)} problème(s) de cohérence :")
    for e in ERRORS:
        print(" -", e)
    sys.exit(1)
print(f"✅ Site cohérent : {n} entrées de journal (FR=EN), index, llms.txt, sitemap et compteurs alignés.")
