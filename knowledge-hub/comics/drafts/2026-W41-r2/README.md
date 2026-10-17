# Nouvelle lecture du pilote — 17 octobre 2026

Brouillon éditorial, non publié. La demande de Hugo porte sur une lecture mobile plus naturelle, des dialogues de comic dans les cases, et une explication plus développée sous chaque scène. Les 24 illustrations approuvées de W41 sont réutilisées sans modification. Les dialogues et explications sont nouveaux : leurs approbations restent à false.

## Choix de lecture

Défilement vertical natif ; deux colonnes au-dessus de 699 px. Sommaire visuel de quatre sujets, barre supérieure compacte et sélecteur natif, liens de continuation dans le flux. Aucun défilement horizontal obligatoire, barre inférieure fixe ou changement automatique de hauteur. Le retour navigateur restaure la position précédente. Les ancres peuvent cibler un sujet ou une case. Sans JavaScript, le contenu et les liens du sommaire restent accessibles.

Les bulles sont composées en HTML dans le cadre de la case, avec un espace réservé au-dessus du dessin pour ne masquer aucun visage. Texte des bulles et explications mobile à 18 px. Un paragraphe de deux phrases environ sous chaque case explique le fait, un exemple ou une limite. Les exemples de l’atelier sont fictifs ; les liens primaires figurent sous chaque histoire. Les dates de consultation des quatre annonces ont été actualisées après lecture le 17 octobre.

## Références consultées

- [Guide officiel WEBTOON, p. 11–15 du PDF](https://webtoons-static.pstatic.net/creator101/fr/pdf/Creator-Handbook.pdf?dt=2024011501) : lecture verticale pensée pour petit écran, rythme et bulles lisibles. Les espacements exprimés en pixels d’illustration ne sont pas repris littéralement en pixels CSS.
- [GlobalComix Reader v3](https://globalcomix.com/news/details/177/announcing-globalcomix-reader-v3) : gestes natifs, navigation entre épisodes dans le flux et suppression de la barre inférieure. Référence de conception, pas affirmation sur l’interface actuelle de leur application.
- [Marvel Infinity Comics](https://help.marvel.com/article/marvel-what-are-marvel-infinity-comics) : format vertical conçu pour téléphone et tablette.

Ce comparatif porte sur les recommandations officielles, pas sur une recette exhaustive de leurs applications.

## Reconstruction et validation

`python3 scripts/build_comics.py --preview 2026-W41-r2`

`python3 scripts/test_comics.py`

URL locale : `/knowledge-hub/comics/drafts/2026-W41-r2/`.

Les archives approuvées, l’index et `latest.json` restent inchangés. Le rendu `reader_variant: story` est activé seulement pour cette révision. Pour publier, enregistrer l’accord éditorial explicite de Hugo avant d’activer l’épisode ; ne pas remplacer W41.

Recette effectuée dans le navigateur avec des vues de 320 × 640, 390 × 844 et 1280 × 900 : pas de débordement horizontal, bulles lisibles, liens entre sujets, sommaire, retour navigateur, thèmes clair et sombre. La validation sur un téléphone physique reste à faire par Hugo.
