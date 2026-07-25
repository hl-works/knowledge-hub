import { describe, expect, it } from "vitest";
import { FakeEmbedder } from "../src/embeddings/fake.js";
import { Knowledge } from "../src/knowledge.js";
import { MemoryStore } from "../src/store/memory.js";

function makeKb() {
  return new Knowledge(new MemoryStore(), new FakeEmbedder(1024));
}

describe("Étape 0 — store : vectorise, stocke, retrouve", () => {
  it("un doc test est vectorisé et stocké, search() le retrouve (au-dessus du bruit)", async () => {
    const kb = makeKb();
    await kb.init();

    await kb.ingest({
      source: "test/cible",
      type: "note",
      projet: "cobra",
      date: "2026-07-25",
      text: "Le connecteur Cobra synchronise le stock Shopify depuis Odoo.",
    });
    // Doc distracteur, sans rapport, pour vérifier le classement.
    await kb.ingest({
      source: "test/bruit",
      type: "note",
      projet: "perso",
      date: "2026-07-25",
      text: "Recette de tarte aux pommes et promenade en forêt le dimanche.",
    });

    expect(await kb.count()).toBeGreaterThan(0);

    const hits = await kb.search("synchronisation du stock Shopify depuis Odoo");
    expect(hits.length).toBeGreaterThan(0);
    // Le bon document remonte en tête, nettement au-dessus du distracteur.
    expect(hits[0]!.source).toBe("test/cible");
    expect(hits[0]!.contenu).toContain("Shopify");
    const bruit = hits.find((h) => h.source === "test/bruit");
    expect(hits[0]!.score).toBeGreaterThan(bruit?.score ?? 0);
  });

  it("dédup par hash : ré-ingérer le même doc n'ajoute rien", async () => {
    const kb = makeKb();
    await kb.init();
    const doc = {
      source: "test/dup",
      type: "note",
      projet: "",
      date: "2026-07-25",
      text: "Contenu identique répété pour tester la déduplication par hash.",
    };

    const first = await kb.ingest(doc);
    expect(first.chunksNew).toBeGreaterThan(0);
    expect(first.chunksDuplicated).toBe(0);

    const countAfterFirst = await kb.count();

    const second = await kb.ingest(doc);
    expect(second.chunksNew).toBe(0);
    expect(second.chunksDuplicated).toBe(first.chunksNew);
    expect(await kb.count()).toBe(countAfterFirst);
  });

  it("le filtre par projet restreint les résultats", async () => {
    const kb = makeKb();
    await kb.init();
    await kb.ingest({
      source: "a",
      type: "note",
      projet: "cobra",
      date: "2026-07-25",
      text: "Note projet cobra sur la logistique et les expéditions.",
    });
    await kb.ingest({
      source: "b",
      type: "note",
      projet: "hifi-lovers",
      date: "2026-07-25",
      text: "Note projet hifi-lovers sur la logistique et les expéditions.",
    });

    const hits = await kb.search("logistique et expéditions", { filter: { projet: "cobra" } });
    expect(hits.length).toBeGreaterThan(0);
    expect(hits.every((h) => h.projet === "cobra")).toBe(true);
  });
});
