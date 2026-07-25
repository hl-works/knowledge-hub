import { makeEmbedder } from "./embeddings/index.js";
import { Knowledge } from "./knowledge.js";
import { makeStore } from "./store/index.js";

export { Knowledge } from "./knowledge.js";
export * from "./types.js";
export { makeStore } from "./store/index.js";
export { makeEmbedder } from "./embeddings/index.js";

/** Fabrique une instance câblée selon la config (.env). */
export function makeKnowledge(): Knowledge {
  return new Knowledge(makeStore(), makeEmbedder());
}
