"""Editorial context and subscription invitation for the Veille landing page."""
import json
import re
from html import escape
from urllib.parse import urlsplit

CSS = '''
.radar-intro{max-width:70ch;margin:0 0 24px}.radar-date{font: .8rem var(--font-mono);color:var(--text-muted)}
.kiosk-news{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}.kiosk-news li{grid-template-columns:32px minmax(0,1fr);gap:12px}.kiosk-news li>div{min-width:0}.kiosk-news time{display:block;margin-bottom:10px}.kiosk-news p{color:var(--text)}.kiosk-news .news-source{font-size:.8rem;color:var(--text-muted)}.kiosk-news a:hover{text-decoration:underline}.kiosk-news a{overflow-wrap:anywhere}
.veille-method{border-top:1px solid var(--border-strong)}.veille-method>p{max-width:75ch}.veille-method details{padding:16px 0;border-bottom:1px solid var(--border)}.veille-method summary{font-weight:700;cursor:pointer}.veille-method details p{max-width:75ch;margin:12px 0 0}
.follow-invite[hidden]{display:none}.follow-invite{position:fixed;right:20px;bottom:20px;z-index:80;width:min(400px,calc(100vw - 32px));background:var(--bg);color:var(--text);border:1px solid var(--border-strong);border-top:4px solid var(--c-red);padding:20px;box-shadow:4px 4px 0 var(--border-strong);max-height:calc(100dvh - 40px);overflow:auto}.follow-invite h2{font-size:1.25rem;line-height:1.2;text-transform:none;margin:0 36px 10px 0}.follow-invite p{font-size:.9rem;line-height:1.45;margin:0 0 14px}.follow-invite nav{display:flex;gap:12px;align-items:center;flex-wrap:wrap}.follow-invite .btn{font-size:.75rem;padding:10px 14px}.follow-close{position:absolute;right:8px;top:8px;min-width:44px;min-height:44px;border:0;background:transparent;color:var(--text);font-size:1.4rem;cursor:pointer}.follow-invite a:focus-visible,.follow-invite button:focus-visible{outline:3px solid var(--c-red);outline-offset:3px}.follow-invite .follow-note{font-size:.7rem;color:var(--text-muted);margin:12px 0 0}
@media(max-width:640px){.kiosk-news{grid-template-columns:1fr}.kiosk-news li{grid-template-columns:24px minmax(0,1fr)}.follow-invite{right:16px;bottom:16px;padding:16px}.follow-invite p{font-size:.85rem}}
'''

def recent_news(feed, limit=6):
    """Most recent items, ranked within each day; preserve each item's real date."""
    selected, seen = [], set()
    for item in sorted(feed, key=lambda x: (x['date'], x.get('score', 0)), reverse=True):
        key = item['tweet_url']
        if key not in seen:
            selected.append(item)
            seen.add(key)
        if len(selected) == limit:
            break
    return selected

def radar_items(news):
    rows = []
    for i, item in enumerate(news, 1):
        date = item['date']
        source = item.get('auteur_x') or urlsplit(item['tweet_url']).hostname
        tags = ' · '.join(item.get('tags', []))
        rows.append(f'<li><span class="news-number">{i:02d}</span><div lang="fr"><time datetime="{date}">{date[8:10]}.{date[5:7]}.{date[:4]}</time><h3><a href="{escape(item["tweet_url"], quote=True)}">{escape(item["titre_fr"])}</a></h3><p>{escape(item["resume_fr"])}</p><p class="news-source">Source : {escape(source)} · {escape(tags)}</p></div></li>')
    return ''.join(rows)

def editorial_context(en, prefix):
    if en:
        title = 'How this AI watch works'
        intro = 'A selection of AI news by Hugo Lahutte, built with Claude, ChatGPT and their tools. The goal: understand announcements, keep their context and return to the sources.'
        questions = [
            ('What topics does it cover?', 'Models, assistants, agents, research, creative tools and the practical uses of AI. Le Radar iA gives you the written update; Le Flash and Le Débrief cover the audio; iAstro Sunday tells the week through comics.'),
            ('Where does the news come from?', 'Each Radar item links to its source and displays its date. The archive brings the selections together. Source coverage is being broadened following a suggestion from Simon Fourticq, a friend and Telegram subscriber.'),
            ('How is the content created?', 'AI tools help select, summarize and adapt the news into different formats. Hugo directs the project. The podcast uses synthetic voices; the comic includes AI-generated artwork and fictional scenes. Read the linked sources to check an announcement and its limits.'),
            ('Can I choose which formats to receive?', 'For now, one Telegram subscription covers text, audio and comics. Choosing one or combining several formats is a planned improvement; those separate preferences are not available yet.'),
            ('Can this method work for another topic?', 'Yes: define the topic, choose relevant sources, filter and verify the information, then adapt it to written, audio or illustrated formats. The selection criteria and review need to fit the subject.')]
        more, archive = 'Read how we built it →', 'Explore the dated archive and sources →'
    else:
        title = 'Comment cette veille est construite'
        intro = 'Une sélection d’actualités sur l’intelligence artificielle par Hugo Lahutte, construite avec Claude, ChatGPT et leurs outils. Le but : comprendre les annonces, garder leur contexte et pouvoir revenir aux sources.'
        questions = [
            ('Quels sujets sont couverts ?', 'Modèles, assistants, agents, recherche, création et usages concrets de l’IA. Le Radar iA donne les nouvelles en texte ; Le Flash et Le Débrief les mettent en voix ; iAstro Sunday raconte la semaine en comic.'),
            ('D’où viennent les informations ?', 'Chaque nouvelle du Radar renvoie à sa source et affiche sa date. Les archives regroupent les sélections. Nous élargissons les sources d’information à la suite d’une proposition de Simon Fourticq, un ami et abonné du Telegram.'),
            ('Comment les contenus sont-ils fabriqués ?', 'Les outils d’IA aident à sélectionner, résumer et adapter les informations aux différents formats. Hugo dirige le projet. Le podcast utilise des voix de synthèse ; le comic comporte des dessins générés par IA et des scènes fictives. Les sources liées permettent de vérifier les annonces et leurs limites.'),
            ('Peut-on choisir les formats à recevoir ?', 'Pour l’instant, un abonnement Telegram commun permet de suivre les textes, les audios et les comics. Le choix d’un format ou d’une combinaison de plusieurs formats est prévu, mais ces préférences séparées ne sont pas encore disponibles.'),
            ('Cette méthode fonctionne-t-elle pour un autre sujet ?', 'Oui : définir un sujet, choisir des sources adaptées, trier et vérifier les informations, puis les décliner en texte, en audio ou en images. Les critères de sélection et la vérification doivent être adaptés au domaine.')]
        more, archive = 'Lire les coulisses de la conception →', 'Explorer les archives datées et les sources →'
    return (f'<section class="veille-method" id="methode-veille"><p class="kicker">'+('Behind the scenes' if en else 'Les coulisses')+f'</p><h2>{title}</h2><p>{intro}</p>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in questions)+f'<p><a href="{prefix}journal/veille-podcast-comics-iastro-chatgpt.html">{more}</a></p><p><a href="{prefix}veille-ia/">{archive}</a></p></section>')

def invitation(en):
    title = 'Keep following AI news?' if en else 'On continue la veille ensemble ?'
    text = 'Text updates, audio and the Sunday comic: follow the Telegram channel, or find Hugo on social media.' if en else 'Les news, les audios et le comic du dimanche : retrouve la suite sur Telegram, ou suis Hugo sur les réseaux.'
    close = 'Close the subscription invitation' if en else 'Fermer l’invitation à s’abonner'
    note = 'External links open in a new tab.' if en else 'Les liens externes s’ouvrent dans un nouvel onglet.'
    return f'''<aside class="follow-invite" id="follow-invite" aria-labelledby="follow-title" hidden><button class="follow-close" type="button" aria-label="{close}">×</button><h2 id="follow-title">{title}</h2><p>{text}</p><nav aria-label="{'Follow Hugo' if en else 'Suivre Hugo'}"><a class="btn btn--primary" href="https://t.me/VeilleIA_HL">{'Join Telegram' if en else 'S’abonner sur Telegram'} ↗</a><a href="https://x.com/hugolh_ai">X ↗</a><a href="https://www.linkedin.com/in/hugo-lahutte/">LinkedIn ↗</a></nav><p class="follow-note">{note}</p></aside>'''

def external_tabs(page):
    def replace(match):
        tag = match.group()
        href = re.search(r'href="([^"]+)"', tag)
        if not href or urlsplit(href[1]).scheme not in ('https', 'http') or urlsplit(href[1]).hostname == 'hl-consulting.tech':
            return tag
        rel = re.search(r'\brel="([^"]*)"', tag)
        values = list(dict.fromkeys((rel[1].split() if rel else []) + ['noopener','noreferrer']))
        tag = re.sub(r'\s(?:target|rel)="[^"]*"', '', tag)
        return tag[:-1] + ' target="_blank" rel="' + ' '.join(values) + '">'
    return re.sub(r'<a\b[^>]*>', replace, page)

def english_interface(content):
    """Translate interface copy; source news, artwork and brand names stay French."""
    translations = {
        'Une sélection de Hugo Lahutte ↗':'Selected by Hugo Lahutte ↗',
        '01 / À LIRE':'01 / READ', '02 / À ÉCOUTER':'02 / LISTEN', '03 / LE DIMANCHE':'03 / SUNDAYS',
        'La veille quotidienne, directement sur Telegram.':'Daily news, also available on Telegram.',
        'Lire les dernières infos ↓':'Read the latest updates ↓',
        'Le Flash ou Le Débrief, à ton rythme.':'Le Flash or Le Débrief, at your own pace.',
        'Écouter les épisodes ↓':'Listen to the episodes ↓',
        'La semaine IA en comic, avec Hugo et iAstro.':'The AI week in comics, with Hugo and iAstro.',
        'Découvrir le comic ↓':'Explore the comic ↓', 'Les trois rendez-vous':'Three ways to follow',
        '01 / La veille quotidienne sur Telegram':'01 / Daily news on Telegram',
        'Toute la veille et ses sources →':'All updates and sources →',
        'Rejoindre Le Radar iA sur Telegram ↗':'Follow Le Radar iA on Telegram ↗',
        'Une sélection issue de la veille quotidienne. Remonte aux sources pour approfondir.':'A selection from the daily watch. Follow the source links for context.',
        '02 / L’actualité IA à écouter':'02 / AI news in audio',
        'Deux formats. Le même regard curieux.':'Two formats. The same curiosity.',
        'Dernière édition ·':'Latest edition ·',
        'Les nouvelles à retenir, en un clin d’œil.':'The key updates, in a short briefing.',
        'Les annonces, leur contexte et ce qu’elles changent.':'Announcements, context and what they change.',
        'Retrouver les audios sur Telegram →':'Find the audio on Telegram →',
        'Audio en français, avec une voix de synthèse. iAstro change de tenue au fil des mois.':'French audio with synthetic voices. iAstro changes outfits throughout the year.',
        'À réécouter':'Previous episodes', '03 / Le comic du dimanche':'03 / The Sunday comic',
        'Les grandes nouvelles de l’IA prennent vie dans l’atelier. Une histoire à la fois, avec ses dessins, ses explications et ses sources.':'AI news comes to life in the workshop. One story at a time, with illustrations, explanations and sources.',
        'Lire le dernier numéro →':'Read the latest issue →',
        'Chaque semaine · en français ·':'Weekly · in French ·', 'histoires · lecture mobile':'stories · mobile reading',
        'Tous les numéros et les archives →':'All issues and archives →',
        'Choisir une semaine de comics':'Choose a comic week',
        'Lire iAstro Sunday du':'Read iAstro Sunday for',
        'Recevoir la veille sur Telegram ↗':'Follow the news on Telegram ↗',
        'Retour au Knowledge Hub →':'Back to Knowledge Hub →',
        'La veille dans ta poche':'AI news in your pocket',
    }
    for fr,en in translations.items(): content = content.replace(fr,en)
    return content

def structured_data(page, en, news, latest, comic_url):
    origin = 'https://hl-consulting.tech'
    url = origin + ('/knowledge-hub/en/immersion-ia/' if en else '/knowledge-hub/immersion-ia/')
    author = {'@type':'Person', '@id':origin+'/#hugo', 'name':'Hugo Lahutte', 'url':origin+'/a-propos/'}
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'CollectionPage','@id':url+'#page','url':url,'name':'AI watch: news, podcasts and iAstro Sunday' if en else 'Veille IA : Radar, podcasts et iAstro Sunday','inLanguage':'en' if en else 'fr','author':author,'description':'Six recent sourced news items, daily audio and a weekly comic.' if en else 'Six actualités récentes avec leurs sources, un podcast quotidien et le comic du dimanche.','mainEntity':{'@id':url+'#formats'}},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Knowledge Hub','item':origin+('/knowledge-hub/en/' if en else '/knowledge-hub/')},{'@type':'ListItem','position':2,'name':'Veille IA','item':url}]},
        {'@type':'ItemList','@id':url+'#formats','itemListElement':[{'@type':'ListItem','position':i,'name':name,'url':url+anchor} for i,name,anchor in [(1,'Le Radar iA','#radar'),(2,'Le Podcast iA','#podcasts'),(3,'iAstro Sunday','#sunday')]]},
        {'@type':'ItemList','name':'Le Radar iA','itemListElement':[{'@type':'ListItem','position':i,'item':{'@type':'CreativeWork','name':n['titre_fr'],'abstract':n['resume_fr'],'url':n['tweet_url'],'inLanguage':'fr'}} for i,n in enumerate(news,1)]},
        {'@type':'PodcastSeries','@id':url+'#series','name':'Le Podcast iA','url':url+'#podcasts','inLanguage':'fr','author':author,'webFeed':origin+'/assets/podcast/feed.xml'}
    ]}
    for kind, name in [('short','Le Flash'),('full','Le Débrief')]:
        track = latest[kind]
        schema['@graph'].append({'@type':'PodcastEpisode','name':name+' — '+latest['date'],'datePublished':latest['date'],'inLanguage':'fr','url':url+'#podcasts','partOfSeries':{'@id':url+'#series'},'associatedMedia':{'@type':'AudioObject','contentUrl':origin+track['src'],'encodingFormat':'audio/mpeg','duration':'PT'+str(track['seconds'])+'S'}})
    encoded = json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    return re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _: '<script type="application/ld+json">'+encoded+'</script>',page,count=1,flags=re.S)
