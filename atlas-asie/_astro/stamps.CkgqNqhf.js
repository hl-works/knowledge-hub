const M={Kazakhstan:"KZ",Kirghizistan:"KG",Mongolie:"MN",Chine:"CN","Hong-Kong":"HK","Hong Kong":"HK",Indonésie:"ID",Malaisie:"MY"},f=t=>M[t]??t.slice(0,2).toUpperCase(),g={KZ:"#0E9CB8",KG:"#D62839",MN:"#C0552B",CN:"#C1121F",HK:"#C71F6B",MY:"#12457A",ID:"#0E8A6B"},p=t=>g[f(t)]??"#C9330B";let y=0;function h(t,r,e,l,o=0){let i="";for(let s=0;s<5;s++){const c=(-90+o+s*72)*Math.PI/180,n=c+36*Math.PI/180;i+=(s?"L":"M")+(t+e*Math.cos(c)).toFixed(1)+" "+(r+e*Math.sin(c)).toFixed(1)+"L"+(t+e*.4*Math.cos(n)).toFixed(1)+" "+(r+e*.4*Math.sin(n)).toFixed(1)}return`<path d="${i}Z" fill="${l}"/>`}function Z(t){let r="";switch(t){case"KZ":r=`<rect width="30" height="20" fill="#00AFCA"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({length:12},(e,l)=>{const o=l*30*Math.PI/180;return`<line x1="16" y1="9" x2="${16+6*Math.cos(o)}" y2="${9+6*Math.sin(o)}"/>`}).join("")}</g><circle cx="16" cy="9" r="3.4" fill="#FFD200"/><rect width="2" height="20" fill="#FFD200"/>`;break;case"KG":r=`<rect width="30" height="20" fill="#E8112D"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({length:16},(e,l)=>{const o=l*22.5*Math.PI/180;return`<line x1="15" y1="10" x2="${15+6*Math.cos(o)}" y2="${10+6*Math.sin(o)}"/>`}).join("")}</g><circle cx="15" cy="10" r="3.6" fill="#FFD200"/><line x1="12" y1="10" x2="18" y2="10" stroke="#E8112D" stroke-width="0.5"/><line x1="15" y1="7.5" x2="15" y2="12.5" stroke="#E8112D" stroke-width="0.5"/>`;break;case"MN":r='<rect width="10" height="20" fill="#C4272E"/><rect x="10" width="10" height="20" fill="#015197"/><rect x="20" width="10" height="20" fill="#C4272E"/><g fill="#F9CF02"><circle cx="5" cy="6" r="1.1"/><path d="M3.6 8h2.8v1H3.6z"/><path d="M3.8 10.2 5 9l1.2 1.2-1.2 1.2z"/><path d="M3.6 12.5h2.8v1H3.6z"/></g>';break;case"CN":r=`<rect width="30" height="20" fill="#DE2910"/>${h(6,5,3.4,"#FFDE00",0)}${h(11,2.4,1.1,"#FFDE00",20)}${h(12.6,4.6,1.1,"#FFDE00",40)}${h(12.6,7.6,1.1,"#FFDE00",-40)}${h(11,9.8,1.1,"#FFDE00",-20)}`;break;case"HK":r=`<rect width="30" height="20" fill="#DE2910"/><g fill="#fff">${Array.from({length:5},(e,l)=>{const o=(-90+l*72)*Math.PI/180;return`<ellipse cx="${15+3.4*Math.cos(o)}" cy="${10+3.4*Math.sin(o)}" rx="1.5" ry="3.4" transform="rotate(${l*72} ${15+3.4*Math.cos(o)} ${10+3.4*Math.sin(o)})"/>`}).join("")}</g><circle cx="15" cy="10" r="1.3" fill="#DE2910"/>`;break;case"MY":r=`${Array.from({length:14},(e,l)=>`<rect y="${l*20/14}" width="30" height="${20/14}" fill="${l%2?"#fff":"#CC0001"}"/>`).join("")}<rect width="15" height="${20/14*8}" fill="#010066"/><circle cx="6.5" cy="5.5" r="3" fill="#FFCC00"/><circle cx="7.8" cy="5.5" r="2.6" fill="#010066"/>${h(10.4,5.5,1.8,"#FFCC00",0)}`;break;case"ID":r='<rect width="30" height="10" fill="#FF0000"/><rect y="10" width="30" height="10" fill="#fff"/>';break;default:r='<rect width="30" height="20" fill="#9A8268"/>'}return`<svg viewBox="0 0 30 20" preserveAspectRatio="none" role="img" aria-label="Drapeau ${t}">${r}</svg>`}function a(t){return`<text x="75" y="26" text-anchor="middle" font-size="11" fill="${t}">★ ✦ ★</text>`}function $(t,r,e,l=64){const o=r.length>9?"4%":"8%";return`<path id="bn${t}" d="M75 ${75+l}a${l} ${l} 0 0 1 0 ${-2*l}" fill="none"/><text font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2.2" fill="${e}"><textPath href="#bn${t}" startOffset="${o}">${r.toUpperCase()}</textPath></text>`}function d(t,r=71){return`<circle cx="75" cy="75" r="${r}" fill="none" stroke="${t}" stroke-width="2" stroke-dasharray="1 4"/>`}const w=(t,r,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="75" cy="50" r="10" fill="${t}"/>
    <g stroke="${t}" stroke-width="1.5">${Array.from({length:12},(l,o)=>{const i=o*30*Math.PI/180;return`<line x1="${75+12*Math.cos(i)}" y1="${50+12*Math.sin(i)}" x2="${75+16*Math.cos(i)}" y2="${50+16*Math.sin(i)}"/>`}).join("")}</g>
    <g fill="${r}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M75 82 C61 70 49 72 35 84 C51 80 63 80 75 88Z"/>
      <path d="M75 82 C89 70 101 72 115 84 C99 80 87 80 75 88Z"/>
      <path d="M71 87 L75 100 L79 87Z"/>
    </g>
    <circle cx="75" cy="80" r="3" fill="${t}"/>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${t}" stroke-width="3"/>
  ${d(t)}${a(t)}${$(e,"Kazakhstan",t)}`,k=(t,r,e)=>`
  <g fill="${t}">${Array.from({length:24},(l,o)=>{const i=o*15*Math.PI/180;return`<path d="M${(75+58*Math.cos(i-.05)).toFixed(1)} ${(75+58*Math.sin(i-.05)).toFixed(1)} L${(75+68*Math.cos(i)).toFixed(1)} ${(75+68*Math.sin(i)).toFixed(1)} L${(75+58*Math.cos(i+.05)).toFixed(1)} ${(75+58*Math.sin(i+.05)).toFixed(1)}Z"/>`}).join("")}</g>
  <circle cx="75" cy="75" r="58" fill="none" stroke="${t}" stroke-width="3"/>
  <clipPath id="c${e}"><circle cx="75" cy="75" r="55"/></clipPath>
  <g clip-path="url(#c${e})"><path d="M18 100 L44 70 L62 90 L82 64 L104 92 L132 100Z" fill="none" stroke="${t}" stroke-width="1.8" stroke-linejoin="round"/></g>
  <g transform="translate(75,64)">
    <circle r="17" fill="${r}" stroke="${t}" stroke-width="2.5"/>
    <g stroke="${t}" stroke-width="2" fill="none"><path d="M-17 0A17 17 0 0 1 17 0"/><path d="M-12 -8A15 15 0 0 1 12 -8"/><path d="M-12 8A15 15 0 0 0 12 8"/></g>
    <line x1="-17" y1="0" x2="17" y2="0" stroke="${t}" stroke-width="1.4"/><line x1="0" y1="-17" x2="0" y2="17" stroke="${t}" stroke-width="1.4"/>
    <line x1="-12" y1="-12" x2="12" y2="12" stroke="${t}" stroke-width="1"/><line x1="12" y1="-12" x2="-12" y2="12" stroke="${t}" stroke-width="1"/>
  </g>
  ${a(t)}${$(e,"Kirghizistan",t)}`,F=(t,r,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="102" cy="52" r="9" fill="${t}"/><g stroke="${t}" stroke-width="1.5">${Array.from({length:8},(l,o)=>{const i=o*45*Math.PI/180;return`<line x1="${102+11*Math.cos(i)}" y1="${52+11*Math.sin(i)}" x2="${102+15*Math.cos(i)}" y2="${52+15*Math.sin(i)}"/>`}).join("")}</g>
    <path d="M15 96 L38 66 L52 84 L70 56 L90 82 L110 68 L135 96Z" fill="none" stroke="${t}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M28 52q4 -5 8 0q4 -5 8 0" fill="none" stroke="${t}" stroke-width="1.4"/>
    <path d="M46 44q3 -4 6 0q3 -4 6 0" fill="none" stroke="${t}" stroke-width="1.2"/>
    <path d="M60 100 V82 H90 V100" fill="${r}" stroke="${t}" stroke-width="2"/>
    <path d="M55 82 Q75 63 95 82" fill="none" stroke="${t}" stroke-width="2"/>
    <line x1="75" y1="63" x2="75" y2="70" stroke="${t}" stroke-width="1.4"/>
    <rect x="71" y="88" width="8" height="12" fill="${t}"/>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${t}" stroke-width="3"/>
  ${d(t)}${a(t)}${$(e,"Mongolie",t)}`,C=(t,r,e)=>`
  <clipPath id="c${e}"><ellipse cx="75" cy="75" rx="54" ry="64"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="98" cy="42" r="8" fill="${t}"/>
    <g fill="${r}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M52 108 V58 Q52 50 57 50 Q62 50 62 58 V108Z"/>
      <path d="M66 108 V44 Q66 36 71 36 Q76 36 76 44 V108Z"/>
      <path d="M80 108 V64 Q80 56 85 56 Q90 56 90 64 V108Z"/>
      <path d="M92 108 V72 Q92 66 96 66 Q100 66 100 72 V108Z"/>
    </g>
    <g stroke="${t}" stroke-width="1.2" opacity=".7"><path d="M40 86 q18 -5 34 0" fill="none"/><path d="M56 98 q16 -5 34 0" fill="none"/></g>
  </g>
  <ellipse cx="75" cy="75" rx="54" ry="64" fill="none" stroke="${t}" stroke-width="3"/>
  <ellipse cx="75" cy="75" rx="60" ry="70" fill="none" stroke="${t}" stroke-width="1.5" stroke-dasharray="1 4"/>
  <text x="75" y="24" text-anchor="middle" font-size="11" fill="${t}">★ ✦ ★</text>
  <text x="75" y="132" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2" fill="${t}">CHINE</text>`,u=(t,r,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="75" r="60"/></clipPath>
  <g clip-path="url(#c${e})">
    <g fill="none" stroke="${t}" stroke-width="2"><path d="M30 74 V54 M38 74 V44 M46 74 V50"/><path d="M96 74 V48 M104 74 V40 M112 74 V52 M120 74 V58"/></g>
    <line x1="20" y1="74" x2="130" y2="74" stroke="${t}" stroke-width="1.5"/>
    <g fill="${t}"><path d="M62 72 V40 L84 72Z"/><path d="M60 72 V46 L44 72Z"/></g>
    <line x1="61" y1="36" x2="61" y2="74" stroke="${t}" stroke-width="2"/>
    <path d="M46 74 H92 L86 84 H52Z" fill="${r}" stroke="${t}" stroke-width="2"/>
    <g stroke="${t}" stroke-width="1.2" opacity=".7"><path d="M28 92 q10 -4 20 0t20 0 20 0 20 0" fill="none"/><path d="M34 100 q10 -4 20 0t20 0 20 0" fill="none"/></g>
  </g>
  <circle cx="75" cy="75" r="60" fill="none" stroke="${t}" stroke-width="3"/>
  ${d(t)}${a(t)}${$(e,"Hong-Kong",t)}`,L=(t,r,e)=>`
  <clipPath id="c${e}"><ellipse cx="75" cy="75" rx="52" ry="64"/></clipPath>
  <g clip-path="url(#c${e})">
    <path d="M104 34 a11 11 0 1 0 3 15 a8.5 8.5 0 1 1 -3 -15Z" fill="${t}"/>
    <g fill="${r}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M56 116 V58 Q56 50 62 48 Q68 50 68 58 V116Z"/>
      <path d="M82 116 V58 Q82 50 88 48 Q94 50 94 58 V116Z"/>
    </g>
    <g stroke="${t}" stroke-width="1.6"><line x1="62" y1="48" x2="62" y2="38"/><line x1="88" y1="48" x2="88" y2="38"/></g>
    <g stroke="${t}" stroke-width="1.2" opacity=".8">${[64,76,88,100].map(l=>`<line x1="56" y1="${l}" x2="68" y2="${l}"/><line x1="82" y1="${l}" x2="94" y2="${l}"/>`).join("")}</g>
    <path d="M68 72 H82 M68 76 H82" stroke="${t}" stroke-width="2"/>
    <path d="M71 72 L75 76 L79 72 M71 76 L75 72 L79 76" stroke="${t}" stroke-width="1" fill="none"/>
    <line x1="24" y1="116" x2="126" y2="116" stroke="${t}" stroke-width="1.5"/>
  </g>
  <ellipse cx="75" cy="75" rx="52" ry="64" fill="none" stroke="${t}" stroke-width="3"/>
  <text x="75" y="22" text-anchor="middle" font-size="11" fill="${t}">★ ✦ ★</text>
  <text x="75" y="132" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="12" letter-spacing="2" fill="${t}">MALAISIE</text>`,m=(t,r,e)=>`
  <clipPath id="c${e}"><path d="M75 16 C112 16 134 38 134 75 C134 112 112 134 75 134 C38 134 16 112 16 75 C16 38 38 16 75 16Z"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="75" cy="46" r="8" fill="${t}"/>
    <path d="M40 104 L66 56 Q75 44 84 56 L110 104Z" fill="${r}" stroke="${t}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M66 58 q9 6 18 0" fill="none" stroke="${t}" stroke-width="1.6"/>
    <path d="M72 52 q3 8 -2 16 M78 52 q-3 8 2 16" fill="none" stroke="${t}" stroke-width="1.6"/>
    <g stroke="${t}" stroke-width="2" fill="none"><path d="M112 104 V78"/><path d="M112 78 q-10 -8 -20 -6 M112 78 q10 -8 20 -6 M112 78 q-6 -12 -14 -14 M112 78 q6 -12 14 -14 M112 80 q-14 -2 -22 4 M112 80 q14 -2 22 4"/></g>
    <line x1="18" y1="104" x2="132" y2="104" stroke="${t}" stroke-width="1.5"/>
    <g stroke="${t}" stroke-width="1.2" opacity=".6"><path d="M24 114 q10 -4 20 0t20 0 20 0 20 0" fill="none"/></g>
  </g>
  <path d="M75 16 C112 16 134 38 134 75 C134 112 112 134 75 134 C38 134 16 112 16 75 C16 38 38 16 75 16Z" fill="none" stroke="${t}" stroke-width="3"/>
  ${a(t)}
  <text x="75" y="130" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="11.5" letter-spacing="1.6" fill="${t}">INDONÉSIE</text>`,D={KZ:w,KG:k,MN:F,CN:C,HK:u,MY:L,ID:m},P=(t,r,e,l)=>`
  <circle cx="75" cy="75" r="72" fill="none" stroke="${t}" stroke-width="3.5"/>
  <circle cx="75" cy="75" r="50" fill="none" stroke="${t}" stroke-width="1.5"/>
  ${a(t)}<text x="75" y="86" text-anchor="middle" font-family="Anton,sans-serif" font-size="30" fill="${t}">${l}</text>`;function V(t,r={}){const e=f(t),l=r.ink??p(t),o=r.paper??"#FFFDF8",i=r.size??138,s=r.opacity??1,c=e+"_"+y++,n=D[e],x=n?n(l,o,c):P(l,o,c,e);return`<svg class="medallion" width="${i}" height="${i}" viewBox="0 0 150 150" role="img" aria-label="Tampon ${t}"${s!==1?` style="opacity:${s}"`:""}>${x}</svg>`}export{f as c,Z as f,V as s};
