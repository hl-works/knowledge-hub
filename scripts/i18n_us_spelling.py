#!/usr/bin/env python3
"""
Normalise l'orthographe britannique → américaine dans le contenu EN.
Cible : en/**/*.html, en/**/*.txt, en/lexique/glossaire.en.json,
search-index.en.json. Ne touche JAMAIS aux fichiers FR.

Liste curée + bornes de mots + préservation de la casse (1re lettre).
Pensé pour rester sûr (pas de "ise→ize" aveugle qui casserait wise/rise/
advise/merchandise/expertise…).
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = {
    # -ise / -isation familles (stems sûrs)
    "organise":"organize","organised":"organized","organising":"organizing",
    "organisation":"organization","organisations":"organizations","organisational":"organizational",
    "optimise":"optimize","optimised":"optimized","optimising":"optimizing","optimisation":"optimization",
    "customise":"customize","customised":"customized","customising":"customizing","customisation":"customization",
    "prioritise":"prioritize","prioritised":"prioritized","prioritising":"prioritizing",
    "specialise":"specialize","specialised":"specialized","specialising":"specializing",
    "realise":"realize","realised":"realized","realising":"realizing",
    "recognise":"recognize","recognised":"recognized","recognising":"recognizing",
    "summarise":"summarize","summarised":"summarized","summarising":"summarizing",
    "categorise":"categorize","categorised":"categorized","categorising":"categorizing",
    "standardise":"standardize","standardised":"standardized","standardising":"standardizing",
    "normalise":"normalize","normalised":"normalized","normalising":"normalizing",
    "centralise":"centralize","centralised":"centralized",
    "maximise":"maximize","maximised":"maximized","minimise":"minimize","minimised":"minimized",
    "emphasise":"emphasize","emphasised":"emphasized",
    "utilise":"utilize","utilised":"utilized","utilisation":"utilization",
    "digitise":"digitize","digitised":"digitized","digitisation":"digitization",
    "modernise":"modernize","modernised":"modernized","modernisation":"modernization",
    "visualise":"visualize","visualised":"visualized","visualisation":"visualization",
    "personalise":"personalize","personalised":"personalized","personalisation":"personalization",
    "monetise":"monetize","monetised":"monetized","monetisation":"monetization",
    "localise":"localize","localised":"localized","localisation":"localization",
    "analyse":"analyze","analysed":"analyzed","analysing":"analyzing","analyser":"analyzer",
    "apologise":"apologize","apologised":"apologized",
    # -our → -or
    "behaviour":"behavior","behaviours":"behaviors","behavioural":"behavioral",
    "colour":"color","colours":"colors","coloured":"colored","colouring":"coloring",
    "favour":"favor","favours":"favors","favoured":"favored","favourite":"favorite","favourites":"favorites",
    "honour":"honor","honoured":"honored","labour":"labor","neighbour":"neighbor",
    "flavour":"flavor","flavours":"flavors","rumour":"rumor","harbour":"harbor",
    # -re → -er
    "centre":"center","centres":"centers","centred":"centered",
    "metre":"meter","metres":"meters","theatre":"theater","fibre":"fiber","calibre":"caliber",
    # -ce / -se
    "licence":"license","licences":"licenses","defence":"defense","offence":"offense","practise":"practice",
    # doublement L
    "modelling":"modeling","modelled":"modeled","labelling":"labeling","labelled":"labeled",
    "cancelling":"canceling","cancelled":"canceled","travelling":"traveling","travelled":"traveled",
    "signalling":"signaling","signalled":"signaled","fuelled":"fueled","fuelling":"fueling",
    # divers
    "grey":"gray","greyed":"grayed","catalogue":"catalog","catalogues":"catalogs",
    "programme":"program","programmes":"programs","whilst":"while","amongst":"among",
    "towards":"toward","learnt":"learned","spelt":"spelled","cosy":"cozy","storey":"story",
    "enrol":"enroll","fulfil":"fulfill","instalment":"installment","sceptical":"skeptical",
}

# regex unique, alternance triée par longueur décroissante
ALT = sorted(PAIRS, key=len, reverse=True)
RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in ALT) + r")\b", re.IGNORECASE)

def repl(m):
    w = m.group(0)
    out = PAIRS[w.lower()]
    if w[0].isupper():
        out = out[0].upper() + out[1:]
    return out

TARGETS = []
for dp, _, fs in os.walk(os.path.join(ROOT, "en")):
    for f in fs:
        if f.endswith((".html", ".txt", ".json")):
            TARGETS.append(os.path.join(dp, f))
TARGETS.append(os.path.join(ROOT, "search-index.en.json"))

def main():
    changed = 0; total = 0
    for p in TARGETS:
        if not os.path.exists(p): continue
        s = open(p, encoding="utf-8").read()
        new, n = RE.subn(repl, s)
        if n:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1; total += n
            print("  %-55s %d rempl." % (os.path.relpath(p, ROOT), n))
    print("Fichiers modifiés : %d | remplacements : %d" % (changed, total))

if __name__ == "__main__":
    main()
