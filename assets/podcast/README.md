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
déjà publiée. `show.json` contient les métadonnées de l'émission. L'adresse de
contact doit être confirmée avant publication : elle sera visible dans le RSS
et utilisée pour la vérification Spotify. Une valeur vide bloque la génération.

```sh
python3 scripts/build_podcast_feed.py --archive-latest
python3 -m unittest discover -s scripts -p test_podcast_feed.py -v
```

Prérequis local/CI : Python 3.9+ et ffprobe (ffmpeg). Sans `--archive-latest`,
le script reconstruit seulement le RSS des archives existantes. Il n'appelle
aucun service, ne génère pas de voix et n'envoie rien sur Telegram.

Sortie prévue : `https://hl-consulting.tech/assets/podcast/feed.xml`.
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

État de ce lot : code préparé et tests locaux ; aucun rattachement aux plateformes
n'est établi par ces fichiers. Ne pas annoncer une distribution automatisée avant
la vérification d'un deuxième épisode réellement propagé.

Repli : retirer l'appel au générateur du bridge pour arrêter l'alimentation du
flux, en conservant le dernier RSS, les MP3 datés et leurs GUID. Ne pas supprimer
les anciennes URLs. Une fois un épisode distribué, sa récupération par une
plateforme n'est pas annulée en restaurant simplement un commit.

Sources : [RSS Apple](https://podcasters.apple.com/support/823-podcast-requirements),
[épisodes via RSS](https://podcasters.apple.com/support/825-how-to-create-an-episode),
[rattachement Spotify](https://support.spotify.com/uk/creators/article/claiming-your-podcast-on-spotify-for-creators/).
