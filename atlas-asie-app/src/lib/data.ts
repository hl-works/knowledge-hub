// Accès données côté client : récupère le CSV d'un onglet (URL publiée si
// dispo, sinon fixture locale) et le parse via PapaParse.
// Résilience : la dernière réponse valide est mise en cache (localStorage).
// En cas d'échec réseau (bus en Mongolie…), on sert le cache + on marque
// la page « hors ligne ».
import { parseCsv, type Row } from './parse';
import { SHEET_TABS, type SheetKey } from './sheets';

function fixtureUrl(key: SheetKey): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/fixtures/${key}.csv`;
}

const cacheKey = (key: SheetKey) => `atlas_csv_${key}`;
const readCache = (key: SheetKey): string | null => {
  try {
    return localStorage.getItem(cacheKey(key));
  } catch {
    return null;
  }
};
const writeCache = (key: SheetKey, text: string) => {
  try {
    localStorage.setItem(cacheKey(key), text);
  } catch {
    /* quota / mode privé : on ignore */
  }
};

export async function fetchTab(key: SheetKey): Promise<Row[]> {
  const tab = SHEET_TABS[key];
  const url = tab.csvUrl || fixtureUrl(key);
  try {
    const res = await fetch(url, { redirect: 'follow' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    writeCache(key, text);
    return parseCsv(text);
  } catch (err) {
    const cached = readCache(key);
    if (cached) {
      document.body?.setAttribute('data-offline', '');
      return parseCsv(cached);
    }
    throw new Error(`Atlas Asie — chargement "${key}" échoué : ${String(err)}`);
  }
}

export function isUsingFixture(key: SheetKey): boolean {
  return SHEET_TABS[key].csvUrl === '';
}
