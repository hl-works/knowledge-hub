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
.comic-reader .chapter-menu{margin:12px 0}.comic-reader .chapter-menu summary{min-height:44px;padding:10px 0;cursor:pointer}
.comic-reader .chapter-links{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}
.comic-reader button,.comic-reader .chapter-links a{border:1px solid var(--border-strong);background:var(--surface);color:var(--text);padding:10px 14px;min-height:44px;font:inherit;cursor:pointer;text-decoration:none;border-radius:8px}
.comic-reader button:disabled{opacity:.45;cursor:default}.comic-reader :focus-visible{outline:3px solid var(--c-red);outline-offset:3px}
.comic-reader .reader-controls{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:8px;padding:10px 0;background:var(--bg);border-bottom:1px solid var(--border)}
.comic-reader .reader-progress{margin:0 auto;font-size:.9rem;font-variant-numeric:tabular-nums}.comic-reader .reader-mode{margin-left:auto;font-size:.85rem}
.comic-reader .comic-track{scroll-margin-top:65px;display:block;outline-offset:3px;padding:12px 0}
.comic-reader .comic-card{width:100%;min-width:0;margin-bottom:40px;scroll-margin-top:90px;border:1px solid var(--border-strong);background:var(--surface);border-radius:12px;overflow:hidden}
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

JS='''
(()=>{document.querySelectorAll('.comic-reader').forEach(root=>{
 const track=root.querySelector('.comic-track'),cards=[...root.querySelectorAll('.comic-card')],status=root.querySelector('.reader-progress');
 const previous=root.querySelector('[data-step="-1"]'),next=root.querySelector('[data-step="1"]'),mode=root.querySelector('.reader-mode');
 let current=0,frame=0;
 function update(i){current=Math.max(0,Math.min(cards.length-1,i));status.textContent=`${current+1} / ${cards.length}`;previous.disabled=current===0;next.disabled=current===cards.length-1;cards.forEach((c,j)=>c.classList.toggle('is-current',j===current));}
 function go(i){i=Math.max(0,Math.min(cards.length-1,i));update(i);const behavior='instant';if(root.dataset.mode==='swipe'){track.scrollTo({left:cards[i].offsetLeft-cards[0].offsetLeft,behavior});}else{cards[i].scrollIntoView({behavior,block:'start'});}}
 root.querySelectorAll('.js-only').forEach(x=>x.hidden=false);root.dataset.mode='swipe';track.tabIndex=0;
 previous.addEventListener('click',()=>go(current-1));next.addEventListener('click',()=>go(current+1));
 track.addEventListener('keydown',ev=>{if(ev.target!==track)return;if(ev.key==='ArrowRight'){ev.preventDefault();go(current+1);}if(ev.key==='ArrowLeft'){ev.preventDefault();go(current-1);}});
 track.addEventListener('scroll',()=>{if(root.dataset.mode!=='swipe')return;cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{const first=cards[0].offsetLeft;let nearest=0,distance=Infinity;cards.forEach((c,i)=>{const d=Math.abs(c.offsetLeft-first-track.scrollLeft);if(d<distance){distance=d;nearest=i;}});update(nearest);});},{passive:true});
 mode.addEventListener('click',()=>{const keep=current,vertical=root.dataset.mode==='swipe';root.dataset.mode=vertical?'vertical':'swipe';mode.textContent=vertical?'Swipe':'Vertical';mode.setAttribute('aria-pressed',String(vertical));requestAnimationFrame(()=>go(keep));});
 root.querySelectorAll('[data-panel]').forEach(link=>link.addEventListener('click',ev=>{ev.preventDefault();root.querySelector('.chapter-menu').open=false;go(Number(link.dataset.panel));track.scrollIntoView({block:'start'});}));
 const observer=new IntersectionObserver(entries=>{if(root.dataset.mode==='swipe')return;const best=entries.filter(x=>x.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];if(best)update(cards.indexOf(best.target));},{threshold:[.3,.6]});cards.forEach(c=>observer.observe(c));update(0);
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
            links.append(f'<a href="#case-{index+1}" data-panel="{index}">{chapter}. {e(n["title"])}</a>')
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
    return f'''<style>{CSS}</style><div class="comic-reader" data-mode="vertical">{draft}<p class="issue-meta">HUGO × IASTRO · {e(period)}</p><h2 class="issue-title">{e(ep['title'])}</h2><p class="reader-help">{len(chapters)} histoires · {total} cases · environ 3 minutes. Glisse vers la gauche pour avancer, ou choisis le défilement vertical.</p><details class="chapter-menu"><summary>Choisir une histoire</summary><nav class="chapter-links" aria-label="Choisir une histoire">{''.join(links)}</nav></details><div class="reader-controls js-only" hidden><button type="button" data-step="-1" aria-label="Case précédente">←</button><p class="reader-progress" role="status" aria-live="polite">1 / {total}</p><button type="button" data-step="1" aria-label="Case suivante">→</button><button type="button" class="reader-mode" aria-pressed="false" aria-label="Changer entre lecture verticale et swipe">Vertical</button></div><div class="comic-track" role="region" aria-label="Cases du comic, flèches gauche et droite pour naviguer">{''.join(cards)}</div><p class="fiction-note">Actualités sourcées, scènes et dialogues imaginés. Les machines illustrent les idées ; elles ne représentent pas les produits réels.</p><details class="sources"><summary>Les {len(chapters)} annonces et leurs sources</summary><ol>{sources}</ol><p>Récit de la période {e(ep["period_start"])} au {e(ep["period_end"])}. Préparation : {e(ep["publication_date"])}.</p></details><noscript><p>JavaScript est désactivé : toutes les cases restent lisibles verticalement.</p></noscript></div><script>{JS}</script>'''
