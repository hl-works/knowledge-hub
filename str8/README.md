# Str8 — Posture & Training (concepts)

App perso de remise en forme / posture (cyphose structurelle, haut du dos, mobilité
thoracique, gainage). **Mobile-first, PWA hors-ligne, aucun compte / base / réseau.**
Toutes les données restent dans le navigateur (localStorage + IndexedDB).

## État : phase 1 — directions artistiques

Avant de développer l'app, 3 concepts graphiques (accueil + écran de séance réels) :

- **`/str8/concepts.html`** — page de comparaison + recommandation (point d'entrée)
- `concept-editorial.html` — **A · Editorial Sport** (revue premium, vermillon) ⭐ reco
- `concept-instrument.html` — **B · Training Instrument** (chronomètre technique, lime)
- `concept-calm.html` — **C · Calm Movement** (studio mobilité, tons naturels)

Prototypes en `noindex` (comme `landing-lab/`). HTML/CSS/JS vanilla autonome, zéro build.

## Décisions déjà tranchées

- **Stockage vidéo navigateur = jouable** : IndexedDB (Blob + `URL.createObjectURL`),
  install PWA iOS incluse, `navigator.storage.persist()` pour la durabilité. Les vraies
  vidéos filmées remplaceront plus tard les animations, sans réécrire l'app.
- **On démarre sur des animations SVG/CSS** (visibles dans les écrans de séance).
  Pas de génération auto de vidéos réalistes.
- **Stack** : app finale prévue en **vanilla PWA statique** (le repo est zéro-build ;
  Next.js/Tailwind ne rentrent pas ici). Archi média flexible : `video | gif | lottie | svg | images`.

## Prochaines étapes (après choix du concept)

1. Design system final du concept retenu
2. Données + bibliothèque des 25 exercices (`exercises.json`)
3. Écran de séance → timers → compteurs modifiables → gestion des séries
4. Couche stockage (`StorageAdapter` → `LocalStorageAdapter`), export/import JSON + CSV
5. Programme 12 semaines · routine 5 min · progrès
6. PWA (manifest, service worker, cache offline) · doc « ajouter mes propres vidéos »

## Ajouter mes propres vidéos (plus tard)

Deux voies prévues :
- **Import local** depuis Réglages → « Médias des exercices » (stocké en IndexedDB).
- **Dépôt manuel** dans `public/media/exercises/videos/` + mapping `exerciseMedia`
  (`{ type, src, poster }`). Boucles muettes de 4–8 s, plan fixe, recommandé.
