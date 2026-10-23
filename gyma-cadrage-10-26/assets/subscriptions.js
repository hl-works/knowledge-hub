'use strict';
(() => {
 const input=document.getElementById('seat-count'); if(!input)return;
 const money=n=>new Intl.NumberFormat('fr-FR',{maximumFractionDigits:2}).format(n)+' $';
 const update=()=>{const seats=Number(input.value);if(![5,10,25,50].includes(seats))return;for(const [name,rate] of [['chatgpt',25],['claude',25],['mistral',24.99]]){document.getElementById(name+'-seats').textContent=money(seats*rate)+' / mois';document.getElementById(name+'-year').textContent=money(seats*rate*12)+' sur 12 mois';}};
 input.addEventListener('change',update);update();
})();
