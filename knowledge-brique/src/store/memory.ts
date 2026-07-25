import type { ChunkRecord, SearchFilter, SearchHit, Store, UpsertResult } from "../types.js";

function cosine(a: number[], b: number[]): number {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i]! * b[i]!;
    na += a[i]! * a[i]!;
    nb += b[i]! * b[i]!;
  }
  const denom = Math.sqrt(na) * Math.sqrt(nb);
  return denom === 0 ? 0 : dot / denom;
}

/** Store en mémoire (dev/tests). Dédup par hash, recherche cosinus exacte. */
export class MemoryStore implements Store {
  private readonly byHash = new Map<string, ChunkRecord>();

  async init(): Promise<void> {}

  async upsertChunks(records: ChunkRecord[]): Promise<UpsertResult> {
    let inserted = 0;
    let duplicates = 0;
    for (const r of records) {
      if (this.byHash.has(r.hash)) {
        duplicates++;
      } else {
        this.byHash.set(r.hash, r);
        inserted++;
      }
    }
    return { inserted, duplicates };
  }

  async search(embedding: number[], topK: number, filter?: SearchFilter): Promise<SearchHit[]> {
    const hits: SearchHit[] = [];
    for (const r of this.byHash.values()) {
      if (filter?.projet && r.projet !== filter.projet) continue;
      if (filter?.type && r.type !== filter.type) continue;
      if (filter?.source && r.source !== filter.source) continue;
      hits.push({
        hash: r.hash,
        contenu: r.contenu,
        source: r.source,
        type: r.type,
        projet: r.projet,
        date: r.date,
        score: cosine(embedding, r.embedding),
      });
    }
    hits.sort((a, b) => b.score - a.score);
    return hits.slice(0, topK);
  }

  async count(): Promise<number> {
    return this.byHash.size;
  }

  async close(): Promise<void> {}
}
