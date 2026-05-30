# CLAUDE.md — Knowledge Hub (instructions agents)

> Fichier de contexte interne pour les agents Claude qui travaillent sur ce repo.
> **Non référencé** depuis le site (exclu du sitemap, bloqué dans robots.txt).
> Ne pas y mettre de secrets — le repo est public.

## Projet

Knowledge Hub de Hugo Lahutte : journal de bord + méthode + portfolio, en
HTML/CSS statique sur GitHub Pages. Objectif : SEO classique **et** GEO (être
lu/cité par les LLMs).

## Règles de contribution (à respecter par tout agent)

- **Stack** : HTML/CSS pur. **Aucune** dépendance, aucun framework, aucun build, un seul `style.css`.
- **Design** : suivre les tokens du design system HiFi Lovers déjà dans `style.css`. Ne pas introduire de nouvelles couleurs/typos hors palette.
- **Chaque page** doit avoir : `<title>` + meta description uniques, `<link rel="canonical">`, Open Graph, et un bloc **JSON-LD** d'authorship (`author` = Hugo Lahutte).
- **Accessibilité** : `lang="fr"`, `skip-link`, `alt` sur les images réelles, contraste respecté.
- **Performance** : pas de JS bloquant, polices en `display=swap`, ratios d'images réservés (`aspect-ratio`) pour éviter le CLS.

## Deux agents

| Agent | Périmètre | Badge |
|-------|-----------|-------|
| Claude · HL | pilotage, perso, méthode | `author--hl` |
| Claude · Cobra | dev Odoo/Shopify | `author--cobra` |

## Ajouter une entrée de journal

1. Copier `journal/_template.html` → `journal/AAAA-MM-JJ-slug.html`, remplir tous les `{{...}}`.
2. Choisir le bon badge auteur.
3. Ajouter le `<li class="entry">` en haut de `journal/index.html`, de la section Journal de `index.html`, et de la verticale concernée.
4. Ajouter l'URL dans `sitemap.xml` et `llms.txt`.

## Workflow git

- Prod = branche **`main`** (publiée par GitHub Pages).
- Commits clairs, préfixés (`journal:`, `feat:`, `fix:`, `content:`).
- Pas de force-push sur `main`.

## À faire (backlog)

- [ ] Compléter la bio réelle dans `a-propos/` (placeholders `⟦À COMPLÉTER⟧`).
- [ ] Ajouter `sameAs` (LinkedIn, X `@hugolh_ai`) au JSON-LD Person.
- [ ] Remplacer les emplacements photo `.ph` par de vraies images (`assets/img/`).
- [ ] Décider d'une vraie solution de pages protégées (Cloudflare Access / repo privé).
- [ ] Image Open Graph (`assets/img/og-cover.jpg`) + dé-commenter les balises `og:image`.
