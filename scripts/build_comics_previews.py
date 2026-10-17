#!/usr/bin/env python3
"""Build the review shelf and story drafts; never change published issues."""
import json
from build_comics import ROOT, REPO, BASE, esc, shell, validate, build_preview
from comics_story_reader import CSS, art


def build():
    episodes = []
    for path in (ROOT / 'episodes').glob('*.json'):
        ep = json.loads(path.read_text())
        if ep.get('status') == 'draft' and ep.get('reader_variant') == 'story':
            episodes.append(validate(ep, preview=True))
    episodes.sort(key=lambda ep: ep['period_start'], reverse=True)
    cards = []
    months = ('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre')
    def dimensions(path):
        data = (ROOT / path).read_bytes()
        return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
    for ep in episodes:
        build_preview(ep['id'])
        start, end = ep['period_start'], ep['period_end']
        period = f"{int(start[8:])} {months[int(start[5:7])-1]} – {int(end[8:])} {months[int(end[5:7])-1]}"
        topics = ' · '.join(n['model_label'] for n in ep['news'])
        cards.append(f'<a class="issue-card" href="{BASE}drafts/{esc(ep["id"])}/">{art(ep["panels"][0], BASE, dimensions)}<span class="issue-copy"><small>{esc(period)} · {len(ep["news"])} histoires</small><h2>{esc(ep["title"])}</h2><p>{esc(topics)}</p><strong>Lire le numéro →</strong></span></a>')
    content = f'''<style>{CSS}
    .review-shelf{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin:28px 0 40px}}
    .issue-card{{display:flex;flex-direction:column;border:2px solid var(--border-strong);text-decoration:none;color:var(--text);background:var(--surface);min-width:0}}
    .issue-card:hover{{border-color:var(--c-red)}}.issue-card:focus-visible{{outline:3px solid var(--c-red);outline-offset:4px}}
    .issue-copy{{padding:20px;display:flex;flex-direction:column;flex:1;gap:14px}}.issue-copy h2{{font-size:26px;line-height:1.1;margin:0}}
    .issue-copy small{{font:12px/1.6 'IBM Plex Mono',monospace;color:var(--c-red)}}.issue-copy p{{font-size:16px;line-height:1.5;margin:0}}.issue-copy strong{{margin-top:auto;padding-top:10px}}
    @media(max-width:900px){{.review-shelf{{grid-template-columns:1fr}}.issue-card{{display:grid;grid-template-columns:160px 1fr}}.issue-copy h2{{font-size:24px}}}}
    @media(max-width:480px){{.issue-card{{display:flex}}.issue-copy{{padding:18px}}.review-shelf{{gap:24px}}}}
    </style><section class="sunday"><p class="edition">Hugo × iAstro · Septembre / octobre 2026</p><h1 class="masthead">iAstro <em>Sunday.</em></h1>
    <p class="dek">Trois semaines d’IA à lire tranquillement. Choisis un numéro, puis une histoire : les cases se lisent en faisant défiler.</p>
    <p class="preview-note">Éditions à relire · 4 histoires et 24 cases par numéro · Dessins et dialogues imaginés, annonces sourcées.</p>
    <div class="review-shelf">{''.join(cards)}</div><p><a href="/knowledge-hub/immersion-ia/">Retour au Kiosque IA →</a></p></section>'''
    for lang in ('fr', 'en'):
        prefix = '<p lang="en">These draft comics are available in French.</p>' if lang == 'en' else ''
        page = shell('iAstro Sunday — Les numéros à relire', 'Trois semaines de nouvelles IA en comics : 21 septembre au 11 octobre 2026.', prefix + content, lang, 'drafts/')
        page = page.replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>').replace('Hugo × Iastro', 'Hugo × iAstro')
        dest = ROOT / 'drafts/index.html' if lang == 'fr' else REPO / 'knowledge-hub/en/comics/drafts/index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page)
    print(f'OK: {len(episodes)} issues on the review shelf; no publication.')


if __name__ == '__main__':
    build()
