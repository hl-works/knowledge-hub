#!/usr/bin/env python3
"""Met à jour la grille vidéos de la home (`index.html`, section « La chaîne
YouTube ») avec les dernières vidéos de la série « Voyage en Haute-Fidélité »
de la chaîne @hautefidelitemag.

Zéro dépendance (stdlib pure, comme le reste du repo). Idempotent : n'écrit que
si les IDs changent. Sans clé API : on lit la page /videos de la chaîne pour les
IDs, et on valide/titre chaque vidéo via l'endpoint oembed public de YouTube.

Robustesse : en cas de souci réseau ou de trop peu de vidéos trouvées, on NE
touche à rien (on garde la grille existante) et on sort en succès — jamais de
grille cassée sur la prod.

Usage :
    python3 scripts/update_home_videos.py            # met à jour si besoin
    python3 scripts/update_home_videos.py --dry-run  # affiche sans écrire
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

CHANNEL_ID = "UCbR9gOW3DHEeQZ92S6dx2ig"   # @hautefidelitemag — Haute-Fidélité Magazine
CHANNEL_HANDLE = "hautefidelitemag"        # oembed renvoie le @handle, pas l'UC id
TITLE_FILTER = "voyage"                    # série « Voyage en Haute-Fidélité »
COUNT = 3                                  # nombre de vignettes dans la grille
SCAN = 15                                  # nb de vidéos récentes à examiner
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")


def _get(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "fr-FR,fr;q=0.9",
        # Cookie de consentement : sinon YouTube sert un mur RGPD sans contenu
        # aux IP datacenter (dont les runners GitHub Actions).
        "Cookie": "CONSENT=YES+cb.20210328-17-p0.en+FX+000",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def _latest_ids(channel_id: str) -> list[str]:
    """IDs vidéo de l'onglet /videos, dans l'ordre d'affichage (récents d'abord)."""
    page = _get(f"https://www.youtube.com/channel/{channel_id}/videos")
    ids: list[str] = []
    for m in re.finditer(r'"videoId":"([\w-]{11})"', page):
        vid = m.group(1)
        if vid not in ids:
            ids.append(vid)
    return ids


def _oembed(vid: str) -> tuple[str, str] | tuple[None, None]:
    """(titre, author_url) via oembed public — sert aussi à valider la chaîne."""
    try:
        data = json.loads(_get(
            "https://www.youtube.com/oembed?url="
            f"https://www.youtube.com/watch?v={vid}&format=json"
        ))
        return data.get("title", ""), data.get("author_url", "")
    except (urllib.error.URLError, ValueError, TimeoutError):
        return None, None


def pick_videos() -> list[str]:
    """Renvoie jusqu'à COUNT IDs : les dernières vidéos « Voyage » de la chaîne.
    Repli sur les dernières vidéos tout court si moins de COUNT « Voyage »."""
    ids = _latest_ids(CHANNEL_ID)[:SCAN]
    matched: list[str] = []   # titres contenant TITLE_FILTER
    channel: list[str] = []   # toutes les vidéos valides de la chaîne (repli)
    for vid in ids:
        title, author = _oembed(vid)
        if not title or CHANNEL_HANDLE not in (author or "").lower():
            continue
        channel.append(vid)
        if TITLE_FILTER.lower() in title.lower():
            matched.append(vid)
        if len(matched) >= COUNT:
            break
    return matched[:COUNT] if len(matched) >= COUNT else channel[:COUNT]


def _cell(vid: str) -> str:
    return (
        '        <div class="e-yt-cell"><button type="button" class="lite-yt" '
        f'data-yt="{vid}" aria-label="Lire la vidéo YouTube / Play YouTube video" '
        f"style=\"background-image:url('https://i.ytimg.com/vi/{vid}/hqdefault.jpg');\">"
        '<span class="lite-yt__play"></span></button></div>'
    )


# Ancré sur la fermeture suivie de `.e-media-cta` → évite le piège des <div> imbriqués.
_GRID_RE = re.compile(
    r'(<div class="e-yt-grid">).*?(\n\s*</div>\s*\n\s*<div class="e-media-cta">)',
    re.DOTALL,
)


def main() -> int:
    dry = "--dry-run" in sys.argv
    try:
        vids = pick_videos()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"[update_home_videos] réseau KO ({exc}) — grille inchangée.", file=sys.stderr)
        return 0
    if len(vids) < COUNT:
        print(f"[update_home_videos] seulement {len(vids)} vidéo(s) trouvée(s) — grille inchangée.",
              file=sys.stderr)
        return 0

    html = INDEX.read_text(encoding="utf-8")
    m = _GRID_RE.search(html)
    if not m:
        print("[update_home_videos] grille .e-yt-grid introuvable — abandon.", file=sys.stderr)
        return 1

    new_grid = m.group(1) + "\n" + "\n".join(_cell(v) for v in vids) + m.group(2)
    new_html = html[:m.start()] + new_grid + html[m.end():]

    if new_html == html:
        print("[update_home_videos] déjà à jour :", ", ".join(vids))
        return 0
    if dry:
        print("[update_home_videos] (dry-run) mettrait :", ", ".join(vids))
        return 0

    INDEX.write_text(new_html, encoding="utf-8")
    print("[update_home_videos] grille mise à jour :", ", ".join(vids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
