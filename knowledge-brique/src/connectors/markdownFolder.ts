import { readdir, readFile } from "node:fs/promises";
import { extname, join, relative } from "node:path";
import type { SourceDocument } from "../types.js";
import type { Connector } from "./types.js";

async function walk(dir: string): Promise<string[]> {
  const out: string[] = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "node_modules" || entry.name.startsWith(".")) continue;
      out.push(...(await walk(full)));
    } else if (extname(entry.name).toLowerCase() === ".md") {
      out.push(full);
    }
  }
  return out;
}

/**
 * Connecteur « dossier docs » (source IN, dépôt fichier).
 * Ingère tous les .md d'un dossier — les CDC / socle / notes que tu déposes.
 */
export class MarkdownFolderConnector implements Connector {
  readonly name = "docs";

  constructor(
    private readonly folder: string,
    private readonly projet = "",
  ) {}

  async fetch(): Promise<SourceDocument[]> {
    const files = await walk(this.folder);
    const docs: SourceDocument[] = [];
    for (const file of files) {
      const text = (await readFile(file, "utf8")).trim();
      if (!text) continue;
      docs.push({
        source: `docs:${relative(this.folder, file)}`,
        type: "doc",
        projet: this.projet,
        date: "",
        text,
      });
    }
    return docs;
  }
}
