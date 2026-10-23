'use strict';
document.documentElement.classList.add('js');
const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
if(menuButton&&nav){menuButton.hidden=false;menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('is-open')){nav.classList.remove('is-open');menuButton.setAttribute('aria-expanded','false');menuButton.focus();}});}
document.querySelectorAll('.print-action').forEach(b=>{b.hidden=false;b.addEventListener('click',()=>window.print());});
let closedForPrint=[];
window.addEventListener('beforeprint',()=>{closedForPrint=[...document.querySelectorAll('details:not([open])')];closedForPrint.forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>{closedForPrint.forEach(d=>d.open=false);closedForPrint=[];});
const form=document.getElementById('roi-form');
if(form){
 const el=id=>document.getElementById(id);
 const euro=n=>new Intl.NumberFormat('fr-FR',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(n);
 const pct=n=>new Intl.NumberFormat('fr-FR',{maximumFractionDigits:1,minimumFractionDigits:1}).format(n)+' %';
 const presets={cloud:[135000,65000],local:[190000,75000],hybrid:[165000,82000]};
 function update(){
  if(!form.checkValidity()){el('calc-error').hidden=false;el('calc-error').textContent='Corrigez les valeurs hors limites ou manquantes pour recalculer.';['tco','benefits','roi'].forEach(id=>el(id).textContent='—');el('payback').textContent='Calcul suspendu.';el('annual-gain').textContent='';el('sensitivity').textContent='Renseignez des hypothèses valides.';return;}
  el('calc-error').hidden=true;
  const I=+el('initial').value,A=+el('annual').value,H=+el('hours').value,R=+el('rate').value,Q=+el('adoption').value/100,O=+el('other').value,F=+el('ramp').value/100;
  const G=H*12*R*Q+O,C=I+3*A,B=G*(F+2),N1=G*F-A,N=G-A;
  el('tco').textContent=euro(C);el('benefits').textContent=euro(B);el('roi').textContent=C>0?pct((B-C)/C*100):'Non défini';
  el('annual-gain').textContent='Gain annuel à régime établi : '+euro(G)+'.';
  let months=I===0&&N1>=0?0:N1>0&&N1>=I?12*I/N1:N>0?12*(1+(I-N1)/N):Infinity;
  el('payback').textContent=Number.isFinite(months)?(months===0?'Investissement nul ; solde non négatif dès le départ.':'Équilibre estimé après '+Math.ceil(months)+' mois'+(months>36?', hors horizon de 36 mois.':'.')):'Équilibre non atteint avec ces hypothèses.';
  el('sensitivity').textContent=C>0?['Gains −30 % : '+pct((B*.7-C)/C*100),'Base : '+pct((B-C)/C*100),'Gains +30 % : '+pct((B*1.3-C)/C*100)].join(' · '):'ROI non défini lorsque le coût total est nul.';
 }
 el('scenario').addEventListener('change',()=>{const p=presets[el('scenario').value];el('initial').value=p[0];el('annual').value=p[1];update();});
 form.addEventListener('input',update);form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('reset',()=>setTimeout(update,0));update();
}
