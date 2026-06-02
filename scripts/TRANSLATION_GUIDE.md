# Guide de traduction FR → EN — Knowledge Hub

Référence unique pour traduire les pages du site en anglais, à la main ou via
le workflow automatique. Objectif : un anglais **naturel, idiomatique**, dans
**exactement le même ton** que le français.

## Ton (le plus important)

- Première personne, **direct et chaleureux**, "build in public".
- Le « tu » français devient un **"you" direct et amical** — jamais corporate.
- Contractions naturelles (it's, you'll, don't, here's).
- Accessible, sans jargon inutile, sans remplissage. Même énergie qu'en FR.
- On garde les apartés, les tirets, le rythme parlé. On ne « lisse » pas.

## À TRADUIRE

- `<title>`, `<meta name="description">`, `og:title`, `og:description`
- Tout le texte visible : titres, paragraphes, listes, boutons, liens, légendes
  (`<figcaption>`), `alt="…"`, et les `aria-label` français.
- Libellés d'UI courants :
  - « Aller au contenu » → "Skip to content"
  - aria-label « Principale » → "Main" · « Sommaire » → "Contents"
  - « Thème » → "Theme" · « Rechercher » → "Search"
- Dans le JSON-LD : **seulement les valeurs** des clés `headline`, `description`,
  `name`, `text`, `articleSection`, et les libellés génériques de `about`.
- Le **bloc prompt** (`.promptbox`) du guide méthode : traduire les instructions
  en anglais (un lecteur EN veut générer un CLAUDE.md en anglais).
- Les dates en texte visible peuvent passer en anglais (« 30 mai 2026 » →
  "May 30, 2026"). **Mais** ne touche jamais l'attribut `datetime="…"`.

## À NE PAS TOUCHER

- Tout ce qui est dans `href="…"`, `src="…"`, `"url":`, `"@id":` — **aucune URL,
  aucun slug** ne change.
- Les `<link rel="alternate" hreflang=…>`, le `<link rel="canonical">`,
  `og:url`, `og:locale` (déjà en `en_US`), `inLanguage` (déjà `en-US`).
- **Le sélecteur de langue** `<li class="nav__lang"><a … >FR</a></li>` : le laisser
  **strictement tel quel** (il pointe volontairement vers le FR et affiche "FR").
- Les `class`, `id`, `data-*`, `datetime`, la structure HTML, les entités.
- Le code, les commandes, les identifiants dans `<code>` / `<pre>` (sauf le
  langage naturel autour).
- Noms propres / marques : Cobra, Haute-Fidélité, HiFi Lovers, Claude, Claude
  Code, Anthropic, Odoo, Shopify, BigQuery, GitHub, SendCloud, Teams, etc.
- Le footer en katakana : `ナレッジ・ハブ`.

## Règles

- Préserver **tous** les tags, l'imbrication, les espaces et les entités HTML.
  Le fichier doit rester du HTML valide.
- Ne rien ajouter, ne rien supprimer comme section.
- Ne traduire **que** le fichier `en/…` indiqué. **Ne jamais** modifier le
  fichier FR correspondant à la racine.
- En cas de doute sur un terme métier, garder le terme et rester factuel.
