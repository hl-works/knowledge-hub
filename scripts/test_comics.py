"""Focused regression tests for editorial gates and stable archives."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('comics',Path(__file__).with_name('build_comics.py'))
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

class ComicsTests(unittest.TestCase):
    def fixture(self,count=5):
        news=[{'id':f'n{i}','title':'Test fixture','fact':'Synthetic test only','sources':[{'title':'Test source','publisher':'Test','url':'https://example.com/test','published_at':'2026-10-12','consulted_at':'2026-10-16'}]} for i in range(count)]
        return {'id':'2026-W42','status':'approved','title':'Test fixture, never publish','period_start':'2026-10-12','period_end':'2026-10-18','publication_date':'2026-10-18','wardrobe_month':10,'approval':{'editorial':True,'art':True,'publish':True,'by':'Hugo','reference':'Synthetic test only'},'news':news,'panels':[{'title':'Test','image':'kit/assets/characters/duo-reference-v2.png','alt':'Test illustration','news_ids':[n['id'] for n in news],'dialogue':[{'speaker':'Astro AI','text':'Test only'}]}],'downloads':{}}
    def test_four_and_seven(self):
        for n in (4,7):b.validate(self.fixture(n))
        for n in (3,8):
            with self.assertRaises(AssertionError):b.validate(self.fixture(n))
    def test_approval_gate(self):
        for field in ('editorial','art','publish'):
            ep=self.fixture();ep['approval'][field]=False
            with self.assertRaises(AssertionError):b.validate(ep)
    def test_missing_source_or_uncovered_fact(self):
        ep=self.fixture();ep['news'][0]['sources']=[]
        with self.assertRaises(AssertionError):b.validate(ep)
        ep=self.fixture();ep['panels'][0]['news_ids'].pop()
        with self.assertRaises(AssertionError):b.validate(ep)
    def test_untrusted_url_and_path(self):
        ep=self.fixture();ep['news'][0]['sources'][0]['url']='javascript:alert(1)'
        with self.assertRaises(AssertionError):b.validate(ep)
        ep=self.fixture();ep['panels'][0]['image']='../../style.css'
        with self.assertRaises(ValueError):b.validate(ep)
    def test_wrong_month(self):
        ep=self.fixture();ep['wardrobe_month']=12
        with self.assertRaises(AssertionError):b.validate(ep)
    def test_archives_latest_and_draft(self):
        oldroot,oldrepo=b.ROOT,b.REPO
        with tempfile.TemporaryDirectory() as tmp:
            b.REPO=Path(tmp);b.ROOT=b.REPO/'knowledge-hub/comics';(b.ROOT/'episodes').mkdir(parents=True)
            art=b.ROOT/'kit/assets/characters/duo-reference-v2.png';art.parent.mkdir(parents=True);art.write_bytes((oldroot/'kit/assets/characters/duo-reference-v2.png').read_bytes())
            try:
                ep=self.fixture();ep['status']='draft';f=b.ROOT/'episodes/2026-W42.json';f.write_text(json.dumps(ep))
                b.build();self.assertIsNone(json.loads((b.ROOT/'latest.json').read_text()))
                ep['status']='approved';f.write_text(json.dumps(ep));b.build()
                self.assertEqual(json.loads((b.ROOT/'latest.json').read_text())['id'],'2026-W42')
                before=(b.ROOT/'2026-W42/index.html').read_bytes();b.build();self.assertEqual(before,(b.ROOT/'2026-W42/index.html').read_bytes())
                ep['title']='Changed';f.write_text(json.dumps(ep))
                with self.assertRaises(ValueError):b.build()
            finally:b.ROOT,b.REPO=oldroot,oldrepo
    def test_escape_dialogue(self):
        out=b.panel(1,'Test','',[('Hugo','<script>alert(1)</script>')]);self.assertNotIn('<script>',out)

if __name__=='__main__':unittest.main()
