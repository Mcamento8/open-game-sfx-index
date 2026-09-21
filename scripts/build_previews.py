#!/usr/bin/env python3
"""Generate per-pack listening pages (previews/<pack>.md) with HTML5 <audio>
players that render directly on github.com, plus previews/README.md index.
Re-run after any batch:  python scripts/build_previews.py
"""
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.json"
OUT = ROOT / "previews"

PACK_TITLES = {
    "ui-audio": ("UI Audio", "🔘", "Buttons, toggles and tabs — the most-used sounds in any game."),
    "interface-sounds": ("Interface Sounds", "🖱️", "Clicks, hovers, confirmations, errors and notifications."),
    "impact-sounds": ("Impact Sounds", "💥", "Hits, crashes, slams and footstep impacts."),
    "sci-fi-sounds": ("Sci-Fi Sounds", "🚀", "Lasers, engines, force fields and space ambience."),
    "digital-audio": ("Digital Audio", "👾", "Retro bleeps, pickups and arcade power-ups."),
    "rpg-audio": ("RPG Audio", "⚔️", "Footsteps, blades, books, coins and fantasy foley."),
    "casino-audio": ("Casino Audio", "🎰", "Cards, dice, chips and tabletop handling."),
    "music-jingles": ("Music Jingles", "🎵", "Win/lose stingers and short musical motifs."),
    "voiceover-pack": ("Voiceover Pack", "🎙️", "Male & female announcements, battles and objectives."),
    "voiceover-pack-fighter": ("Voiceover Pack (Fighter)", "🥊", "Fighter announcer: rounds, fights and victories."),
}


def main():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    by_pack = defaultdict(list)
    for s in data["sounds"]:
        by_pack[s["pack"]].append(s)
    OUT.mkdir(exist_ok=True)

    for pack in sorted(by_pack):
        sounds = sorted(by_pack[pack], key=lambda s: s["id"])
        title, emoji, desc = PACK_TITLES.get(pack, (pack, "🔊", ""))
        lines = [
            f"# {emoji} {title}",
            "",
            f"> {desc}",
            "",
            f"**{len(sounds)} sounds** · OGG · CC0 public domain · "
            f"[⬅ Back to all previews](README.md) · "
            f"[🤖 Machine index](../index.json)",
            "",
            "| # | Sound | Duration | Tags | ▶ Listen |",
            "|---|-------|----------|------|----------|",
        ]
        for i, s in enumerate(sounds, 1):
            url = s["download_url_ogg"] or s["download_url_mp3"] or ""
            dur = f'{s["duration_sec"]}s' if s.get("duration_sec") else "—"
            tags = ", ".join(s["tags"][:5])
            name = s["title"]
            player = f'<audio controls preload="none" src="{url}"></audio>' if url else "—"
            lines.append(f"| {i} | **{name}**<br>`{s['id']}` | {dur} | {tags} | {player} |")
        lines += [
            "",
            f"_Source: Kenney · Upstream: https://kenney.nl/assets/{pack} · License: CC0-1.0_",
        ]
        (OUT / f"{pack}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    idx = [
        "# 🎧 Listen — click a pack, press play",
        "",
        "Every sound below plays **right here on GitHub** — no download needed. "
        "Pick what you like, then copy its download link (or let your AI agent fetch it from `index.json`).",
        "",
        "| Pack | Sounds | Preview page |",
        "|------|--------|--------------|",
    ]
    for pack in sorted(by_pack):
        title, emoji, desc = PACK_TITLES.get(pack, (pack, "🔊", ""))
        idx.append(f"| {emoji} **{title}**<br>{desc} | {len(by_pack[pack])} | [▶ Listen →]({pack}.md) |")
    idx += ["", f"_Total: **{data['count']} sounds** · 10 packs · CC0 public domain._"]
    (OUT / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"previews rebuilt: {len(by_pack)} pages, {data['count']} players")


if __name__ == "__main__":
    main()
