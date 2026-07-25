import { createHash } from "node:crypto";
import type { Embedder } from "../types.js";

/**
 * Embedder déterministe, hors-ligne, pour les tests et le dev.
 * Même texte → même vecteur (donc cosinus = 1 pour un match exact).
 * On projette des n-grammes de mots dans un espace de `dim` dimensions via
 * hachage, puis on normalise (L2). Ce n'est pas sémantique, mais c'est
 * suffisant et reproductible pour valider le pipeline store/search/dédup.
 */
export class FakeEmbedder implements Embedder {
  constructor(readonly dim: number = 1024) {}

  async embed(texts: string[]): Promise<number[][]> {
    return texts.map((t) => this.embedOne(t));
  }

  private embedOne(text: string): number[] {
    const vec = new Array<number>(this.dim).fill(0);
    const tokens = text.toLowerCase().match(/\p{L}+|\p{N}+/gu) ?? [];
    for (let i = 0; i < tokens.length; i++) {
      const unigram = tokens[i]!;
      const bigram = i > 0 ? tokens[i - 1] + " " + unigram : unigram;
      for (const term of [unigram, bigram]) {
        const h = createHash("md5").update(term).digest();
        const idx = h.readUInt32BE(0) % this.dim;
        const sign = (h[4]! & 1) === 0 ? 1 : -1;
        vec[idx]! += sign;
      }
    }
    const norm = Math.hypot(...vec) || 1;
    return vec.map((x) => x / norm);
  }
}
