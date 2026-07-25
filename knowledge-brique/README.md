# knowledge-brique

**Brique commune — mega brain ⇄ publisher hub.** Un seul store, deux sens :

- **IN** — ingestion privée de tout ce qui te concerne, RAG interrogeable par tes IA.
- **OUT** — publication curatée vers le knowledge-hub public, avec validation humaine.

Ce ne sont pas deux projets : c'est **une brique à deux sens**, qui partage un store
(Postgres + pgvector) et le socle IA. Le privé reste privé — rien ne part en public
sans un tap humain.

> Spec complète : [`knowledge-hub/docs/knowledge-brique-commune.md`](../knowledge-hub/docs/knowledge-brique-commune.md).
>
> ⚠️ **Emplacement temporaire.** Ce dossier `knowledge-brique/` est *parqué* sur une
> branche de feature du repo knowledge-hub (jamais mergée sur `main`, donc jamais
> déployée) faute d'avoir pu créer un repo dédié depuis la session (l'app GitHub n'a pas
> le droit de créer des repos). **À déplacer** dans un repo privé dédié
> (`hl-works/knowledge-brique`). Le knowledge-hub doit rester un site statique
> HTML/CSS zéro-dépendance — il est *source* (IN) et *cible* (OUT) de la brique, pas
> l'hôte de son backend.

## Stack

TypeScript / Node 20+, `pg` pour Postgres + pgvector, embeddings pluggables. Aucun
build : exécution via `tsx`, tests via `vitest`.

## Architecture

```
SourceDocument ──chunk──▶ chunks ──embed──▶ vecteurs ──upsert(dédup hash)──▶ Store
                                                                              │
                    requête ──embed──▶ vecteur ──search(cosinus, topK)───────┘
```

- **Store** (`src/store`) — interface unique, deux backends :
  - `memory` : cosinus en mémoire, pour dev/tests (aucune infra).
  - `pg` : Postgres + pgvector (`vector(dim)`, index HNSW cosinus, `UNIQUE(hash)`).
- **Embedder** (`src/embeddings`) — interface unique, deux fournisseurs :
  - `fake` : déterministe, hors-ligne (tests). Même texte → même vecteur.
  - `openai` : tout endpoint compatible OpenAI `/embeddings` — couvre l'API OpenAI
    **et** un self-host BGE-M3 / nomic-embed (base URL + modèle configurables).
- **Connecteurs** (`src/connectors`) — sources du sens IN, on démarre par l'accès propre :
  - `knowledge-hub` : parse `llms-full.txt` (export texte auto-généré) → 1 doc/entrée.
  - `docs` : tous les `.md` d'un dossier (CDC / socle / notes).
- **Cœur** (`src/knowledge.ts`) — `ingest()`, `ingestBatch()`, `search()`, compteurs.

Tout se câble depuis `.env` (voir `.env.example`) via `makeKnowledge()`.

## Démarrer

```bash
cp .env.example .env      # défauts : STORE_BACKEND=memory, EMBEDDER=fake (offline)
npm install
npm test                  # Étape 0 + connecteur
npm run demo:etape0       # démo store dans le terminal
KNOWLEDGE_HUB_PATH=../knowledge-hub npm run ingest
```

Contre un vrai Postgres + pgvector :

```bash
docker compose up -d
STORE_BACKEND=pg \
  DATABASE_URL=postgres://kb:kb@localhost:5433/knowledge \
  EMBEDDER=openai EMBEDDINGS_API_KEY=… EMBEDDING_DIM=1536 \
  npm run ingest
```

## Feuille de route (critères de succès de la spec)

| Étape | Description | État |
|------|-------------|------|
| **0** | Store : vectorise, stocke, `search()` retrouve | ✅ (test + démo verts) |
| **1** | Ingestion knowledge-hub (+ dossier docs), dédup, compteurs | ✅ (89 docs, re-run = 0 nouveau) |
| 1bis | Connecteur **Zéro** (tâches + résumés mails, même Postgres) | ⏳ à câbler |
| 2 | Serveur MCP `search` + 1 Claude en connecteur custom | ⏳ |
| 3 | ChatGPT + 2ᵉ Claude sur le même serveur | ⏳ |
| 4 | Publisher : rédaction voix + rendu au gabarit knowledge-hub | ⏳ |
| 5 | Validation Telegram → commit/push GitHub | ⏳ |
| 6 | Fraîcheur (re-scan) + filtre « pas d'infos sensibles » | ⏳ |

## Décisions ouvertes

1. Modèle d'embeddings : open (BGE-M3 / nomic) vs OpenAI. → `EMBEDDER` le rend
   interchangeable ; à trancher sur coût/qualité/souveraineté.
2. Emplacement du dossier d'ingestion des docs perso.
3. Auth du serveur MCP (token simple d'abord, durci ensuite).
4. Ordre d'ajout des sources après le corpus de démarrage.

## Garde-fou

Public = jamais sans validation. Le filtre « pas d'infos sensibles » (clés, montants
confidentiels, données nominatives de tiers) s'appliquera au sens OUT (Étape 6).
Secrets (token GitHub, auth MCP, clés embeddings) en config serveur — jamais commités.
