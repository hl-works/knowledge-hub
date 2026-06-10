#!/usr/bin/env python3
"""Génère llms-full.txt et en/llms-full.txt depuis le contenu du site (idempotent).

Sections : Méthode · Guides (un par page) · Lexique (depuis glossaire.json) ·
Journal (toutes les entrées, antéchronologique) · À propos.
Le texte est extrait du <main> de chaque page (les blocs CTA/contact sont exclus).

À relancer après tout ajout/modif de contenu :
    python3 scripts/build_llms_full.py
(un workflow GitHub Actions le fait aussi automatiquement au push sur main)
"""
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://hugolahutte.github.io/knowledge-hub"
BAR = "=" * 64

HEADER_FR = """# Knowledge Hub — Hugo Lahutte (version étendue)

> Journal de bord et méthode de Hugo Lahutte, qui construit ses projets et son contenu avec Claude. Build in public.

Auteur : Hugo Lahutte — hugo@hl-consulting.tech — DG de Cobra, éditeur de Haute Fidélité, fondateur de HL Consulting.
Localisation : Chennevières-sur-Marne, Île-de-France, France.
Parcours : 17 ans chez Son-Vidéo.com (n°1 français HiFi/home-cinéma en ligne) — achats, vente, stratégie commerciale, marketing/communication, partenariats ; croissance de 10 à 62 M€. Depuis 2024 : DG de Cobra (oct. 2024), éditeur & directeur de publication de Haute Fidélité (janv. 2025, magazine de référence 30+ ans relancé), fondateur de HL Consulting (juil. 2024). Enseignant marketing à Creapole-ESDI. Passionné de musique, cinéma et culture japonaise (Japan Expo 2004-2009).
LinkedIn : https://www.linkedin.com/in/hugo-lahutte — X : https://x.com/hugolh_ai

Document généré automatiquement depuis le contenu du site (scripts/build_llms_full.py). Dernière mise à jour : {date}
"""

HEADER_EN = """# Knowledge Hub — Hugo Lahutte (extended version)

> Hugo Lahutte's worklog and method — building his projects and content with Claude. Build in public.

Author: Hugo Lahutte — hugo@hl-consulting.tech — CEO of Cobra, publisher of Haute Fidélité, founder of HL Consulting.
Location: Chennevières-sur-Marne, Île-de-France, France.
Background: 17 years at Son-Vidéo.com (France's #1 HiFi/home cinema e-retailer) — purchasing, sales, commercial strategy, marketing/communications, partnerships; growth from €10M to €62M. Since 2024: CEO of Cobra (Oct. 2024), publisher & editorial director of Haute Fidélité (Jan. 2025, 30+ year reference magazine relaunched), founder of HL Consulting (Jul. 2024). Marketing lecturer at Creapole-ESDI. Passionate about music, cinema, and Japanese culture (Japan Expo 2004–2009).
LinkedIn: https://www.linkedin.com/in/hugo-lahutte — X: https://x.com/hugolh_ai

Document generated automatically from the site content (scripts/build_llms_full.py). Last updated: {date}
"""

BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "figcaption", "blockquote", "pre"}
VOID_TAGS = {"img", "br", "hr", "input", "meta", "link", "source", "embed", "wbr", "track", "area", "col"}


class MainExtractor(HTMLParser):
    """Texte du <main>, blocs séparés par des sauts de ligne, CTA/contact exclus."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = 0
        self.skip = 0
        self.stack = []  # (tag, ouvre_une_zone_skip)
        self.blocks = []
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        if tag == "main":
            self.in_main += 1
            return
        if not self.in_main:
            return
        a = dict(attrs)
        opens_skip = tag in ("script", "style", "nav") \
            or a.get("id") == "contact" or "cta-band" in (a.get("class") or "")
        self.stack.append((tag, opens_skip))
        if opens_skip:
            self.skip += 1
        elif not self.skip and tag in ("h2", "h3", "h4"):
            self._flush()
        elif not self.skip and tag == "li":
            self._flush()
            self.cur.append("- ")

    def handle_endtag(self, tag):
        if tag == "main" and self.in_main:
            self.in_main -= 1
            return
        if not self.in_main:
            return
        # dépile jusqu'au tag correspondant (tolérant aux balises mal fermées)
        while self.stack:
            t, opened_skip = self.stack.pop()
            if opened_skip:
                self.skip = max(0, self.skip - 1)
            if t == tag:
                break
        if not self.skip and tag in BLOCK_TAGS:
            self._flush()

    def handle_data(self, data):
        if self.in_main and not self.skip:
            self.cur.append(data)

    def _flush(self):
        txt = re.sub(r"[ \t\n]+", " ", "".join(self.cur)).strip()
        if txt:
            self.blocks.append(txt)
        self.cur = []

    def text(self):
        self._flush()
        return "\n".join(self.blocks)


def meta(src: str, pattern: str) -> str:
    m = re.search(pattern, src, re.S)
    return m.group(1).strip() if m else ""


def page_section(path: Path, url: str, lang: str) -> str:
    src = path.read_text(encoding="utf-8")
    title = meta(src, r"<title>(.*?)(?:\s+—.*)?</title>")
    desc = meta(src, r'name="description" content="(.*?)"')
    pub = meta(src, r'"datePublished":\s*"([\d-]+)"') or meta(src, r'article:published_time" content="([\d-]+)"')
    ext = MainExtractor()
    ext.feed(src)
    label_url = "URL :" if lang == "fr" else "URL:"
    label_pub = "Publié :" if lang == "fr" else "Published:"
    head = [BAR, title.upper(), f"{label_url} {url}"]
    if pub:
        head.append(f"{label_pub} {pub}")
    head.append(BAR)
    body = (desc + "\n\n" if desc else "") + ext.text()
    return "\n".join(head) + "\n\n" + body.strip() + "\n"


def journal_entries(journal_dir: Path) -> list:
    """[(date, slug)] antéchronologique, depuis les pages elles-mêmes."""
    entries = []
    for f in journal_dir.glob("*.html"):
        if f.name in ("index.html", "_template.html"):
            continue
        src = f.read_text(encoding="utf-8")
        pub = meta(src, r'"datePublished":\s*"([\d-]+)"') or "0000-00-00"
        entries.append((pub, f))
    return sorted(entries, key=lambda e: (e[0], e[1].name), reverse=True)


def guide_order(guides_index: Path) -> list:
    """Slugs dans l'ordre des cartes de guides/index.html."""
    src = guides_index.read_text(encoding="utf-8")
    return re.findall(r'class="guide-card" href="([^"]+\.html)"', src)


def lexique_section(gloss_path: Path, lang: str) -> str:
    data = json.loads(gloss_path.read_text(encoding="utf-8"))
    if lang == "fr":
        head = [BAR, "LEXIQUE — LES TERMES DE L'IA, DÉFINIS SIMPLEMENT",
                f"URL : {BASE}/lexique/", BAR]
    else:
        head = [BAR, "GLOSSARY — AI TERMS, PLAINLY DEFINED",
                f"URL: {BASE}/en/lexique/", BAR]
    lines = [f"- {e['terme']} : {e['definition']}" for e in data]
    return "\n".join(head) + "\n\n" + "\n".join(lines) + "\n"


def build(lang: str) -> None:
    prefix = ROOT if lang == "fr" else ROOT / "en"
    url_prefix = BASE if lang == "fr" else BASE + "/en"
    out = [(HEADER_FR if lang == "fr" else HEADER_EN).format(date=date.today().isoformat())]

    out.append(page_section(prefix / "how-to" / "index.html", f"{url_prefix}/how-to/", lang))
    for slug in guide_order(prefix / "guides" / "index.html"):
        out.append(page_section(prefix / "guides" / slug, f"{url_prefix}/guides/{slug}", lang))
    gloss = prefix / "lexique" / ("glossaire.json" if lang == "fr" else "glossaire.en.json")
    out.append(lexique_section(gloss, lang))
    for pub, f in journal_entries(prefix / "journal"):
        out.append(page_section(f, f"{url_prefix}/journal/{f.name}", lang))
    out.append(page_section(prefix / "a-propos" / "index.html", f"{url_prefix}/a-propos/", lang))

    target = prefix / "llms-full.txt"
    target.write_text("\n\n".join(out), encoding="utf-8")
    print(f"{target.relative_to(ROOT)} : {len(out) - 1} sections, {target.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    build("fr")
    build("en")
