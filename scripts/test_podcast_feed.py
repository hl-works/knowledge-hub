"""Exercise real MP3 validation, immutable archives and RSS identity locally."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

import build_podcast_feed as feed


class PodcastFeedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'assets/podcast'
        self.folder.mkdir(parents=True)
        show = feed.read_json(feed.ROOT / 'assets/podcast/show.json')
        show['email'] = 'owner@example.test'
        feed.write_json(self.folder / 'show.json', show)
        (self.folder / 'show-cover-v1.jpg').write_bytes(b'fixture')
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                        'sine=frequency=440:sample_rate=44100', '-t', '1',
                        '-c:a', 'libmp3lame', '-b:a', '128k', str(self.folder / 'full.mp3')], check=True)
        self.audio = (self.folder / 'full.mp3').read_bytes()
        (self.folder / 'short.mp3').write_bytes(self.audio)
        self.latest = {'date': '2026-10-17',
                       'version': hashlib.sha256(self.audio * 2).hexdigest()[:16]}
        for kind in ('short', 'full'):
            self.latest[kind] = {'src': f'/assets/podcast/{kind}.mp3', 'seconds': 1}
        feed.write_json(self.folder / 'latest.json', self.latest)
        feed.write_json(self.folder / 'episodes.json', {'episodes': []})

    def xml(self):
        return ET.parse(self.folder / 'feed.xml')

    def test_full_only_and_stable_identity_after_rename_and_next_day(self):
        feed.build(self.root, archive=True)
        before = (self.folder / 'feed.xml').read_bytes()
        guid = self.xml().findtext('./channel/item/guid')
        enclosure = self.xml().find('./channel/item/enclosure').attrib
        self.assertEqual(enclosure['length'], str(len(self.audio)))
        self.assertIn('/archive/2026-10-17/full.mp3', enclosure['url'])
        self.assertNotIn('short.mp3', before.decode())
        feed.build(self.root, archive=True)
        self.assertEqual(before, (self.folder / 'feed.xml').read_bytes())
        show = feed.read_json(self.folder / 'show.json')
        show['title'] = 'Un titre révisé & fidèle'
        feed.write_json(self.folder / 'show.json', show)
        self.latest['date'] = '2026-10-18'
        feed.write_json(self.folder / 'latest.json', self.latest)
        feed.build(self.root, archive=True)
        items = self.xml().findall('./channel/item')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[1].findtext('guid'), guid)
        self.assertEqual(items[1].find('enclosure').attrib, enclosure)
        self.assertEqual(self.xml().findtext('./channel/title'), show['title'])

    def test_same_day_regeneration_cannot_overwrite_archive(self):
        feed.build(self.root, archive=True)
        before = (self.folder / 'feed.xml').read_bytes()
        (self.folder / 'full.mp3').write_bytes(self.audio + b'changed')
        self.latest['version'] = hashlib.sha256(self.audio * 2 + b'changed').hexdigest()[:16]
        feed.write_json(self.folder / 'latest.json', self.latest)
        with self.assertRaisesRegex(ValueError, 'immutable'):
            feed.build(self.root, archive=True)
        self.assertEqual((self.folder / 'archive/2026-10-17/full.mp3').read_bytes(), self.audio)
        self.assertEqual((self.folder / 'feed.xml').read_bytes(), before)

    def test_incomplete_pair_and_bad_version_do_not_create_archive(self):
        (self.folder / 'full.mp3').unlink()
        with self.assertRaises(ValueError):
            feed.build(self.root, archive=True)
        self.assertFalse((self.folder / 'archive').exists())
        (self.folder / 'full.mp3').write_bytes(self.audio)
        self.latest['version'] = 'invalid'
        feed.write_json(self.folder / 'latest.json', self.latest)
        with self.assertRaisesRegex(ValueError, 'manifest'):
            feed.build(self.root, archive=True)
        self.assertFalse((self.folder / 'archive').exists())

    def test_mutable_url_duplicate_date_and_changed_archive_rejected(self):
        feed.build(self.root, archive=True)
        manifest = feed.read_json(self.folder / 'episodes.json')
        bad = copy.deepcopy(manifest)
        bad['episodes'][0]['full']['src'] = '/assets/podcast/full.mp3'
        feed.write_json(self.folder / 'episodes.json', bad)
        with self.assertRaisesRegex(ValueError, 'permanent'):
            feed.build(self.root)
        bad = copy.deepcopy(manifest)
        bad['episodes'].append(copy.deepcopy(bad['episodes'][0]))
        feed.write_json(self.folder / 'episodes.json', bad)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            feed.build(self.root)
        feed.write_json(self.folder / 'episodes.json', manifest)
        (self.folder / 'archive/2026-10-17/full.mp3').write_bytes(self.audio + b'changed')
        with self.assertRaisesRegex(ValueError, 'changed'):
            feed.build(self.root)

    def test_missing_contact_blocks_public_feed_before_archiving(self):
        show = feed.read_json(self.folder / 'show.json')
        show['email'] = None
        feed.write_json(self.folder / 'show.json', show)
        with self.assertRaisesRegex(ValueError, 'contact'):
            feed.build(self.root, archive=True)
        self.assertFalse((self.folder / 'archive').exists())
        self.assertFalse((self.folder / 'feed.xml').exists())


if __name__ == '__main__':
    unittest.main()
