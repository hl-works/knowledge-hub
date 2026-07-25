import type { SourceDocument } from "../types.js";

/**
 * Un connecteur = une source du sens IN. On démarre par les sources à accès
 * propre (knowledge-hub, dossier docs) ; les autres s'ajoutent au fil de l'eau.
 */
export interface Connector {
  readonly name: string;
  fetch(): Promise<SourceDocument[]>;
}
