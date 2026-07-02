#!/usr/bin/env node
// Ajoute des photos du voyage à une escale de l'Atlas d'Asie.
//
//   node scripts/add-photos.mjs <ordre> [--legende "…"] fichier1.jpg [fichier2.heic …]
//
// - redimensionne à 1600 px max (JPEG qualité 75, ~200-400 Ko) via sharp
// - range dans atlas-asie-app/public/photos/<ordre>/NN.jpg
// - met à jour public/photos/manifest.json (fusionné par le site avec la Sheet)
// La légende s'applique à toutes les photos de l'appel (relancer par lot sinon).
// Ensuite : rebuild Astro + build_atlas_static.py + commit (cf. CLAUDE.md).
import { createRequire } from 'node:module';
import { mkdirSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(resolve(repo, 'atlas-asie-app', 'package.json'));
const sharp = require('sharp');

const args = process.argv.slice(2);
const ordre = args.shift();
let legende = '';
const li = args.indexOf('--legende');
if (li !== -1) { legende = args[li + 1] ?? ''; args.splice(li, 2); }
if (!ordre || !/^\d+$/.test(ordre) || !args.length) {
  console.error('Usage : node scripts/add-photos.mjs <ordre> [--legende "…"] fichiers…');
  process.exit(1);
}

const photosDir = resolve(repo, 'atlas-asie-app', 'public', 'photos');
const destDir = resolve(photosDir, ordre);
mkdirSync(destDir, { recursive: true });
const manifestPath = resolve(photosDir, 'manifest.json');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
manifest[ordre] ??= [];

let n = readdirSync(destDir).filter((f) => f.endsWith('.jpg')).length;
for (const file of args) {
  n += 1;
  const name = String(n).padStart(2, '0') + '.jpg';
  const out = resolve(destDir, name);
  await sharp(file).rotate().resize({ width: 1600, height: 1600, fit: 'inside', withoutEnlargement: true })
    .jpeg({ quality: 75, mozjpeg: true }).toFile(out);
  const entry = { src: `photos/${ordre}/${name}` };
  if (legende) entry.legende = legende;
  manifest[ordre].push(entry);
  console.log(`✓ escale ${ordre} ← ${name}${legende ? ` (« ${legende} »)` : ''}`);
}
writeFileSync(manifestPath, JSON.stringify(manifest, null, 1) + '\n');
console.log(`manifest.json : escale ${ordre} → ${manifest[ordre].length} photo(s)`);
