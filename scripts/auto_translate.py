#!/usr/bin/env python3
"""
Auto-traduction FR → EN d'une ou plusieurs pages, via l'API Claude.

Pour chaque page FR passée en argument (chemin relatif au repo, ex.
`guides/cest-quoi-claude.html`) :
  1. génère le squelette EN (chemins, hreflang, sélecteur de langue…) via
     scripts/i18n_scaffold.make_en — le contenu y est encore en français ;
  2. demande à Claude de traduire ce squelette en respectant
     scripts/TRANSLATION_GUIDE.md (ton, règles, zones à ne pas toucher) ;
  3. écrit le résultat dans en/<page>.

Conçu pour tourner en CI (GitHub Actions) : chaque contenu FR nouveau ou
modifié déclenche la (re)traduction de sa seule jumelle EN. Le site FR n'est
jamais modifié. Zéro dépendance pip : appel HTTP via urllib.

Variables d'env : ANTHROPIC_API_KEY (requis), KH_MODEL (optionnel,
défaut claude-sonnet-4-6).
"""
import os, sys, json, urllib.request, urllib.error

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
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read())
    return "".join(part.get("text", "") for part in data.get("content", []))

def scaffold_en(rel):
    """Produit le HTML EN scaffoldé (contenu FR) pour la page FR `rel`."""
    sp = sc.site_path(rel)
    fr_full = sc.ORIGIN + sp
    en_full = sc.ORIGIN + sp.replace(sc.BASE + "/", sc.BASE + "/en/", 1)
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        html = f.read()
    return sc.make_en(html, rel, fr_full, en_full)

SYSTEM_SUFFIX = (
    "\n\nYou are a professional FR→EN translator for a static website. "
    "You receive a full HTML document whose visible text is in French but "
    "whose scaffolding (paths, hreflang, language switcher, canonical) is "
    "already correct. Translate ONLY what the guide says to translate, leave "
    "everything else byte-for-byte identical. Output the COMPLETE translated "
    "HTML document and NOTHING else — no markdown fences, no commentary."
)

def translate_file(rel, api_key):
    en_html = scaffold_en(rel)
    system = guide() + SYSTEM_SUFFIX
    user = ("Translate this HTML document's French text to English, per the "
            "rules above. Return the full document only:\n\n" + en_html)
    out = call_claude(system, user, api_key).strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0]
    if "<!DOCTYPE" not in out[:200] and "<html" not in out[:200]:
        raise RuntimeError("Réponse inattendue (pas de HTML) pour %s" % rel)
    dest = os.path.join(ROOT, "en", rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out if out.endswith("\n") else out + "\n")
    return dest

def main(argv):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ANTHROPIC_API_KEY manquant.")
    rels = []
    for a in argv:
        a = a.strip()
        if not a.endswith(".html"):
            continue
        if a.startswith("en/") or a.startswith("coffre/"):
            continue
        if os.path.basename(a) in ("404.html",) or a.endswith("_template.html"):
            continue
        if os.path.exists(os.path.join(ROOT, a)):
            rels.append(a)
    if not rels:
        print("Aucune page FR à traduire.")
        return
    for rel in rels:
        print("→ traduction :", rel)
        try:
            dest = translate_file(rel, api_key)
            print("  écrit :", os.path.relpath(dest, ROOT))
        except Exception as e:
            print("  ÉCHEC :", e, file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv[1:])
