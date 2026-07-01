import{s as p}from"./stamps.DM4M0S79.js";const c={Kazakhstan:["#FA4616","#C9330B"],Kirghizistan:["#149E7C","#0C5A5E"],Mongolie:["#E89B2E","#B86A12"],Chine:["#F2516F","#C12B49"],"Hong-Kong":["#1E96C8","#0C5A7E"],Indonésie:["#149E7C","#0C5A5E"],Malaisie:["#E89B2E","#B86A12"]},r=s=>s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/(^-|-$)/g,""),i=s=>s.replace(/[&<>"]/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[a]);function g(s,a=""){const[t,e]=c[s]??["#FA4616","#C9330B"];return`<div class="pays-head" style="--pc1:${t};--pc2:${e}">
    <span class="stamp-slot" data-pays="${r(s)}" aria-hidden="true">${p(s,{size:58})}</span>
    <h2 class="disp">${i(s)}</h2>
    ${a?`<span class="pays-sub">${i(a)}</span>`:""}
  </div>`}function h(s,a){const t=[],e=new Map;for(const o of s){const n=a(o);e.has(n)||(e.set(n,t.length),t.push({pays:n,items:[]})),t[e.get(n)].items.push(o)}return t}export{c as P,h as g,g as p,r as s};
