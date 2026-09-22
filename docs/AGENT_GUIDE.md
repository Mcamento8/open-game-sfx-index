# Agent guide — how to pick the right SFX without downloading everything

This repo is designed so an AI agent downloads **kilobytes (index.json)** instead of
**hundreds of megabytes (all audio)**.

## 1. Load the catalog

Raw URL (always current `main`):

```
https://raw.githubusercontent.com/Mcamento8/open-game-sfx-index/main/index.json
```

Schema per entry:

```json
{
  "id": "ui_click_001",
  "title": "UI click 001",
  "pack": "ui-audio",
  "category": "ui",
  "tags": ["ui", "click", "button"],
  "use_cases": ["menu navigation", "mobile tap"],
  "mood": ["neutral", "clean"],
  "keywords_en": ["click", "tap", "button press"],
  "keywords_ar": ["ضغطة", "زر", "نقرة واجهة"],
  "duration_sec": 0.18,
  "formats": ["ogg", "mp3"],
  "file_ogg": "audio/ui-audio/Ogg/click1.ogg",
  "file_mp3": "audio/ui-audio/Mp3/click1.mp3",
  "download_url_ogg": "https://raw.githubusercontent.com/.../audio/ui-audio/Ogg/click1.ogg",
  "download_url_mp3": "https://raw.githubusercontent.com/.../audio/ui-audio/Mp3/click1.mp3",
  "size_ogg": 12345,
  "size_mp3": 15678,
  "license": "CC0-1.0",
  "source": "https://kenney.nl/assets/ui-audio"
}
```

## 2. Search strategy (recommended order)

1. Exact `category` match (`ui`, `interface`, `impact`, `sci-fi`, `digital`,
   `rpg`, `casino`, `music-jingle`, `voiceover`, `retro`, `horror`).
2. `tags` overlap with the task (e.g. task "jump" → tags `jump`, `movement`).
3. `use_cases` / `mood` for ambience fit.
4. Fall back to bilingual keyword search (`keywords_en` + `keywords_ar`).

Use `scripts/search.py` locally, or replicate its scoring in your own runtime.

## 3. Download policy

- Download **only the chosen format** (prefer OGG for games, MP3 for quick preview).
- Cache by `id` + sha256 (`sha256_ogg` / `sha256_mp3` in index).
- Cite `source` + `license: CC0-1.0` in your own credits file (optional, appreciated).
- The `download_url_*` fields are percent-encoded. Some packs keep the upstream
  archive's folder names, which contain spaces and brackets; a client that
  re-encodes an already-encoded URL is fine, but a client that *strips* the
  encoding will produce an unparseable URL. Use the field verbatim.

### ⚠️ Which format can Minecraft actually PLAY?

**Only OGG.** A vanilla 1.8-style `sounds.json` entry resolves to
`assets/<namespace>/sounds/<entry-name>.ogg` — the `.ogg` is appended
unconditionally, with no extension handling. A WAV/MP3/FLAC placed in a resource
pack is copied but never requested, so it plays nothing while looking installed.

| Your target | What to take |
|---|---|
| Minecraft (any version with `sounds.json`) | an **OGG** entry |
| Godot / Unity / Unreal / web | OGG or WAV both fine |
| Quick auditioning / placeholders | MP3 is smallest |

Packs that currently ship **no OGG** (WAV or FLAC only) are:
`oga-512-retro`, `oga-rpg-pack`, `oga-battle`, `oga-gui-lokif`,
`oga-levelup-powerup`, `oga-zombies` (WAV) and `oga-hits-punches` (FLAC).
For a Minecraft target, either transcode those (`ffmpeg -i in.wav -c:a libvorbis
-q:a 5 out.ogg`) or prefer the 11 packs that already ship OGG.

## 4. Category cheat-sheet (most-used first)

| category | when to use | packs |
|----------|-------------|-------|
| ui | buttons, toggles, tabs — every game needs these | ui-audio |
| interface | clicks, hovers, errors, confirmations | interface-sounds |
| impact | hits, crashes, footsteps impacts | impact-sounds |
| sci-fi | lasers, engines, space UI | sci-fi-sounds |
| digital | retro bleeps, pickups | digital-audio |
| rpg | swords, footsteps, potions | rpg-audio |
| casino | cards, dice, chips | casino-audio |
| music-jingle | win/lose stingers, short loops | music-jingles |
| voiceover | fighter grunts, male/female lines | voiceover packs |
| retro | 8-bit/16-bit chiptune arcade | oga-512-retro |
| horror | zombies, monsters, dark ambience | oga-zombies |
