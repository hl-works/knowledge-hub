#!/usr/bin/env python3
"""Build the local Immersion IA landing page and dated podcast archive."""
import json
from pathlib import Path
from html import escape as e
from build_comics import shell
ROOT=Path(__file__).resolve().parents[1]

def duration(seconds):return f'{seconds//60}:{seconds%60:02d}'

def build():
    archive=json.loads((ROOT/'assets/podcast/episodes.json').read_text())['episodes']
    latest=json.loads((ROOT/'assets/podcast/latest.json').read_text())
    for lang in ('fr','en'):
        en=lang=='en';prefix='/knowledge-hub/'+('en/' if en else '')
        heading='One week. Three ways to explore AI.' if en else 'L’IA à lire, à écouter, à découvrir en BD.'
        cards=[('01','AI watch' if en else 'La veille IA','The news and its sources, every day.' if en else 'Les annonces et leurs sources, chaque jour.',prefix+'veille-ia/','Read the brief →' if en else 'Lire la veille →'),('02','Podcasts','Short or full briefings. Audio in French.' if en else 'L’essentiel ou le tour complet, avec une voix de synthèse.','#podcasts','Listen →' if en else 'Écouter →'),('03','IA immersion BD','Hugo and Iastro bring the week to life.' if en else 'Hugo et Iastro racontent les grandes infos de la semaine.',prefix+'comics/','Discover the comic →' if en else 'Découvrir la BD →')]
        content=f'<style>.immersion-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:20px}}.immersion-card{{border:1px solid var(--border-strong);border-radius:12px;padding:24px;background:var(--surface)}}.immersion-card h2{{font-size:1.5rem;margin:12px 0}}.immersion-card p{{line-height:1.6}}.podcast-row{{padding:20px 0;border-top:1px solid var(--border)}}.podcast-row summary{{cursor:pointer;min-height:44px;padding:12px 0}}.podcast-row audio{{width:100%;margin:8px 0 20px}}#podcasts{{scroll-margin-top:24px}}.immersion-links{{display:flex;gap:20px;flex-wrap:wrap}}</style><section><p class="kicker">Knowledge Hub · Immersion IA</p><h1 style="font-size:clamp(2rem,6vw,4rem);max-width:22ch">{heading}</h1><p class="lead">'+('A single home for the daily brief, audio and weekly comics.' if en else 'Un même rendez-vous pour garder le fil : la veille quotidienne, les podcasts et les comics hebdomadaires.')+'</p><div class="immersion-grid">'
        for number,title,desc,link,cta in cards:content+=f'<article class="immersion-card"><span class="kicker">{number}</span><h2>{title}</h2><p>{desc}</p><a href="{link}">{cta}</a></article>'
        content+='</div></section><section id="podcasts"><p class="kicker">'+('Listen to AI news' if en else 'L’actualité IA à écouter')+'</p><h2>Podcasts</h2><p>'+('Dated daily editions, in French. The archive currently covers October 12–16; it is not a weekly roundup.' if en else 'Des éditions quotidiennes datées, en version courte ou complète. L’archive disponible couvre le 12–16 octobre ; il ne s’agit pas d’un récapitulatif hebdomadaire.')+'</p>'
        # Keep the live latest edition using the existing player contract.
        content+='<div id="daily-podcast" class="podcast-row"><h3>'+('Latest edition' if en else 'Dernière édition')+' · <time id="podcast-date"></time></h3><div id="podcast-tracks" hidden>'
        for name,label in [('short','L’essentiel'),('full','Le tour complet')]:content+=f'<h4 id="podcast-{name}-title">{label} · <span id="podcast-{name}-duration"></span></h4><audio id="podcast-{name}" controls preload="none" aria-labelledby="podcast-{name}-title"></audio>'
        content+='</div><p id="podcast-fallback"><a href="https://t.me/VeilleIA_HL">'+('Listen on Telegram' if en else 'Écouter sur Telegram')+'</a></p></div><h3>'+('Dated archives' if en else 'Les éditions à retrouver')+'</h3>'
        for episode in archive:
            content+=f'<details class="podcast-row"><summary>{episode["date"]} · {duration(episode["short"]["seconds"])} / {duration(episode["full"]["seconds"])}</summary>'
            for name,label in [('short','L’essentiel'),('full','Le tour complet')]:
                audio=episode[name];assert (ROOT/audio['src'].lstrip('/')).is_file()
                content+=f'<p id="audio-{episode["date"]}-{name}">{label} · {duration(audio["seconds"])}</p><audio controls preload="none" src="{e(audio["src"])}" aria-labelledby="audio-{episode["date"]}-{name}"></audio>'
            content+='</details>'
        content+='</section><script src="/assets/podcast/player.js" defer></script><script>document.addEventListener("play",event=>{if(event.target.tagName==="AUDIO")document.querySelectorAll("audio").forEach(a=>{if(a!==event.target)a.pause();});},true);</script>'
        page=shell('Immersion IA — veille, podcasts et BD',heading,content,lang,root_path='/knowledge-hub/immersion-ia/')
        page=page.replace('Hugo × Iastro · Dessins générés par IA. Direction éditoriale : Hugo Lahutte.','Veille, podcasts et BD · Hugo Lahutte.').replace('Hugo × Iastro · AI-generated artwork. Editorial direction: Hugo Lahutte.','AI watch, podcasts and comics · Hugo Lahutte.')
        dest=ROOT/prefix.lstrip('/')/'immersion-ia/index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
    print('Immersion IA FR/EN et cinq éditions audio préparées localement.')
if __name__=='__main__':build()
