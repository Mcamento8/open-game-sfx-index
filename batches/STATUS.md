# Batch protocol (disk-safe)

Goal: mirror ~730 upstream sounds as OGG+MP3 (~1460 files) **without filling the disk**.

## Order (most-used / most-popular first — based on game-dev usage)

1. **Batch 1 (highest priority):** `ui-audio` (50) + `interface-sounds` (100)
   → every game needs UI clicks. ~150 sounds → ~300 files.
2. **Batch 2:** `impact-sounds` (130) → hits/collisions, 2nd most-used.
3. **Batch 3:** `sci-fi-sounds` (70) + `digital-audio` (60) → shooters/arcade popular.
4. **Batch 4:** `rpg-audio` (50) + `casino-audio` (50) → genre foley.
5. **Batch 5:** `music-jingles` (85) + `voiceover-pack` (90) + `voiceover-pack-fighter` (45).

## Per-batch steps (repeat, delete temp each time)

1. Download ONE pack ZIP into `_tmp/` (never keep 2 zips at once).
2. Extract, **keep only OGG+MP3**, delete WAV + ZIP immediately.
3. Move to `audio/<pack>/` with original filenames.
4. Run `python scripts/build_index.py` to regenerate `index.json`.
5. `git add audio/<pack> index.json` → commit `feat(batch-N): add <pack>` → push.
6. Verify on github.com, then `rm -rf _tmp/*` (frees disk before next batch).
7. Update this file + README status table.

## Log (completed 2026-09-21 — temp ZIPs deleted after each push, disk-safe)

- [x] Batch 1: ui-audio (51) + interface-sounds (100) → 151 indexed — pushed `1f78fa4`
- [x] Batch 2: impact-sounds (130) → 281 total — pushed `f9ce9b9`
- [x] Batch 3: sci-fi-sounds (73) + digital-audio (62) → 416 total — pushed `303b6cf`
- [x] Batch 4: rpg-audio (51) + casino-audio (54) → 521 total — pushed `f09841b`
- [x] Batch 5: music-jingles (85) + voiceover-pack (92) + voiceover-pack-fighter (46) → 744 total (after voiceover fix below)

Note: upstream packs contain OGG only (no MP3/WAV), so the mirror is OGG files,
~12.5 MB total. index.json `formats`/`download_url_mp3` are null where MP3 does not exist.

## Wave 2 — OpenGameArt CC0 (2026-09-21, +707 sounds → 1451 total)

License audit first (`scripts/oga_audit.py`): 11/16 candidate packs CC0.
Skipped: 5 non-CC0 packs + 5 Kenney re-uploads (dupes of Wave 1).
`__MACOSX`/`._` junk removed (144 files); AIFF→WAV lossless; FLAC supported.

- [x] oga-512-retro (512, SubspaceAudio) + oga-rpg-pack (96, artisticdude)
- [x] oga-gui-lokif (13) + oga-hits-punches (37 FLAC) + oga-levelup-powerup (13)
- [x] oga-zombies (24) + oga-footsteps (8) + oga-battle (4)

## Not mirrored (legal reasons — see ATTRIBUTION.md)

- Sonniss GDC: redistribution as sound library prohibited + AI use prohibited.
- Freesound: needs user API key (OAuth for originals); API ToS forbids DB replication.
  → pending user credentials for a small curated import.

## Fix 2026-09-21: voiceover-pack completeness

Audit found `voiceover-pack` ships `Male/1.ogg` + `Female/1.ogg` (same basenames),
so flat extraction overwrote 44 files (repo had 48, upstream 92).
Fixed by preserving `Male/` + `Female/` subfolders; `build_index.py` now keys by
relative path for collision-proof IDs. Verified: 753 OGG in upstream ZIPs −
9 preview tracks = **744 mirrored**. All `_tmp/` audit ZIPs deleted.
