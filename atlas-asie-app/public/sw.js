// Service worker minimal — coquille hors-ligne pour Atlas d'Asie.
// Stratégie réseau d'abord, repli sur le cache (utile en bus/steppe sans réseau).
const CACHE = 'atlas-asie-v1';
const SHELL = ['./', './parcours/', './pays/', './hotels/', './trajets/', './carnet/', './galerie/'];

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
        if (res.ok && (req.url.endsWith('.csv') || req.destination === 'document')) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      })
      .catch(() => caches.match(req).then((m) => m || caches.match('./'))),
  );
});
