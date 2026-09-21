# Open Game SFX Index 🎮🔊

**AI-searchable index of public-domain game sound effects (OGG + MP3) with a machine-readable catalog.**

AI agents and developers can **search `index.json` first** (tags, categories, use-cases in English + Arabic keywords),
**preview a single file**, then **download only that file** — no need to clone/download the whole library.

> ⚖️ **No copyright risk:** all audio files are from [Kenney.nl](https://kenney.nl/assets/category:Audio)
> released under **Creative Commons CC0 1.0 Universal (public domain)**.
> This repo is an **independent community index** — not affiliated with or endorsed by Kenney.
> See [ATTRIBUTION.md](ATTRIBUTION.md) and [SOURCES.md](SOURCES.md).

## 📊 Status

| Pack | Files (upstream) | Status |
|------|------------------|--------|
| UI Audio (most-used first) | 50 | ⏳ Batch 1 |
| Interface Sounds (most-used first) | 100 | ⏳ Batch 1 |
| Impact Sounds | 130 | ⏳ Batch 2 |
| Sci-fi Sounds | 70 | ⏳ Batch 3 |
| Digital Audio | 60 | ⏳ Batch 3 |
| RPG Audio | 50 | ⏳ Batch 4 |
| Casino Audio | 50 | ⏳ Batch 4 |
| Music Jingles | 85 | ⏳ Batch 5 |
| Voiceover Pack | 90 | ⏳ Batch 5 |
| Voiceover Pack (Fighter) | 45 | ⏳ Batch 5 |
| **Total** | **~730 upstream → ~1460 OGG+MP3** | |

Progress is tracked in [`batches/STATUS.md`](batches/STATUS.md).

## 🤖 For AI agents (read this!)

1. **Fetch the catalog** (small, KBs):
   `https://raw.githubusercontent.com/Mcamento8/open-game-sfx-index/main/index.json`
2. **Filter in your code** by `category`, `tags`, `use_cases`, `mood`, or bilingual `keywords_ar` / `keywords_en`.
   Example (Python):
   ```python
   import json, urllib.request
   idx = json.load(urllib.request.urlopen("https://raw.githubusercontent.com/Mcamento8/open-game-sfx-index/main/index.json"))
   hits = [s for s in idx["sounds"] if "click" in s["tags"] and s["formats"] ]
   print(hits[0])  # contains download_url_ogg + download_url_mp3
   ```
3. **Download ONE file only:**
   `download_url_ogg` or `download_url_mp3` from the matched entry (raw.githubusercontent.com URL).
4. **Never clone the whole repo** for a single SFX. Full clone is only for mirroring.

Full guide: [`docs/AGENT_GUIDE.md`](docs/AGENT_GUIDE.md)
Lightweight search helper: [`scripts/search.py`](scripts/search.py)

```bash
python scripts/search.py --q "button click" --category ui --limit 5
python scripts/search.py --q "زر ضغطة" --limit 5   # Arabic keywords supported
```

## 📁 Layout

```
open-game-sfx-index/
  README.md            # this file
  ATTRIBUTION.md       # credit + CC0 proof
  SOURCES.md           # upstream pack URLs + hashes
  LICENSE              # MIT for code/scripts + CC0 note for audio
  index.json           # MASTER catalog (agents read this)
  categories.json      # category → description + counts
  audio/<pack>/...ogg/.mp3
  scripts/search.py    # keyword search (no heavy deps)
  scripts/build_index.py
  docs/AGENT_GUIDE.md
  batches/STATUS.md
```

## 🎧 Formats

Upstream zips contain `WAV + OGG + MP3` per sound.
To keep the repo lean and GitHub-friendly, **only `OGG + MP3` are stored**:

- `OGG` → best quality/size for games (recommended)
- `MP3` → universal preview compatibility
- `WAV` → skipped (large, redundant; regenerable from upstream)

## ⚖️ License

- **Audio (`audio/`)**: CC0 1.0 Universal — public domain. Do anything, no attribution required (credit appreciated).
  Source: Kenney — https://kenney.nl/assets/category:Audio
- **Code/metadata (`scripts/`, `index.json`, docs)**: MIT (see LICENSE).

## 🤝 Contributing

Batch uploads welcome. See `batches/STATUS.md` for the batch protocol
(download 1 pack → keep OGG+MP3 → rebuild index → push → delete zip/temp/WAV).
