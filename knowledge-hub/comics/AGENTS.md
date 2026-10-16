# Comics : Hugo × Iastro

Lire `README.md`, `kit/AGENTS.md`, `kit/docs/BIBLE.md`, `kit/manifest.json` et le manifeste de personnage pertinent sous `kit/kits/`. Le nom public est Iastro. Ne pas réinventer les visages ni remplacer le garçon par un robot à écran.

Cadence hebdomadaire, 4 à 7 grandes actualités (5 par défaut). Source primaire consultée pour chaque fait. La date de l’épisode détermine le vestiaire ; une tenue différente par mois. Références mensuelles en duo, PNG opaques.

Séparer le texte des illustrations. Faire vérifier les scènes nouvelles et le contenu. Aucun brouillon ne devient un épisode publié sans accord explicite de Hugo. Les champs d’approbation documentent cet accord, ils ne le remplacent pas. Ne pas les remplir à sa place.

Les pages HTML sont générées par `scripts/build_comics.py` à la racine du dépôt. Le script ne déploie rien. Ne pas écraser une archive publiée : correction dans un nouvel épisode avec une note visible. Ne pas ajouter de cron sans demande explicite.

### Orientation des têtes et des regards — correction de Hugo, 16 octobre 2026

La tête droite est la pose de référence pour Hugo et Iastro : axe du visage vertical, ligne des yeux horizontale et cou naturel. Prévoir des vues franchement de face, avec regard direct vers le lecteur, ainsi que des trois-quarts tête droite et des regards vers l’interlocuteur. Varier la direction du regard indépendamment de l’inclinaison de la tête.

Réserver une tête penchée à une intention précise (doute, écoute, surprise), occasionnellement. Ne pas recopier systématiquement l’inclinaison des anciennes fiches : elles fixent l’identité, pas une posture obligatoire. Vérifier la diversité des orientations sur l’ensemble de la planche. Cette correction concerne les prochaines illustrations ; elle ne signifie pas que les PNG déjà livrés ont été redessinés.

## Mise à jour de direction — Iastro et casting ouvert

Le nom choisi est **Iastro**. Lire la direction graphique `kit/docs/DIRECTION.md` depuis comics/ (`docs/DIRECTION.md` depuis kit/). Les personnages réels de l’actualité sont désormais autorisés par Hugo : la restriction initiale est remplacée. Le registre `cast.json` au niveau comics/ décrit références, rôles vérifiés et états de préparation. Une scène doit s’appuyer sur les fiches de tous ses personnages. Les citations réelles sont sourcées ; les répliques inventées attribuées aux invités doivent être clairement identifiées comme fiction, sans inventer d’annonce ou de conduite réelle.

La tête droite est une base, pas une immobilité : exploiter bouches largement ouvertes, profils, pleines faces, trois-quarts, gros plans, vues lointaines et silhouettes en action. Les références sont un modèle d’identité ; ne pas assembler systématiquement les vignettes anciennes comme un diaporama. Préférer des scènes nouvelles et une mise en page dont le rythme sert le scénario.

Pour les invités, vérifier le look récent en plus du rôle actuel. Le Wang de référence doit désormais suivre Meta Connect 2026 (camouflage avec cerf, lunettes fines, cheveux bouclés longs à la nuque, Crocs camouflage), pas le look chemise bleue de Scale. Conserver les versions anciennes sans les présenter comme actuelles.

## Priorité mobile — demande du 16 octobre 2026

99 % de lecture prévue sur téléphone. Une info = une histoire de 5 ou 6 cases, et une case affichée à la fois en swipe, avec lecture verticale disponible. Cette consigne remplace le format initial d’une ou deux cases par nouvelle. Dialogues courts en HTML à au moins 18 px ; ne pas réduire une planche entière pour la faire tenir dans la largeur mobile. Conserver le dessin de L’atelier des possibles, les variations de cadrage et les tenues du mois.

Valider d’abord le pilote de la semaine du 5 au 11 octobre. Le rattrapage des semaines d’août/septembre vient après ce retour ; l’inventaire ne vaut ni validation ni automatisation.

## Humour et repères de marque — retour de Hugo du 16 octobre 2026

L’approche du pilote est approuvée. Cela ne vaut pas validation de publication. Les blagues doivent se comprendre immédiatement avec la scène : une chute concrète, des répliques courtes, sans détour technique ni référence obscure. Le dessin et le dialogue doivent raconter la même blague.

Ajouter de petits logos officiels quand une entreprise, un modèle ou un outil est évoqué (OpenAI, Anthropic, etc.). Accompagner le logo du nom de la marque et du modèle : un symbole seul n’est pas assez explicite. Utiliser les fichiers locaux de brands/ et documenter leur source ; conserver proportions et couleurs. Garder ces repères discrets et lisibles sur téléphone, séparés des illustrations pour permettre les corrections.

## Une ouverture explicative par histoire — retour de Hugo du 16 octobre 2026

Commencer chaque sujet par une case numéro 1 : logo officiel plus grand, nom de la marque et du modèle, titre explicite et résumé très court en français simple. Le lecteur doit comprendre l’annonce avant les métaphores et les blagues. Conserver les limites essentielles de l’annonce. Puis dérouler les cases dessinées, avec petits repères de marque. Cette ouverture s’ajoute aux 5 ou 6 cases dessinées ; le sommaire pointe vers elle et la numérotation l’inclut.

Hugo valide fortement le traitement de Mistral et du Chonk : conserver ce personnage et cette scène. Ce retour valide cette direction créative, pas la publication automatique du numéro.

## Sommaire visuel — demande de Hugo du 16 octobre 2026

Prévoir un niveau d’accueil au-dessus des histoires : cartes visibles avec logo, marque/modèle, titre de l’histoire et accès direct à sa case d’ouverture. Le sommaire doit être disponible sans ouvrir un menu replié. Garder un retour « Sommaire » accessible pendant la lecture pour changer de news. Conserver le swipe et le défilement vertical, les liens directs et la navigation clavier.
