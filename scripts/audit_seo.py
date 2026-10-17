#!/usr/bin/env python3
"""Audit all sitemap-listed KH pages without network calls or dependencies."""
import argparse
from collections import Counter, defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://hl-consulting.tech'
NS = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta = {}; self.canonical = []; self.alternates = {}; self.links = []; self.images = []
        self.ids = []; self.h1 = 0; self.lang = ''; self.title = ''; self.schemas = []
        self.in_title = False; self.in_schema = False; self.schema_text = ''
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag == 'html': self.lang = a.get('lang', '')
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.in_title = True
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'a' and a.get('href'): self.links.append(a)
        if tag == 'img': self.images.append(a)
        if tag == 'link':
            if a.get('rel') == 'canonical': self.canonical.append(a.get('href'))
            if a.get('hreflang'): self.alternates[a['hreflang']] = a.get('href')
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_schema = True; self.schema_text = ''
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script' and self.in_schema:
            self.schemas.append(self.schema_text); self.in_schema = False
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schema_text += data

def file_for(url):
    path = unquote(urlsplit(url).path)
    file = ROOT / path.lstrip('/')
    return file / 'index.html' if path.endswith('/') else file

def sitemap_urls():
    return [node.text for node in ET.parse(ROOT/'knowledge-hub/sitemap.xml').findall('.//s:loc', NS)]

def audit():
    urls = sitemap_urls(); issues = defaultdict(list); cache = {}; titles = defaultdict(list)
    def parse(url):
        path = file_for(url)
        if path not in cache: cache[path] = Page(path.read_text()) if path.is_file() and path.suffix == '.html' else None
        return cache[path]
    def issue(kind, url, detail=''): issues[kind].append({'url':url, 'detail':detail})
    for url in urls:
        if not file_for(url).is_file(): issue('missing_page',url); continue
        page = parse(url)
        if not page: continue
        fr = url.replace('/knowledge-hub/en/', '/knowledge-hub/', 1)
        has_english = file_for(fr.replace('/knowledge-hub/','/knowledge-hub/en/',1)).is_file()
        titles[page.title.strip()].append(url)
        if not page.title.strip(): issue('missing_title',url)
        if page.canonical != [url]: issue('canonical',url,str(page.canonical))
        if not page.lang: issue('missing_lang',url)
        if page.h1 != 1: issue('heading_count',url,str(page.h1))
        if 'noindex' in page.meta.get('robots',''): issue('noindex_in_sitemap',url)
        for key in ['description','og:title','og:description','og:url','og:image','og:locale','og:locale:alternate']:
            if key == 'og:locale:alternate' and not has_english: continue
            if not page.meta.get(key): issue('missing_'+key,url)
        if page.meta.get('og:url') and page.meta['og:url'] != url: issue('og_url',url,page.meta['og:url'])
        image = page.meta.get('og:image')
        if image and image.startswith(ORIGIN) and not file_for(image).is_file(): issue('missing_social_image',url,image)
        for lang in ('fr','en','x-default'):
            if lang == 'en' and not has_english: continue
            target = page.alternates.get(lang)
            if not target: issue('missing_hreflang',url,lang); continue
            if not file_for(target).is_file(): issue('broken_hreflang',url,target); continue
            other = parse(target)
            if other and url not in other.alternates.values(): issue('nonreciprocal_hreflang',url,target)
        if not page.schemas: issue('missing_schema',url)
        for schema in page.schemas:
            try: json.loads(schema)
            except ValueError: issue('invalid_schema',url)
        for name, count in Counter(page.ids).items():
            if count > 1: issue('duplicate_id',url,name)
        for img in page.images:
            if 'alt' not in img: issue('missing_alt',url,img.get('src',''))
            src = urljoin(url,img.get('src',''))
            if src.startswith(ORIGIN) and not file_for(src).is_file(): issue('missing_image',url,src)
        for link in page.links:
            target = urljoin(url,link['href']); parts = urlsplit(target)
            if parts.netloc != 'hl-consulting.tech' or parts.scheme not in ('http','https'): continue
            if not file_for(target).is_file(): issue('broken_internal_link',url,target); continue
            if parts.fragment and file_for(target).suffix == '.html':
                other = parse(target)
                if other and unquote(parts.fragment) not in other.ids: issue('broken_anchor',url,target)
    duplicates = [v for k,v in titles.items() if k and len(v)>1]
    return {'pages':len(urls),'counts':{k:len(v) for k,v in sorted(issues.items())},'issues':dict(issues),'duplicate_titles':duplicates}

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output'); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    result=audit()
    if args.output: Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pages':result['pages'],'counts':result['counts'],'duplicate_title_groups':len(result['duplicate_titles'])},ensure_ascii=False,indent=2))
    if args.check:
        # Original W41 is a frozen edition, superseded by the approved W41-r2.
        archived={ORIGIN+'/knowledge-hub/comics/2026-W41/',ORIGIN+'/knowledge-hub/en/comics/2026-W41/'}
        failures=[item for kind,items in result['issues'].items() for item in items if not (kind=='heading_count' and item['url'] in archived)]
        if failures: raise SystemExit(1)
