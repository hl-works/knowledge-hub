import { config } from "../config.js";
import type { Store } from "../types.js";
import { MemoryStore } from "./memory.js";
import { PgStore } from "./pg.js";

export function makeStore(): Store {
  switch (config.store.backend) {
    case "memory":
      return new MemoryStore();
    case "pg":
      return new PgStore(config.store.databaseUrl, config.embeddings.dim);
    default:
      throw new Error(`STORE_BACKEND inconnu : ${config.store.backend}`);
  }
}

export { MemoryStore, PgStore };
