#!/usr/bin/env python3
"""
Auto-traduction FR → EN d'une ou plusieurs pages, via l'API Claude.

Deux modes :
  • SPLICE (la jumelle en/<page> existe déjà — cas normal) : on garde tout le
    « chrome » de la page EN existante (nav, footer, hreflang, sélecteur de
    langue, liens d'assets, JSON-LD de nav — déjà corrects et en anglais US) et
    on ne re-traduit QUE le contenu (<main>) et les méta de tête (title,
    description, og:title, og:description) à partir de la version FR mise à jour.
    → idempotent, ne casse jamais le balisage i18n.
  • SCAFFOLD (page neuve, pas encore de jumelle EN) : on génère le squelette EN
    via i18n_scaffold.make_en (source FR vierge) puis on traduit toute la page.

Conçu pour la CI : chaque page FR nouvelle/modifiée (re)génère sa seule jumelle
EN. Le site FR n'est jamais modifié. Zéro dépendance pip (HTTP via urllib).

Env : ANTHROPIC_API_KEY (requis), KH_MODEL (défaut claude-sonnet-4-6).
"""
import os, sys, json, re, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import i18n_scaffold as sc

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("KH_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 32000

def guide():
    with open(os.path.join(ROOT, "scripts", "TRANSLATION_GUIDE.md"), encoding="utf-8") as f:
        return f.read()

def call_claude(system, user, api_key):
    body = json.dumps({
        "model": MODEL, "max_tokens": MAX_TOKENS, "system": system,
        "messages": [{"role": "user", "content": user}],
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        raise RuntimeError("API %s (modèle=%s) : %s" % (e.code, MODEL, detail))
    if data.get("type") == "error" or "content" not in data:
        raise RuntimeError("Réponse API inattendue : %s" % json.dumps(data)[:600])
    return "".join(part.get("text", "") for part in data.get("content", []))

# ---- transforms déterministes sur un fragment (corps <main>) ----
ASSET_ALT = "|".join(re.escape(a) for a in sc.ASSETS)
def absolutize(frag):
    frag = re.sub(r'(href|src)="(\.\./)?(' + ASSET_ALT + r')',
                  r'\1="' + sc.BASE + r'/\3', frag)
    frag = re.sub(r'(href|src)="(\.\./)?assets/', r'\1="' + sc.BASE + '/assets/', frag)
    frag = frag.replace('href="%s/"' % sc.BASE, 'href="%s/en/"' % sc.BASE)
    for s in sc.SECTIONS:
        frag = frag.replace('href="%s/%s' % (sc.BASE, s), 'href="%s/en/%s' % (sc.BASE, s))
    return frag

# ---- extraction de blocs ----
def grab(pattern, html, flags=0):
    m = re.search(pattern, html, flags)
    return m.group(1) if m else None

def head_strings(html):
    return {
        "title": grab(r"<title>(.*?)</title>", html, re.S),
        "description": grab(r'<meta name="description" content="(.*?)">', html, re.S),
        "og_title": grab(r'<meta property="og:title" content="(.*?)">', html, re.S),
        "og_description": grab(r'<meta property="og:description" content="(.*?)">', html, re.S),
    }

SYS_FRAG = ("\n\nTranslate the French text in this HTML fragment to natural, "
            "idiomatic American English (en-US), same tone, per the rules above. "
            "Keep ALL tags, attributes, URLs, hrefs and tag labels exactly as-is. "
            "Return ONLY the translated HTML fragment, no fences, no commentary.")
SYS_META = ('\n\nTranslate the VALUES of this JSON object from French to natural '
            'American English (en-US), same tone. Keep keys identical, keep proper '
            'nouns/brands. Return ONLY valid JSON, no fences.')

def translate_main(fr_main, api_key):
    out = call_claude(guide() + SYS_FRAG, fr_main, api_key).strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return absolutize(out)

def translate_meta(strings, api_key):
    payload = {k: v for k, v in strings.items() if v is not None}
    if not payload:
        return {}
    out = call_claude(guide() + SYS_META, json.dumps(payload, ensure_ascii=False), api_key).strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        return json.loads(out)
    except Exception:
        raise RuntimeError("Méta : JSON invalide renvoyé par l'API : %s" % out[:300])

def splice(rel, api_key):
    fr_html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    en_path = os.path.join(ROOT, "en", rel)
    en_html = open(en_path, encoding="utf-8").read()

    # 1) corps <main> : traduit depuis le FR, assets absolutisés, s-injecté
    m = re.search(r"(<main\b[^>]*>)(.*?)(</main>)", fr_html, re.S)
    if not m:
        raise RuntimeError("pas de <main> dans %s" % rel)
    en_main = translate_main(m.group(2), api_key)
    en_html = re.sub(r"(<main\b[^>]*>)(.*?)(</main>)",
                     lambda mm: mm.group(1) + en_main + mm.group(3),
                     en_html, count=1, flags=re.S)

    # 2) méta de tête (title / description / og:*) : traduites depuis le FR
    meta = translate_meta(head_strings(fr_html), api_key)
    def attr_esc(s): return s.replace("&", "&amp;").replace('"', "&quot;")
    def text_esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")
    if meta.get("title"):
        t = text_esc(meta["title"])
        en_html = re.sub(r"<title>.*?</title>", lambda x: "<title>%s</title>" % t, en_html, count=1, flags=re.S)
    if meta.get("description"):
        d = attr_esc(meta["description"])
        en_html = re.sub(r'(<meta name="description" content=").*?(">)', lambda x: x.group(1) + d + x.group(2), en_html, count=1, flags=re.S)
    if meta.get("og_title"):
        ot = attr_esc(meta["og_title"])
        en_html = re.sub(r'(<meta property="og:title" content=").*?(">)', lambda x: x.group(1) + ot + x.group(2), en_html, count=1, flags=re.S)
    if meta.get("og_description"):
        od = attr_esc(meta["og_description"])
        en_html = re.sub(r'(<meta property="og:description" content=").*?(">)', lambda x: x.group(1) + od + x.group(2), en_html, count=1, flags=re.S)

    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_html if en_html.endswith("\n") else en_html + "\n")
    return en_path

def scaffold_full(rel, api_key):
    """Page neuve : squelette EN (source FR vierge) + traduction complète."""
    sp = sc.site_path(rel)
    fr_full = sc.ORIGIN + sp
    en_full = sc.ORIGIN + sp.replace(sc.BASE + "/", sc.BASE + "/en/", 1)
    fr_html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    scaffolded = sc.make_en(fr_html, rel, fr_full, en_full)
    sysmsg = guide() + ("\n\nTranslate this full HTML document's French text to "
                        "American English (en-US), per the rules. The scaffolding "
                        "(paths, hreflang, language switcher) is already correct — "
                        "leave it untouched. Return ONLY the complete HTML document.")
    out = call_claude(sysmsg, scaffolded, api_key).strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    dest = os.path.join(ROOT, "en", rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out if out.endswith("\n") else out + "\n")
    return dest

def translate_file(rel, api_key):
    en_path = os.path.join(ROOT, "en", rel)
    return splice(rel, api_key) if os.path.exists(en_path) else scaffold_full(rel, api_key)

def main(argv):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY manquant.")
    rels = []
    for a in argv:
        a = a.strip()
        if not a.endswith(".html") or a.startswith(("en/", "coffre/")):
            continue
        if os.path.basename(a) == "404.html" or a.endswith("_template.html"):
            continue
        if os.path.exists(os.path.join(ROOT, a)):
            rels.append(a)
    if not rels:
        print("Aucune page FR à traduire.")
        return
    failures = []
    for rel in rels:
        mode = "splice" if os.path.exists(os.path.join(ROOT, "en", rel)) else "scaffold"
        print("→ traduction (%s) : %s" % (mode, rel))
        try:
            dest = translate_file(rel, api_key)
            print("  écrit :", os.path.relpath(dest, ROOT))
        except Exception as e:
            print("  ÉCHEC :", e, file=sys.stderr)
            failures.append(rel)
    if failures:
        sys.exit("Échec de traduction sur %d page(s) : %s" % (len(failures), ", ".join(failures)))

if __name__ == "__main__":
    main(sys.argv[1:])
