import{j as c,f as l}from"./model.IubqTyN7.js";const a=t=>t.replace(/[&<>"]/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[s]),d=["janv.","févr.","mars","avr.","mai","juin","juil.","août","sept.","oct.","nov.","déc."],o=t=>`<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${t}</svg>`,i={Avion:o('<path d="M17.8 19.2 16 11l3.5-3.5a2 2 0 0 0-2.8-2.8L13 8.2 4.8 6.4a1 1 0 0 0-.9 1.7l6 3.3-2.3 2.3-2-.3-1 1 3 1.5L12 20l1-1-.3-2 2.3-2.3 3.3 6a1 1 0 0 0 1.7-.9Z"/>'),Bus:o('<rect x="4" y="4" width="16" height="13" rx="2"/><path d="M4 11h16M8 17v2M16 17v2"/><circle cx="8" cy="14" r="1"/><circle cx="16" cy="14" r="1"/>'),Bateau:o('<path d="M3 14l1.5 5a2 2 0 0 0 2 1.5h11a2 2 0 0 0 2-1.5L21 14M5 14V7l7-3 7 3v7M12 4v10"/>')};function v(t){const s=t.date?`${t.date.getDate()} ${d[t.date.getMonth()]}`:a(t.dateRaw),e=[t.departH,t.arriveeH].filter(Boolean).join(" → "),r=[t.compagnie,t.vol].filter(Boolean).join(" · "),n=/réserv/i.test(t.statut);return`<article class="trip">
      <span class="tico">${i[t.type]??i.Avion}</span>
      <div class="mid">
        <div class="route">${a(t.de)}<span class="arrow">→</span>${a(t.vers)}</div>
        ${e?`<div class="sub">${a(e)}</div>`:""}
        ${r?`<div class="comp">${a(r)}</div>`:""}
      </div>
      <div class="right">
        <div class="date">${s}</div>
        <span class="st ${n?"st--ok":"st--todo"}">${a(t.statut||"—")}</span>
      </div>
    </article>`}(async()=>{const t=document.getElementById("trajets");try{const s=c(await l("transports"));t.innerHTML=s.map(v).join("")}catch(s){t.innerHTML=`<p class="loading">${String(s)}</p>`}})();
