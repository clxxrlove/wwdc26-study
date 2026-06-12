#!/usr/bin/env python3
"""
Create a blank session note from docs/note-template.md.

Usage:
  python scripts/make_session_note.py "What’s new in Xcode 27" "https://developer.apple.com/videos/play/wwdc2026/258/"
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "docs" / "note-template.md"
OUT_DIR = ROOT / "sessions" / "notes"


def slugify(title: str) -> str:
    slug = title.lower()
    slug = slug.replace("’", "").replace("'", "")
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "session"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: make_session_note.py <title> [url]", file=sys.stderr)
        return 2

    title = sys.argv[1]
    url = sys.argv[2] if len(sys.argv) >= 3 else ""

    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("{session_title}", title)
    text = text.replace("- URL:", f"- URL: {url}")
    text = text.replace("- Last updated:", f"- Last updated: {date.today().isoformat()}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{slugify(title)}.md"
    if out.exists():
        print(f"Already exists: {out}")
        return 1

    out.write_text(text, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
