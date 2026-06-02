#!/usr/bin/env python3
"""
Passe de cohérence du chrome (nav + footer) des pages EN.

- Remplace le bloc <footer class="footer">…</footer> par le footer EN de
  référence (identique sur toutes les pages) → footer parfaitement uniforme.
- Normalise les libellés de la nav (header) et du JSON-LD de navigation :
  traduit les libellés FR restants et harmonise les variantes
  (Lexicon→Glossary, Get in touch→Connect, AI Monitor→AI Watch).
  N'agit QUE dans la zone skip-link + <header>…</header> et dans la zone
  </main>…<footer (JSON-LD de nav) — jamais dans le corps de page.

Idempotent. Ne touche pas aux pages FR.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = os.path.join(ROOT, "en")
REF = os.path.join(EN, "index.html")

def extract_footer(html):
    m = re.search(r'<footer class="footer">.*?</footer>', html, re.S)
    return m.group(0) if m else None

CANON_FOOTER = extract_footer(open(REF, encoding="utf-8").read())
assert CANON_FOOTER, "footer de référence introuvable dans en/index.html"

# Remplacements appliqués UNIQUEMENT dans les zones chrome (ordre = important)
REPL = [
    ('aria-label="Rechercher (touche /)"', 'aria-label="Search (press /)"'),
    ('aria-label="Thème : automatique"', 'aria-label="Theme: automatic"'),
    ('aria-label="Principale"', 'aria-label="Main"'),
    ('aria-label="Rechercher"', 'aria-label="Search"'),
    ('title="Thème"', 'title="Theme"'),
    ('Aller au contenu', 'Skip to content'),
    ('>Méthode<', '>Method<'),
    ('"name": "Méthode"', '"name": "Method"'),
    ('>Veille IA<', '>AI Watch<'),
    ('"name": "Veille IA"', '"name": "AI Watch"'),
    ('>À propos<', '>About<'),
    ('"name": "À propos"', '"name": "About"'),
    ('>Projets<', '>Projects<'),
    ('>Échanger<', '>Connect<'),
    ('>Lexique<', '>Glossary<'),
    ('"name": "Lexique"', '"name": "Glossary"'),
    ('>Lexicon<', '>Glossary<'),
    ('>Get in touch<', '>Connect<'),
    ('>AI Monitor<', '>AI Watch<'),
]

def normalize_region(html, start_pat, end_pat):
    m = re.search(start_pat, html)
    if not m: return html, False
    e = re.search(end_pat, html[m.start():])
    if not e: return html, False
    a, b = m.start(), m.start() + e.end()
    seg = html[a:b]
    new = seg
    for src, dst in REPL:
        new = new.replace(src, dst)
    if new == seg: return html, False
    return html[:a] + new + html[b:], True

def main():
    n_footer = n_nav = 0
    for dp, _, files in os.walk(EN):
        for f in files:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f)
            html = open(p, encoding="utf-8").read()
            orig = html
            # 1) footer canonique
            cur = extract_footer(html)
            if cur and cur != CANON_FOOTER:
                html = html.replace(cur, CANON_FOOTER, 1); n_footer += 1
            # 2) header nav (skip-link -> </header>)
            html, c1 = normalize_region(html, r'<a class="skip-link"', r'</header>')
            # 3) JSON-LD de nav (</main> -> <footer)
            html, c2 = normalize_region(html, r'</main>', r'<footer class="footer">')
            if c1 or c2: n_nav += 1
            if html != orig:
                open(p, "w", encoding="utf-8").write(html)
    print("Footers canonisés : %d | Navs normalisées : %d" % (n_footer, n_nav))

if __name__ == "__main__":
    main()
