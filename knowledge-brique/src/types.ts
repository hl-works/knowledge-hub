/** Un chunk prêt à stocker : le contenu + ses métadonnées + son vecteur. */
export interface ChunkRecord {
  /** sha256 du contenu normalisé — clé de déduplication. */
  hash: string;
  contenu: string;
  source: string;
  type: string;
  /** projet rattaché (peut être vide). */
  projet: string;
  /** ISO date (YYYY-MM-DD) ou timestamp. */
  date: string;
  embedding: number[];
}

/** Document brut à ingérer, avant découpage. */
export interface SourceDocument {
  source: string;
  type: string;
  projet: string;
  date: string;
  text: string;
}

export interface SearchHit {
  hash: string;
  contenu: string;
  source: string;
  type: string;
  projet: string;
  date: string;
  /** similarité cosinus dans [0,1], 1 = identique. */
  score: number;
}

export interface UpsertResult {
  /** chunks réellement insérés (nouveaux hash). */
  inserted: number;
  /** chunks ignorés car hash déjà présent. */
  duplicates: number;
}

/** Filtre optionnel de recherche par métadonnée. */
export interface SearchFilter {
  projet?: string;
  type?: string;
  source?: string;
}

export interface Store {
  init(): Promise<void>;
  upsertChunks(records: ChunkRecord[]): Promise<UpsertResult>;
  search(embedding: number[], topK: number, filter?: SearchFilter): Promise<SearchHit[]>;
  count(): Promise<number>;
  close(): Promise<void>;
}

export interface Embedder {
  readonly dim: number;
  embed(texts: string[]): Promise<number[][]>;
}
