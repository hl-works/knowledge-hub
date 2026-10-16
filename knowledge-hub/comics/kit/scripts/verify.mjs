import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const m=JSON.parse(fs.readFileSync(path.join(root,'manifest.json')));
const ids=new Set();
for(const a of m.assets){
 if(ids.has(a.id))throw Error(`Duplicate id: ${a.id}`);ids.add(a.id);
 const p=path.resolve(root,a.path);if(!p.startsWith(root+path.sep))throw Error('External path');
 const b=fs.readFileSync(p);if(b.toString('hex',0,8)!=='89504e470d0a1a0a')throw Error(`Not PNG: ${a.id}`);
 if(b.readUInt32BE(16)!==a.width||b.readUInt32BE(20)!==a.height)throw Error(`Dimensions: ${a.id}`);
 if(crypto.createHash('sha256').update(b).digest('hex')!==a.sha256)throw Error(`Checksum: ${a.id}`);
 if(a.sourceId&&!m.assets.some(s=>s.id===a.sourceId))throw Error(`Source: ${a.id}`);
}
if(!ids.has(m.identityReference))throw Error('Missing canonical reference');
const months=m.assets.filter(a=>a.kind==='tile'&&a.month).map(a=>a.month);
if(new Set(months).size!==12)throw Error('Missing month');
for(const c of ['hugo','ia']){if(m.assets.filter(a=>a.character===c&&a.expression).length!==6||m.assets.filter(a=>a.character===c&&a.pose).length!==6)throw Error(`Missing pose/expression: ${c}`);}
console.log(`OK: ${m.assets.length} PNG, unique IDs, dimensions, hashes, source links, 12 months and 24 acting tiles.`);
