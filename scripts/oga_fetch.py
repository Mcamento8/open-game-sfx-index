#!/usr/bin/env python3
"""Download verified CC0 OGA packs (one at a time), extract audio, keep
original formats (wav/ogg/mp3), preserve subfolders, delete archives after.
Usage: python scripts/oga_fetch.py
"""
import urllib.request
import urllib.parse
import zipfile
import pathlib
import shutil
import re

PACKS = [
    # NOTE: OGA pages authored by Kenney (RPGsounds_Kenney.zip, UI_SFX_Set,
    # Digital_SFX_Set, Voiceover Pack, kenney_casino-audio) are re-uploads of
    # packs already mirrored from kenney.nl — deliberately skipped (dupes).
    ("oga-512-retro",
     "https://opengameart.org/sites/default/files/The%20Essential%20Retro%20Video%20Game%20Sound%20Effects%20Collection%20%5B512%20sounds%5D.zip"),
    ("oga-rpg-pack",
     "https://opengameart.org/sites/default/files/rpg_sound_pack.zip"),
    ("oga-gui-lokif",
     "https://opengameart.org/sites/default/files/GUI_Sound_Effects_by_Lokif.7z"),
    ("oga-hits-punches",
     "https://opengameart.org/sites/default/files/independent_nu_ljudbank-hits_and_punches.7z"),
    ("oga-levelup-powerup",
     "https://opengameart.org/sites/default/files/SoundPack01.zip"),
    ("oga-zombies",
     "https://opengameart.org/sites/default/files/zombies.zip"),
    ("oga-footsteps",
     "https://opengameart.org/sites/default/files/%5Bkdd%5DDifferentSteps_0.zip"),
    ("oga-battle",
     "https://opengameart.org/sites/default/files/battle_sound_effects_0.zip"),
]

AUDIO_EXTS = (".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff")
CONVERT_TO_WAV = (".aif", ".aiff")
SKIP_NAMES = ("preview", "readme", "license", "license.txt")


def save_audio(src: pathlib.Path, target: pathlib.Path):
    """Copy audio; losslessly convert AIFF -> WAV (both PCM) for compatibility."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in CONVERT_TO_WAV:
        import soundfile as sf
        data, rate = sf.read(str(src))
        target = target.with_suffix(".wav")
        if target.exists():
            target = target.parent / (target.stem + "_aiff.wav")
        sf.write(str(target), data, rate, subtype="PCM_16")
    else:
        if target.exists():
            target = target.parent / (target.stem + "_" + src.suffix.lstrip(".") + target.suffix)
        shutil.copy2(src, target)


def extract_archive(archive: pathlib.Path, tmp: pathlib.Path):
    if archive.suffix.lower() == ".zip":
        with zipfile.ZipFile(archive) as z:
            z.extractall(tmp)
    elif archive.suffix.lower() == ".7z":
        try:
            import py7zr
        except ImportError:
            raise SystemExit("py7zr missing: pip install py7zr")
        with py7zr.SevenZipFile(archive, "r") as z:
            z.extractall(tmp)
    else:
        raise SystemExit("unknown archive: " + str(archive))


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    tmp_root = root / "_tmp" / "oga"
    for pack, url in PACKS:
        dest = root / "audio" / pack
        if dest.exists() and any(dest.rglob("*")):
            print(pack + ": already present, skipping")
            continue
        raw_name = urllib.parse.unquote(url.rsplit("/", 1)[-1])
        ext = pathlib.Path(raw_name).suffix.lower() or ".zip"
        fname = re.sub(r"[^A-Za-z0-9._-]", "_", raw_name)
        archive = tmp_root / (fname[:60] + ext if not fname.lower().endswith(ext) else fname[:80])
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists():
            print("downloading " + pack + " ...")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(archive, "wb") as f:
                shutil.copyfileobj(r, f)
            print("  MB: " + str(round(archive.stat().st_size / 1048576, 2)))
        tmp = tmp_root / ("ex_" + pack)
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        extract_archive(archive, tmp)
        n = 0
        for src in sorted(tmp.rglob("*")):
            if not src.is_file():
                continue
            if "__MACOSX" in src.parts or src.name.startswith("._"):
                continue
            if src.suffix.lower() not in AUDIO_EXTS:
                continue
            low = src.name.lower()
            if low.startswith(SKIP_NAMES) and "preview" in low:
                continue
            rel = src.relative_to(tmp)
            # flatten single top-level wrapper folder, keep deeper structure
            parts = rel.parts
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                # collision: prefix with parent folder name
                target = target.parent / (rel.parent.name + "_" + src.name)
            save_audio(src, target)
            n += 1
        print(pack + " kept audio files: " + str(n))
        archive.unlink(missing_ok=True)
        shutil.rmtree(tmp, ignore_errors=True)
    print("OGA fetch done")


if __name__ == "__main__":
    main()
