# Str8 — l'app (v0.1)

App perso de **posture & renforcement**. Mobile-first, **PWA hors-ligne**, aucun compte,
aucune base, aucun serveur. Toutes les données restent **sur l'appareil** (localStorage).

Concept retenu : **Training Instrument** (charbon + lime). Illustrations : **blueprint SVG**.

## Lancer

Site statique, zéro build. En local :

```bash
cd str8/app && python3 -m http.server 8000
# → http://localhost:8000/
```

En prod : `hl-consulting.tech/str8/app/` (GitHub Pages). Sur iPhone : Safari → Partager →
« Sur l'écran d'accueil » pour l'installer en PWA.

## Ce qu'il y a

- **Accueil** : séance recommandée du jour, régularité, série de semaines, routine 5 min, log course/marche.
- **Séance** : média blueprint + consigne + erreurs, **séries** (points), **compteur reps −/+** (mémorisé),
  **timer** pour les maintiens (démarrer/pause/±10 s), **repos auto**, variante plus simple, bouton douleur.
- **Routine 5 min** : enchaînement chronométré.
- **Exercices** : bibliothèque des **25 mouvements** (objectif, consignes, erreurs, variantes, réglages mémorisés).
- **Progrès** : séances/semaine, minutes, série de semaines, 6 dernières semaines, historique, gênes signalées.
- **Réglages** : profil éditable, préférences (repos auto, vibration, son), **export/import JSON**,
  **export CSV**, réinitialisation. Disclaimer sécurité au 1er lancement.

## Fichiers

```
index.html   shell SPA            data.js    profil + 25 exos + séances A/B/C + routine + programme 12 sem
style.css    design system        media.js   médias blueprint (SVG schématiques par pattern)
app.js       routeur + logique    store.js   StorageAdapter → LocalStorageAdapter
sw.js        service worker       manifest.webmanifest · icon.svg
```

La couche `store.js` est abstraite : on pourra brancher une base distante un jour sans réécrire l'app.

## Ajouter mes propres vidéos (plus tard)

Les démonstrations actuelles sont des **repères SVG**, faits pour être remplacés par de vraies vidéos.
Le plus propre : filmer chaque mouvement en **plan fixe**, produire des **boucles de 4–8 s, sans son**.

1. Dépose tes fichiers dans `str8/app/media-video/` (ex. `band-pull-apart.mp4`, + `posters/band-pull-apart.webp`).
2. Mappe-les dans un objet simple (à ajouter dans `media.js`) :

```js
const exerciseVideo = {
  'band-pull-apart': { type:'video', src:'media-video/band-pull-apart.mp4', poster:'media-video/posters/band-pull-apart.webp' },
};
```

3. Le rendu du média (`media(ex.media)`) lira d'abord `exerciseVideo[ex.id]` s'il existe, sinon le SVG.

**Import direct depuis l'appareil** (stockage IndexedDB du Blob) : prévu, non inclus en v0.1.
Techniquement OK sur iOS (Blob + `URL.createObjectURL`), avec `navigator.storage.persist()` pour la durabilité —
pense quand même à **exporter ta sauvegarde JSON** régulièrement.

## À faire ensuite

- Rendu vidéo/GIF dans le média (mapping ci-dessus) + import local IndexedDB.
- Poses départ/arrivée animées par exo · affiner certains blueprints.
- Progression 12 semaines plus fine (montée de charge guidée).
- Icônes PNG pour un rendu d'install iOS parfait (l'icône est en SVG pour l'instant).
