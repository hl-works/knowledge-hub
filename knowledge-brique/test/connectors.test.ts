import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { KnowledgeHubConnector } from "../src/connectors/knowledgeHub.js";

const SAMPLE = `# Knowledge Hub — préambule

> intro

================================================================
MON TITRE DE TEST
URL : https://hl-consulting.tech/knowledge-hub/journal/exemple.html
Publié : 2026-07-01
================================================================

Corps du premier document. Il parle de logistique et d'expéditions.

================================================================
DEUXIEME ENTREE
URL : https://hl-consulting.tech/knowledge-hub/guides/autre.html
Publié : 2026-07-10
================================================================

Corps du deuxième document.
`;

describe("Étape 1 — connecteur knowledge-hub", () => {
  it("parse llms-full.txt en un document par entrée", async () => {
    const dir = await mkdtemp(join(tmpdir(), "kh-"));
    await writeFile(join(dir, "llms-full.txt"), SAMPLE, "utf8");

    const docs = await new KnowledgeHubConnector(dir).fetch();
    expect(docs).toHaveLength(2);

    const first = docs[0]!;
    expect(first.source).toBe(
      "https://hl-consulting.tech/knowledge-hub/journal/exemple.html",
    );
    expect(first.type).toBe("kh:journal");
    expect(first.date).toBe("2026-07-01");
    expect(first.text).toContain("MON TITRE DE TEST");
    expect(first.text).toContain("logistique");

    expect(docs[1]!.type).toBe("kh:guides");
  });
});
