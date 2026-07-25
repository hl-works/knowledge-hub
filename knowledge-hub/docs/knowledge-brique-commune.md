# Knowledge — brique commune (mega brain ⇄ publisher hub)

> Spec / CDC interne. 3ᵉ brique, à côté de `Zéro` (mail + tâches) et du `Socle IA`.
> Un seul store, deux sens : **IN** = ingestion privée de tout ce qui te concerne
> (RAG interrogeable par tes IA), **OUT** = publication curatée vers le knowledge-hub
> public, avec validation. MàJ : 2026-07-25.

---

## 1. Principe

- **Un store, deux directions.** Le *mega brain* (entrée) et le *publisher hub*
  (sortie) partagent le même store et le même socle IA — ce ne sont pas deux projets,
  c'est une brique à deux sens.
- **Réutilise** : Postgres (HF-OS), le Socle IA (rédaction + embeddings), le pattern
  secrets chiffrés.
- **Garde-fou transverse** : le privé reste privé, rien ne part en public sans un tap
  humain. Secrets (token GitHub, auth MCP) en config serveur.

## 2. Store

- Postgres (HF-OS) + pgvector. Collection Payload `Knowledge` : `contenu`, `source`,
  `type`, `projet`, `date`, `embedding`, `hash` (dédup).
- **Embeddings** : modèle open (BGE-M3 / nomic-embed, via API ou self-host léger),
  fallback OpenAI embeddings — cohérent avec la règle open/close du socle.

## 3. Sens IN — ingestion + MCP

### 3.1 Connecteurs de source (corpus de démarrage)

- **knowledge-hub** (repo / markdown public) — accès propre, facile.
- **Zéro** (tâches + résumés de mails triés) — natif, même Postgres.
- **Dossier docs** (project docs / CDC / socle / notes que tu déposes en markdown) —
  dépôt fichier.
- Plus tard : autres sources au fil de l'eau.

Honnêteté : chaque source = un petit connecteur, on démarre par celles à accès propre.
Les docs du projet Claude n'ont pas d'API d'export propre → tu les déposes en markdown
dans le dossier d'ingestion (ou on les recopie une fois). Ne pas sous-estimer :
l'ingestion et la fraîcheur, c'est les 80 % du boulot, pas le branchement.

### 3.2 Pipeline

Fetch incrémental → découpage (chunk) → embeddings → upsert avec dédup par hash →
fraîcheur (re-scan périodique). Compteurs en log (lus / nouveaux / dédupliqués —
pattern Cobra).

### 3.3 Serveur MCP

- Serveur MCP distant exposant `search(query)` sur le store.
- Se branche sur tes 2 Claude + ChatGPT via connecteur custom (auth par token).
  Un seul serveur = un seul cerveau pour les trois.
- Le Socle IA (apps internes) peut l'interroger aussi.

## 4. Sens OUT — publisher hub

### 4.1 Pipeline

- **Déclencheur** : toi (« publie cette idée ») via Telegram, ou une tâche Zéro taguée
  « à publier ».
- Le Socle IA rédige l'entrée dans ta voix, au format exact du gabarit knowledge-hub
  (titre, métadonnées, sections Contexte / Construit / Difficile / Stack / Illustre,
  tags, excerpt, auteur HL / Cobra).
- Génère la page HTML au format du site + met à jour `journal/index.html`, la page
  verticale, l'accueil, `sitemap.xml`, `llms.txt`, JSON-LD, maillage « Voir aussi ».
- **Validation** : brouillon poussé sur Telegram → tu valides d'un tap.
- **Commit / push** sur `hugolahutte/knowledge-hub` (branche `main`) via l'API GitHub
  (token en config). En ligne ~1 min après.

### 4.2 Garde-fou

Public = jamais sans validation. Filtre « pas d'infos sensibles » rappelé au pipeline
(pas de clés, montants confidentiels, données nominatives de tiers) — la règle
éditoriale du hub, appliquée par l'agent.

## 5. Plan de dev (critères de succès)

**Étape 0 — Store.** Collection `Knowledge` + pgvector + modèle d'embeddings branché.
✅ Critère : un doc test est vectorisé et stocké, `search()` le retrouve.

**Étape 1 — Ingestion (knowledge-hub + Zéro).** Connecteurs + pipeline
chunk/embed/upsert + dédup.
✅ Critère : un run ingère le knowledge-hub et les tâches Zéro sans doublon, compteurs
en log.

**Étape 2 — Serveur MCP + 1 Claude.** Serveur MCP `search` + branchement d'un Claude
en connecteur custom.
✅ Critère : depuis Claude, une question sur un projet remonte le bon extrait du store.

**Étape 3 — ChatGPT + 2ᵉ Claude.** Même serveur, deux clients de plus.
✅ Critère : les 3 clients interrogent le même cerveau.

**Étape 4 — Publisher (rédaction + rendu).** Rédaction voix + rendu au gabarit,
brouillon local.
✅ Critère : une idée devient une page knowledge-hub valide (format + SEO), non publiée.

**Étape 5 — Validation Telegram + push GitHub.** Brouillon → tap → commit/push.
✅ Critère : tu valides d'un tap, l'entrée est en ligne ~1 min après ; rien ne part sans
validation.

**Étape 6 — Fraîcheur + garde-fous.** Re-scan périodique + filtre sensible.
✅ Critère : les sources se remettent à jour seules ; un contenu avec info sensible est
bloqué / signalé avant publication.

## 6. Décisions ouvertes

1. Modèle d'embeddings : open (BGE / nomic) vs OpenAI.
2. Emplacement du dossier / collection d'ingestion des docs perso.
3. Auth du serveur MCP (token simple d'abord, durci ensuite).
4. Ordre d'ajout des sources après le corpus de démarrage.
