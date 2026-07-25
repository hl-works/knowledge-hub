import { createHash } from "node:crypto";

/** Normalise le texte (espaces, casse conservée) pour un hash stable de dédup. */
export function normalize(text: string): string {
  return text.replace(/\r\n/g, "\n").replace(/[ \t]+/g, " ").trim();
}

export function contentHash(text: string): string {
  return createHash("sha256").update(normalize(text), "utf8").digest("hex");
}
