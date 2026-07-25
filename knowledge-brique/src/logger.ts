/** Compteurs d'ingestion — pattern Cobra (lus / nouveaux / dédupliqués). */
export interface Counters {
  documents: number;
  chunksRead: number;
  chunksNew: number;
  chunksDuplicated: number;
}

export function newCounters(): Counters {
  return { documents: 0, chunksRead: 0, chunksNew: 0, chunksDuplicated: 0 };
}

export function logCounters(scope: string, c: Counters): void {
  console.log(
    `[${scope}] docs=${c.documents} lus=${c.chunksRead} ` +
      `nouveaux=${c.chunksNew} dédupliqués=${c.chunksDuplicated}`,
  );
}
