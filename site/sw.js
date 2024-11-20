const CACHE_NAME = 'schoolkit-v1';
const urlsToCache = [
    '/',
    '/home.html',
    '/chat.html',
    '/info.html',
    '/contact.html',
    '/styles.css',
    '/home.css',
    '/chat.css',
    '/info.css',
    '/script.js',
    '/home.js',
    '/chat.js',
    'https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request)
                    .then(response => {
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });
                        return response;
                    });
            })
    );
});