// Modèle métier Atlas d'Asie : mappe les lignes CSV brutes vers des objets
// typés et fournit les calculs dérivés (statut, compteurs, live).
import type { Row } from './parse';

export type Statut = 'passe' | 'en-cours' | 'a-venir';

export interface Stop {
  ordre: number;
  pays: string;
  ville: string;
  arrivee: Date | null;
  depart: Date | null;
  hotelNom: string;
  hotelLien: string;
  hotelAdresse: string;
  hotelPhoto: string;
  lat: number;
  lng: number;
  description: string;
  photos: string[];
  video: string;
  statut: Statut;
  photoQuery: string;
}

export interface Country {
  pays: string;
  capitale: string;
  monnaie: string;
  langue: string;
  population: string;
  histoire: string;
  funFacts: string[];
  photoQuery: string;
  photoHero: string;
}

export interface QuizQ {
  pays: string;
  question: string;
  choix: [string, string, string];
  bonne: 'a' | 'b' | 'c';
  explication: string;
}

/** Parse une date `JJ/MM/AAAA` (format de la Sheet). */
export function parseDMY(s: string | undefined): Date | null {
  if (!s) return null;
  const m = s.trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!m) return null;
  const d = new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]));
  d.setHours(0, 0, 0, 0);
  return isNaN(d.getTime()) ? null : d;
}

const num = (s: string | undefined): number => {
  const n = parseFloat((s ?? '').replace(',', '.'));
  return isNaN(n) ? 0 : n;
};
const splitList = (s: string | undefined, sep: RegExp | string): string[] =>
  (s ?? '')
    .split(sep)
    .map((x) => x.trim())
    .filter(Boolean);

/** Statut calculé à partir des dates si `manuel` est vide/inconnu. */
export function computeStatut(
  arrivee: Date | null,
  depart: Date | null,
  today: Date,
  manuel?: string,
): Statut {
  const known = ['passe', 'en-cours', 'a-venir'];
  const norm = (manuel ?? '').toLowerCase().replace(/[éè]/g, 'e').replace(/\s+/g, '-');
  if (known.includes(norm)) return norm as Statut;
  if (arrivee && today < arrivee) return 'a-venir';
  if (depart && today > depart) return 'passe';
  if (arrivee && !depart && today > arrivee) return 'passe';
  if (arrivee && today >= arrivee && (!depart || today <= depart)) return 'en-cours';
  return 'a-venir';
}

export function toStops(rows: Row[], today: Date = startOfToday()): Stop[] {
  return rows
    .map((r) => {
      const arrivee = parseDMY(r.date_arrivee);
      const depart = parseDMY(r.date_depart);
      return {
        ordre: num(r.ordre),
        pays: (r.pays ?? '').trim(),
        ville: (r.ville ?? '').trim(),
        arrivee,
        depart,
        hotelNom: (r.hotel_nom ?? '').trim(),
        hotelLien: (r.hotel_lien ?? '').trim(),
        hotelAdresse: (r.hotel_adresse ?? '').trim(),
        hotelPhoto: (r.hotel_photo ?? '').trim(),
        lat: num(r.lat),
        lng: num(r.lng),
        description: (r.description ?? '').trim(),
        photos: splitList(r.photos, ','),
        video: (r.video ?? '').trim(),
        statut: computeStatut(arrivee, depart, today, r.statut),
        photoQuery: (r.photo_query ?? '').trim(),
      } satisfies Stop;
    })
    .sort((a, b) => a.ordre - b.ordre);
}

export function toCountries(rows: Row[]): Country[] {
  return rows.map((r) => ({
    pays: (r.pays ?? '').trim(),
    capitale: (r.capitale ?? '').trim(),
    monnaie: (r.monnaie ?? '').trim(),
    langue: (r.langue ?? '').trim(),
    population: (r.population ?? '').trim(),
    histoire: (r.histoire ?? '').trim(),
    funFacts: splitList(r.fun_facts, '•'),
    photoQuery: (r.photo_query ?? '').trim(),
    photoHero: (r.photo_hero ?? '').trim(),
  }));
}

export function toQuiz(rows: Row[]): QuizQ[] {
  const b = (v: string) => (['a', 'b', 'c'].includes(v) ? (v as 'a' | 'b' | 'c') : 'a');
  return rows.map((r) => ({
    pays: (r.pays ?? '').trim(),
    question: (r.question ?? '').trim(),
    choix: [(r.choix_a ?? '').trim(), (r.choix_b ?? '').trim(), (r.choix_c ?? '').trim()],
    bonne: b((r.bonne ?? '').trim().toLowerCase()),
    explication: (r.explication ?? '').trim(),
  }));
}

/** Distance grand-cercle en km entre deux points [lat, lng]. */
export function haversine(a: [number, number], b: [number, number]): number {
  const R = 6371;
  const t = (x: number) => (x * Math.PI) / 180;
  const dLa = t(b[0] - a[0]);
  const dLo = t(b[1] - a[1]);
  const u =
    Math.sin(dLa / 2) ** 2 +
    Math.cos(t(a[0])) * Math.cos(t(b[0])) * Math.sin(dLo / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(u));
}

export interface Counters {
  pays: number;
  escales: number;
  nuits: number;
  km: number;
  jours: number;
}

/** Le retour maison (France) n'est ni un pays "visité" ni une escale. */
const isRetour = (s: Stop) => s.pays.toLowerCase() === 'france';

export function computeCounters(stops: Stop[]): Counters {
  const visites = stops.filter((s) => !isRetour(s));
  const pays = new Set(visites.map((s) => s.pays)).size;
  const escales = visites.length;
  let nuits = 0;
  for (const s of stops) {
    if (s.arrivee && s.depart) nuits += Math.round((+s.depart - +s.arrivee) / 864e5);
  }
  // Distance : on ne relie que les escales à coordonnées valides — une ligne
  // mal saisie (lat/lng vide → 0) ne doit pas créer de trajet fantôme.
  let km = 0;
  const geo = stops.filter((s) => s.lat && s.lng);
  for (let i = 1; i < geo.length; i++) {
    km += haversine([geo[i - 1].lat, geo[i - 1].lng], [geo[i].lat, geo[i].lng]);
  }
  const dates = stops.flatMap((s) => [s.arrivee, s.depart]).filter((d): d is Date => !!d);
  const min = dates.length ? new Date(Math.min(...dates.map((d) => +d))) : null;
  const max = dates.length ? new Date(Math.max(...dates.map((d) => +d))) : null;
  const jours = min && max ? Math.round((+max - +min) / 864e5) : 0;
  return { pays, escales, nuits, km: Math.round(km / 50) * 50, jours };
}

export interface Live {
  state: 'avant' | 'pendant' | 'apres';
  current: Stop | null;
  next: Stop | null;
  daysToStart: number;
  dayIndex: number;
}

export function startOfToday(): Date {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

export function computeLive(stops: Stop[], today: Date = startOfToday()): Live {
  const withDates = stops.filter((s) => s.arrivee);
  const first = withDates[0]?.arrivee ?? null;
  const dates = stops.flatMap((s) => [s.arrivee, s.depart]).filter((d): d is Date => !!d);
  const last = dates.length ? new Date(Math.max(...dates.map((d) => +d))) : null;
  const day = 864e5;

  if (first && today < first) {
    const next = stops.find((s) => !isRetour(s)) ?? null;
    return {
      state: 'avant',
      current: null,
      next,
      daysToStart: Math.round((+first - +today) / day),
      dayIndex: 0,
    };
  }
  if (last && today > last) {
    return { state: 'apres', current: null, next: null, daysToStart: 0, dayIndex: 0 };
  }
  const idx = stops.findIndex((s) => {
    const a = s.arrivee;
    const d = s.depart ?? s.arrivee;
    return a && d && today >= a && today <= d;
  });
  const current = idx >= 0 ? stops[idx] : null;
  const next = idx >= 0 ? stops.slice(idx + 1).find((s) => !isRetour(s)) ?? null : null;
  const dayIndex = first ? Math.round((+today - +first) / day) + 1 : 0;
  return { state: 'pendant', current, next, daysToStart: 0, dayIndex };
}
