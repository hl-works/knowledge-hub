import{f,a as m,d as b}from"./model.ByxRXaPf.js";const t=a=>a.replace(/[&<>"]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[e]),v=a=>a.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/(^-|-$)/g,""),y={Kazakhstan:["#FA4616","#C9330B"],Kirghizistan:["#149E7C","#0C5A5E"],Mongolie:["#E89B2E","#B86A12"],Chine:["#F2516F","#C12B49"],"Hong-Kong":["#1E96C8","#0C5A7E"],Indonésie:["#149E7C","#0C5A5E"],Malaisie:["#E89B2E","#B86A12"]},C={Kazakhstan:"KZ",Kirghizistan:"KG",Mongolie:"MN",Chine:"CN","Hong-Kong":"HK",Indonésie:"ID",Malaisie:"MY"};function E(a){return a.length?`<div class="quiz"><h3>Mini-quiz · duel Alexis / Emma</h3>${a.map((i,o)=>{const l=i.choix.map((s,n)=>{if(!s)return"";const c=["a","b","c"][n];return`<button class="opt" data-k="${c}" data-good="${i.bonne}"><span class="k">${c.toUpperCase()}</span><span>${t(s)}</span></button>`}).join("");return`<div class="q" data-q="${o}">
          <p class="qq">${o+1}. ${t(i.question)}</p>
          <div class="opts">${l}</div>
          <p class="expl">${t(i.explication)}</p>
        </div>`}).join("")}<p class="score" data-total="${a.length}"></p></div>`:""}function q(a,e){const[i,o]=y[a.pays]??["#FA4616","#C9330B"],l=[a.capitale&&`<span class="chip"><b>Capitale</b> ${t(a.capitale)}</span>`,a.monnaie&&`<span class="chip"><b>Monnaie</b> ${t(a.monnaie)}</span>`,a.langue&&`<span class="chip"><b>Langue</b> ${t(a.langue)}</span>`,a.population&&`<span class="chip"><b>Population</b> ${t(a.population)}</span>`].filter(Boolean).join(""),s=a.funFacts.map(n=>`<li>${t(n)}</li>`).join("");return`
      <article class="fiche" id="${v(a.pays)}">
        <div class="banner" style="background:linear-gradient(135deg, ${i}, ${o})">
          <span class="code">${C[a.pays]??""}</span>
          <h2>${t(a.pays)}</h2>
          ${a.capitale?`<div class="cap">${t(a.capitale)}</div>`:""}
        </div>
        <div class="body">
          <div class="facts">${l}</div>
          ${a.histoire?`<p class="histoire">${t(a.histoire)}</p>`:""}
          ${s?`<div class="savais"><h3>Le savais-tu ?</h3><ul>${s}</ul></div>`:""}
          ${E(e)}
        </div>
      </article>`}(async()=>{const a=document.getElementById("fiches");try{const[e,i]=await Promise.all([f("pays"),f("quiz")]),o=m(e).filter(s=>s.pays),l=b(i);if(a.innerHTML=o.map(s=>q(s,l.filter(n=>n.pays===s.pays))).join(""),a.querySelectorAll(".quiz").forEach(s=>{const n=s.querySelectorAll(".q").length;let c=0,u=0;s.querySelectorAll(".q").forEach(h=>{const $=h.querySelectorAll(".opt");$.forEach(r=>{r.addEventListener("click",()=>{const p=r.dataset.good,g=r.dataset.k;$.forEach(d=>{d.disabled=!0,d.dataset.k===p&&d.classList.add("good")}),g!==p&&r.classList.add("bad"),h.querySelector(".expl")?.classList.add("show"),c++,g===p&&u++,c===n&&(s.querySelector(".score").textContent=`Score : ${u} / ${n}`)})})})}),location.hash){const s=document.getElementById(location.hash.slice(1));s&&setTimeout(()=>s.scrollIntoView({behavior:"smooth",block:"start"}),100)}}catch(e){a.innerHTML=`<p class="loading">${String(e)}</p>`}})();
