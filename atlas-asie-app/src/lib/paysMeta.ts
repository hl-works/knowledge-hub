// Métadonnées visuelles par pays : palette, code « passeport », slug d'ancre,
// et en-tête de groupe (avec emplacement réservé pour le futur tampon AMHE).
// Source unique pour toutes les pages. ⚠️ scripts/build_atlas_static.py garde
// un miroir Python de PAL/CODE : synchroniser si on ajoute un pays.

export const PAL: Record<string, [string, string]> = {
  Kazakhstan: ['#FA4616', '#C9330B'], Kirghizistan: ['#149E7C', '#0C5A5E'],
  Mongolie: ['#E89B2E', '#B86A12'], Chine: ['#F2516F', '#C12B49'],
  'Hong-Kong': ['#1E96C8', '#0C5A7E'], Indonésie: ['#149E7C', '#0C5A5E'],
  Malaisie: ['#E89B2E', '#B86A12'],
};

export const CODE: Record<string, string> = {
  Kazakhstan: 'KZ', Kirghizistan: 'KG', Mongolie: 'MN', Chine: 'CN',
  'Hong-Kong': 'HK', Indonésie: 'ID', Malaisie: 'MY',
};

export const slugPays = (s: string) =>
  s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

import { stampEki } from './stamps';

const esc = (s: string) =>
  s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] as string));

/**
 * En-tête de groupe « pays » commun à toutes les pages listées par pays
 * (hôtels, parcours, galerie…). Le `.stamp-slot` est l'emplacement réservé
 * au tampon AMHE du pays : le design le remplira (le code pays sert de
 * placeholder d'ici là).
 */
export function paysHead(pays: string, sub = ''): string {
  const [c1, c2] = PAL[pays] ?? ['#FA4616', '#C9330B'];
  return `<div class="pays-head" style="--pc1:${c1};--pc2:${c2}">
    <span class="stamp-slot" data-pays="${slugPays(pays)}" aria-hidden="true">${stampEki(pays, { size: 58 })}</span>
    <h2 class="disp">${esc(pays)}</h2>
    ${sub ? `<span class="pays-sub">${esc(sub)}</span>` : ''}
  </div>`;
}

/** Groupe des éléments par pays en respectant l'ordre d'apparition. */
export function groupByPays<T>(items: T[], pays: (t: T) => string): Array<{ pays: string; items: T[] }> {
  const out: Array<{ pays: string; items: T[] }> = [];
  const idx = new Map<string, number>();
  for (const it of items) {
    const p = pays(it);
    if (!idx.has(p)) {
      idx.set(p, out.length);
      out.push({ pays: p, items: [] });
    }
    out[idx.get(p)!].items.push(it);
  }
  return out;
}
