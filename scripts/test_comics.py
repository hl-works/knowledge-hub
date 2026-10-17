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
        return {'id':'2026-W42','status':'approved','title':'Test fixture, never publish','period_start':'2026-10-12','period_end':'2026-10-18','publication_date':'2026-10-18','wardrobe_month':10,'approval':{'editorial':True,'art':True,'publish':True,'by':'Hugo','reference':'Synthetic test only'},'news':news,'panels':[{'title':'Test','image':'kit/assets/characters/duo-reference-v2.png','alt':'Test illustration','news_ids':[n['id'] for n in news],'dialogue':[{'speaker':'Iastro','text':'Test only'}]}],'downloads':{}}
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
    def test_retrospective_uses_original_season(self):
        ep=self.fixture();ep.update(id='2026-W36',period_start='2026-08-31',period_end='2026-09-06',publication_date='2026-10-16',wardrobe_month=9)
        b.validate(ep)
        ep['wardrobe_month']=10
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
                original_shell=b.shell
                try:
                    b.shell=lambda *args,**kwargs: original_shell(*args,**kwargs).replace('</head>','<style>/* Reader UI refresh */</style></head>')
                    with self.assertRaises(ValueError):b.build()
                    b.build(refresh_reader=True)
                    self.assertIn('Reader UI refresh',(b.ROOT/'2026-W42/index.html').read_text())
                finally:b.shell=original_shell
                ep['title']='Changed';f.write_text(json.dumps(ep))
                with self.assertRaises(ValueError):b.build()
                with self.assertRaises(ValueError):b.build(refresh_reader=True)
            finally:b.ROOT,b.REPO=oldroot,oldrepo
    def test_public_figure_attribution(self):
        ep=self.fixture();ep['cast_ids']=['hugo','iastro','alexandr-wang']
        line={'speaker':'Alexandr Wang','text':'Synthetic test only'};ep['panels'][0]['dialogue']=[line]
        with self.assertRaises(AssertionError):b.validate(ep)
        line['attribution']='fiction';b.validate(ep)
        self.assertIn('scène imaginée',b.render_episode(ep))
        line['attribution']='quote'
        with self.assertRaises(AssertionError):b.validate(ep)
        line['source_url']='https://example.com/test';b.validate(ep)
        ep['cast_ids']=['hugo','iastro']
        with self.assertRaises(AssertionError):b.validate(ep)
    def test_wide_panel(self):
        ep=self.fixture();ep['panels'][0]['layout']='wide';b.validate(ep)
        self.assertIn('grid-column:1 / -1',b.render_episode(ep))
        ep['panels'][0]['layout']='unknown'
        with self.assertRaises(AssertionError):b.validate(ep)
    def test_mobile_story_structure_and_crop(self):
        ep=self.fixture(4);ep['format']='webtoon';base=ep['panels'][0]
        ep['panels']=[]
        for news in ep['news']:
            for _ in range(6):
                p=copy.deepcopy(base);p['news_ids']=[news['id']];p['crop']={'x':0,'y':0,'w':1/3,'h':1/2};ep['panels'].append(p)
        b.validate(ep)
        out=b.render_episode(ep);self.assertEqual(out.count('class="comic-card"'),24)
        self.assertIn('aria-label="Case suivante"',out)
        ep['panels'][0]['crop']['x']=.9
        with self.assertRaises(AssertionError):b.validate(ep)
        ep['panels'][0]['crop']['x']=float('nan')
        with self.assertRaises(AssertionError):b.validate(ep)
        ep['panels'][0]['crop']['x']=0
        del ep['panels'][:2]
        with self.assertRaises(AssertionError):b.validate(ep)
    def test_draft_preview_cannot_publish(self):
        oldroot,oldrepo=b.ROOT,b.REPO
        with tempfile.TemporaryDirectory() as tmp:
            b.REPO=Path(tmp);b.ROOT=b.REPO/'knowledge-hub/comics';(b.ROOT/'episodes').mkdir(parents=True)
            art=b.ROOT/'kit/assets/characters/duo-reference-v2.png';art.parent.mkdir(parents=True);art.write_bytes((oldroot/'kit/assets/characters/duo-reference-v2.png').read_bytes())
            try:
                ep=self.fixture();ep['status']='draft';ep['approval']={'editorial':False,'art':False,'publish':False}
                (b.ROOT/'episodes/2026-W42.json').write_text(json.dumps(ep))
                b.build();before=(b.ROOT/'latest.json').read_bytes();b.build_preview('2026-W42')
                self.assertEqual(before,(b.ROOT/'latest.json').read_bytes())
                self.assertFalse((b.ROOT/'2026-W42').exists())
                self.assertIn('noindex,nofollow',(b.ROOT/'drafts/2026-W42/index.html').read_text())
                with self.assertRaises(AssertionError):b.validate(ep)
                with self.assertRaises(AssertionError):b.build_preview('../../bad')
            finally:b.ROOT,b.REPO=oldroot,oldrepo
    def test_story_reader_preserves_text_and_requires_explanations(self):
        ep=json.loads((b.ROOT/'episodes/2026-W41-r2.json').read_text())
        ep['status']='draft'
        ep['approval']={'editorial':False,'art':False,'publish':False}
        b.validate(ep,preview=True)
        out=b.render_episode(ep,preview=True)
        self.assertEqual(out.count('class="scene"'),24)
        self.assertEqual(out.count('class="scene-note"'),24)
        self.assertEqual(out.count('class="story"'),4)
        self.assertIn('href="#info-mistral"',out)
        self.assertNotIn('reader-pager',out)
        ep['panels'][0]['explanation']['text']='<script>alert(1)</script>'
        self.assertIn('&lt;script&gt;',b.render_episode(ep,preview=True))
        del ep['panels'][0]['explanation']
        with self.assertRaises(AssertionError):b.validate(ep,preview=True)

    def test_escape_dialogue(self):
        out=b.panel(1,'Test','',[('Hugo','<script>alert(1)</script>')]);self.assertNotIn('<script>',out)

    def test_week_catalog_prefers_revision_and_chronology(self):
        def edition(id, start, end, published):
            return {'id':id,'period_start':start,'period_end':end,'publication_date':published}
        old=edition('2026-W39','2026-09-21','2026-09-27','2026-10-20')
        middle=edition('2026-W40','2026-09-28','2026-10-04','2026-10-17')
        first=edition('2026-W41','2026-10-05','2026-10-11','2026-10-16')
        revision=dict(first,id='2026-W41-r2')
        later_revision=dict(first,id='2026-W41-r10')
        editions=b.comics_catalog.current_editions([first,later_revision,old,revision,middle])
        self.assertEqual([ep['id'] for ep in editions],['2026-W39','2026-W40','2026-W41-r10'])
        top,bottom=b.comics_catalog.navigation(middle,editions,b.BASE)
        self.assertIn('21–27 septembre 2026',bottom)
        self.assertIn('5–11 octobre 2026',bottom)
        self.assertIn('rel="prev" href="/knowledge-hub/comics/2026-W39/"',bottom)
        self.assertIn('rel="next" href="/knowledge-hub/comics/2026-W41-r10/"',bottom)
        self.assertNotIn('/2026-W41-r2/',top)
        self.assertIn('aria-current="page"',top)

if __name__=='__main__':unittest.main()
