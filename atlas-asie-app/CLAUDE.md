# CLAUDE.md — Atlas d'Asie (site de voyage, famille Lahutte)

## Objectif

Site de voyage familial, **très graphique, photo + vidéo en avant**. Deux usages distincts :

1. **Suivi du voyage** — où on est, où on va, dans quels hôtels (pour nous et pour les grands-parents).
2. **Découverte des pays** — contenu *evergreen* et éducatif : les enfants (Alexis et Emma) comme les parents peuvent venir apprendre des choses.

Voyage : **HM26 Atlas d'Asie été 2026**, famille Lahutte (Hugo, Marion, Alexis, Emma), Asie / Indonésie. Départ imminent → V1 doit être en ligne vite, puis on enrichit.

## Stack

- **Astro** — statique, i18n natif, perf, liberté de design totale.
- **Hébergement** — sous le domaine existant **`hl-consulting.tech`**, servi au chemin **`/atlas-asie`**, en **déploiement indépendant** (on réplique le montage du "hub", déjà servi à part sous ce domaine). Pas de Netlify.
- **Données = Google Sheet existante**, lue **en direct côté client** via CSV publié (PapaParse). Édition depuis le téléphone → site à jour en quelques secondes, **aucun rebuild**.

> ⚠️ **Sous-chemin (piège n°1 du déploiement)** : configurer `base: '/atlas-asie'` et `site: 'https://hl-consulting.tech'` dans `astro.config`. Tous les liens et assets doivent passer par `import.meta.env.BASE_URL` (ou les helpers Astro `<a href>` / `Astro.url`) — sinon le site marche en local mais casse en prod sur le sous-chemin (CSS non chargé, liens absolus morts).

## Source de données — RÈGLE DE SÉCURITÉ (non négociable)

- Trois onglets publiés en CSV et lus par le site : **`Parcours`**, **`Pays`** et **`Quiz`**.
- **NE JAMAIS lire, publier ni afficher** les onglets **`Passeport`** (numéros de passeport en clair) ni **`Financier`** (budget). Aucune donnée personnelle sensible ne doit toucher le site, ni en build ni en runtime.
- Les CSV publiés sont récupérés au chargement de la page, parsés, rendus.

## Modèle de données

### Onglet `Parcours` (le suivi — une ligne par escale)

`ordre` · `pays` · `ville` · `date_arrivee` · `date_depart` · `hotel_nom` · `hotel_lien` · `hotel_adresse` · `hotel_photo` · `lat` · `lng` · `description` · `photos` (URLs séparées par virgule) · `video` (URL) · `statut` · `photo_query`

- Une ligne = une **escale où on dort** (avec son hôtel, ses dates, ses coordonnées). Sert à la fois la carte (un point par escale) et la page hôtels.
- `statut` peut être calculé automatiquement à partir des dates (passé / en cours / à venir) ; sinon valeur manuelle.
- `photo_query` = mot-clé pour le fallback photo (voir section Médias).

### Onglet `Pays` (evergreen — une ligne par pays)

`pays` · `capitale` · `monnaie` · `langue` · `population` · `histoire` · `fun_facts` · `photo_query`

- `fun_facts` = liste séparée par ` • ` (un seul champ ; le code l'éclate en puces).
- `photo_hero` (optionnel) : si Hugo colle une URL, elle passe devant le fallback.

### Onglet `Quiz` (une ligne par question)

`pays` · `question` · `choix_a` · `choix_b` · `choix_c` · `bonne` (a/b/c) · `explication`

- 4 questions par pays, dont une reliée au voyage de la famille. Le code affiche, sous chaque fiche Pays, le mini-quiz des questions dont `pays` correspond.

## Pages (V1)

1. **Accueil** — hero plein cadre (photo ou vidéo), titre du voyage, **carte animée du parcours**, **bloc Live** ("Jour X · on est à [escale] · prochaine étape [ville] dans N jours" + mini compte à rebours), et **compteurs animés** (pays visités, vols pris, nuits, km parcourus, plus haut sommet) — tout calculé depuis le Parcours.
2. **Le Parcours** — timeline verticale des escales. Pour chaque escale : pays, ville, dates, **hôtel mis en avant** (nom, photo, adresse, lien), statut visuel (passé / en cours / à venir), photos + vidéo, et la **météo du lieu** (voir section Météo). C'est LA page que les grands-parents ouvrent.
3. **Les Pays** — une fiche par pays : grande photo, capitale, monnaie, langue, population, histoire, fun facts, et **un mini-quiz en bas de fiche** (questions du pays affiché, à choix multiples, avec correction + explication). Éducatif, lisible par un enfant, pensé pour un duel Alexis/Emma.
4. **Le Carnet** — feed **Instagram** (reels + posts) via widget **Behold.so**. Réutilisable en bandeau sur d'autres pages.
5. **Galerie** — agrège **toutes les photos/vidéos du champ `photos` des escales** (source unique = la sheet, pas de double saisie). Grille graphique, lightbox.

**Carte animée** (Leaflet ou MapLibre) : le tracé relie les escales dans l'ordre et s'allume selon le statut — passé en plein, escale en cours qui pulse, futur en pointillé. Élément signature du site.

## Univers graphique — AMHE

L'identité visuelle vient d'**AMHE** (initiales A·M·H·E + jeu de mots avec « âme »), la marque du premier grand voyage de la famille.

- **Source de vérité = `brief/amhe-design.md`** : le système de design distillé (concept, colonne vertébrale commune, 3 directions avec tokens exacts, do/don't).
- **Maquettes de référence** dans `brief/reference/` : `amhe-expedition.html`, `amhe-affiche.html`, `amhe-nuit.html`.
- CC reconstitue la colonne vertébrale commune en variables CSS, implémente la **direction retenue par Hugo** comme thème principal, et **n'invente pas** une autre identité.
- ⚠️ Les **données dans les maquettes sont des fixtures bidon** (Thaïlande/Vietnam/Angkor) : les vraies données sont dans `parcours.csv` / `pays.csv` / `quiz.csv`.
- Contraintes **structurelles** : photo full-bleed, beaucoup d'air, hiérarchie typo claire, mobile-first, grandes zones tactiles, perf (Lighthouse vert), animations sobres (`prefers-reduced-motion` respecté).

## i18n

FR d'abord. Mettre en place la structure i18n d'Astro pour pouvoir ajouter l'EN plus tard **sans refactor**. Ne PAS bloquer la V1 sur la traduction.

## Médias & photos

Stratégie photo à deux niveaux, pour avoir un max de belles images sans coller d'URLs à la main :

1. **Photo perso prioritaire** — si un champ photo (`hotel_photo`, `photos`, `photo_hero`) contient une URL dans la sheet, on l'affiche. Les photos du voyage passent toujours devant.
2. **Fallback automatique via API photo gratuite (Pexels)** — sinon, le site va chercher une image à partir du champ `photo_query` de l'escale / du pays. Légal, gratuit, hotlinkable, et ça couvre les 26 escales + 7 pays sans travail manuel.

- Clé API Pexels en variable d'environnement (jamais en dur). Unsplash possible en alternative.
- Créditer la source si l'API le demande (petit crédit discret).
## Météo

- **Open-Meteo** : gratuit, **sans clé API ni compte**. Appel côté client à partir des `lat`/`lng` du Parcours.
- Afficher la météo de l'escale en cours + une prévi rapide de la prochaine étape.
- Pas de donnée à remplir, zéro maintenance.

## Instagram — page "Le Carnet"

- Feed via **Behold.so** (offre gratuite), **pas l'API Meta directe** (Basic Display fermée fin 2024 → token à renouveler, revue d'app : trop fragile pour un site qui doit tourner seul).
- Connexion du compte une fois → widget posé sur la page Le Carnet, réutilisable en bandeau ailleurs.
- ⚠️ Le compte Insta doit être **public** sinon le feed ne tire rien.
- ⚠️ **Instagram est bloqué en Chine continentale** (escales 23/07–03/08 : Pékin, Zhangjiajie, Shanghai) : poste via VPN, le feed ne bouge pas ces jours-là. Le reste du site n'en dépend pas.

## Hors V1 (plus tard — "on ira de plus en plus loin")

- **Version EN complète**.
- **Quiz global multi-pays** (tous pays mélangés, scores).
- **Livre d'or** (mots des proches) → **nécessite un back** (Google Form qui écrit dans un onglet, ou widget de commentaires). **Exclu tant qu'on voyage** : on évite tout back à date.
- Convention de hashtag par lieu (#atlasasie_lombok…) pour router auto les posts Insta vers la bonne escale.

## Contraintes

- Mobile-first, perf (viser un Lighthouse vert).
- Aucune donnée sensible (cf. règle de sécurité).
- Contenu = la sheet, **jamais d'invention** de données factuelles.

## Critère de succès

On modifie une ligne de l'onglet `Parcours` dans la Google Sheet depuis le téléphone → en rechargeant le site (desktop **et** mobile), l'étape, l'hôtel et les médias sont à jour, **sans rebuild**. Les fiches `Pays` affichent photo + infos. Le rendu est "waouh" en plein écran.

## Méthode de build (plan court, validation à chaque étape)

1. Scaffold Astro (avec `base: '/atlas-asie'` + `site`) + structure i18n, puis premier déploiement sous `hl-consulting.tech/atlas-asie` en répliquant le montage du hub (squelette en ligne).
2. Couche données : fetch + parse des trois CSV publiés (Parcours, Pays, Quiz), types/modèle, fallback photo Pexels.
3. Accueil : carte animée + bloc Live + compteurs (tout dérivé du Parcours).
4. Page **Le Parcours** (timeline + hôtels + médias + météo Open-Meteo).
5. Page **Les Pays** (fiches evergreen + mini-quiz en bas de fiche).
6. Page **Le Carnet** (widget Insta Behold) + page **Galerie** (agrège les photos du Parcours).
7. Direction artistique / polish.

> Avant de coder une étape : énoncer le plan court et le critère de "c'est bon". Modifications chirurgicales, simplicité d'abord. Demander si ambigu (une question à la fois).
