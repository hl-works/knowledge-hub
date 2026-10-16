# Radio Iastro

Direction proposée le 16 octobre 2026 : **Le Radar IA** pour la veille écrite, **Radio Iastro** pour l'audio et **Iastro Sunday** pour le comic du dimanche, réunis dans **Le Kiosque IA**. Ces nouveaux noms restent une proposition à Hugo. « IA immersion BD » est abandonné à sa demande ; l'URL existante est conservée.

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
