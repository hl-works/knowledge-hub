import pg from "pg";
import type { ChunkRecord, SearchFilter, SearchHit, Store, UpsertResult } from "../types.js";

const { Pool } = pg;

function toVectorLiteral(v: number[]): string {
  return `[${v.join(",")}]`;
}

/**
 * Store Postgres + pgvector. Réutilise le Postgres HF-OS.
 * Collection `knowledge` : contenu, source, type, projet, date, embedding, hash.
 * Dédup par contrainte UNIQUE(hash) + ON CONFLICT DO NOTHING.
 * Recherche : distance cosinus pgvector (`<=>`), score = 1 - distance.
 */
export class PgStore implements Store {
  private readonly pool: pg.Pool;

  constructor(
    databaseUrl: string,
    private readonly dim: number,
  ) {
    this.pool = new Pool({ connectionString: databaseUrl });
  }

  async init(): Promise<void> {
    await this.pool.query("CREATE EXTENSION IF NOT EXISTS vector");
    await this.pool.query(`
      CREATE TABLE IF NOT EXISTS knowledge (
        hash       text PRIMARY KEY,
        contenu    text NOT NULL,
        source     text NOT NULL,
        type       text NOT NULL,
        projet     text NOT NULL DEFAULT '',
        date       text NOT NULL,
        embedding  vector(${this.dim}) NOT NULL
      )
    `);
    await this.pool.query(`
      CREATE INDEX IF NOT EXISTS knowledge_embedding_idx
      ON knowledge USING hnsw (embedding vector_cosine_ops)
    `);
    await this.pool.query(`CREATE INDEX IF NOT EXISTS knowledge_projet_idx ON knowledge (projet)`);
  }

  async upsertChunks(records: ChunkRecord[]): Promise<UpsertResult> {
    if (records.length === 0) return { inserted: 0, duplicates: 0 };
    const client = await this.pool.connect();
    let inserted = 0;
    try {
      await client.query("BEGIN");
      for (const r of records) {
        const res = await client.query(
          `INSERT INTO knowledge (hash, contenu, source, type, projet, date, embedding)
           VALUES ($1,$2,$3,$4,$5,$6,$7)
           ON CONFLICT (hash) DO NOTHING`,
          [r.hash, r.contenu, r.source, r.type, r.projet, r.date, toVectorLiteral(r.embedding)],
        );
        inserted += res.rowCount ?? 0;
      }
      await client.query("COMMIT");
    } catch (e) {
      await client.query("ROLLBACK");
      throw e;
    } finally {
      client.release();
    }
    return { inserted, duplicates: records.length - inserted };
  }

  async search(embedding: number[], topK: number, filter?: SearchFilter): Promise<SearchHit[]> {
    const where: string[] = [];
    const params: unknown[] = [toVectorLiteral(embedding), topK];
    if (filter?.projet) {
      params.push(filter.projet);
      where.push(`projet = $${params.length}`);
    }
    if (filter?.type) {
      params.push(filter.type);
      where.push(`type = $${params.length}`);
    }
    if (filter?.source) {
      params.push(filter.source);
      where.push(`source = $${params.length}`);
    }
    const whereSql = where.length ? `WHERE ${where.join(" AND ")}` : "";
    const res = await this.pool.query(
      `SELECT hash, contenu, source, type, projet, date,
              1 - (embedding <=> $1) AS score
       FROM knowledge
       ${whereSql}
       ORDER BY embedding <=> $1
       LIMIT $2`,
      params,
    );
    return res.rows.map((row) => ({
      hash: row.hash,
      contenu: row.contenu,
      source: row.source,
      type: row.type,
      projet: row.projet,
      date: row.date,
      score: Number(row.score),
    }));
  }

  async count(): Promise<number> {
    const res = await this.pool.query("SELECT COUNT(*)::int AS n FROM knowledge");
    return res.rows[0]?.n ?? 0;
  }

  async close(): Promise<void> {
    await this.pool.end();
  }
}
