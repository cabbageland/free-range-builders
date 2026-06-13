#!/usr/bin/env python3
"""Non-failing daily state check for the Free Range Builders cron.

The real verifier intentionally exits non-zero when today's notes are missing.
That is useful for CI/final validation, but it is a bad first command in an
agent cron because missing notes are the normal "go do the task" state.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from verify_daily import check_note, default_date


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=default_date(), help="YYYY-MM-DD; defaults to America/Los_Angeles today")
    parser.add_argument("--notes-dir", default="notes")
    args = parser.parse_args()

    notes_dir = Path(args.notes_dir)
    prefix = f"{args.date}_"

    github_notes = sorted(
        p for p in notes_dir.glob(f"{prefix}*.md")
        if not p.name.startswith(f"{args.date}_hf_")
    ) if notes_dir.is_dir() else []
    hf_notes = sorted(notes_dir.glob(f"{args.date}_hf_*.md")) if notes_dir.is_dir() else []

    errors: list[str] = []
    missing: list[str] = []

    if not notes_dir.is_dir():
        errors.append(f"missing notes directory: {notes_dir}")
    if not github_notes:
        missing.append(f"notes/{args.date}_<github-repo-slug>.md")
    if not hf_notes:
        missing.append(f"notes/{args.date}_hf_<hugging-face-slug>.md")

    for path in github_notes + hf_notes:
        errors.extend(check_note(path))

    if errors:
        status = "invalid"
    elif missing:
        status = "missing"
    else:
        status = "complete"

    print(f"date={args.date}")
    print(f"status={status}")
    print(f"github_notes={len(github_notes)}")
    for path in github_notes:
        print(f"github_note={path}")
    print(f"hugging_face_notes={len(hf_notes)}")
    for path in hf_notes:
        print(f"hugging_face_note={path}")
    for path in missing:
        print(f"missing={path}")
    for error in errors:
        print(f"error={error}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
