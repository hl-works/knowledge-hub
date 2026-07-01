const M={Kazakhstan:"KZ",Kirghizistan:"KG",Mongolie:"MN",Chine:"CN","Hong-Kong":"HK","Hong Kong":"HK",Indonésie:"ID",Malaisie:"MY"},g=t=>M[t]??t.slice(0,2).toUpperCase(),y={KZ:"#0E9CB8",KG:"#D62839",MN:"#C0552B",CN:"#C1121F",HK:"#C71F6B",MY:"#12457A",ID:"#0E8A6B"},w=t=>y[g(t)]??"#C9330B";let F=0;function d(t,l,e,r,o=0){let h="";for(let i=0;i<5;i++){const c=(-90+o+i*72)*Math.PI/180,s=c+36*Math.PI/180;h+=(i?"L":"M")+(t+e*Math.cos(c)).toFixed(1)+" "+(l+e*Math.sin(c)).toFixed(1)+"L"+(t+e*.4*Math.cos(s)).toFixed(1)+" "+(l+e*.4*Math.sin(s)).toFixed(1)}return`<path d="${h}Z" fill="${r}"/>`}function H(t){let l="";switch(t){case"KZ":l=`<rect width="30" height="20" fill="#00AFCA"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({length:12},(e,r)=>{const o=r*30*Math.PI/180;return`<line x1="16" y1="9" x2="${16+6*Math.cos(o)}" y2="${9+6*Math.sin(o)}"/>`}).join("")}</g><circle cx="16" cy="9" r="3.4" fill="#FFD200"/><rect width="2" height="20" fill="#FFD200"/>`;break;case"KG":l=`<rect width="30" height="20" fill="#E8112D"/><g stroke="#FFD200" stroke-width="0.5">${Array.from({length:16},(e,r)=>{const o=r*22.5*Math.PI/180;return`<line x1="15" y1="10" x2="${15+6*Math.cos(o)}" y2="${10+6*Math.sin(o)}"/>`}).join("")}</g><circle cx="15" cy="10" r="3.6" fill="#FFD200"/><line x1="12" y1="10" x2="18" y2="10" stroke="#E8112D" stroke-width="0.5"/><line x1="15" y1="7.5" x2="15" y2="12.5" stroke="#E8112D" stroke-width="0.5"/>`;break;case"MN":l='<rect width="10" height="20" fill="#C4272E"/><rect x="10" width="10" height="20" fill="#015197"/><rect x="20" width="10" height="20" fill="#C4272E"/><g fill="#F9CF02"><circle cx="5" cy="6" r="1.1"/><path d="M3.6 8h2.8v1H3.6z"/><path d="M3.8 10.2 5 9l1.2 1.2-1.2 1.2z"/><path d="M3.6 12.5h2.8v1H3.6z"/></g>';break;case"CN":l=`<rect width="30" height="20" fill="#DE2910"/>${d(6,5,3.4,"#FFDE00",0)}${d(11,2.4,1.1,"#FFDE00",20)}${d(12.6,4.6,1.1,"#FFDE00",40)}${d(12.6,7.6,1.1,"#FFDE00",-40)}${d(11,9.8,1.1,"#FFDE00",-20)}`;break;case"HK":l=`<rect width="30" height="20" fill="#DE2910"/><g fill="#fff">${Array.from({length:5},(e,r)=>{const o=(-90+r*72)*Math.PI/180;return`<ellipse cx="${15+3.4*Math.cos(o)}" cy="${10+3.4*Math.sin(o)}" rx="1.5" ry="3.4" transform="rotate(${r*72} ${15+3.4*Math.cos(o)} ${10+3.4*Math.sin(o)})"/>`}).join("")}</g><circle cx="15" cy="10" r="1.3" fill="#DE2910"/>`;break;case"MY":l=`${Array.from({length:14},(e,r)=>`<rect y="${r*20/14}" width="30" height="${20/14}" fill="${r%2?"#fff":"#CC0001"}"/>`).join("")}<rect width="15" height="${20/14*8}" fill="#010066"/><circle cx="6.5" cy="5.5" r="3" fill="#FFCC00"/><circle cx="7.8" cy="5.5" r="2.6" fill="#010066"/>${d(10.4,5.5,1.8,"#FFCC00",0)}`;break;case"ID":l='<rect width="30" height="10" fill="#FF0000"/><rect y="10" width="30" height="10" fill="#fff"/>';break;default:l='<rect width="30" height="20" fill="#9A8268"/>'}return`<svg viewBox="0 0 30 20" preserveAspectRatio="none" role="img" aria-label="Drapeau ${t}">${l}</svg>`}function a(t){return`<text x="75" y="27" text-anchor="middle" font-size="10" letter-spacing="2" fill="${t}">★ ✦ ★</text>`}function $(t,l,e,r=60){return`<path id="bn${t}" d="M${(75-r).toFixed(1)} 75 A ${r} ${r} 0 0 0 ${(75+r).toFixed(1)} 75" fill="none"/><text font-family="'Fraunces',Georgia,serif" font-weight="600" font-size="12" letter-spacing="1.3" fill="${e}" text-anchor="middle"><textPath href="#bn${t}" startOffset="50%">${l.toUpperCase()}</textPath></text>`}function p(t,l,e,r,o,h,i=1.4){let c="";for(let s=0;s<o;s++){const n=s*(360/o)*Math.PI/180;c+=`<line x1="${(t+e*Math.cos(n)).toFixed(1)}" y1="${(l+e*Math.sin(n)).toFixed(1)}" x2="${(t+r*Math.cos(n)).toFixed(1)}" y2="${(l+r*Math.sin(n)).toFixed(1)}"/>`}return`<g stroke="${h}" stroke-width="${i}">${c}</g>`}function f(t){return`<circle cx="75" cy="75" r="70" fill="none" stroke="${t}" stroke-width="2.4"/><circle cx="75" cy="75" r="66" fill="none" stroke="${t}" stroke-width="0.9"/>`}function x(t,l,e){return`<ellipse cx="75" cy="75" rx="${l}" ry="${e}" fill="none" stroke="${t}" stroke-width="2.4"/><ellipse cx="75" cy="75" rx="${l-4}" ry="${e-4}" fill="none" stroke="${t}" stroke-width="0.9"/>`}const k="M75 12 C114 12 138 36 138 75 C138 114 114 138 75 138 C36 138 12 114 12 75 C12 36 36 12 75 12Z",C="M75 17 C110 17 133 40 133 75 C133 110 110 133 75 133 C40 133 17 110 17 75 C17 40 40 17 75 17Z",u=(t,l,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="75" cy="48" r="8" fill="${t}"/>${p(75,48,10,14,12,t)}
    <g fill="${l}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M75 78 C63 68 53 70 43 79 C55 76 65 76 75 83Z"/>
      <path d="M75 78 C87 68 97 70 107 79 C95 76 85 76 75 83Z"/>
      <path d="M72 82 L75 92 L78 82Z"/>
    </g>
    <circle cx="75" cy="77" r="2.6" fill="${t}"/>
  </g>
  ${f(t)}${a(t)}${$(e,"Kazakhstan",t,60)}`,D=(t,l,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${e})">
    <path d="M20 96 L44 74 L60 88 L80 68 L100 90 L130 96Z" fill="none" stroke="${t}" stroke-width="1.8" stroke-linejoin="round"/>
    ${p(75,53,14,19,20,t,1.2)}
    <circle cx="75" cy="53" r="13" fill="${l}" stroke="${t}" stroke-width="2"/>
    <g transform="translate(75,53)" stroke="${t}" fill="none">
      <path d="M-11 0A11 11 0 0 1 11 0" stroke-width="1.5"/>
      <path d="M-8 -5A10 10 0 0 1 8 -5" stroke-width="1.1"/>
      <path d="M-8 5A10 10 0 0 0 8 5" stroke-width="1.1"/>
      <line x1="-11" y1="0" x2="11" y2="0" stroke-width="1.1"/><line x1="0" y1="-11" x2="0" y2="11" stroke-width="1.1"/>
    </g>
  </g>
  ${f(t)}${a(t)}${$(e,"Kirghizistan",t,60)}`,P=(t,l,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="100" cy="50" r="8" fill="${t}"/>${p(100,50,10,13,8,t)}
    <path d="M22 94 L42 68 L54 82 L70 58 L88 80 L106 68 L128 94Z" fill="none" stroke="${t}" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M32 52q4 -5 8 0q4 -5 8 0" fill="none" stroke="${t}" stroke-width="1.3"/>
    <path d="M60 96 V80 H90 V96" fill="${l}" stroke="${t}" stroke-width="2"/>
    <path d="M55 80 Q75 62 95 80" fill="none" stroke="${t}" stroke-width="2"/>
    <line x1="75" y1="61" x2="75" y2="68" stroke="${t}" stroke-width="1.3"/>
    <rect x="71" y="85" width="8" height="11" fill="${t}"/>
  </g>
  ${f(t)}${a(t)}${$(e,"Mongolie",t,60)}`,Z=(t,l,e)=>`
  <clipPath id="c${e}"><ellipse cx="75" cy="72" rx="46" ry="54"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="96" cy="42" r="7" fill="${t}"/>
    <g fill="${l}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M54 100 V56 Q54 49 58 49 Q62 49 62 56 V100Z"/>
      <path d="M66 100 V44 Q66 37 71 37 Q76 37 76 44 V100Z"/>
      <path d="M80 100 V60 Q80 53 84 53 Q88 53 88 60 V100Z"/>
      <path d="M90 100 V70 Q90 64 94 64 Q98 64 98 70 V100Z"/>
    </g>
    <g stroke="${t}" stroke-width="1.1" opacity=".65"><path d="M46 84 q16 -5 30 0" fill="none"/><path d="M58 94 q14 -5 28 0" fill="none"/></g>
  </g>
  ${x(t,56,68)}${a(t)}${$(e,"Chine",t,56)}`,K=(t,l,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="72" r="52"/></clipPath>
  <g clip-path="url(#c${e})">
    <g fill="none" stroke="${t}" stroke-width="2"><path d="M34 72 V54 M42 72 V46 M50 72 V52"/><path d="M96 72 V50 M104 72 V42 M112 72 V54"/></g>
    <line x1="26" y1="72" x2="124" y2="72" stroke="${t}" stroke-width="1.4"/>
    <g fill="${t}"><path d="M62 70 V42 L82 70Z"/><path d="M60 70 V48 L46 70Z"/></g>
    <line x1="61" y1="38" x2="61" y2="72" stroke="${t}" stroke-width="2"/>
    <path d="M48 72 H90 L84 81 H54Z" fill="${l}" stroke="${t}" stroke-width="2"/>
    <g stroke="${t}" stroke-width="1.1" opacity=".65"><path d="M34 90 q9 -4 18 0t18 0 18 0" fill="none"/></g>
  </g>
  ${f(t)}${a(t)}${$(e,"Hong-Kong",t,60)}`,V=(t,l,e)=>`
  <clipPath id="c${e}"><ellipse cx="75" cy="72" rx="46" ry="54"/></clipPath>
  <g clip-path="url(#c${e})">
    <path d="M99 36 a10 10 0 1 0 3 14 a8 8 0 1 1 -3 -14Z" fill="${t}"/>
    <g fill="${l}" stroke="${t}" stroke-width="2" stroke-linejoin="round">
      <path d="M58 100 V58 Q58 51 63 49 Q68 51 68 58 V100Z"/>
      <path d="M82 100 V58 Q82 51 87 49 Q92 51 92 58 V100Z"/>
    </g>
    <g stroke="${t}" stroke-width="1.5"><line x1="63" y1="49" x2="63" y2="40"/><line x1="87" y1="49" x2="87" y2="40"/></g>
    <g stroke="${t}" stroke-width="1.1" opacity=".8">${[64,74,84,94].map(r=>`<line x1="58" y1="${r}" x2="68" y2="${r}"/><line x1="82" y1="${r}" x2="92" y2="${r}"/>`).join("")}</g>
    <path d="M68 70 H82 M68 74 H82" stroke="${t}" stroke-width="1.8"/>
  </g>
  ${x(t,56,68)}${a(t)}${$(e,"Malaisie",t,56)}`,L=(t,l,e)=>`
  <clipPath id="c${e}"><circle cx="75" cy="70" r="50"/></clipPath>
  <g clip-path="url(#c${e})">
    <circle cx="75" cy="44" r="8" fill="${t}"/>
    <path d="M42 92 L66 54 Q75 43 84 54 L108 92Z" fill="${l}" stroke="${t}" stroke-width="2" stroke-linejoin="round"/>
    <path d="M66 56 q9 6 18 0" fill="none" stroke="${t}" stroke-width="1.5"/>
    <g stroke="${t}" stroke-width="2" fill="none"><path d="M108 92 V70"/><path d="M108 70 q-9 -7 -18 -5 M108 70 q9 -7 18 -5 M108 70 q-5 -11 -12 -13 M108 70 q5 -11 12 -13"/></g>
    <line x1="24" y1="92" x2="126" y2="92" stroke="${t}" stroke-width="1.4"/>
    <g stroke="${t}" stroke-width="1.1" opacity=".55"><path d="M30 100 q9 -4 18 0t18 0 18 0" fill="none"/></g>
  </g>
  <path d="${k}" fill="none" stroke="${t}" stroke-width="2.4"/><path d="${C}" fill="none" stroke="${t}" stroke-width="0.9"/>
  ${a(t)}${$(e,"Indonésie",t,55)}`,m={KZ:u,KG:D,MN:P,CN:Z,HK:K,MY:V,ID:L},E=(t,l,e,r)=>`
  <circle cx="75" cy="75" r="72" fill="none" stroke="${t}" stroke-width="3.5"/>
  <circle cx="75" cy="75" r="50" fill="none" stroke="${t}" stroke-width="1.5"/>
  ${topStars(t)}<text x="75" y="86" text-anchor="middle" font-family="Anton,sans-serif" font-size="30" fill="${t}">${r}</text>`;function A(t,l={}){const e=g(t),r=l.ink??w(t),o=l.paper??"#FFFDF8",h=l.size??138,i=l.opacity??1,c=e+"_"+F++,s=m[e],n=s?s(r,o,c):E(r,o,c,e);return`<svg class="medallion" width="${h}" height="${h}" viewBox="0 0 150 150" role="img" aria-label="Tampon ${t}"${i!==1?` style="opacity:${i}"`:""}>${n}</svg>`}export{g as c,H as f,A as s};
