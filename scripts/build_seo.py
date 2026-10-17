#!/usr/bin/env python3
"""Complete missing sharing metadata and keep canonical language pairs correct.

Only public sitemap pages are processed. Published comic archives are preserved.
"""
import json
import re
from html import escape
from audit_seo import Page, ROOT, ORIGIN, sitemap_urls, file_for
from veille_experience import external_tabs

def build():
    changed = 0
    for url in sitemap_urls():
        # Published comic editions have a separate immutable editorial workflow.
        if '/comics/' in url: continue
        path = file_for(url)
        if not path.is_file(): continue
        raw = path.read_text(); page = Page(raw); additions = []
        en = '/knowledge-hub/en/' in url
        fr = url.replace('/knowledge-hub/en/', '/knowledge-hub/', 1)
        english = fr.replace('/knowledge-hub/', '/knowledge-hub/en/', 1)
        has_english = file_for(english).is_file()
        # Correct only proven stale URLs; preserve the original editorial text.
        raw = raw.replace('dynaudio-analyze-ventes.html','dynaudio-analyse-ventes.html')
        raw = raw.replace('/knowledge-hub/en/coffre/', '/knowledge-hub/coffre/')
        raw = re.sub(r'<link\b[^>]*rel="canonical"[^>]*>', '<link rel="canonical" href="'+url+'">', raw)
        for lang, target in [('fr',fr),('en',english),('x-default',fr)]:
            if lang == 'en' and not has_english:
                raw = re.sub(r'<link\b[^>]*hreflang="en"[^>]*>\s*', '', raw)
                continue
            element = '<link rel="alternate" hreflang="'+lang+'" href="'+target+'">'
            pattern = r'<link\b[^>]*hreflang="'+lang+r'"[^>]*>'
            if re.search(pattern,raw): raw = re.sub(pattern,element,raw)
            else: additions.append(element)
        defaults = {
            'og:title':page.title, 'og:description':page.meta.get('description',''),
            'og:url':url, 'og:type':'website',
            'og:locale':'en_US' if en else 'fr_FR', 'og:locale:alternate':'fr_FR' if en else 'en_US',
            'og:image':ORIGIN+'/knowledge-hub/assets/img/stage-panel-wide.jpg',
        }
        if not has_english:
            defaults.pop('og:locale:alternate')
            raw = re.sub(r'<meta\b[^>]*property="og:locale:alternate"[^>]*>\s*', '', raw)
        for key, value in defaults.items():
            if not page.meta.get(key): additions.append('<meta property="'+key+'" content="'+escape(value,quote=True)+'">')
        if not page.meta.get('twitter:card'): additions.append('<meta name="twitter:card" content="summary_large_image">')
        if not page.schemas:
            schema = {'@context':'https://schema.org','@type':'WebPage','name':page.title,'description':page.meta.get('description',''),'url':url,'inLanguage':'en' if en else 'fr','author':{'@type':'Person','@id':ORIGIN+'/#hugo','name':'Hugo Lahutte'}}
            additions.append('<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>')
        # Three legacy English pages had a language switch pointing to themselves.
        if en:
            raw = re.sub(r'<a\b[^>]*href="'+re.escape(urlsplit_path(english))+r'"[^>]*hreflang="en"[^>]*>EN</a>', '<a href="'+urlsplit_path(fr)+'" hreflang="fr" lang="fr" aria-label="Lire en français" title="Lire en français">FR</a>',raw)
        if additions: raw = raw.replace('</head>', '\n'+'\n'.join(additions)+'\n</head>',1)
        raw = external_tabs(raw)
        if raw != path.read_text(): path.write_text(raw); changed += 1
    print(f'SEO metadata: {changed} pages updated.')

def urlsplit_path(url):
    return url.removeprefix(ORIGIN)

if __name__ == '__main__': build()
