#!/usr/bin/env python3
"""Audit itch.io CC0 sound packs: price (free vs paid/PWYW) + direct download links.
No login used. Usage: python scripts/itch_audit.py
"""
import urllib.request
import re
import json
import pathlib

URLS = [
    "https://aarparproj.itch.io/sci-fi-nes-sfx",
    "https://brainzplayz.itch.io/retro-sounds-32-bit",
    "https://brainzplayz.itch.io/retro-sounds-8-bit",
    "https://cicifyre.itch.io/free-catgirl-fighting-voice-pack",
    "https://cicifyre.itch.io/rpg-voice-starter-pack",
    "https://cluckfox.itch.io/disappointing-bells",
    "https://cluckfox.itch.io/rain-and-thunder",
    "https://halfwitsfailedcrits.itch.io/sfx-pack-rolling-dice",
    "https://harvey656.itch.io/freesfxforanything",
    "https://ivoryred.itch.io/8-bit-sfx",
    "https://jacob-creates.itch.io/game-sound-effects",
    "https://johncarroll.itch.io/mage-voice-pack",
    "https://johncarroll.itch.io/orc-voice-pack",
    "https://johncarroll.itch.io/warrior-voice-pack",
    "https://kaijinsoft.itch.io/noise-channel-free-sfx-pack",
    "https://kanekizlf.itch.io/jump-sounds",
    "https://kronbits.itch.io/freesfx",
    "https://kurz.itch.io/100-free-retro-sound-effects",
    "https://liminal-space-dev.itch.io/free-horror-sfx-sounds",
    "https://loveyourdemons.itch.io/slr-sfx",
    "https://ne-mene.itch.io/general-sound-pack",
    "https://nihil-existentia.itch.io/free-audio-asset-collection",
    "https://niiiemand.itch.io/niiiemands-explosion-sfx",
    "https://obsydianx.itch.io/interface-sfx-pack-1",
    "https://petars.itch.io/tower-of-the-kobito-audio-assets",
    "https://phlegmlee.itch.io/horror-sound-pack",
    "https://polar-34.itch.io/magic-sound-effects",
    "https://polar-34.itch.io/sound-effects",
    "https://stormyman.itch.io/goofy-sounds-for-scary-monsters",
    "https://vladislavzh.itch.io/glitch-noises",
]

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")


out = []
for u in URLS:
    try:
        html = get(u)
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        title = re.sub(r"\s+", " ", title.group(1)).strip()[:80] if title else "?"
        paid = bool(re.search(r"purchase|pay what you want|\$\d", html, re.I))
        price_m = re.search(r"(Free|\$[\d.]+)", html)
        uploads = re.findall(r"/download/(\d+)", html)
        uploads = list(dict.fromkeys(uploads))
        fnames = re.findall(r"upload[^>]{0,200}?name[^>]*?>([^<]{1,80})<", html)
        out.append({"url": u, "title": title, "paid_hint": paid,
                    "uploads": uploads, "file_hints": fnames[:6]})
        print(u.split("//")[1].split("/")[0], "|", title[:50], "| paid_hint=",
              paid, "| uploads=", uploads)
    except Exception as e:
        print(u, "ERROR", str(e)[:100])
        out.append({"url": u, "error": str(e)[:100]})

pathlib.Path("_tmp").mkdir(exist_ok=True)
with open("_tmp/itch_audit.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("saved")
