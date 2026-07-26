/* Str8 — service worker : app-shell offline. */
const CACHE = 'str8-v0-1-20260726a';
const ASSETS = [
  './', './index.html',
  './style.css?v=20260726a',
  './media.js?v=20260726a', './data.js?v=20260726a', './store.js?v=20260726a', './app.js?v=20260726a',
  './manifest.webmanifest', './icon.svg',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const { request } = e;
  if (request.method !== 'GET') return;
  e.respondWith(
    caches.match(request, { ignoreSearch: false }).then(cached => {
      if (cached) return cached;
      return fetch(request).then(res => {
        // cache à la volée (fonts Google incluses, réponses opaques comprises)
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(request, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match('./index.html'));
    })
  );
});
