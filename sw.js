/*
 * Service worker for the Last Resort DM screen.
 *
 * - The app and the campaign files are cached on install, so the screen works
 *   offline at the table once it has been opened once.
 * - The page and campaign files are network-first: when online you always get
 *   the latest version, and the cached copy is the fallback.
 * - Fonts and the markdown library (other sites) are served from cache and
 *   refreshed in the background.
 * - The archived Wild Sheep Chase site under /archive/ is left alone.
 *
 * Bump VERSION when adding or renaming a campaign file so the new list is
 * precached; ordinary edits to existing files arrive on their own.
 */
const VERSION = "last-resort-v2";
const CONTENT = [
  "00_README.md", "01_Story_Bible.md", "02_Session1_Millhaven.md", "03_Session2_Undercroft.md",
  "04_Session3_ShangriLa.md", "05_NPCs.md", "06_Monsters.md", "07_Puzzles.md", "08_Roll_Tables.md",
  "09_Table_Guide.md", "10_Handouts.md", "11_Prep_Timeline.md", "12_Magic_Items.md",
].map(f => "content/" + f);
const SHELL = [
  "./", "index.html", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-192.png", "icons/icon-maskable-512.png",
  ...CONTENT,
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(VERSION).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

async function networkFirst(request) {
  const cache = await caches.open(VERSION);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await cache.match(request, { ignoreSearch: true });
    if (cached) return cached;
    if (request.mode === "navigate") return (await cache.match("index.html")) || Response.error();
    return Response.error();
  }
}

async function staleWhileRevalidate(request) {
  const cache = await caches.open(VERSION);
  const cached = await cache.match(request);
  const fresh = fetch(request)
    .then(response => {
      if (response.ok || response.type === "opaque") cache.put(request, response.clone());
      return response;
    })
    .catch(() => cached);
  return cached || fresh;
}

self.addEventListener("fetch", event => {
  const { request } = event;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin === self.location.origin) {
    if (url.pathname.includes("/archive/")) return; // the old site manages itself
    event.respondWith(networkFirst(request));
    return;
  }
  if (/(^|\.)fonts\.(googleapis|gstatic)\.com$|^cdnjs\.cloudflare\.com$/.test(url.hostname)) {
    event.respondWith(staleWhileRevalidate(request));
  }
});
