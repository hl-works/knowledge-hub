'use strict';
(() => {
 const blue=[29,78,216],ink=[23,39,71],muted=[83,101,129],green=[0,137,57],red=[207,0,51];
 function create(sections, generatedAt=new Date()) {
  if(!window.jspdf?.jsPDF || !window.GYMA_PDF_ASSETS) throw new Error('Le module PDF n’est pas chargé. Rechargez la page puis réessayez.');
  const doc=new window.jspdf.jsPDF({unit:'mm',format:'a4',compress:true,putOnlyUsedFonts:true});
  doc.addFileToVFS('DejaVuSans.ttf',window.GYMA_PDF_ASSETS.font);
  doc.addFont('DejaVuSans.ttf','DejaVu','normal');doc.setFont('DejaVu','normal');
  doc.setProperties({title:'Réponses de Pierre - Cadrage IA GYMA',subject:'Questionnaire de cadrage - HL Consulting × GYMA',author:'Pierre',creator:'HL Consulting × GYMA'});
  let y=0;
  const width=174,left=18,bottom=274;
  function header(first=false){
   doc.setTextColor(...blue);doc.setFontSize(11);doc.text('HL CONSULTING',left,18);
   doc.addImage(window.GYMA_PDF_ASSETS.logo,'PNG',170,7,22,14.5);
   doc.setDrawColor(...blue);doc.setLineWidth(.8);doc.line(left,25,105,25);doc.setDrawColor(...green);doc.line(105,25,150,25);doc.setDrawColor(...red);doc.line(150,25,192,25);
   y=first?39:36;
   if(first){doc.setFontSize(23);doc.setTextColor(...ink);doc.text('Les réponses de Pierre',left,y);y+=10;
    doc.setFontSize(10);doc.setTextColor(...muted);doc.text('Cadrage du projet IA · GYMA',left,y);y+=7;
    doc.setFontSize(8.5);doc.text('Préparé le '+generatedAt.toLocaleString('fr-FR',{timeZone:'Europe/Paris'})+' (Paris)',left,y);y+=7;
    doc.text('Destinataire : Hugo · HL Consulting',left,y);y+=8;
    doc.setFontSize(9);doc.text('Réponses déclaratives à confirmer lors de l’audit.',left,y);y+=13;}
  }
  function ensure(h){if(y+h>bottom){doc.addPage();header();}}
  function textBlock(value,size=10.5,color=ink,spacing=5.5){
   doc.setFontSize(size);doc.setTextColor(...color);
   // Render supplied text as text only. Explicit newlines and long answers are preserved.
   const lines=doc.splitTextToSize(String(value).replace(/\r\n?/g,'\n'),width);
   for(const line of lines){ensure(spacing);doc.setFontSize(size);doc.setTextColor(...color);doc.text(line,left,y);y+=spacing;}
  }
  header(true);
  for(let i=0;i<sections.length;i++){
   const section=sections[i];doc.setFontSize(13);
   const heading=doc.splitTextToSize(String(i+1).padStart(2,'0')+'  '+section.title,width);
   ensure(heading.length*6+20);
   doc.setTextColor(...blue);doc.setFontSize(13);heading.forEach(line=>{doc.text(line,left,y);y+=6;});y+=3;
   for(const field of section.fields){
    if(section.fields.length>1){ensure(18);textBlock(field.label,9,muted,5);}
    textBlock(field.value);y+=4;
   }
   y+=6;
  }
  const total=doc.getNumberOfPages();
  for(let page=1;page<=total;page++){
   doc.setPage(page);doc.setDrawColor(218,228,243);doc.setLineWidth(.25);doc.line(left,280,192,280);
   doc.setFont('DejaVu','normal');doc.setFontSize(8);doc.setTextColor(...muted);
   doc.text('HL Consulting × GYMA · Réponses de Pierre',left,286);doc.text(page+' / '+total,192,286,{align:'right'});
  }
  return doc;
 }
 window.GymaResponsesPDF={create};
})();
