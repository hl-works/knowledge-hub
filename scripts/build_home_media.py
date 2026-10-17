#!/usr/bin/env python3
"""Build KH's orientation and a compact promotion of the separate Veille IA space."""
import json
import re
from html import escape as e
from pathlib import Path
from comics_catalog import current_editions

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- home-media:start -->'
END = '<!-- home-media:end -->'
CSS = '''
.kh-intro{padding:52px 0 28px}.kh-intro-top{display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:center}.kh-intro h1{font-size:clamp(2.6rem,4.8vw,4.2rem);line-height:1.04;letter-spacing:-.045em;text-transform:none;margin:16px 0 0}.kh-intro h1 em{font-style:normal;color:var(--c-red)}.kh-intro .lead{font-size:1.1rem;line-height:1.6;margin:0}.kh-intro .btn-row{margin-top:22px}.kh-intro .btn{font-size:.75rem;padding:12px 18px}.kh-intro .caption{margin:18px 0 0}
.kh-paths{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:32px}.kh-path{display:flex;flex-direction:column;gap:10px;padding:20px;border:1px solid var(--border);text-decoration:none;min-width:0;background:var(--bg)}.kh-path:hover{border-color:var(--c-red);background:var(--surface)}.kh-path small{font:11px var(--font-mono);color:var(--c-red)}.kh-path strong{font:800 1.25rem var(--font-display)}.kh-path span{font-size:.85rem;line-height:1.45;color:var(--text-muted)}
.kh-veille-push{padding:12px 0 40px;scroll-margin-top:100px}.kh-veille-banner{border:1px solid var(--border-strong);border-left:5px solid var(--c-red);background:var(--surface);padding:24px;display:grid;grid-template-columns:76px 1fr;gap:20px}.kh-veille-banner>img{width:76px;height:76px;object-fit:contain;background:var(--c-white)}.kh-veille-heading{display:flex;justify-content:space-between;gap:20px;align-items:center}.kh-veille-heading h2{font-size:1.65rem;line-height:1.15;text-transform:none;margin:0}.kh-veille-heading .kicker{font-size:.65rem;margin-bottom:6px}.kh-veille-heading>a{font-size:.8rem;white-space:nowrap}.kh-veille-formats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;grid-column:1/-1;border-top:1px solid var(--border);padding-top:16px}.kh-veille-formats a{font-size:.9rem;text-decoration:none;font-weight:700;display:block}.kh-veille-formats a:hover{color:var(--c-red)}.kh-veille-formats small{display:block;font-size:.75rem;line-height:1.5;font-weight:400;color:var(--text-muted);margin-top:4px}.kh-veille-banner .caption{grid-column:1/-1;margin:0;font-size:.75rem}.kh-growth{padding:24px 0 40px}.kh-growth .container{display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center}.kh-growth h2{font-size:clamp(1.7rem,3vw,2.5rem);text-transform:none;line-height:1.1;margin:12px 0 16px}.kh-growth img{width:100%;height:330px;object-fit:cover;object-position:top;border:1px solid var(--border)}.kh-growth p{font-size:1rem;line-height:1.6}.kh-growth .caption{font-size:.75rem}.kh-growth .btn{margin-top:16px}
.kh-path:focus-visible,.kh-veille-banner a:focus-visible{outline:3px solid var(--c-red);outline-offset:4px}
@media(min-width:761px) and (max-width:1100px){.nav{flex-wrap:wrap;gap:12px}.nav>nav{width:100%}.nav__links{justify-content:space-between;gap:12px}}
@media(max-width:760px){.kh-intro{padding:28px 0 16px}.kh-intro-top{grid-template-columns:1fr;gap:24px}.kh-intro h1{font-size:2.65rem}.kh-intro .lead{font-size:1rem}.kh-paths{grid-template-columns:1fr 1fr;gap:10px;margin-top:24px}.kh-path{padding:16px;gap:8px}.kh-path strong{font-size:1.05rem}.kh-path span{font-size:.8rem}.kh-veille-banner{padding:18px;grid-template-columns:54px 1fr;gap:14px}.kh-veille-banner>img{width:54px;height:54px}.kh-veille-heading{display:block}.kh-veille-heading h2{font-size:1.35rem}.kh-veille-heading>a{display:inline-block;margin-top:10px;white-space:normal}.kh-veille-formats{grid-template-columns:1fr;gap:14px}.kh-veille-formats a{min-height:44px}.kh-growth .container{grid-template-columns:1fr;gap:24px}}
'''

def latest_comic():
    episodes = [json.loads(p.read_text()) for p in (ROOT/'knowledge-hub/comics/episodes').glob('*.json')]
    approved = [ep for ep in episodes if ep.get('status') == 'approved' and all(ep.get('approval',{}).get(k) is True for k in ('editorial','art','publish')) and (ROOT/f'knowledge-hub/comics/{ep["id"]}/index.html').is_file()]
    return current_editions(approved)[-1]

def build():
    latest=json.loads((ROOT/'assets/podcast/latest.json').read_text())
    comic=latest_comic()
    for en in (False,True):
        prefix='/knowledge-hub/'+('en/' if en else '')
        path=ROOT/(prefix.lstrip('/')+'index.html');raw=path.read_text()
        tr=lambda fr,eng:eng if en else fr
        count=re.search(r'id="stat-sessions">(\d+)<',raw).group(1)
        comic_url=prefix+'comics/'+comic['id']+'/'
        routes=[('how-to/','01 / '+tr('La méthode','The method'),tr('Commencer','Get started'),tr('Mon organisation, mes outils et mes fichiers de contexte.','My workflow, tools and context files.')),('guides/','02 / '+tr('Les guides','The guides'),tr('Comprendre','Understand'),tr('Des explications claires, du premier repère au cas concret.','Clear explanations, from first principles to real examples.')),('#projets','03 / '+tr('Les projets','The projects'),tr('Voir le terrain','Explore the work'),tr('Commerce, audio, outils métier : ce que je construis vraiment.','Commerce, audio and business tools: what I actually build.')),('journal/','04 / '+tr('Le journal','The journal'),tr('Suivre les chantiers','Follow the projects'),tr('Les décisions, les essais et les leçons, session après session.','Decisions, experiments and lessons, session by session.'))]
        route_html=''.join(f'<a class="kh-path" href="{url}"><small>{e(label)}</small><strong>{e(title)} ↗</strong><span>{e(desc)}</span></a>' for url,label,title,desc in routes)
        hero=f'''<section class="kh-intro"><div class="container"><div class="kh-intro-top"><div><p class="kicker">Knowledge Hub · Hugo Lahutte</p><h1>{tr('Construire avec l’IA.<br><em>Partager ce qui marche.</em>','Build with AI.<br><em>Share what works.</em>')}</h1></div><div><p class="lead">{tr('Un carnet de terrain pour passer des outils aux projets. Je partage ma méthode, des guides et les coulisses de ce que je construis : ce qui fonctionne, ce qui coince et ce que j’en retiens.','A field notebook for turning tools into projects. My method, practical guides and a look behind the scenes: what works, what gets in the way and what I learn.')}</p><div class="btn-row"><a class="btn btn--primary" href="how-to/">{tr('Découvrir ma méthode →','Explore my method →')}</a><a class="btn btn--ghost" href="#projets">{tr('Voir les projets','See the projects')}</a></div><p class="caption"><b id="stat-sessions">{count}</b> {tr('sessions documentées · des projets réels, des retours concrets.','documented sessions · real projects, practical lessons.')}</p></div></div><nav class="kh-paths" aria-label="{tr('Explorer le Knowledge Hub','Explore the Knowledge Hub')}">{route_html}</nav></div></section>'''
        raw,n=re.subn(r'<section class="(?:hero home-intro|kh-intro)">.*?</section>',lambda _:hero,raw,count=1,flags=re.S)
        if n!=1:raise ValueError('Home introduction not found')
        banner=f'''{START}
<section id="a-la-une" class="kh-veille-push" aria-labelledby="kh-veille-title"><div class="container"><aside class="kh-veille-banner"><img src="/assets/podcast/art/iastro-{latest['date'][5:7]}-v1.png" alt="iAstro" width="76" height="76"><div class="kh-veille-heading"><div><p class="kicker">{tr('À suivre aussi · la Veille IA','Also follow · AI watch')}</p><h2 id="kh-veille-title">{tr('L’actualité IA, en trois rendez-vous.','AI news, in three formats.')}</h2></div><a href="{prefix}immersion-ia/">{tr('Découvrir la Veille IA →','Explore AI watch →')}</a></div><nav class="kh-veille-formats" aria-label="{tr('Les trois formats de la Veille IA','Three ways to follow AI news')}"><a href="https://t.me/VeilleIA_HL">{tr('Les news sur Telegram ↗','News on Telegram ↗')}<small>{tr('Le Radar iA · les nouvelles à retenir.','Le Radar iA · the news worth following.')}</small></a><a href="{prefix}immersion-ia/#podcasts">{tr('Écouter le podcast →','Listen to the podcast →')}<small>{tr('Le Flash et le Débrief · chaque jour.','Le Flash and Le Débrief · every day.')}</small></a><a href="{comic_url}">{tr('Lire le comic du dimanche →','Read the Sunday comic →')}<small>iAstro Sunday · Hugo × iAstro.</small></a></nav><p class="caption">{tr('Un abonnement commun sur Telegram pour suivre les trois rendez-vous.','One shared Telegram subscription for all three formats.')}</p></aside></div></section>
{END}'''
        raw=re.sub(re.escape(START)+r'.*?'+re.escape(END),lambda _:banner,raw,flags=re.S)
        raw=re.sub(r'<li class="home-news-nav">.*?</li>',f'<li><a href="{prefix}immersion-ia/">{tr("Veille IA","AI watch")}</a></li>',raw,flags=re.S)
        style='<style id="home-media-style">'+CSS+'</style>'
        raw=re.sub(r'<style id="home-media-style">.*?</style>',lambda _:style,raw,flags=re.S)
        raw=re.sub(r'<script id="home-media-behavior">.*?</script>\s*<script src="/assets/podcast/player.js[^\"]*" defer></script>','',raw,flags=re.S)
        # Keep KH's home as an orientation page, with detail in the dedicated guides.
        raw=re.sub(r'<section id="methode">.*?</section>','',raw,flags=re.S)
        raw=re.sub(r'<section id="guides">.*?</section>','',raw,flags=re.S)
        growth=f'''<section id="nouveau" class="kh-growth"><div class="container"><div><p class="kicker">{tr('Dans les coulisses · une étude de cas','Behind the scenes · a case study')}</p><h2>{tr('Comment notre veille devient un média.','How our news watch is becoming a media project.')}</h2><p>{tr('Avec ChatGPT et Codex : un podcast court et long, les comics du dimanche, la création d’iAstro et tout un travail de design. Les coulisses d’une veille qui s’améliore — et d’une méthode adaptable à d’autres sujets.','With ChatGPT and Codex: short and long podcasts, Sunday comics, the creation of iAstro and the full design process. How our news watch is evolving, with a method that can be adapted to other subjects.')}</p><a class="btn btn--primary" href="journal/veille-podcast-comics-iastro-chatgpt.html">{tr('Lire le retour d’expérience →','Read the case study →')}</a></div><figure><img src="/knowledge-hub/comics/kit/assets/characters/duo-reference-v2.png" alt="{tr('Fiche de recherche du duo Hugo et iAstro','Hugo and iAstro character research sheet')}" loading="lazy" decoding="async"><figcaption class="caption">{tr('Hugo × iAstro · les recherches de personnages.','Hugo × iAstro · character research.')}</figcaption></figure></div></section>'''
        raw=re.sub(r'<section id="nouveau"[^>]*>.*?</section>',lambda _:growth,raw,flags=re.S)
        # Route cards replace the long guide teasers; retain projects, journal and contact.
        raw=re.sub(r'<title>.*?</title>', '<title>'+tr('Knowledge Hub — Méthode, guides et projets avec l’IA · Hugo Lahutte','Knowledge Hub — AI methods, guides and projects · Hugo Lahutte')+'</title>',raw,count=1)
        desc=tr('La méthode, les guides et les projets de Hugo Lahutte : des retours de terrain pour construire avec l’IA. Retrouvez aussi la Veille IA, ses podcasts et ses comics.','Hugo Lahutte’s method, guides and projects: practical lessons from building with AI. Also discover AI news, podcasts and comics.')
        raw=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*(">)',lambda m:m[1]+e(desc,quote=True)+m[2],raw)
        footer=re.search(r'<footer.*?</footer>',raw,re.S)
        if footer:
            updated=footer.group().replace('href="'+prefix+'veille-ia/"','href="'+prefix+'immersion-ia/"')
            raw=raw[:footer.start()]+updated+raw[footer.end():]
        path.write_text(raw)
    print('KH FR/EN: orientation, method, projects and compact Veille IA banner; no audio players on home.')

if __name__=='__main__':build()
