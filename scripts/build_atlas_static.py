#!/usr/bin/env python3
"""Artefacts SEO/GEO de l'Atlas d'Asie (idempotent) : statique + sitemap + llms.txt.

Pourquoi : les pages de l'atlas rendent les CSV (Google Sheet ou fixtures)
côté client, or les crawlers IA (GPTBot, ClaudeBot, PerplexityBot…)
n'exécutent pas le JavaScript. Ce script :

1. injecte un rendu HTML statique des fiches Pays dans atlas-asie/pays/index.html
   et de la timeline Parcours dans atlas-asie/parcours/index.html (entre
   marqueurs, à la place des skeletons ; le JS de la page écrase ce contenu au
   chargement chez les visiteurs — progressive enhancement) ;
2. régénère atlas-asie/sitemap.xml (référencé dans robots.txt) ;
3. régénère atlas-asie/llms.txt (index GEO du sous-site).

Source de données = la même que le site : les URLs CSV publiées déclarées dans
atlas-asie-app/src/lib/sheets.ts, avec repli sur atlas-asie/fixtures/<clé>.csv
quand l'URL est vide. ⚠️ On ne lit QUE Parcours / Pays (jamais Passeport,
Financier ni l'onglet Vols privé — règle de sécurité du brief).

À relancer après un rebuild Astro (qui purge ces artefacts — c'est attendu)
ou une maj des données :
    python3 scripts/build_atlas_static.py
(le workflow site-autobuild.yml le fait automatiquement, cron quotidien inclus)
"""
import csv
import html
import io
import re
import unicodedata
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS = REPO / "atlas-asie"
SHEETS_TS = REPO / "atlas-asie-app" / "src" / "lib" / "sheets.ts"
ORIGIN = "https://hl-consulting.tech"
BASE_URL = f"{ORIGIN}/atlas-asie/"

MARK = {
    "pays": ("<!-- atlas-pays-static:start (généré par scripts/build_atlas_static.py) -->",
             "<!-- atlas-pays-static:end -->"),
    "parcours": ("<!-- atlas-parcours-static:start (généré par scripts/build_atlas_static.py) -->",
                 "<!-- atlas-parcours-static:end -->"),
}

# Palette / codes pays — miroir de src/pages/pays.astro (rendu client).
PAL = {
    "Kazakhstan": ("#FA4616", "#C9330B"), "Kirghizistan": ("#149E7C", "#0C5A5E"),
    "Mongolie": ("#E89B2E", "#B86A12"), "Chine": ("#F2516F", "#C12B49"),
    "Hong-Kong": ("#1E96C8", "#0C5A7E"), "Indonésie": ("#149E7C", "#0C5A5E"),
    "Malaisie": ("#E89B2E", "#B86A12"),
}
CODE = {
    "Kazakhstan": "KZ", "Kirghizistan": "KG", "Mongolie": "MN", "Chine": "CN",
    "Hong-Kong": "HK", "Indonésie": "ID", "Malaisie": "MY",
}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s))


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


# ---------- données ----------

def csv_urls() -> dict[str, str]:
    """Lit les csvUrl déclarées dans sheets.ts ('' => fixture locale)."""
    src = SHEETS_TS.read_text(encoding="utf-8")
    urls = {}
    for m in re.finditer(r"(\w+):\s*\{\s*key:\s*'(\w+)'[^}]*csvUrl:\s*'([^']*)'", src):
        urls[m.group(2)] = m.group(3)
    if not urls:
        raise SystemExit(f"{SHEETS_TS} : SHEET_TABS introuvable (format changé ?)")
    return urls


def load_tab(key: str) -> list[dict]:
    url = csv_urls().get(key, "")
    if url:
        with urllib.request.urlopen(url, timeout=30) as r:
            text = r.read().decode("utf-8")
    else:
        text = (ATLAS / "fixtures" / f"{key}.csv").read_text(encoding="utf-8")
    # tolérant aux lignes bancales : clés None (colonnes en trop) ignorées
    return [{k.strip(): (v if isinstance(v, str) else "").strip()
             for k, v in row.items() if k}
            for row in csv.DictReader(io.StringIO(text))]


# ---------- rendu statique : fiches pays ----------

def render_pays(rows: list[dict], recits: list[dict], miam: list[dict]) -> str:
    out = []
    for c in rows:
        pays = c.get("pays", "")
        if not pays:
            continue
        c1, c2 = PAL.get(pays, ("#FA4616", "#C9330B"))
        facts = "".join(
            f'<span class="chip"><b>{label}</b> {esc(val)}</span>'
            for label, val in (("Capitale", c.get("capitale")), ("Monnaie", c.get("monnaie")),
                               ("Langue", c.get("langue")), ("Population", c.get("population")))
            if val
        )
        funs = "".join(
            f"<li>{esc(f.strip())}</li>"
            for f in c.get("fun_facts", "").split("•") if f.strip()
        )
        out.append(
            f'<article class="fiche" id="{slug(pays)}">'
            f'<div class="banner" style="background:linear-gradient(135deg, {c1}, {c2})">'
            f'<span class="code">{CODE.get(pays, "")}</span>'
            f"<h2>{esc(pays)}</h2>"
            + (f'<div class="cap">{esc(c["capitale"])}</div>' if c.get("capitale") else "")
            + '</div><div class="body">'
            f'<div class="facts">{facts}</div>'
            + (f'<p class="histoire">{esc(c["histoire"])}</p>' if c.get("histoire") else "")
            + (f'<div class="block savais"><h3>Le savais-tu ?</h3><ul>{funs}</ul></div>' if funs else "")
            + recits_html(pays, recits)
            + miam_html(pays, miam)
            + "</div></article>"
        )
    return "\n".join(out)


def recits_html(pays: str, recits: list[dict]) -> str:
    mine = [r for r in recits if pays in [p.strip() for p in r.get("pays", "").split(",")]]
    if not mine:
        return ""
    out = ['<div class="block"><h3>La grande histoire</h3>']
    for r in mine:
        out.append(f'<details class="recit"><summary><span class="rtit">{esc(r["titre"])}</span>'
                   f'<span class="racc">{esc(r.get("accroche", ""))}</span></summary>'
                   f'<div class="rbody"><p>{esc(r.get("texte", ""))}</p></div></details>')
    out.append("</div>")
    return "".join(out)


def miam_html(pays: str, miam: list[dict]) -> str:
    mine = [m for m in miam if m.get("pays") == pays and m.get("plat")]
    if not mine:
        return ""
    items = "".join(
        f'<div class="mcard"><div class="mtxt"><div class="mn">{esc(m["plat"])}'
        + (f' <span class="ml">{esc(m["nom_local"])}</span>' if m.get("nom_local") and m["nom_local"] != m["plat"] else "")
        + f'</div><p class="md">{esc(m.get("description", ""))}</p></div></div>'
        for m in mine
    )
    return f'<div class="block"><h3>Miam</h3><div class="miam">{items}</div></div>'


# ---------- rendu statique : timeline parcours ----------

def iso(d: str) -> str:
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", d)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def render_parcours(rows: list[dict], lieux: list[dict]) -> str:
    rows = sorted((r for r in rows if r.get("ville")),
                  key=lambda r: int(r.get("ordre") or 0))
    out = ['<ol class="tl-static" style="list-style:none;margin:0;padding:0;display:grid;gap:18px;">']
    for r in rows:
        dates = ""
        if r.get("date_arrivee"):
            dates = f'<time datetime="{iso(r["date_arrivee"])}">{esc(r["date_arrivee"])}</time>'
            if r.get("date_depart"):
                dates += f' → <time datetime="{iso(r["date_depart"])}">{esc(r["date_depart"])}</time>'
        hotel = f' · Hébergement : {esc(r["hotel_nom"])}' if r.get("hotel_nom") else ""
        mes_lieux = [l for l in lieux if l.get("ordre") == r.get("ordre") and l.get("lieu")]
        avoir = ""
        if mes_lieux:
            lis = "".join(
                f'<li><b>{esc(l["lieu"])}</b>'
                + (f' <em>({esc(l["statut"])})</em>' if l.get("statut") else "")
                + f' — {esc(l.get("texte", ""))}</li>' for l in mes_lieux
            )
            avoir = f'<p style="margin:8px 0 0;font-weight:700;">À voir :</p><ul style="margin:4px 0 0;">{lis}</ul>'
        out.append(
            '<li style="border:2px solid var(--ink);border-radius:14px;background:var(--card);padding:16px 18px;">'
            f'<p style="margin:0;font-weight:700;">{esc(r["ville"])} — {esc(r.get("pays", ""))}</p>'
            f'<p style="margin:4px 0 0;font-size:.9rem;color:var(--ink-soft);">{dates}{hotel}</p>'
            + (f'<p style="margin:6px 0 0;color:var(--ink-soft);">{esc(r["description"])}</p>'
               if r.get("description") else "")
            + avoir
            + "</li>"
        )
    out.append("</ol>")
    return "\n".join(out)


def inject(page: Path, key: str, static_html: str, container_re: str) -> None:
    """Écrit le bloc entre marqueurs ; au premier passage, remplace les
    skeletons (.sk.sk-card) laissés par le build Astro dans le conteneur."""
    src = page.read_text(encoding="utf-8")
    start, end = MARK[key]
    block = f"{start}\n{static_html}\n{end}"
    if start in src:
        new = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, src, flags=re.S)
    else:
        anchor = re.compile(container_re + r'(?:\s*<div class="sk sk-card"></div>)+')
        new, n = anchor.subn(lambda m: m.group(1) + block, src, count=1)
        if not n:
            raise SystemExit(f"{page} : point d'injection introuvable ({container_re!r})")
    page.write_text(new, encoding="utf-8")
    print(f"{page.relative_to(REPO)} : rendu statique injecté")


# ---------- sitemap ----------

def build_sitemap() -> None:
    rels = (p.parent.relative_to(ATLAS).as_posix() for p in ATLAS.rglob("index.html"))
    pages = sorted("" if r == "." else r for r in rels)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in pages:
        loc = BASE_URL + (rel + "/" if rel else "")
        out.append("  <url><loc>%s</loc></url>" % loc)
    out.append("</urlset>\n")
    (ATLAS / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")
    print(f"atlas-asie/sitemap.xml : {len(pages)} URLs")


# ---------- llms.txt ----------

def first_sentence(s: str, maxlen: int = 220) -> str:
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    s = m.group(1) if m else s
    return s if len(s) <= maxlen else s[: maxlen - 1].rstrip() + "…"


def build_llms(pays: list[dict], parcours: list[dict]) -> None:
    stops = [r for r in parcours if r.get("ville")]
    dates = [d for r in stops for d in (r.get("date_arrivee"), r.get("date_depart")) if d and iso(d)]
    periode = f"du {min(dates, key=iso)} au {max(dates, key=iso)}" if dates else "été 2026"
    noms = [c["pays"] for c in pays if c.get("pays")]

    lines = [
        "# Atlas d'Asie — AMHE (famille Lahutte)",
        "",
        "> Carnet de voyage de la famille Lahutte (Hugo, Marion, Alexis, Emma) : "
        f"l'été 2026 en Asie, {periode}, du Kazakhstan à l'Indonésie. "
        "Suivi du parcours en direct (escales, hôtels, trajets, carte animée), fiches pays "
        "éducatives (evergreen, lisibles par un enfant) et photos. "
        "AMHE = les initiales de la famille, comme « âme ».",
        "",
        "Auteur : Hugo Lahutte (hugo@hl-consulting.tech) — voir https://hl-consulting.tech/knowledge-hub/llms.txt",
        "Site en français.",
        f"Voyage : {len(stops)} escales dans {len(noms)} pays et territoires ({', '.join(noms)}).",
        "",
        "## Pages",
        "",
        f"- [Accueil]({BASE_URL}): carte animée de l'itinéraire, bloc « où on est », compteurs du voyage.",
        f"- [Le parcours]({BASE_URL}parcours/): timeline des escales — villes, hôtels, dates, météo, incontournables à voir (badges UNESCO).",
        f"- [Les pays]({BASE_URL}pays/): fiches evergreen par pays — histoire, grands récits"
        " à lire, gastronomie, fun facts, infos pratiques à l'arrivée, animaux à repérer,"
        " mots à connaître, mini-quiz.",
        f"- [Nos hôtels]({BASE_URL}hotels/): tous les hébergements du voyage, dates et adresses.",
        f"- [Les trajets]({BASE_URL}trajets/): vols, bus et bateaux entre les escales.",
        f"- [Le carnet]({BASE_URL}carnet/): le fil Instagram du voyage.",
        f"- [Galerie]({BASE_URL}galerie/): toutes les photos des escales.",
        "",
        "## Les pays traversés (fiches evergreen)",
        "",
    ]
    for c in pays:
        if not c.get("pays"):
            continue
        infos = " · ".join(x for x in (
            f"capitale {c['capitale']}" if c.get("capitale") else "",
            f"monnaie {c['monnaie']}" if c.get("monnaie") else "",
            f"langue {c['langue']}" if c.get("langue") else "",
        ) if x)
        lines.append(f"- [{c['pays']}]({BASE_URL}pays/#{slug(c['pays'])}): {infos}. "
                     f"{first_sentence(c.get('histoire', ''))}")
    lines.append("")
    (ATLAS / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"atlas-asie/llms.txt : {len(noms)} pays, {len(stops)} escales")


if __name__ == "__main__":
    pays = load_tab("pays")
    parcours = load_tab("parcours")
    recits = load_tab("recits")
    miam = load_tab("miam")
    lieux = load_tab("lieux")
    inject(ATLAS / "pays" / "index.html", "pays", render_pays(pays, recits, miam),
           r'(<div id="fiches">)')
    inject(ATLAS / "parcours" / "index.html", "parcours", render_parcours(parcours, lieux),
           r'(<div class="timeline" id="timeline">)')
    build_sitemap()
    build_llms(pays, parcours)
