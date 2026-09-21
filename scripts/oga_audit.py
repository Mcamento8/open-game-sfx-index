#!/usr/bin/env python3
"""Audit OGA candidate pages: verify CC0 license + extract direct file URLs."""
import urllib.request
import re
import json
import pathlib

SLUGS = [
    "50-rpg-sound-effects",
    "gui-sound-effects",
    "37-hitspunches",
    "51-ui-sound-effects-buttons-switches-and-clicks",
    "level-up-power-up-coin-get-13-sounds",
    "inventory-sound-effects",
    "63-digital-sound-effects-lasers-phasers-space-etc",
    "fantasy-sound-effects-library",
    "voiceover-pack-40-lines",
    "54-casino-sound-effects-cards-dice-chips",
    "spell-sounds-starter-pack",
    "zombies-sound-pack",
    "different-steps-on-wood-stone-leaves-gravel-and-mud",
    "chaingun-pistol-rifle-shotgun-shots",
    "battle-sound-effects",
    "ui-sound-effects-pack",
]

out = []
for s in SLUGS:
    try:
        req = urllib.request.Request(
            "https://opengameart.org/content/" + s,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")
        is_cc0 = "license_images/cc0" in html
        m_author = re.search(r"/users/[a-z0-9-]+\">([^<]{2,40})</a>", html)
        author = m_author.group(1).strip() if m_author else "?"
        files = re.findall(
            r'href="(https://opengameart\.org/sites/default/files/[^"]+)"', html
        )
        files = [
            f for f in files
            if re.search(r"\.(zip|7z|rar|tar\.gz|wav|ogg|mp3|flac)(\?.*)?$", f, re.I)
            and "styles/" not in f and "license_images" not in f
        ]
        # dedupe preserving order
        seen = set()
        uniq = []
        for f in files:
            if f not in seen:
                seen.add(f)
                uniq.append(f)
        size_m = re.search(r"([\d.]+ ?Mb)", html)
        out.append({
            "slug": s,
            "cc0": is_cc0,
            "author": author,
            "size": size_m.group(1) if size_m else "?",
            "files": uniq[:4],
        })
        print(s + " | CC0=" + str(is_cc0) + " | by " + author + " | " + str(len(uniq)) + " files | " + (size_m.group(1) if size_m else "?"))
    except Exception as e:
        print(s + " ERROR " + str(e)[:120])
        out.append({"slug": s, "cc0": False, "error": str(e)[:120]})

pathlib.Path("_tmp").mkdir(exist_ok=True)
with open("_tmp/oga_audit.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("saved _tmp/oga_audit.json")
