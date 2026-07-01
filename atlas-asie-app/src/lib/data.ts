// Accès données côté client : récupère le CSV d'un onglet (URL publiée si
// dispo, sinon fixture locale) et le parse via PapaParse.
import { parseCsv, type Row } from './parse';
import { SHEET_TABS, type SheetKey } from './sheets';

function fixtureUrl(key: SheetKey): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/fixtures/${key}.csv`;
}

export async function fetchTab(key: SheetKey): Promise<Row[]> {
  const tab = SHEET_TABS[key];
  const url = tab.csvUrl || fixtureUrl(key);
  const res = await fetch(url, { redirect: 'follow' });
  if (!res.ok) {
    throw new Error(`Atlas Asie — chargement "${key}" échoué (${res.status}) : ${url}`);
  }
  return parseCsv(await res.text());
}

export function isUsingFixture(key: SheetKey): boolean {
  return SHEET_TABS[key].csvUrl === '';
}
