// static/sw.js
let jwtToken = null;

self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SET_JWT') {
    jwtToken = event.data.token;
    console.log('[SW] JWT set:', jwtToken);
  }
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // Intercept only API calls
  if (url.pathname.startsWith('/api/')) {
    const headers = new Headers(event.request.headers);
    if (jwtToken) {
      headers.set('Authorization', 'Bearer ' + jwtToken);
    }
    const modReq = new Request(event.request, {
      method: event.request.method,
      headers,
      body: event.request.body,
      mode: event.request.mode,
      credentials: event.request.credentials,
      redirect: event.request.redirect,
      cache: event.request.cache
    });
    event.respondWith(fetch(modReq));
  }
});
