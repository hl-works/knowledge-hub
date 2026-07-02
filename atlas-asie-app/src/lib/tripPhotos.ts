// Photos du voyage hébergées dans le repo : public/photos/<ordre>-<slug>/…
// indexées par public/photos/manifest.json :
//   { "<ordre escale>": [{ "src": "photos/12-bichkek/01.jpg", "legende": "…" }] }
// Elles FUSIONNENT avec la colonne `photos` de la Sheet (les deux coexistent).
// Ajout depuis le téléphone : envoyer les photos à Claude avec le n° d'escale
// (procédure « Ajouter les photos du voyage » du CLAUDE.md) — ou en local :
//   node scripts/add-photos.mjs <ordre> [--legende "…"] fichiers…

export interface TripPhoto {
  src: string; // relatif à la base du site
  legende?: string;
}

let manifest: Record<string, TripPhoto[]> = {};

export async function loadTripPhotos(): Promise<void> {
  try {
    const base = import.meta.env.BASE_URL.replace(/\/$/, '');
    const res = await fetch(`${base}/photos/manifest.json`);
    if (res.ok) manifest = await res.json();
  } catch {
    manifest = {};
  }
}

/** Photos du repo pour une escale (URL absolue de base résolue). */
export function tripPhotos(ordre: number): Array<{ url: string; legende?: string }> {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return (manifest[String(ordre)] ?? []).map((p) => ({
    url: p.src.startsWith('http') ? p.src : `${base}/${p.src.replace(/^\//, '')}`,
    legende: p.legende,
  }));
}
