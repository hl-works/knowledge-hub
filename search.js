/* Recherche globale du Knowledge Hub — overlay accessible, zéro dépendance.
   Charge search-index.json (toutes pages + entrées), filtre en live. */
(function(){
  // Base du site (gère le sous-dossier /knowledge-hub/ et l'exécution locale)
  var BASE = (location.pathname.indexOf('/knowledge-hub/')===0) ? '/knowledge-hub' : '';
  var overlay, input, results, empty, idx=null, items=[], active=-1;

  function build(){
    overlay=document.createElement('div');
    overlay.className='site-search'; overlay.setAttribute('role','dialog');
    overlay.setAttribute('aria-modal','true'); overlay.setAttribute('aria-label','Rechercher dans le site');
    overlay.innerHTML=
      '<div class="site-search__panel">'+
        '<div class="site-search__bar">'+
          '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>'+
          '<input type="search" id="ss-input" placeholder="Rechercher un guide, une session, un sujet…" aria-label="Rechercher" autocomplete="off">'+
          '<kbd>Échap</kbd>'+
        '</div>'+
        '<ul class="site-search__results" id="ss-results"></ul>'+
        '<p class="site-search__empty" id="ss-empty" hidden>Tapez pour rechercher dans tout le site.</p>'+
      '</div>';
    document.body.appendChild(overlay);
    input=overlay.querySelector('#ss-input');
    results=overlay.querySelector('#ss-results');
    empty=overlay.querySelector('#ss-empty');
    overlay.addEventListener('click', function(e){ if(e.target===overlay) close(); });
    input.addEventListener('input', function(){ render(input.value); });
    input.addEventListener('keydown', onKey);
  }

  function loadIndex(){
    if(idx) return Promise.resolve(idx);
    return fetch(BASE+'/search-index.json',{cache:'no-store'})
      .then(function(r){ return r.json(); })
      .then(function(d){ idx=d; return d; })
      .catch(function(){ idx=[]; return []; });
  }

  function esc(s){ return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function hl(text,q){
    if(!q) return esc(text);
    try{ var re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
      return esc(text).replace(re,'<mark>$1</mark>'); }catch(e){ return esc(text); }
  }

  function render(q){
    q=(q||'').trim();
    results.innerHTML=''; active=-1;
    if(!q){ empty.hidden=false; empty.textContent='Tapez pour rechercher dans tout le site.'; return; }
    var needle=q.toLowerCase();
    var matched=idx.filter(function(it){
      return (it.title+' '+it.excerpt+' '+(it.tags||'')+' '+it.kind).toLowerCase().indexOf(needle)>-1;
    }).slice(0,12);
    if(!matched.length){ empty.hidden=false; empty.textContent='Aucun résultat pour « '+q+' ».'; return; }
    empty.hidden=true;
    matched.forEach(function(it){
      var li=document.createElement('li');
      li.innerHTML='<a href="'+it.url+'">'+
        '<span class="r-kicker">'+esc(it.kind)+'</span>'+
        '<div class="r-title">'+hl(it.title,q)+'</div>'+
        '<div class="r-excerpt">'+hl(it.excerpt,q)+'</div></a>';
      results.appendChild(li);
    });
  }

  function onKey(e){
    var links=[].slice.call(results.querySelectorAll('a'));
    if(e.key==='Escape'){ close(); }
    else if(e.key==='ArrowDown'){ e.preventDefault(); active=Math.min(active+1,links.length-1); focusActive(links); }
    else if(e.key==='ArrowUp'){ e.preventDefault(); active=Math.max(active-1,0); focusActive(links); }
    else if(e.key==='Enter' && active>-1 && links[active]){ links[active].click(); }
  }
  function focusActive(links){ links.forEach(function(a,i){ a.classList.toggle('is-active',i===active); }); if(links[active]) links[active].scrollIntoView({block:'nearest'}); }

  function open(){
    loadIndex().then(function(){
      overlay.classList.add('is-open');
      document.body.style.overflow='hidden';
      input.value=''; render(''); input.focus();
    });
  }
  function close(){ overlay.classList.remove('is-open'); document.body.style.overflow=''; }

  document.addEventListener('DOMContentLoaded', function(){
    build();
    // boutons loupe
    [].slice.call(document.querySelectorAll('[data-search-open]')).forEach(function(btn){
      btn.addEventListener('click', open);
    });
    // raccourci clavier "/"
    document.addEventListener('keydown', function(e){
      if(e.key==='/' && !/input|textarea|select/i.test((e.target.tagName||''))){ e.preventDefault(); open(); }
    });
    // burger menu
    var nav=document.querySelector('.nav');
    var burger=document.querySelector('.nav__burger');
    if(burger && nav){
      burger.addEventListener('click', function(){
        var openNow=nav.getAttribute('data-open')==='true';
        nav.setAttribute('data-open', openNow?'false':'true');
        burger.setAttribute('aria-expanded', openNow?'false':'true');
      });
      // referme au clic sur un lien
      nav.querySelectorAll('.nav__links a').forEach(function(a){
        a.addEventListener('click', function(){ nav.setAttribute('data-open','false'); burger.setAttribute('aria-expanded','false'); });
      });
    }
  });
})();
