# Knowledge Hub — Hugo Lahutte

Journal de bord et méthode de tout ce que je construis avec Claude. Mi-portfolio IA,
mi-documentation opérationnelle. Site statique **HTML/CSS, zéro dépendance, zéro
framework**, publié sur GitHub Pages.

🔗 **Live** : https://hl-consulting.tech/knowledge-hub/

> Domaine custom `hl-consulting.tech` (GitHub Pages + CNAME). Le contenu du KH vit
> dans le sous-dossier `knowledge-hub/` (servi à `…/knowledge-hub/`) ; la racine du
> repo porte la page d'accueil minimale, `CNAME`, `robots.txt`, `404.html` et le
> `sitemap.xml` d'index.

---

## Stack & principes

- HTML statique + un seul `style.css` (design system **HiFi Lovers v1.0**).
- **Perf SEO** : pas de JS bloquant, polices en `display=swap`, ratios d'images réservés (zéro CLS).
- **GEO** (être lu/indexé par les LLMs) : `llms.txt` + `llms-full.txt`, JSON-LD `Person` / `TechArticle` / `HowTo` / `ProfilePage` sur chaque page, `robots.txt` ouvert aux bots IA.
- Une **page HTML par entrée de journal** (indexabilité maximale).

## Structure

```
knowledge-hub/
├── index.html              ← accueil (méthode + projets + journal + contact)
├── style.css               ← feuille de style unique partagée
├── README.md
├── llms.txt / llms-full.txt← pointeurs GEO pour les LLMs
├── robots.txt / sitemap.xml
├── how-to/index.html       ← LA méthode (« Comment j'utilise Claude »)
├── a-propos/index.html     ← parcours / qui je suis (GEO authorship)
├── journal/
│   ├── index.html          ← liste chronologique
│   ├── _template.html      ← template à copier pour une nouvelle entrée
│   └── AAAA-MM-JJ-slug.html
├── cobra/ haute-fidelite/ hifi-lovers/ perso/
│   └── index.html          ← pages verticales (description + entrées liées)
└── docs/                   ← NON référencé, NON linké depuis le site
    └── CLAUDE.md
```

> ⚠️ `docs/` est exclu du sitemap et bloqué dans `robots.txt`. Pour du contenu
> réellement sensible (prompts, .md privés), **ne pas le commiter dans ce repo public** —
> voir « Pages protégées » plus bas.

---

## Workflow de contribution

Deux agents Claude alimentent ce repo :

| Agent | Périmètre | Badge auteur |
|-------|-----------|--------------|
| **Claude · HL** (perso) | Pilotage du projet, sessions perso, méthode | `author--hl` (noir) |
| **Claude · Cobra** | Sessions Odoo / Shopify / dev | `author--cobra` (indigo) |

### Ajouter une entrée de journal

1. Copier `journal/_template.html` → `journal/AAAA-MM-JJ-slug.html`
   (date du jour + slug en minuscules avec tirets).
2. Remplir : titre, date, contenu, **tags**, **badge auteur** (HL ou Cobra), et le bloc **JSON-LD** en tête (`datePublished`, `author`).
3. Ajouter une ligne `<li class="entry">…</li>` en haut de `journal/index.html`
   et de la section « Journal » de `index.html`.
4. Ajouter l'URL dans `sitemap.xml` et `llms.txt`.
5. Commit + push (voir ci-dessous).

### Format d'une entrée

- **Titre** : court, orienté résultat (« Webhook Shopify → Odoo : dédup des commandes »).
- **Excerpt** : 1–2 phrases, ce qui a été fait et pourquoi.
- **Tags** : projet (`cobra`, `perso`…) + techno (`shopify`, `css`…).
- **Auteur** : le bon badge selon l'agent.

### Pusher

```bash
git add -A
git commit -m "journal: <titre de l'entrée>"
git push -u origin <branche>
```

GitHub Pages redéploie automatiquement à chaque push sur la branche de publication.

---

## Pages protégées (sensibles)

GitHub Pages est **100 % statique** → pas de vraie auth côté serveur. Pour les `.md`,
prompts et projets confidentiels, au choix :

- **Ne pas les commiter ici** : les garder dans un repo privé séparé.
- **Cloudflare Access** (gratuit) devant un sous-domaine custom → mot de passe / SSO réel.
- En attendant : pages marquées `🔒` côté UI + `noindex`, mais le contenu reste public si commité. **Ne pas s'y fier pour du vraiment sensible.**

---

## Bilingue FR / EN

Le site est bilingue. **Le français reste la racine** ; l'anglais vit en miroir
sous `/en/`.

- `/knowledge-hub/<page>` → FR · `/knowledge-hub/en/<page>` → EN (mêmes slugs).
- Chaque page déclare ses alternatives : `hreflang` `fr` / `en` / `x-default`
  (x-default = FR), `canonical` et `og:locale` propres à chaque langue.
- Un **sélecteur de langue FR/EN** est présent dans la nav de chaque page
  (`li.nav__lang`), zéro JS pour la bascule.
- `search.js` et `lexique.js` détectent `/en/` et chargent l'index
  (`search-index.en.json`), le glossaire (`en/lexique/glossaire.en.json`) et les
  libellés d'UI en anglais.
- `sitemap.xml` liste les deux langues avec alternances `xhtml:link`.
- GEO : `en/llms.txt` + `en/llms-full.txt` ; le `llms.txt` FR pointe vers l'EN.
- Exclus du miroir : `coffre/` (privé), `404.html`, `journal/_template.html`.

### Outils (dossier `scripts/`)

| Script | Rôle |
|--------|------|
| `i18n_scaffold.py` | Génère/rafraîchit le miroir `/en/` (chemins, hreflang, sélecteur) — contenu FR à traduire ensuite. Idempotent. |
| `auto_translate.py` | Traduit une page FR → sa jumelle EN via l'API Claude, selon `TRANSLATION_GUIDE.md`. |
| `build_sitemap.py` | Régénère `sitemap.xml` bilingue (alternances hreflang). |
| `TRANSLATION_GUIDE.md` | Le ton et les règles de traduction (zones à ne pas toucher). |

### Workflow d'auto-traduction

`.github/workflows/i18n-translate.yml` : à chaque push sur `main` touchant une
page FR (`**.html` hors `en/`), il (re)traduit **uniquement** la jumelle EN et
ouvre une **Pull Request** (relecture humaine avant publication). Isolé du site
servi, donc sans risque de casse. **Prérequis** : secret `ANTHROPIC_API_KEY`
(Settings → Secrets → Actions). Déclenchable aussi à la main (`workflow_dispatch`).

> Règle de maintenance : tout nouveau contenu naît en FR ; la PR EN est générée
> automatiquement et relue avant merge.

---

## Développement local

Aucune build. Ouvrir `index.html` dans un navigateur, ou servir le dossier :

```bash
python3 -m http.server 8000   # puis http://localhost:8000
```

---

© 2026 Hugo Lahutte — Build in public avec Claude. Contact : hugo@hl-consulting.tech
