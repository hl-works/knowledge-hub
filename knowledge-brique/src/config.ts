import "dotenv/config";

function req(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Variable d'environnement manquante : ${name}`);
  return v;
}

export const config = {
  store: {
    backend: (process.env.STORE_BACKEND ?? "memory") as "memory" | "pg",
    get databaseUrl() {
      return req("DATABASE_URL");
    },
  },
  embeddings: {
    provider: (process.env.EMBEDDER ?? "fake") as "fake" | "openai",
    dim: Number(process.env.EMBEDDING_DIM ?? 1024),
    baseUrl: process.env.EMBEDDINGS_BASE_URL ?? "https://api.openai.com/v1",
    model: process.env.EMBEDDINGS_MODEL ?? "text-embedding-3-small",
    apiKey: process.env.EMBEDDINGS_API_KEY ?? "",
  },
  ingestion: {
    knowledgeHubPath: process.env.KNOWLEDGE_HUB_PATH ?? "../knowledge-hub",
  },
};
