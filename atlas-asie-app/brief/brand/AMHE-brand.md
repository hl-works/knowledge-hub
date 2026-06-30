# AMHE — marque (extraite du pack logo officiel)

Tokens et assets **extraits du pack de marque** (`brief/brand/AMHE/`). Complète
`brief/amhe-design.md` (système design des maquettes) avec la **vraie identité**.

## Concept

- **AMHE** = Alexis · Marion · Hugo · Emma — et jeu de mots avec « âme ».
- **Baseline officielle : « ONE LOVE ».**
- **Logo** : icône = carré arrondi contenant un **disque (soleil)** + un **cœur**
  évidé + une **ligne d'horizon** sous le soleil (= soleil couchant sur la mer +
  amour). Wordmark **« AMHE »** en capitales **condensées massives**. Baseline
  « ONE LOVE » en capitales espacées.

## Couleurs (hex officiels, samplés du pack)

| Rôle | Hex | Usage |
|------|-----|-------|
| **Orange AMHE (primaire)** | `#FA4616` | accent principal, CTA, traits du logo |
| **Pêche clair** | `#FEE3DC` | fond doux alternatif, surfaces |
| **Jaune signature** | `#F3EA5D` | « la couleur sympa » — aplats / surbrillances **uniquement** (faible contraste sur clair → jamais en texte sur fond clair) |
| **Encre / nuit** | `#0D0C12` | texte, fonds sombres (tiré du ciel de la photo) |
| **Blanc** | `#FFFFFF` | logo sur photo, négatif |

> Réconciliation avec les tokens V2 de `amhe-design.md` : remplacer
> `--coral #FF5E3A` → **`#FA4616`** (vrai orange marque) ; `--gold #FFB22E`
> reste l'or chaud des compteurs, et **ajouter `--amhe-yellow #F3EA5D`** comme
> accent signature (aplats). `--cream #FFF4E2` ↔ option `#FEE3DC` (pêche).

## Typo

- Wordmark = sans **condensé massif** → proxy web **Anton** (Google Fonts),
  déjà utilisé en V2. Corps : **Inter**.

## Assets clés (chemins)

- **Hero photo prêt à l'emploi** : `AMHE/coucher-soleil-matane-gaspesie-ciel.jpg`
  (1250×703, coucher de soleil + logo blanc centré). Full-bleed idéal pour la home.
- **Logo animé** : `AMHE/animation.gif` (91 frames, le logo se construit) +
  `AMHE/animation-black-white.gif`. Pour intro hero / loader.
- **Logo (raster haute déf, transparent)** :
  - complet : `AMHE/package_highres_ung3hjuu/base/full/base_logo_transparent_background.png`
  - icône (→ **favicon / apple-touch / og**) : `…/base/icon/base_icon_transparent_background.png`
  - wordmark seul : `…/base/text/base_textlogo_transparent_background.png`
  - variantes **blanc** (sur fond sombre/photo) : dossiers `…/black/…` (`white_*`)
  - variante orange sur pêche : `…/color1/…`
- **Vectoriels** (impression) : `AMHE/package_print_ung3hjuu/**.pdf` (+ `.eps`).
  Pas de SVG fourni → si besoin d'un logo vectoriel web, le retracer en SVG
  depuis le PDF/PNG icône.
- **Réseaux sociaux** : `AMHE/reseaux-sociaux/` (profils + couvertures FB/IG/YT).

## À produire pour le site (plus tard)

- **Favicon set** (16/32/180/192/512 + .ico) depuis l'icône.
- **OG image** depuis le hero coucher de soleil.
- Logo SVG inline (header) retracé depuis l'icône.
