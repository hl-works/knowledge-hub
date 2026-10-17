#!/usr/bin/env python3
"""Build Le Kiosque IA using the Knowledge Hub's navigation and design tokens."""
import json,re
from pathlib import Path
from html import escape as e
from urllib.parse import urljoin
from build_comics import shell
from build_home_media import CSS as HOME_MEDIA_CSS, JS as HOME_NAV_JS
from comics_catalog import current_editions, period
from podcast_design import cover,COVER_CSS,duration
from telegram_design import phone, PHONE_CSS
ROOT=Path(__file__).resolve().parents[1]
CSS='''
#main{scroll-margin-top:130px}
.kiosk section{padding-block:48px}.kiosk .kiosk-hero{padding-block:24px 12px;border-bottom:0}
.kiosk-meta{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-family:var(--font-mono);font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}
.kiosk-hero h1{font-size:clamp(1.8rem,3.5vw,3rem);max-width:none;line-height:1.1;margin:16px 0 12px}
.kiosk-hero h1 em{font-style:normal;color:var(--c-red)}
.kiosk-intro{display:flex;align-items:end;justify-content:space-between;gap:32px}.kiosk-intro p{font-size:1.1rem;max-width:47ch;margin:0}.kiosk-signature{font-family:var(--font-mono);font-size:.8rem;white-space:nowrap}
 .kiosk-formats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;padding:24px 0 36px;border-bottom:1px solid var(--border-strong)}
.format-card{display:flex;flex-direction:column;min-width:0;border:1px solid var(--border-strong);color:var(--text);background:var(--bg);text-decoration:none;box-shadow:4px 4px 0 var(--border-strong)}
.format-card:hover{border-color:var(--c-red);box-shadow:4px 4px 0 var(--c-red)}
.format-preview{height:156px;overflow:hidden;background:var(--surface);border-bottom:1px solid var(--border);position:relative;display:flex;justify-content:center;align-items:center}
.format-portrait{width:100%;height:100%;object-fit:contain;background:#FFFCF8}
.format-comic{position:relative;display:block;width:156px;height:156px;overflow:hidden}.format-comic img{position:absolute;width:300%;max-width:none;height:200%;left:0;top:0}
.format-radar{display:block;padding:16px 18px}.format-radar small{font:10px var(--font-mono);color:var(--c-red)}.format-headline{display:block;font-size:.75rem;line-height:1.3;font-weight:600;padding:8px 0;border-bottom:1px solid var(--border);overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.format-telegram{background:#e6f2f9;gap:18px}.telegram-device{position:relative;width:79px;height:141px;flex:none;display:block}.format-telegram .telegram-phone{position:absolute;left:0;top:0;transform:scale(.4);transform-origin:top left}.telegram-wordmark{color:#1879aa;font-size:1.1rem;font-weight:800}.telegram-wordmark small{display:block;max-width:12ch;font-size:.7rem;font-weight:400;margin-top:6px;line-height:1.3}
.format-copy{padding:20px;display:flex;flex-direction:column;flex:1;gap:10px}.format-eyebrow{font:11px var(--font-mono);color:var(--c-red)}
.format-title{font-family:var(--font-display);font-size:clamp(1.3rem,2.2vw,1.8rem);font-weight:900;line-height:1.1;letter-spacing:-.04em;text-transform:none}
.format-description{font-size:.9rem;line-height:1.4}.format-action{font-size:.85rem;font-weight:700;margin-top:auto;padding-top:8px}
.kiosk-section-head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:24px}.kiosk-section-head h2{font-size:clamp(1.8rem,4vw,3rem)}.kiosk-section-head p{margin:0}.kiosk-section-head .kicker{margin-bottom:8px}
.kiosk-feature{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:center;border-bottom:1px solid var(--border-strong)}
.kiosk-feature h2{font-size:clamp(2.4rem,5vw,4.4rem);text-transform:none;line-height:.98;max-width:9ch;margin:12px 0 20px}
.kiosk-feature p{max-width:43ch}.kiosk-feature .lead{font-size:1.2rem;line-height:1.55}
.kiosk-comic{position:relative;aspect-ratio:1;overflow:hidden;border:2px solid var(--border-strong);background:var(--surface);box-shadow:8px 8px 0 var(--c-red)}
.kiosk-comic img{position:absolute;max-width:none;width:300%;height:200%;left:0;top:0;object-fit:fill}
.kiosk-comic-caption{position:absolute;bottom:0;left:0;right:0;margin:0;padding:12px 16px;background:var(--c-black);color:var(--c-white);font-size:.8rem;font-family:var(--font-mono)}
.kiosk-tag{display:inline-block;border:1px solid var(--border-strong);font-size:.75rem;padding:3px 8px;font-family:var(--font-mono)}
.kiosk .radio-section{border-bottom:1px solid var(--border-strong)}
.radio-latest{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.radio-episode{min-width:0;display:grid;grid-template-columns:minmax(140px,.9fr) minmax(0,1fr);gap:20px;align-items:center;padding:0 0 28px}
.radio-copy h3{font-size:1.4rem;margin-bottom:8px}.radio-copy p{font-size:.9rem;line-height:1.5;margin:8px 0}.radio-copy audio{width:100%;height:42px;margin-top:12px}
.radio-duration{font-family:var(--font-mono);color:var(--text-muted);font-size:.8rem}
.radio-archive{border-top:1px solid var(--border);padding-top:24px}.radio-archive h3{margin-bottom:16px}
.radio-archive details{border-bottom:1px solid var(--border)}.radio-archive summary{display:flex;justify-content:space-between;gap:16px;cursor:pointer;padding:16px 0;min-height:48px;list-style:none}
.radio-archive summary::after{content:'+';font-size:1.3rem}.radio-archive details[open] summary::after{content:'−'}
.radio-archive .radio-latest{padding-top:12px}.radio-archive .radio-episode{grid-template-columns:110px minmax(0,1fr)}
.kiosk-news{list-style:none;margin:0;padding:0;border-top:1px solid var(--border-strong)}
.kiosk-news li{display:grid;grid-template-columns:48px 1fr auto;gap:20px;padding:24px 0;border-bottom:1px solid var(--border);align-items:start}
.kiosk-news .news-number{font:1rem var(--font-mono);color:var(--c-red)}.kiosk-news h3{font-size:1.2rem;line-height:1.3}.kiosk-news p{font-size:.95rem;color:var(--text-muted);margin:8px 0 0}.kiosk-news a{text-decoration:none}.kiosk-news time{font:.75rem var(--font-mono);white-space:nowrap}
.kiosk-note{font-size:.8rem;color:var(--text-muted);line-height:1.5}.kiosk-foot{border-top:3px solid var(--border-strong);padding:28px 0 40px;display:flex;gap:24px;flex-wrap:wrap;justify-content:space-between}
.kiosk section[id]{scroll-margin-top:100px}.kiosk a:focus-visible,.kiosk summary:focus-visible{outline:3px solid var(--c-red);outline-offset:4px}
@media(min-width:761px) and (max-width:1000px){.nav{flex-wrap:wrap;gap:12px}.nav>nav{width:100%}.nav__links{justify-content:space-between}}
@media(max-width:1000px){.kiosk-intro{display:block}.kiosk-signature{display:block;margin-top:18px}.radio-episode{display:block}.radio-copy{padding-top:16px}.radio-archive .radio-episode{display:grid}.kiosk-feature{gap:28px}}
@media(max-width:640px){.kiosk section{padding-block:32px}.kiosk .kiosk-hero{padding-top:28px}.kiosk-hero h1{font-size:1.8rem}.kiosk-signature{display:none!important}.kiosk-meta{font-size:.65rem}.kiosk-intro p{font-size:.95rem}.kiosk-intro{display:block}.kiosk-signature{display:block;margin-top:18px}.kiosk-formats{grid-template-columns:1fr;gap:12px;padding:16px 0 28px}.format-card{display:grid;grid-template-columns:92px minmax(0,1fr);box-shadow:3px 3px 0 var(--border-strong)}.format-preview{height:100%;min-height:118px;border-bottom:0;border-right:1px solid var(--border)}.format-comic{width:92px;height:92px}.format-copy{padding:12px;gap:6px}.format-title{font-size:1.2rem}.format-description{font-size:.8rem}.format-action{font-size:.8rem;padding-top:2px}.format-eyebrow{font-size:9px}.format-telegram{gap:0}.telegram-wordmark{display:none}.format-telegram .telegram-phone{transform:scale(.36)}.telegram-device{width:71px;height:127px}.format-radar{padding:12px 8px;display:flex;flex-direction:column;justify-content:center;align-items:stretch}.format-headline{font-size:.6rem;padding:7px 0}.format-radar small{font-size:8px}.kiosk-feature{grid-template-columns:1fr;gap:24px}.kiosk-feature h2{max-width:none}.kiosk-comic{margin:0 8px 8px 0}.kiosk-section-head{display:block}.kiosk-section-head>p{margin-top:12px}.radio-latest{gap:20px;grid-template-columns:1fr}.radio-episode{display:grid;grid-template-columns:42% minmax(0,1fr);gap:16px}.radio-copy{padding:0}.radio-copy h3{font-size:1.15rem}.radio-copy p{font-size:.85rem}.radio-copy audio{grid-column:1/-1}.radio-archive .radio-episode{grid-template-columns:96px minmax(0,1fr)}.kiosk-news li{grid-template-columns:24px 1fr;gap:12px}.kiosk-news time{grid-column:2;grid-row:1;margin-bottom:6px}.kiosk-news li>div{grid-column:2}.kiosk-news h3{font-size:1.1rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

def site_header(en):
    home=ROOT/('knowledge-hub/en/index.html' if en else 'knowledge-hub/index.html')
    raw=home.read_text();header=re.search(r'<header class="nav">.*?</header>',raw,re.S).group()
    prefix='/knowledge-hub/'+('en/' if en else '')
    def absolute(m):
        url=m.group(1)
        return 'href="'+(urljoin(prefix,url) if not url.startswith(('/', 'https:','http:','mailto:')) else url)+'"'
    header=re.sub(r'href="([^"]*)"',absolute,header)
    header=header.replace('href="/knowledge-hub/en/" hreflang="en"','href="/knowledge-hub/en/immersion-ia/" hreflang="en"').replace('href="/knowledge-hub/" hreflang="fr"','href="/knowledge-hub/immersion-ia/" hreflang="fr"')
    return header

def episode_card(ep,kind,live=False):
    name='Le Flash' if kind=='short' else 'Le Débrief';desc='Les nouvelles à retenir, en un clin d’œil.' if kind=='short' else 'Les annonces, leur contexte et ce qu’elles changent.'
    track=ep[kind];cid=f'podcast-{kind}' if live else f'archive-{ep["date"]}-{kind}'
    image=cover(ep['date'],kind,track['seconds'])
    duration_span=f'<span id="podcast-{kind}-duration">{duration(track["seconds"])}</span>' if live else duration(track['seconds'])
    # The live player keeps its original IDs; the cover metadata follows the manifest too.
    if live:image=f'<div data-radio-cover="{kind}">{image}</div>'
    return f'<article class="radio-episode">{image}<div class="radio-copy"><p class="kicker">Le Podcast iA</p><h3 id="{cid}-title">{name}</h3><p>{desc}</p><p class="radio-duration">{duration_span} · FR</p></div><audio id="{cid}" controls preload="none" src="{e(track["src"])}" aria-labelledby="{cid}-title" style="grid-column:1/-1;width:100%;height:42px"></audio></article>'

def build():
    archive=json.loads((ROOT/'assets/podcast/episodes.json').read_text())['episodes']
    latest=json.loads((ROOT/'assets/podcast/latest.json').read_text())
    feed=json.loads((ROOT/'knowledge-hub/veille-ia/feed.json').read_text());last=max(x['date'] for x in feed);news=sorted([x for x in feed if x['date']==last],key=lambda x:-x.get('score',0))[:3]
    comic_root = ROOT/'knowledge-hub/comics'
    comic_editions = current_editions([ep for path in (comic_root/'episodes').glob('*.json') if (ep := json.loads(path.read_text())).get('status') == 'approved'])
    comic_latest = comic_editions[-1]
    comic_panel = next((p for p in comic_latest['panels'] if 'mistral' in p['news_ids']), comic_latest['panels'][0])
    comic_image = '/knowledge-hub/comics/' + comic_panel['image']
    for lang in ('fr','en'):
        en=lang=='en';prefix='/knowledge-hub/'+('en/' if en else '')
        intro='The daily signal. A voice to follow. A comic on Sunday.' if en else 'Le signal du jour. Une voix pour suivre. Un comic le dimanche.'
        title='Le Kiosque IA — Le Radar iA, Le Podcast iA & iAstro Sunday'
        content='<style>'+CSS+COVER_CSS+PHONE_CSS+'</style><div class="kiosk"><section class="kiosk-hero"><div class="kiosk-meta"><span>Knowledge Hub / Le Kiosque IA</span><span>'+('Read · Listen · Explore' if en else 'Lire · Écouter · Explorer')+'</span></div><div class="kiosk-intro"><div><h1>'+('Stay curious. <em>Keep up.</em>' if en else 'Garde le fil. <em>Reste curieux.</em>')+'</h1><p>'+intro+'</p></div><span class="kiosk-signature">Une sélection de Hugo Lahutte ↗</span></div></section>'
        radar_preview='<span class="format-preview format-telegram" aria-hidden="true">'+'<span class="telegram-device">'+phone()+'</span><span class="telegram-wordmark">Telegram<small>La veille dans ta poche</small></span></span>'
        podcast_preview='<span class="format-preview" aria-hidden="true"><img class="format-portrait" src="/assets/podcast/art/iastro-'+latest['date'][5:7]+'-v1.png" alt="" width="1254" height="1254"></span>'
        comic_preview='<span class="format-preview" aria-hidden="true"><span class="format-comic"><img src="/knowledge-hub/comics/art/2026-W41/mistral-v1.png" alt="" width="1536" height="1024"></span></span>'
        formats=[('https://t.me/VeilleIA_HL','01 / SUR TELEGRAM','Le Radar iA','La veille quotidienne, directement sur Telegram.','Rejoindre la chaîne ↗',radar_preview),('#podcasts','02 / À ÉCOUTER','Le Podcast iA','Le Flash ou Le Débrief, à ton rythme.','Écouter les épisodes ↓',podcast_preview),('#sunday','03 / LE DIMANCHE','iAstro Sunday','La semaine IA en comic, avec Hugo et iAstro.','Découvrir le comic ↓',comic_preview)]
        content+='<nav class="kiosk-formats" aria-label="Les trois rendez-vous">'+''.join(f'<a class="format-card" href="{anchor}" aria-label="{e(title)} — {e(action)}">{preview}<span class="format-copy"><span class="format-eyebrow">{eyebrow}</span><strong class="format-title">{title}</strong><span class="format-description">{description}</span><span class="format-action">{action}</span></span></a>' for anchor,eyebrow,title,description,action,preview in formats)+'</nav>'
        comic_url = prefix + 'comics/' + comic_latest['id'] + '/'
        week_links = ''.join(f'<a href="{prefix}comics/{ep["id"]}/" style="display:inline-flex;align-items:center;min-height:44px;padding:8px 12px;border:1px solid var(--border-strong);font-size:14px">{e(period(ep))}</a>' for ep in reversed(comic_editions))
        content+=f'<section id="sunday" class="kiosk-feature"><div><p class="kicker">03 / Le comic du dimanche</p><h2>iAstro<br>Sunday<span style="color:var(--c-red)">.</span></h2><span class="kiosk-tag">Hugo × iAstro · {e(period(comic_latest))}</span><p class="lead">Les grandes nouvelles de l’IA prennent vie dans l’atelier. Une histoire à la fois, avec ses dessins, ses explications et ses sources.</p><a class="btn btn--primary" href="{comic_url}">Lire le dernier numéro →</a><p class="kiosk-note">Chaque semaine · en français · {len(comic_latest["news"])} histoires · lecture mobile</p><a href="{prefix}comics/">Tous les numéros et les archives →</a><nav aria-label="Choisir une semaine de comics" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:16px">{week_links}</nav></div><a class="kiosk-comic" href="{comic_url}" aria-label="Lire iAstro Sunday du {e(period(comic_latest))}"><img src="{comic_image}" width="1536" height="1024" alt="{e(comic_panel["alt"].replace("Iastro","iAstro"))}"><span class="kiosk-comic-caption">{e(comic_latest["title"])}</span></a></section>'
        content+='<section id="podcasts" class="radio-section"><div class="kiosk-section-head"><div><p class="kicker">02 / L’actualité IA à écouter</p><h2>Le Podcast iA<span style="color:var(--c-red)">.</span></h2></div><p>Deux formats. Le même regard curieux.</p></div><div id="daily-podcast"><p class="kiosk-meta">Dernière édition · <time id="podcast-date">'+latest['date']+'</time></p><div id="podcast-tracks" class="radio-latest">'+''.join(episode_card(latest,k,True) for k in ('short','full'))+'</div><p id="podcast-fallback" hidden><a href="https://t.me/VeilleIA_HL">Retrouver les audios sur Telegram →</a></p></div><p class="kiosk-note">Audio en français, avec une voix de synthèse. iAstro change de tenue au fil des mois.</p><div class="radio-archive"><h3>À réécouter</h3>'
        for ep in archive:
            content+=f'<details><summary><span>{ep["date"][8:10]}.{ep["date"][5:7]}.{ep["date"][:4]}</span><span class="radio-duration">Flash {duration(ep["short"]["seconds"])} / Débrief {duration(ep["full"]["seconds"])}</span></summary><div class="radio-latest">'+''.join(episode_card(ep,k) for k in ('short','full'))+'</div></details>'
        content+='</div></section><section id="radar"><div class="kiosk-section-head"><div><p class="kicker">01 / La veille quotidienne sur Telegram</p><h2>Le Radar iA<span style="color:var(--c-red)">.</span></h2></div><a href="'+prefix+'veille-ia/">Toute la veille et ses sources →</a></div><ol class="kiosk-news">'
        for i,n in enumerate(news,1):content+=f'<li><span class="news-number">{i:02d}</span><div><h3><a href="{e(n["tweet_url"])}">{e(n["titre_fr"])}</a></h3><p>{e(n["resume_fr"][:200])}{"…" if len(n["resume_fr"])>200 else ""}</p></div><time datetime="{last}">{last[8:10]}.{last[5:7]}</time></li>'
        content+='</ol><p><a class="btn btn--primary" href="https://t.me/VeilleIA_HL">Rejoindre Le Radar iA sur Telegram ↗</a></p><p class="kiosk-note">Une sélection issue de la veille quotidienne. Remonte aux sources pour approfondir.</p></section><div class="kiosk-foot"><strong>LE KIOSQUE IA</strong><a href="https://t.me/VeilleIA_HL">Recevoir la veille sur Telegram ↗</a><a href="'+prefix+'">Retour au Knowledge Hub →</a></div></div>'
        if en:content=content.replace('<div class="kiosk">','<div class="kiosk"><p class="kiosk-note" lang="en">The editorial editions, comics and audio below are currently available in French.</p>',1)
        page=shell(title,intro,content,lang,root_path='/knowledge-hub/immersion-ia/')
        page=re.sub(r'<header style=.*?</header>',site_header(en),page,flags=re.S)
        page=page.replace('</head>', '<style>'+HOME_MEDIA_CSS+'</style></head>')
        page=page.replace('</body>', '<script>'+HOME_NAV_JS+'</script></body>')
        page=page.replace('</body>','<script src="/knowledge-hub/search.js?v=20260601d" defer></script><script src="/assets/podcast/player.js?v=20261017c" defer></script><script>document.addEventListener("play",event=>{if(event.target.tagName==="AUDIO")document.querySelectorAll("audio").forEach(a=>{if(a!==event.target)a.pause();});},true);</script></body>')
        page=page.replace('Hugo × Iastro · Dessins générés par IA. Direction éditoriale : Hugo Lahutte.','Le Kiosque IA · Hugo Lahutte.').replace('Hugo × Iastro · AI-generated artwork. Editorial direction: Hugo Lahutte.','Le Kiosque IA · Hugo Lahutte.')
        dest=ROOT/prefix.lstrip('/')/'immersion-ia/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
    # Stable, exact-size HTML layouts for browser export. No dates/durations baked into art.
    layouts=ROOT/'assets/podcast/cover-layouts';layouts.mkdir(exist_ok=True)
    for ep in archive:
        for kind in ('short','full'):
            name=f'{ep["date"]}-{kind}'
            page='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Le Podcast iA — '+name+'</title><link rel="preconnect" href="https://api.fontshare.com" crossorigin><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700,900&display=swap" rel="stylesheet"><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;800;900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="/knowledge-hub/style.css?v=20260622a"><style>'+COVER_CSS+'html,body{margin:0;padding:0;background:#FFFCF8;overflow:hidden}.podcast-cover{width:100vw;height:100vw;border:0}</style></head><body>'+cover(ep['date'],kind,ep[kind]['seconds'])+'</body></html>'
            (layouts/(name+'.html')).write_text(page)
    print('Le Kiosque IA FR/EN et dix mises en page de pochette préparés.')
if __name__=='__main__':build()
