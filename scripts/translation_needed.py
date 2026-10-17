#!/usr/bin/env python3
"""Exit 0 for changed text, 2 for unchanged text; errors stay nonzero and distinct."""
from html import unescape
from pathlib import Path
import re
import subprocess
import sys
from audit_seo import Page, ROOT
from build_llms_full import MainExtractor

def signature(text):
    page=Page(text)
    main=MainExtractor(); main.feed(text); main._flush()
    values=[page.title,page.meta.get('description',''),page.meta.get('og:title',page.title),page.meta.get('og:description',page.meta.get('description','')),*main.blocks]
    return tuple(re.sub(r'\s+',' ',unescape(v)).strip() for v in values)

def needed(relative):
    path='knowledge-hub/'+relative
    try: old=subprocess.check_output(['git','show','HEAD~1:'+path],cwd=ROOT,stderr=subprocess.DEVNULL).decode()
    except subprocess.CalledProcessError: return True
    return signature(old)!=signature((ROOT/path).read_text())

if __name__=='__main__': sys.exit(0 if needed(sys.argv[1]) else 2)
