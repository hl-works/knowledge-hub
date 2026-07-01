// Carte interactive de l'itinéraire (Leaflet) — élément signature de la home.
// Fond sombre premium, tracé orange animé, pins colorés par statut, et pins
// cliquables qui renvoient vers l'étape du Parcours et la fiche Pays.
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { Stop } from './model';

export function slugPays(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

const fmt = (d: Date | null) =>
  d ? d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' }) : '';

const STATUT_LABEL: Record<Stop['statut'], string> = {
  passe: 'Passé',
  'en-cours': 'En ce moment',
  'a-venir': 'À venir',
};

export function initMap(el: HTMLElement, stops: Stop[], base: string): void {
  // On exclut le départ/retour France : la carte se concentre sur l'Asie.
  const geo = stops.filter((s) => s.lat && s.lng && s.pays.toLowerCase() !== 'france');
  if (!geo.length) return;
  const reduced = matchMedia('(prefers-reduced-motion:reduce)').matches;

  const map = L.map(el, {
    zoomControl: true,
    scrollWheelZoom: false, // évite de capturer le scroll de la page
    attributionControl: true,
  });

  L.tileLayer(
    'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    {
      subdomains: 'abcd',
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    },
  ).addTo(map);

  const latlngs = geo.map((s) => [s.lat, s.lng] as [number, number]);

  // Tracé : une ligne "glow" large + une ligne fine animée par-dessus.
  L.polyline(latlngs, { color: '#FA4616', weight: 8, opacity: 0.28, className: 'route-glow' }).addTo(map);
  const line = L.polyline(latlngs, {
    color: '#FA4616',
    weight: 3,
    opacity: 0.95,
    className: reduced ? 'route-line' : 'route-line route-line--anim',
    dashArray: '1 9',
    lineCap: 'round',
  }).addTo(map);

  // Marqueurs par escale.
  geo.forEach((s, i) => {
    const cls =
      s.statut === 'en-cours' && !reduced ? 'pin pin--now pin--pulse' : `pin pin--${s.statut}`;
    const icon = L.divIcon({
      className: 'pin-wrap',
      html: `<span class="${cls}"></span>`,
      iconSize: [18, 18],
      iconAnchor: [9, 9],
    });
    const paysHref = `${base}pays#${slugPays(s.pays)}`;
    const etapeHref = `${base}parcours#e-${s.ordre}`;
    const dates = [fmt(s.arrivee), fmt(s.depart)].filter(Boolean).join(' → ');
    const hotel = s.hotelNom ? `<div class="pp-hotel">🏨 ${s.hotelNom}</div>` : '';
    const popup = `
      <div class="pp">
        <span class="pp-tag pp-tag--${s.statut}">${STATUT_LABEL[s.statut]}</span>
        <div class="pp-ville">${s.ville}</div>
        <div class="pp-sub">${s.pays}${dates ? ' · ' + dates : ''}</div>
        ${hotel}
        <div class="pp-links">
          <a href="${etapeHref}">Voir l'étape →</a>
          <a href="${paysHref}">${s.pays} →</a>
        </div>
      </div>`;
    L.marker([s.lat, s.lng], { icon, title: s.ville, riseOnHover: true })
      .addTo(map)
      .bindPopup(popup, { closeButton: true, offset: [0, -4] });
  });

  map.fitBounds(line.getBounds(), { padding: [40, 40] });
  setTimeout(() => map.invalidateSize(), 250);
  // Réactive le zoom molette seulement quand la carte a le focus / au clic.
  map.on('focus', () => map.scrollWheelZoom.enable());
  map.on('blur', () => map.scrollWheelZoom.disable());
}
