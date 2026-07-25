/**
 * Découpage simple et robuste, orienté markdown.
 * On segmente sur les paragraphes (lignes vides) et les titres, puis on
 * empaquette jusqu'à ~targetChars, avec un léger recouvrement pour ne pas
 * couper une idée en deux entre deux chunks.
 */
export interface ChunkOptions {
  targetChars?: number;
  overlapChars?: number;
}

export function chunkText(text: string, opts: ChunkOptions = {}): string[] {
  const targetChars = opts.targetChars ?? 1200;
  const overlapChars = opts.overlapChars ?? 150;

  const blocks = text
    .replace(/\r\n/g, "\n")
    .split(/\n{2,}/)
    .map((b) => b.trim())
    .filter(Boolean);

  const chunks: string[] = [];
  let current = "";

  const flush = () => {
    const trimmed = current.trim();
    if (trimmed) chunks.push(trimmed);
    current = "";
  };

  for (const block of blocks) {
    // Un bloc plus gros que la cible : on le coupe durement.
    if (block.length > targetChars) {
      flush();
      for (let i = 0; i < block.length; i += targetChars - overlapChars) {
        chunks.push(block.slice(i, i + targetChars).trim());
      }
      continue;
    }
    if (current.length + block.length + 2 > targetChars) {
      const tail = current.slice(Math.max(0, current.length - overlapChars));
      flush();
      current = tail ? tail + "\n\n" + block : block;
    } else {
      current = current ? current + "\n\n" + block : block;
    }
  }
  flush();
  return chunks;
}
