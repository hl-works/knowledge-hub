# Production et diffusion proposées

## Qui fait quoi ?

Le choix utile porte sur les étapes et les outils, pas sur une promesse qu’un agent ne fera jamais d’erreur.

- **Agent éditorial / intégrateur** : exploite la veille existante, trie quatre à sept sujets, vérifie les sources, écrit le dialogue, choisit les références, compose la page et prépare les exports. Claude ou Codex peuvent tenir ce rôle selon les accès disponibles.
- **Production graphique** : utilise le même générateur d’images et la même référence canonique, avec les tenues du mois. Hugo peut la confier à ce chat ; une intégration ultérieure peut aussi la rendre accessible à l’autre agent. Cette connexion n’est pas installée par le pack.
- **Contrôle éditorial et visuel** : rapproche chaque case du script et des sources, compare les têtes à la V2, vérifie les bulles et la lecture sur téléphone. Hugo valide l’épisode avant publication.

Une bibliothèque améliore la cohérence ; elle ne garantit pas la fidélité de nouvelles générations. La documentation OpenAI recommande des références réutilisables pour conserver un personnage et décrit l’édition à partir d’images : [guide de prompting](https://developers.openai.com/api/docs/guides/image-prompting), [génération et édition](https://developers.openai.com/api/docs/guides/image-generation). Il s’agit de possibilités techniques, pas d’un engagement d’absence d’erreurs.

## Pipeline d’un épisode

1. Constituer le dossier de sources de la semaine ; conserver URL, date de consultation, date de publication et fait utilisé. Les sources primaires sont à privilégier. Les limites ou désaccords doivent apparaître dans le texte si pertinents.
2. Choisir quatre à sept nouvelles fortes et un fil conducteur. Réduire le nombre de sujets si la lecture devient trop dense.
3. Écrire des cases avec locuteurs, texte exact, but narratif et description visuelle. Vérifier le script avant la production graphique.
4. Réutiliser une pose quand elle sert la scène. Générer une nouvelle scène quand le décor, l’action ou la composition l’exige, avec la V2 et le vestiaire du mois en références. Produire l’illustration sans texte afin de ne pas dépendre du lettrage généré.
5. Assembler illustration et bulles dans une composition déterministe. Les coordonnées et l’ordre des bulles appartiennent à la case. Sur mobile, passer les cases en une colonne et conserver une taille de lecture confortable ; sur grand écran, utiliser une grille de deux ou trois colonnes lorsque les cases le permettent.
6. Vérifier la page à 360–430 px de large et sur grand écran. Lire le texte, contrôler les accents, les queues de bulles, les sources et l’intégrité du dessin. Exporter PNG/PDF depuis cette même composition, pas depuis une seconde version indépendante.
7. Après validation de Hugo, publier l’archive datée et mettre à jour la page du dernier épisode. Ne pas transformer automatiquement les brouillons en publications.

## URL et téléchargement

Recommandation : une URL permanente `/knowledge-hub/comics/` qui présente le dernier épisode **publié**, et une URL d’archive propre à chaque semaine, par exemple `/comics/2026-W42/`. Ce sont des chemins proposés, pas des pages existantes.

Le lien permanent est pratique dans le profil ou la navigation. Dans un message Telegram ou une newsletter annonçant un épisode, partager plutôt son lien d’archive : le lecteur retrouvera la même histoire un mois plus tard. La page propose « Lire », « Télécharger en PNG » et « Télécharger en PDF », plus les sources sous la BD et une transcription accessible.

Les fichiers d’épisodes publiés doivent être versionnés. En cas de correction, garder une trace et afficher un erratum. Un pointeur `latest.json` ne doit viser qu’un épisode publié avec un export existant ; le mettre à jour après les fichiers, pas avant. Définir une politique de cache courte pour ce pointeur et longue pour les fichiers versionnés.

## Quotidien ou hebdomadaire ?

Commencer par trois épisodes pilotes hebdomadaires. Cela donne de la place au scénario, à la vérification et aux dessins spécifiques. Mesurer le temps réel de fabrication, les reprises nécessaires et les retours lecteurs avant d’envisager un format quotidien plus court. Aucune fréquence automatique n’est configurée ici.

## Prochain lot graphique utile

Après validation du pilote : préparer un petit ensemble de personnages vraiment détourés pour les poses fréquentes et quelques décors récurrents, puis ajouter des scènes spéciales au besoin. Ne pas générer d’avance des centaines de variantes croisées mois × poses × expressions : la bibliothèque deviendrait coûteuse à maintenir et répétitive à lire.

Le pack actuel est une base de références et de vignettes réutilisables. Il ne contient pas encore un épisode d’actualité terminé. Le lecteur statique et la préparation des archives sont fournis à côté du kit ; les exports illustrés seront attachés aux épisodes produits.
