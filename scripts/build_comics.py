#!/usr/bin/env python3
"""Render comics locally. No dependencies, network, schedule or deployment."""
from pathlib import Path
from datetime import date
import argparse
import html
import json
import re

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'knowledge-hub/comics'
MANIFEST = json.loads((ROOT / 'kit/manifest.json').read_text())
ASSETS = {a['id']: a for a in MANIFEST['assets']}
BASE = '/knowledge-hub/comics/'
ORIGIN = 'https://hl-consulting.tech'

def esc(value):
    return html.escape(str(value), quote=True)

def local_file(value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('A relative local file path is required')
    p = (ROOT / value).resolve()
    if not p.is_relative_to(ROOT.resolve()) or not p.is_file():
        raise ValueError(f'Missing or unsafe local file: {value}')
    return p

def validate(ep):
    assert re.fullmatch(r'\d{4}-W\d{2}(?:-r\d+)?', ep['id']), 'Use YYYY-Www, optionally -r2 for a correction'
    start, end, pub = [date.fromisoformat(ep[k]) for k in ('period_start', 'period_end', 'publication_date')]
    assert start <= end <= pub, 'Invalid editorial period'
    assert ep['wardrobe_month'] == pub.month, 'Wardrobe must match publication date'
    assert ep['status'] == 'approved', 'Only explicitly approved episodes enter the reader'
    approval = ep['approval']
    assert all(approval.get(k) is True for k in ('editorial', 'art', 'publish')), 'Approval incomplete'
    assert approval.get('by') == 'Hugo' and approval.get('reference'), 'Record Hugo’s explicit approval reference'
    assert 4 <= len(ep['news']) <= 7, 'Select 4 to 7 news items'
    news_ids = {n['id'] for n in ep['news']}
    assert len(news_ids) == len(ep['news']), 'Duplicate news ID'
    for n in ep['news']:
        assert n['title'].strip() and n['fact'].strip() and n['sources'], 'News must contain facts and sources'
        for s in n['sources']:
            assert re.match(r'https?://[^\s]+$', s['url']), 'Invalid source URL'
            assert s['title'].strip() and s['publisher'].strip(), 'Source attribution required'
            date.fromisoformat(s['consulted_at'])
            date.fromisoformat(s['published_at'])
    covered = set()
    assert ep['panels'], 'An episode needs artwork and dialogue'
    for panel in ep['panels']:
        assert panel['alt'].strip(), 'Artwork needs descriptive alternative text'
        art = local_file(panel['image']).read_bytes()
        assert art[:8] == b'\x89PNG\r\n\x1a\n', 'Panel illustrations must be PNG'
        assert int.from_bytes(art[16:20], 'big') > 0 and int.from_bytes(art[20:24], 'big') > 0, 'Invalid PNG dimensions'
        for nid in panel['news_ids']:
            assert nid in news_ids, 'Unknown news ID'
            covered.add(nid)
        for line in panel['dialogue']:
            assert line['speaker'] in ('Hugo', 'Astro AI', 'Narration') and line['text'].strip(), 'Invalid dialogue'
    assert covered == news_ids, 'Each news item must appear in the comic'
    for value in ep.get('downloads', {}).values():
        if value:
            local_file(value)
    return ep

def image(asset_id, **kwargs):
    a = ASSETS[asset_id]
    alt = kwargs.get('alt', a['title'])
    return f'<img src="{BASE}kit/{a["path"]}" width="{a["width"]}" height="{a["height"]}" alt="{esc(alt)}" loading="lazy" style="width:100%;height:auto;object-fit:contain">'

def shell(title, description, content, language='fr', suffix=''):
    en = language == 'en'
    fr = BASE + suffix
    enurl = '/knowledge-hub/en/comics/' + suffix
    url = enurl if en else fr
    schema = {'@context':'https://schema.org', '@type':'CollectionPage', 'name':title, 'url':ORIGIN+url, 'inLanguage':language, 'author':{'@type':'Person','@id':ORIGIN+'/#hugo','name':'Hugo Lahutte'}}
    return f'''<!doctype html>
<html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Knowledge Hub</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{ORIGIN+url}"><link rel="alternate" hreflang="fr" href="{ORIGIN+fr}"><link rel="alternate" hreflang="en" href="{ORIGIN+enurl}"><link rel="alternate" hreflang="x-default" href="{ORIGIN+fr}">
<meta name="theme-color" content="#FFFCF8"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{ORIGIN+url}"><meta property="og:locale" content="{'en_US' if en else 'fr_FR'}"><meta property="og:locale:alternate" content="{'fr_FR' if en else 'en_US'}"><meta property="og:image" content="{ORIGIN+BASE}kit/assets/characters/duo-reference-v2.png">
<script>(function(){{try{{var t=localStorage.getItem('kh-theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="/knowledge-hub/style.css?v=20260622a"><link rel="icon" href="/knowledge-hub/favicon.svg" type="image/svg+xml">
<script src="/knowledge-hub/theme.js?v=20260601d" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<','&lt;')}</script>
</head><body><a class="skip-link" href="#main">{'Skip to content' if en else 'Aller au contenu'}</a>
<header style="border-bottom:1px solid var(--border-strong);padding:18px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px"><a class="nav__wordmark" href="/knowledge-hub/">Knowledge Hub</a><nav aria-label="{'Navigation' if en else 'Navigation principale'}" style="display:flex;gap:20px;flex-wrap:wrap;align-items:center"><a href="/knowledge-hub/{'en/' if en else ''}veille-ia/">{'AI watch' if en else 'La veille IA'}</a><a href="{fr if en else enurl}" lang="{'fr' if en else 'en'}">{'FR' if en else 'EN'}</a><button class="btn" data-theme-toggle type="button" style="color:var(--text);background:var(--surface);border-color:var(--border)">{'Auto / Light / Dark' if en else 'Auto / Clair / Sombre'}</button></nav></header>
<main id="main" class="container">{content}</main><footer class="container" style="border-top:1px solid var(--border-strong);padding-block:24px"><p class="caption">Hugo × Astro AI · {'AI-generated artwork. Editorial direction: Hugo Lahutte.' if en else 'Dessins générés par IA. Direction éditoriale : Hugo Lahutte.'}</p></footer></body></html>'''

GRID = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px'

def panel(number, title, art, dialogue):
    lines = ''.join(f'<p style="padding:14px 18px;margin:0;border:2px solid var(--border-strong);border-radius:20px;background:var(--surface);color:var(--text);line-height:1.5"><strong style="display:block;font-size:.75rem;letter-spacing:.06em;text-transform:uppercase">{esc(speaker)}</strong>{esc(text)}</p>' for speaker,text in dialogue)
    return f'<article style="border:2px solid var(--border-strong);padding:20px;background:var(--surface);display:flex;flex-direction:column;gap:18px"><h3 style="font-size:1rem">{number:02d} / {esc(title)}</h3><div style="display:grid;gap:12px">{lines}</div><div style="margin-top:auto">{art}</div></article>'

def intro(en=False):
    titles = ['A week moves fast.', 'Let’s take a step back.', 'Same duo. New season.', 'See you next week.'] if en else ['Ça va vite, une semaine.', 'On prend du recul.', 'Même duo. Nouvelle saison.', 'À la semaine prochaine.']
    dialogue = [ [('Hugo','Every week there’s another wave of AI news. Where do we start?')], [('Astro AI','Four to seven stories that matter. What happened, what it changes, and what’s still uncertain.')], [('Hugo','One outfit a month. In October, we’re ready for Halloween!')], [('Astro AI','A comic to read at your own pace. And sources to explore further.')] ] if en else [ [('Hugo','Toutes les semaines, une nouvelle avalanche d’annonces IA. On commence par quoi ?')], [('Astro AI','Quatre à sept infos qui comptent. Ce qui se passe, ce que ça change et ce qui reste incertain.')], [('Hugo','Une tenue par mois. En octobre, on est prêts pour Halloween !')], [('Astro AI','Une BD à lire tranquillement. Et les sources pour aller plus loin.')] ]
    ids=['hugo-pose-reflechit-v1','ia-pose-explique-v1','month-10-octobre-v1','ia-pose-se-rejouit-v1']
    # The monthly card is a wardrobe reference, intentionally presented whole.
    arts=[image(a) for a in ids]
    arts[2]=f'<div style="max-width:250px;margin:auto">{arts[2]}</div>'
    return '<div style="'+GRID+'">'+''.join(panel(i+1,t,arts[i],dialogue[i]) for i,t in enumerate(titles))+'</div>'

def render_episode(ep):
    panels = []
    for i,p in enumerate(ep['panels']):
        data = local_file(p['image']).read_bytes()
        width, height = int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
        art = f'<img width="{width}" height="{height}" src="{BASE+esc(p["image"])}" alt="{esc(p["alt"])}" style="width:100%;height:auto" loading="lazy">'
        panels.append(panel(i+1,p['title'],art,[(d['speaker'],d['text']) for d in p['dialogue']]))
    sources = ''.join('<li><strong>'+esc(n['title'])+'</strong><ul>'+''.join(f'<li><a href="{esc(s["url"])}">{esc(s["title"])}</a> — {esc(s["publisher"])}, {esc(s["published_at"])}</li>' for s in n['sources'])+'</ul></li>' for n in ep['news'])
    downloads = ' · '.join(f'<a download href="{BASE+esc(p)}">{esc(fmt.upper())}</a>' for fmt,p in ep.get('downloads',{}).items() if p)
    return f'<p class="kicker">{esc(ep["id"])} · {esc(ep["period_start"])} → {esc(ep["period_end"])}</p><h2>{esc(ep["title"])}</h2><p>{esc(ep.get("correction_note", ""))}</p><div style="{GRID}">{"".join(panels)}</div><section><h2>Sources</h2><ol>{sources}</ol>{downloads}</section>'

def home(episodes, en=False):
    heading = 'The week in AI.<br>A comic to unwind with.' if en else 'La semaine IA.<br>En bande dessinée.'
    desc = 'Four to seven big stories, a little perspective, and our recurring duo.' if en else 'Quatre à sept grandes infos, un peu de recul et notre duo pour raconter la semaine.'
    content = f'<section style="padding-block:48px 32px;border-bottom:3px solid var(--border-strong)"><p class="kicker">Hugo × Astro AI · {"Weekly comic" if en else "Le rendez-vous hebdo"}</p><h1 style="font-size:clamp(2.6rem,6vw,5.3rem);margin-top:16px;max-width:18ch">{heading}</h1><p class="lead" style="font-size:1.25rem;max-width:48ch">{desc}</p><a class="btn btn--primary" href="#episode">{"Read the comic" if en else "Lire la BD"} ↓</a></section><section id="episode">'
    if episodes:
        content += render_episode(episodes[-1])
        if en: content = content.replace('<section id="episode">','<section id="episode"><p lang="en">This episode is available in French.</p>')
    else:
        content += f'<p class="kicker">{"Meet the duo" if en else "Avant le premier numéro"}</p><h2 style="margin-block:12px 20px">{"A new ritual." if en else "On fait les présentations."}</h2><p>{"Introduction to the format. This is not a news issue." if en else "Une présentation du format et des personnages. Ce strip ne contient pas d’actualités."}</p>'+intro(en)
    content += '</section><section style="padding-top:0"><h2>'+('The previous weeks' if en else 'Les semaines précédentes')+'</h2>'
    if episodes:
        content += '<ul>'+''.join(f'<li><a href="{BASE+e["id"]}/">{esc(e["id"])} — {esc(e["title"])}</a></li>' for e in reversed(episodes))+'</ul>'
    else:
        content += '<p>'+('The first weekly issue is being prepared.' if en else 'Le premier numéro hebdomadaire est en préparation.')+'</p>'
    content += f'</section><aside style="padding:24px 0;border-top:1px solid var(--border)"><p class="caption"><a href="{BASE}kit/">{"Character studio: poses, expressions and twelve outfits" if en else "L’atelier : poses, expressions et douze tenues"}</a></p></aside>'
    return shell('Hugo × Astro AI — '+('The week in AI comics' if en else 'La semaine IA en BD'),desc,content,'en' if en else 'fr')

def build(check=False):
    episodes=[]
    for p in sorted((ROOT/'episodes').glob('*.json')):
        ep=json.loads(p.read_text())
        if ep.get('status')=='approved': episodes.append(validate(ep))
        elif ep.get('status') not in ('draft','template'): raise ValueError(f'Unknown status in {p}')
    assert len({e['id'] for e in episodes})==len(episodes), 'Duplicate episode ID'
    episodes.sort(key=lambda e:(e['publication_date'],e['id']))
    rendered=[]
    for ep in episodes:
        for lang in ('fr','en'):
            dest=ROOT/ep['id']/'index.html' if lang=='fr' else REPO/'knowledge-hub/en/comics'/ep['id']/'index.html'
            content=render_episode(ep)
            if lang=='en': content='<p>This episode is available in French.</p>'+content
            page=shell(ep['title'],ep['title'],f'<section>{content}</section>',lang,ep['id']+'/')
            if dest.exists() and dest.read_text()!=page: raise ValueError(f'Archive immutable: create a revision instead of replacing {ep["id"]}')
            rendered.append((dest,page))
    if not check:
        rendered.extend([(ROOT/'index.html',home(episodes)),(REPO/'knowledge-hub/en/comics/index.html',home(episodes,True))])
        for dest,page in rendered:
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
        latest={'id':episodes[-1]['id'],'url':BASE+episodes[-1]['id']+'/'} if episodes else None
        (ROOT/'latest.json').write_text(json.dumps(latest,indent=2)+'\n')
    print(f'OK: {len(episodes)} approved episodes; 12 monthly references; FR/EN reader.' + (' Validation only.' if check else ' Files prepared locally.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    build(parser.parse_args().check)
