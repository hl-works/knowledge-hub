# AMHE — Référentiel design (Atlas d'Asie)

Système de design distillé des 3 maquettes (`reference/amhe-expedition.html`, `amhe-affiche.html`, `amhe-nuit.html`). **Source de vérité visuelle.** CC s'y ancre et **n'invente pas** une autre identité.

---

## 1. Le concept AMHE

**AMHE** = les initiales de la famille — **A**lexis · **M**arion · **H**ugo · **E**mma — et un jeu de mots avec **« âme »**. Le site, c'est l'**âme du voyage** de la famille. Marque chapeau du premier grand voyage, réutilisée pour celui-ci.

- Wordmark affiché : **« Atlas d'Asie »**.
- Signature/monogramme possible : **AMHE** (discret, footer ou hero), à porter comme clin d'œil identitaire.
- Ton éditorial : **carnet de voyage** (kicker type « Carnet de voyage · 2026 » / « Carnet d'expédition »), chaleureux, soigné, jamais scrapbook.

---

## 2. Colonne vertébrale commune (ce qui EST AMHE, quelle que soit la direction)

À conserver dans toutes les directions :

- **Typo de base : Inter** (corps + UI), poids 400/500/600.
- **Accent OR signature** — présent dans les 3 maquettes, c'est le fil rouge AMHE (teinte précise selon la direction, voir §3).
- **Wordmark « Atlas d'Asie »** + kicker « Carnet de voyage ».
- **Structure** : Le parcours · Les pays · compteurs (étapes, pays, jours/km).
- **Bilingue FR/EN natif** (déjà câblé dans les protos).
- **Un jeton visuel par pays** : médaillon « tampon de passeport » (V1) / mini-affiche duotone soleil-montagnes-mer (V2) / orbe duotone (V3). **Idée forte à garder** — chaque pays a son emblème généré.
- Footer : `hl-consulting.tech/atlas-asie`.

---

## 3. Les 3 directions (tokens exacts)

### V1 — Expédition cartographique
Carnet d'expédition, cartographie, sépia chaleureux. Serif à caractère.

- **Polices** : titres `Fraunces` (serif), corps `Inter`.
- **Palette** :
  - paper `#F3E7CE` · paper-2 `#ECDCBC`
  - ink `#22251F` · ink-soft `#5A5848` · muted `#8C7E63` · line `#D8C49C`
  - sea `#86A79A` · sea-deep `#3C6E60`
  - route `#C0552F` · route-deep `#8E3A1B`
  - **gold `#C2922F`**
- **Motifs** : médaillon « tampon de passeport » par pays ; tracé du parcours en **pointillés** ; texture papier ; radial-gradients très subtils.

### V2 — Affiche de voyage
Affiche vintage, typo massive, couleurs franches.

- **Polices** : display `Anton` (titres condensés massifs), corps `Inter`.
- **Palette** :
  - cream `#FFF4E2`
  - ink `#241A14` · ink-soft `#5E4B3C` · muted `#9A8268` · line `#EAD7BC`
  - coral `#FF5E3A` · coral-deep `#D83E1E`
  - jade `#149E7C` · teal `#0C5A5E`
  - **gold `#FFB22E`**
- **Motifs** : mini-affiche **SVG par pays** (soleil + montagnes + mer en duotone propre au pays) ; grandes typos.

### V3 — Cinématique nuit
Nocturne, immersif, glassmorphism, néons.

- **Polices** : display `Space Grotesk`, corps `Inter`.
- **Palette** :
  - bg `#0A0E1F` · bg-2 `#0F1530`
  - surface `rgba(255,255,255,.055)` · surface-line `rgba(255,255,255,.12)`
  - text `#ECECF6` · text-soft `#AEB2CC` · muted `#7B7FA0`
  - magenta `#E8568F` · magenta-deep `#B43A6E`
  - cyan `#46D8C8` · indigo `#6C7BFF`
  - **gold `#F4C95D`**
- **Motifs** : gradients néon (radial indigo/magenta), **orbe duotone** par pays (radial cyan→magenta), cartes en verre dépoli.

---

## 4. Animations

Les protos sont **sobres** : pas de `@keyframes`, surtout des transitions au survol (`transform`, `box-shadow`, `border-color`, ~.18–.25s ease). Tous respectent `prefers-reduced-motion` (animations coupées). **Garder cette retenue** : micro-interactions au survol + révélations douces au scroll, pas d'animation tape-à-l'œil.

---

## 5. Do / Don't

**Do**
- Photo **full-bleed** qui mène la page.
- Garder l'**accent or** comme signature.
- Un **jeton/emblème par pays** (médaillon, affiche ou orbe selon la direction).
- Ton **carnet de voyage**, éditorial, bilingue.
- Sobriété des animations (survol + reveal doux).

**Don't**
- Pas de scrapbook / stickers.
- Pas de surcharge d'effets.
- Ne pas réutiliser les **données fixtures** des maquettes (Thaïlande/Vietnam/Angkor) : **les vraies données sont dans `parcours.csv` / `pays.csv` / `quiz.csv`** (Kazakhstan → Indonésie, 26 escales).

---

## 6. Comment t'en servir (CC)

1. Reconstituer la **colonne vertébrale commune** (§2) en variables CSS réutilisables.
2. Implémenter la **direction retenue** (§3) comme thème principal — Hugo a déjà fait son choix.
3. Garder les deux autres comme **inspiration** (motifs, jetons par pays) sans les mélanger.
4. Proposer si besoin **2-3 variations à l'intérieur de la direction retenue**, toutes fidèles à cet ADN AMHE.
