import{s as i}from"./stamps.DM4M0S79.js";const o={Kazakhstan:["#FA4616","#C9330B"],Kirghizistan:["#149E7C","#0C5A5E"],Mongolie:["#E89B2E","#B86A12"],Chine:["#F2516F","#C12B49"],"Hong-Kong":["#1E96C8","#0C5A7E"],Indonésie:["#149E7C","#0C5A5E"],Malaisie:["#E89B2E","#B86A12"]},l=s=>s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/(^-|-$)/g,""),p=s=>s.replace(/[&<>"]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[e]);function d(s,e=""){const[a,t]=o[s]??["#FA4616","#C9330B"];return`<div class="pays-head" style="--pc1:${a};--pc2:${t}">
    <span class="stamp-slot" data-pays="${l(s)}" aria-hidden="true">${i(s,{size:58})}</span>
    <h2 class="disp">${p(s)}</h2>
    ${e?`<span class="pays-sub">${p(e)}</span>`:""}
  </div>`}function h(s,e,a=""){const[t,n]=o[s]??["#FA4616","#C9330B"];return`<div class="pays-head" style="--pc1:${t};--pc2:${n}">
    <span class="stamp-slot" data-pays="${l(s)}" aria-hidden="true">${i(s,{size:58})}</span>
    <h2 class="disp">${p(e)}</h2>
    ${a?`<span class="pays-sub">${p(a)}</span>`:""}
  </div>`}function $(s,e){const a=[],t=new Map;for(const n of s){const c=e(n);t.has(c)||(t.set(c,a.length),a.push({pays:c,items:[]})),a[t.get(c)].items.push(n)}return a}export{o as P,h as e,$ as g,d as p,l as s};
