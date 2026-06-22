#!/usr/bin/env python3
"""
Régénère sitemap.xml en bilingue : pour chaque page FR du sitemap qui a une
jumelle EN sous /en/, émet l'URL FR et l'URL EN, chacune avec les alternances
hreflang (fr / en / x-default). Les pages sans jumelle EN (ex. coffre) restent
seules. Idempotent — relit le sitemap existant comme source des pages FR.
"""
import re, os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge-hub")
ORIGIN = "https://hl-consulting.tech"
BASE = "/knowledge-hub"
SITEMAP = os.path.join(ROOT, "sitemap.xml")

def field(b, tag):
    m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), b, re.S)
    return m.group(1).strip() if m else None

def en_rel(loc):
    path = loc.replace(ORIGIN + BASE + "/", "")
    if path == "":
        return "index.html"
    if path.endswith("/"):
        return path + "index.html"
    return path

def main():
    src = open(SITEMAP, encoding="utf-8").read()
    blocks = re.findall(r"<url>(.*?)</url>", src, re.S)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">']

    def alts(fr_loc, en_loc):
        return ['    <xhtml:link rel="alternate" hreflang="fr" href="%s"/>' % fr_loc,
                '    <xhtml:link rel="alternate" hreflang="en" href="%s"/>' % en_loc,
                '    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % fr_loc]

    seen = set()
    for b in blocks:
        loc = field(b, "loc")
        if not loc or loc.startswith(ORIGIN + BASE + "/en/"):
            continue  # on régénère les EN à partir des FR
        if loc in seen:
            continue
        seen.add(loc)
        lastmod = field(b, "lastmod")
        prio = field(b, "priority")
        has_en = os.path.exists(os.path.join(ROOT, "en", en_rel(loc)))
        en_loc = loc.replace(BASE + "/", BASE + "/en/", 1)

        def emit(l, with_alts):
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % l)
            if lastmod:
                out.append("    <lastmod>%s</lastmod>" % lastmod)
            if prio:
                out.append("    <priority>%s</priority>" % prio)
            if with_alts:
                out.extend(alts(loc, en_loc))
            out.append("  </url>")

        emit(loc, has_en)
        if has_en:
            emit(en_loc, True)

    out.append("</urlset>")
    open(SITEMAP, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("sitemap.xml régénéré (%d entrées <loc>)" % sum(1 for l in out if l.strip().startswith("<loc>")))

if __name__ == "__main__":
    main()
