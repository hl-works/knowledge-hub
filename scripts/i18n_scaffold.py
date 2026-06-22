#!/usr/bin/env python3
"""
Socle i18n du Knowledge Hub — génère le miroir /en/ et injecte le balisage
bilingue (hreflang + sélecteur de langue) dans les pages FR.

Approche : miroir fidèle de l'arborescence sous /en/ (les liens de page
relatifs fonctionnent tels quels), réécriture des seules références d'assets
en chemins absolus /knowledge-hub/..., et des liens de nav/footer absolus
vers /knowledge-hub/en/...

Le CONTENU reste en français à ce stade : il est traduit lot par lot ensuite.
Le site reste donc déployable et fonctionnel à chaque commit.

Idempotent : peut être relancé sans dupliquer le balisage.
"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge-hub")
ORIGIN = "https://hl-consulting.tech"
BASE = "/knowledge-hub"

# Sections = liens de page (à préfixer par /en/). Pas les assets.
SECTIONS = ["how-to", "guides", "veille-ia", "lexique", "journal",
            "a-propos", "cobra", "haute-fidelite", "hifi-lovers",
            "perso", "flux-ia", "coffre"]

ASSETS = ["style.css", "search.js", "theme.js", "lexique.js",
          "site.webmanifest", "favicon.ico", "favicon.svg",
          "favicon-16.png", "favicon-32.png", "favicon-48.png",
          "apple-touch-icon.png"]

# Pages exclues du miroir/injection
EXCLUDE = {"404.html", "journal/_template.html"}
EXCLUDE_DIRS = {"coffre"}  # vault privé/chiffré : sensible, non traduit

def site_path(rel):
    """rel = chemin relatif depuis la racine repo -> chemin site /knowledge-hub/..."""
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel

def all_pages():
    out = []
    for dirpath, _, files in os.walk(ROOT):
        if "/.git" in dirpath or "/scripts" in dirpath or "/en" in dirpath.replace(ROOT, "", 1):
            continue
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
            if rel in EXCLUDE:
                continue
            top = rel.split("/")[0]
            if top in EXCLUDE_DIRS:
                continue
            # pages top-level autres que index (ex : 404 déjà exclue) -> skip
            if "/" not in rel and rel != "index.html":
                continue
            out.append(rel)
    return sorted(out)

def switcher_li(target_href, lang, label, aria):
    return ('<li class="nav__lang"><a href="%s" hreflang="%s" lang="%s" '
            'aria-label="%s" title="%s">%s</a></li>'
            % (target_href, lang, lang, aria, aria, label))

def inject_hreflang(html, fr_full, en_full, after_canonical=True):
    block = ('\n<link rel="alternate" hreflang="fr" href="%s">'
             '\n<link rel="alternate" hreflang="en" href="%s">'
             '\n<link rel="alternate" hreflang="x-default" href="%s">'
             % (fr_full, en_full, fr_full))
    if 'hreflang="en"' in html:
        return html  # déjà injecté
    # insère après la ligne canonical
    m = re.search(r'(<link rel="canonical"[^>]*>)', html)
    if m:
        return html[:m.end()] + block + html[m.end():]
    return html

def inject_switcher(html, li):
    if 'nav__lang' in html:
        return html
    return html.replace(
        '<ul class="nav__links" id="nav-links">',
        '<ul class="nav__links" id="nav-links">\n      ' + li, 1)

def make_en(html, rel, fr_full, en_full):
    # 1. lang
    html = html.replace('<html lang="fr">', '<html lang="en">', 1)
    # 2. assets -> absolus
    asset_alt = "|".join(re.escape(a) for a in ASSETS)
    html = re.sub(r'(href|src)="(\.\./)?(' + asset_alt + r')',
                  r'\1="' + BASE + r'/\3', html)
    html = re.sub(r'(href|src)="(\.\./)?assets/',
                  r'\1="' + BASE + '/assets/', html)
    # 3. liens de page absolus -> /en/
    html = html.replace('href="%s/"' % BASE, 'href="%s/en/"' % BASE)
    for s in SECTIONS:
        html = html.replace('href="%s/%s' % (BASE, s),
                            'href="%s/en/%s' % (BASE, s))
    # 4. canonical + og:url -> EN
    html = html.replace('href="%s"' % fr_full, 'href="%s"' % en_full)
    html = html.replace('content="%s"' % fr_full, 'content="%s"' % en_full)
    # 5. og:locale
    html = html.replace(
        '<meta property="og:locale" content="fr_FR">',
        '<meta property="og:locale" content="en_US">\n'
        '<meta property="og:locale:alternate" content="fr_FR">', 1)
    # 6. JSON-LD inLanguage
    html = html.replace('fr-FR', 'en-US')
    # 7. hreflang
    html = inject_hreflang(html, fr_full, en_full)
    # 8. switcher -> lien vers FR
    fr_site = fr_full.replace(ORIGIN, "")
    html = inject_switcher(html, switcher_li(fr_site, "fr", "FR",
                                             "Lire en français"))
    return html

def make_fr(html, rel, fr_full, en_full):
    en_site = en_full.replace(ORIGIN, "")
    # og:locale alternate
    if 'og:locale:alternate' not in html:
        html = html.replace(
            '<meta property="og:locale" content="fr_FR">',
            '<meta property="og:locale" content="fr_FR">\n'
            '<meta property="og:locale:alternate" content="en_US">', 1)
    html = inject_hreflang(html, fr_full, en_full)
    html = inject_switcher(html, switcher_li(en_site, "en", "EN",
                                             "Read in English"))
    return html

def main():
    pages = all_pages()
    n_en = n_fr = 0
    for rel in pages:
        sp = site_path(rel)
        fr_full = ORIGIN + sp
        en_full = ORIGIN + sp.replace(BASE + "/", BASE + "/en/", 1)
        src = os.path.join(ROOT, rel)
        with open(src, encoding="utf-8") as fh:
            html = fh.read()

        # --- FR : injection en place ---
        fr_html = make_fr(html, rel, fr_full, en_full)
        if fr_html != html:
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(fr_html)
            n_fr += 1

        # --- EN : miroir ---
        en_rel = "en/" + rel
        en_path = os.path.join(ROOT, en_rel)
        os.makedirs(os.path.dirname(en_path), exist_ok=True)
        en_html = make_en(html, rel, fr_full, en_full)
        with open(en_path, "w", encoding="utf-8") as fh:
            fh.write(en_html)
        n_en += 1

    print("Pages FR balisées : %d" % n_fr)
    print("Pages EN générées : %d" % n_en)

if __name__ == "__main__":
    main()
