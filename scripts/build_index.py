#!/usr/bin/env python3
"""Rebuild index.json from audio/ + pack metadata.
- Reads OGG/MP3 durations via mutagen, sizes + sha256.
- Infers tags/use_cases/moods/keywords (EN+AR) from filename + pack defaults.
Run after each batch:  python scripts/build_index.py
"""
import datetime
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
INDEX = ROOT / "index.json"
REPO = "Mcamento8/open-game-sfx-index"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"

PACK_META = {
    "ui-audio": {"category": "ui", "source": "https://kenney.nl/assets/ui-audio",
                 "tags": ["ui", "button", "click"], "use_cases": ["menu navigation", "mobile tap", "settings toggle"],
                 "mood": ["neutral", "clean"], "ar": ["زر", "ضغطة", "نقرة واجهة", "قائمة"]},
    "interface-sounds": {"category": "interface", "source": "https://kenney.nl/assets/interface-sounds",
                 "tags": ["interface", "click", "hover", "confirm", "error"], "use_cases": ["dialogs", "inventory", "notifications"],
                 "mood": ["neutral", "crisp"], "ar": ["واجهة", "تأكيد", "خطأ", "تنبيه", "تمرير"]},
    "impact-sounds": {"category": "impact", "source": "https://kenney.nl/assets/impact-sounds",
                 "tags": ["impact", "hit", "collision"], "use_cases": ["combat hit", "crash", "footstep impact"],
                 "mood": ["heavy", "punchy"], "ar": ["اصطدام", "ضربة", "تحطم"]},
    "sci-fi-sounds": {"category": "sci-fi", "source": "https://kenney.nl/assets/sci-fi-sounds",
                 "tags": ["sci-fi", "laser", "space", "engine"], "use_cases": ["shooter", "spaceship", "futuristic UI"],
                 "mood": ["futuristic", "tense"], "ar": ["ليزر", "فضاء", "خيال علمي", "محرك"]},
    "digital-audio": {"category": "digital", "source": "https://kenney.nl/assets/digital-audio",
                 "tags": ["digital", "retro", "blip", "pickup"], "use_cases": ["arcade pickup", "retro UI", "powerup"],
                 "mood": ["retro", "playful"], "ar": ["رقمي", "التقاط", "رجعي"]},
    "rpg-audio": {"category": "rpg", "source": "https://kenney.nl/assets/rpg-audio",
                 "tags": ["rpg", "footstep", "weapon", "foley"], "use_cases": ["exploration", "melee", "potion"],
                 "mood": ["adventurous", "organic"], "ar": ["خطوات", "سيف", "فانتازيا"]},
    "casino-audio": {"category": "casino", "source": "https://kenney.nl/assets/casino-audio",
                 "tags": ["casino", "card", "dice", "chip"], "use_cases": ["card game", "board game", "slots"],
                 "mood": ["playful", "tense"], "ar": ["ورق", "نرد", "كازينو"]},
    "music-jingles": {"category": "music-jingle", "source": "https://kenney.nl/assets/music-jingles",
                 "tags": ["music", "jingle", "stinger"], "use_cases": ["win fanfare", "lose sting", "level complete"],
                 "mood": ["uplifting", "dramatic"], "ar": ["موسيقى", "فوز", "خسارة"]},
    "voiceover-pack": {"category": "voiceover", "source": "https://kenney.nl/assets/voiceover-pack",
                 "tags": ["voice", "male", "female"], "use_cases": ["character barks", "tutorials"],
                 "mood": ["human", "expressive"], "ar": ["صوت بشري", "تعليق"]},
    "voiceover-pack-fighter": {"category": "voiceover", "source": "https://kenney.nl/assets/voiceover-pack-fighter",
                 "tags": ["voice", "fighter", "grunt"], "use_cases": ["fighting game", "efforts", "taunts"],
                 "mood": ["aggressive", "energetic"], "ar": ["مقاتل", "صرخة"]},
}

WORD_SPLIT = re.compile(r"[^a-z0-9\u0600-\u06FF]+")


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def duration(p: pathlib.Path):
    try:
        from mutagen import File as MFile
        m = MFile(str(p))
        if m is not None and hasattr(m, "info") and m.info is not None:
            return round(float(m.info.length), 3)
    except Exception:
        pass
    return None


def main():
    sounds = []
    batches = sorted([d.name for d in AUDIO.iterdir()]) if AUDIO.exists() else []
    for pack in batches:
        meta = PACK_META.get(pack, {"category": pack, "source": "", "tags": [pack],
                                    "use_cases": [], "mood": [], "ar": []})
        pdir = AUDIO / pack
        if not pdir.is_dir():
            continue
        # pair by stem: prefer OGG path as canonical, attach MP3 sibling
        oggs = {p.stem.lower(): p for p in pdir.rglob("*.ogg")}
        mp3s = {p.stem.lower(): p for p in pdir.rglob("*.mp3")}
        stems = sorted(set(oggs) | set(mp3s))
        for stem in stems:
            ogg = oggs.get(stem)
            mp3 = mp3s.get(stem)
            if ogg is None and mp3 is None:
                continue
            base = ogg or mp3
            words = [w for w in WORD_SPLIT.split(stem.lower()) if w]
            tags = sorted(set(meta["tags"] + words[:6]))
            sid = f"{pack}_{stem}".replace(" ", "_")[:120]
            rel_ogg = (ogg.relative_to(ROOT).as_posix()) if ogg else None
            rel_mp3 = (mp3.relative_to(ROOT).as_posix()) if mp3 else None
            dur = duration(ogg or mp3)
            sounds.append({
                "id": sid,
                "title": stem.replace("_", " ").replace("-", " "),
                "pack": pack,
                "category": meta["category"],
                "tags": tags,
                "use_cases": meta["use_cases"],
                "mood": meta["mood"],
                "keywords_en": sorted(set(words + meta["tags"])),
                "keywords_ar": meta["ar"],
                "duration_sec": dur,
                "formats": [f for f, p in (("ogg", ogg), ("mp3", mp3)) if p],
                "file_ogg": rel_ogg,
                "file_mp3": rel_mp3,
                "download_url_ogg": f"{RAW}/{rel_ogg}" if rel_ogg else None,
                "download_url_mp3": f"{RAW}/{rel_mp3}" if rel_mp3 else None,
                "size_ogg": ogg.stat().st_size if ogg else None,
                "size_mp3": mp3.stat().st_size if mp3 else None,
                "sha256_ogg": sha256(ogg) if ogg else None,
                "sha256_mp3": sha256(mp3) if mp3 else None,
                "license": "CC0-1.0",
                "source": meta["source"],
            })
    sounds.sort(key=lambda s: (s["pack"], s["id"]))
    payload = {
        "version": "0.1.0",
        "repo": REPO,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "license_audio": "CC0-1.0",
        "count": len(sounds),
        "batches": batches,
        "sounds": sounds,
    }
    INDEX.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"index.json rebuilt: {len(sounds)} sounds from packs {batches}")


if __name__ == "__main__":
    main()
