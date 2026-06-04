#!/usr/bin/env python3
"""Verify the daily Free Range Builders note pair exists and has basic shape."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


REQUIRED_SECTIONS = (
    "## Executive summary",
    "## Layered architecture dissection",
    "## Key",
    "## Practical questions and answers",
    "## What is smart",
    "## What is flawed or weak",
    "## What we can learn / steal",
    "## Bottom line",
)


def default_date() -> str:
    return datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")


def check_note(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    if len(text) < 2500:
        errors.append(f"{path}: too short for a builder teardown ({len(text)} chars)")
    if not text.startswith("# "):
        errors.append(f"{path}: missing top-level title")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path}: missing section containing {section!r}")
    if "](https://" not in text:
        errors.append(f"{path}: expected concrete source links")
    if "- Date:" not in text:
        errors.append(f"{path}: missing Date metadata")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=default_date(), help="YYYY-MM-DD; defaults to America/Los_Angeles today")
    parser.add_argument("--notes-dir", default="notes")
    args = parser.parse_args()

    notes_dir = Path(args.notes_dir)
    if not notes_dir.is_dir():
        print(f"missing notes directory: {notes_dir}", file=sys.stderr)
        return 1

    prefix = f"{args.date}_"
    github_notes = sorted(
        p for p in notes_dir.glob(f"{prefix}*.md")
        if not p.name.startswith(f"{args.date}_hf_")
    )
    hf_notes = sorted(notes_dir.glob(f"{args.date}_hf_*.md"))

    errors: list[str] = []
    if not github_notes:
        errors.append(f"missing GitHub scout note for {args.date}: notes/{args.date}_<repo-slug>.md")
    if not hf_notes:
        errors.append(f"missing Hugging Face scout note for {args.date}: notes/{args.date}_hf_<artifact-slug>.md")

    for path in github_notes + hf_notes:
        errors.extend(check_note(path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"ok: {args.date}: {len(github_notes)} GitHub note(s), {len(hf_notes)} Hugging Face note(s)")
    for path in github_notes + hf_notes:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
