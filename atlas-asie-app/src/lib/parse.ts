// Parsing CSV via PapaParse (robuste : guillemets, virgules internes,
// retours-ligne dans une cellule, en-têtes). Agnostique du schéma.
import Papa from 'papaparse';

export type Row = Record<string, string>;

export function parseCsv(text: string): Row[] {
  const res = Papa.parse<Row>(text, {
    header: true,
    skipEmptyLines: 'greedy',
    transformHeader: (h) => h.trim(),
  });
  // On ne garde que les lignes non vides (au moins une clé remplie).
  return (res.data || []).filter(
    (r) => r && Object.values(r).some((v) => (v ?? '').toString().trim() !== ''),
  );
}
