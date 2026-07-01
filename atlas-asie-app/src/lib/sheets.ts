// Registre des onglets Google Sheet publiés en CSV.
//
// ⚠️ RÈGLE DE SÉCURITÉ (brief) : n'exposer QUE ces 7 onglets.
// Ne JAMAIS ajouter ici `Passeport` (n° de passeport), `Financier` (budget),
// ni l'onglet Vols privé (références de réservation Trip.com/Booking).
// Aucune donnée sensible ne doit toucher le site, ni en build ni en runtime.
//
// URL d'un onglet publié en CSV (Fichier > Partager > Publier sur le web,
// onglet + format CSV) :
//   https://docs.google.com/spreadsheets/d/e/<ID>/pub?gid=<GID>&single=true&output=csv
// Tant que les URLs réelles ne sont pas fournies, on retombe sur les
// fixtures locales (public/fixtures/<clé>.csv).

export interface SheetTab {
  key: string;
  label: string;
  csvUrl: string; // '' => fixture locale
}

export const SHEET_TABS = {
  parcours: { key: 'parcours', label: 'Parcours', csvUrl: '' },
  pays: { key: 'pays', label: 'Pays', csvUrl: '' },
  quiz: { key: 'quiz', label: 'Quiz', csvUrl: '' },
  bestiaire: { key: 'bestiaire', label: 'Bestiaire', csvUrl: '' },
  lexique: { key: 'lexique', label: 'Lexique', csvUrl: '' },
  transports: { key: 'transports', label: 'Transports', csvUrl: '' },
  pratique: { key: 'pratique', label: 'Pratique', csvUrl: '' },
} satisfies Record<string, SheetTab>;

export type SheetKey = keyof typeof SHEET_TABS;
