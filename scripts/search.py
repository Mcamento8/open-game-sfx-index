#!/usr/bin/env python3
"""Keyword search over index.json — works offline, no heavy deps.
Supports English + Arabic queries. Usage:
  python scripts/search.py --q "button click" --category ui --limit 5
  python scripts/search.py --q "زر" --limit 5
"""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.json"

TOKEN = re.compile(r"[\w\u0600-\u06FF]+")


def tokenize(s: str):
    return [t.lower() for t in TOKEN.findall(s or "")]


def score(entry, qtokens):
    hay = " ".join([
        entry.get("title", ""),
        entry.get("category", ""),
        entry.get("pack", ""),
        " ".join(entry.get("tags", [])),
        " ".join(entry.get("use_cases", [])),
        " ".join(entry.get("keywords_en", [])),
        " ".join(entry.get("keywords_ar", [])),
    ]).lower()
    s = 0
    for q in qtokens:
        if q in hay:
            s += 3 if q in entry.get("title", "").lower() else 2
            if q in " ".join(entry.get("tags", [])).lower():
                s += 1
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True, help="query, EN or AR")
    ap.add_argument("--category", default=None)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    data = json.loads(INDEX.read_text(encoding="utf-8"))
    qtokens = tokenize(args.q)
    out = []
    for e in data.get("sounds", []):
        if args.category and e.get("category") != args.category:
            continue
        sc = score(e, qtokens)
        if sc > 0:
            out.append((sc, e))
    out.sort(key=lambda x: -x[0])
    for sc, e in out[: args.limit]:
        print(f"[{sc}] {e['id']} | {e['title']} | {e['category']} | {e['duration_sec']}s")
        print(f"    OGG: {e['download_url_ogg']}")
        print(f"    MP3: {e['download_url_mp3']}")
    if not out:
        print("No matches. Try broader terms, e.g. --q click --category ui")


if __name__ == "__main__":
    main()
