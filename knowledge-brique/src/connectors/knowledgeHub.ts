import { readFile } from "node:fs/promises";
import { join } from "node:path";
import type { SourceDocument } from "../types.js";
import type { Connector } from "./types.js";

const DELIM = /^={16,}$/;

function sectionFromUrl(url: string): string {
  const m = url.match(/\/knowledge-hub\/([^/]+)\//);
  return m ? m[1]! : "page";
}

/**
 * Connecteur knowledge-hub (source IN, accès propre).
 * Parse `llms-full.txt` — l'export texte intégral auto-généré pour les LLMs —
 * en un document par entrée (titre / URL / date + corps). C'est le corpus
 * curaté du site, sans avoir à parser le HTML.
 *
 * Format d'une entrée :
 *   ====================
 *   TITRE
 *   URL : https://…
 *   Publié : YYYY-MM-DD
 *   ====================
 *   <corps…>
 */
export class KnowledgeHubConnector implements Connector {
  readonly name = "knowledge-hub";

  constructor(private readonly repoPath: string) {}

  async fetch(): Promise<SourceDocument[]> {
    const raw = await readFile(join(this.repoPath, "llms-full.txt"), "utf8");
    const parts = raw.split(new RegExp(DELIM.source, "m"));
    // parts[0] = préambule ; puis (header, body) alternés.
    const docs: SourceDocument[] = [];
    for (let k = 1; k + 1 < parts.length; k += 2) {
      const header = parts[k]!;
      const body = (parts[k + 1] ?? "").trim();
      if (!body) continue;

      const lines = header.split("\n").map((l) => l.trim());
      const url = lines.find((l) => l.startsWith("URL :"))?.slice(5).trim() ?? "";
      const date =
        lines.find((l) => l.startsWith("Publié :"))?.slice(8).trim() ?? "";
      const title =
        lines.find((l) => l && !l.startsWith("URL :") && !l.startsWith("Publié :")) ?? url;

      docs.push({
        source: url || `knowledge-hub:${title}`,
        type: `kh:${sectionFromUrl(url)}`,
        projet: "",
        date: date || "",
        text: title ? `${title}\n\n${body}` : body,
      });
    }
    return docs;
  }
}
