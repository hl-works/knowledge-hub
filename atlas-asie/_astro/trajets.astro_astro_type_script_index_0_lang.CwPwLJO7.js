import{f as d,m as h,n as $}from"./model.eI87Udvv.js";const c=t=>t.replace(/[&<>"]/g,o=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[o]),u=["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."],r=t=>`<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${t}</svg>`,l={Avion:r('<path d="M17.8 19.2 16 11l3.5-3.5a2 2 0 0 0-2.8-2.8L13 8.2 4.8 6.4a1 1 0 0 0-.9 1.7l6 3.3-2.3 2.3-2-.3-1 1 3 1.5L12 20l1-1-.3-2 2.3-2.3 3.3 6a1 1 0 0 0 1.7-.9Z"/>'),Bus:r('<rect x="4" y="4" width="16" height="13" rx="2"/><path d="M4 11h16M8 17v2M16 17v2"/><circle cx="8" cy="14" r="1"/><circle cx="16" cy="14" r="1"/>'),Bateau:r('<path d="M3 14l1.5 5a2 2 0 0 0 2 1.5h11a2 2 0 0 0 2-1.5L21 14M5 14V7l7-3 7 3v7M12 4v10"/>')},p=t=>(t.match(/\b([A-Z]{3})\b/)??[])[1]??"",g=t=>(t.match(/\bT(\d)\b/)??[])[1]??"",y=r('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>'),b=r('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>');function v(t,o,s){if(!s)return"";const e=g(o),a=e?` · T${e}`:"",n=s.nomLocal&&s.nomLocal!==s.nomEn?s.nomLocal+a:"",i=(n||s.nomEn+a).trim(),m=`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(`${s.nomEn} ${s.code}`)}`;return`<div class="apt">
      <span class="apt-lbl">${t}</span>
      <div class="apt-en">${c(s.nomEn)}${a}</div>
      ${s.adresseEn?`<div class="apt-adr">${c(s.adresseEn)}</div>`:""}
      ${n?`<div class="apt-local">${c(n)}</div>`:""}
      <div class="apt-btns">
        <a class="btn-apt btn-apt--map" href="${m}" target="_blank" rel="noopener">${y} Carte</a>
        <button type="button" class="btn-apt btn-apt--copy" data-copy="${c(i)}">${b} Copier</button>
      </div>
    </div>`}function M(t,o){const s=v("Départ",t.de,o.get(p(t.de))),e=v("Arrivée",t.vers,o.get(p(t.vers)));return!s&&!e?"":`<details class="taxi">
      <summary>Aéroports & taxi</summary>
      <div class="taxi-grid">${s}${e}</div>
    </details>`}function f(t,o){const s=t.date?`${t.date.getDate()} ${u[t.date.getMonth()]}`:c(t.dateRaw),e=[t.departH,t.arriveeH].filter(Boolean).join(" → "),a=[t.compagnie,t.vol].filter(Boolean).join(" · "),n=/réserv/i.test(t.statut);return`<article class="trip">
      <span class="tico">${l[t.type]??l.Avion}</span>
      <div class="mid">
        <div class="route">${c(t.de)}<span class="arrow">→</span>${c(t.vers)}</div>
        ${e?`<div class="sub">${c(e)}</div>`:""}
        ${a?`<div class="comp">${c(a)}</div>`:""}
      </div>
      <div class="right">
        <div class="date">${s}</div>
        <span class="st ${n?"st--ok":"st--todo"}">${c(t.statut||"—")}</span>
      </div>
      ${M(t,o)}
    </article>`}(async()=>{const t=document.getElementById("trajets");try{const[o,s]=await Promise.all([d("transports").then(h),d("aeroports").then($).catch(()=>[])]),e=new Map(s.map(a=>[a.code,a]));t.innerHTML=o.map(a=>f(a,e)).join(""),t.addEventListener("click",async a=>{const n=a.target.closest(".btn-apt--copy");if(n)try{await navigator.clipboard.writeText(n.dataset.copy);const i=n.innerHTML;n.innerHTML="✓ Copié",setTimeout(()=>{n.innerHTML=i},1400)}catch{}})}catch(o){t.innerHTML=`<p class="loading">${String(o)}</p>`}})();
