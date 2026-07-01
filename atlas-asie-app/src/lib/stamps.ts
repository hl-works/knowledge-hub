// Tampons « eki » — une forme + une scène qui raconte le pays, à la manière des
// tampons de gare/temple japonais. Encre = couleur signature du pays (mur
// multicolore façon carnet). Petit format = drapeau stylisé.
// Tout renvoie une CHAÎNE SVG, injectable en innerHTML (client) comme en SSR.

export const CODE: Record<string, string> = {
  Kazakhstan: 'KZ', Kirghizistan: 'KG', Mongolie: 'MN', Chine: 'CN',
  'Hong-Kong': 'HK', 'Hong Kong': 'HK', Indonésie: 'ID', Malaisie: 'MY',
};
export const codeForPays = (nom: string): string => CODE[nom] ?? nom.slice(0, 2).toUpperCase();

// Couleur signature par pays : choisie pour être évocatrice ET pour donner un mur
// bien multicolore (les drapeaux sont presque tous rouges → on varie).
const COL: Record<string, string> = {
  KZ: '#0E9CB8', // turquoise — ciel de la steppe
  KG: '#D62839', // rouge — drapeau
  MN: '#C0552B', // terracotta — Gobi / steppe
  CN: '#C1121F', // rouge impérial
  HK: '#C71F6B', // magenta — la fleur de bauhinia
  MY: '#12457A', // bleu nuit — les tours
  ID: '#0E8A6B', // vert-jade — jungle & mer
};
export const colorForPays = (nom: string): string => COL[codeForPays(nom)] ?? '#C9330B';

let _uid = 0;

// ---------- petites aides géométriques ----------
function star(cx: number, cy: number, r: number, fill: string, rot = 0): string {
  let p = '';
  for (let i = 0; i < 5; i++) {
    const a = ((-90 + rot + i * 72) * Math.PI) / 180;
    const a2 = a + (36 * Math.PI) / 180;
    p += (i ? 'L' : 'M') + (cx + r * Math.cos(a)).toFixed(1) + ' ' + (cy + r * Math.sin(a)).toFixed(1) +
      'L' + (cx + r * 0.4 * Math.cos(a2)).toFixed(1) + ' ' + (cy + r * 0.4 * Math.sin(a2)).toFixed(1);
  }
  return `<path d="${p}Z" fill="${fill}"/>`;
}

// ---------- drapeaux stylisés (petit format) ----------
export function flag(code: string): string {
  let g = '';
  switch (code) {
    case 'KZ': g = `<rect width="30" height="20" fill="#00AFCA"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({ length: 12 }, (_, i) => { const a = (i * 30 * Math.PI) / 180; return `<line x1="16" y1="9" x2="${16 + 6 * Math.cos(a)}" y2="${9 + 6 * Math.sin(a)}"/>`; }).join('')}</g><circle cx="16" cy="9" r="3.4" fill="#FFD200"/><rect width="2" height="20" fill="#FFD200"/>`; break;
    case 'KG': g = `<rect width="30" height="20" fill="#E8112D"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({ length: 16 }, (_, i) => { const a = (i * 22.5 * Math.PI) / 180; return `<line x1="15" y1="10" x2="${15 + 6 * Math.cos(a)}" y2="${10 + 6 * Math.sin(a)}"/>`; }).join('')}</g><circle cx="15" cy="10" r="3.6" fill="#FFD200"/><line x1="12" y1="10" x2="18" y2="10" stroke="#E8112D" stroke-width="0.5"/><line x1="15" y1="7.5" x2="15" y2="12.5" stroke="#E8112D" stroke-width="0.5"/>`; break;
    case 'MN': g = `<rect width="10" height="20" fill="#C4272E"/><rect x="10" width="10" height="20" fill="#015197"/><rect x="20" width="10" height="20" fill="#C4272E"/><g fill="#F9CF02"><circle cx="5" cy="6" r="1.1"/><path d="M3.6 8h2.8v1H3.6z"/><path d="M3.8 10.2 5 9l1.2 1.2-1.2 1.2z"/><path d="M3.6 12.5h2.8v1H3.6z"/></g>`; break;
    case 'CN': g = `<rect width="30" height="20" fill="#DE2910"/>${star(6, 5, 3.4, '#FFDE00', 0)}${star(11, 2.4, 1.1, '#FFDE00', 20)}${star(12.6, 4.6, 1.1, '#FFDE00', 40)}${star(12.6, 7.6, 1.1, '#FFDE00', -40)}${star(11, 9.8, 1.1, '#FFDE00', -20)}`; break;
    case 'HK': g = `<rect width="30" height="20" fill="#DE2910"/><g fill="#fff">${Array.from({ length: 5 }, (_, i) => { const a = ((-90 + i * 72) * Math.PI) / 180; return `<ellipse cx="${15 + 3.4 * Math.cos(a)}" cy="${10 + 3.4 * Math.sin(a)}" rx="1.5" ry="3.4" transform="rotate(${i * 72} ${15 + 3.4 * Math.cos(a)} ${10 + 3.4 * Math.sin(a)})"/>`; }).join('')}</g><circle cx="15" cy="10" r="1.3" fill="#DE2910"/>`; break;
    case 'MY': g = `${Array.from({ length: 14 }, (_, i) => `<rect y="${(i * 20) / 14}" width="30" height="${20 / 14}" fill="${i % 2 ? '#fff' : '#CC0001'}"/>`).join('')}<rect width="15" height="${(20 / 14) * 8}" fill="#010066"/><circle cx="6.5" cy="5.5" r="3" fill="#FFCC00"/><circle cx="7.8" cy="5.5" r="2.6" fill="#010066"/>${star(10.4, 5.5, 1.8, '#FFCC00', 0)}`; break;
    case 'ID': g = `<rect width="30" height="10" fill="#FF0000"/><rect y="10" width="30" height="10" fill="#fff"/>`; break;
    default: g = `<rect width="30" height="20" fill="#9A8268"/>`;
  }
  return `<svg viewBox="0 0 30 20" preserveAspectRatio="none" role="img" aria-label="Drapeau ${code}">${g}</svg>`;
}

// ---------- tampons eki : une scène par pays ----------
type EkiOpts = { size?: number; ink?: string; paper?: string; opacity?: number };
type Scene = (ink: string, paper: string, id: string) => string;

function topOrn(ink: string): string {
  return `<text x="75" y="27" text-anchor="middle" font-size="10" letter-spacing="2" fill="${ink}">★ ✦ ★</text>`;
}
// Nom du pays, arqué le long du bas dans une bande propre — serif élégant (Diptyque/Assouline).
function nameArc(id: string, txt: string, ink: string, r = 60): string {
  return `<path id="bn${id}" d="M${(75 - r).toFixed(1)} 75 A ${r} ${r} 0 0 0 ${(75 + r).toFixed(1)} 75" fill="none"/><text font-family="'Fraunces',Georgia,serif" font-weight="600" font-size="12" letter-spacing="1.3" fill="${ink}" text-anchor="middle"><textPath href="#bn${id}" startOffset="50%">${txt.toUpperCase()}</textPath></text>`;
}
function rays(cx: number, cy: number, r0: number, r1: number, n: number, ink: string, w = 1.4): string {
  let s = '';
  for (let i = 0; i < n; i++) { const a = (i * (360 / n) * Math.PI) / 180; s += `<line x1="${(cx + r0 * Math.cos(a)).toFixed(1)}" y1="${(cy + r0 * Math.sin(a)).toFixed(1)}" x2="${(cx + r1 * Math.cos(a)).toFixed(1)}" y2="${(cy + r1 * Math.sin(a)).toFixed(1)}"/>`; }
  return `<g stroke="${ink}" stroke-width="${w}">${s}</g>`;
}
function rayCrown(cx: number, cy: number, r0: number, r1: number, n: number, ink: string): string {
  let s = '';
  for (let i = 0; i < n; i++) { const a = (i * (360 / n) * Math.PI) / 180; const w = 0.055; s += `<path d="M${(cx + r0 * Math.cos(a - w)).toFixed(1)} ${(cy + r0 * Math.sin(a - w)).toFixed(1)} L${(cx + r1 * Math.cos(a)).toFixed(1)} ${(cy + r1 * Math.sin(a)).toFixed(1)} L${(cx + r0 * Math.cos(a + w)).toFixed(1)} ${(cy + r0 * Math.sin(a + w)).toFixed(1)}Z"/>`; }
  return `<g fill="${ink}">${s}</g>`;
}
// Cadres : double filet fin (signature Diptyque).
function circleFrame(ink: string): string {
  return `<circle cx="75" cy="75" r="70" fill="none" stroke="${ink}" stroke-width="2.4"/><circle cx="75" cy="75" r="66" fill="none" stroke="${ink}" stroke-width="0.9"/>`;
}
function ovalFrame(ink: string, rx: number, ry: number): string {
  return `<ellipse cx="75" cy="75" rx="${rx}" ry="${ry}" fill="none" stroke="${ink}" stroke-width="2.4"/><ellipse cx="75" cy="75" rx="${rx - 4}" ry="${ry - 4}" fill="none" stroke="${ink}" stroke-width="0.9"/>`;
}
const CUSHION = 'M75 12 C114 12 138 36 138 75 C138 114 114 138 75 138 C36 138 12 114 12 75 C12 36 36 12 75 12Z';
const CUSHION_IN = 'M75 17 C110 17 133 40 133 75 C133 110 110 133 75 133 C40 133 17 110 17 75 C17 40 40 17 75 17Z';

// KAZAKHSTAN — cercle · aigle de la steppe sous le soleil
const scKZ: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="75" cy="48" r="8" fill="${ink}"/>${rays(75, 48, 10, 14, 12, ink)}
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M75 78 C63 68 53 70 43 79 C55 76 65 76 75 83Z"/>
      <path d="M75 78 C87 68 97 70 107 79 C95 76 85 76 75 83Z"/>
      <path d="M72 82 L75 92 L78 82Z"/>
    </g>
    <circle cx="75" cy="77" r="2.6" fill="${ink}"/>
  </g>
  ${circleFrame(ink)}${topOrn(ink)}${nameArc(id, 'Kazakhstan', ink, 60)}`;

// KIRGHIZISTAN — cercle · le soleil-tunduk (emblème du drapeau) sur les monts
const scKG: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${id})">
    <path d="M20 96 L44 74 L60 88 L80 68 L100 90 L130 96Z" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linejoin="round"/>
    ${rays(75, 53, 14, 19, 20, ink, 1.2)}
    <circle cx="75" cy="53" r="13" fill="${paper}" stroke="${ink}" stroke-width="2"/>
    <g transform="translate(75,53)" stroke="${ink}" fill="none">
      <path d="M-11 0A11 11 0 0 1 11 0" stroke-width="1.5"/>
      <path d="M-8 -5A10 10 0 0 1 8 -5" stroke-width="1.1"/>
      <path d="M-8 5A10 10 0 0 0 8 5" stroke-width="1.1"/>
      <line x1="-11" y1="0" x2="11" y2="0" stroke-width="1.1"/><line x1="0" y1="-11" x2="0" y2="11" stroke-width="1.1"/>
    </g>
  </g>
  ${circleFrame(ink)}${topOrn(ink)}${nameArc(id, 'Kirghizistan', ink, 60)}`;

// MONGOLIE — cercle · ger (yourte) dans la steppe, aigles, soleil
const scMN: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="100" cy="50" r="8" fill="${ink}"/>${rays(100, 50, 10, 13, 8, ink)}
    <path d="M22 94 L42 68 L54 82 L70 58 L88 80 L106 68 L128 94Z" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M32 52q4 -5 8 0q4 -5 8 0" fill="none" stroke="${ink}" stroke-width="1.3"/>
    <path d="M60 96 V80 H90 V96" fill="${paper}" stroke="${ink}" stroke-width="2"/>
    <path d="M55 80 Q75 62 95 80" fill="none" stroke="${ink}" stroke-width="2"/>
    <line x1="75" y1="61" x2="75" y2="68" stroke="${ink}" stroke-width="1.3"/>
    <rect x="71" y="85" width="8" height="11" fill="${ink}"/>
  </g>
  ${circleFrame(ink)}${topOrn(ink)}${nameArc(id, 'Mongolie', ink, 60)}`;

// CHINE — ovale vertical · pitons de Zhangjiajie dans la brume + soleil
const scCN: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><ellipse cx="75" cy="72" rx="46" ry="54"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="96" cy="42" r="7" fill="${ink}"/>
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M54 100 V56 Q54 49 58 49 Q62 49 62 56 V100Z"/>
      <path d="M66 100 V44 Q66 37 71 37 Q76 37 76 44 V100Z"/>
      <path d="M80 100 V60 Q80 53 84 53 Q88 53 88 60 V100Z"/>
      <path d="M90 100 V70 Q90 64 94 64 Q98 64 98 70 V100Z"/>
    </g>
    <g stroke="${ink}" stroke-width="1.1" opacity=".65"><path d="M46 84 q16 -5 30 0" fill="none"/><path d="M58 94 q14 -5 28 0" fill="none"/></g>
  </g>
  ${ovalFrame(ink, 56, 68)}${topOrn(ink)}${nameArc(id, 'Chine', ink, 56)}`;

// HONG-KONG — cercle · jonque à voile devant les tours
const scHK: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${id})">
    <g fill="none" stroke="${ink}" stroke-width="2"><path d="M34 72 V54 M42 72 V46 M50 72 V52"/><path d="M96 72 V50 M104 72 V42 M112 72 V54"/></g>
    <line x1="26" y1="72" x2="124" y2="72" stroke="${ink}" stroke-width="1.4"/>
    <g fill="${ink}"><path d="M62 70 V42 L82 70Z"/><path d="M60 70 V48 L46 70Z"/></g>
    <line x1="61" y1="38" x2="61" y2="72" stroke="${ink}" stroke-width="2"/>
    <path d="M48 72 H90 L84 81 H54Z" fill="${paper}" stroke="${ink}" stroke-width="2"/>
    <g stroke="${ink}" stroke-width="1.1" opacity=".65"><path d="M34 90 q9 -4 18 0t18 0 18 0" fill="none"/></g>
  </g>
  ${circleFrame(ink)}${topOrn(ink)}${nameArc(id, 'Hong-Kong', ink, 60)}`;

// MALAISIE — ovale vertical · les tours jumelles Petronas + croissant
const scMY: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><ellipse cx="75" cy="72" rx="46" ry="54"/></clipPath>
  <g clip-path="url(#c${id})">
    <path d="M99 36 a10 10 0 1 0 3 14 a8 8 0 1 1 -3 -14Z" fill="${ink}"/>
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M58 100 V58 Q58 51 63 49 Q68 51 68 58 V100Z"/>
      <path d="M82 100 V58 Q82 51 87 49 Q92 51 92 58 V100Z"/>
    </g>
    <g stroke="${ink}" stroke-width="1.5"><line x1="63" y1="49" x2="63" y2="40"/><line x1="87" y1="49" x2="87" y2="40"/></g>
    <g stroke="${ink}" stroke-width="1.1" opacity=".8">${[64, 74, 84, 94].map((y) => `<line x1="58" y1="${y}" x2="68" y2="${y}"/><line x1="82" y1="${y}" x2="92" y2="${y}"/>`).join('')}</g>
    <path d="M68 70 H82 M68 74 H82" stroke="${ink}" stroke-width="1.8"/>
  </g>
  ${ovalFrame(ink, 56, 68)}${topOrn(ink)}${nameArc(id, 'Malaisie', ink, 56)}`;

// INDONÉSIE — coussin arrondi · volcan, palmier, mer
const scID: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="70" r="50"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="75" cy="44" r="8" fill="${ink}"/>
    <path d="M42 92 L66 54 Q75 43 84 54 L108 92Z" fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M66 56 q9 6 18 0" fill="none" stroke="${ink}" stroke-width="1.5"/>
    <g stroke="${ink}" stroke-width="2" fill="none"><path d="M108 92 V70"/><path d="M108 70 q-9 -7 -18 -5 M108 70 q9 -7 18 -5 M108 70 q-5 -11 -12 -13 M108 70 q5 -11 12 -13"/></g>
    <line x1="24" y1="92" x2="126" y2="92" stroke="${ink}" stroke-width="1.4"/>
    <g stroke="${ink}" stroke-width="1.1" opacity=".55"><path d="M30 100 q9 -4 18 0t18 0 18 0" fill="none"/></g>
  </g>
  <path d="${CUSHION}" fill="none" stroke="${ink}" stroke-width="2.4"/><path d="${CUSHION_IN}" fill="none" stroke="${ink}" stroke-width="0.9"/>
  ${topOrn(ink)}${nameArc(id, 'Indonésie', ink, 55)}`;

const SCENES: Record<string, Scene> = { KZ: scKZ, KG: scKG, MN: scMN, CN: scCN, HK: scHK, MY: scMY, ID: scID };

// Tampon générique (pays inconnu) — passeport rond épuré.
const scFallback = (ink: string, _p: string, id: string, code: string): string => `
  <circle cx="75" cy="75" r="72" fill="none" stroke="${ink}" stroke-width="3.5"/>
  <circle cx="75" cy="75" r="50" fill="none" stroke="${ink}" stroke-width="1.5"/>
  ${topStars(ink)}<text x="75" y="86" text-anchor="middle" font-family="Anton,sans-serif" font-size="30" fill="${ink}">${code}</text>`;

/**
 * Tampon eki d'un pays (chaîne SVG).
 * Par défaut encré dans la couleur du pays sur fond papier (fonds clairs).
 * Sur fond coloré (bandeau de fiche), passer ink:'#fff' + paper:'none'.
 */
export function stampEki(pays: string, opts: EkiOpts = {}): string {
  const code = codeForPays(pays);
  const ink = opts.ink ?? colorForPays(pays);
  const paper = opts.paper ?? '#FFFDF8';
  const size = opts.size ?? 138;
  const op = opts.opacity ?? 1;
  const id = code + '_' + _uid++;
  const scene = SCENES[code];
  const inner = scene ? scene(ink, paper, id) : scFallback(ink, paper, id, code);
  return `<svg class="medallion" width="${size}" height="${size}" viewBox="0 0 150 150" role="img" aria-label="Tampon ${pays}"${op !== 1 ? ` style="opacity:${op}"` : ''}>${inner}</svg>`;
}
