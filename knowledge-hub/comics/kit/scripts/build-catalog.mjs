throw new Error('Archive v1 : ne pas régénérer ce manifeste. Les PNG et leurs identifiants sont figés ; ajouter de nouvelles versions explicitement.');
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const assets = [];
const dim = p => { const b=fs.readFileSync(p); return {width:b.readUInt32BE(16),height:b.readUInt32BE(20)}; };
function add(id, file, title, meta={}) {
  const p=path.join(root,file), b=fs.readFileSync(p);
  const a={id,path:file,title,...dim(p),bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),background:'opaque',...meta};
  assets.push(a); return a;
}
function crop(source,id,title,rect,meta) {
  const file=`assets/tiles/${id}.png`; fs.mkdirSync(path.join(root,'assets/tiles'),{recursive:true});
  const [x,y,w,h]=rect;
  execFileSync('sips',['--cropToHeightWidth',String(h),String(w),'--cropOffset',String(y),String(x),path.join(root,source.path),'--out',path.join(root,file)],{stdio:'pipe'});
  return add(id,file,title,{kind:'tile',sourceId:source.id,crop:{x,y,width:w,height:h},reviewStatus:source.reviewStatus,transparentCutout:false,...meta});
}
add('duo-reference-v2','assets/characters/duo-reference-v2.png','Duo — référence validée V2',{kind:'identity_reference',reviewStatus:'approved',authoritativeIdentity:true});
const expressions=['curieux','etonne','dubitatif','inquiet','amuse','enthousiaste'];
const poses=['explique','ecoute','montre','reflechit','se-rejouit','assis'];
for (const character of ['hugo','ia']) {
  const sheet=add(`${character}-poses-v1`,`assets/characters/${character}-expressions-poses-v1.png`,`${character==='hugo'?'Hugo':'Garçon androïde'} — expressions et poses`,{kind:'acting_reference',character,reviewStatus:character==='ia'?'proposed':'approved'});
  for(let i=0;i<6;i++) crop(sheet,`${character}-expression-${expressions[i]}-v1`,`${character} · ${expressions[i]}`,[i*241+8,112,234,218],{character,expression:expressions[i],use:'portrait_inset'});
  for(let i=0;i<6;i++) crop(sheet,`${character}-pose-${poses[i]}-v1`,`${character} · ${poses[i]}`,[i%3*482+14,i<3?378:707,466,291],{character,pose:poses[i],use:'illustration_inset'});
}
const seasons=[['hiver',[12,1,2]],['printemps',[3,4,5]],['ete',[6,7,8]],['automne',[9,10,11]]];
const monthNames=['janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre'];
for(const [season,months] of seasons){
  const sheet=add(`season-${season}-v1`,`assets/seasons/${season}-v1.png`,`${season} — trois mois`,{kind:'wardrobe_reference',season,months,reviewStatus:'delivered'});
  months.forEach((month,i)=>crop(sheet,`month-${String(month).padStart(2,'0')}-${monthNames[month-1]}-v1`,`${monthNames[month-1]} · duo`,[i*512,season==='ete'?185:150,512,season==='ete'?755:790],{month,season,character:'duo',use:'wardrobe_reference_only'}));
}
const manifest={schemaVersion:1,packVersion:'1.0.0',created:'2026-10-16',identityReference:'duo-reference-v2',notes:['Les planches et vignettes sont opaques, pas des sprites détourés.','approved = validation dans la conversation ; delivered = livré sans validation individuelle explicite ; proposed = nouvelle proposition.','Les vignettes de mois conservent leurs libellés ; elles servent de références de tenue.'],assets};
fs.writeFileSync(path.join(root,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cards=assets.map(a=>`<article data-kind="${esc(a.kind)}" data-character="${esc(a.character||'duo')}"><a href="${esc(a.path)}"><img src="${esc(a.path)}" alt="${esc(a.title)}" loading="lazy"></a><h2>${esc(a.title)}</h2><p>${esc(a.id)}</p><small>${a.width} × ${a.height} · ${esc(a.reviewStatus)}</small><a download href="${esc(a.path)}">Télécharger le PNG</a></article>`).join('\n');
fs.writeFileSync(path.join(root,'index.html'),`<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pack comics — Hugo × L’IA</title><style>*{box-sizing:border-box}body{margin:0;background:#f7f4ed;color:#191b32;font:16px system-ui,sans-serif}header,main{max-width:1400px;margin:auto;padding:32px}header{padding-bottom:12px}h1{font-size:clamp(30px,5vw,64px);margin:6px 0}header p{max-width:850px;line-height:1.6}nav{display:flex;flex-wrap:wrap;gap:8px}button{padding:10px 16px;border:1px solid #c9bedf;border-radius:22px;background:white;cursor:pointer}button[aria-pressed=true]{background:#392b65;color:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:20px}article{background:white;border:1px solid #e2ddeb;border-radius:14px;padding:15px;overflow:hidden}article img{width:100%;height:220px;object-fit:contain}article h2{font-size:18px;margin-bottom:5px}article p{font-size:12px;overflow-wrap:anywhere}article small{display:block;color:#655d72;margin-bottom:12px}a{color:#6142a0}article[hidden]{display:none}</style><header><small>BIBLIOTHÈQUE DE RÉFÉRENCE · VERSION 1</small><h1>Hugo × L’IA</h1><p>43 visuels : 7 planches, 12 expressions, 12 poses et 12 vignettes mensuelles. La nouvelle planche de l’IA et ses dérivés restent proposés à validation. Les PNG ont un fond illustré ; ce ne sont pas des découpes transparentes.</p><p><a href="README.md">Mode d’emploi</a> · <a href="docs/PRODUCTION.md">Organisation de la série</a> · <a href="manifest.json">Catalogue pour les agents</a></p><nav aria-label="Filtres"><button aria-pressed="true" data-filter="all">Tout</button><button aria-pressed="false" data-filter="sheets">Planches</button><button aria-pressed="false" data-filter="hugo">Hugo</button><button aria-pressed="false" data-filter="ia">L’IA</button><button aria-pressed="false" data-filter="months">12 mois</button></nav></header><main>${cards}</main><script>for(const b of document.querySelectorAll('button'))b.onclick=()=>{for(const c of document.querySelectorAll('button'))c.setAttribute('aria-pressed',String(c===b));for(const a of document.querySelectorAll('article')){const f=b.dataset.filter;a.hidden=!(f==='all'||f==='sheets'&&a.dataset.kind!=='tile'||f==='months'&&a.dataset.kind==='tile'&&a.dataset.character==='duo'||f===a.dataset.character&&f!=='all')}};</script></html>`);
console.log(`Created ${assets.length} assets, manifest and offline gallery.`);
