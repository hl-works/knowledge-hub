#!/usr/bin/env python3
"""Met à jour l'encart « dernier numéro » du magazine sur la home (`index.html`)
avec le dernier numéro de Haute Fidélité publié sur la boutique Shopify.

Zéro dépendance (stdlib pure). Sans clé API : on lit la fiche produit publique
`…/products/haute-fidelite-<N>.json` de store.hautefidelite-hifi.com. On part du
numéro actuel affiché sur la home et on sonde les numéros suivants pour trouver
le plus récent en ligne.

Met à jour, dans le SEUL bloc « cover » du magazine (pas le hors-série) :
lien boutique, image de couverture, texte alt et libellé « n°N ».

Idempotent, fail-safe : réseau KO ou rien de neuf → home inchangée, sortie OK.

Usage :
    python3 scripts/update_home_magazine.py
    python3 scripts/update_home_magazine.py --dry-run
"""
from __future__ import annotations

import html as _html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

STORE = "https://store.hautefidelite-hifi.com"
HANDLE = "haute-fidelite-{}"     # slug produit par numéro
PROBE_AHEAD = 6                  # nb de numéros suivants à sonder
UA = "Mozilla/5.0 (compatible; hl-consulting-bot/1.0; +https://hl-consulting.tech)"

# Le bloc « cover » du magazine (celui qui pointe vers products/haute-fidelite-<N>).
_COVER_RE = re.compile(
    r'<a class="e-cover" href="[^"]*?/products/haute-fidelite-\d+".*?</a>',
    re.DOTALL,
)


def _get(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _product(number: int) -> dict | None:
    """Fiche produit JSON d'un numéro, ou None si absent (404)."""
    try:
        raw = _get(f"{STORE}/products/{HANDLE.format(number)}.json")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    try:
        return json.loads(raw).get("product")
    except ValueError:
        return None


def _latest_number(current: int) -> tuple[int, dict] | tuple[None, None]:
    """Numéro le plus récent en ligne (>= current) + sa fiche produit."""
    latest, prod = None, None
    # le numéro courant lui-même (au cas où la home serait déjà en retard d'une source)
    p = _product(current)
    if p:
        latest, prod = current, p
    n = current + 1
    misses = 0
    while misses < PROBE_AHEAD:
        p = _product(n)
        if p:
            latest, prod = n, p
            misses = 0
        else:
            misses += 1
        n += 1
    return (latest, prod) if latest else (None, None)


def _cover_url(prod: dict) -> str | None:
    img = (prod.get("image") or {}).get("src")
    if img:
        return img
    images = prod.get("images") or []
    return images[0].get("src") if images else None


def _featured_gear(prod: dict) -> str:
    """Produit vedette « en couverture » (best-effort, pour le texte alt)."""
    text = _html.unescape(re.sub(r"<[^>]+>", " ", prod.get("body_html", "")))
    text = re.sub(r"\s+", " ", text)
    m = re.search(
        r"[Ee]n couverture[,:]?\s*(?:retrouvez\s+)?"
        r"(?:la\s+|le\s+|les\s+|l['’]|une\s+|un\s+)?"
        r"(?:spectaculaire\s+|magnifique\s+|nouvelle\s+|nouveau\s+|superbe\s+|sublime\s+)?"
        r"([A-ZÉÈÀ][\w '’\-\.]{2,45}?)(?:,|\.|\s+accompagn|\s+qui\s|\s+et\s)",
        text,
    )
    return m.group(1).strip() if m else ""


def _update_cover(block: str, number: int, cover: str, alt: str) -> str:
    block = re.sub(r"(/products/haute-fidelite-)\d+", rf"\g<1>{number}", block)
    block = re.sub(r'(<img src=")[^"]*"', rf'\g<1>{cover}"', block, count=1)
    block = re.sub(r'(\balt=")[^"]*"', rf'\g<1>{alt}"', block, count=1)
    block = re.sub(r"(Haute Fidélité · n°)\d+", rf"\g<1>{number}", block)
    return block


def main() -> int:
    dry = "--dry-run" in sys.argv
    html_text = INDEX.read_text(encoding="utf-8")

    m = _COVER_RE.search(html_text)
    if not m:
        print("[update_home_magazine] bloc cover magazine introuvable — abandon.", file=sys.stderr)
        return 1
    block = m.group(0)

    cur = re.search(r"/products/haute-fidelite-(\d+)", block)
    if not cur:
        print("[update_home_magazine] numéro courant illisible — abandon.", file=sys.stderr)
        return 1
    current = int(cur.group(1))

    try:
        number, prod = _latest_number(current)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"[update_home_magazine] réseau KO ({exc}) — home inchangée.", file=sys.stderr)
        return 0
    if not prod:
        print("[update_home_magazine] aucune fiche produit trouvée — home inchangée.", file=sys.stderr)
        return 0

    cover = _cover_url(prod)
    if not cover:
        print("[update_home_magazine] pas d'image de couverture — home inchangée.", file=sys.stderr)
        return 0
    gear = _featured_gear(prod)
    alt = f"Couverture de Haute Fidélité n°{number}"
    if gear:
        alt += f" — {gear}"

    new_block = _update_cover(block, number, cover, alt)
    if new_block == block:
        print(f"[update_home_magazine] déjà à jour (n°{current}).")
        return 0

    if dry:
        print(f"[update_home_magazine] (dry-run) n°{current} → n°{number} | {alt}")
        return 0

    INDEX.write_text(html_text[:m.start()] + new_block + html_text[m.end():], encoding="utf-8")
    print(f"[update_home_magazine] mis à jour : n°{current} → n°{number} ({gear or 'sans vedette'}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
