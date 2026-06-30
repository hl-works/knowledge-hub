// Registre des onglets de la Google Sheet publiée.
// Ajouter un onglet = ajouter une entrée ici. Aucune autre modif nécessaire.
//
// URL d'un onglet publié en CSV (Fichier > Partager > Publier sur le web,
// puis choisir l'onglet + format CSV) :
//   https://docs.google.com/spreadsheets/d/e/<ID_PUBLICATION>/pub?gid=<GID>&single=true&output=csv
//
// Tant que les URLs réelles ne sont pas fournies, on laisse des placeholders.
// Le pipeline est validé via les fixtures locales (voir lib/data.ts).

export interface SheetTab {
  /** Clé stable utilisée dans le code (ne pas changer une fois publiée). */
  key: string;
  /** Libellé humain (debug / UI éventuelle). */
  label: string;
  /** URL CSV publiée de l'onglet. '' = non encore fourni. */
  csvUrl: string;
}

export const SHEET_TABS = {
  parcours: {
    key: 'parcours',
    label: 'Parcours',
    csvUrl: '', // TODO: coller l'URL CSV publiée de l'onglet Parcours
  },
  pays: {
    key: 'pays',
    label: 'Pays',
    csvUrl: '', // TODO: coller l'URL CSV publiée de l'onglet Pays
  },
  // Nouveaux onglets à venir : ajouter ici (ex. villes, etapes, sources…).
} satisfies Record<string, SheetTab>;

export type SheetKey = keyof typeof SHEET_TABS;

export function getTab(key: SheetKey): SheetTab {
  return SHEET_TABS[key];
}
