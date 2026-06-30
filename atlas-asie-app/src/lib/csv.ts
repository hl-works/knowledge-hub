// Parser CSV agnostique : ne connaît aucun schéma.
// Gère : guillemets, virgules internes, retours-ligne dans une cellule,
// guillemets échappés ("" -> "), CRLF/LF, BOM, champs vides.
// Sortie : tableau d'objets { [colonne]: valeur } en se basant sur la
// première ligne (en-têtes). Les colonnes sans en-tête sont ignorées.

export type CsvRow = Record<string, string>;

/** Découpe un texte CSV en matrice de cellules (gère guillemets et sauts de ligne). */
export function parseCsvToMatrix(input: string): string[][] {
  // Retire un éventuel BOM en tête.
  const text = input.charCodeAt(0) === 0xfeff ? input.slice(1) : input;

  const rows: string[][] = [];
  let row: string[] = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];

    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          field += '"'; // guillemet échappé
          i++;
        } else {
          inQuotes = false; // fin de cellule quotée
        }
      } else {
        field += ch;
      }
      continue;
    }

    if (ch === '"') {
      inQuotes = true;
    } else if (ch === ',') {
      row.push(field);
      field = '';
    } else if (ch === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (ch === '\r') {
      // CRLF : on ignore le \r, le \n suivant clôt la ligne.
      // CR seul (vieux Mac) : on clôt aussi la ligne.
      if (text[i + 1] !== '\n') {
        row.push(field);
        rows.push(row);
        row = [];
        field = '';
      }
    } else {
      field += ch;
    }
  }

  // Dernière cellule / dernière ligne (si pas de saut final).
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  return rows;
}

/** Parse un CSV en tableau d'objets indexés par en-tête. */
export function parseCsv(input: string): CsvRow[] {
  const matrix = parseCsvToMatrix(input);
  if (matrix.length === 0) return [];

  const headers = matrix[0].map((h) => h.trim());
  const out: CsvRow[] = [];

  for (let r = 1; r < matrix.length; r++) {
    const cells = matrix[r];
    // Ligne entièrement vide -> on saute (artefact fréquent des exports Sheets).
    if (cells.length === 1 && cells[0].trim() === '') continue;

    const obj: CsvRow = {};
    for (let c = 0; c < headers.length; c++) {
      const key = headers[c];
      if (!key) continue; // colonne sans en-tête : ignorée
      obj[key] = cells[c] ?? '';
    }
    out.push(obj);
  }

  return out;
}
