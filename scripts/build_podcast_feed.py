#!/usr/bin/env python3
"""Archive the public daily pair and build the full-only podcast RSS, offline.

Run after the producer's public-Telegram export, in its isolated site checkout.
No network, TTS, Telegram send or platform submission is performed here.
"""
import argparse
from datetime import date, datetime, time
from email.utils import format_datetime
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import uuid
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hl-consulting.tech'
FEED_URL = BASE + '/assets/podcast/feed.xml'
ITUNES = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
ATOM = 'http://www.w3.org/2005/Atom'
ET.register_namespace('itunes', ITUNES)
ET.register_namespace('atom', ATOM)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def audio_info(path, seconds):
    if not path.is_file() or not 1024 < path.stat().st_size < 25_000_000:
        raise ValueError(f'Missing or invalid MP3: {path}')
    probe = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration:stream=codec_name,codec_type', '-of', 'json', str(path)
    ], text=True, timeout=30))
    actual = float(probe['format']['duration'])
    audio = [s for s in probe['streams'] if s.get('codec_type') == 'audio']
    if (not audio or any(s['codec_name'] != 'mp3' for s in audio)
            or not math.isfinite(actual) or type(seconds) is not int
            or not 0 < seconds < 1800 or abs(actual - seconds) > 2):
        raise ValueError(f'Invalid MP3 codec or duration: {path}')
    return {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def archive_latest(root):
    """Refuse to change a dated archive, including a regenerated same-day MP3."""
    folder = root / 'assets/podcast'
    latest = read_json(folder / 'latest.json')
    day = date.fromisoformat(latest['date']).isoformat()
    manifest = read_json(folder / 'episodes.json')
    existing = next((e for e in manifest['episodes'] if e['date'] == day), None)
    if any(e['date'] > day for e in manifest['episodes']):
        raise ValueError('Latest audio is older than an existing archive')
    entry = {'date': day, 'version': latest['version']}
    digest = hashlib.sha256()
    copies = []
    for kind in ('short', 'full'):
        if latest[kind]['src'] != f'/assets/podcast/{kind}.mp3':
            raise ValueError('Unexpected latest audio path')
        source = folder / f'{kind}.mp3'
        info = audio_info(source, latest[kind]['seconds'])
        digest.update(source.read_bytes())
        relative = f'/assets/podcast/archive/{day}/{kind}.mp3'
        target = root / relative.lstrip('/')
        if existing and existing[kind]['src'] != relative:
            raise ValueError('Existing archive URL must not change')
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != info['sha256']:
            raise ValueError(f'Archive is immutable: {relative}')
        if existing and existing[kind].get('sha256', info['sha256']) != info['sha256']:
            raise ValueError(f'Archive hash changed: {relative}')
        # Keep already published artwork metadata on an idempotent daily retry.
        entry[kind] = {**(existing[kind] if existing else {}),
                       'src': relative, 'seconds': latest[kind]['seconds'], **info}
        copies.append((source, target))
    if digest.hexdigest()[:16] != latest['version']:
        raise ValueError('Latest manifest does not match the audio pair')
    # Validate both before copying either. Failed builds are never git-pushed.
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copyfile(source, target)
    if existing:
        existing.update(entry)
    else:
        manifest['episodes'].append(entry)
    manifest['episodes'].sort(key=lambda e: e['date'], reverse=True)
    manifest['archived_on'] = max(e['date'] for e in manifest['episodes'])
    write_json(folder / 'episodes.json', manifest)


def build(root=ROOT, archive=False, render_covers=False):
    folder = root / 'assets/podcast'
    show = read_json(folder / 'show.json')
    if not isinstance(show.get('email'), str) or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', show['email']):
        raise ValueError('A confirmed public podcast contact email is required in show.json')
    if not (folder / 'show-cover-v1.jpg').is_file():
        raise ValueError('Show artwork is missing')
    if archive:
        archive_latest(root)
    manifest = read_json(folder / 'episodes.json')
    episodes = manifest['episodes']
    if not episodes or len({e['date'] for e in episodes}) != len(episodes):
        raise ValueError('Empty archive or duplicate episode date')
    if render_covers:
        from render_podcast_covers import render
        render(root, episodes)
        write_json(folder / 'episodes.json', manifest)
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')

    def tag(parent, name, value=None, **attrs):
        element = ET.SubElement(parent, name, attrs)
        if value is not None:
            element.text = str(value)
        return element

    for key in ('title', 'link', 'description', 'language'):
        tag(channel, key, show[key])
    tag(channel, f'{{{ATOM}}}link', href=FEED_URL, rel='self', type='application/rss+xml')
    tag(channel, f'{{{ITUNES}}}author', show['author'])
    tag(channel, f'{{{ITUNES}}}explicit', 'false')
    tag(channel, f'{{{ITUNES}}}type', 'episodic')
    tag(channel, f'{{{ITUNES}}}category', text=show['category'])
    tag(channel, f'{{{ITUNES}}}image', href=show['image'])
    owner = tag(channel, f'{{{ITUNES}}}owner')
    tag(owner, f'{{{ITUNES}}}name', show['author'])
    tag(owner, f'{{{ITUNES}}}email', show['email'])
    image = tag(channel, 'image')
    for key, value in [('url', show['image']), ('title', show['title']), ('link', show['link'])]:
        tag(image, key, value)
    for episode in sorted(episodes, key=lambda e: e['date'], reverse=True):
        day = date.fromisoformat(episode['date'])
        track = episode['full']
        expected = f'/assets/podcast/archive/{day.isoformat()}/full.mp3'
        if track['src'] != expected:
            raise ValueError('Only permanent dated full audio URLs are allowed')
        info = audio_info(root / expected.lstrip('/'), track['seconds'])
        if track.get('sha256', info['sha256']) != info['sha256']:
            raise ValueError(f'Published archive has changed: {expected}')
        item = tag(channel, 'item')
        tag(item, 'title', episode.get('title') or f'Le Débrief du {day:%d/%m/%Y}')
        tag(item, 'link', show['link'])
        tag(item, 'description', episode.get('description') or (
            f'Le Débrief de la veille IA du {day:%d/%m/%Y}. '
            'Les annonces, leur contexte et leurs implications pratiques. '
            f'Retrouve les formats et la veille sur {show["link"]} '
            'Émission de Hugo LaHutte, avec une voix de synthèse.'))
        # Identity deliberately independent of show title, author and cover.
        guid = str(uuid.uuid5(uuid.NAMESPACE_URL, BASE + expected))
        tag(item, 'guid', 'urn:uuid:' + guid, isPermaLink='false')
        # Legacy manifests only provide a date: midnight Paris is a convention,
        # not a claim about the original Telegram send time.
        published = datetime.combine(day, time(), ZoneInfo('Europe/Paris'))
        tag(item, 'pubDate', format_datetime(published))
        tag(item, 'enclosure', url=BASE + expected, length=str(info['bytes']), type='audio/mpeg')
        tag(item, f'{{{ITUNES}}}duration', track['seconds'])
        tag(item, f'{{{ITUNES}}}explicit', 'false')
        tag(item, f'{{{ITUNES}}}episodeType', 'full')
        if track.get('image'):
            expected_image = track['image']
            allowed_images = [f'/assets/podcast/archive/{day.isoformat()}/full-cover-v{v}.jpg' for v in (1, 2)]
            picture = root / expected_image.lstrip('/')
            if (expected_image not in allowed_images or not picture.is_file()
                    or hashlib.sha256(picture.read_bytes()).hexdigest() != track.get('image_sha256')):
                raise ValueError(f'Published cover missing or changed: {expected_image}')
            probe = json.loads(subprocess.check_output([
                'ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height',
                '-of', 'json', str(picture)], text=True, timeout=30))['streams']
            if not probe or probe[0] != {'codec_name': 'mjpeg', 'width': 3000, 'height': 3000}:
                raise ValueError(f'Expected a 3000px JPEG: {expected_image}')
            tag(item, f'{{{ITUNES}}}image', href=BASE + expected_image)
    ET.indent(rss, space='  ')
    xml = ET.tostring(rss, encoding='utf-8', xml_declaration=True) + b'\n'
    output = folder / 'feed.xml'
    if not output.exists() or output.read_bytes() != xml:
        output.write_bytes(xml)
    return len(episodes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--archive-latest', action='store_true')
    parser.add_argument('--render-covers', action='store_true')
    args = parser.parse_args()
    print(f'{build(args.root, args.archive_latest, args.render_covers)} épisodes complets dans assets/podcast/feed.xml')
