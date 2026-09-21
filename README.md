<div align="center">

# 🎮 Open Game SFX Index 🔊

**Every Kenney game sound — searchable by AI, playable in your browser.**

[![Sounds](https://img.shields.io/badge/sounds-744-brightgreen?style=for-the-badge)](previews/README.md)
[![Packs](https://img.shields.io/badge/packs-10-blue?style=for-the-badge)](SOURCES.md)
[![License](https://img.shields.io/badge/license-CC0_1.0-lightgrey?style=for-the-badge)](ATTRIBUTION.md)
[![AI Ready](https://img.shields.io/badge/AI-index.json-orange?style=for-the-badge)](docs/AGENT_GUIDE.md)

[🎧 **Listen now**](previews/README.md) · [🤖 **Agent guide**](docs/AGENT_GUIDE.md) · [📖 **Sources**](SOURCES.md) · [⚖️ **License**](ATTRIBUTION.md)

</div>

---

## ✨ What is this?

**744 public-domain game sound effects** (OGG, ~12 MB total) from
[Kenney.nl](https://kenney.nl/assets/category:Audio), organized so that
**humans can listen in one click** and **AI agents can search without downloading everything**.

| I am… | Do this |
|-------|---------|
| 🧑 Human | Open [🎧 **previews/README.md**](previews/README.md) → pick a pack → press ▶ on any sound |
| 🤖 AI agent | Fetch [`index.json`](https://raw.githubusercontent.com/Mcamento8/open-game-sfx-index/main/index.json) → filter → download **one** file |

> ⚖️ **100% copyright-safe:** all audio is **Creative Commons CC0 1.0** (public domain).
> Independent community index — not affiliated with Kenney. Proof in [ATTRIBUTION.md](ATTRIBUTION.md).

## 🎧 Listen (no download needed)

| Pack | Sounds | Listen | Upstream |
|------|--------|--------|----------|
| 🔘 UI Audio | 51 | [▶ Play](previews/ui-audio.md) | [kenney.nl](https://kenney.nl/assets/ui-audio) |
| 🖱️ Interface Sounds | 100 | [▶ Play](previews/interface-sounds.md) | [kenney.nl](https://kenney.nl/assets/interface-sounds) |
| 💥 Impact Sounds | 130 | [▶ Play](previews/impact-sounds.md) | [kenney.nl](https://kenney.nl/assets/impact-sounds) |
| 🚀 Sci-Fi Sounds | 73 | [▶ Play](previews/sci-fi-sounds.md) | [kenney.nl](https://kenney.nl/assets/sci-fi-sounds) |
| 👾 Digital Audio | 62 | [▶ Play](previews/digital-audio.md) | [kenney.nl](https://kenney.nl/assets/digital-audio) |
| ⚔️ RPG Audio | 51 | [▶ Play](previews/rpg-audio.md) | [kenney.nl](https://kenney.nl/assets/rpg-audio) |
| 🎰 Casino Audio | 54 | [▶ Play](previews/casino-audio.md) | [kenney.nl](https://kenney.nl/assets/casino-audio) |
| 🎵 Music Jingles | 85 | [▶ Play](previews/music-jingles.md) | [kenney.nl](https://kenney.nl/assets/music-jingles) |
| 🎙️ Voiceover Pack (Male ♂ / Female ♀) | 92 | [▶ Play](previews/voiceover-pack.md) | [kenney.nl](https://kenney.nl/assets/voiceover-pack) |
| 🥊 Voiceover Pack (Fighter) | 46 | [▶ Play](previews/voiceover-pack-fighter.md) | [kenney.nl](https://kenney.nl/assets/voiceover-pack-fighter) |

## 🤖 For AI agents

```python
import json, urllib.request
URL = "https://raw.githubusercontent.com/Mcamento8/open-game-sfx-index/main/index.json"
idx = json.load(urllib.request.urlopen(URL))          # kilobytes, not megabytes
hits = [s for s in idx["sounds"]                      # filter locally
        if "click" in s["tags"] and s["category"] == "ui"]
print(hits[0]["download_url_ogg"])                    # download ONE file only
```

Or locally: `python scripts/search.py --q "button click" --limit 5`
(Arabic works too: `--q "زر"`)

📖 Full guide: [docs/AGENT_GUIDE.md](docs/AGENT_GUIDE.md)

Each entry carries: `id, title, pack, category, tags, use_cases, mood,`
bilingual `keywords_en/ar, duration_sec, size, sha256, download URLs, license, source`.

## 📁 Layout

```
├── previews/            # ▶ per-pack listening pages (start here as a human)
├── audio/<pack>/        # 744 OGG files (voiceover split into Male/ + Female/)
├── index.json           # master machine catalog (agents read this)
├── categories.json      # category descriptions
├── scripts/search.py    # offline keyword search (EN + AR)
├── scripts/build_index.py      # rebuild index.json
├── scripts/build_previews.py   # rebuild previews/
├── docs/AGENT_GUIDE.md  # how agents pick the right SFX
├── SOURCES.md           # exact upstream ZIP URLs
├── ATTRIBUTION.md       # CC0 proof + credit
└── batches/STATUS.md    # upload log
```

## ❓ FAQ

**Is this the complete Kenney audio collection?**
Yes — all **10 packs** in the [Audio category](https://kenney.nl/assets/category:Audio),
verified file-by-file against the upstream ZIPs (753 OGG shipped − 9 preview tracks = **744**).

**Why OGG only?**
Upstream ships OGG only. OGG plays natively on GitHub file pages and in every game engine,
at a fraction of WAV size (whole library ≈ 12 MB).

**Can I use these commercially?**
Yes. CC0 = public domain: commercial use, modification and redistribution allowed,
no permission or attribution required (credit appreciated).

## ⚖️ License

- **Audio (`audio/`)**: CC0 1.0 Universal — public domain, by Kenney.
- **Code / metadata / docs**: MIT — see [LICENSE](LICENSE).
