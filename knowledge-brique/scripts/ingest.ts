/**
 * Étape 1 — ingestion : `npm run ingest`.
 * Branche les connecteurs à accès propre (knowledge-hub + dossier docs),
 * ingère dans le store (chunk → embed → upsert avec dédup par hash) et
 * loggue les compteurs. Un 2ᵉ passage prouve la dédup : 0 nouveau chunk.
 */
import { config } from "../src/config.js";
import { KnowledgeHubConnector } from "../src/connectors/knowledgeHub.js";
import { makeKnowledge } from "../src/index.js";
import { logCounters, newCounters } from "../src/logger.js";
import type { Connector } from "../src/connectors/index.js";

const kb = makeKnowledge();
await kb.init();

const connectors: Connector[] = [new KnowledgeHubConnector(config.ingestion.knowledgeHubPath)];

async function runOnce(scope: string) {
  const total = newCounters();
  for (const c of connectors) {
    const docs = await c.fetch();
    const counters = await kb.ingestBatch(docs, c.name);
    total.documents += counters.documents;
    total.chunksRead += counters.chunksRead;
    total.chunksNew += counters.chunksNew;
    total.chunksDuplicated += counters.chunksDuplicated;
  }
  logCounters(scope, total);
}

console.log("— Passage 1 (ingestion initiale) —");
await runOnce("total-run1");

console.log("\n— Passage 2 (re-scan : doit tout dédupliquer) —");
await runOnce("total-run2");

console.log(`\nStore final : ${await kb.count()} chunk(s).`);
await kb.close();
