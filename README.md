# Knowledge Hub — Hugo Lahutte

Journal de bord et méthode de tout ce que je construis avec Claude. Mi-portfolio IA,
mi-documentation opérationnelle. Site statique **HTML/CSS, zéro dépendance, zéro
framework**, publié sur GitHub Pages.

🔗 **Live** : https://hugolahutte.github.io/knowledge-hub/

---

## Stack & principes

- HTML statique + un seul `style.css` (design system **HiFi Lovers v1.0**).
- **Perf SEO** : pas de JS bloquant, polices en `display=swap`, ratios d'images réservés (zéro CLS).
- **GEO** (être lu/indexé par les LLMs) : `llms.txt` + `llms-full.txt`, JSON-LD `Person` / `TechArticle` / `HowTo` / `ProfilePage` sur chaque page, `robots.txt` ouvert aux bots IA.
- Une **page HTML par entrée de journal** (indexabilité maximale).

## Structure

```
knowledge-hub/
├── index.html              ← accueil (méthode + projets + journal + consulting)
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

## Développement local

Aucune build. Ouvrir `index.html` dans un navigateur, ou servir le dossier :

```bash
python3 -m http.server 8000   # puis http://localhost:8000
```

---

© 2026 Hugo Lahutte — Build in public avec Claude. Conseil : **HL Consulting** · hugo.lahutte@gmail.com
