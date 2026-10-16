"""Accessible mobile comic: one illustrated panel per swipe, optional vertical reading."""
import html
from datetime import date

def e(v):return html.escape(str(v),quote=True)

BRANDS={
    'openai':('OpenAI','openai.png'),
    'anthropic':('Anthropic','anthropic.png'),
    'mistral':('Mistral','mistral.svg'),
    'google':('Google DeepMind','google.png'),
}


CSS='''
main:has(.comic-reader)>section{padding-block:20px}
.comic-reader{max-width:560px;margin:0 auto;color:var(--text)}
.comic-reader *{box-sizing:border-box}.comic-reader h2,.comic-reader h3{letter-spacing:0;text-transform:none}
.comic-reader .issue-title{font-size:clamp(1.6rem,5vw,2.3rem);line-height:1.1;margin:8px 0 16px}
.comic-reader .issue-meta{font-size:.85rem;margin:0}.comic-reader .reader-help{font-size:.95rem;line-height:1.5;margin:12px 0}
.comic-reader .chapter-menu{margin:24px 0;scroll-margin-top:20px}
.comic-reader .chapter-heading{font-size:1.4rem;margin:0 0 6px}
.comic-reader .chapter-hint{font-size:1rem;line-height:1.5;margin:0 0 16px}
.comic-reader .chapter-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:16px 0}
.comic-reader .chapter-links .chapter-card{display:flex;flex-direction:column;align-items:flex-start;gap:10px;padding:16px;border-radius:16px;border-width:2px;box-shadow:3px 3px 0 var(--border-strong);min-width:0;overflow-wrap:anywhere}
.comic-reader .chapter-card:hover,.comic-reader .chapter-card[aria-current=step]{border-color:var(--c-red)}
.comic-reader .chapter-card-top{display:flex;align-items:center;justify-content:space-between;width:100%;gap:8px}
.comic-reader .chapter-number{font-size:.8rem;font-weight:700;color:var(--text-muted)}
.comic-reader .chapter-model{font-size:.85rem;color:var(--text-muted);line-height:1.4}
.comic-reader .chapter-name{font-size:1.125rem;line-height:1.25}
.comic-reader .chapter-enter{font-size:.85rem;margin-top:auto;padding-top:6px}
.comic-reader .reader-home{flex:0 0 100%;color:var(--text);min-height:44px;display:flex;align-items:center;gap:8px;font-size:.95rem;text-underline-offset:4px}
@media(max-width:379px){.comic-reader .chapter-links{grid-template-columns:minmax(0,1fr)}}
.comic-reader button,.comic-reader .chapter-links a{border:1px solid var(--border-strong);background:var(--surface);color:var(--text);padding:10px 14px;min-height:44px;font:inherit;cursor:pointer;text-decoration:none;border-radius:8px}
.comic-reader button:disabled{opacity:.45;cursor:default}.comic-reader :focus-visible{outline:3px solid var(--c-red);outline-offset:3px}
.comic-reader .reader-controls{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:10px 0;background:var(--bg);border-bottom:1px solid var(--border)}
.comic-reader .reader-progress{margin:0 auto;font-size:.9rem;font-variant-numeric:tabular-nums}.comic-reader .reader-mode{margin-left:auto;font-size:.85rem}
.comic-reader .comic-track{scroll-margin-top:125px;display:block;outline-offset:3px;padding:12px 0}
.comic-reader .comic-card{width:100%;min-width:0;margin-bottom:40px;scroll-margin-top:125px;border:1px solid var(--border-strong);background:var(--surface);border-radius:12px;overflow:hidden}
.comic-reader .panel-label{font-size:.78rem;font-weight:700;margin:0;padding:12px 14px 4px;color:var(--text-muted)}
.comic-reader .panel-title{font-size:1.2rem;line-height:1.25;margin:0;padding:0 14px 12px}
.comic-reader .brand-label{display:flex;align-items:center;gap:8px;margin:0;padding:0 14px 12px;font-size:.85rem;line-height:1.35;overflow-wrap:anywhere}
.comic-reader .brand-icon{display:flex;align-items:center;justify-content:center;flex:0 0 32px;height:32px;padding:4px;border-radius:6px;background:#fff}
.comic-reader .brand-icon img{display:block;width:24px;height:24px;object-fit:contain}
.comic-reader .brand-icon.wordmark{flex-basis:80px}.comic-reader .brand-icon.wordmark img{width:72px;height:24px}
.comic-reader .story-intro{padding-bottom:24px}
.comic-reader .intro-body{padding:20px clamp(18px,5vw,32px) 12px}
.comic-reader .intro-logo{display:flex;align-items:center;justify-content:center;width:104px;height:104px;padding:16px;background:#fff;border-radius:16px;margin:0 0 20px}
.comic-reader .intro-logo img{width:72px;height:72px;object-fit:contain;display:block}
.comic-reader .intro-logo.wordmark{width:192px}.comic-reader .intro-logo.wordmark img{width:160px;height:72px}
.comic-reader .intro-brand{font-size:1rem;font-weight:700;line-height:1.4;margin:0 0 12px}
.comic-reader .intro-title{font-size:clamp(1.5rem,6vw,2rem);line-height:1.18;margin:0 0 16px}
.comic-reader .intro-summary{font-size:1.125rem;line-height:1.55;margin:0 0 24px}
.comic-reader .intro-cue{font-size:.9rem;color:var(--text-muted);margin:0}
.comic-reader .art-window{position:relative;overflow:hidden;width:100%;background:var(--bg)}
.comic-reader .art-window img{position:absolute;max-width:none;display:block;object-fit:fill}
.comic-reader .dialogue{padding:16px;display:grid;gap:12px}.comic-reader .bubble{font-size:1.125rem;line-height:1.5;margin:0;overflow-wrap:anywhere}
.comic-reader .bubble strong{display:block;font-size:.75rem;line-height:1.4;letter-spacing:.06em;margin-bottom:4px;text-transform:uppercase;color:var(--text-muted)}
.comic-reader .sources{font-size:1rem;line-height:1.6;margin-top:28px}.comic-reader .sources li{margin:16px 0}.comic-reader .sources a{overflow-wrap:anywhere}
.comic-reader .draft-label{padding:10px 12px;border-left:4px solid var(--c-red);background:var(--surface);font-size:.9rem;margin:0 0 14px}
.comic-reader .fiction-note{font-size:.85rem;line-height:1.5;color:var(--text-muted)}
.comic-reader[data-mode=swipe] .comic-track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px;align-items:flex-start;overscroll-behavior-x:contain;scrollbar-width:thin}
.comic-reader[data-mode=swipe] .comic-card{flex:0 0 100%;scroll-snap-align:start;scroll-snap-stop:always;margin-bottom:0}
.comic-reader[data-mode=swipe] .comic-card:not(.is-current) a{visibility:hidden}
.comic-reader .js-only[hidden]{display:none}
@media print{.comic-reader .reader-controls,.comic-reader .chapter-links,.comic-reader .reader-help{display:none!important}.comic-reader[data-mode] .comic-track{display:block;overflow:visible}.comic-reader .comic-card{break-inside:avoid;margin:0 0 24px}main:has(.comic-reader)>section{padding-block:20px}
.comic-reader{max-width:460px}}
@media(prefers-reduced-motion:reduce){.comic-reader *{scroll-behavior:auto!important}}
'''

CSS += '''
/* Separate the story chooser from the reading surface. */
.comic-reader{overflow-anchor:none;scroll-margin-top:12px}
.comic-reader .chapter-menu{padding:0;margin:24px 0}
.comic-reader[data-view=menu] .reading-stage{display:none}
.comic-reader[data-view=reading] .issue-overview,.comic-reader[data-view=reading] .chapter-menu{display:none}
.comic-reader .reader-controls{display:grid;grid-template-columns:auto 44px minmax(32px,1fr) 44px 44px;gap:6px;padding:8px 0;align-items:center}
.comic-reader .reader-home{font-size:.82rem;min-height:44px;white-space:nowrap;text-decoration:none;padding-right:4px}
.comic-reader .reader-controls button{padding:8px;min-width:44px}
.comic-reader .reader-mode{margin:0;font-size:1.1rem}
.comic-reader .reader-progress{font-size:.85rem;margin:0;text-align:center;white-space:nowrap}
.comic-reader .story-position{grid-column:1/-1;margin:0;font-size:.8rem;line-height:1.3;color:var(--text-muted)}
.comic-reader .comic-track{scroll-margin-top:95px;overflow-anchor:none}
.comic-reader[data-mode=swipe] .comic-track{transition:none;overflow-y:hidden}
.comic-reader .comic-card{scroll-margin-top:95px}
.comic-reader .reading-end{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}
.comic-reader .reading-end a{color:var(--text);padding:12px 0;min-height:44px}
@media print{.comic-reader[data-view] .reading-stage{display:block}.comic-reader .reading-end,.comic-reader .chapter-menu{display:none!important}.comic-reader[data-mode] .comic-track{height:auto!important}.comic-reader .comic-card{visibility:visible!important}}
'''

JS=r'''
(()=>{document.querySelectorAll('.comic-reader').forEach(root=>{
 const track=root.querySelector('.comic-track'),cards=[...root.querySelectorAll('.comic-card')];
 const chapters=[...root.querySelectorAll('[data-panel]')],menu=root.querySelector('.chapter-menu');
 const status=root.querySelector('.reader-progress'),position=root.querySelector('.story-position');
 const previous=root.querySelector('[data-step="-1"]'),next=root.querySelector('[data-step="1"]'),mode=root.querySelector('.reader-mode');
 let current=0,frame=0,chapter=0,navigating=false,navigationToken=0,verticalUserScroll=false;
 const fit=()=>{track.style.height=root.dataset.mode==='swipe'?`${cards[current].offsetHeight+24}px`:'';};
 const sizeObserver=new ResizeObserver(fit);
 function update(i){
  current=Math.max(0,Math.min(cards.length-1,i));
  chapter=chapters.findLastIndex(link=>Number(link.dataset.panel)<=current);
  const start=Number(chapters[chapter].dataset.panel),end=chapter+1<chapters.length?Number(chapters[chapter+1].dataset.panel):cards.length;
  status.textContent=`${current-start+1} / ${end-start}`;
  position.textContent=`Histoire ${chapter+1} / ${chapters.length} · ${chapters[chapter].querySelector('.chapter-model').textContent}`;
  previous.disabled=current===0;next.disabled=current===cards.length-1;
  next.setAttribute('aria-label',current===end-1?'Histoire suivante':'Case suivante');
  cards.forEach((c,j)=>{c.classList.toggle('is-current',j===current);c.inert=root.dataset.mode==='swipe'&&j!==current;});
  chapters.forEach((link,j)=>{if(j===chapter)link.setAttribute('aria-current','step');else link.removeAttribute('aria-current');});
  sizeObserver.disconnect();sizeObserver.observe(cards[current]);fit();
 }
 function setHash(value,push){if(location.hash!==value)history[push?'pushState':'replaceState'](null,'',value);}
 function go(i,{open=false,push=false,focus=false}={}){
  const token=++navigationToken;navigating=true;verticalUserScroll=false;cancelAnimationFrame(frame);track.style.scrollSnapType='none';root.dataset.view='reading';update(i);
  if(root.dataset.mode==='swipe')track.scrollTo({left:cards[current].offsetLeft-cards[0].offsetLeft,behavior:'instant'});
  if(open||root.dataset.mode==='swipe'){root.scrollIntoView({block:'start',behavior:'instant'});requestAnimationFrame(()=>root.scrollIntoView({block:'start',behavior:'instant'}));}
  else if(root.dataset.mode==='vertical')cards[current].scrollIntoView({block:'start',behavior:'instant'});
  setHash('#'+cards[current].id,push);
  if(focus)(root.dataset.mode==='swipe'?track:cards[current]).focus({preventScroll:true});
  requestAnimationFrame(()=>{if(token!==navigationToken)return;if(root.dataset.mode==='swipe')track.scrollTo({left:cards[current].offsetLeft-cards[0].offsetLeft,behavior:'instant'});requestAnimationFrame(()=>{if(token===navigationToken){track.style.scrollSnapType='';navigating=false;}});});
 }
 function home(push=true){root.dataset.view='menu';setHash('#sommaire',push);root.scrollIntoView({block:'start',behavior:'instant'});chapters[chapter].focus({preventScroll:true});}
 function route(){const index=cards.findIndex(c=>'#'+c.id===location.hash);if(index>=0)go(index,{open:true});else home(false);}
 root.querySelectorAll('.js-only').forEach(x=>x.hidden=false);root.dataset.mode='swipe';root.dataset.view='menu';track.tabIndex=0;cards.forEach(c=>c.tabIndex=-1);
 previous.addEventListener('click',()=>go(current-1));next.addEventListener('click',()=>go(current+1));
 track.addEventListener('keydown',ev=>{if(ev.target!==track)return;if(ev.key==='ArrowRight'){ev.preventDefault();go(current+1);}if(ev.key==='ArrowLeft'){ev.preventDefault();go(current-1);}if(ev.key==='Escape'){ev.preventDefault();home();}});
 track.addEventListener('scroll',()=>{if(navigating||root.dataset.mode!=='swipe'||root.dataset.view!=='reading')return;cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{const first=cards[0].offsetLeft;let nearest=current,distance=Infinity;cards.forEach((c,i)=>{const d=Math.abs(c.offsetLeft-first-track.scrollLeft);if(d<distance){distance=d;nearest=i;}});if(nearest!==current){update(nearest);setHash('#'+cards[current].id,false);}});},{passive:true});
 mode.addEventListener('click',()=>{const keep=current,vertical=root.dataset.mode==='swipe';navigating=true;cancelAnimationFrame(frame);track.style.scrollSnapType='none';root.dataset.mode=vertical?'vertical':'swipe';mode.textContent=vertical?'↔':'↕';mode.setAttribute('aria-pressed',String(vertical));mode.setAttribute('aria-label',vertical?'Passer en lecture par swipe':'Passer en lecture verticale');update(keep);requestAnimationFrame(()=>go(keep));});
 chapters.forEach(link=>link.addEventListener('click',ev=>{ev.preventDefault();go(Number(link.dataset.panel),{open:true,push:true,focus:true});}));
 root.querySelectorAll('[href="#sommaire"]').forEach(link=>link.addEventListener('click',ev=>{ev.preventDefault();home();}));
 // Track vertical progress only after a reader scroll gesture, not layout/focus changes.
 addEventListener('wheel',()=>{verticalUserScroll=true;},{passive:true});
 addEventListener('touchmove',()=>{verticalUserScroll=true;},{passive:true});
 addEventListener('keydown',ev=>{if(['PageDown','PageUp','Home','End',' '].includes(ev.key))verticalUserScroll=true;});
 addEventListener('scroll',()=>{if(!verticalUserScroll||navigating||root.dataset.mode!=='vertical'||root.dataset.view!=='reading')return;const top=root.querySelector('.reader-controls').getBoundingClientRect().bottom;let best=current,area=0;cards.forEach((card,i)=>{const rect=card.getBoundingClientRect(),visible=Math.max(0,Math.min(innerHeight,rect.bottom)-Math.max(top,rect.top));if(visible>area){area=visible;best=i;}});if(best!==current)update(best);},{passive:true});
 addEventListener('popstate',route);addEventListener('hashchange',route);
 addEventListener('resize',()=>{if(root.dataset.view==='reading'&&root.dataset.mode==='swipe')go(current);});
 update(0);if(/^#case-\d+$/.test(location.hash))route();
});})();
'''

def render(ep,base,dimensions,preview=False):
    chapters={n['id']:(i+1,n) for i,n in enumerate(ep['news'])}
    cards=[];links=[];seen={};total=len(ep['panels'])+sum(bool(n.get('intro')) for n in ep['news'])
    for i,p in enumerate(ep['panels']):
        nid=p['news_ids'][0];chapter,n=chapters[nid];seen[nid]=seen.get(nid,0)+1;count=sum(nid in q['news_ids'] for q in ep['panels'])
        has_intro=bool(n.get('intro'));story_total=count+int(has_intro)
        if seen[nid]==1:
            index=len(cards)
            chapter_logo='';chapter_brand=''
            if n.get('brand_id') in BRANDS:
                brand_name,brand_file=BRANDS[n['brand_id']]
                wordmark=' wordmark' if n['brand_id']=='mistral' else ''
                chapter_logo=f'<span class="brand-icon{wordmark}"><img src="{e(base+"brands/"+brand_file)}" alt="" width="{72 if wordmark else 24}" height="24"></span>'
                chapter_brand=f'{brand_name} · {n.get("model_label", "")}'
            links.append(f'<a class="chapter-card" href="#case-{index+1}" data-panel="{index}"><span class="chapter-card-top">{chapter_logo}<span class="chapter-number">{chapter:02d}</span></span><span class="chapter-model">{e(chapter_brand)}</span><strong class="chapter-name">{e(n["title"])}</strong><span class="chapter-enter">Lire l’histoire → · {story_total} cases</span></a>')
            if has_intro:
                intro=n['intro'];logo='';name=''
                if n.get('brand_id') in BRANDS:
                    name,filename=BRANDS[n['brand_id']]
                    logo_class=' wordmark' if n['brand_id']=='mistral' else ''
                    logo=f'<div class="intro-logo{logo_class}"><img src="{e(base+"brands/"+filename)}" alt="" width="{160 if logo_class else 72}" height="72"></div>'
                cards.append(f'<article id="case-{index+1}" class="comic-card story-intro" aria-label="Histoire {chapter}, case 1 sur {story_total}, introduction"><p class="panel-label">HISTOIRE {chapter} / {len(chapters)} · CASE 1 / {story_total}</p><div class="intro-body">{logo}<p class="intro-brand">{e(name)} · {e(n.get("model_label", ""))}</p><h3 class="intro-title">{e(intro["title"])}</h3><p class="intro-summary">{e(intro["summary"])}</p><p class="intro-cue">La suite avec Hugo et Iastro →</p></div></article>')
        width,height=dimensions(p['image']);crop=p.get('crop',{'x':0,'y':0,'w':1,'h':1})
        style=f'width:{100/crop["w"]:.8f}%;height:{100/crop["h"]:.8f}%;left:{-100*crop["x"]/crop["w"]:.8f}%;top:{-100*crop["y"]/crop["h"]:.8f}%'
        art=f'<div class="art-window" style="aspect-ratio:{width*crop["w"]}/{height*crop["h"]}"><img src="{e(base+p["image"])}" width="{width}" height="{height}" alt="{e(p["alt"])}" style="{style}" loading="{"eager" if i==0 else "lazy"}"></div>'
        dialogue=''.join(f'<p class="bubble"><strong>{e(d["speaker"])}{e({"fiction":" — scène imaginée","paraphrase":" — reformulation","quote":" — citation"}.get(d.get("attribution"),""))}</strong>{e(d["text"])}</p>' for d in p['dialogue'])
        brand=''
        if n.get('brand_id') in BRANDS:
            name,filename=BRANDS[n['brand_id']]
            logo_class=' wordmark' if n['brand_id']=='mistral' else ''
            brand=f'<p class="brand-label"><span class="brand-icon{logo_class}"><img src="{e(base+"brands/"+filename)}" alt="" width="{72 if logo_class else 24}" height="24"></span><span>{e(name)} · {e(n.get("model_label", ""))}</span></p>'
        cards.append(f'<article id="case-{len(cards)+1}" class="comic-card" aria-label="Histoire {chapter}, case {seen[nid]+int(has_intro)} sur {story_total}"><p class="panel-label">HISTOIRE {chapter} / {len(chapters)} · CASE {seen[nid]+int(has_intro)} / {story_total}</p><h3 class="panel-title">{e(n["title"])}</h3>{brand}{art}<div class="dialogue">{dialogue}</div></article>')
    sources=''.join('<li><strong>'+e(n['title'])+'</strong><br>'+ ' · '.join(f'<a href="{e(s["url"])}">{e(s["publisher"])} — {e(s["published_at"])}</a>' for s in n['sources'])+'</li>' for n in ep['news'])
    start,end=[date.fromisoformat(ep[k]) for k in ('period_start','period_end')]
    month=['','janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.']
    period=f'{start.day}–{end.day} {month[end.month]} {end.year}' if start.month==end.month and start.year==end.year else f'{start:%d/%m/%Y} → {end:%d/%m/%Y}'
    draft='<p class="draft-label">Pilote à valider · non publié</p>' if preview else ''
    return f'''<style>{CSS}</style><div class="comic-reader" data-mode="vertical"><div class="issue-overview">{draft}<p class="issue-meta">HUGO × IASTRO · {e(period)}</p><h2 class="issue-title">{e(ep['title'])}</h2><p class="reader-help">{len(chapters)} histoires · {total} cases · environ 3 minutes. Glisse vers la gauche pour avancer, ou choisis le défilement vertical.</p></div><section id="sommaire" class="chapter-menu" tabindex="-1" aria-labelledby="sommaire-titre"><h3 id="sommaire-titre" class="chapter-heading">Choisis ton histoire</h3><p class="chapter-hint">{len(chapters)} portes d’entrée dans l’atelier. Commence par la news qui te tente.</p><nav class="chapter-links" aria-label="Sommaire des histoires">{''.join(links)}</nav></section><div class="reading-stage"><div class="reader-controls js-only" hidden><p class="story-position"></p><a class="reader-home" href="#sommaire">☷ Sommaire</a><button type="button" data-step="-1" aria-label="Case précédente">←</button><p class="reader-progress" role="status" aria-live="polite">1 / {total}</p><button type="button" data-step="1" aria-label="Case suivante">→</button><button type="button" class="reader-mode" aria-pressed="false" aria-label="Passer en lecture verticale" title="Changer le mode de lecture">↕</button></div><div class="comic-track" role="region" aria-label="Cases du comic, flèches gauche et droite pour naviguer">{''.join(cards)}</div><div class="reading-end"><a href="#sommaire">Choisir une autre histoire →</a></div><p class="fiction-note">Actualités sourcées, scènes et dialogues imaginés. Les machines illustrent les idées ; elles ne représentent pas les produits réels.</p><details class="sources"><summary>Les {len(chapters)} annonces et leurs sources</summary><ol>{sources}</ol><p>Récit de la période {e(ep["period_start"])} au {e(ep["period_end"])}. Préparation : {e(ep["publication_date"])}.</p></details><noscript><p>JavaScript est désactivé : toutes les cases restent lisibles verticalement.</p></noscript></div></div><script>{JS}</script>'''
