// Service worker minimal — coquille hors-ligne pour Atlas d'Asie.
// Stratégie réseau d'abord, repli sur le cache (utile en bus/steppe sans réseau).
const CACHE = 'atlas-asie-v4';
// Coquille + données précachées à l'installation : le site complet se
// consulte hors ligne dès la première visite (bus en Mongolie approuvé).
const SHELL = [
  './', './parcours/', './pays/', './hotels/', './trajets/', './carnet/', './galerie/', './offline.html',
  './fixtures/parcours.csv', './fixtures/pays.csv', './fixtures/quiz.csv', './fixtures/bestiaire.csv',
  './fixtures/lexique.csv', './fixtures/transports.csv', './fixtures/pratique.csv', './fixtures/aeroports.csv',
  './fixtures/lieux.csv', './fixtures/miam.csv', './fixtures/recits.csv', './fixtures/photos.json',
  './manifest.webmanifest', './photos/manifest.json',
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL).catch(() => {})));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  e.respondWith(
    fetch(req)
      .then((res) => {
        // Réseau d'abord, et on garde une copie de TOUT ce qui servira hors
        // ligne : pages, CSS/JS (_astro), données (CSV/JSON — y compris les
        // URLs Google Sheets publiées, qui ne finissent pas par .csv), images
        // (Commons est en CORS via crossorigin), fontes.
        if (res.ok || res.type === 'opaque') {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      })
      .catch(async () => {
        const hit = await caches.match(req);
        if (hit) return hit;
        // Navigation vers une page jamais visitée : page hors-ligne tamponnée.
        if (req.destination === 'document') {
          return (await caches.match('./offline.html')) || caches.match('./');
        }
        return caches.match('./');
      }),
  );
});
