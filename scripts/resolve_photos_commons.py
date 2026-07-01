#!/usr/bin/env python3
"""Résout les photo_query de l'Atlas d'Asie en images libres de droits.

Pour chaque `photo_query` des onglets Lieux / Miam / Recits / Bestiaire,
interroge l'API Wikimedia Commons (aucune clé nécessaire), garde la première
image en licence libre (CC / domaine public, bitmap, ≥ 500 px) et écrit un
mapping statique dans atlas-asie-app/public/fixtures/photos.json :

    { "<photo_query>": { "src": <thumb 640px>, "credit": "Auteur — Licence",
                         "page": <page Commons> }, … }

Le site lit ce fichier côté client (zéro appel API au runtime, hotlink
upload.wikimedia.org autorisé par la Wikimedia Foundation). Une photo perso
dans la Sheet reste prioritaire (stratégie « photo perso d'abord » du brief).

À relancer quand des photo_query changent :
    python3 scripts/resolve_photos_commons.py
(les requêtes déjà résolues sont conservées ; --force pour tout refaire)
"""
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = REPO / "atlas-asie-app" / "public" / "fixtures"
OUT = FIXTURES / "photos.json"
TABS = ["lieux", "miam", "recits", "bestiaire"]
API = "https://commons.wikimedia.org/w/api.php"
THUMB = 640

OK_LICENSE = re.compile(r"\b(CC|Public domain|No restrictions)", re.I)
STRIP_TAGS = re.compile(r"<[^>]+>")


def queries() -> list[str]:
    out: list[str] = []
    for tab in TABS:
        f = FIXTURES / f"{tab}.csv"
        if not f.exists():
            continue
        for row in csv.DictReader(f.open(encoding="utf-8")):
            q = (row.get("photo_query") or "").strip()
            if q and q not in out:
                out.append(q)
    return out


def search(q: str) -> dict | None:
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"{q} filetype:bitmap", "gsrnamespace": "6", "gsrlimit": "6",
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": str(THUMB),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "atlas-asie-photos/1.0 (hl-consulting.tech)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        lic = em.get("LicenseShortName", {}).get("value", "")
        if not OK_LICENSE.search(lic):
            continue
        if ii.get("width", 0) < 500 or ii.get("mime", "") not in ("image/jpeg", "image/png"):
            continue
        artist = STRIP_TAGS.sub("", em.get("Artist", {}).get("value", "")).strip() or "Wikimedia Commons"
        return {
            "src": ii.get("thumburl") or ii.get("url"),
            "credit": f"{artist[:60]} — {lic}, Wikimedia Commons",
            "page": ii.get("descriptionshorturl") or ii.get("descriptionurl", ""),
        }
    return None


def main() -> None:
    force = "--force" in sys.argv
    known: dict = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() and not force else {}
    qs = queries()
    todo = [q for q in qs if q not in known]
    print(f"{len(qs)} photo_query, {len(todo)} à résoudre")
    miss = []
    for i, q in enumerate(todo, 1):
        hit = None
        words = q.split()
        # requête complète, puis repli en retirant le dernier mot (min. 2 mots)
        for n in range(len(words), 1, -1):
            try:
                hit = search(" ".join(words[:n]))
            except Exception as e:  # réseau : on continue, le mapping reste partiel
                print(f"  ! {q} : {e}")
                break
            if hit:
                break
            time.sleep(0.2)
        if hit:
            known[q] = hit
        else:
            miss.append(q)
        if i % 10 == 0:
            print(f"  … {i}/{len(todo)}")
        time.sleep(0.3)
    # on ne garde que les requêtes encore présentes dans les CSV
    known = {q: v for q, v in known.items() if q in qs}
    OUT.write_text(json.dumps(known, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"photos.json : {len(known)} images résolues, {len(miss)} sans résultat")
    for q in miss:
        print(f"  (sans image : {q})")


if __name__ == "__main__":
    main()
