"""Render the shared cover layout to permanent, opaque episode JPEGs.

Only composes existing monthly artwork and factual typography; no image or
audio generation service, external font, Telegram or platform API is called.
Chromium is used by the publishing job, not by visitors to the static site.
"""
import base64
from datetime import date
import hashlib
import json
from pathlib import Path

from podcast_design import COVER_CSS, cover

COVER_VERSION = 2


def layout(root, day, kind, seconds):
    day = date.fromisoformat(day).isoformat()
    if kind not in ('short', 'full') or type(seconds) is not int or not 0 < seconds < 1800:
        raise ValueError('Invalid cover format or duration')
    portrait = root / f'assets/podcast/art/iastro-{day[5:7]}-v1.png'
    if not portrait.is_file():
        raise ValueError(f'Monthly iAstro portrait missing: {portrait.name}')
    uri = 'data:image/png;base64,' + base64.b64encode(portrait.read_bytes()).decode()
    # Same layout as the site, with local system fonts so publication never
    # depends on Google Fonts/Fontshare availability. All dimensions are CSS.
    css = COVER_CSS + '''
    *{box-sizing:border-box}html,body{margin:0;padding:0;background:#FFFCF8;
    overflow:hidden;font-family:Arial,sans-serif}
    .podcast-cover{width:3000px;height:3000px;border:0}
    '''
    return ('<!doctype html><html lang="fr"><meta charset="utf-8">'
            '<title>Le Podcast IA</title><style>' + css + '</style>'
            + cover(day, kind, seconds, uri) + '</html>')


def render(root, episodes):
    """Render missing covers only; never overwrite an already linked image."""
    plans = []
    for episode in episodes:
        for kind in ('short', 'full'):
            if kind not in episode:
                continue
            track = episode[kind]
            relative = f'/assets/podcast/archive/{episode["date"]}/{kind}-cover-v{COVER_VERSION}.jpg'
            target = root / relative.lstrip('/')
            if track.get('image'):
                previous = root / track['image'].lstrip('/')
                allowed = [f'/assets/podcast/archive/{episode["date"]}/{kind}-cover-v{v}.jpg'
                           for v in (1, COVER_VERSION)]
                if track['image'] not in allowed or not previous.is_file():
                    raise ValueError(f'Invalid permanent cover: {track["image"]}')
                if hashlib.sha256(previous.read_bytes()).hexdigest() != track.get('image_sha256'):
                    raise ValueError(f'Published cover has changed: {track["image"]}')
                if track['image'] == relative:
                    continue
                # A new layout gets a new URL. Keep the old JPEG untouched.
            if target.exists():
                raise ValueError(f'Untracked cover already exists: {relative}')
            # Validate all monthly sources before writing anything.
            plans.append((track, relative, target,
                          layout(root, episode['date'], kind, track['seconds'])))
    if not plans:
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(viewport={'width': 3000, 'height': 3000},
                                    device_scale_factor=1)
            page.route('**/*', lambda route: route.abort())
            for track, relative, target, html in plans:
                page.set_content(html, wait_until='load')
                page.evaluate('''async () => {
                    await document.fonts.ready;
                    await Promise.all([...document.images].map(img => img.decode()));
                }''')
                result = page.screenshot(type='jpeg', quality=92)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(result)
                track.update(image=relative, image_sha256=hashlib.sha256(result).hexdigest())
                # Update the downloadable 1080px PNGs from the same layout.
                export = root / 'assets/podcast/covers' / (target.parent.name + '-' + target.name.split('-')[0] + '.png')
                export.parent.mkdir(parents=True, exist_ok=True)
                page.add_style_tag(content='.podcast-cover{width:1080px;height:1080px}')
                page.locator('.podcast-cover').screenshot(path=str(export), type='png')
        finally:
            browser.close()


def render_daily(root, output, day, short_seconds, full_seconds):
    """Prepare one unpublished pair using exactly the archive renderer."""
    import shutil
    import tempfile
    day = date.fromisoformat(day).isoformat()
    episode = dict(date=day, full={'seconds': full_seconds})
    if short_seconds != 0:
        episode['short'] = {'seconds': short_seconds}
    # A fresh staging root avoids touching any previously published episode.
    with tempfile.TemporaryDirectory() as directory:
        stage = Path(directory)
        art = stage / 'assets/podcast/art'
        art.parent.mkdir(parents=True)
        art.symlink_to((root / 'assets/podcast/art').resolve(), target_is_directory=True)
        render(stage, [episode])
        output.mkdir(parents=True, exist_ok=True)
        for kind in ('short', 'full'):
            if kind not in episode:
                continue
            track = episode[kind]
            shutil.copyfile(stage / track['image'].lstrip('/'), output / f'{kind}-cover.jpg')
            shutil.copyfile(stage / f'assets/podcast/covers/{day}-{kind}.png', output / f'{kind}-cover.png')
        (output / 'artwork.json').write_text(json.dumps(episode, indent=2) + '\n')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--daily', help='Prepare unpublished artwork for YYYY-MM-DD')
    parser.add_argument('--short-seconds', type=int)
    parser.add_argument('--full-seconds', type=int)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.daily:
        if args.output is None:
            parser.error('--output is required with --daily')
        render_daily(args.root, args.output, args.daily, args.short_seconds, args.full_seconds)
    else:
        path = args.root / 'assets/podcast/episodes.json'
        manifest = json.loads(path.read_text())
        render(args.root, manifest['episodes'])
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
