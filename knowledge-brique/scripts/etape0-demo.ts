/**
 * Démo Étape 0 exécutable : `npm run demo:etape0`.
 * Prouve le critère de succès dans le terminal — vectorise un doc, le stocke,
 * puis le retrouve par recherche sémantique.
 * Marche hors-ligne (STORE_BACKEND=memory, EMBEDDER=fake par défaut) et,
 * tel quel, contre un vrai Postgres+pgvector si STORE_BACKEND=pg.
 */
import { makeKnowledge } from "../src/index.js";

const kb = makeKnowledge();
await kb.init();

await kb.ingest({
  source: "docs/knowledge-brique-commune.md",
  type: "spec",
  projet: "brique-commune",
  date: "2026-07-25",
  text:
    "Un store, deux directions. Le mega brain (entrée) et le publisher hub " +
    "(sortie) partagent le même store Postgres + pgvector et le même socle IA. " +
    "L'ingestion découpe, embed et upsert avec dédup par hash. Le sens OUT rédige " +
    "une entrée au gabarit knowledge-hub et pousse sur GitHub après validation.",
});

console.log(`\nStore : ${await kb.count()} chunk(s).\n`);

const query = "comment le contenu est-il stocké et dédupliqué ?";
const hits = await kb.search(query, { topK: 3 });

console.log(`Requête : « ${query} »\n`);
for (const [i, h] of hits.entries()) {
  console.log(`#${i + 1}  score=${h.score.toFixed(3)}  [${h.source}]`);
  console.log(`     ${h.contenu.slice(0, 120)}…\n`);
}

await kb.close();
