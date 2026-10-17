"""Month selection and real browser rendering; no publication or TTS."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import render_podcast_covers as artwork

ROOT = Path(__file__).resolve().parents[1]


class ArtworkTests(unittest.TestCase):
    def test_date_duration_and_missing_month(self):
        html = artwork.layout(ROOT, '2026-11-01', 'full', 442)
        self.assertIn('01.11.2026', html)
        self.assertIn('7:22', html)
        self.assertIn('Le Débrief', html)
        self.assertNotIn('https://', html)
        with self.assertRaisesRegex(ValueError, 'Monthly iAstro portrait missing'):
            artwork.layout(ROOT, '2027-01-01', 'full', 442)

    @unittest.skipUnless(os.environ.get('PODCAST_RENDER_TEST') == '1', 'Chromium integration runs in CI')
    def test_month_rollover_and_preserved_artwork(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'assets/podcast/art', root / 'assets/podcast/art')
            episodes = [dict(date=day, short={'seconds': 63}, full={'seconds': 442})
                        for day in ('2026-10-31', '2026-11-01', '2026-12-01')]
            artwork.render(root, episodes)
            hashes = []
            for episode in episodes:
                path = root / episode['full']['image'].lstrip('/')
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest, episode['full']['image_sha256'])
                hashes.append(digest)
                stream = json.loads(subprocess.check_output([
                    'ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,codec_name',
                    '-of', 'json', str(path)], text=True))['streams'][0]
                self.assertEqual(stream, {'codec_name': 'mjpeg', 'width': 3000, 'height': 3000})
                if os.environ.get('PODCAST_PREVIEW_DIR'):
                    dest = Path(os.environ['PODCAST_PREVIEW_DIR'])
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, dest / (episode['date'] + '-test.jpg'))
            self.assertEqual(len(set(hashes)), 3)
            before = json.dumps(episodes)
            artwork.render(root, episodes)
            self.assertEqual(json.dumps(episodes), before)
            path.write_bytes(path.read_bytes() + b'changed')
            with self.assertRaisesRegex(ValueError, 'Published cover has changed'):
                artwork.render(root, episodes)
