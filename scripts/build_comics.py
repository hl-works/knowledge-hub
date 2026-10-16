#!/usr/bin/env python3
"""Render comics locally. No dependencies, network, schedule or deployment."""
from pathlib import Path
from datetime import date
import argparse
import html
import json
import re
import math
import comics_reader

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / 'knowledge-hub/comics'
MANIFEST = json.loads((ROOT / 'kit/manifest.json').read_text())
ASSETS = {a['id']: a for a in MANIFEST['assets']}
CAST = {c['id']: c for c in json.loads((ROOT / 'cast.json').read_text())['characters']}
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

def validate(ep, preview=False):
    assert re.fullmatch(r'\d{4}-W\d{2}(?:-r\d+)?', ep['id']), 'Use YYYY-Www, optionally -r2 for a correction'
    start, end, pub = [date.fromisoformat(ep[k]) for k in ('period_start', 'period_end', 'publication_date')]
    assert start <= end <= pub, 'Invalid editorial period'
    assert ep['wardrobe_month'] == end.month, 'Wardrobe must match the week being told, including retrospective issues'
    if preview:
        assert ep['status'] == 'draft', 'Only drafts use preview mode'
    else:
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
    cast_ids = ep.get('cast_ids', ['hugo', 'iastro'])
    assert set(cast_ids) <= set(CAST), 'Unknown cast member'
    speakers = {CAST[c]['name']: CAST[c] for c in cast_ids}
    for character in speakers.values():
        assert character['reference_asset_ids'], 'A cast member needs a visual reference before appearing'
        assert all(a in ASSETS for a in character['reference_asset_ids']), 'Missing cast asset'
    covered = set()
    assert ep['panels'], 'An episode needs artwork and dialogue'
    assert ep.get('format', 'standard') in ('standard', 'webtoon'), 'Unknown reading format'
    for panel in ep['panels']:
        assert panel['alt'].strip(), 'Artwork needs descriptive alternative text'
        art = local_file(panel['image']).read_bytes()
        assert art[:8] == b'\x89PNG\r\n\x1a\n', 'Panel illustrations must be PNG'
        assert int.from_bytes(art[16:20], 'big') > 0 and int.from_bytes(art[20:24], 'big') > 0, 'Invalid PNG dimensions'
        if 'crop' in panel:
            crop = panel['crop']
            assert set(crop) == {'x','y','w','h'}, 'Invalid crop fields'
            assert all(type(v) in (int,float) and math.isfinite(v) for v in crop.values()), 'Invalid crop values'
            assert 0 <= crop['x'] < 1 and 0 <= crop['y'] < 1 and crop['w'] > 0 and crop['h'] > 0, 'Invalid crop extent'
            assert crop['x']+crop['w'] <= 1.00000001 and crop['y']+crop['h'] <= 1.00000001, 'Crop outside image'
        for nid in panel['news_ids']:
            assert nid in news_ids, 'Unknown news ID'
            covered.add(nid)
        assert panel.get('layout', 'standard') in ('standard', 'wide'), 'Invalid panel layout'
        for line in panel['dialogue']:
            assert line['speaker'] in (*speakers, 'Narration') and line['text'].strip(), 'Invalid dialogue'
            if line['speaker'] in speakers and speakers[line['speaker']]['kind'] == 'public_figure':
                assert line.get('attribution') in ('quote', 'paraphrase', 'fiction'), 'Label public-figure speech'
                if line['attribution'] != 'fiction':
                    urls = {source['url'] for news in ep['news'] for source in news['sources']}
                    assert line.get('source_url') in urls, 'Public-figure speech needs a consulted source'
    assert covered == news_ids, 'Each news item must appear in the comic'
    if ep.get('format') == 'webtoon':
        assert all(len(p['news_ids']) == 1 for p in ep['panels']), 'One story per mobile panel'
        for nid in news_ids:
            indexes = [i for i,p in enumerate(ep['panels']) if nid in p['news_ids']]
            assert 5 <= len(indexes) <= 6, 'A mobile story needs 5 or 6 panels'
            assert indexes == list(range(indexes[0],indexes[-1]+1)), 'Keep each story contiguous'
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
<main id="main" class="container">{content}</main><footer class="container" style="border-top:1px solid var(--border-strong);padding-block:24px"><p class="caption">Hugo × Iastro · {'AI-generated artwork. Editorial direction: Hugo Lahutte.' if en else 'Dessins générés par IA. Direction éditoriale : Hugo Lahutte.'}</p></footer></body></html>'''

GRID = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px'

def panel(number, title, art, dialogue, wide=False):
    lines = ''.join(f'<p style="padding:14px 18px;margin:0;border:2px solid var(--border-strong);border-radius:20px;background:var(--surface);color:var(--text);line-height:1.5"><strong style="display:block;font-size:.75rem;letter-spacing:.06em;text-transform:uppercase">{esc(speaker)}</strong>{esc(text)}</p>' for speaker,text in dialogue)
    return f'<article style="grid-column:{"1 / -1" if wide else "auto"};border:2px solid var(--border-strong);padding:20px;background:var(--surface);display:flex;flex-direction:column;gap:18px"><h3 style="font-size:1rem">{number:02d} / {esc(title)}</h3><div style="display:grid;gap:12px">{lines}</div><div style="margin-top:auto">{art}</div></article>'

def intro(en=False):
    caption = ('Visual study: a fictional scene with Hugo, Iastro and Alexandr Wang. It depicts no real event or announcement.' if en else 'Étude de mise en scène : scène fictive avec Hugo, Iastro et Alexandr Wang. Aucun événement réel ni aucune annonce ne sont représentés.')
    transcript = ('In a workshop, a machine starts producing far too much paper. Hugo panics, Iastro watches calmly, then they rush to catch the sheets while Wang stops the machine. They finally sit outside with one selected page.' if en else 'Dans l’atelier, une machine produit beaucoup trop de feuilles. Hugo s’affole, Iastro observe impassiblement, puis tous deux essaient de rattraper les papiers pendant que Wang arrête la machine. Ils finissent assis dehors, autour d’une seule feuille choisie.')
    art = image('atelier-des-possibles-v2-camouflage', alt=transcript)
    return f'<figure style="margin:0;max-width:980px">{art}<figcaption style="padding-block:16px">{caption}</figcaption></figure><details><summary>{"Scene description" if en else "Description de la scène"}</summary><p>{transcript}</p></details>'


def render_episode(ep, preview=False):
    if ep.get('format') == 'webtoon':
        def dimensions(path):
            data = local_file(path).read_bytes()
            return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
        return comics_reader.render(ep, BASE, dimensions, preview)
    panels = []
    for i,p in enumerate(ep['panels']):
        data = local_file(p['image']).read_bytes()
        width, height = int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
        art = f'<img width="{width}" height="{height}" src="{BASE+esc(p["image"])}" alt="{esc(p["alt"])}" style="width:100%;height:auto" loading="lazy">'
        dialogue = []
        for d in p['dialogue']:
            label = {'fiction':' — scène imaginée', 'paraphrase':' — reformulation', 'quote':' — citation'}.get(d.get('attribution'), '')
            dialogue.append((d['speaker'] + label, d['text']))
        panels.append(panel(i+1,p['title'],art,dialogue,p.get('layout') == 'wide'))
    sources = ''.join('<li><strong>'+esc(n['title'])+'</strong><ul>'+''.join(f'<li><a href="{esc(s["url"])}">{esc(s["title"])}</a> — {esc(s["publisher"])}, {esc(s["published_at"])}</li>' for s in n['sources'])+'</ul></li>' for n in ep['news'])
    downloads = ' · '.join(f'<a download href="{BASE+esc(p)}">{esc(fmt.upper())}</a>' for fmt,p in ep.get('downloads',{}).items() if p)
    return f'<p class="kicker">{esc(ep["id"])} · {esc(ep["period_start"])} → {esc(ep["period_end"])}</p><h2>{esc(ep["title"])}</h2><p>{esc(ep.get("correction_note", ""))}</p><div style="{GRID}">{"".join(panels)}</div><section><h2>Sources</h2><ol>{sources}</ol>{downloads}</section>'

def home(episodes, en=False):
    heading = 'The week in AI.<br>A comic to unwind with.' if en else 'La semaine IA.<br>En bande dessinée.'
    desc = 'Four to seven big stories, a little perspective, and our recurring duo.' if en else 'Quatre à sept grandes infos, un peu de recul et notre duo pour raconter la semaine.'
    content = f'<section style="padding-block:48px 32px;border-bottom:3px solid var(--border-strong)"><p class="kicker">Hugo × Iastro · {"Weekly comic" if en else "Le rendez-vous hebdo"}</p><h1 style="font-size:clamp(2.6rem,6vw,5.3rem);margin-top:16px;max-width:18ch">{heading}</h1><p class="lead" style="font-size:1.25rem;max-width:48ch">{desc}</p><a class="btn btn--primary" href="#episode">{"Read the comic" if en else "Lire la BD"} ↓</a></section><section id="episode">'
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
    if not any(ep['id'] == '2026-W41' for ep in episodes) and (ROOT/'drafts/2026-W41/index.html').exists():
        content += '<p><a href="'+BASE+'drafts/2026-W41/">'+('Preview the October 5–11 pilot (French, not published)' if en else 'Lire le pilote du 5–11 octobre — à valider, non publié')+'</a></p>'
    content += f'</section><aside style="padding:24px 0;border-top:1px solid var(--border)"><p class="caption"><a href="{BASE}kit/">{"Character studio: poses, expressions and twelve outfits" if en else "L’atelier : poses, expressions et douze tenues"}</a></p></aside>'
    return shell('Hugo × Iastro — '+('The week in AI comics' if en else 'La semaine IA en BD'),desc,content,'en' if en else 'fr')

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

def build_preview(episode_id):
    assert re.fullmatch(r'\d{4}-W\d{2}(?:-r\d+)?', episode_id), 'Invalid preview ID'
    ep = validate(json.loads((ROOT/'episodes'/f'{episode_id}.json').read_text()), preview=True)
    for lang in ('fr','en'):
        content = render_episode(ep, preview=True)
        if lang == 'en': content = '<p>This draft comic is available in French.</p>'+content
        page = shell('Pilote — '+ep['title'], 'Brouillon du comic hebdomadaire à relire.', '<section>'+content+'</section>', lang, f'drafts/{episode_id}/')
        page = page.replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>')
        dest = ROOT/'drafts'/episode_id/'index.html' if lang == 'fr' else REPO/'knowledge-hub/en/comics/drafts'/episode_id/'index.html'
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
    print(f'OK: draft preview {episode_id}; latest and published archives unchanged.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    parser.add_argument('--preview', metavar='YYYY-Www', help='Render a draft without publishing it')
    args=parser.parse_args()
    if args.preview:
        if args.check: parser.error('--preview and --check are separate operations')
        build_preview(args.preview)
    else: build(args.check)
