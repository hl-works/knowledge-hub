# Le Podcast iA

Direction proposée le 16 octobre 2026 : **Le Radar iA** pour la veille écrite, **Le Podcast iA** pour l'audio et **iAstro Sunday** pour le comic du dimanche, réunis dans **Le Kiosque IA**. Hugo retient le trio texte / podcast / comic ; « Radio Iastro » est remplacé par « Le Podcast iA ». « IA immersion BD » est abandonné à sa demande ; l'URL existante est conservée.

## Visuels

Les portraits `art/iastro-10-v1.png`, `art/iastro-11-v1.png` et `art/iastro-12-v1.png` couvrent octobre, novembre et décembre. Ils ont été créés avec Imagegen intégré, à partir de l'identité et du vestiaire approuvés. Prompts complets dans `art/prompts.json`. Les neuf autres portraits mensuels ne sont pas encore produits ; les références de tenues annuelles sont dans le kit comics.

Le Flash est rouge ; Le Débrief est violet. Le visage, la date et la durée réelle sont prioritaires, y compris en miniature. Les dates, noms et durées sont composés en HTML/CSS, jamais dessinés dans le portrait. `scripts/podcast_design.py` est la source du composant partagé. `player.js` synchronise les métadonnées et le mois avec `latest.json`.

## Reconstruction et export

1. Mettre à jour les manifestes audio, puis lancer `python3 scripts/build_immersion.py`.
2. Ouvrir les fichiers `cover-layouts/YYYY-MM-DD-{short,full}.html` avec le serveur local. Exporter chaque page carrée à 1080 × 1080 dans `covers/`, puis à 320 × 320 dans `<sortie>/thumbnails-png/`. Attendre le chargement des polices et du portrait ; vérifier date et durée.
3. Lancer `python3 scripts/package_podcasts.py --output <sortie>` avec ffmpeg/ffprobe installés. Le script compose le ZIP avec les couvertures, miniatures JPEG, portraits, prompts et copies MP3 illustrées. Il vérifie l'image attachée, la durée et l'identité du flux audio. Les originaux restent inchangés.

Le pack du 12–16 octobre contient dix couvertures et dix pistes existantes. Aucun nouveau podcast n'est généré. Il ne s'agit pas d'un récapitulatif hebdomadaire.

## Telegram

Pour `sendAudio`, joindre le MP3, le titre, l'interprète et le JPEG correspondant en `thumbnail` multipart : JPEG de moins de 200 ko et au plus 320 × 320. Voir la [documentation officielle](https://core.telegram.org/bots/api#sendaudio). Le PNG 1080 est également disponible pour accompagner un message avec un grand visuel. Le rendu dépend du client Telegram.

Cette modification prépare les fichiers ; elle ne modifie pas le bot et n'envoie aucun message. Aucun automatisme mensuel n'a été installé. Préparer le portrait du mois avant de changer de période.

## Distribution podcast — préparation du 17 octobre 2026

Décision de Hugo : une émission **Le Podcast IA**, par **Hugo LaHutte**, dans
l'univers d'**iAstro**. Le flux distribue uniquement **Le Débrief** complet ;
**Le Flash** reste sur le site et Telegram. Le titre pourra évoluer sans changer
l'identité des épisodes. La voix actuelle est synthétique ; une voix propre à
iAstro sera choisie après casting, sans modifier rétroactivement les archives.

Le producteur est désormais identifié : dépôt `hl-works/veille-ia`, workflow
`.github/workflows/veille.yml`, moteur `veille/audio.py`, export public
`scripts/export-podcast.py` et bridge `scripts/push-podcast-site.sh`.
Il exporte seulement une paire complète dont les deux envois au canal Telegram
sont confirmés. La branche `ecoute` contient aussi des aperçus : ne jamais
publier son contenu aveuglément. Le RSS de veille demeure un flux d'articles.

### Construction

La couverture principale `show-cover-v1.jpg` (3000 × 3000, JPEG opaque) est
déjà publiée. `show.json` contient les métadonnées de l'émission. Hugo a confirmé
le contact professionnel `hugo@hl-consulting.tech` le 17 octobre 2026 : il est
visible dans le RSS et utilisé pour la vérification Spotify. Une valeur vide
bloque la génération.

```sh
python3 scripts/build_podcast_feed.py --archive-latest
python3 -m unittest discover -s scripts -p test_podcast_feed.py -v
```

Prérequis local/CI : Python 3.9+ et ffprobe (ffmpeg). Sans `--archive-latest`,
le script reconstruit seulement le RSS des archives existantes. Il n'appelle
aucun service, ne génère pas de voix et n'envoie rien sur Telegram.

URL du flux : `https://hl-consulting.tech/assets/podcast/feed.xml`.
Chaque enclosure pointe exclusivement sur `archive/YYYY-MM-DD/full.mp3`, avec
sa taille réelle et le MIME `audio/mpeg`. Les durées et le codec sont vérifiés
avec ffprobe. SHA-256 protège les fichiers archivés ; une régénération différente
du même jour est refusée, elle ne remplace pas un épisode déjà distribué.
Les GUID UUIDv5 dépendent de l'URL d'archive, jamais du titre ou de la couverture.
Les manifestes historiques ne donnant que la date, `pubDate` utilise minuit
Europe/Paris par convention, sans prétendre être l'heure d'envoi Telegram.
Les champs facultatifs `title` et `description` d'un épisode permettent une
retouche éditoriale sans changement de GUID ou d'enclosure.

### Mise en service et contrôle

1. Confirmer le contact public, construire et valider le flux avec les vrais MP3.
2. Déployer le flux initial, vérifier HTTP 200, HEAD, les tailles et les plages
   d'octets (206), puis rattacher cette URL dans Spotify for Creators.
3. Hugo réalise les accords contractuels et les connexions nécessaires.
4. Déployer le raccordement du producteur seulement après un essai local avec
   une sortie quotidienne réelle déjà publique. Il archive et reconstruit dans
   son clone temporaire avant le push ; un échec conserve la publication précédente.
5. Observer un premier épisode visible sur Spotify, puis l'arrivée du suivant.
   Effectuer aussi la soumission Apple Podcasts et son contrôle séparément.

État vérifié le 17 octobre 2026 : six Débriefs du 12 au 17 octobre visibles sur
[Spotify](https://open.spotify.com/show/10f9eIN4y5iCxx0hc17FUK) et
[Apple Podcasts](https://podcasts.apple.com/us/podcast/le-podcast-ia/id6823971009?l=fr).
Les deux pages publiques proposent de suivre l’émission. Le site FR/EN affiche
les deux liens au-dessus des lecteurs ; le producteur les ajoute aux prochains
audios Telegram, avec le site comme accès de secours. L’auditeur confirme
l’abonnement dans son application. Le Flash reste sur le site et Telegram.

La prononciation « I. A. » a été validée à l’écoute par Hugo le 17 octobre et
intégrée au producteur. Contrôle restant : l’arrivée de la prochaine édition
après ces modifications, du producteur jusqu’aux deux plateformes. Ne pas
confondre l’import des six archives avec ce contrôle de propagation quotidienne.
Évolutions à cadrer : titre définitif, voix originale d’iAstro, portraits des
neuf autres mois, puis promotion LinkedIn et X. Pas de campagne sociale activée.

Repli : retirer l'appel au générateur du bridge pour arrêter l'alimentation du
flux, en conservant le dernier RSS, les MP3 datés et leurs GUID. Ne pas supprimer
les anciennes URLs. Une fois un épisode distribué, sa récupération par une
plateforme n'est pas annulée en restaurant simplement un commit.

Sources : [RSS Apple](https://podcasters.apple.com/support/823-podcast-requirements),
[épisodes via RSS](https://podcasters.apple.com/support/825-how-to-create-an-episode),
[rattachement Spotify](https://support.spotify.com/uk/creators/article/claiming-your-podcast-on-spotify-for-creators/).

## Pochettes d’épisodes automatiques — 17 octobre 2026

Chaque piste archivée reçoit `archive/YYYY-MM-DD/{short,full}-cover-v1.jpg` :
JPEG opaque de 3000 × 3000, composé à partir du même layout que le site,
du portrait `art/iastro-MM-v1.png`, de la date de l’épisode et de sa durée
vérifiée dans le MP3. Le RSS référence le JPEG du Débrief dans chaque
`item/itunes:image`. La couverture générale de l’émission reste distincte.
Les dates et durées restent du texte composé ; aucun dessin n’est régénéré
pendant le job quotidien. Les polices système évitent une dépendance à un CDN.

```sh
python3 -m pip install -r scripts/requirements-podcast-covers.txt
python3 -m playwright install --with-deps chromium
python3 scripts/build_podcast_feed.py --archive-latest --render-covers
```

Le bridge de `veille-ia` effectue ces opérations dans son clone temporaire et
publie images, archives, manifeste et RSS ensemble. Les images déjà référencées
sont conservées et leur SHA-256 est contrôlé. Ajouter une image ne modifie ni
les MP3, ni les GUID, ni les URLs audio des épisodes existants.

Octobre, novembre et décembre sont prêts. **Les portraits de janvier à septembre
restent à produire avant leur première utilisation.** Le renderer signale un portrait manquant ou un échec. Dans la chaîne
quotidienne, ces erreurs sont désormais rattrapées par le producteur : les
audios vérifiés partent sans pochette dédiée et sont publiés dans le RSS.
La couverture générale de l’émission reste disponible. Ne pas prétendre à une autonomie annuelle tant que ces neuf portraits
ne sont pas disponibles. Les anciens exports PNG 1080 sont conservés, mais ne
sont pas les images RSS (minimum Apple : 1400 px).

Le workflow `podcast-check.yml` teste le passage octobre → novembre → décembre,
le rendu réel 3000 px, les empreintes et le rejeu sans modification. Il produit
des aperçus de test en artefacts, sans publier ni envoyer de message.

État plateformes au 17 octobre : Spotify public avec six épisodes, lecture du
17 octobre testée ; Apple Connect affiche les six épisodes disponibles, visibilité
publique encore à confirmer lors du dernier contrôle. Le prochain nouvel épisode
reste à observer de bout en bout avant d’affirmer la propagation quotidienne.


## Maquette validée par Hugo — date et durée

La date complète reste sur **une seule ligne**, en grands chiffres : 17.10.2026.
La mention « L’actualité IA » disparaît du pied. La durée utilise les symboles
minutes et secondes **7′ 23″**, sans horloge. Le Flash et Le Débrief utilisent
le même pied ; les portraits mensuels et les couleurs restent inchangés.

Les nouvelles images RSS portent le suffixe `-cover-v2.jpg`, y compris pour
les éditions existantes : l’URL changée permet aux plateformes de récupérer
la correction. Les anciens JPEG v1 restent accessibles. Le générateur vérifie
leur empreinte avant migration ; les MP3, GUID et dates de publication restent
identiques. Les exports PNG 1080 et les mises en page HTML sont également mis
à jour. Le lecteur dynamique conserve les symboles lorsqu’il actualise la durée.


## Pochette préparée avant Telegram — 17 octobre 2026

Le producteur appelle maintenant le même renderer avec `--daily YYYY-MM-DD
--short-seconds N --full-seconds N --output DOSSIER` avant les envois.
Le rendu isolé fournit les JPEG 3000, PNG 1080 et leur manifeste sans modifier
les épisodes publiés. Une version complète seule reste possible si le Flash
échoue ; le bridge public exige toujours les deux envois confirmés.

Le producteur intègre une déclinaison JPEG 1080 dans le MP3 sans réencoder le
son et joint une miniature JPEG 320 de moins de 200 ko à `sendAudio`. Le bridge
copie les fichiers préparés et transmet leurs empreintes dans `latest.json` ;
le générateur de RSS conserve ces images exactes sans les redessiner.
Les archives déjà distribuées ne sont pas réécrites. Le changement concerne
les prochains audios. La réception effective de la miniature Telegram doit
être distinguée des tests de préparation et des réponses de l’API.


### Priorité à l’audio — correction demandée par Hugo

**Une panne de pochette ne doit jamais, à elle seule, bloquer un audio valide.**
Le producteur `veille-ia` tente le rendu et l’intégration ; en cas d’échec, il
restaure les MP3 originaux vérifiés, omet la miniature Telegram et poursuit
l’export RSS sans `item/itunes:image`. `artwork_status=unavailable` conserve la
trace du repli. Le téléchargement du modèle graphique et l’installation du
renderer sont eux aussi facultatifs et bornés en durée. Aucun appel à une IA
d’image n’est nécessaire pour la composition quotidienne des couvertures.

Les contrôles d’intégrité audio, durée, destination, archives immuables et
absence de réessai automatique après timeout ambigu restent obligatoires.
Ne pas réintroduire un blocage de diffusion pour une image absente. Les tests
du producteur couvrent le chemin illustré et le chemin sans image jusqu’au RSS.

## Rattrapages réservés aux plateformes

`platform-episodes.json` contient les Débriefs dont la publication RSS a été
explicitement autorisée sans nouvel envoi Telegram. Le 18 octobre 2026 est
rattrapé ainsi, à la demande de Hugo le 19. Le MP3 approuvé et sa pochette sont
hébergés sous leur URL datée ; aucun Flash ni dernier duo du site n'est remplacé.
Le générateur fusionne ces entrées avec les archives quotidiennes pour le RSS
seulement, avec les mêmes contrôles de fichier, durée, empreinte et GUID.
Les dates en double sont refusées. L'arrivée des prochaines éditions quotidiennes
ne doit pas retirer ces rattrapages du flux. Les reçus Telegram ne sont pas modifiés.
