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

- Onglets publiés en CSV et lus par le site : **`Parcours`**, **`Pays`**, **`Quiz`**, **`Bestiaire`**, **`Lexique`**, **`Transports`**, **`Pratique`**, **`Aeroports`**, **`Lieux`**, **`Miam`**, **`Recits`**.
- **NE JAMAIS lire, publier ni afficher** les onglets **`Passeport`** (numéros de passeport en clair) ni **`Financier`** (budget). Aucune donnée personnelle sensible ne doit toucher le site, ni en build ni en runtime.
- **Références de réservation** (numéros Trip.com/Booking) : sensibles aussi (résa accessible avec réf + nom). Elles restent dans l'onglet Vols privé, **jamais publiées**. L'onglet `Transports` du site n'en contient pas.
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

### Onglet `Bestiaire` (une ligne par animal)

`pays` · `animal` · `ou_voir` · `fait` · `photo_query`

- ~3 animaux par pays, calés sur le focus nature du voyage. Affiché en bloc « Animaux à repérer » sur la fiche Pays. Photo via `photo_query` (fallback Pexels).

### Onglet `Lexique` (une ligne par mot)

`langue` · `pays` · `francais` · `mot_local` · `prononciation`

- 20 mots essentiels par langue. `pays` peut lister plusieurs pays (ex. le russe sert pour `Kazakhstan, Kirghizistan`) → CC éclate sur la virgule pour mapper langue → pays. Affiché en bloc « Mots à connaître » sur la fiche Pays.

### Onglet `Pratique` (une ligne par pays — le « Routard de poche »)

`pays` · `visa` · `formalites` · `argent` · `budget_repere` · `prises` · `internet` · `apps` · `eau` · `pourboire` · `do_dont` · `urgences` · `decalage`

- Bloc **« À l'arrivée »** affiché sur la fiche Pays (accordéon ou cartes par thème avec icônes : 💳 argent, 🔌 prises, 📶 internet, 🚕 apps, 💧 eau, 🙏 coutumes, 🆘 urgences, 🕐 décalage). Ton vivant, calibré famille.
- Infos vérifiées au 01/07/2026 (visas, formalités digitales). Les règles bougent : re-vérifier sur diplomatie.gouv.fr avant chaque frontière.

### Onglet `Transports` (une ligne par trajet)

`ordre` · `date` · `type` (Avion / Bus / Bateau) · `de` · `depart_h` · `vers` · `arrivee_h` · `compagnie` · `vol` · `statut` (Réservé / À trouver)

- Une ligne = un trajet entre deux escales. Pas de référence de réservation (cf. règle de sécurité). Alimente la page « Les trajets » ; on peut aussi rattacher le trajet correspondant à chaque escale du Parcours (par date).

### Onglet `Lieux` (une ligne par incontournable — le « à voir » du Routard)

`ordre` (référence à l'escale du Parcours) · `pays` · `lieu` · `statut` (ex. « UNESCO 1987 », vide sinon) · `texte` · `photo_query`

- Affiché en bloc **« À voir »** sur chaque escale de la page Le Parcours (2-4 lieux par grande escale ; les escales de transit n'en ont pas → ne rien afficher). Badge visuel pour le statut UNESCO.

### Onglet `Miam` (une ligne par plat — la gastronomie)

`pays` · `plat` · `nom_local` · `description` · `photo_query`

- ~5 plats par pays. Affiché en bloc **« Miam »** sur la fiche Pays (cartes avec photo libre de droits via `photo_query`).

### Onglet `Recits` (une ligne par grande histoire — « de quoi lire »)

`pays` (peut lister plusieurs pays, séparés par virgule) · `titre` · `accroche` · `texte` (long, 200-300 mots) · `photo_query`

- Les textes longs du site : Gengis Khan, la Route de la Soie, la Grande Muraille, la route des épices, la ceinture de feu… Affichés en **« La grande histoire »** sur la fiche Pays (accroche + « Lire la suite » qui déplie, typographie généreuse type mode lecture, Fraunces).

### Onglet `Aeroports` (une ligne par aéroport — référentiel taxi)

`code` · `ville` · `pays` · `nom_en` · `nom_local` · `adresse_en`

- `code` = IATA (ALA, PEK, PKX…), la clé : les champs `de`/`vers` de `Transports` le contiennent (« Pékin PKX (Daxing) ») et la page Trajets fait la jointure dessus.
- `nom_local` = l'écriture locale (中文, кириллица…) : c'est ce qu'on montre au chauffeur ou qu'on colle dans DiDi ; le bouton « Copier » copie cette valeur.
- Rendu : bloc dépliant « Aéroports & taxi » sous chaque vol (nom EN + adresse EN + nom local en grand + boutons Carte / Copier).

## Pages (V1)

1. **Accueil** — hero plein cadre (photo ou vidéo), titre du voyage, **carte animée du parcours**, **bloc Live** ("Jour X · on est à [escale] · prochaine étape [ville] dans N jours" + mini compte à rebours), et **compteurs animés** (pays visités, vols pris, nuits, km parcourus, plus haut sommet) — tout calculé depuis le Parcours.
2. **Le Parcours** — timeline verticale des escales. Pour chaque escale : pays, ville, dates, **hôtel mis en avant** (nom, photo, adresse, lien), statut visuel (passé / en cours / à venir), photos + vidéo, et la **météo du lieu** (voir section Météo). C'est LA page que les grands-parents ouvrent.
3. **Les Pays** — une fiche par pays : grande photo, capitale, monnaie, langue, population, histoire, fun facts, un bloc **« À l'arrivée »** (Pratique : visa, formalités, argent, prises, internet, apps, coutumes, urgences), un bloc **« Animaux à repérer »** (Bestiaire), un bloc **« Mots à connaître »** (Lexique, 20 mots avec écriture locale + prononciation), et **un mini-quiz en bas de fiche**. Éducatif, lisible par un enfant, pensé pour un duel Alexis/Emma.
4. **Le Carnet** — feed **Instagram** (reels + posts) via widget **Behold.so**. Réutilisable en bandeau sur d'autres pages.
5. **Galerie** — agrège **toutes les photos/vidéos du champ `photos` des escales** (source unique = la sheet, pas de double saisie). Grille graphique, lightbox.
6. **Nos hôtels** — liste chronologique propre de tous les hébergements (lue depuis le Parcours) : escale, dates, nom de l'hôtel, **adresse**, lien de réservation, statut de confirmation, et **bouton « Voir sur le plan »** (ouvre Google/Apple Maps via `lat`/`lng`). Pensée pour que la famille **et les grands-parents** suivent facilement où on dort. C'est une vue dédiée, distincte de la timeline du Parcours.
7. **Les trajets** — pense-bête transport (lu depuis `Transports`) : liste chronologique de tous les vols/bus/bateaux avec date, trajet, horaires, compagnie, n° de vol et **statut de résa** (voir d'un coup d'œil ce qui est encore « à trouver »). Sans références de réservation.

**Carte animée** (Leaflet ou MapLibre) : le tracé relie les escales dans l'ordre et s'allume selon le statut — passé en plein, escale en cours qui pulse, futur en pointillé. Élément signature du site.

## Univers graphique — AMHE

L'identité visuelle vient d'**AMHE** (initiales A·M·H·E + jeu de mots avec « âme »), la marque du premier grand voyage de la famille.

- **Source de vérité = `brief/amhe-design.md`** : le système de design distillé (concept, colonne vertébrale commune, 3 directions avec tokens exacts, do/don't).
- **Maquettes de référence** dans `brief/reference/` : `amhe-expedition.html`, `amhe-affiche.html`, `amhe-nuit.html`.
- CC reconstitue la colonne vertébrale commune en variables CSS, implémente la **direction retenue par Hugo** comme thème principal, et **n'invente pas** une autre identité.
- ⚠️ Les **données dans les maquettes sont des fixtures bidon** (Thaïlande/Vietnam/Angkor) : les vraies données sont dans `parcours.csv` / `pays.csv` / `quiz.csv`.
- Contraintes **structurelles** : photo full-bleed, beaucoup d'air, hiérarchie typo claire, mobile-first, grandes zones tactiles, perf (Lighthouse vert), animations sobres (`prefers-reduced-motion` respecté).

## UI/UX

- **Navigation mobile = barre d'onglets en bas** (Accueil · Parcours · Pays · Hôtels · « + » pour Carnet/Galerie/Trajets), pas de menu burger. Utilisateurs : enfants et grands-parents, au pouce.
- **Skeleton loaders obligatoires** : les CSV sont fetchés côté client → prévoir des squelettes élégants pendant le chargement, jamais de page blanche ni de saut de layout.
- **Cache local de la dernière donnée chargée** (localStorage) : si pas de réseau (bus en Mongolie…), le site affiche les dernières données connues avec un indicateur discret « hors ligne ».
- **PWA légère** : manifest + icônes pour « Ajouter à l'écran d'accueil ». Le site doit se vivre comme une app.
- **Hors-ligne complet** (sw.js v3) : le service worker précache les 7 pages + tous les CSV/photos.json à l'installation, et met en cache au fil de l'eau tout ce qui passe (CSS/JS, images Commons en CORS, URLs Google Sheets publiées). Une visite de l'accueil avec du réseau suffit ; ensuite le site entier se consulte sans connexion (données = dernière version connue). Penser à bumper `CACHE = 'atlas-asie-vN'` à chaque évolution du SW.
- **Accueil à états selon la phase du voyage** : avant le 04/07 = compte à rebours ; pendant = bloc Live ; après le 27/08 = récap (compteurs finaux, carte complète).
- **Signature visuelle** : l'audace se dépense sur les éléments AMHE distinctifs (jetons par pays, tampons, tracé pointillé de la carte) — le reste reste sobre et discipliné. Éviter que la base « crème + serif + accent chaud » ressemble à un template générique : c'est la signature qui différencie.
- **Groupage par pays** : les listes (Hôtels, Parcours, Galerie) sont sectionnées par pays via `paysHead()` (`src/lib/paysMeta.ts`, source unique palette/codes — miroir Python dans `scripts/build_atlas_static.py`). Chaque en-tête contient un **`.stamp-slot`** : l'emplacement réservé au futur tampon AMHE du pays (placeholder = code pays dans un rond pointillé, à remplacer quand le design des tampons est prêt).

## Partage, SEO & GEO

- **Priorité n°1 : Open Graph** — le site sera partagé sur WhatsApp (grands-parents). Chaque page a `og:title`, `og:description` et une **belle `og:image`** (l'accueil : visuel AMHE du voyage). Tester le rendu du lien partagé.
- **SEO + GEO en place depuis juillet 2026** (décision Hugo, remplace l'ancien « pas de GEO ») : **lire `GUIDE-EVERGREEN.md`** avant de toucher au contenu Pays ou au head des pages. Pipeline : `scripts/build_atlas_static.py` (rendu statique pays/parcours pour crawlers sans JS + `sitemap.xml` + `llms.txt`), relancé par le workflow `site-autobuild.yml` (push + cron quotidien).
- Le head SEO (canonical, OG, JSON-LD avec le `@id` canonique `https://hl-consulting.tech/#hugo`) vit dans `src/layouts/Base.astro`.
- ⚠️ Un `npm run build` purge `../atlas-asie/` (blocs statiques, sitemap, llms.txt compris) : normal, le workflow réinjecte au push ; en local relancer `python3 scripts/build_atlas_static.py` après un build.

## i18n

Site **monolingue FR** (décision juin 2026 : pas de version EN, une coquille EN
autour d'une Sheet FR ne vaut rien). La config i18n d'Astro reste en place dans
`astro.config.mjs` pour pouvoir ajouter l'EN plus tard sans refactor — mais pas
de page `/en/`, pas de hreflang, pas de toggle de langue tant qu'il n'y a pas de
vraies données EN (voir `GUIDE-EVERGREEN.md` §5).

## Données pas à jour (procédure Claude — pendant le voyage)

Tant que les URLs CSV publiées ne sont pas branchées dans `sheets.ts`, la
source de vérité est `public/fixtures/*.csv`. **Quand Hugo demande de changer
une donnée** (« l'hôtel de l'escale 12 a changé », « décale les dates de
Lombok »…) : éditer la fixture concernée, rebuild + statique, prod. Après la
bascule Sheet, ces demandes se font dans la Sheet — sauf les coordonnées :
la Sheet n'a que des noms de villes, les `lat`/`lng` viennent du référentiel
bundlé `src/lib/coords.json` (jointure par `ordre`, une valeur présente dans
la Sheet gagne). Nouvelle escale ou escale déplacée → mettre à jour
`coords.json` **et** régénérer.

## Ajouter les photos du voyage (procédure Claude — pendant le voyage)

Le site fusionne deux sources de photos par escale : la colonne `photos` de la
Sheet (URLs) **et** les photos committées dans le repo
(`atlas-asie-app/public/photos/<ordre>/NN.jpg` + `public/photos/manifest.json`).
Le repo est la voie recommandée : URLs stables, servies par le site, hors ligne.

**Quand Hugo envoie des photos dans une conversation avec un n° ou un nom
d'escale** (ex. « escale 12 » ou « Bichkek : ces 3 photos, légende … ») :

1. Retrouver l'`ordre` de l'escale dans `public/fixtures/parcours.csv` si Hugo
   donne un nom de ville.
2. Photos : `node scripts/add-photos.mjs <ordre> [--legende "…"] <fichiers>` —
   redimensionne (1600 px, WebP q78, ~150-300 Ko), range et met à jour le
   manifest. Une légende différente par photo → un appel par photo.
   Vidéos : `node scripts/add-video.mjs <ordre> [--legende "…"] <fichier>` —
   H.264 720p CRF 27 + AAC + poster WebP, rendue en <video> sur l'escale
   (pas dans la Galerie). ⚠️ ffmpeg complet requis :
   `apt-get update && apt-get install -y ffmpeg` (celui de Playwright n'a ni
   H.264 ni audio). Viser des clips courts (< 60 s / < 25 Mo, le script
   avertit au-delà).
   **Limites de poids** : pièces jointes Claude ~30 Mo par fichier ; GitHub
   100 Mo max par fichier ; GitHub Pages ~1 Go pour tout le site → photos
   quasi illimitées, vidéos avec parcimonie (garder les meilleures).
3. Rebuild : `cd atlas-asie-app && npm run build` puis
   `python3 scripts/build_atlas_static.py` (le build purge `atlas-asie/`).
4. Commit + passage en prod (`content(atlas): photos escale <ordre> — <ville>`).

Les photos apparaissent automatiquement sur **l'escale du Parcours** et dans la
**Galerie** (groupée par pays, légende affichée). Pas de page d'upload sur le
site : statique sans back, c'est Claude le guichet.

## Médias & photos

Stratégie photo à deux niveaux, pour avoir un max de belles images sans coller d'URLs à la main :

1. **Photo perso prioritaire** — si un champ photo (`hotel_photo`, `photos`, `photo_hero`) contient une URL dans la sheet, on l'affiche. Les photos du voyage passent toujours devant.
2. **Fallback libre de droits via Wikimedia Commons** — `scripts/resolve_photos_commons.py` résout une fois pour toutes chaque `photo_query` (Lieux, Miam, Recits, Bestiaire) en image libre (CC / domaine public) dans `public/fixtures/photos.json` ; le site lit ce mapping statique (zéro appel API au runtime, hotlink officiellement autorisé, crédit dans le `title` de chaque image + mention sur la page). Relancer le script quand des `photo_query` changent. (L'option Pexels du brief d'origine nécessitait une clé API ; Commons n'en demande pas.)

> **Photos d'hôtels** : pas de récup auto depuis Booking (aucune API publique, scraping fragile et contraire aux CGU). Pour montrer le *vrai* hôtel, Hugo colle une URL dans `hotel_photo` (à réserver aux hôtels qui comptent). Sinon, fallback Pexels sur le nom de la ville.

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
6. Page **Le Carnet** (widget Insta Behold) + page **Galerie** (agrège les photos du Parcours) + page **Nos hôtels** (liste + clic-vers-le-plan).
7. Direction artistique / polish.

> Avant de coder une étape : énoncer le plan court et le critère de "c'est bon". Modifications chirurgicales, simplicité d'abord. Demander si ambigu (une question à la fois).
