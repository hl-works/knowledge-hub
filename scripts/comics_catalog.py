"""Dated archives and navigation between the latest approved weekly editions."""
from datetime import date
from html import escape as e
from comics_story_reader import CSS as READER_CSS, art

MONTHS = ('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre')


def period(ep):
    start, end = (date.fromisoformat(ep[k]) for k in ('period_start', 'period_end'))
    left = str(start.day) if start.month == end.month and start.year == end.year else f'{start.day} {MONTHS[start.month-1]}' + (f' {start.year}' if start.year != end.year else '')
    return f'{left}–{end.day} {MONTHS[end.month-1]} {end.year}'


def current_editions(episodes):
    weeks = {}
    for ep in episodes:
        week, _, revision = ep['id'].partition('-r')
        rank = int(revision or 1)
        if week not in weeks or rank > weeks[week][0]:
            weeks[week] = (rank, ep)
    return sorted((entry[1] for entry in weeks.values()), key=lambda ep: ep['period_start'])


CSS = '''
.issue-nav,.week-pagination{max-width:1060px;margin:0 auto;color:var(--text)}
.issue-nav{display:flex;gap:16px;align-items:flex-start;justify-content:space-between;margin-bottom:24px;font-size:14px}
.issue-nav a,.issue-nav summary{min-height:44px;padding:10px 0;display:block;cursor:pointer}
.issue-nav details{border:1px solid var(--border-strong);padding:0 14px;max-width:100%;background:var(--surface)}
.issue-nav details a{border-top:1px solid var(--border);text-underline-offset:4px}
.issue-nav [aria-current=page]{font-weight:700;color:var(--c-red)}
.week-pagination{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-block:32px}
.week-pagination a{display:flex;flex-direction:column;gap:8px;border:1px solid var(--border-strong);padding:16px;min-height:68px;text-decoration:none;background:var(--surface);color:var(--text)}
.week-pagination small{font-size:13px}.week-pagination strong{font-size:16px}.week-pagination .all-issues{grid-column:1/-1;min-height:44px;text-align:center;justify-content:center}
.issue-nav a:focus-visible,.issue-nav summary:focus-visible,.week-pagination a:focus-visible{outline:3px solid var(--c-red);outline-offset:3px}
.review-shelf{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin:28px 0 40px}
.issue-card{display:flex;flex-direction:column;border:2px solid var(--border-strong);text-decoration:none;color:var(--text);background:var(--surface);min-width:0}
.issue-card:hover{border-color:var(--c-red)}.issue-card:focus-visible{outline:3px solid var(--c-red);outline-offset:4px}
.issue-copy{padding:20px;display:flex;flex-direction:column;flex:1;gap:14px}.issue-copy h2{font-size:26px;line-height:1.1;margin:0}
.issue-copy small{font:12px/1.6 'IBM Plex Mono',monospace;color:var(--c-red)}.issue-copy p{font-size:16px;line-height:1.5;margin:0}.issue-copy strong{margin-top:auto;padding-top:10px}
.archive-start{display:inline-flex;align-items:center;min-height:48px;padding:12px 18px;background:var(--text);color:var(--bg)!important;text-decoration:none;font-weight:700}
@media(max-width:900px){.review-shelf{grid-template-columns:1fr}.issue-card{display:grid;grid-template-columns:160px 1fr}.issue-copy h2{font-size:24px}}
@media(max-width:480px){.issue-nav{flex-direction:column;gap:6px}.issue-nav details{width:100%}.issue-card{grid-template-columns:100px 1fr}.issue-copy{padding:14px;gap:10px}.issue-copy h2{font-size:21px}.issue-copy p{font-size:14px}.issue-copy small{font-size:11px}.issue-card .crop{align-self:center}.review-shelf{gap:16px}.week-pagination{gap:8px}.week-pagination a{padding:12px}.week-pagination strong{font-size:14px}}
@media print{.issue-nav,.week-pagination{display:none}}
'''


def navigation(ep, editions, base):
    options = ''.join(f'<a href="{base}{e(item["id"])}/"'+(' aria-current="page"' if item['id']==ep['id'] else '')+f'>{e(period(item))}</a>' for item in reversed(editions))
    top = f'<style>{CSS}</style><nav class="issue-nav" aria-label="Navigation entre les semaines"><a href="{base}">← Tous les numéros</a><details><summary>Changer de semaine · {e(period(ep))}</summary>{options}</details></nav>'
    links = []
    before = [x for x in editions if x['period_start'] < ep['period_start']]
    after = [x for x in editions if x['period_start'] > ep['period_start']]
    for item, label, relation in [(before[-1] if before else None, '← Semaine précédente', 'prev'), (after[0] if after else None, 'Semaine suivante →', 'next')]:
        if item:
            links.append(f'<a rel="{relation}" href="{base}{e(item["id"])}/"><small>{label}</small><strong>{e(period(item))}</strong></a>')
    links.append(f'<a class="all-issues" href="{base}">Tous les numéros · choisir une date →</a>')
    bottom = '<nav class="week-pagination" aria-label="Continuer avec une autre semaine">'+''.join(links)+'</nav>'
    return top, bottom


def archive(editions, base, art_base, dimensions, en=False):
    cards=[]
    for ep in reversed(editions):
        topics=' · '.join(n.get('model_label',n['title']) for n in ep['news'])
        cards.append(f'<a class="issue-card" href="{base}{e(ep["id"])}/">{art(ep["panels"][0],art_base,dimensions)}<span class="issue-copy"><small><time datetime="{ep["period_start"]}">{e(period(ep))}</time> · {len(ep["news"])} histoires</small><h2>{e(ep["title"])}</h2><p>{e(topics)}</p><strong>Lire le numéro →</strong></span></a>')
    latest=editions[-1]
    return f'''<style>{READER_CSS}{CSS}</style><section class="sunday"><p class="edition">Hugo × iAstro · Le comic du dimanche</p><h1 class="masthead">iAstro <em>Sunday.</em></h1>
<p class="dek">Les grandes nouvelles de l’IA, une semaine à la fois. Choisis une date, puis une histoire : les cases se lisent en faisant défiler.</p>
{'<p lang="en">These weekly comics are available in French.</p>' if en else ''}
<a class="archive-start" href="{base}{e(latest["id"])}/">Dernier numéro · {e(period(latest))} →</a>
<div class="review-shelf">{''.join(cards)}</div><p>Dessins et dialogues imaginés. Chaque histoire comporte ses explications et les sources des annonces.</p></section>'''
