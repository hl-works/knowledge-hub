import { config } from "../config.js";
import type { Embedder } from "../types.js";
import { FakeEmbedder } from "./fake.js";
import { OpenAIEmbedder } from "./openai.js";

export function makeEmbedder(): Embedder {
  const { provider, dim, baseUrl, model, apiKey } = config.embeddings;
  switch (provider) {
    case "fake":
      return new FakeEmbedder(dim);
    case "openai":
      return new OpenAIEmbedder(dim, baseUrl, model, apiKey);
    default:
      throw new Error(`EMBEDDER inconnu : ${provider}`);
  }
}

export { FakeEmbedder, OpenAIEmbedder };
