/*
 * Service worker for the Last Resort DM screen.
 *
 * - The app and the campaign files are cached on install, so the screen works
 *   offline at the table once it has been opened once.
 * - The page, campaign files, maps and portraits are network-first: when online
 *   you always get the latest version, and the cached copy is the fallback.
 *   Requests skip the browser's HTTP cache (GitHub Pages lets it keep images for
 *   hours), so a replaced portrait or map shows up on the next load.
 * - Fonts and the markdown library (other sites) are served from cache and
 *   refreshed in the background.
 * - The archived Wild Sheep Chase site under /archive/ is left alone.
 *
 * Bump VERSION when adding or renaming a campaign file so the new list is
 * precached; ordinary edits to existing files arrive on their own.
 */
const VERSION = "last-resort-v15";
const CONTENT = [
  "00_README.md", "01_Story_Bible.md", "02_Session1_Millhaven.md", "03_Session2_Undercroft.md",
  "04_Session3_ShangriLa.md", "05_NPCs.md", "06_Monsters.md", "07_Puzzles.md", "08_Roll_Tables.md",
  "09_Table_Guide.md", "10_Handouts.md", "11_Prep_Timeline.md",
].map(f => "content/" + f);
// Battlemaps and handout art for the Maps page (keep in step with MAPS and MAP_V in index.html).
const MAP_V = 4;
const MAPS = [
  "scn2-fish-toss-fight", "rm02-bullywug-hollow", "rm03-fishfolk-camp", "rm04-three-oaks-steam-hall",
  "rm05-toll-bridge", "rm06-mothers-grave", "rm07-grotto-portal", "rm08-hall-of-five-doors",
  "rm09-welcome-hall-seers-floor", "scn5-gilded-hand-fight",
  "sla1-the-vale", "sla2-vale-revealed", "sla3-heart-beneath", "sla4-escape-across",
  "ho01-millhaven", "ho02-undercroft", "ho03-shangri-la", "ho04-seers-floor-key",
].flatMap(f => ["maps/" + f + ".jpg?v=" + MAP_V, "maps/thumbs/" + f + ".jpg?v=" + MAP_V]);
// Generated NPC and monster portraits (keep in step with the image lines in content/05_NPCs.md and 06_Monsters.md).
const PORTRAITS = [
  "alric-thane", "auntie-grell", "baby-mimic", "bastian", "brother-ansel",
  "bullywugs", "content-guests", "corwin-vell", "feast-mimics", "fishfolk",
  "gilded-hand-crew", "groundskeepers", "heart-of-shangri-la", "ilsabet-quill", "king-bulgrot",
  "lantern-imps", "little-holm", "mira-grell", "old-mossback", "oldmin-paulus",
  "roderic-saye", "snik", "the-luggage", "the-steward", "tidy-hands",
  "tobias-vell", "towel-golems", "wren",
].map(f => "portraits/" + f + ".jpg");
const SHELL = [
  "./", "index.html", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-192.png", "icons/icon-maskable-512.png",
  ...CONTENT,
  ...MAPS,
  ...PORTRAITS,
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(VERSION).then(cache => cache.addAll(SHELL.map(u => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
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
    // "no-cache" revalidates with the server (a cheap 304 when nothing changed) instead of trusting the HTTP cache.
    const response = await fetch(request, { cache: "no-cache" });
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
