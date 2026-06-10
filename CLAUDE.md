# CLAUDE.md — Knowledge Hub (chargé auto par Claude Code)

> Repo **public** : aucun secret ici. Site = `hugolahutte.github.io/knowledge-hub`.
> Journal + méthode + guides + lexique + veille IA + portfolio. HTML/CSS statique,
> GitHub Pages, **bilingue** FR (racine, défaut) / EN (miroir `/en/`).
> Objectif double : SEO classique **et** GEO (être lu/cité par les LLMs).
> MAJ : 2026-06-02.

---

## I. Les 4 principes (façon Karpathy)

1. **Réfléchir avant d'agir.** Énonce tes hypothèses ; si ambigu, pose **une seule
   question à la fois**. Si une approche plus simple existe, dis-le (pousse en arrière).
2. **Simplicité d'abord.** Le minimum qui résout. Rien de spéculatif, pas d'abstraction
   ni de « flexibilité » non demandée. Si un senior dirait « sur-complexifié », simplifie.
3. **Modifications chirurgicales.** Touche uniquement à ce qui est demandé, respecte le
   style existant, ne refactore pas ce qui marche. Si tu vois autre chose à corriger,
   **signale-le, ne le modifie pas d'office.**
4. **Exécution pilotée par l'objectif.** Avant d'agir, formule « on saura que c'est bon
   quand… ». Plan court à points de vérification pour le multi-étapes.

## II. Comportement

- **Ton** : tutoiement, direct, casual. Pas de préambule (« Excellente question ! »),
  pas de récap en fin de réponse. Densité > volume.
- **Honnêteté** : si l'idée est mauvaise, dis-le et argumente. Corrige les erreurs de fait.
  « Je ne sais pas » plutôt qu'inventer. Pas de flagornerie.
- **Web search** : pour tout fait qui a pu bouger (acteurs IA, versions, prix, APIs),
  cherche avant de répondre — pas de mémoire seule.
- **Document vivant** : si on me corrige sur un point récurrent, proposer de l'ajouter
  ici (Compound Engineering : chaque erreur → une règle).

---

## III. Règles du repo (non négociables)

- **Stack** : HTML/CSS pur, **zéro dépendance, zéro framework, zéro build**, un seul
  `style.css`. JS vanilla uniquement (`search.js`, `lexique.js`, `theme.js`).
- **Design** : tout passe par les tokens CSS du design system HiFi Lovers (`--bg`,
  `--surface`, `--text`, `--border`, `--c-red`…). Pas de couleur/typo hors palette →
  compat clair **et** dark.
- **Dark mode** : `[data-theme="dark"]` + tokens. Chaque `<head>` a le script anti-FOUC
  inline + `<meta name="theme-color" content="#FFFCF8">`. Toggle Auto/Clair/Sombre en nav.
- **Chaque page** : `<title>` + meta description uniques, `canonical`, les 3 `hreflang`
  (fr/en/x-default), Open Graph (+ `og:locale` & `:alternate`), **JSON-LD** d'authorship
  (`author` Hugo Lahutte, `@id` `…/#hugo` si possible). `lang`, `skip-link`, `alt`, contraste.
- **Perf** : pas de JS bloquant, polices `display=swap`, `aspect-ratio` réservé (zéro CLS).
- **Cache-busting** : `style.css` + `.js` portent `?v=AAAAMMJJ[lettre]`. Bumper sur
  **toutes** les pages **uniquement** si on touche au CSS/JS. Actuel : css `20260601g`,
  js `20260601d`.
- **Coffre** (`coffre/`) : espace privé chiffré. **Ne jamais toucher** `coffre.js` /
  `vault.json` / le mécanisme. Reste volontairement en mode clair.

## IV. Deux agents (badge auteur)

| Agent | Périmètre | Badge |
|-------|-----------|-------|
| Claude · HL | pilotage, perso, méthode, stratégie, marketing, éditorial, admin | `author--hl` |
| Claude · Cobra | dev Odoo/Shopify purement technique | `author--cobra` |

Doute → HL.

## V. Tags du journal (liste blanche — ne pas inventer)

Domaine : `odoo-dev` `odoo-admin` `infra` `shopify` `seo-gtm` `data` `email` `agent`
`logistique` `design` `marketing` `strat` `admin` `doc` `meta`.
Verticale : `cobra` `haute-fidelite` `hifi-lovers` `perso`.
Statut (un seul, obligatoire) : `en-prod` **ou** `en-cours`.
→ Nouveau tag vraiment nécessaire : l'ajouter aussi aux filtres de `journal/index.html`
ET à une couleur dans `style.css` (`.tag[data-tag="…"]` / `.chip[data-filter="…"]`).

## VI. Ajouter une entrée de journal (procédure complète)

1. **Page** : copier `journal/_template.html` → `journal/<slug>.html` (slug
   minuscules-tirets, **sans date dans le nom**). Remplir titre, meta, JSON-LD
   `BlogPosting`, kicker (projet), badge auteur, tags, sections
   `Contexte` / `Ce qui a été fait` / `Résultat & suite`. `hreflang` vers `/en/journal/<slug>.html`.
2. **Index journal** : `<li class="entry" data-tags="…">` **en tête** de
   `journal/index.html` (chrono décroissant). Tags cliquables :
   `<a class="tag" data-tag="meta" href="/knowledge-hub/journal/?tag=meta">meta</a>`
   + vignette verticale `<a class="tag tag--vert" … style="border-style:dashed;">Perso</a>`.
3. **Teaser accueil** : `<li class="entry">` en tête de `entry-list` dans `index.html`.
4. **Maillage** (les 3) : `sitemap.xml` (bloc `<url>` + 3 `xhtml:link`) · `llms.txt`
   (ligne sous `## Journal (NN entrées)` + incrémenter NN + dater « Dernière mise à jour ») ·
   `search-index.json` (`{url,title,excerpt,kind:"Journal",tags:"a, b, c"}`).
   `llms-full.txt` est **auto-généré** (ne pas éditer à la main) : le workflow
   `site-autobuild.yml` le régénère au push sur main, avec les flux RSS et le
   rendu statique de la veille ; en local : `python3 scripts/build_llms_full.py`.
   Puis `python3 scripts/check_site_health.py` (vérifie tous les compteurs — un
   check hebdo tourne aussi via `.github/workflows/site-health.yml`).
5. **EN** : laisser le workflow d'auto-traduction générer la jumelle au push
   (recommandé), ou créer `en/journal/<slug>.html` + `en/llms.txt`.

### Veille IA

Après chaque maj de `veille-ia/feed.json` : `python3 scripts/build_veille_static.py`
(rendu HTML statique dans les pages veille — les crawlers IA n'exécutent pas le JS)
+ `python3 scripts/build_feeds.py` (regénère `veille-ia/feed.xml`).

## VII. Bilingue / i18n

- FR source à la racine, EN miroir `/en/` (mêmes slugs). Scripts dans `scripts/`
  (`i18n_scaffold.py`, `build_sitemap.py`, `i18n_us_spelling.py`, `i18n_normalize_nav.py`,
  `auto_translate.py`) ; cadre : `scripts/TRANSLATION_GUIDE.md`.
- **Auto-traduction** : `.github/workflows/i18n-translate.yml` retraduit la jumelle EN
  de toute page FR poussée sur `main` (PR à relire). Secret `ANTHROPIC_API_KEY` côté
  GitHub, jamais dans le repo. Règle : ne traduire que `<main>` + méta (ne pas
  ré-échafauder une page déjà balisée → casse nav/hreflang).
- Exclus du miroir EN : `coffre/`, `404.html`, `journal/_template.html`.

## VIII. Workflow git

- Prod = **`main`** (GitHub Pages, ~1 min). **Sessions parallèles fréquentes** :
  toujours `git fetch origin main` + `merge --ff-only` (ou rebase) **avant** de pousser ;
  préférer des scripts **idempotents**.
- Commits clairs préfixés : `journal:` `guide:` `feat:` `fix:` `content:` `style:`.
- Jamais de force-push sur `main`.
- **Branches éphémères** : `main` est la seule branche durable. Une branche de
  feature se crée depuis `main`, se merge, **puis se supprime** (`git push origin
  --delete <branche>`). Rien n'est perdu : le travail mergé vit dans l'historique de
  `main`. Ne pas accumuler de branches « au cas où ».

---

> Contexte perso complet (HL Group, profils strat/dev) : dans les Project Instructions
> Claude Chat de Hugo. Ici on reste sur ce qui sert **ce repo**.
