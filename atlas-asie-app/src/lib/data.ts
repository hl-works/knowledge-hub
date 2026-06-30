// Couche d'accès aux données, exécutée CÔTÉ CLIENT (navigateur).
// Récupère le CSV publié d'un onglet et le parse en lignes brutes.
//
// Tant que l'URL réelle d'un onglet n'est pas renseignée dans sheets.ts,
// on retombe sur une fixture locale (public/fixtures/<key>.csv) pour
// valider le pipeline de bout en bout sans dépendre de la Sheet.

import { parseCsv, type CsvRow } from './csv';
import { SHEET_TABS, type SheetKey } from './sheets';

/** Construit l'URL de la fixture locale en respectant le base path (/atlas-asie). */
function fixtureUrl(key: SheetKey): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/fixtures/${key}.csv`;
}

/** Récupère les lignes brutes d'un onglet (URL publiée si dispo, sinon fixture). */
export async function fetchTab(key: SheetKey): Promise<CsvRow[]> {
  const tab = SHEET_TABS[key];
  const url = tab.csvUrl || fixtureUrl(key);

  const res = await fetch(url, { redirect: 'follow' });
  if (!res.ok) {
    throw new Error(`Atlas Asie — échec du chargement de "${key}" (${res.status}) : ${url}`);
  }
  const text = await res.text();
  return parseCsv(text);
}

/** True si l'onglet pointe encore sur une fixture (URL réelle non fournie). */
export function isUsingFixture(key: SheetKey): boolean {
  return SHEET_TABS[key].csvUrl === '';
}
