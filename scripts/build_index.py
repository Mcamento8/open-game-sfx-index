#!/usr/bin/env python3
"""Rebuild index.json from audio/ + pack metadata.
- Reads OGG/MP3/WAV durations via mutagen, sizes + sha256.
- Infers tags/use_cases/moods/keywords (EN+AR) from filename + pack defaults.
Run after each batch:  python scripts/build_index.py
"""
import datetime
import hashlib
import json
import pathlib
import urllib.parse
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
INDEX = ROOT / "index.json"
REPO = "Mcamento8/open-game-sfx-index"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"


def raw_url(rel: str) -> str:
    """Build a fetchable raw URL for a repo-relative path.

    Percent-encode each path segment: several packs (oga-512-retro,
    oga-rpg-pack) keep the upstream archive's directory names, which contain
    spaces and square brackets. Emitting those literally produces a URL that no
    HTTP client will even parse, so every one of those entries was unusable as
    written — the file existed, the link did not work.
    """
    return RAW + "/" + "/".join(urllib.parse.quote(seg, safe="") for seg in rel.split("/"))

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
    "oga-512-retro": {"category": "retro", "source": "https://opengameart.org/content/512-sound-effects-8-bit-style",
                 "tags": ["retro", "8-bit", "16-bit", "chiptune", "arcade"], "use_cases": ["retro platformer", "pickup", "jump", "shoot"],
                 "mood": ["retro", "playful"], "ar": ["ريترو", "8 بت", "أركيد", "التقاط", "قفز"]},
    "oga-rpg-pack": {"category": "rpg", "source": "https://opengameart.org/content/rpg-sound-pack",
                 "tags": ["rpg", "fantasy", "battle", "inventory", "npc"], "use_cases": ["exploration", "combat", "inventory"],
                 "mood": ["adventurous", "organic"], "ar": ["فانتازيا", "معركة", "وحش", "عملات"]},
    "oga-gui-lokif": {"category": "ui", "source": "https://opengameart.org/content/gui-sound-effects",
                 "tags": ["ui", "gui", "click", "button"], "use_cases": ["menu navigation", "settings"],
                 "mood": ["neutral", "clean"], "ar": ["زر", "واجهة", "قائمة"]},
    "oga-hits-punches": {"category": "impact", "source": "https://opengameart.org/content/37-hitspunches",
                 "tags": ["impact", "hit", "punch", "fight"], "use_cases": ["melee hit", "fighting game"],
                 "mood": ["heavy", "punchy"], "ar": ["ضربة", "لكمة", "قتال"]},
    "oga-levelup-powerup": {"category": "digital", "source": "https://opengameart.org/content/level-up-power-up-coin-get-13-sounds",
                 "tags": ["levelup", "powerup", "coin", "pickup"], "use_cases": ["level complete", "coin collect", "powerup"],
                 "mood": ["uplifting", "playful"], "ar": ["فوز", "عملة", "ترقية"]},
    "oga-zombies": {"category": "horror", "source": "https://opengameart.org/content/zombies-sound-pack",
                 "tags": ["zombie", "monster", "growl", "horror"], "use_cases": ["horror game", "enemy vocals"],
                 "mood": ["dark", "scary"], "ar": ["زومبي", "رعب", "وحش"]},
    "oga-footsteps": {"category": "impact", "source": "https://opengameart.org/content/different-steps-on-wood-stone-leaves-gravel-and-mud",
                 "tags": ["footstep", "walk", "foley"], "use_cases": ["walking", "terrain feedback"],
                 "mood": ["organic", "neutral"], "ar": ["خطوات", "مشي"]},
    "oga-battle": {"category": "impact", "source": "https://opengameart.org/content/battle-sound-effects",
                 "tags": ["battle", "weapon", "combat"], "use_cases": ["combat", "action game"],
                 "mood": ["intense", "punchy"], "ar": ["معركة", "سلاح"]},
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
        # pair by RELATIVE PATH (not bare stem): packs like voiceover-pack
        # ship Male/1.ogg + Female/1.ogg which would collide on stem alone.
        # Keys are relative paths so WAV/OGG/MP3 variants pair only when names match.
        oggs = {p.relative_to(pdir).as_posix().lower(): p for p in pdir.rglob("*.ogg")}
        mp3s = {p.relative_to(pdir).as_posix().lower(): p for p in pdir.rglob("*.mp3")}
        wavs = {p.relative_to(pdir).as_posix().lower(): p for p in pdir.rglob("*.wav")}
        flacs = {}
        for p in pdir.rglob("*.flac"):
            flacs[p.relative_to(pdir).as_posix().lower()] = p
        norm = lambda k: re.sub(r"\.(ogg|mp3|wav|flac)$", "", k)
        keys = sorted(set(norm(k) for k in list(oggs) + list(mp3s) + list(wavs) + list(flacs)))
        for key in keys:
            ogg = oggs.get(key + ".ogg")
            mp3 = mp3s.get(key + ".mp3")
            wav = wavs.get(key + ".wav")
            flac = flacs.get(key + ".flac")
            if ogg is None and mp3 is None and wav is None and flac is None:
                continue
            base = ogg or mp3 or wav or flac
            rel_base = base.relative_to(pdir)
            stem = base.stem
            sub = rel_base.parent.as_posix() if rel_base.parent.as_posix() != "." else ""
            words = [w for w in WORD_SPLIT.split(stem.lower()) if w]
            subwords = [w for w in WORD_SPLIT.split(sub.lower().replace("/", " ")) if w]
            tags = sorted(set(meta["tags"] + subwords + words[:6]))
            sid = f"{pack}_{sub}_{stem}".replace(" ", "_").replace("/", "_") if sub else f"{pack}_{stem}".replace(" ", "_")
            sid = sid[:150]
            rel_ogg = (ogg.relative_to(ROOT).as_posix()) if ogg else None
            rel_mp3 = (mp3.relative_to(ROOT).as_posix()) if mp3 else None
            rel_wav = (wav.relative_to(ROOT).as_posix()) if wav else None
            rel_flac = (flac.relative_to(ROOT).as_posix()) if flac else None
            dur = duration(ogg or mp3 or wav or flac)
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
                "formats": [f for f, p in (("ogg", ogg), ("mp3", mp3), ("wav", wav), ("flac", flac)) if p],
                "file_ogg": rel_ogg,
                "file_mp3": rel_mp3,
                "file_wav": rel_wav,
                "file_flac": rel_flac,
                "download_url_ogg": raw_url(rel_ogg) if rel_ogg else None,
                "download_url_mp3": raw_url(rel_mp3) if rel_mp3 else None,
                "download_url_wav": raw_url(rel_wav) if rel_wav else None,
                "download_url_flac": raw_url(rel_flac) if rel_flac else None,
                "size_ogg": ogg.stat().st_size if ogg else None,
                "size_mp3": mp3.stat().st_size if mp3 else None,
                "size_wav": wav.stat().st_size if wav else None,
                "size_flac": flac.stat().st_size if flac else None,
                "sha256_ogg": sha256(ogg) if ogg else None,
                "sha256_mp3": sha256(mp3) if mp3 else None,
                "sha256_wav": sha256(wav) if wav else None,
                "sha256_flac": sha256(flac) if flac else None,
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
