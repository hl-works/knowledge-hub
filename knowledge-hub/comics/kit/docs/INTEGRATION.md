# Intégration Knowledge Hub

Le kit partagé vit dans `knowledge-hub/comics/kit/`. Le nom du personnage est **Astro AI** ; les identifiants historiques `ia-*` restent stables pour ne pas casser les références.

Lire `AGENTS.md`, `docs/BIBLE.md`, `manifest.json`, puis le manifeste de personnage dans `kits/`. Ouvrir les images retenues avant de générer une scène. Les douze références mensuelles montrent les deux personnages ensemble. Les PNG sont opaques, sans calques séparés.

Les scènes nouvelles utilisent la référence V2 et la tenue du mois de l’épisode. Ne pas croiser automatiquement douze mois × toutes les poses : créer les scènes selon le scénario.

Le lecteur est `knowledge-hub/comics/index.html`. Le script `python3 scripts/build_comics.py` prépare les pages statiques depuis les épisodes approuvés. Le déploiement existant du site reste responsable de la mise en ligne. Ne jamais pousser sur main sans accord de publication.

Contrôle : `node knowledge-hub/comics/kit/scripts/verify.mjs`.
Les ZIP livrés à Hugo ne sont pas versionnés dans Git. Aucune photo personnelle source, clé API ou ancienne bannière LinkedIn n’est incluse.
