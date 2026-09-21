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

## Log

- [ ] Batch 1: ui-audio + interface-sounds
- [ ] Batch 2: impact-sounds
- [ ] Batch 3: sci-fi-sounds + digital-audio
- [ ] Batch 4: rpg-audio + casino-audio
- [ ] Batch 5: music-jingles + voiceover-pack + voiceover-pack-fighter
