/* Deterministic checks of the reading timer, suppression and dialog interaction. */
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../knowledge-hub/immersion-ia/follow.js'), 'utf8');
function setup({ hidden=false, dismissed=false, seen=false, blocked=false } = {}) {
  let now = 1000000, next=0, dialogVisible=false;
  const tasks = new Map(), events={}, button={}, link={};
  const storage = entries => ({ getItem(k) { if(blocked) throw Error('blocked'); return entries[k] || null; }, setItem(k,v) { if(blocked) throw Error('blocked'); entries[k]=v; } });
  const panel = {hidden:true, querySelector:()=>({addEventListener:(n,f)=>button[n]=f}), querySelectorAll:()=>[{addEventListener:(n,f)=>link[n]=f}]};
  const doc = {hidden, getElementById:()=>panel, addEventListener:(n,f)=>events[n]=f, querySelectorAll:()=>[{getClientRects:()=>dialogVisible?[{}]:[]}]};
  const local = dismissed?{'kh-follow-dismissed-until':'9000000'}:{};
  const session = seen?{'kh-follow-shown':'1'}:{};
  vm.runInNewContext(code,{document:doc,window:{localStorage:storage(local),sessionStorage:storage(session)},Date:{now:()=>now},setTimeout:(f,delay)=>{tasks.set(++next,{at:now+delay,f});return next;},clearTimeout:id=>tasks.delete(id),getComputedStyle:()=>({visibility:'visible'})});
  function advance(ms) {const end=now+ms; while(true){const due=[...tasks.entries()].filter(([,t])=>t.at<=end).sort((a,b)=>a[1].at-b[1].at)[0];if(!due)break;tasks.delete(due[0]);now=due[1].at;due[1].f();}now=end;}
  return {panel,advance,local,session,close:()=>button.click(),click:()=>link.click(),visibility(value){doc.hidden=value;events.visibilitychange?.();},dialog(value){dialogVisible=value;}};
}
let s=setup();s.advance(29999);assert(s.panel.hidden);s.advance(1);assert(!s.panel.hidden);s.close();assert(s.panel.hidden);assert(Number(s.local['kh-follow-dismissed-until'])>1000000);
s=setup();s.advance(10000);s.visibility(true);s.advance(60000);assert(s.panel.hidden);s.visibility(false);s.advance(19999);assert(s.panel.hidden);s.advance(1);assert(!s.panel.hidden);
for(const options of [{dismissed:true},{seen:true},{hidden:true}]){s=setup(options);s.advance(60000);assert(s.panel.hidden);}
s=setup({blocked:true});s.advance(30000);assert(!s.panel.hidden);s.close();assert(s.panel.hidden);
s=setup();s.dialog(true);s.advance(31000);assert(s.panel.hidden);s.dialog(false);s.advance(1000);assert(!s.panel.hidden);s.click();assert(s.panel.hidden);
console.log('Subscription invitation: all timer, visibility, storage and dismissal checks passed.');
