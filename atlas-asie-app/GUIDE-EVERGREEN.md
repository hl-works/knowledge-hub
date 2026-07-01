# Guide — écrire de l'evergreen correct (SEO + GEO) sur l'Atlas d'Asie

L'evergreen de ce site, ce sont les onglets **`Pays`**, **`Bestiaire`**,
**`Lexique`** et **`Pratique`** de la Google Sheet : le contenu qui a vocation à
être trouvé (Google) et cité (ChatGPT, Claude, Perplexity) **après** le voyage.
Le parcours, les trajets, le carnet Insta et la galerie sont datés par nature —
c'est très bien comme ça.

## 1. Comment le contenu devient visible (le pipeline)

Les pages rendent les CSV **côté client** ; les crawlers IA n'exécutent pas le JS.
Sans rien faire, Google et les LLMs ne verraient que des skeletons vides. D'où :

```
Google Sheet (ou fixtures CSV) ──▶ scripts/build_atlas_static.py ──▶
  • HTML statique des fiches Pays injecté dans atlas-asie/pays/index.html
    (facts + histoire + fun facts — le cœur citable)
  • timeline statique du Parcours dans atlas-asie/parcours/index.html
  • atlas-asie/sitemap.xml   (référencé par robots.txt)
  • atlas-asie/llms.txt      (index GEO, référencé par /llms.txt racine)
```

- Le JS de la page **écrase** le bloc statique au chargement : les visiteurs
  voient toujours la donnée fraîche, les crawlers voient le snapshot.
- Tout est automatique : le workflow `site-autobuild.yml` relance le script à
  chaque push touchant `atlas-asie/` **et chaque jour à 05:00 UTC** (cron), pour
  suivre la Sheet quand les URLs CSV publiées seront branchées dans `sheets.ts`.
- Un rebuild Astro (`npm run build`) purge le dossier `atlas-asie/` — blocs
  injectés, sitemap et llms.txt disparaissent : normal, le workflow les
  réinjecte au push. En local : `python3 scripts/build_atlas_static.py`.
- Bestiaire / Lexique / Pratique restent client-only pour l'instant (le snapshot
  statique couvre facts + histoire + fun facts). Si un jour on veut les rendre
  citables aussi : étendre `render_pays()` dans le script.

## 2. Les règles d'écriture d'une fiche evergreen

Une fiche est « evergreen » si elle reste vraie et citable dans 5 ans, sortie de
son contexte. Concrètement, dans la Sheet :

1. **Dates absolues, jamais relatives.** « Indépendant depuis 1991 », jamais
   « depuis 30 ans », « récemment », « l'année dernière ». Un LLM cite la phrase
   hors contexte et sans date de lecture.
2. **Un fait par fun fact, autonome et vérifiable.** Chaque puce doit se
   comprendre seule (c'est l'unité que les LLMs citent) : « La Grande Muraille
   dépasse 20 000 km » ✓ — « Elle est immense » ✗ (« elle » = perdu hors contexte).
3. **Chiffres avec ordre de grandeur, pas de précision périssable.**
   « ~20 millions d'habitants » vieillit bien ; « 19 874 233 habitants » est faux
   dans 6 mois. Le `~` est un choix, pas une paresse.
4. **Le voyage ne contamine pas l'evergreen.** « Vous allez les voir » ou
   « pour vous, c'est la porte d'entrée » date la fiche. Tout ce qui parle de
   *nous* va dans `Parcours` (description d'escale) ou le quiz « question
   famille » — pas dans `histoire`, `fun_facts` ni `Bestiaire`.
5. **`histoire` : 80–150 mots, du général au particulier.** Première phrase =
   la plus citable (c'est elle qui part dans llms.txt). Pas d'actualité chaude :
   ce qui peut changer à la prochaine élection n'a rien à y faire.
6. **Exception assumée : `Pratique`.** Visas, formalités, prix repères sont
   périssables par nature — c'est pour ça que la Sheet porte la mention
   « vérifié au 01/07/2026 ». Garder une date de vérification explicite, la
   mettre à jour quand on re-vérifie.
7. **Stabilité des noms.** `pays` sert de clé partout (palette, quiz, bestiaire,
   lexique, pratique, ancre `pays/#kazakhstan`) : ne pas renommer un pays dans
   la Sheet sans vérifier `PAL`/`CODE` dans `pays.astro` **et**
   `build_atlas_static.py`.

## 3. Checklist quand on ajoute / modifie un pays

- [ ] Ligne `Pays` complète : capitale, monnaie, langue, population (~), histoire, fun facts (séparés par ` • `), `photo_query`.
- [ ] 4 questions dans `Quiz` (dont 1 liée au voyage) avec `explication` — l'explication est aussi du contenu citable, soigne-la.
- [ ] ~3 animaux dans `Bestiaire`, les mots dans `Lexique`, la ligne `Pratique`.
- [ ] Relire avec le filtre « vrai dans 5 ans ? » (règles ci-dessus).
- [ ] Si nouveau pays : ajouter sa palette dans `PAL` et son code dans `CODE` (`pays.astro` + `build_atlas_static.py`).
- [ ] Rien d'autre à faire : le cron régénère statique + sitemap + llms.txt. Pour forcer : lancer le workflow `site-autobuild` à la main, ou `python3 scripts/build_atlas_static.py` en local.

## 4. Ce qui est déjà en place (ne pas re-payer le ticket)

- `<title>` + meta description uniques par page, canonical normalisé (slash final).
- Open Graph complet (url, image `brand/og.jpg`, image:alt, locale, site_name) + Twitter card — priorité WhatsApp assumée.
- JSON-LD authorship sur toutes les pages (`Person` = le `@id` canonique du
  domaine `https://hl-consulting.tech/#hugo`, `WebSite`, `WebPage`).
- Pas de hreflang : le site est monolingue FR (choix assumé, juin 2026). Un
  hreflang vers une page absente est pire que rien — on ne le rajoute que le
  jour où une vraie version EN existe.
- `robots.txt` racine : sitemap atlas déclaré, bots IA (GPTBot, ClaudeBot,
  PerplexityBot, Google-Extended) explicitement bienvenus.
- `/llms.txt` racine du domaine qui pointe vers les llms.txt du hub et de l'atlas.
- Liens internes avec slash final (sinon GitHub Pages répond par un 301).

## 5. Plus tard (dans l'ordre où ça rapporte)

1. **Brancher les URLs CSV publiées** dans `sheets.ts` : à partir de là, la Sheet
   pilote aussi le snapshot statique via le cron quotidien.
2. **Étendre le statique** à Bestiaire / Lexique / Pratique (du contenu evergreen
   aujourd'hui invisible des crawlers).
3. **Une page par pays** (`pays/kazakhstan/`) : une URL dédiée par sujet est ce
   qui se positionne et se cite le mieux. Le jour où on la fait, garder les
   ancres actuelles en redirection interne (liens `pays/#kazakhstan` → nouvelle page).
4. **Version EN des fiches Pays** (si un jour) : c'est l'evergreen qui mérite
   la traduction en premier (le parcours, non). Tant que le contenu vient d'une
   Sheet FR, une « version EN » n'est qu'une coquille — ne la lancer que si les
   données suivent. Rétablir alors pages `/en/`, hreflang et sitemap bilingue.
5. **Après le voyage** : passer les descriptions d'escales au passé une bonne
   fois (« nous avons dormi… ») — un site de voyage terminé qui parle au futur
   fait douter de tout le reste.
