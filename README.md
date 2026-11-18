# Shangri-La: The Last Resort — DM Screen

A tablet DM screen for **Shangri-La: The Last Resort**, a three-session D&D 5e adventure for a weekend away (January 29–31, 2027). It installs as an app on the tablet's home screen and works offline once it has been opened.

Live at **https://dm.mgriffioen.com/** (GitHub Pages; the domain is set by `CNAME`).

## Install on the tablet

1. Open https://dm.mgriffioen.com/ in Chrome.
2. Menu (⋮) → **Install app** (or **Add to Home screen**).
3. Launch it from the home screen. It opens full-screen, like SpellMaster.

Open it once while online so the campaign is cached for offline play. After an update, close the app fully and reopen it to pick up the new version.

## What it does

- **The whole campaign**: three sessions, roll tables, handouts, NPCs, monsters, puzzles, story bible, table guide, prep timeline and overview, rendered from the Markdown files in `content/`. Includes search, section chips, and links between files that jump to the right section.
- **Tap-to-roll**: every d-numbered table, every dice expression in the text, and a dice tray with advantage and disadvantage.
- **Stat blocks**: tap a monster or NPC name for its full stat block, its loot, a **Roll loot** button, and **Roll & add** to send it to initiative.
- **Initiative tracker** with HP bars, Hit and Heal, and downed monsters skipped. Also a party tracker with Contentment and Memory Tokens, a puzzle timer, and session notes.
- **Printing with [SpellMaster](https://spellmaster.mgriffioen.com/)**: **🖨 Print** on any handout card, stat block or the initiative strip copies the card. Switch to the SpellMaster app, already connected to the printer, and it picks the card up from the clipboard. "Open in a new tab" is the fallback.

Party, initiative and notes are saved in the browser on the tablet (`localStorage`).

## Files

| Path | What it is |
|---|---|
| `index.html` | The DM screen: one page, no build step |
| `content/*.md` | The campaign. Edit these to change what the screen shows |
| `manifest.webmanifest`, `icons/` | Home-screen install (name, colours, icons) |
| `sw.js` | Service worker: offline cache; network-first for the page and campaign files |
| `archive/the-wild-sheep-chase/` | The previous DM screen, for *A Wild Sheep Chase*, kept as it was. It's still live at https://dm.mgriffioen.com/archive/the-wild-sheep-chase/ |
| `CNAME` | Custom domain for GitHub Pages |
| `.nojekyll` | Serve files as-is (no Jekyll processing of the Markdown) |

The last commit of the Wild Sheep Chase site at the root is tagged `wild-sheep-chase-final`.

## Editing the campaign

Change the Markdown in `content/` and merge to `main`; GitHub Pages publishes it. The page reads several formats from these files, so keep them when editing:

- **Loot:** NPCs use `- **Loot:** …` lines in `05_NPCs.md`. Monsters use the `## 💰 Loot` table in `06_Monsters.md`.
- **Handouts:** each card in `10_Handouts.md` is a `###` heading with `**Type** / **Value** / **Weight** / **Charges** / **Found** / **Also called** / **DM**` lines and quoted player text.
- **Stat block links:** monster names in *italics* (e.g. `*Mimic*`) open stat blocks.

If you add or rename a file in `content/`, add it to `DOCS` in `index.html` and to `CONTENT` in `sw.js`, and bump `VERSION` in `sw.js`.
