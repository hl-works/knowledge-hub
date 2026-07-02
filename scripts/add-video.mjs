#!/usr/bin/env node
// Ajoute une vidéo légère du voyage à une escale de l'Atlas d'Asie.
//
//   node scripts/add-video.mjs <ordre> [--legende "…"] video.mp4|mov
//
// - compresse en H.264 720p (CRF 27, audio AAC 96k, faststart) via ffmpeg
//   ⚠️ nécessite le vrai ffmpeg : apt-get update && apt-get install -y ffmpeg
// - extrait une image poster (premier plan net) en .webp
// - range dans atlas-asie-app/public/photos/<ordre>/NN.mp4 + met à jour
//   public/photos/manifest.json (type "video") ; rendue en <video> sur
//   l'escale du Parcours. Viser des clips courts (< ~60 s, < ~25 Mo).
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
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
if (!ordre || !/^\d+$/.test(ordre) || args.length !== 1) {
  console.error('Usage : node scripts/add-video.mjs <ordre> [--legende "…"] video');
  process.exit(1);
}

const destDir = resolve(repo, 'atlas-asie-app', 'public', 'photos', ordre);
mkdirSync(destDir, { recursive: true });
const n = readdirSync(destDir).filter((f) => /\.(jpg|webp|mp4)$/.test(f) && !f.includes('-poster')).length + 1;
const base = String(n).padStart(2, '0');
const outVid = resolve(destDir, base + '.mp4');
const outPoster = resolve(destDir, base + '-poster.webp');

execFileSync('ffmpeg', ['-y', '-i', args[0],
  '-vf', "scale='min(1280,iw)':-2", '-c:v', 'libx264', '-crf', '27', '-preset', 'medium',
  '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', outVid], { stdio: 'inherit' });
const tmpJpg = outPoster.replace('.webp', '.tmp.jpg');
execFileSync('ffmpeg', ['-y', '-ss', '0.5', '-i', outVid, '-frames:v', '1', tmpJpg], { stdio: 'ignore' });
await sharp(tmpJpg).webp({ quality: 75 }).toFile(outPoster);
execFileSync('rm', [tmpJpg]);

const mb = statSync(outVid).size / 1048576;
if (mb > 25) console.warn(`⚠️ ${mb.toFixed(1)} Mo — c'est lourd : envisager de couper le clip.`);

const manifestPath = resolve(repo, 'atlas-asie-app', 'public', 'photos', 'manifest.json');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
manifest[ordre] ??= [];
const entry = { src: `photos/${ordre}/${base}.mp4`, type: 'video', poster: `photos/${ordre}/${base}-poster.webp` };
if (legende) entry.legende = legende;
manifest[ordre].push(entry);
writeFileSync(manifestPath, JSON.stringify(manifest, null, 1) + '\n');
console.log(`✓ escale ${ordre} ← ${base}.mp4 (${mb.toFixed(1)} Mo)${legende ? ` (« ${legende} »)` : ''}`);
