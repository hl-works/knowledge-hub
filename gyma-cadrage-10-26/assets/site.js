'use strict';
document.documentElement.classList.add('js');
const menuButton=document.querySelector('.menu-toggle');
const mobileMenu=document.getElementById('mobile-menu');
if(menuButton&&mobileMenu){
 const mobileViewport=matchMedia('(max-width: 900px)');
 const closeMenu=()=>{if(mobileMenu.open)mobileMenu.close();};
 const syncClosed=()=>{menuButton.setAttribute('aria-expanded','false');document.documentElement.classList.remove('mobile-menu-open');};
 menuButton.hidden=false;
 menuButton.addEventListener('click',()=>{
  if(!mobileViewport.matches)return;
  mobileMenu.showModal();menuButton.setAttribute('aria-expanded','true');document.documentElement.classList.add('mobile-menu-open');
  mobileMenu.querySelector('.mobile-menu-close').focus();
  mobileMenu.querySelector('[aria-current="page"]')?.scrollIntoView({block:'nearest'});
 });
 mobileMenu.querySelector('.mobile-menu-close').addEventListener('click',closeMenu);
 mobileMenu.addEventListener('close',syncClosed);
 mobileMenu.addEventListener('keydown',e=>{
  if(e.key!=='Tab')return;
  const items=[...mobileMenu.querySelectorAll('button:not([disabled]),a[href]')].filter(el=>el.getClientRects().length);
  if(!items.length)return;
  const index=items.indexOf(document.activeElement);
  e.preventDefault();items[(index+(e.shiftKey?-1:1)+items.length)%items.length].focus();
 });
 mobileMenu.addEventListener('cancel',()=>{closeMenu();});
 // Only a click outside the drawer closes it; whitespace within the drawer does not.
 mobileMenu.addEventListener('click',e=>{if(e.target!==mobileMenu)return;const r=mobileMenu.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeMenu();});
 mobileMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
 mobileViewport.addEventListener('change',e=>{if(!e.matches)closeMenu();});
 window.addEventListener('pagehide',closeMenu);window.addEventListener('beforeprint',closeMenu);
}
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
  const valid=form.checkValidity();el('calc-error').hidden=valid;
  if(!valid){el('calc-error').textContent='Corrige les valeurs hors limites ou manquantes pour recalculer.';el('tco').textContent='—';el('gain-target').textContent='—';el('roi-estimate').hidden=true;return;}
  const I=+el('initial').value,A=+el('annual').value,F=+el('ramp').value/100,C=I+3*A;
  el('tco').textContent=euro(C);el('gain-target').textContent=euro(C/(2+F))+' / an';
  el('target-explanation').textContent='Gains annuels nécessaires à régime établi, avec '+el('ramp').value+' % des gains en année 1. Ce seuil ne prédit pas les gains de GYMA.';
  const filled=el('observed-gain').value.trim()!=='';el('roi-estimate').hidden=!filled;
  if(filled){const G=+el('observed-gain').value,B=G*(2+F);el('roi').textContent=C>0?pct((B-C)/C*100):'Non défini';el('roi-detail').textContent='Avec ton estimation de '+euro(G)+' par an, les gains cumulés sur 36 mois sont de '+euro(B)+'. Résultat fondé sur ta saisie, à valider par les pilotes.';}
 }
 el('scenario').addEventListener('change',()=>{const p=presets[el('scenario').value];el('initial').value=p[0];el('annual').value=p[1];update();});
 form.addEventListener('input',update);form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('reset',()=>setTimeout(update,0));update();
}
