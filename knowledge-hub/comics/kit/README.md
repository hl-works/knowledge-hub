# Hugo × Iastro — bibliothèque graphique 1.2

Deux kits de personnage, un vestiaire commun de douze mois, 47 PNG référencés.

- `kits/hugo.json` : six expressions, six poses, identité et douze tenues de référence.
- `kits/iastro.json` : même structure pour Iastro ; identifiants historiques `ia-*` conservés.
- `index.html` : catalogue visuel et téléchargements individuels.
- `manifest.json` : chemins, dimensions, empreintes, provenance et état de validation.
- `docs/BIBLE.md` : identité et calendrier vestimentaire.

Les planches mensuelles représentent le duo. Ce sont des références illustrées opaques, pas 24 personnages détourés ni 144 poses saisonnières. Chaque nouveau dessin doit s’appuyer sur la V2 et le mois choisi. Les statuts individuels d’origine sont conservés ; le choix du nom et l’intégration des deux kits ont été demandés par Hugo le 16 octobre 2026.

Format retenu : hebdomadaire, cinq actualités par défaut, quatre à sept selon la semaine. Le nombre de cases suit les sujets ; ne jamais réduire la police pour tout faire tenir. Aucun épisode d’actualité n’est encore publié.

Lire `../README.md` pour préparer et vérifier un épisode.

## Direction narrative et casting

Le nom est **Iastro**. Le premier lot est complété par une étude de mise en scène dans « L’atelier des possibles » et une fiche de casting d’Alexandr Wang, La mise en scène V1 est validée par Hugo ; sa variante camouflage V2 et la fiche Wang V2 sont proposées. Les V1 restent archivées. Lire la direction dans `kit/docs/DIRECTION.md` depuis comics/ ou `docs/DIRECTION.md` depuis kit/. Les 43 PNG initiaux restent disponibles et inchangés.

Le registre `cast.json` au niveau comics/ contient les invités dessinés et les candidats à préparer. Ajouter `cast_ids` à un épisode ; un invité doit avoir sa référence graphique. Pour une réplique d’un invité réel : `attribution` vaut `quote`, `paraphrase` ou `fiction` ; les deux premières exigent `source_url` parmi les sources consultées. Le lecteur affiche le type d’attribution. `layout: wide` permet à une case d’occuper toute la rangée ; le mobile garde l’ordre de lecture.
