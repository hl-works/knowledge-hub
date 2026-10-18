"""Accessible mobile comic: one illustrated panel per swipe, optional vertical reading."""
import html
from datetime import date

def e(v):return html.escape(str(v),quote=True)

BRANDS={
    'openai':('OpenAI','openai.png'),
    'anthropic':('Anthropic','anthropic.png'),
    'mistral':('Mistral','mistral.svg'),
    'google':('Google DeepMind','google.png'),
    'shopify':('Shopify × Meta','shopify.svg'),
    'elevenlabs':('ElevenLabs','elevenlabs.svg'),
    'shop':('Shopify','shopify.svg'),
    'meta':('Meta','meta.png'),
    'perplexity':('Perplexity','perplexity.png'),
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
/* Mobile reading: persistent thumb controls and an explicit story chooser. */
.comic-reader{overflow-anchor:none;scroll-margin-top:0}
.comic-reader [hidden]{display:none!important}
.comic-reader[data-view=menu] .reading-stage,.comic-reader[data-view=complete] .reading-stage{display:none}
.comic-reader[data-view=reading] .issue-overview,.comic-reader[data-view=reading] .chapter-menu,.comic-reader[data-view=complete] .issue-overview,.comic-reader[data-view=complete] .chapter-menu{display:none}
.comic-reader .reader-start{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
.comic-reader .reader-start a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:12px 18px;border:2px solid var(--border-strong);background:var(--text);color:var(--bg);text-decoration:none;font-weight:700;border-radius:8px}
.comic-reader .reader-start [data-resume]{background:var(--surface);color:var(--text)}
.comic-reader .chapter-menu{padding:0;margin:20px 0}
.comic-reader .chapter-links{grid-template-columns:1fr;gap:10px;margin:12px 0}
.comic-reader .chapter-links .chapter-card{display:grid;grid-template-columns:80px minmax(0,1fr);gap:4px 12px;padding:14px;border-radius:10px;box-shadow:2px 2px 0 var(--border-strong)}
.comic-reader .chapter-card-top{grid-row:1/4;display:flex;flex-direction:column;justify-content:center;gap:8px}
.comic-reader .chapter-name{font-size:1.1rem;line-height:1.25}.comic-reader .chapter-model{font-size:.8rem}
.comic-reader .chapter-enter{padding:2px 0 0;font-size:.8rem}.comic-reader .chapter-card[aria-current=step]{border-color:var(--c-red)}
.comic-reader .reader-controls{display:flex;flex-direction:column;align-items:stretch;gap:10px;padding:10px 0;background:var(--bg);border-bottom:1px solid var(--border);top:0}
.comic-reader .reader-toolbar{display:flex;align-items:center;justify-content:space-between;gap:10px}
.comic-reader .reader-home{flex:none;min-height:44px;padding:8px 10px;border:1px solid var(--border-strong);border-radius:8px;font-size:.9rem;text-decoration:none;white-space:nowrap}
.comic-reader .reader-mode{font-size:.85rem;margin:0;padding:8px 10px;min-height:44px}
.comic-reader .story-position{margin:0;font-size:.85rem;line-height:1.3;font-weight:700}
.comic-reader .case-dots{display:flex;gap:5px;height:4px}.comic-reader .case-dots span{flex:1;background:var(--border);border-radius:2px}.comic-reader .case-dots .passed{background:var(--c-red)}
.comic-reader .reader-pager{position:fixed;bottom:0;left:50%;transform:translateX(-50%);z-index:10;width:min(100%,592px);display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1.2fr);align-items:center;gap:10px;padding:12px 16px calc(12px + env(safe-area-inset-bottom));border-top:1px solid var(--border-strong);background:var(--bg);box-shadow:0 -4px 16px #0000000a}
.comic-reader .reader-pager button{font-size:.9rem;font-weight:700;min-height:48px;padding:8px 10px;line-height:1.2}
.comic-reader .reader-pager [data-step="1"]{background:var(--text);color:var(--bg)}
.comic-reader .reader-progress{font-size:.8rem;line-height:1.3;text-align:center;white-space:pre-line;margin:0}
.comic-reader[data-view=reading] .reading-stage{padding-bottom:100px}
.comic-reader .comic-track{scroll-margin-top:120px;overflow-anchor:none;padding:12px 0}
.comic-reader[data-mode=swipe] .comic-track{overflow-y:hidden;scrollbar-width:none;transition:none}
.comic-reader[data-mode=swipe] .comic-track::-webkit-scrollbar{display:none}
.comic-reader .comic-card{scroll-margin-top:120px}
.comic-reader .panel-label{display:none}.comic-reader[data-mode=vertical] .panel-label{display:block}
.comic-reader .panel-title{display:none}.comic-reader .brand-label{padding:10px 12px;font-size:.8rem}
.comic-reader .intro-logo{width:72px;height:72px;padding:12px;margin-bottom:16px}.comic-reader .intro-logo img{width:48px;height:48px}
.comic-reader .intro-logo.wordmark{width:152px}.comic-reader .intro-logo.wordmark img{width:128px;height:48px}
.comic-reader .intro-body{padding:20px}.comic-reader .intro-title{font-size:1.5rem}.comic-reader .intro-summary{line-height:1.45;margin-bottom:16px}
.comic-reader .reader-hint{font-size:.8rem;line-height:1.4;text-align:center;color:var(--text-muted);margin:0 0 16px}
.comic-reader .reading-end{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}.comic-reader .reading-end a{color:var(--text);padding:12px 0;min-height:44px}
.comic-reader .reader-finish{padding:28px 0}.comic-reader .reader-finish h3{font-size:2rem;margin:12px 0}.comic-reader .reader-finish p{font-size:1.1rem;line-height:1.5}
.comic-reader .finish-links{display:flex;gap:12px;flex-direction:column;margin-top:24px}.comic-reader .finish-links a{display:block;padding:14px;border:2px solid var(--border-strong);color:var(--text);border-radius:8px;text-decoration:none;font-weight:700;min-height:48px}
@media(max-width:640px){
 body:has(.comic-reader)>header{padding:12px 16px!important;gap:10px!important;flex-wrap:nowrap!important}
 body:has(.comic-reader)>header .nav__wordmark{font-size:.85rem}
 body:has(.comic-reader)>header nav{gap:10px!important;flex-wrap:nowrap!important}
 body:has(.comic-reader)>header nav>a:not([href$="immersion-ia/"]){display:none}
 body:has(.comic-reader)>header nav>a{font-size:.8rem}
 body:has(.comic-reader)>header [data-theme-toggle]{font-size:0;padding:8px;min-width:44px;min-height:44px}
 body:has(.comic-reader)>header [data-theme-toggle]::after{content:'◐';font-size:20px}
 main:has(.comic-reader){padding-inline:16px}
 body:has(.comic-reader[data-view=reading])>header,body:has(.comic-reader[data-view=reading]) #main>section>p{display:none}
 main:has(.comic-reader[data-view=reading])>section{padding-top:0}
 body:has(.comic-reader) #main>section:has(>.kicker){padding-block:20px!important}
 body:has(.comic-reader) #main>section:has(>.kicker) h1{font-size:2rem!important;max-width:none!important;margin-top:10px!important;text-transform:none}
 body:has(.comic-reader) #main>section:has(>.kicker) .lead{font-size:1rem!important}
 .comic-reader .issue-title{font-size:1.7rem;margin-bottom:12px}.comic-reader .issue-meta{font-size:.8rem;text-transform:none}
 .comic-reader .reader-help{font-size:.9rem;margin:8px 0}.comic-reader .chapter-hint{font-size:.9rem}
 .comic-reader .chapter-heading{font-size:1.2rem}.comic-reader .chapter-menu{margin:18px 0}
 .comic-reader .reader-start a{flex:1;font-size:.9rem}
}
@media print{.comic-reader[data-view] .reading-stage{display:block}.comic-reader .reader-controls,.comic-reader .reader-pager,.comic-reader .reader-start,.comic-reader .reader-finish,.comic-reader .reader-hint,.comic-reader .reading-end,.comic-reader .chapter-menu{display:none!important}.comic-reader[data-mode] .comic-track{height:auto!important;display:block;overflow:visible}.comic-reader .comic-card{visibility:visible!important}.comic-reader .panel-label,.comic-reader .panel-title{display:block}}
'''

JS=r'''
(()=>{document.querySelectorAll('.comic-reader').forEach(root=>{
 const track=root.querySelector('.comic-track'),cards=[...root.querySelectorAll('.comic-card')];
 const chapters=[...root.querySelectorAll('[data-panel]')];
 const status=root.querySelector('.reader-progress'),position=root.querySelector('.story-position'),dots=root.querySelector('.case-dots');
 const previous=root.querySelector('[data-step="-1"]'),next=root.querySelector('[data-step="1"]'),mode=root.querySelector('.reader-mode');
 const finishPanel=root.querySelector('.reader-finish'),resume=root.querySelector('[data-resume]'),hint=root.querySelector('.reader-hint');
 let current=0,chapter=-1,navigating=false,token=0,scrollTimer=0,verticalFrame=0,verticalUserScroll=false,started=false,lastWidth=0;
 const fit=()=>{track.style.height=root.dataset.mode==='swipe'?`${cards[current].offsetHeight+24}px`:'';};
 const cardObserver=new ResizeObserver(fit);
 const startAt=c=>Number(chapters[c].dataset.panel);
 const endAt=c=>c+1<chapters.length?startAt(c+1):cards.length;
 function update(i){
  current=Math.max(0,Math.min(cards.length-1,i));
  const selected=chapters.findLastIndex(link=>Number(link.dataset.panel)<=current);
  if(selected!==chapter){chapter=selected;dots.replaceChildren(...Array.from({length:endAt(chapter)-startAt(chapter)},()=>document.createElement('span')));}
  const local=current-startAt(chapter)+1,total=endAt(chapter)-startAt(chapter);
  status.textContent=`Case ${local}\nsur ${total}`;
  position.textContent=`Histoire ${chapter+1} / ${chapters.length} · ${chapters[chapter].querySelector('.chapter-model').textContent}`;
  [...dots.children].forEach((dot,j)=>dot.classList.toggle('passed',j<local));
  previous.disabled=current===0;
  next.textContent=current===cards.length-1?'Terminer ✓':current===endAt(chapter)-1?'Info suivante →':'Suivant →';
  next.setAttribute('aria-label',current===cards.length-1?'Terminer le numéro':current===endAt(chapter)-1?'Histoire suivante':'Case suivante');
  cards.forEach((card,j)=>{card.classList.toggle('is-current',j===current);card.inert=root.dataset.mode==='swipe'&&j!==current;});
  chapters.forEach((link,j)=>{if(started&&j===chapter)link.setAttribute('aria-current','step');else link.removeAttribute('aria-current');});
  resume.hidden=!started;resume.setAttribute('href','#'+cards[current].id);resume.textContent=`Reprendre · histoire ${chapter+1}`;
  cardObserver.disconnect();cardObserver.observe(cards[current]);fit();
 }
 function setHash(value,push=false){if(location.hash!==value)history[push?'pushState':'replaceState'](null,'',value);}
 function show(view){root.dataset.view=view;finishPanel.hidden=view!=='complete';}
 function align(){track.scrollTo({left:cards[current].offsetLeft-cards[0].offsetLeft,behavior:'instant'});}
 function go(i,{push=false,focus=false}={}){
  if(i>=cards.length){complete(push);return;}
  const run=++token;navigating=true;started=true;verticalUserScroll=false;clearTimeout(scrollTimer);cancelAnimationFrame(verticalFrame);
  show('reading');track.style.scrollSnapType='none';update(i);
  if(root.dataset.mode==='swipe'){align();root.scrollIntoView({block:'start',behavior:'instant'});}
  else cards[current].scrollIntoView({block:'start',behavior:'instant'});
  setHash('#'+cards[current].id,push);
  if(focus)(root.dataset.mode==='swipe'?track:cards[current]).focus({preventScroll:true});
  requestAnimationFrame(()=>{if(run!==token)return;if(root.dataset.mode==='swipe')align();requestAnimationFrame(()=>{if(run===token){track.style.scrollSnapType='';navigating=false;}});});
 }
 function home(push=true,focus=true){++token;navigating=false;clearTimeout(scrollTimer);show('menu');setHash('#sommaire',push);root.scrollIntoView({block:'start',behavior:'instant'});if(focus)chapters[Math.max(0,chapter)].focus({preventScroll:true});}
 function complete(push=false){++token;clearTimeout(scrollTimer);show('complete');setHash('#fin',push);root.scrollIntoView({block:'start',behavior:'instant'});finishPanel.focus({preventScroll:true});}
 function route(){const i=cards.findIndex(card=>'#'+card.id===location.hash);if(i>=0)go(i);else if(location.hash==='#fin')complete();else home(false,false);}
 root.querySelectorAll('.js-only').forEach(x=>x.hidden=false);root.dataset.mode='swipe';show('menu');track.tabIndex=0;cards.forEach(card=>card.tabIndex=-1);
 previous.addEventListener('click',()=>go(current-1));next.addEventListener('click',()=>go(current+1));
 root.querySelector('[data-start]').addEventListener('click',ev=>{ev.preventDefault();go(0,{push:true,focus:true});});
 resume.addEventListener('click',ev=>{ev.preventDefault();go(current,{push:true,focus:true});});
 track.addEventListener('keydown',ev=>{if(ev.target!==track)return;if(ev.key==='ArrowRight'){ev.preventDefault();go(current+1);}else if(ev.key==='ArrowLeft'){ev.preventDefault();go(current-1);}else if(ev.key==='Escape'){ev.preventDefault();home();}});
 // Wait for a swipe to settle before resizing the track or changing its active card.
 track.addEventListener('scroll',()=>{if(navigating||root.dataset.mode!=='swipe'||root.dataset.view!=='reading')return;clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{
  if(navigating||root.dataset.mode!=='swipe'||root.dataset.view!=='reading')return;
  const first=cards[0].offsetLeft;let nearest=current,distance=Infinity;
  cards.forEach((card,i)=>{const d=Math.abs(card.offsetLeft-first-track.scrollLeft);if(d<distance){distance=d;nearest=i;}});
  if(nearest!==current){started=true;update(nearest);setHash('#'+cards[current].id);}
 },120);},{passive:true});
 mode.addEventListener('click',()=>{const keep=current,vertical=root.dataset.mode==='swipe';root.dataset.mode=vertical?'vertical':'swipe';mode.textContent=vertical?'Case par case ↔':'Défilement ↓';mode.setAttribute('aria-pressed',String(vertical));mode.setAttribute('aria-label',vertical?'Passer en lecture case par case':'Passer en défilement vertical');hint.textContent=vertical?'Fais défiler pour lire. Les boutons restent disponibles.':'Glisse vers la gauche ou touche « Suivant ».';go(keep);});
 chapters.forEach(link=>link.addEventListener('click',ev=>{ev.preventDefault();go(Number(link.dataset.panel),{push:true,focus:true});}));
 root.querySelectorAll('[href="#sommaire"]').forEach(link=>link.addEventListener('click',ev=>{ev.preventDefault();home();}));
 const userScroll=()=>{verticalUserScroll=true;};
 addEventListener('wheel',userScroll,{passive:true});addEventListener('touchmove',userScroll,{passive:true});
 addEventListener('keydown',ev=>{if(['PageDown','PageUp','Home','End',' '].includes(ev.key))verticalUserScroll=true;});
 addEventListener('scroll',()=>{
  if(!verticalUserScroll||navigating||root.dataset.mode!=='vertical'||root.dataset.view!=='reading')return;
  cancelAnimationFrame(verticalFrame);verticalFrame=requestAnimationFrame(()=>{
   if(navigating||root.dataset.view!=='reading'||root.dataset.mode!=='vertical')return;
   const top=root.querySelector('.reader-controls').getBoundingClientRect().bottom,bottom=root.querySelector('.reader-pager').getBoundingClientRect().top;
   let best=current,area=0;
   cards.forEach((card,i)=>{const r=card.getBoundingClientRect(),visible=Math.max(0,Math.min(bottom,r.bottom)-Math.max(top,r.top));if(visible>area){area=visible;best=i;}});
   if(best!==current){update(best);setHash('#'+cards[current].id);}
  });
 },{passive:true});
 addEventListener('popstate',route);addEventListener('hashchange',route);
 // Mobile browser chrome changes height while scrolling: never jump back to the top.
 new ResizeObserver(()=>{const width=track.clientWidth;if(width&&width!==lastWidth){lastWidth=width;if(root.dataset.view==='reading'&&root.dataset.mode==='swipe'){align();fit();}}}).observe(track);
 update(0);if(/^#case-\d+$/.test(location.hash)||location.hash==='#fin')route();
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
                cards.append(f'<article id="case-{index+1}" class="comic-card story-intro" aria-label="Histoire {chapter}, case 1 sur {story_total}, introduction"><p class="panel-label">HISTOIRE {chapter} / {len(chapters)} · CASE 1 / {story_total}</p><div class="intro-body">{logo}<p class="intro-brand">{e(name)} · {e(n.get("model_label", ""))}</p><h3 class="intro-title">{e(intro["title"])}</h3><p class="intro-summary">{e(intro["summary"])}</p><p class="intro-cue">La suite avec Hugo et iAstro →</p></div></article>')
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
    return f'''<style>{CSS}</style><div class="comic-reader" data-mode="vertical"><div class="issue-overview">{draft}<p class="issue-meta">Hugo × iAstro · {e(period)}</p><h2 class="issue-title">{e(ep['title'])}</h2><p class="reader-help">{len(chapters)} histoires · {total} cases · environ 3 minutes. </p><div class="reader-start js-only" hidden><a href="#case-1" data-start>Commencer la lecture →</a><a href="#case-1" data-resume hidden>Reprendre</a></div></div><section id="sommaire" class="chapter-menu" tabindex="-1" aria-labelledby="sommaire-titre"><h3 id="sommaire-titre" class="chapter-heading">Choisis ton histoire</h3><p class="chapter-hint">Ou passe directement à la news qui t’intéresse.</p><nav class="chapter-links" aria-label="Sommaire des histoires">{''.join(links)}</nav></section><div class="reading-stage"><div class="reader-controls js-only" hidden><div class="reader-toolbar"><a class="reader-home" href="#sommaire">← Sommaire</a><button type="button" class="reader-mode" aria-pressed="false" aria-label="Passer en défilement vertical">Défilement ↓</button></div><p class="story-position"></p><div class="case-dots" aria-hidden="true"></div></div><div class="reader-pager js-only" hidden aria-label="Navigation entre les cases"><button type="button" data-step="-1" aria-label="Case précédente">← Retour</button><p class="reader-progress" role="status" aria-live="polite" aria-atomic="true">Case 1 sur {total}</p><button type="button" data-step="1" aria-label="Case suivante">Suivant →</button></div><div class="comic-track" role="region" aria-label="Cases du comic, flèches gauche et droite pour naviguer">{''.join(cards)}</div><p class="reader-hint js-only" hidden>Glisse vers la gauche ou touche « Suivant ».</p><div class="reading-end"><a href="#sommaire">Choisir une autre histoire →</a></div><p class="fiction-note">Actualités sourcées, scènes et dialogues imaginés. Les machines illustrent les idées ; elles ne représentent pas les produits réels.</p><details class="sources"><summary>Les {len(chapters)} annonces et leurs sources</summary><ol>{sources}</ol><p>Récit de la période {e(ep["period_start"])} au {e(ep["period_end"])}. Préparation : {e(ep["publication_date"])}.</p></details><noscript><p>JavaScript est désactivé : toutes les cases restent lisibles verticalement.</p></noscript></div><section class="reader-finish" hidden tabindex="-1"><p class="issue-meta">iAstro Sunday · {e(period)}</p><h3>À dimanche prochain !</h3><p>Tu es arrivé au bout du numéro. Retrouve les autres histoires ou continue ta veille dans Le Kiosque IA.</p><div class="finish-links"><a href="#sommaire">Revenir au sommaire</a><a href="/knowledge-hub/immersion-ia/">Ouvrir Le Kiosque IA →</a></div></section></div><script>{JS}</script>'''
