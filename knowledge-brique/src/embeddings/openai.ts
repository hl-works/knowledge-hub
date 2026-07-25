import type { Embedder } from "../types.js";

/**
 * Embedder pour tout endpoint compatible OpenAI (`POST /embeddings`).
 * Couvre l'API OpenAI ET un self-host BGE-M3 / nomic-embed exposé via un
 * serveur d'inférence compatible (base URL + modèle configurables).
 */
export class OpenAIEmbedder implements Embedder {
  constructor(
    readonly dim: number,
    private readonly baseUrl: string,
    private readonly model: string,
    private readonly apiKey: string,
  ) {}

  async embed(texts: string[]): Promise<number[][]> {
    if (texts.length === 0) return [];
    const res = await fetch(`${this.baseUrl.replace(/\/$/, "")}/embeddings`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(this.apiKey ? { authorization: `Bearer ${this.apiKey}` } : {}),
      },
      body: JSON.stringify({ model: this.model, input: texts }),
    });
    if (!res.ok) {
      throw new Error(`Embeddings HTTP ${res.status}: ${await res.text()}`);
    }
    const json = (await res.json()) as { data: { embedding: number[] }[] };
    const out = json.data.map((d) => d.embedding);
    for (const v of out) {
      if (v.length !== this.dim) {
        throw new Error(
          `Dimension embeddings inattendue : ${v.length} ≠ EMBEDDING_DIM=${this.dim}`,
        );
      }
    }
    return out;
  }
}
