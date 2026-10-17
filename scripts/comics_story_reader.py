"""Story-first comic composition: native vertical reading, editable balloons and notes."""
from html import escape as e
from datetime import date
from comics_reader import BRANDS

CSS = '''
html:has(.sunday){scroll-behavior:auto}
main:has(.sunday){max-width:1120px;padding-inline:24px}
.sunday{--sunday-accent:var(--c-red);--ink:var(--c-black);--paper:var(--c-offwhite);color:var(--text);max-width:1060px;margin:auto}
.sunday *{box-sizing:border-box}.sunday [hidden]{display:none!important}
.sunday h1,.sunday h2,.sunday h3{text-transform:none;letter-spacing:-.025em}
.sunday a{color:inherit;text-underline-offset:4px}.sunday :focus-visible:not([tabindex="-1"]){outline:3px solid var(--sunday-accent);outline-offset:5px}
.sunday .edition{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font:12px 'IBM Plex Mono',monospace;border-bottom:2px solid var(--text);padding-bottom:14px}
.sunday .masthead{font:900 clamp(2.7rem,9vw,5rem)/.98 'Archivo',sans-serif;margin:22px 0 16px}
.sunday .masthead em{color:var(--sunday-accent);font-style:normal}.sunday .dek{max-width:680px;font-size:18px;line-height:1.6;margin:0 0 24px}
.sunday .preview-note{font-size:13px;line-height:1.5;border-left:3px solid var(--sunday-accent);padding:8px 12px;margin:0 0 22px}
.sunday .contents{scroll-margin-top:84px;margin-bottom:42px}.sunday .contents h2{font-size:21px;margin:0 0 16px}
.sunday .contents-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.sunday .contents-card{display:grid;grid-template-columns:84px 1fr;gap:14px;align-items:center;border:1px solid var(--border-strong);padding:12px;text-decoration:none;min-width:0;background:var(--surface)}
.sunday .contents-card:hover{border-color:var(--sunday-accent)}.sunday .contents-card strong{display:block;font-size:18px;line-height:1.25;margin:5px 0}.sunday .contents-card small{font-size:12px;line-height:1.4}.sunday .contents-card .crop{border:1px solid var(--ink)}
.sunday .crop{position:relative;overflow:hidden;aspect-ratio:1;background:var(--paper)}.sunday .crop img{display:block;position:absolute;max-width:none}
.sunday .readbar{position:sticky;top:0;z-index:10;background:var(--bg);border-block:1px solid var(--border-strong);padding:8px 0;display:flex;gap:12px;align-items:center;margin-bottom:36px}
.sunday .readbar a{min-height:44px;display:flex;align-items:center;font-weight:700;font-size:14px;white-space:nowrap}
.sunday .readbar select{font:inherit;font-size:14px;min-height:44px;min-width:0;flex:1;color:var(--text);background:var(--surface);border:1px solid var(--border-strong);border-radius:0;padding:8px 28px 8px 10px;max-width:300px;margin-left:auto}
.sunday .story{padding:0;scroll-margin-top:84px;margin:0 0 76px}.sunday .story-heading{display:grid;grid-template-columns:72px 1fr;gap:18px;margin-bottom:28px;padding-bottom:24px;border-bottom:3px solid var(--text)}
.sunday .brand-logo{display:flex;align-items:center;justify-content:center;background:var(--c-white);padding:10px;width:72px;height:72px;border:1px solid var(--c-platinum)}
.sunday .brand-logo.wordmark{width:128px;height:52px;grid-column:1/-1}.sunday .story-heading:has(.wordmark)>div{grid-column:1/-1}
.sunday .brand-logo img{width:100%;height:100%;object-fit:contain}.sunday .eyebrow{font:12px/1.5 'IBM Plex Mono',monospace;color:var(--sunday-accent);margin:0 0 8px}
.sunday .story-heading h2{font:900 clamp(1.8rem,5vw,2.9rem)/1.08 'Archivo',sans-serif;margin:0 0 14px;max-width:720px}.sunday .story-summary{grid-column:1/-1;font-size:18px;line-height:1.55;margin:0;max-width:730px}
.sunday .scenes{display:grid;grid-template-columns:1fr 1fr;gap:32px 24px;align-items:start}
.sunday .scene{min-width:0;margin:0;scroll-margin-top:84px}
.sunday .panel{border:2px solid var(--ink);background:var(--paper);color:var(--ink);box-shadow:3px 3px 0 var(--ink)}
.sunday .speech-track{display:flex;flex-direction:column;gap:12px;padding:14px 14px 22px;position:relative;z-index:1;background:var(--paper)}
.sunday .speech{font:700 18px/1.35 'Satoshi',system-ui,sans-serif;position:relative;background:var(--c-white);border:2px solid var(--ink);border-radius:48% 46% 44% 40% / 20px 22px 20px 22px;padding:12px 18px;margin:0;max-width:94%;align-self:flex-start}
.sunday .speech.right{align-self:flex-end}.sunday .speech:after{content:'';position:absolute;bottom:-12px;left:28px;width:16px;height:20px;background:var(--c-white);border-right:2px solid var(--ink);border-bottom:2px solid var(--ink);transform:skewY(35deg)}
.sunday .speech.right:after{left:auto;right:28px;transform:skewY(-35deg);border-right:0;border-left:2px solid var(--ink)}
.sunday .speech strong{display:block;text-transform:none;font:700 11px/1.2 'IBM Plex Mono',monospace;margin-bottom:4px}
.sunday .scene-note{padding:20px 4px 0}.sunday .scene-note h3{font-size:18px;line-height:1.3;margin:0 0 8px;display:flex;align-items:baseline;gap:10px}.sunday .scene-number{font:12px 'IBM Plex Mono',monospace;color:var(--sunday-accent)}
.sunday .scene-note p{font-size:17px;line-height:1.65;margin:0}.sunday .source{font-size:14px;line-height:1.6;border-top:1px solid var(--border);padding-top:18px;margin-top:32px}.sunday .source a{display:inline-block;padding-block:8px}
.sunday .story-end{display:flex;justify-content:space-between;gap:16px;align-items:center;border-block:2px solid var(--text);padding:16px 0;margin-top:20px;flex-wrap:wrap}
.sunday .story-end a{min-height:48px;display:flex;align-items:center;font-size:15px;font-weight:700}.sunday .story-end .next{background:var(--text);color:var(--bg);padding:12px 18px;text-decoration:none}
.sunday .endnote{font-size:14px;line-height:1.6;border-top:1px solid var(--border);padding-top:20px}.sunday .readbar .bar-label{font-size:12px;color:var(--text-muted)}
@media(max-width:699px){main:has(.sunday){padding-inline:16px}main:has(.sunday)>section{padding-block:18px}.sunday .contents-grid,.sunday .scenes{grid-template-columns:1fr}.sunday .scenes{gap:36px}.sunday .story-heading{grid-template-columns:52px 1fr;gap:12px}.sunday .brand-logo{width:52px;height:52px;padding:8px}.sunday .story-summary{grid-column:1/-1;font-size:17px}.sunday .story-heading h2{font-size:29px}.sunday .readbar{gap:10px;margin-bottom:26px}.sunday .readbar .bar-label{display:none}.sunday .readbar select{font-size:13px;padding-left:8px}.sunday .story{margin-bottom:56px}.sunday .story-heading{margin-bottom:20px}.sunday .speech{font-size:18px}.sunday .speech-track{padding:12px 12px 20px}.sunday .contents{margin-bottom:26px}.sunday .dek{font-size:17px}.sunday .edition{font-size:11px}.sunday .story-end .next{max-width:100%}.sunday .scene-note p{font-size:18px;line-height:1.6}
body:has(.sunday)>header{padding:12px 16px!important;gap:8px!important}body:has(.sunday)>header nav{gap:12px!important;font-size:12px}body:has(.sunday)>header nav>a:nth-child(2){display:none}body:has(.sunday)>header .nav__wordmark{font-size:15px}body:has(.sunday)>header button{min-height:44px;font-size:11px;padding:8px}}
[data-theme="dark"] .sunday{--sunday-accent:var(--c-sunset)}
@media print{.sunday .readbar,.sunday .contents,.sunday .story-end,body:has(.sunday)>header{display:none}.sunday .scene{break-inside:avoid}.sunday .scenes{grid-template-columns:1fr 1fr}.sunday .story{break-before:page}}
'''

JS = '''
(()=>{
const root=document.querySelector('.sunday');if(!root)return;
const bar=root.querySelector('.readbar'), select=bar.querySelector('select');
const stories=[...root.querySelectorAll('.story')];
bar.hidden=false;
select.addEventListener('change',()=>{if(select.value)location.hash=select.value;else location.hash='sommaire';});
// Native anchors retain browser Back, zoom, text selection and scrolling.
// Track the section under the toolbar; never move the page on resize or scroll.
let scheduled=false;
function position(){scheduled=false;let active='';const line=120;
for(const story of stories){if(story.getBoundingClientRect().top<=line)active=story.id;}
if(document.documentElement.scrollHeight-innerHeight-scrollY<4)active=stories.at(-1).id;
select.value=active;
}
addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(position);}},{passive:true});
addEventListener('resize',position);addEventListener('pageshow',position);
root.addEventListener('click',event=>{const link=event.target.closest('a[href^="#"]');if(!link)return;const target=document.getElementById(link.hash.slice(1));if(target){target.focus({preventScroll:true});}});
position();
})();
'''

def art(panel,base,dimensions):
    width,height=dimensions(panel['image']); c=panel.get('crop',{'x':0,'y':0,'w':1,'h':1})
    style=f'width:{100/c["w"]:.6f}%;height:{100/c["h"]:.6f}%;left:{-100*c["x"]/c["w"]:.6f}%;top:{-100*c["y"]/c["h"]:.6f}%'
    return f'<div class="crop" style="aspect-ratio:{width*c["w"]}/{height*c["h"]}"><img src="{base+e(panel["image"])}" width="{width}" height="{height}" alt="{e(panel["alt"].replace("Iastro","iAstro"))}" loading="lazy" decoding="async" style="{style}"></div>'

def render(ep,base,dimensions,preview=False):
    count=len(ep['news'])
    start=date.fromisoformat(ep['period_start']);end=date.fromisoformat(ep['period_end'])
    months=('janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre')
    period=f'{start.day} {months[start.month-1]} – {end.day} {months[end.month-1]} {end.year}'
    menu=[];stories=[];options=['<option value="">Choisir une info</option>']
    for ni,n in enumerate(ep['news']):
        nid=n['id']; brand,logo=BRANDS[n['brand_id']]; panels=[p for p in ep['panels'] if nid in p['news_ids']]
        options.append(f'<option value="info-{e(nid)}">{ni+1}/{count} · {e(n["model_label"])}</option>')
        menu.append(f'<a class="contents-card" href="#info-{e(nid)}">{art(panels[0],base,dimensions)}<span><small>{ni+1:02d} / {e(brand)} · {e(n["model_label"])}</small><strong>{e(n["intro"]["title"])}</strong><small>Lire les {len(panels)} cases →</small></span></a>')
        scenes=[]
        for pi,p in enumerate(panels):
            bubbles=[]
            for line in p['dialogue']:
                speaker=line['speaker'].replace('Iastro','iAstro')
                side=line.get('side','left')
                bubbles.append(f'<p class="speech {e(side)}"><strong>{e(speaker)}</strong>{e(line["text"])}</p>')
            scenes.append(f'<figure class="scene" id="{e(nid)}-case-{pi+1}" tabindex="-1"><div class="panel"><div class="speech-track">{"".join(bubbles)}</div>{art(p,base,dimensions)}</div><figcaption class="scene-note"><h3><span class="scene-number">{pi+1:02d}/{len(panels):02d}</span>{e(p["explanation"]["title"])}</h3><p>{e(p["explanation"]["text"])}</p></figcaption></figure>')
        src=' · '.join(f'<a href="{e(s["url"])}">{e(s["publisher"])} — annonce du {e(s["published_at"][8:])}/{e(s["published_at"][5:7])}</a>' for s in n['sources'])
        if ni<len(ep['news'])-1:
            nxt=ep['news'][ni+1]; nextlink=f'<a class="next" href="#info-{e(nxt["id"])}">Info suivante · {e(nxt["model_label"])} →</a>'
        else:nextlink='<a class="next" href="/knowledge-hub/immersion-ia/">Fin du numéro · Le Kiosque IA →</a>'
        stories.append(f'<section class="story" id="info-{e(nid)}" tabindex="-1" aria-labelledby="title-{e(nid)}"><header class="story-heading"><span class="brand-logo {"wordmark" if n["brand_id"] == "mistral" else ""}"><img src="{base}brands/{logo}" alt="{e(brand)}" width="72" height="72"></span><div><p class="eyebrow">{ni+1:02d} / {count:02d} · {e(brand)} · {e(n["model_label"])}</p><h2 id="title-{e(nid)}">{e(n["intro"]["title"])}</h2></div><p class="story-summary">{e(n["intro"]["summary"])}</p></header><div class="scenes">{"".join(scenes)}</div><p class="source">Pour vérifier l’annonce : {src}<br>Les scènes sont imaginées. Les paragraphes sous les cases expliquent les faits et notre lecture de leurs usages.</p><nav class="story-end" aria-label="Après {e(n["model_label"])}"><a href="#sommaire">↑ Les {count} infos</a>{nextlink}</nav></section>')
    note=f'<p class="preview-note">Version de travail · {e(ep.get("correction_note","À relire avant publication."))}</p>' if preview else ''
    return f'''<style>{CSS}</style><article class="sunday" aria-label="iAstro Sunday, {e(period)}">
<div class="edition"><span>HUGO × iAstro</span><span>{e(period.upper())}</span></div>
<h1 class="masthead">iAstro <em>Sunday.</em></h1><p class="dek">{e(ep.get("reader_description", "Les nouvelles de l’IA, racontées dans l’atelier. Des scènes, des explications et un peu de recul."))}</p>{note}
<nav class="contents" id="sommaire" tabindex="-1" aria-labelledby="contents-title"><h2 id="contents-title">Cette semaine, dans l’atelier</h2><div class="contents-grid">{''.join(menu)}</div></nav>
<nav class="readbar" aria-label="Navigation du comic" hidden><a href="#sommaire">↑ Sommaire</a><span class="bar-label">Fais défiler pour lire</span><select aria-label="Aller à une info">{''.join(options)}</select></nav>
{''.join(stories)}<p class="endnote">Hugo × iAstro · Dessins générés par IA, sélection et direction éditoriale : Hugo Lahutte. Cette édition revient sur la semaine du {e(period)} ; les disponibilités indiquées sont celles annoncées à cette date.</p></article><script>{JS}</script>'''
