#!/usr/bin/env python3
"""Generate a machine-readable tutorial inventory manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

NUMBERED_MD_PATTERN = "[0-9][0-9]*.md"


def tutorial_record(root: Path, tutorial_dir: Path) -> dict:
    has_index = (tutorial_dir / "index.md").is_file()
    top_level_files = sorted(tutorial_dir.glob(NUMBERED_MD_PATTERN))
    docs_dir = tutorial_dir / "docs"
    docs_files = sorted(docs_dir.glob(NUMBERED_MD_PATTERN)) if docs_dir.exists() else []

    top_level_count = len(top_level_files)
    docs_count = len(docs_files)
    total_count = top_level_count + docs_count

    if top_level_count > 0 and docs_count == 0:
        structure = "root_only"
    elif top_level_count == 0 and docs_count > 0:
        structure = "docs_only"
    elif top_level_count == 0 and docs_count == 0:
        structure = "index_only"
    else:
        structure = "mixed"

    chapter_numbers = []
    for f in top_level_files + docs_files:
        chapter_numbers.append(f.name[:2])

    return {
        "name": tutorial_dir.name,
        "path": tutorial_dir.relative_to(root).as_posix(),
        "has_index": has_index,
        "structure": structure,
        "top_level_chapter_count": top_level_count,
        "docs_chapter_count": docs_count,
        "total_numbered_chapter_count": total_count,
        "chapter_numbers": sorted(chapter_numbers),
    }


def build_manifest(root: Path) -> dict:
    tutorials_root = root / "tutorials"
    tutorials = [
        tutorial_record(root, t)
        for t in sorted([p for p in tutorials_root.iterdir() if p.is_dir()], key=lambda p: p.name)
    ]

    structure_counts = {
        "root_only": 0,
        "docs_only": 0,
        "index_only": 0,
        "mixed": 0,
    }
    for t in tutorials:
        structure_counts[t["structure"]] += 1

    return {
        "tutorial_count": len(tutorials),
        "structure_counts": structure_counts,
        "tutorials": tutorials,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate tutorial manifest")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--output", default="tutorials/tutorial-manifest.json", help="Manifest output path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_path = (root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(root)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote manifest: {output_path}")
    print(f"tutorial_count={manifest['tutorial_count']}")
    print("structure_counts=" + json.dumps(manifest["structure_counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
