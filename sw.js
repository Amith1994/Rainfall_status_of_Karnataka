const CACHE_NAME = 'gkms-karnataka-v2';
const STATIC_ASSETS = [
    './',
    '1st_updated.html',
    'index.html',
    'assets/icon.png',
    'assets/icon.ico',
    'manifest.json'
];

// Install Event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('[Service Worker] Pre-caching static assets');
            return cache.addAll(STATIC_ASSETS);
        }).then(() => self.skipWaiting())
    );
});

// Activate Event
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        console.log('[Service Worker] Removing old cache', key);
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event - Network First for HTML, Cache First for assets/CDNs
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);
    
    // Check if it's an HTML file or root path
    const isHtml = event.request.mode === 'navigate' || 
                   url.pathname.endsWith('.html') || 
                   url.pathname === '/' || 
                   url.pathname.endsWith('/');

    if (isHtml) {
        // Network-first strategy for HTML (keeps weather data fresh)
        event.respondWith(
            fetch(event.request)
                .then(networkResponse => {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                })
                .catch(() => {
                    // Offline fallback
                    return caches.match(event.request);
                })
        );
    } else {
        // Cache-first strategy for static assets, fonts, leaflet JS/CSS, and CDN assets
        event.respondWith(
            caches.match(event.request).then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse;
                }
                
                return fetch(event.request).then(networkResponse => {
                    // Only cache valid responses (not extension/chrome requests)
                    if (networkResponse.status === 200 && (url.origin === self.location.origin || url.origin.includes('unpkg.com') || url.origin.includes('cdnjs.cloudflare.com') || url.origin.includes('fonts.googleapis.com') || url.origin.includes('fonts.gstatic.com'))) {
                        return caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    }
                    return networkResponse;
                }).catch(err => {
                    console.error('[Service Worker] Fetch failed:', err);
                });
            })
        );
    }
});
