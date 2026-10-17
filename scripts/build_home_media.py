#!/usr/bin/env python3
"""Keep the home page's direct audio players and latest approved comic current."""
import json
import re
from datetime import date
from html import escape as e
from pathlib import Path
from comics_catalog import current_editions

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- home-media:start -->'
END = '<!-- home-media:end -->'

CSS = '''
.home-intro{padding:40px 0 24px}.home-intro .container{display:grid;grid-template-columns:1fr 1fr;column-gap:48px;align-items:center}
.home-intro .kicker{grid-column:1/-1;margin-bottom:16px}.home-intro h1{grid-column:1;grid-row:2/4;font-size:clamp(2.5rem,4.5vw,4rem);margin:0;line-height:1.02}.home-intro .rule--accent{display:none}
.home-intro .lead{grid-column:2;font-size:1rem;margin:0;line-height:1.55}.home-intro .btn-row{grid-column:2;margin-top:16px;gap:16px}.home-intro .btn{padding:10px 14px;font-size:.7rem}
.home-intro .meta{grid-column:1/-1;margin-top:24px;padding-top:16px;border-top:1px solid var(--border);gap:24px}.home-intro .stat{display:flex;gap:8px;align-items:baseline}.home-intro .stat b{font-size:1.25rem}.home-intro .stat span{font-size:.62rem}
.home-media{padding:12px 0 48px;scroll-margin-top:100px}.home-media-head{display:flex;justify-content:space-between;align-items:center;gap:24px;margin-bottom:20px}.home-media-head .kicker{margin:0 0 6px}.home-media-head h2{font-size:clamp(1.4rem,2.5vw,2.2rem);letter-spacing:-.035em;line-height:1.1;text-transform:none}.home-media-head>a{font-size:.8rem;white-space:nowrap}
.home-media-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.home-media-card{min-width:0;border:1px solid var(--border-strong);background:var(--bg);box-shadow:5px 5px 0 var(--border-strong);padding:24px;display:flex;flex-direction:column;scroll-margin-top:100px}
.home-media-card h3{font-size:clamp(1.6rem,2.8vw,2.3rem);line-height:1.1;text-transform:none;letter-spacing:-.035em;margin:6px 0 12px}.home-media-card p{font-size:.9rem;margin:0;line-height:1.45}.home-media-card .kicker{font-size:.65rem;color:var(--c-red)}
.home-radio-top{display:grid;grid-template-columns:112px 1fr;gap:20px;align-items:center;margin-bottom:18px}.home-radio-top img{width:112px;height:112px;object-fit:contain;background:var(--c-white);border:1px solid var(--border)}
.home-media-date{font-family:var(--font-mono);font-size:.7rem!important;color:var(--text-muted)}.home-media-tracks{display:grid;gap:14px;margin-top:12px}.home-media-track label{display:flex;align-items:baseline;justify-content:space-between;gap:12px;font-size:.85rem;font-weight:700;margin-bottom:6px}.home-media-track label span{font-family:var(--font-mono);font-size:.72rem;color:var(--text-muted);font-weight:400}.home-media-track audio{display:block;width:100%;height:36px}.home-media-card .home-media-links{margin-top:auto;padding-top:20px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.8rem}
.home-comic-top{display:flex;justify-content:space-between;gap:16px;align-items:baseline}.home-comic-art{display:block;position:relative;overflow:hidden;aspect-ratio:2.2;border:1px solid var(--border);background:var(--surface);margin:4px 0 14px}.home-comic-art img{position:absolute;max-width:none}.home-comic-title{font-weight:700}.home-media-card .btn{padding:10px 14px;font-size:.72rem}
.home-media-foot{margin:20px 0 0;font-size:.75rem;display:flex;gap:16px;justify-content:space-between;flex-wrap:wrap;color:var(--text-muted)}.home-media :focus-visible,.home-news-nav :focus-visible{outline:3px solid var(--c-red);outline-offset:4px}
.home-news-nav{display:flex;align-items:center;gap:2px;position:relative}.home-news-nav>a{color:var(--c-red)}.home-news-nav details>summary{display:flex;align-items:center;justify-content:center;cursor:pointer;list-style:none;width:28px;height:36px;font-size:.85rem}.home-news-nav summary::-webkit-details-marker{display:none}.home-news-nav details[open]>summary{color:var(--c-red)}
.home-news-menu{position:absolute;top:calc(100% + 12px);left:-16px;min-width:275px;padding:12px;background:var(--bg);border:1px solid var(--border-strong);box-shadow:4px 4px 0 var(--border-strong);z-index:60}.nav__links .home-news-menu a{display:block;padding:12px;font-size:.8rem;letter-spacing:0;text-transform:none}.home-news-menu small{display:block;color:var(--text-muted);font-weight:400;font-family:var(--font-body);margin-top:3px}.home-news-menu a:hover{background:var(--surface)}
@media(min-width:761px) and (max-width:1100px){.nav{flex-wrap:wrap;gap:12px}.nav>nav{width:100%}.nav__links{justify-content:space-between;gap:12px}}
@media(max-width:760px){.home-intro{padding:28px 0 20px}.home-intro .container{display:block}.home-intro h1{font-size:2.8rem}.home-intro .lead{margin-top:16px}.home-intro .meta{display:flex;flex-wrap:wrap;gap:10px 20px;margin-top:20px}.home-intro .stat{gap:6px}.home-intro .stat span{font-size:.6rem}.home-media-head{display:block}.home-media-head>a{display:inline-block;margin-top:10px}.home-media-grid{grid-template-columns:1fr;gap:20px}.home-media-card{padding:20px}.home-radio-top{grid-template-columns:88px 1fr;gap:16px}.home-radio-top img{width:88px;height:88px}.home-media-card h3{font-size:1.8rem}.home-comic-top{display:block}.home-comic-art{margin-top:14px}.home-news-nav{flex-wrap:wrap;gap:8px;width:100%}.home-news-nav details>summary{width:44px;height:44px}.home-news-menu{position:static;margin-top:10px;box-shadow:none;min-width:0;width:100%;padding:4px}.home-news-nav details[open]{width:100%}.home-news-nav details[open]>summary{position:absolute;top:0;right:0}.nav__links .home-news-menu a{font-size:1rem}}
'''

JS = '''
document.querySelectorAll('.home-news-nav details').forEach(menu=>{
  document.addEventListener('click',event=>{if(!menu.parentElement.contains(event.target))menu.open=false;});
  menu.addEventListener('keydown',event=>{if(event.key==='Escape'){menu.open=false;menu.querySelector('summary').focus();}});
  menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{menu.open=false;}));
});
'''

def human_date(value, en=False):
    d = date.fromisoformat(value)
    months = ('January February March April May June July August September October November December' if en else 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre').split()
    return f'{d.day} {months[d.month-1]} {d.year}'

def latest_comic():
    episodes = [json.loads(p.read_text()) for p in (ROOT/'knowledge-hub/comics/episodes').glob('*.json')]
    approved = [ep for ep in episodes if ep.get('status') == 'approved' and all(ep.get('approval', {}).get(k) is True for k in ('editorial','art','publish')) and (ROOT/f'knowledge-hub/comics/{ep["id"]}/index.html').is_file()]
    return current_editions(approved)[-1]

def build():
    latest = json.loads((ROOT/'assets/podcast/latest.json').read_text())
    comic = latest_comic()
    panel = next((p for p in comic['panels'] if 'mistral' in p['news_ids']), comic['panels'][0])
    crop = panel.get('crop', {'x':0,'y':0,'w':1,'h':1})
    # Preserve the panel's actual crop; the link opens the full reader.
    image_path = ROOT/'knowledge-hub/comics'/panel['image']
    with image_path.open('rb') as image_file:
        png_header = image_file.read(24)
    if png_header[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Comic teaser requires a PNG panel')
    image_width = int.from_bytes(png_header[16:20], 'big')
    image_height = int.from_bytes(png_header[20:24], 'big')
    top = 50 - 100 * (crop['y'] + crop['h']/2) * image_height/image_width * 2.2/crop['w']
    image_style = f'width:{100/crop["w"]}%;height:auto;left:{-100*crop["x"]/crop["w"]}%;top:{top}%'
    for en in (False, True):
        prefix='/knowledge-hub/'+('en/' if en else '')
        path=ROOT/(prefix.lstrip('/')+'index.html')
        raw=path.read_text()
        comic_url=prefix+'comics/'+comic['id']+'/'
        if not (ROOT/(comic_url.lstrip('/')+'index.html')).exists():
            comic_url='/knowledge-hub/comics/'+comic['id']+'/'
        tr=lambda fr,eng:eng if en else fr
        tracks=''
        for kind, label in (('short','Le Flash'),('full','Le Débrief')):
            t=latest[kind];timing=f'{t["seconds"]//60}′ {t["seconds"]%60:02d}″'
            tracks+=f'<div class="home-media-track"><label id="podcast-{kind}-title" for="podcast-{kind}">{label}<span id="podcast-{kind}-duration">{timing}</span></label><audio id="podcast-{kind}" controls preload="none" src="{e(t["src"])}?v={e(latest.get("version", latest["date"]))}" aria-labelledby="podcast-{kind}-title"></audio></div>'
        start_label = str(date.fromisoformat(comic['period_start']).day) if comic['period_start'][:7] == comic['period_end'][:7] else human_date(comic['period_start'],en)
        period=f'{start_label}–{human_date(comic["period_end"],en)}'
        content=f'''{START}
<section id="a-la-une" class="home-media" aria-labelledby="home-media-title"><div class="container">
  <div class="home-media-head"><div><p class="kicker">{tr('Les rendez-vous IA de Hugo','Hugo’s AI editions')}</p><h2 id="home-media-title">{tr('Une voix pour suivre. Des histoires pour comprendre.','Listen to keep up. Read to understand.')}</h2></div><a href="{prefix}veille-ia/">{tr('Toute la veille écrite →','All AI news →')}</a></div>
  <div class="home-media-grid">
    <article class="home-media-card" id="podcasts" aria-labelledby="home-podcast-title"><div id="daily-podcast">
      <div class="home-radio-top"><img src="/assets/podcast/art/iastro-{latest['date'][5:7]}-v1.png" width="112" height="112" alt="iAstro"><div><p class="kicker">{tr('À écouter · tous les jours','Listen · every day')}</p><h3 id="home-podcast-title">Le Podcast iA</h3><p>{tr('Le Flash pour l’essentiel. Le Débrief pour prendre du recul.','Le Flash for the essentials. Le Débrief for the bigger picture.')}</p></div></div>
      <p class="home-media-date">{tr('Dernière édition','Latest edition')} · <time id="podcast-date" datetime="{latest['date']}">{human_date(latest['date'],en)}</time></p>
      <div id="podcast-tracks" class="home-media-tracks">{tracks}</div>
      <p id="podcast-fallback" hidden><a href="https://t.me/VeilleIA_HL">{tr('Retrouver les audios sur Telegram →','Listen on Telegram →')}</a></p>
    </div><div class="home-media-links"><a href="{prefix}immersion-ia/#podcasts">{tr('Tous les épisodes →','All episodes →')}</a><a href="/assets/podcast/feed.xml">{tr('S’abonner au podcast ↗','Subscribe to the podcast ↗')}</a></div></article>
    <article class="home-media-card" id="comic" aria-labelledby="home-comic-title">
      <div class="home-comic-top"><div><p class="kicker">{tr('À lire · le comic du dimanche','Read · the Sunday comic')}</p><h3 id="home-comic-title">iAstro Sunday</h3></div><span class="home-media-date">Hugo × iAstro</span></div>
      <a class="home-comic-art" href="{comic_url}" aria-label="{tr('Lire le dernier comic','Read the latest comic')}"><img src="/knowledge-hub/comics/{e(panel['image'])}" width="1536" height="1024" style="{image_style}" alt="{e(panel['alt'])}"></a>
      <p class="home-media-date">{e(period)}</p><p class="home-comic-title" lang="fr">{e(comic['title'])}</p>
      <div class="home-media-links"><a class="btn btn--primary" href="{comic_url}">{tr('Lire le dernier numéro →','Read the latest issue →')}</a><a href="{prefix}comics/">{tr('Tous les numéros →','All issues →')}</a></div>
    </article>
  </div>
  <div class="home-media-foot"><span>{tr('Podcasts et comics en français · voix de synthèse, dessins générés par IA.','Podcasts and comics in French · synthetic voice, AI-generated illustrations.')}</span><a href="https://t.me/VeilleIA_HL">{tr('Le Radar iA sur Telegram ↗','Le Radar iA on Telegram ↗')}</a></div>
</div></section>
{END}'''
        if START in raw:
            raw=re.sub(re.escape(START)+r'.*?'+re.escape(END),lambda _:content,raw,flags=re.S)
        else:
            hero=re.search(r'<section class="hero">.*?</section>',raw,re.S)
            if not hero:raise ValueError(f'Home hero missing in {path}')
            raw=raw[:hero.end()]+'\n\n'+content+raw[hero.end():]
        raw=raw.replace('<section class="hero">','<section class="hero home-intro">',1)
        hero=re.search(r'<section class="hero home-intro">.*?</section>',raw,re.S)
        hero_html=hero.group()
        intro=tr('Ma méthode, mes projets et ce que je construis avec l’IA. Et pour garder le fil : un podcast chaque jour, un comic le dimanche.', 'My method, my projects and what I build with AI. To keep up: a daily podcast and a Sunday comic.')
        hero_html=re.sub(r'<p class="lead">.*?</p>', '<p class="lead">'+intro+'</p>',hero_html,flags=re.S)
        actions=f'<div class="btn-row"><a class="btn btn--primary" href="#podcasts">{tr("Écouter le podcast ↓", "Listen to the podcast ↓")}</a><a class="btn btn--ghost" href="{comic_url}">{tr("Lire le comic →", "Read the comic →")}</a></div>'
        hero_html=re.sub(r'<div class="btn-row">.*?</div>',lambda _:actions,hero_html,flags=re.S)
        raw=raw[:hero.start()]+hero_html+raw[hero.end():]
        # Retire the old intermediate Kiosque callout; retain the written-news teaser.
        raw=re.sub(r'\s*<aside class="callout"[^>]*>\s*<p class="kicker">Le Kiosque IA</p>.*?</aside>','',raw,flags=re.S)
        nav=f'''<li class="home-news-nav"><a href="{prefix}#a-la-une">{tr('Veille IA','AI watch')}</a><details><summary aria-label="{tr('Accès directs à la veille IA','AI news shortcuts')}">⌄</summary><div class="home-news-menu"><a href="{prefix}#podcasts">Le Podcast iA<small>{tr('Écouter le Flash ou le Débrief','Listen to Le Flash or Le Débrief')}</small></a><a href="{comic_url}">iAstro Sunday<small>{tr('Ouvrir le dernier comic','Open the latest comic')}</small></a><a href="{prefix}veille-ia/">{tr('La veille écrite','Written AI news')}<small>{tr('Les nouvelles et leurs sources','The news and its sources')}</small></a></div></details></li>'''
        if '<li class="home-news-nav">' in raw:
            raw=re.sub(r'<li class="home-news-nav">.*?</li>',lambda _:nav,raw,count=1,flags=re.S)
        else:
            raw,n=re.subn(r'<li><a href="(?:/knowledge-hub/(?:en/)?)?veille-ia/">[^<]*</a></li>',lambda _:nav,raw,count=1)
            if n!=1:raise ValueError(f'Veille navigation not found in {path}')
        style='<style id="home-media-style">'+CSS+'</style>'
        if 'id="home-media-style"' in raw:raw=re.sub(r'<style id="home-media-style">.*?</style>',lambda _:style,raw,flags=re.S)
        else:raw=raw.replace('</head>',style+'\n</head>',1)
        # Reuse the maintained podcast player, including its cache version.
        kiosk=(ROOT/(prefix.lstrip('/')+'immersion-ia/index.html')).read_text()
        player=re.search(r'<script src="/assets/podcast/player.js[^\"]*" defer></script>',kiosk).group()
        scripts='<script id="home-media-behavior">'+JS+'</script>\n'+player
        if 'id="home-media-behavior"' in raw:raw=re.sub(r'<script id="home-media-behavior">.*?</script>\s*<script src="/assets/podcast/player.js[^\"]*" defer></script>',lambda _:scripts,raw,flags=re.S)
        else:raw=raw.replace('</body>',scripts+'\n</body>')
        path.write_text(raw)
    print('Home FR/EN: direct audio players, latest approved comic and Veille shortcuts updated.')

if __name__=='__main__':build()
