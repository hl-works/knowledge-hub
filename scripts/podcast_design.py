"""Editable podcast cover layout. Illustration and dated typography stay separate."""
from html import escape

def duration(seconds):return f'{seconds//60}:{seconds%60:02d}'

COVER_CSS='''
.podcast-cover{--cover-accent:var(--c-red,#C6121F);container-type:inline-size;position:relative;aspect-ratio:1;width:100%;overflow:hidden;background:#FFFCF8;color:#0C0C0C;border:1px solid #0C0C0C;isolation:isolate}
.podcast-cover.full{--cover-accent:#39359E}
.cover-masthead{position:absolute;inset:0 0 auto;height:17%;padding:5% 6% 2%;display:flex;align-items:center;justify-content:space-between;gap:3%;z-index:2;border-bottom:1px solid #0C0C0C}
.cover-brand{font-family:var(--font-display,Arial),sans-serif;font-weight:900;letter-spacing:-.055em;font-size:8cqw;line-height:1;text-transform:uppercase;white-space:nowrap}
.cover-brand span{color:var(--cover-accent)}
.cover-signal{font-family:monospace;font-size:4cqw;color:var(--cover-accent)}
.cover-portrait{position:absolute;top:17%;left:0;width:100%;height:68%;object-fit:contain;background:#FFFCF8}
.cover-format{position:absolute;top:21%;left:5%;z-index:2;padding:1.5% 2.6%;background:var(--cover-accent);color:#fff;font-weight:800;font-size:3.7cqw;letter-spacing:.04em;text-transform:uppercase}
.cover-footer{position:absolute;inset:auto 0 0;height:17%;padding:3% 5%;display:flex;align-items:center;justify-content:space-between;gap:4%;border-top:1px solid #0C0C0C;background:#FFFCF8;z-index:2}
.cover-date{font-family:var(--font-mono,monospace);font-size:3.7cqw;line-height:1.45;text-transform:uppercase}
.cover-date strong{display:block;font-size:4.2cqw}
.cover-time{background:var(--cover-accent);color:white;font-family:var(--font-display,Arial);font-weight:900;font-size:9cqw;line-height:1;padding:4% 5%;min-width:30%;text-align:center}
'''

def cover(date,kind,seconds,portrait=None):
    month=date[5:7];portrait=portrait or f'/assets/podcast/art/iastro-{month}-v1.png'
    label='Le Flash' if kind=='short' else 'Le Débrief'
    d=date[8:10]+'.'+date[5:7]+'.'+date[:4]
    return f'''<div class="podcast-cover {kind}" role="img" aria-label="Radio Iastro, {label}, {d}, durée {duration(seconds)}"><div class="cover-masthead"><span class="cover-brand">Radio <span>Iastro</span></span><span class="cover-signal" aria-hidden="true">)))</span></div><img class="cover-portrait" src="{escape(portrait)}" alt="" width="1024" height="1024"><span class="cover-format">{label}</span><div class="cover-footer"><span class="cover-date">L’actualité IA<strong>{d}</strong></span><span class="cover-time">{duration(seconds)}</span></div></div>'''
