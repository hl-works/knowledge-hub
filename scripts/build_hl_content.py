#!/usr/bin/env python3
"""Régénère hl-content/index.html depuis hl-content/_template.html + status.json.

Source de vérité = hl-content/status.json (les briques et leur statut). Le script
recalcule la barre d'avancement, la liste, le résumé chiffré et la date de mise à
jour, puis réécrit index.html. Idempotent (même entrée → même sortie) et ne touche
QU'À index.html. Lancé par .github/workflows/hl-content-build.yml au push du
manifeste (+ cron hebdo). En local : python3 scripts/build_hl_content.py
"""
import html
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "hl-content"

STATUS = {
    "done":  {"item": "done",  "idx": "✓", "pill": "ok",   "txt": "fait",    "seg": "ok"},
    "ready": {"item": "ready", "idx": "→", "pill": "wip",  "txt": "prêt",    "seg": "ready"},
    "next":  {"item": "next",  "idx": "•", "pill": "todo", "txt": "à venir", "seg": ""},
}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def plur(n: int, mot: str) -> str:
    return f"{n} {mot}{'s' if n > 1 else ''}"


def date_maj() -> str:
    """Date de la dernière modif de status.json (via git) → idempotent au fil des
    re-runs ; repli sur aujourd'hui si git indisponible."""
    iso = None
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", "hl-content/status.json"],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        iso = out or None
    except Exception:
        iso = None
    d = date.fromisoformat(iso) if iso else date.today()
    return f"{d.day} {MOIS[d.month - 1]} {d.year}"


def main() -> None:
    tpl = (BASE / "_template.html").read_text(encoding="utf-8")
    items = json.loads((BASE / "status.json").read_text(encoding="utf-8"))["items"]

    # Liste d'avancement
    rows = []
    for it in items:
        st = STATUS[it["status"]]
        idx = esc(str(it.get("idx", st["idx"])))
        rows.append(
            f'        <div class="item {st["item"]}"><span class="idx mono">{idx}</span>'
            f'<span class="t">{esc(it["label"])} <small>{esc(it["sub"])}</small></span>'
            f'<span class="pill {st["pill"]}">{st["txt"]}</span></div>'
        )
    track = "\n".join(rows)

    # Barre : un segment par brique, couleur selon le statut
    def seg(it):
        s = STATUS[it["status"]]["seg"]
        return f'<span class="pseg {s}"></span>' if s else '<span class="pseg"></span>'
    progress = "        " + "".join(seg(it) for it in items)

    # Résumé chiffré
    n_done = sum(1 for it in items if it["status"] == "done")
    n_ready = sum(1 for it in items if it["status"] == "ready")
    n_next = sum(1 for it in items if it["status"] == "next")
    parts = [p for p in [
        plur(n_done, "fait") if n_done else "",
        plur(n_ready, "prêt") if n_ready else "",
        f"{n_next} à venir" if n_next else "",
    ] if p]
    cap = " · ".join(parts)
    label = " · ".join(p for p in [
        plur(n_done, "faite") if n_done else "",
        plur(n_ready, "prête") if n_ready else "",
        f"{n_next} à venir" if n_next else "",
    ] if p)

    updated = (f'Mis à jour le {date_maj()} · régénéré automatiquement depuis '
               f'<span class="mono">status.json</span>.')

    out = (tpl
           .replace("{{CAP}}", esc(cap))
           .replace("{{PBAR_LABEL}}", esc(label))
           .replace("{{PROGRESS}}", progress)
           .replace("{{TRACK}}", track)
           .replace("{{UPDATED}}", updated))

    (BASE / "index.html").write_text(out, encoding="utf-8")
    print(f"index.html régénéré : {len(items)} briques · {cap}")


if __name__ == "__main__":
    main()
