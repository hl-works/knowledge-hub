# La semaine IA en BD — Hugo × Iastro

## Ce qui est installé

- Une page statique FR et une page d’accueil EN sous `/knowledge-hub/comics/` et `/knowledge-hub/en/comics/`.
- Un strip de présentation clairement identifié : **aucune actualité fictive**.
- Deux kits : `kit/kits/hugo.json` et `kit/kits/iastro.json`.
- 47 PNG : 7 planches initiales, 12 expressions, 12 poses, 12 références mensuelles, 2 études de mise en scène et 2 fiches de Wang.
- Un lecteur mobile : une case par swipe, boutons précédent/suivant et mode vertical ; textes HTML agrandissables et mode clair/sombre. Le format historique reste disponible.
- Un générateur local de pages d’archives et du dernier épisode. Aucun service supplémentaire, secret ni automatisation.

## Préparer une semaine

1. Dupliquer `episodes/template.json` vers `episodes/YYYY-Www.json`, statut `draft`.
2. Choisir **4 à 7 nouvelles**, 5 par défaut. Chaque info devient une histoire de 5 ou 6 cases. Le pilote comporte 4 histoires × 6 cases, soit 24 cases. Une semaine s’étend du lundi au dimanche, fuseau Europe/Paris.
3. Consulter les sources primaires et renseigner fait exact, titre, éditeur, URL, dates de publication et consultation. Le générateur contrôle leur présence, pas leur véracité : la vérification humaine/éditoriale reste nécessaire. Ne pas recopier les affirmations du prototype du 15 octobre sans vérification.
4. Choisir les références du mois de fin de la semaine racontée dans `kit/manifest.json`. Dessiner avec V2 + tenue, sans texte ; enregistrer dans `art/YYYY-Www/`. Les images actuelles sont opaques : ne pas les coller comme des sprites détourés.
5. Remplir les cases dans l’ordre de lecture. Les chemins `image` et `downloads` sont relatifs à `comics/`. Pour le lecteur, dimensionner les images de façon cohérente et prévoir de l’espace pour le dialogue, qui est composé séparément sous l’art à 18 px minimum.
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

Le strip d’accueil est une étude originale de mise en scène sans dialogue, explicitement fictive. Un pilote rétrospectif du 5–11 octobre est préparé en brouillon : quatre histoires et 24 cases. Aucun épisode n’est approuvé pour publication ; aucun cron ni envoi Telegram. Les 12 tenues sont des références en duo, pas une bibliothèque de toutes les poses dans chaque tenue. Produire les scènes nouvelles selon le scénario pour éviter les répétitions.

## Direction narrative et casting

Le nom est **Iastro**. Le premier lot est complété par une étude de mise en scène dans « L’atelier des possibles » et une fiche de casting d’Alexandr Wang, La mise en scène V1 est validée par Hugo ; sa variante camouflage V2 et la fiche Wang V2 sont proposées. Les V1 restent archivées. Lire la direction dans `kit/docs/DIRECTION.md` depuis comics/ ou `docs/DIRECTION.md` depuis kit/. Les 43 PNG initiaux restent disponibles et inchangés.

Le registre `cast.json` au niveau comics/ contient les invités dessinés et les candidats à préparer. Ajouter `cast_ids` à un épisode ; un invité doit avoir sa référence graphique. Pour une réplique d’un invité réel : `attribution` vaut `quote`, `paraphrase` ou `fiction` ; les deux premières exigent `source_url` parmi les sources consultées. Le lecteur affiche le type d’attribution. `layout: wide` permet à une case d’occuper toute la rangée ; le mobile garde l’ordre de lecture.

### Invités et découpage

`cast_ids` liste les identifiants de `cast.json` utilisés dans l’épisode (par défaut : `hugo`, `iastro`). Chaque invité doit avoir une référence graphique enregistrée. Pour un invité réel, chaque ligne de dialogue porte `attribution: "fiction"`, `"paraphrase"` ou `"quote"`. Les deux derniers exigent `source_url`, présente parmi les sources consultées de l’épisode ; le rendu affiche la nature de la réplique. Le contrôle vérifie la présence de la source, pas la fidélité de la citation : la relecture éditoriale reste nécessaire.

Chaque case accepte `layout: "standard"` ou `"wide"`. `wide` occupe toute la largeur disponible. Les variations de cadrage et d’expression sont produites dans les dessins ; le kit ne se limite pas à assembler des poses prédécoupées.

## Pilote mobile — semaine du 5 au 11 octobre 2026

Source : `episodes/2026-W41.json`. Quatre histoires de six cases : GPT-6/Intelligent UI, Haiku 5.5, Mistral Large 4 et SynthID. Sources primaires et arbitrages : `drafts/2026-W41/SOURCES.md`. La date de préparation est le 16 octobre ; la période racontée reste le 5–11 octobre.

```sh
python3 scripts/build_comics.py --preview 2026-W41
```

Cette commande vérifie le contenu et les images, puis rend seulement `drafts/2026-W41/` (FR et accueil EN signalant que la BD est en français), avec `noindex,nofollow`. Elle ne touche pas `latest.json` ni les archives publiées. Le générateur normal ignore les brouillons.

`format: "webtoon"` active le lecteur mobile. Chaque sujet regroupe 5 ou 6 cases contiguës. Les fichiers maîtres illustrés contiennent une grille de six cases ; `crop` décrit la fenêtre normalisée `{x,y,w,h}` de chaque case. Le navigateur affiche la fenêtre sans modifier les pixels du maître. Le texte est HTML, jamais gravé dans l’image. Revoir les séparations après chaque nouvelle génération. Le lecteur reste entièrement vertical sans JavaScript.

`backlog.json` inventorie huit semaines à partir du 17 août, avec des candidats issus de la veille. Ce sont des pistes non vérifiées, pas des comics publiés ou programmés. Attendre le retour de Hugo sur le pilote avant de produire la rétrospective.

## Reprise du 16 octobre — navigation et archives

Le pilote comprend désormais 28 écrans : 4 ouvertures explicatives et 24 cases dessinées. Le sommaire et la lecture sont deux vues distinctes, avec liens directs, retour navigateur, progression par histoire et mode vertical.

La rubrique Immersion IA (`../immersion-ia/`) rassemble veille, podcasts et IA immersion BD. Elle est préparée dans la branche, non déployée. La sélection des huit semaines est dans `editorial-plan.json` et sa vue de relecture dans `drafts/planning/` : 32 pistes d’après les archives, non encore vérifiées au niveau des sources primaires et non dessinées sauf le pilote W41.

Recette locale : 28 écrans parcourus, quatre accès directs à 320 px sans débordement, retour navigateur et trois bascules vertical/swipe conservant la case 8. Les 10 MP3 des cinq éditions du 12 au 16 octobre sont décodables et leurs durées concordent avec les manifestes. 12 tests du générateur et contrôle de cohérence du site passent. La validation éditoriale des rétrospectives et la publication restent à faire.


## Mise en production autorisée — 16 octobre 2026

Hugo demande explicitement la mise en production de la version présentée. Le numéro 2026-W41 est approuvé et publié sous `/knowledge-hub/comics/2026-W41/`, référencé par `latest.json`, le sommaire, le moteur de recherche et le sitemap. Les anciennes adresses du pilote redirigent vers ce numéro. Le Kiosque IA réunit Le Radar iA, Le Podcast iA et iAstro Sunday. Les paragraphes de préparation ci-dessus décrivent l’historique ; ils ne remplacent pas cet état. Les rétrospectives restent des pistes non publiées.

Apple Podcasts, Spotify et le flux RSS podcast constituent le prochain lot : aucun compte ouvert ni distribution activée ici.

## Navigation mobile — 17 octobre 2026

Le lecteur conserve le swipe et la lecture verticale. Son sommaire utilise des cartes sur une colonne, un départ explicite et une reprise de la case en cours (pendant la visite). Les commandes précédent/suivant restent en bas de l’écran, avec une progression par histoire. Le changement d’histoire et la fin du numéro sont annoncés explicitement. Le mode vertical conserve la position et met à jour le lien de la case.

Une mise à jour technique du lecteur peut désormais utiliser `python3 scripts/build_comics.py --refresh-reader`. Elle exige que l’empreinte SHA-256 des données éditoriales soit identique à celle de l’archive publiée. Toute modification du scénario, des sources, des images référencées ou de l’approbation exige toujours une nouvelle révision. Pour le numéro W41 existant, l’empreinte a été ajoutée après vérification de l’identité entre le HTML publié et son générateur d’origine. Aucun dessin ni dialogue n’a changé.

## Publication des trois semaines — 17 octobre 2026

Hugo autorise explicitement la production des trois numéros W39, W40 et W41-r2 après leur présentation. Les manifestes portent son accord éditorial, graphique et de publication. La collection publique `/knowledge-hub/comics/` présente une seule version par semaine, la révision approuvée la plus récente, classée par période couverte. Le dernier numéro est W41-r2, même si des rétrospectives sont préparées après lui.

Chaque numéro propose « Tous les numéros », un choix de semaine par dates et des liens semaine précédente/suivante. Le Kiosque affiche aussi les trois périodes. W41 original conserve ses dessins et textes ; seule sa navigation est actualisée, avec un lien vers W41-r2. Les anciennes adresses de prévisualisation redirigent vers les éditions publiées.

Reconstruction : `python3 scripts/build_comics.py --refresh-reader`, puis `python3 scripts/build_immersion.py`. La première commande ne peut modifier l’éditorial d’une archive : son empreinte doit rester identique. Les archives, le catalogue et les liens sont générés par `scripts/comics_catalog.py`. Vérifications : `python3 scripts/test_comics.py`, `python3 scripts/build_comics.py --check`, `python3 scripts/check_site_health.py`.

Retour arrière : rétablir le précédent commit de déploiement par un revert Git, sans force-push. Ne pas écraser les anciens dessins ni les épisodes. Les liens permanents déjà partagés doivent rester utilisables.


## Édition du 18 octobre 2026 — W42

Hugo a autorisé la préparation et la publication de cette édition, puis un push
Telegram avec une couverture et le lien direct mobile. Le suivi ponctuel du
18 octobre reprend cette instruction explicite ; les restrictions antérieures
sur la publication sans accord ne bloquent pas ce numéro autorisé.
Quatre histoires originales de six cases : GPT-6 Pro/agents parallèles, Shop MCP,
Muse Spark Open, SPACE. Sources primaires consultées le 18 octobre, sélection
arrêtée à 7 h (Europe/Paris). Les annonces postérieures à cette coupure ne sont
pas couvertes. Textes, dessins et contrôles sont consignés dans le manifeste
W42 et art/2026-W42/production.json. Aucun changement des voix du podcast.

Le push utilise le bot existant de hl-works/veille-ia, workflow manuel
iastro-sunday-w42.yml (PR 17), avec vérification publique, réservation durable
avant envoi et reçu contenant le message ID. Un résultat ambigu ne doit jamais
être rejoué automatiquement. Le prochain numéro nécessitera sa propre autorisation.
