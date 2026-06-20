# A Wild Sheep Chase – DM Reference

A single-file, mobile-friendly DM reference site for running [A Wild Sheep Chase](https://www.drivethrurpg.com/product/149267/A-Wild-Sheep-Chase) by Winghorn Press. Built for use on a tablet at the table — no internet required once loaded.

## Features

- **Scene guide** — full walkthrough of each encounter with notes and optional full PDF text
- **NPC & Monster stat blocks** — clickable cards with full stats in a modal overlay, including custom entries (Bed Dragon Wyrmling, polymorphed wolves and rats, Gibbering Mouther, drunk patron, seagull, and more)
- **Live HP trackers** — per-creature HP tracking with +/− buttons, persisted to `localStorage`; supports multiple tokens for grouped creatures (wolves, giant rats)
- **Player character sheets** — quick-reference cards for Bram, Dusty, and Medrick with key stats, abilities, and equipment
- **Initiative tracker** — add combatants manually or via quick-add buttons (one per PC and common monster); numeric keypad auto-opens on mobile/tablet; full-screen mode hides the rest of the page
- **Key items** — Scroll of Speak With Animals (with player-facing seal image), Modified Wand of True Polymorph with full d20 misfire table
- **Beginner cheat sheet** — embedded PDF link for new players

## Files

| File | Description |
|---|---|
| `index.html` | Entire site — open this in a browser |
| `scroll-seal.jpg` | Scroll seal image shown to players |
| `player_cheat_sheet.pdf` | Beginner cheat sheet for new players |
| `make_cheatsheet.py` | ReportLab script used to generate the cheat sheet PDF |
| `Bram_Thornvale.pdf` | Bram's full character sheet |
| `Dusty_Fleetwood.pdf` | Dusty's full character sheet |
| `Medrick_Bendelroot.pdf` | Medrick's full character sheet |
| `the_wild_sheep_chase_v2.pdf` | The adventure PDF (Winghorn Press) |

## Usage

Open `index.html` in any modern browser. Everything is self-contained — no build step, no dependencies, no server needed.

For tablet use at the table, add it to your home screen or bookmark it locally. The initiative tracker's full-screen mode (`⛶ Full Screen`) is designed for keeping the tracker visible during combat without the rest of the page.

## Adventure

*A Wild Sheep Chase* is a short D&D 5E adventure by Winghorn Press, designed for 3–5 characters of level 3. The party must rescue a wizard who has been polymorphed into a sheep by a rival. Available free at [Winghorn Press](https://winghornpress.com/).
