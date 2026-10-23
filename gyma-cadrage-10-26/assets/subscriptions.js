 'use strict';
(() => {
 const input=document.getElementById('seat-count');if(!input)return;
 const money=(n,currency)=>new Intl.NumberFormat('fr-FR',{minimumFractionDigits:0,maximumFractionDigits:2}).format(n)+(currency==='EUR'?' € TTC':' $');
 const update=()=>{const seats=Number(input.value);if(![5,10,25,50].includes(seats))return;for(const [name,rate,currency] of [['chatgpt',25,'USD'],['claude',25,'USD'],['mistral',29.99,'EUR']]){document.getElementById(name+'-seats').textContent=money(seats*rate,currency)+' / mois';document.getElementById(name+'-year').textContent=money(seats*rate*12,currency)+' sur 12 mois';}};
 input.addEventListener('change',update);update();
})();
