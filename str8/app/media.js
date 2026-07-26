/* Str8 — médias blueprint (SVG schématiques, style « instrument »).
   Chaque scène = corps neutre (gris) + zone active / flèches / élastique en lime.
   Volontairement schématique (repère de mouvement), remplaçable par une vidéo.
   viewBox commun 0 0 240 200. */

const SVG = (inner) => `<svg viewBox="0 0 240 200" class="bp" role="img">${inner}</svg>`;

// briques réutilisables
const head = (x, y, r = 15) => `<circle class="bp-head" cx="${x}" cy="${y}" r="${r}"/>`;
const lbl  = (x, y, t) => `<text class="bp-lbl" x="${x}" y="${y}" text-anchor="middle">${t}</text>`;

const MEDIA = {
  // ---- debout, de face : ouverture band pull-apart / reverse fly ----
  bandOpen: SVG(`
    ${head(120,40)}
    <path class="bp-body" d="M120 55 V120"/>
    <path class="bp-body" d="M120 64 L64 88"/>
    <path class="bp-body" d="M120 64 L176 88"/>
    <path class="bp-body" d="M120 118 L100 176"/>
    <path class="bp-body" d="M120 118 L140 176"/>
    <rect class="bp-zone" x="92" y="58" width="56" height="30" rx="8"/>
    ${lbl(120,52,'OMOPLATES')}
    <path class="bp-band" d="M64 88 Q120 74 176 88"/>
    <path class="bp-arrow" d="M60 96 L52 90 L56 100"/>
    <path class="bp-arrow" d="M180 96 L188 90 L184 100"/>`),

  // ---- debout, de face : rowing (coudes tirés en arrière) ----
  row: SVG(`
    ${head(120,40)}
    <path class="bp-body" d="M120 55 V120"/>
    <path class="bp-body" d="M120 64 L92 92 L120 104"/>
    <path class="bp-body" d="M120 64 L148 92 L120 104"/>
    <path class="bp-body" d="M120 118 L100 176"/>
    <path class="bp-body" d="M120 118 L140 176"/>
    <rect class="bp-zone" x="96" y="60" width="48" height="26" rx="8"/>
    ${lbl(120,54,'DOS')}
    <path class="bp-band" d="M120 104 L120 150"/>
    <path class="bp-arrow" d="M112 76 L104 70 L108 80"/>
    <path class="bp-arrow" d="M128 76 L136 70 L132 80"/>`),

  // ---- debout, de face : face pull / Y raise (coudes hauts) ----
  faceHigh: SVG(`
    ${head(120,44)}
    <path class="bp-body" d="M120 59 V122"/>
    <path class="bp-body" d="M120 66 L88 52 L70 66"/>
    <path class="bp-body" d="M120 66 L152 52 L170 66"/>
    <path class="bp-body" d="M120 120 L102 176"/>
    <path class="bp-body" d="M120 120 L138 176"/>
    <rect class="bp-zone" x="94" y="46" width="52" height="26" rx="8"/>
    ${lbl(120,40,'TRAPÈZES')}
    <path class="bp-band" d="M70 66 Q120 84 170 66"/>
    <path class="bp-arrow" d="M74 60 L66 56 L70 66"/>
    <path class="bp-arrow" d="M166 60 L174 56 L170 66"/>`),

  // ---- de profil : hip hinge / good morning ----
  hinge: SVG(`
    ${head(78,58)}
    <path class="bp-body" d="M84 70 Q120 92 150 104"/>
    <path class="bp-body" d="M150 104 L150 176"/>
    <path class="bp-body" d="M110 88 L112 140"/>
    <path class="bp-dash" d="M150 60 L150 176"/>
    <rect class="bp-zone" x="96" y="78" width="60" height="26" rx="10" transform="rotate(18 126 91)"/>
    ${lbl(128,52,'CHARNIÈRE DE HANCHE')}
    <path class="bp-arrow" d="M92 96 q26 18 52 22"/>`),

  // ---- quadrupédie : bird dog ----
  quad: SVG(`
    ${head(58,86)}
    <path class="bp-body" d="M66 92 Q120 78 176 92"/>
    <path class="bp-body" d="M78 96 L80 150"/>
    <path class="bp-body" d="M160 96 L162 150"/>
    <path class="bp-body" d="M66 92 L36 70"/>
    <path class="bp-body" d="M176 92 L212 74"/>
    <rect class="bp-zone" x="96" y="72" width="56" height="22" rx="8"/>
    ${lbl(124,66,'GAINAGE + DOS')}
    <path class="bp-dash" d="M36 70 L212 74"/>`),

  // ---- quadrupédie : cat-cow ----
  catcow: SVG(`
    ${head(60,92)}
    <path class="bp-body" d="M68 96 Q120 66 172 96"/>
    <path class="bp-body" d="M84 92 L86 150"/>
    <path class="bp-body" d="M156 92 L158 150"/>
    <path class="bp-body" d="M68 96 L60 122"/>
    <rect class="bp-zone" x="98" y="68" width="48" height="22" rx="8"/>
    ${lbl(122,62,'MOBILITÉ RACHIS')}
    <path class="bp-arrow" d="M120 60 q0 -8 0 -14"/>`),

  // ---- sur le dos : dead bug ----
  deadbug: SVG(`
    <path class="bp-dash" d="M40 140 L210 140"/>
    ${head(56,124)}
    <path class="bp-body" d="M64 130 L170 132"/>
    <path class="bp-body" d="M96 130 L110 92 L112 74"/>
    <path class="bp-body" d="M140 132 L156 96 L160 78"/>
    <path class="bp-body" d="M170 132 L182 108"/>
    <rect class="bp-zone" x="92" y="120" width="56" height="20" rx="8"/>
    ${lbl(120,116,'GAINAGE PROFOND')}`),

  // ---- de profil : planche ----
  plank: SVG(`
    <path class="bp-dash" d="M30 150 L214 150"/>
    ${head(52,96)}
    <path class="bp-body" d="M60 100 L184 138"/>
    <path class="bp-body" d="M74 106 L70 148"/>
    <path class="bp-body" d="M184 138 L206 148"/>
    <rect class="bp-zone" x="96" y="104" width="66" height="22" rx="10" transform="rotate(17 129 115)"/>
    ${lbl(128,92,'LIGNE GAINÉE')}`),

  // ---- de face : side plank ----
  sideplank: SVG(`
    <path class="bp-dash" d="M40 158 L206 158"/>
    ${head(60,72)}
    <path class="bp-body" d="M68 78 L182 150"/>
    <path class="bp-body" d="M74 82 L72 156"/>
    <path class="bp-body" d="M96 96 L96 60"/>
    <rect class="bp-zone" x="92" y="96" width="52" height="22" rx="10" transform="rotate(28 118 107)"/>
    ${lbl(120,50,'OBLIQUES')}`),

  // ---- assis : extension thoracique sur chaise ----
  seatedExt: SVG(`
    <path class="bp-body" d="M150 118 L200 118"/>
    <path class="bp-body" d="M164 118 L164 168"/>
    <path class="bp-body" d="M196 118 L196 168"/>
    <path class="bp-body" d="M196 118 L196 84"/>
    ${head(150,58)}
    <path class="bp-body" d="M150 72 Q160 96 176 104"/>
    <path class="bp-body" d="M150 78 L118 66"/>
    <rect class="bp-zone" x="150" y="74" width="42" height="22" rx="8" transform="rotate(-18 171 85)"/>
    ${lbl(128,44,'EXTENSION HAUT DU DOS')}
    <path class="bp-arrow" d="M150 46 q-8 -6 -18 -6"/>`),

  // ---- au sol : cobra léger ----
  cobra: SVG(`
    <path class="bp-dash" d="M30 156 L214 156"/>
    ${head(180,96)}
    <path class="bp-body" d="M172 104 Q150 128 60 150"/>
    <path class="bp-body" d="M150 120 L150 152"/>
    <rect class="bp-zone" x="120" y="112" width="52" height="22" rx="10" transform="rotate(-24 146 123)"/>
    ${lbl(120,96,'EXTENSION DOUCE')}
    <path class="bp-arrow" d="M186 84 q4 -8 12 -12"/>`),

  // ---- de face : étirement pectoral (encadrement de porte) ----
  pec: SVG(`
    ${head(120,42)}
    <path class="bp-body" d="M120 57 V120"/>
    <path class="bp-body" d="M120 66 L74 60"/>
    <path class="bp-body" d="M120 66 L166 60"/>
    <path class="bp-body" d="M120 118 L102 176"/>
    <path class="bp-body" d="M120 118 L138 176"/>
    <rect class="bp-zone" x="96" y="72" width="48" height="22" rx="8"/>
    ${lbl(120,66,'PECTORAUX')}
    <path class="bp-arrow" d="M78 52 l-8 -4 l4 8"/>
    <path class="bp-arrow" d="M162 52 l8 -4 l-4 8"/>`),

  // ---- de profil : wall slide ----
  wallslide: SVG(`
    <path class="bp-dash" d="M180 30 L180 178"/>
    ${head(150,52)}
    <path class="bp-body" d="M150 66 V126"/>
    <path class="bp-body" d="M150 74 L120 56 L112 34"/>
    <path class="bp-body" d="M150 124 L150 176"/>
    <rect class="bp-zone" x="110" y="40" width="46" height="24" rx="8"/>
    ${lbl(120,30,'GLISSÉ AU MUR')}
    <path class="bp-arrow" d="M116 44 q-4 -8 -2 -16"/>`),

  // ---- assis : respiration costale ----
  breath: SVG(`
    ${head(120,52)}
    <path class="bp-body" d="M120 67 V128"/>
    <path class="bp-body" d="M120 78 L96 104"/>
    <path class="bp-body" d="M120 78 L144 104"/>
    <path class="bp-body" d="M120 126 L104 172"/>
    <path class="bp-body" d="M120 126 L136 172"/>
    <ellipse class="bp-zone" cx="120" cy="98" rx="34" ry="20"/>
    ${lbl(120,44,'RESPIRATION COSTALE')}
    <path class="bp-arrow" d="M86 98 q-8 0 -14 0"/>
    <path class="bp-arrow" d="M154 98 q8 0 14 0"/>`),

  // ---- debout : maintien isométrique ----
  iso: SVG(`
    ${head(120,42)}
    <path class="bp-body" d="M120 57 V120"/>
    <path class="bp-body" d="M120 66 L86 88"/>
    <path class="bp-body" d="M120 66 L154 88"/>
    <path class="bp-body" d="M120 118 L102 176"/>
    <path class="bp-body" d="M120 118 L138 176"/>
    <path class="bp-band" d="M86 88 Q120 100 154 88"/>
    ${lbl(120,54,'MAINTIEN — 0 MOUVEMENT')}
    <path class="bp-arrow" d="M120 150 v10 M116 156 l4 6 l4 -6"/>`),

  // ---- quadrupédie : rotation thoracique / thread the needle ----
  rotation: SVG(`
    ${head(58,88)}
    <path class="bp-body" d="M66 94 Q120 80 174 94"/>
    <path class="bp-body" d="M80 96 L82 150"/>
    <path class="bp-body" d="M158 96 L160 150"/>
    <path class="bp-body" d="M120 86 L150 56"/>
    <rect class="bp-zone" x="100" y="66" width="44" height="22" rx="8" transform="rotate(-20 122 77)"/>
    ${lbl(126,52,'ROTATION THORACIQUE')}
    <path class="bp-arrow" d="M150 56 q8 -2 14 2"/>`),
};

if (typeof window !== 'undefined') window.MEDIA = MEDIA;
