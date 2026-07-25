# `/mail` — Agent Email « boucles ouvertes » (page protégée)

Page projet interne servie sous `hl-consulting.tech/mail`, **protégée par mot de passe**
via **StatiCrypt** (même pattern que `hvs-carto-2026/`) : le contenu est chiffré en AES
côté build, illisible sans le mot de passe même en regardant la source.

## Fichiers

- `index.source.html` — **source en clair** (toutes les idées du projet). Ne vit **que**
  sur la branche feature, **jamais sur `main`** (sinon la page serait publique en clair).
- `index.html` — **artefact chiffré** généré par StatiCrypt. C'est le **seul** fichier
  `mail/` qui doit atterrir sur `main`.

## Générer / mettre à jour la page chiffrée

En local (Node requis), depuis la racine du repo :

```bash
# 1. chiffrer la source avec TON mot de passe (jamais commité, jamais dans le repo)
npx staticrypt mail/index.source.html -o mail/index.html

#    → StatiCrypt demande le mot de passe en interactif (ne pas le passer en -p pour
#      qu'il ne reste pas dans l'historique shell). Choisis un mot de passe fort.

# 2. vérifier en ouvrant mail/index.html dans un navigateur : écran de login → contenu.

# 3. ne pousser QUE l'artefact chiffré sur main
git checkout main
git pull origin main
git checkout claude/mail-code-project-50ghyv -- mail/index.html
git add mail/index.html
git commit -m "content: page projet agent email (/mail), protégée StatiCrypt"
git push origin main
```

> ⚠️ Ne jamais faire `git add mail/index.source.html` sur `main`.
> La source reste sur la branche feature (non déployée) pour les futures éditions.

## Éditer le contenu plus tard

1. modifier `mail/index.source.html` (sur la branche feature),
2. re-chiffrer (commande ci-dessus),
3. re-pousser `mail/index.html` sur `main`.

## Notes

- `robots: noindex, nofollow` + page hors sitemap/llms/search-index (privée, jamais
  indexée — ne pas la mailler dans les fichiers de découverte du knowledge-hub).
- Style : typo du site (Space Grotesk / Space Mono), fond blanc/noir + dark mode,
  **pas de corail** (réservé à l'accueil).
- Rappel : cette page présente les **idées** du projet. L'**agent** lui-même (fetch IMAP,
  triage LLM, Telegram, brouillons) est un process serveur → il vit sur le serveur
  Agents-IA (`/opt/agents/email`), pas sur GitHub Pages qui ne sert que du statique.
