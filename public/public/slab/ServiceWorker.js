const cacheName = "SLAB-WhereIsMyCatTheAdventure-100006";
const contentToCache = [
    "Build/26911e2d7bce21e98161daee5c8c2598.loader.js",
    "Build/ee2b9f1e2be9439f04f69f40a015326f.framework.js.br",
    "Build/c1412b62618f80f714a2f9969719e66b.data.br",
    "Build/79c874ceb38def5aab344f5538438fd0.wasm.br",
    "TemplateData/style.css"

];

self.addEventListener('install', function (e) {
    console.log('[Service Worker] Install');
    
    e.waitUntil((async function () {
      const cache = await caches.open(cacheName);
      console.log('[Service Worker] Caching all: app shell and content');
      await cache.addAll(contentToCache);
    })());
});

self.addEventListener('fetch', function (e) {
    e.respondWith((async function () {
      let response = await caches.match(e.request);
      console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
      if (response) { return response; }

      response = await fetch(e.request);
      const cache = await caches.open(cacheName);
      console.log(`[Service Worker] Caching new resource: ${e.request.url}`);
      cache.put(e.request, response.clone());
      return response;
    })());
});
