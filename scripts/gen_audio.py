#!/usr/bin/env python3
"""Pré-génère les prononciations des mots du Lexique en MP3 (TTS Google
Translate, sans clé) → atlas-asie-app/public/fixtures/audio/*.mp3 + audio.json.

Qualité homogène sur tous les appareils (le site joue le MP3 au clic ; fallback
voix native du navigateur si le mot n'a pas de fichier — cas du mongol).
Idempotent : ne re-télécharge pas un fichier déjà présent.
"""
import csv, json, os, subprocess, time, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(ROOT, "atlas-asie-app", "public", "fixtures")
AUDIO_DIR = os.path.join(FIX, "audio")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# langue (Lexique) -> code TTS Google Translate. Mongol : pas de voix → natif.
TL = {"Russe": "ru", "Mandarin": "zh-CN", "Cantonais": "yue",
      "Malais": "ms", "Indonésien": "id"}


def tts(tl: str, text: str, out: str) -> bool:
    url = ("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob"
           f"&tl={tl}&q={urllib.parse.quote(text)}")
    r = subprocess.run(["curl", "-s", "-A", UA, "-o", out, "-w", "%{http_code}:%{content_type}", url],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    ok = code.startswith("200") and "audio" in code and os.path.getsize(out) > 800
    if not ok and os.path.exists(out):
        os.remove(out)
    return ok


def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    mapping = {}
    counters = {}
    seen = {}
    made = skipped = failed = 0
    with open(os.path.join(FIX, "lexique.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            langue = (row.get("langue") or "").strip()
            text = (row.get("mot_local") or "").strip()
            tl = TL.get(langue)
            if not tl or not text:
                continue
            key = f"{tl}|{text}"
            if key in seen:          # déjà traité (dédup)
                mapping[key] = seen[key]
                continue
            counters[tl] = counters.get(tl, 0) + 1
            fname = f"{tl}-{counters[tl]:02d}.mp3"
            path = os.path.join(AUDIO_DIR, fname)
            if os.path.exists(path) and os.path.getsize(path) > 800:
                skipped += 1
            else:
                if tts(tl, text, path):
                    made += 1
                    time.sleep(0.35)
                else:
                    failed += 1
                    print(f"  ⚠ échec {tl} '{text}'")
                    continue
            seen[key] = fname
            mapping[key] = fname
    with open(os.path.join(FIX, "audio.json"), "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=0)
    print(f"audio.json : {len(mapping)} mots | {made} générés, {skipped} déjà là, {failed} échecs")


if __name__ == "__main__":
    main()
