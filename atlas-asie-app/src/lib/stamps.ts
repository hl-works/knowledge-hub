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

function topStars(ink: string): string {
  return `<text x="75" y="26" text-anchor="middle" font-size="11" fill="${ink}">★ ✦ ★</text>`;
}
function nameArc(id: string, txt: string, ink: string, r = 64): string {
  const off = txt.length > 9 ? '4%' : '8%';
  return `<path id="bn${id}" d="M75 ${75 + r}a${r} ${r} 0 0 1 0 ${-2 * r}" fill="none"/><text font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2.2" fill="${ink}"><textPath href="#bn${id}" startOffset="${off}">${txt.toUpperCase()}</textPath></text>`;
}
function ringDashed(ink: string, r = 71): string {
  return `<circle cx="75" cy="75" r="${r}" fill="none" stroke="${ink}" stroke-width="2" stroke-dasharray="1 4"/>`;
}

// KAZAKHSTAN — cercle · aigle de la steppe sous le soleil
const scKZ: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="75" cy="50" r="10" fill="${ink}"/>
    <g stroke="${ink}" stroke-width="1.5">${Array.from({ length: 12 }, (_, i) => { const a = (i * 30 * Math.PI) / 180; return `<line x1="${75 + 12 * Math.cos(a)}" y1="${50 + 12 * Math.sin(a)}" x2="${75 + 16 * Math.cos(a)}" y2="${50 + 16 * Math.sin(a)}"/>`; }).join('')}</g>
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M75 82 C61 70 49 72 35 84 C51 80 63 80 75 88Z"/>
      <path d="M75 82 C89 70 101 72 115 84 C99 80 87 80 75 88Z"/>
      <path d="M71 87 L75 100 L79 87Z"/>
    </g>
    <circle cx="75" cy="80" r="3" fill="${ink}"/>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${ink}" stroke-width="3"/>
  ${ringDashed(ink)}${topStars(ink)}${nameArc(id, 'Kazakhstan', ink)}`;

// KIRGHIZISTAN — cercle rayonnant · tunduk (couronne de yourte) sur les monts
const scKG: Scene = (ink, paper, id) => `
  <g fill="${ink}">${Array.from({ length: 24 }, (_, i) => { const a = (i * 15 * Math.PI) / 180; return `<path d="M${(75 + 58 * Math.cos(a - 0.05)).toFixed(1)} ${(75 + 58 * Math.sin(a - 0.05)).toFixed(1)} L${(75 + 68 * Math.cos(a)).toFixed(1)} ${(75 + 68 * Math.sin(a)).toFixed(1)} L${(75 + 58 * Math.cos(a + 0.05)).toFixed(1)} ${(75 + 58 * Math.sin(a + 0.05)).toFixed(1)}Z"/>`; }).join('')}</g>
  <circle cx="75" cy="75" r="58" fill="none" stroke="${ink}" stroke-width="3"/>
  <clipPath id="c${id}"><circle cx="75" cy="75" r="55"/></clipPath>
  <g clip-path="url(#c${id})"><path d="M18 100 L44 70 L62 90 L82 64 L104 92 L132 100Z" fill="none" stroke="${ink}" stroke-width="1.8" stroke-linejoin="round"/></g>
  <g transform="translate(75,64)">
    <circle r="17" fill="${paper}" stroke="${ink}" stroke-width="2.5"/>
    <g stroke="${ink}" stroke-width="2" fill="none"><path d="M-17 0A17 17 0 0 1 17 0"/><path d="M-12 -8A15 15 0 0 1 12 -8"/><path d="M-12 8A15 15 0 0 0 12 8"/></g>
    <line x1="-17" y1="0" x2="17" y2="0" stroke="${ink}" stroke-width="1.4"/><line x1="0" y1="-17" x2="0" y2="17" stroke="${ink}" stroke-width="1.4"/>
    <line x1="-12" y1="-12" x2="12" y2="12" stroke="${ink}" stroke-width="1"/><line x1="12" y1="-12" x2="-12" y2="12" stroke="${ink}" stroke-width="1"/>
  </g>
  ${topStars(ink)}${nameArc(id, 'Kirghizistan', ink)}`;

// MONGOLIE — cercle · ger (yourte) dans la steppe, aigles, soleil
const scMN: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="102" cy="52" r="9" fill="${ink}"/><g stroke="${ink}" stroke-width="1.5">${Array.from({ length: 8 }, (_, i) => { const a = (i * 45 * Math.PI) / 180; return `<line x1="${102 + 11 * Math.cos(a)}" y1="${52 + 11 * Math.sin(a)}" x2="${102 + 15 * Math.cos(a)}" y2="${52 + 15 * Math.sin(a)}"/>`; }).join('')}</g>
    <path d="M15 96 L38 66 L52 84 L70 56 L90 82 L110 68 L135 96Z" fill="none" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M28 52q4 -5 8 0q4 -5 8 0" fill="none" stroke="${ink}" stroke-width="1.4"/>
    <path d="M46 44q3 -4 6 0q3 -4 6 0" fill="none" stroke="${ink}" stroke-width="1.2"/>
    <path d="M60 100 V82 H90 V100" fill="${paper}" stroke="${ink}" stroke-width="2"/>
    <path d="M55 82 Q75 63 95 82" fill="none" stroke="${ink}" stroke-width="2"/>
    <line x1="75" y1="63" x2="75" y2="70" stroke="${ink}" stroke-width="1.4"/>
    <rect x="71" y="88" width="8" height="12" fill="${ink}"/>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${ink}" stroke-width="3"/>
  ${ringDashed(ink)}${topStars(ink)}${nameArc(id, 'Mongolie', ink)}`;

// CHINE — ovale vertical · pitons de Zhangjiajie dans la brume + soleil
const scCN: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><ellipse cx="75" cy="75" rx="54" ry="64"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="98" cy="42" r="8" fill="${ink}"/>
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M52 108 V58 Q52 50 57 50 Q62 50 62 58 V108Z"/>
      <path d="M66 108 V44 Q66 36 71 36 Q76 36 76 44 V108Z"/>
      <path d="M80 108 V64 Q80 56 85 56 Q90 56 90 64 V108Z"/>
      <path d="M92 108 V72 Q92 66 96 66 Q100 66 100 72 V108Z"/>
    </g>
    <g stroke="${ink}" stroke-width="1.2" opacity=".7"><path d="M40 86 q18 -5 34 0" fill="none"/><path d="M56 98 q16 -5 34 0" fill="none"/></g>
  </g>
  <ellipse cx="75" cy="75" rx="54" ry="64" fill="none" stroke="${ink}" stroke-width="3"/>
  <ellipse cx="75" cy="75" rx="60" ry="70" fill="none" stroke="${ink}" stroke-width="1.5" stroke-dasharray="1 4"/>
  <text x="75" y="24" text-anchor="middle" font-size="11" fill="${ink}">★ ✦ ★</text>
  <text x="75" y="132" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2" fill="${ink}">CHINE</text>`;

// HONG-KONG — cercle · jonque à voile rouge devant les tours
const scHK: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${id})">
    <g fill="none" stroke="${ink}" stroke-width="2"><path d="M30 74 V54 M38 74 V44 M46 74 V50"/><path d="M96 74 V48 M104 74 V40 M112 74 V52 M120 74 V58"/></g>
    <line x1="20" y1="74" x2="130" y2="74" stroke="${ink}" stroke-width="1.5"/>
    <g fill="${ink}"><path d="M62 72 V40 L84 72Z"/><path d="M60 72 V46 L44 72Z"/></g>
    <line x1="61" y1="36" x2="61" y2="74" stroke="${ink}" stroke-width="2"/>
    <path d="M46 74 H92 L86 84 H52Z" fill="${paper}" stroke="${ink}" stroke-width="2"/>
    <g stroke="${ink}" stroke-width="1.2" opacity=".7"><path d="M28 92 q10 -4 20 0t20 0 20 0 20 0" fill="none"/><path d="M34 100 q10 -4 20 0t20 0 20 0" fill="none"/></g>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${ink}" stroke-width="3"/>
  ${ringDashed(ink)}${topStars(ink)}${nameArc(id, 'Hong-Kong', ink)}`;

// MALAISIE — arche verticale · les tours jumelles Petronas + croissant
const scMY: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><ellipse cx="75" cy="75" rx="52" ry="64"/></clipPath>
  <g clip-path="url(#c${id})">
    <path d="M104 34 a11 11 0 1 0 3 15 a8.5 8.5 0 1 1 -3 -15Z" fill="${ink}"/>
    <g fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round">
      <path d="M56 116 V58 Q56 50 62 48 Q68 50 68 58 V116Z"/>
      <path d="M82 116 V58 Q82 50 88 48 Q94 50 94 58 V116Z"/>
    </g>
    <g stroke="${ink}" stroke-width="1.6"><line x1="62" y1="48" x2="62" y2="38"/><line x1="88" y1="48" x2="88" y2="38"/></g>
    <g stroke="${ink}" stroke-width="1.2" opacity=".8">${[64, 76, 88, 100].map((y) => `<line x1="56" y1="${y}" x2="68" y2="${y}"/><line x1="82" y1="${y}" x2="94" y2="${y}"/>`).join('')}</g>
    <path d="M68 72 H82 M68 76 H82" stroke="${ink}" stroke-width="2"/>
    <path d="M71 72 L75 76 L79 72 M71 76 L75 72 L79 76" stroke="${ink}" stroke-width="1" fill="none"/>
    <line x1="24" y1="116" x2="126" y2="116" stroke="${ink}" stroke-width="1.5"/>
  </g>
  <ellipse cx="75" cy="75" rx="52" ry="64" fill="none" stroke="${ink}" stroke-width="3"/>
  <text x="75" y="22" text-anchor="middle" font-size="11" fill="${ink}">★ ✦ ★</text>
  <text x="75" y="132" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2" fill="${ink}">MALAISIE</text>`;

// INDONÉSIE — coussin arrondi · volcan, palmier, mer
const scID: Scene = (ink, paper, id) => `
  <clipPath id="c${id}"><path d="M75 16 C112 16 134 38 134 75 C134 112 112 134 75 134 C38 134 16 112 16 75 C16 38 38 16 75 16Z"/></clipPath>
  <g clip-path="url(#c${id})">
    <circle cx="75" cy="46" r="8" fill="${ink}"/>
    <path d="M40 104 L66 56 Q75 44 84 56 L110 104Z" fill="${paper}" stroke="${ink}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M66 58 q9 6 18 0" fill="none" stroke="${ink}" stroke-width="1.6"/>
    <path d="M72 52 q3 8 -2 16 M78 52 q-3 8 2 16" fill="none" stroke="${ink}" stroke-width="1.6"/>
    <g stroke="${ink}" stroke-width="2" fill="none"><path d="M112 104 V78"/><path d="M112 78 q-10 -8 -20 -6 M112 78 q10 -8 20 -6 M112 78 q-6 -12 -14 -14 M112 78 q6 -12 14 -14 M112 80 q-14 -2 -22 4 M112 80 q14 -2 22 4"/></g>
    <line x1="18" y1="104" x2="132" y2="104" stroke="${ink}" stroke-width="1.5"/>
    <g stroke="${ink}" stroke-width="1.2" opacity=".6"><path d="M24 114 q10 -4 20 0t20 0 20 0 20 0" fill="none"/></g>
  </g>
  <path d="M75 16 C112 16 134 38 134 75 C134 112 112 134 75 134 C38 134 16 112 16 75 C16 38 38 16 75 16Z" fill="none" stroke="${ink}" stroke-width="3"/>
  ${topStars(ink)}
  <text x="75" y="130" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="11.5" letter-spacing="1.6" fill="${ink}">INDONÉSIE</text>`;

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
