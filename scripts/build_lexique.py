#!/usr/bin/env python3
"""Render the bilingual glossary from its JSON sources, including no-JS content."""
from pathlib import Path
import html
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1] / 'knowledge-hub'
CATEGORIES = {
    'bases': ('Les bases', 'Foundations'),
    'acteurs': ('Entreprises et plateformes', 'Companies and platforms'),
    'outils': ('Applications et assistants', 'Apps and assistants'),
    'modeles': ('Modèles', 'Models'),
    'agents': ('Agents et automatisation', 'Agents and automation'),
    'creation': ('Image, voix et design', 'Images, voice and design'),
    'donnees': ('Données et recherche', 'Data and search'),
    'qualite': ('Qualité et vérification', 'Quality and verification'),
    'developpement': ('Développement', 'Development'),
}
CSS = '''
.lex-hero h1{font-size:clamp(2.2rem,4vw,3.4rem);text-transform:none}.lex-intro{max-width:850px}.lex-orientation{margin:24px 0;border-block:1px solid var(--border);padding:16px 0}.lex-orientation summary{cursor:pointer;font-weight:700;font-size:.9rem}.lex-orientation summary:focus-visible{outline:3px solid var(--c-red);outline-offset:4px}.lex-map{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:28px 0}.lex-map article{background:var(--surface);border:1px solid var(--border);padding:20px;min-width:0}.lex-map small{font:11px var(--font-mono);color:var(--c-red)}.lex-map h2{font-size:1.1rem;text-transform:none;margin:12px 0 8px}.lex-map p{font-size:.85rem;line-height:1.5;margin:0}.lex-map a{display:block;margin-top:10px;font-size:.8rem}.lex-controls{display:grid;grid-template-columns:2fr 1fr;gap:16px;align-items:end;margin-top:30px}.lex-controls label{display:block;font-size:.8rem;font-weight:700;margin-bottom:8px}.lex-controls .lex-search{margin:0;max-width:none}.lex-controls select{width:100%;min-height:48px;padding:12px;background:var(--bg);color:var(--text);border:1px solid var(--border);font:inherit;font-size:.9rem}.lex-controls button{font:inherit;background:var(--surface);color:var(--text);border:1px solid var(--border);padding:10px 14px;cursor:pointer}.lex-status{display:flex;gap:20px;justify-content:space-between;align-items:center;margin:16px 0}.lex-status p{margin:0}.lex-entry[hidden]{display:none}.lex-entry{scroll-margin-top:110px}.lex-entry h2{text-transform:none;overflow-wrap:anywhere}.lex-entry__category{font:11px var(--font-mono);color:var(--text-muted);margin:0 0 8px}.lex-entry__source{font-size:.75rem;line-height:1.6;margin-top:12px;color:var(--text-muted);overflow-wrap:anywhere}.lex-entry__source a{color:inherit}.lex-entry:target{outline:2px solid var(--c-red);outline-offset:8px}.lex-az{flex-wrap:wrap}.lex-topics{font-size:.85rem;line-height:1.8}.lex-topics a{white-space:nowrap}.lex-controls input:focus-visible,.lex-controls select:focus-visible,.lex-controls button:focus-visible{outline:3px solid var(--c-red);outline-offset:3px}
@media(min-width:761px) and (max-width:1100px){.nav{flex-wrap:wrap;gap:12px}.nav>nav{width:100%}.nav__links{justify-content:space-between;gap:12px}}
@media(max-width:760px){.lex-map{grid-template-columns:1fr 1fr;gap:10px}.lex-map article{padding:16px}.lex-controls{grid-template-columns:1fr}.lex-status{align-items:flex-start}.lex-entry{scroll-margin-top:140px}}
'''
JS = r'''
(function(){
  var q=document.getElementById('lex-q'), category=document.getElementById('lex-category');
  var entries=Array.from(document.querySelectorAll('#lex-list > .lex-entry'));
  var az=document.getElementById('lex-az'), count=document.getElementById('lex-count');
  var en=document.documentElement.lang==='en';
  function norm(s){return s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();}
  function render(){
    var words=norm(q.value).trim().split(/\s+/).filter(Boolean), letters={}, shown=0;
    az.replaceChildren();
    entries.forEach(function(el){
      var visible=(!category.value||el.dataset.category===category.value)&&words.every(function(w){return el.dataset.search.indexOf(w)>-1;});
      el.hidden=!visible;
      if(!visible)return;
      shown++;
      var letter=el.dataset.letter;
      if(!letters[letter]){letters[letter]=true;var a=document.createElement('a');a.href='#'+el.id;a.textContent=letter;az.appendChild(a);}
    });
    count.textContent=shown+' / '+entries.length+(en?' terms':' termes');
    document.getElementById('lex-empty').hidden=shown!==0;
  }
  function revealHash(){
    var id;try{id=decodeURIComponent(location.hash.slice(1));}catch(e){return;}
    var target=document.getElementById(id);
    if(!target||!target.classList.contains('lex-entry'))return;
    if(target.hidden){q.value='';category.value='';render();}
    target.scrollIntoView({block:'start'});
  }
  q.addEventListener('input',render);category.addEventListener('change',render);
  document.getElementById('lex-reset').addEventListener('click',function(){q.value='';category.value='';render();q.focus();});
  window.addEventListener('hashchange',revealHash);
  render();if(location.hash)revealHash();
})();
'''

def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value) if not unicodedata.combining(c)).lower()

def bold(value):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html.escape(value))

def build():
    for en in (False, True):
        directory=ROOT/('en/' if en else '')/'lexique'
        terms=json.loads((directory/('glossaire.en.json' if en else 'glossaire.json')).read_text())
        assert len({t['id'] for t in terms})==len(terms), 'Duplicate glossary ID'
        assert all(t['category'] in CATEGORIES for t in terms), 'Unknown category'
        terms.sort(key=lambda t:norm(t['terme']))
        tr=lambda fr,eng:eng if en else fr
        esc=html.escape
        prefix='/knowledge-hub/'+('en/' if en else '')
        url='https://hl-consulting.tech'+prefix+'lexique/'
        rows=[]; az=[]; letters=set()
        for t in terms:
            letter=norm(t['terme'])[0].upper()
            if letter not in letters:
                letters.add(letter);az.append(f'<a href="#lex-{t["id"]}">{letter}</a>')
            links=[]
            for field,label in [('guides',tr('Guides','Guides')),('projets',tr('Projets','Projects'))]:
                parts=[f'<a href="{esc(x["url"])}">{esc(x["label"])}</a>' if x.get('url') else esc(x['label']) for x in t.get(field,[])]
                if parts:links.append(f'<span class="lk"><b>{label}</b>'+ ' · '.join(parts)+'</span>')
            sources=' · '.join(f'<a href="{esc(s["url"])}">{esc(s["label"])}</a>' for s in t.get('sources',[]))
            source_html=f'<p class="lex-entry__source">{tr("Sources","Sources")} : {sources} · {tr("Vérifié le","Checked")} <time datetime="{t.get("verified","")}">{t.get("verified","")}</time></p>' if sources else ''
            hay=norm(' '.join([t['terme'],*t.get('aliases',[]),t['definition']]))
            rows.append(f'<li class="lex-entry" id="lex-{t["id"]}" data-category="{t["category"]}" data-letter="{letter}" data-search="{esc(hay)}"><p class="lex-entry__category">{CATEGORIES[t["category"]][int(en)]}</p><h2>{esc(t["terme"])}</h2><p class="lex-entry__def">{bold(t["definition"])}</p><div class="lex-entry__links">{"".join(links)}</div>{source_html}</li>')
        options=''.join(f'<option value="{k}">{v[int(en)]}</option>' for k,v in CATEGORIES.items())
        cards=[('01',tr('L’entreprise','The company'),tr('Qui développe les outils et modèles.','Who develops tools and models.'),'OpenAI / Anthropic','openai'),('02',tr('L’application','The app'),tr('L’espace dans lequel tu travailles.','The workspace you use.'),'ChatGPT / Claude','chatgpt'),('03',tr('L’agent de travail','The work agent'),tr('Les outils pour agir sur un projet.','Tools for acting on a project.'),'Codex / Claude Code','codex'),('04',tr('Le modèle','The model'),tr('Le moteur choisi pour une tâche.','The engine selected for a task.'),'Astra / Opus / Gemini','gpt-6-astra')]
        cardhtml=''.join(f'<article><small>{n}</small><h2>{label}</h2><p>{desc}</p><a href="#lex-{ident}">{names} →</a></article>' for n,label,desc,names,ident in cards)
        title=tr('Lexique IA : outils, modèles et concepts · Knowledge Hub','AI glossary: tools, models and concepts · Knowledge Hub')
        description=tr(f'{len(terms)} définitions : OpenAI, ChatGPT, Codex, Astra, Claude Design, Gemini, agents, RAG, voix et design. Recherche, catégories et sources officielles.',f'{len(terms)} definitions: OpenAI, ChatGPT, Codex, Astra, Claude Design, Gemini, agents, RAG, voice and design. Search, categories and official sources.')
        main=f'''<main id="main"><section class="hero lex-hero" style="padding-block:var(--space-12) var(--space-8);"><div class="container">
<p class="kicker">{tr('Comprendre pour construire','Understand to build')}</p><h1>{tr('Le lexique de l’IA.','The AI glossary.')}</h1><hr class="rule--accent">
<p class="lead lex-intro">{tr('Des entreprises aux outils, des modèles aux usages : '+str(len(terms))+' définitions pour comprendre ce que tu utilises et suivre les projets du Knowledge Hub.','From companies and tools to models and use cases: '+str(len(terms))+' definitions to understand what you use and follow Knowledge Hub projects.')}</p>
<details class="lex-orientation"><summary>{tr("Entreprise, application, agent ou modèle : les repères","Company, app, agent or model: a quick guide")}</summary><div class="lex-map">{cardhtml}</div>
<p class="lex-topics">{tr('À distinguer','Tell them apart')} : <a href="#lex-gpt-6-astra">GPT-6 Astra</a> / <a href="#lex-project-astra">Project Astra</a> / <a href="#lex-iastro">iAstro</a> · <a href="#lex-claude-design">Claude Design</a> / <a href="#lex-claude-code">Claude Code</a></p></details>
<p class="caption">{tr('Les nouvelles fiches sont sourcées et datées. Les noms, versions et disponibilités évoluent : les liens officiels permettent de les vérifier.','New entries include dated references. Names, versions and availability change; official links let you check them.')}</p>
<div class="lex-controls"><div><label for="lex-q">{tr('Un mot, un outil, une question','A term, a tool, a question')}</label><div class="lex-search"><input type="search" id="lex-q" placeholder="ChatGPT, Astra, RAG, podcast…" autocomplete="off"></div></div><div><label for="lex-category">{tr('Explorer par catégorie','Browse by category')}</label><select id="lex-category"><option value="">{tr('Toutes les catégories','All categories')}</option>{options}</select></div></div>
<div class="lex-status"><p class="caption" id="lex-count" aria-live="polite">{len(terms)} / {len(terms)} {tr('termes','terms')}</p><button type="button" class="btn btn--ghost" id="lex-reset">{tr('Tout afficher','Show all')}</button></div>
<nav class="lex-az" id="lex-az" aria-label="{tr('Index alphabétique','Alphabetical index')}">{''.join(az)}</nav>
</div></section><section style="padding-top:0;"><div class="container"><ul class="lex-list" id="lex-list">{chr(10).join(rows)}</ul><p class="caption" id="lex-empty" hidden>{tr('Aucun terme trouvé. Essaie un autre mot ou une autre catégorie.','No matching terms. Try another word or category.')}</p></div></section></main>'''
        p=directory/'index.html';raw=p.read_text()
        raw=re.sub(r'<main id="main">.*?</main>',lambda _:main,raw,count=1,flags=re.S)
        raw=re.sub(r'<title>.*?</title>',lambda _:f'<title>{title}</title>',raw,count=1)
        for attr,value in [('name="description"',description),('property="og:description"',description),('property="og:title"',title)]:
            raw=re.sub('(<meta '+re.escape(attr)+r' content=")[^"]*(">)',lambda m:m[1]+esc(value)+m[2],raw,count=1)
        # Replace the former client-only list renderer, while preserving shared scripts.
        raw=re.sub(r'<script>\s*\(function\(\)\{\s*var listEl=.*?</script>','',raw,flags=re.S)
        raw=re.sub(r'<style id="lexique-style">.*?</style>','',raw,flags=re.S)
        raw=re.sub(r'<script id="lexique-filter">.*?</script>','',raw,flags=re.S)
        raw=re.sub(r'<script type="application/ld\+json" id="lexique-schema">.*?</script>','',raw,flags=re.S)
        raw=raw.replace('<!-- JSON-LD DefinedTermSet : injecté dynamiquement depuis glossaire.json (voir script) -->','')
        schema={'@context':'https://schema.org','@type':'DefinedTermSet','name':title,'url':url,'inLanguage':'en' if en else 'fr','author':{'@type':'Person','name':'Hugo Lahutte','@id':'https://hl-consulting.tech/#hugo'},'hasDefinedTerm':[{'@type':'DefinedTerm','name':t['terme'],'description':t['definition'].replace('**',''),'url':url+'#lex-'+t['id']} for t in terms]}
        raw=raw.replace('</head>',f'<style id="lexique-style">{CSS}</style>\n<script type="application/ld+json" id="lexique-schema">{json.dumps(schema,ensure_ascii=False).replace("<",chr(92)+"u003c")}</script>\n</head>')
        if 'property="og:image"' not in raw:raw=raw.replace('</head>','<meta property="og:image" content="https://hl-consulting.tech/knowledge-hub/assets/img/stage-panel-wide.jpg">\n</head>')
        if 'property="og:locale"' not in raw:raw=raw.replace('</head>',f'<meta property="og:locale" content="{tr("fr_FR","en_US")}">\n<meta property="og:locale:alternate" content="{tr("en_US","fr_FR")}">\n</head>')
        raw=raw.replace('Build in public avec Claude','Build in public avec Claude et ChatGPT').replace('Build in public with Claude','Build in public with Claude and ChatGPT') if 'Build in public avec Claude et ChatGPT' not in raw and 'Build in public with Claude and ChatGPT' not in raw else raw
        raw=raw.replace('</body>',f'<script id="lexique-filter">{JS}</script>\n</body>')
        raw=raw.replace('/knowledge-hub/en/coffre/','/knowledge-hub/coffre/')
        p.write_text(re.sub(r'\n{3,}','\n\n',raw))
        print(f'{p.relative_to(ROOT)}: {len(terms)} terms, static HTML, filters and sources')

if __name__=='__main__':
    build()
