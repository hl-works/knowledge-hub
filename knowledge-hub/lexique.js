/* Lexique — infobulles site-wide. Zéro dépendance.
   - Charge glossaire.json (source unique partagée avec la page /lexique/).
   - Lie la 1re occurrence par page de chaque terme "dur" (via aliases).
   - Desktop : hover. Mobile : tap → popover + lien "voir dans le lexique".
   - Ne touche pas : nav, footer, code, liens, titres, la page /lexique/ elle-même. */
(function(){
  if (location.pathname.indexOf('/lexique/')>-1) return; // pas d'auto-lien sur la page lexique
  var BASE = (location.pathname.indexOf('/knowledge-hub/')===0) ? '/knowledge-hub' : '';
  // Bilingue : version anglaise (/en/) -> glossaire EN + page lexique EN
  var EN = /(^|\/)en\//.test(location.pathname);
  var LEXPATH = BASE + (EN ? '/en/lexique/' : '/lexique/');
  var GLOSS = BASE + (EN ? '/en/lexique/glossaire.en.json' : '/lexique/glossaire.json');

  function norm(s){ return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase(); }

  fetch(GLOSS,{cache:'force-cache'})
    .then(function(r){return r.json();})
    .then(function(terms){ init(terms); })
    .catch(function(){});

  function init(terms){
    // map alias normalisé -> terme (alias les plus longs d'abord pour matcher "grand modèle de langage" avant "modèle")
    var entries=[];
    terms.forEach(function(t){
      (t.aliases&&t.aliases.length?t.aliases:[t.terme]).forEach(function(a){
        entries.push({alias:a, na:norm(a), term:t});
      });
    });
    entries.sort(function(a,b){ return b.na.length-a.na.length; });
    var done={};               // id de terme déjà lié sur cette page
    var scope=document.querySelector('main')||document.body;

    // parcours des nœuds texte, hors zones interdites
    var SKIP=/^(A|BUTTON|CODE|PRE|H1|H2|H3|SCRIPT|STYLE|NAV)$/;
    function walk(node){
      for(var i=0;i<node.childNodes.length;i++){
        var c=node.childNodes[i];
        if(c.nodeType===1){
          if(SKIP.test(c.tagName)) continue;
          if(c.classList && (c.classList.contains('lex-term')||c.classList.contains('nav')||c.classList.contains('footer'))) continue;
          walk(c);
        } else if(c.nodeType===3 && c.nodeValue.trim().length>2){
          tryLink(c);
        }
      }
    }
    function tryLink(textNode){
      var txt=textNode.nodeValue, ntxt=norm(txt);
      for(var k=0;k<entries.length;k++){
        var e=entries[k];
        if(done[e.term.id]) continue;
        var idx=findWord(ntxt, e.na);
        if(idx<0) continue;
        // découpe le nœud : avant | match | après
        var before=txt.slice(0,idx), match=txt.slice(idx, idx+e.alias.length), after=txt.slice(idx+e.alias.length);
        var span=document.createElement('a');
        span.className='lex-term';
        span.setAttribute('href', LEXPATH+'#lex-'+e.term.id);
        span.setAttribute('data-term', e.term.id);
        span.setAttribute('data-def', e.term.definition);
        span.textContent=match;
        var frag=document.createDocumentFragment();
        if(before) frag.appendChild(document.createTextNode(before));
        frag.appendChild(span);
        if(after) frag.appendChild(document.createTextNode(after));
        textNode.parentNode.replaceChild(frag, textNode);
        done[e.term.id]=1;
        return; // un seul lien par nœud
      }
    }
    // match sur frontière de mot (évite "api" dans "rapide")
    function findWord(hay, needle){
      var from=0, idx;
      while((idx=hay.indexOf(needle, from))>-1){
        var b=hay[idx-1], a=hay[idx+needle.length];
        var bOk=(idx===0)||/[^a-z0-9]/.test(b);
        var aOk=(idx+needle.length>=hay.length)||/[^a-z0-9]/.test(a);
        if(bOk&&aOk) return idx;
        from=idx+1;
      }
      return -1;
    }
    walk(scope);

    // ---- popover ----
    var pop=document.createElement('div'); pop.className='lex-pop'; document.body.appendChild(pop);
    var isTouch=window.matchMedia('(hover: none)').matches;
    var current=null, hideTimer=null;
    function mdBold(s){ return (s||'').replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>'); }
    function show(el){
      clearTimeout(hideTimer);
      var id=el.getAttribute('data-term'), def=el.getAttribute('data-def');
      pop.innerHTML='<b>'+el.textContent+'</b> — '+mdBold(def)+'<br><a href="'+LEXPATH+'#lex-'+id+'">'+(EN?'see in the glossary →':'voir dans le lexique →')+'</a>';
      var r=el.getBoundingClientRect();
      pop.style.left=Math.max(8, Math.min(window.innerWidth-308, r.left+window.scrollX))+'px';
      pop.style.top=(r.bottom+window.scrollY+6)+'px';
      pop.classList.add('is-open'); current=el;
    }
    function hide(){ pop.classList.remove('is-open'); current=null; }
    function scheduleHide(){ clearTimeout(hideTimer); hideTimer=setTimeout(hide, 180); }

    document.querySelectorAll('.lex-term[data-term]').forEach(function(el){
      if(isTouch){
        // 1er tap : aperçu de la définition ; le lien du popover navigue.
        el.addEventListener('click', function(ev){ ev.preventDefault(); (current===el)?hide():show(el); });
      } else {
        // hover = aperçu ; clic sur le mot = navigation (comportement par défaut du lien).
        el.addEventListener('mouseenter', function(){ show(el); });
        el.addEventListener('mouseleave', scheduleHide);
        el.addEventListener('focus', function(){ show(el); });
        el.addEventListener('blur', scheduleHide);
      }
    });
    // pont de survol : garder le popover ouvert quand la souris passe dessus
    if(!isTouch){
      pop.addEventListener('mouseenter', function(){ clearTimeout(hideTimer); });
      pop.addEventListener('mouseleave', scheduleHide);
    }
    if(isTouch){ document.addEventListener('click', function(ev){ if(current && !ev.target.closest('.lex-term') && !ev.target.closest('.lex-pop')) hide(); }); }
    window.addEventListener('scroll', function(){ if(current && !isTouch) hide(); }, {passive:true});
  }
})();
