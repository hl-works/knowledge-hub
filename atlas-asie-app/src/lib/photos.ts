// Photos libres de droits (Wikimedia Commons), résolues au préalable par
// scripts/resolve_photos_commons.py dans public/fixtures/photos.json :
//   { "<photo_query>": { src, credit, page } }
// Zéro appel API au runtime ; hotlink upload.wikimedia.org autorisé.
// Le crédit (obligation CC) est porté par le title/aria de chaque image,
// + mention globale sur la page. Une photo perso de la Sheet reste prioritaire.

export interface CcPhoto {
  src: string;
  credit: string;
  page?: string;
}

let map: Record<string, CcPhoto> = {};

export async function loadPhotos(): Promise<void> {
  try {
    const base = import.meta.env.BASE_URL.replace(/\/$/, '');
    const res = await fetch(`${base}/fixtures/photos.json`);
    if (res.ok) map = await res.json();
  } catch {
    map = {};
  }
}

const esc = (s: string) =>
  s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] as string));

/** Balise <img> prête à injecter pour une photo_query ('' si non résolue). */
export function ccImg(query: string, alt: string, cls = ''): string {
  const p = map[query];
  if (!p) return '';
  return `<img${cls ? ` class="${cls}"` : ''} src="${esc(p.src)}" alt="${esc(alt)}" title="${esc(p.credit)}" loading="lazy" />`;
}
