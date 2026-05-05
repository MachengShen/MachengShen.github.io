const VERSION = 'macheng-agent-sw-v5-reset'
const CACHE_PREFIX = 'macheng-agent-pwa-'

self.addEventListener('install', (event) => {
  event.waitUntil(Promise.resolve())
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith(CACHE_PREFIX))
            .map((key) => caches.delete(key)),
        ),
      )
      .then(() => self.clients.claim())
      .then(() => self.clients.matchAll({ type: 'window' }))
      .then((clients) => {
        for (const client of clients) {
          client.postMessage({ type: 'SW_VERSION', version: VERSION })
        }
      }),
  )
})
