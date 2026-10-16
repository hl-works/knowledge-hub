# La semaine IA en BD — Hugo × Iastro

## Ce qui est installé

- Une page statique FR et une page d’accueil EN sous `/knowledge-hub/comics/` et `/knowledge-hub/en/comics/`.
- Un strip de présentation clairement identifié : **aucune actualité fictive**.
- Deux kits : `kit/kits/hugo.json` et `kit/kits/iastro.json`.
- 47 PNG : 7 planches initiales, 12 expressions, 12 poses, 12 références mensuelles, 2 études de mise en scène et 2 fiches de Wang.
- Une lecture en deux colonnes sur grand écran et une colonne sur téléphone ; textes HTML accessibles, mode clair/sombre du Hub.
- Un générateur local de pages d’archives et du dernier épisode. Aucun service supplémentaire, secret ni automatisation.

## Préparer une semaine

1. Dupliquer `episodes/template.json` vers `episodes/YYYY-Www.json`, statut `draft`.
2. Choisir **4 à 7 nouvelles**, 5 par défaut. Une ouverture + 1 à 2 cases par sujet + une chute : typiquement 6 à 16 cases. Ne pas forcer 7 sujets dans 5 cases. Une semaine s’étend du lundi au dimanche, fuseau Europe/Paris.
3. Consulter les sources primaires et renseigner fait exact, titre, éditeur, URL, dates de publication et consultation. Le générateur contrôle leur présence, pas leur véracité : la vérification humaine/éditoriale reste nécessaire. Ne pas recopier les affirmations du prototype du 15 octobre sans vérification.
4. Choisir les références du mois de publication dans `kit/manifest.json`. Dessiner avec V2 + tenue, sans texte ; enregistrer dans `art/YYYY-Www/`. Les images actuelles sont opaques : ne pas les coller comme des sprites détourés.
5. Remplir les cases dans l’ordre de lecture. Les chemins `image` et `downloads` sont relatifs à `comics/`. Pour le lecteur, dimensionner les images de façon cohérente et prévoir de l’espace pour le dialogue, qui est composé séparément au-dessus de l’art.
6. Faire valider à Hugo le scénario et le dessin, puis la publication. Consigner son accord explicite dans `approval.reference` et les trois booléens. Passer à `approved` uniquement après ces accords.
7. Exécuter à la racine du dépôt :

```sh
node knowledge-hub/comics/kit/scripts/verify.mjs
python3 scripts/build_comics.py --check
python3 scripts/build_comics.py
python3 scripts/test_comics.py
```

8. Vérifier les pages sur mobile et grand écran, joindre PNG/PDF si produits (aucun faux bouton de téléchargement). Faire relire le diff et utiliser le déploiement habituel du Knowledge Hub après accord. Le script **n’envoie et ne publie rien**.

Le lien permanent affiche le dernier épisode approuvé. Partager `/knowledge-hub/comics/YYYY-Www/` pour garder un lien stable vers une semaine. Les archives sont immuables : pour corriger, créer `YYYY-Www-r2` avec `correction_note`, conserver l’ancienne version.

La page EN annonce honnêtement les épisodes disponibles seulement en français. Traduire un épisode dans un lot dédié plutôt que laisser une traduction automatique altérer un script validé.

## Vestiaire annuel

Janvier : parka et maille. Février : camel et prune. Mars : sauge. Avril : pluie jaune. Mai : lilas. Juin : lin et bleu ciel. Juillet : terracotta et bermuda. Août : écru et olive. Septembre : rentrée beige. Octobre : rouille et cape Halloween. Novembre : maille et velours. Décembre : vert et écharpe bordeaux, accessoires de Noël.

Les costumes changent ; les visages restent ceux des références validées. Le calendrier des deux personnages est détaillé dans `kit/docs/BIBLE.md`.

## Limites du premier lot

Le strip d’accueil est une étude originale de mise en scène sans dialogue, explicitement fictive. Aucun numéro d’actualité, export PDF/PNG d’épisode, cron ou envoi Telegram n’a été produit. Les 12 tenues sont des références en duo, pas une bibliothèque de toutes les poses dans chaque tenue. Produire les scènes nouvelles selon le scénario pour éviter les répétitions.

## Direction narrative et casting

Le nom est **Iastro**. Le premier lot est complété par une étude de mise en scène dans « L’atelier des possibles » et une fiche de casting d’Alexandr Wang, La mise en scène V1 est validée par Hugo ; sa variante camouflage V2 et la fiche Wang V2 sont proposées. Les V1 restent archivées. Lire la direction dans `kit/docs/DIRECTION.md` depuis comics/ ou `docs/DIRECTION.md` depuis kit/. Les 43 PNG initiaux restent disponibles et inchangés.

Le registre `cast.json` au niveau comics/ contient les invités dessinés et les candidats à préparer. Ajouter `cast_ids` à un épisode ; un invité doit avoir sa référence graphique. Pour une réplique d’un invité réel : `attribution` vaut `quote`, `paraphrase` ou `fiction` ; les deux premières exigent `source_url` parmi les sources consultées. Le lecteur affiche le type d’attribution. `layout: wide` permet à une case d’occuper toute la rangée ; le mobile garde l’ordre de lecture.

### Invités et découpage

`cast_ids` liste les identifiants de `cast.json` utilisés dans l’épisode (par défaut : `hugo`, `iastro`). Chaque invité doit avoir une référence graphique enregistrée. Pour un invité réel, chaque ligne de dialogue porte `attribution: "fiction"`, `"paraphrase"` ou `"quote"`. Les deux derniers exigent `source_url`, présente parmi les sources consultées de l’épisode ; le rendu affiche la nature de la réplique. Le contrôle vérifie la présence de la source, pas la fidélité de la citation : la relecture éditoriale reste nécessaire.

Chaque case accepte `layout: "standard"` ou `"wide"`. `wide` occupe toute la largeur disponible. Les variations de cadrage et d’expression sont produites dans les dessins ; le kit ne se limite pas à assembler des poses prédécoupées.
