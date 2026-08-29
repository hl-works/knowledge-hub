---
name: kh-post-brief
description: Génère, en fin de session de travail, un brief Markdown prêt à publier sur le Knowledge Hub de Hugo Lahutte (hl-consulting.tech/knowledge-hub) — titre, verticale, auteur, tags de la liste blanche, statut, date, sections (contexte / ce qui a été fait / ce qui était difficile / stack / ce que ça illustre), visuels à joindre et garde-fous de sanitisation. À utiliser quand Hugo veut transformer une session (avec n'importe quelle IA) en entrée de journal KH. Le brief produit est ensuite collé à Claude Code sur le repo `hl-works/knowledge-hub`, qui publie l'entrée FR+EN et tout le maillage.
---

# Brief pour une entrée du Knowledge Hub

> **Portable.** Tout ce qui suit la ligne `═══` est autosuffisant : copie-le dans
> l'IA de ton choix (ChatGPT, Gemini, un autre Claude…) à la fin d'une session de
> travail, et elle produira le brief. Tu récupères le Markdown, tu le donnes à
> Claude sur le repo `knowledge-hub`, et il publie (FR + EN + maillage + health).

## Comment ça marche (côté Hugo)

1. Fin de session avec une IA → tu colles le bloc ci-dessous.
2. L'IA te rend un brief Markdown rempli.
3. Tu **attaches les captures/vidéos en fichiers** (bouton +, **pas** collées inline —
   sinon Claude ne peut pas les intégrer) et tu donnes le tout à Claude Code sur
   `hl-works/knowledge-hub`.
4. Claude crée l'entrée `journal/<slug>.html` (FR), sa jumelle `en/`, et met à jour
   index journal, teaser accueil, sitemap, `llms.txt`/`en`, `search-index` FR+EN,
   compteurs, `llms-full`, puis health check + PR.

Tu n'as **rien à savoir de la technique** : remplis le fond, Claude gère la forme.

═══════════════════════════════════════════════════════════════════════════

# 📝 Consigne : produis un brief d'entrée pour le Knowledge Hub

Tu es en fin de session de travail avec Hugo Lahutte. Résume ce qu'on a fait
en **un brief Markdown** destiné à devenir une entrée de son journal de bord
public « build in public » (Knowledge Hub). Objectif : un post **intéressant et
honnête** — pas un rapport interne. On raconte un problème réel, ce qui a été
construit, ce qui a coincé, et la leçon transférable.

Rends **uniquement** le Markdown ci-dessous, rempli. Écris en **français**
(la version anglaise est générée automatiquement ensuite). Sois **concret et
dense** : chiffres réels quand ils existent, zéro remplissage marketing.

```markdown
# Brief KH — <titre court et accrocheur>

## Méta
- **Verticale** : <cobra | haute-fidelite | hifi-lovers | perso>
- **Auteur** : <Claude · HL | Claude · Cobra>
- **Statut** : <en-prod | en-cours>
- **Date** : <AAAA-MM-JJ>
- **Tags** : <2 à 4 tags de la liste blanche, ex. agent, infra, data>
- **Temps passé** : <optionnel, ex. ~3 h / 2 sessions>

## Pitch (1 phrase)
<Ce que ça fait / résout, en une phrase claire.>

## Contexte — le problème
<Pourquoi on s'y est mis. Le point de douleur concret avant.>

## Ce qui a été fait
<Ce qui a été construit ou changé. Puces si utile. Termine par le RÉSULTAT
chiffré s'il existe (ex. « 6 familles en prod, ~300 prix réalignés »).>

## Ce qui était difficile / ce qu'on a appris
<Le vrai intérêt d'un post build-in-public : le piège rencontré, la décision
non triviale, la leçon transférable.>

## Stack / méthode
<Outils, langages, services, briques. Ex. Odoo 18, Python, Flask, API Claude…>

## Ce que ça illustre
<La leçon générale — ce qu'un lecteur retient même sans faire la même chose.>

## Visuels à joindre
<Liste chaque capture / vidéo et ce qu'elle montre. Hugo les attachera en
fichiers. Ex. « 1. dashboard-prix.png — la vue liste avec le statut par produit ».
Si un visuel contient des infos sensibles, dis-le (ex. « floute la colonne marge »).>
```

## Règles de choix (référence)

**Verticale** (une seule) :
- `cobra` — l'enseigne HiFi/Home-Cinéma dont Hugo est DG (dev Odoo/Shopify, ops, prix…).
- `haute-fidelite` — le magazine Haute Fidélité / HL Média (édito, veille, outils média).
- `hifi-lovers` — la marque/communauté HiFi Lovers.
- `perso` — méthode, réflexion, personnel, transverse.

**Auteur** (badge) :
- **Claude · Cobra** — uniquement pour du **dev Odoo/Shopify purement technique**.
- **Claude · HL** — tout le reste : pilotage, perso, méthode, stratégie, marketing,
  éditorial, média, admin, infra transverse. **Dans le doute → HL.**

**Tags — liste blanche stricte (ne rien inventer)** :
- *Domaine* : `odoo-dev` `odoo-admin` `infra` `shopify` `seo-gtm` `data` `email`
  `agent` `logistique` `design` `marketing` `strat` `admin` `doc` `meta`
- *Verticale* : `cobra` `haute-fidelite` `hifi-lovers` `perso`
- *Statut* (obligatoire, un seul) : `en-prod` **ou** `en-cours`
- Vise 2 à 4 tags : 1–3 domaine + le statut. La verticale est reprise à part.
  Si aucun tag existant ne colle vraiment, propose-le en le signalant — ne force pas.

**Statut** : `en-prod` = tourne réellement en production. `en-cours` = en chantier / partiel.

## Garde-fous — sanitisation (repo & site PUBLICS)

Ne mets **jamais** dans le brief :
- Secrets : tokens, clés API, mots de passe, adresses IP de serveurs, identifiants,
  noms d'hôtes internes, chemins privés.
- Chiffres financiers internes sensibles : marges, prix d'achat, CA détaillé,
  soldes bancaires. (Les ordres de grandeur opérationnels — « ~300 prix », « 6
  familles », « ~3-4 €/mois » — sont OK.)
- URLs / domaines d'**apps internes** privées (décris-les : « une app Flask à accès
  protégé », pas l'URL).

C'est **OK** de nommer : outils et services publics (Odoo, Shopify, Wiser, Telegram…),
marques et concurrents publics (Darty, Boulanger, Fnac, Son-Vidéo…), et de donner
les résultats en ordre de grandeur.

## Exemple (brief rempli)

```markdown
# Brief KH — Un agent qui lit les tarifs fournisseurs à ma place

## Méta
- **Verticale** : cobra
- **Auteur** : Claude · Cobra
- **Statut** : en-prod
- **Date** : 2026-08-07
- **Tags** : agent, odoo-dev, email
- **Temps passé** : ~2 sessions

## Pitch (1 phrase)
Une app interne qui lit les tarifs fournisseurs (PDF ou mail) et prépare la
création / mise à jour des produits dans Odoo, avec validation humaine.

## Contexte — le problème
Chaque tarif fournisseur demandait un traitement manuel long et propice aux
erreurs : lire, retrouver le produit, vérifier EAN/SKU, saisir les prix.

## Ce qui a été fait
Pipeline automatisé : upload PDF ou surveillance d'une boîte mail en lecture
seule → extraction EAN/SKU/prix via un modèle Claude → matching sur la base
Odoo → détection de doublons → validation humaine avant toute écriture.
Garde-fou : aucun produit créé n'est publié en ligne automatiquement.

## Ce qui était difficile / ce qu'on a appris
Filtrer le bruit d'une boîte mail chargée (newsletters, threads) sans rater les
vrais tarifs → passe de tri IA en amont. Et écrire dans Odoo sans corrompre les
prix des autres variantes d'un même produit.

## Stack / méthode
Python, IA générative pour l'extraction de documents, API Odoo, lecture d'une
boîte mail pro, interface web dédiée à accès protégé.

## Ce que ça illustre
Le bon pattern n'est pas « tout automatiser » mais : extraction → rapprochement
→ validation humaine → écriture. On garde l'humain aux étapes qui comptent.

## Visuels à joindre
1. maj-produits-liste.png — l'écran de validation avant écriture (ok tel quel).
```
