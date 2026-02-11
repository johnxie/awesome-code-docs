#!/usr/bin/env python3
"""Regenerate repository status docs from current tutorial state."""

from __future__ import annotations

import argparse
from pathlib import Path

NUMBERED_MD_PATTERN = "[0-9][0-9]*.md"


def collect_tutorial_dirs(root: Path) -> list[Path]:
    tutorials_root = root / "tutorials"
    return sorted([p for p in tutorials_root.iterdir() if p.is_dir() and (p / "index.md").is_file()])


def chapter_count(tutorial_dir: Path) -> int:
    return len(list(tutorial_dir.glob(NUMBERED_MD_PATTERN)))


def structure_kind(tutorial_dir: Path) -> str:
    top_level = len(list(tutorial_dir.glob(NUMBERED_MD_PATTERN)))
    docs_dir = tutorial_dir / "docs"
    docs_count = len(list(docs_dir.glob(NUMBERED_MD_PATTERN))) if docs_dir.exists() else 0
    if top_level > 0 and docs_count == 0:
        return "root_only"
    if top_level == 0 and docs_count > 0:
        return "docs_only"
    if top_level == 0 and docs_count == 0:
        return "index_only"
    return "mixed"


def generate_tutorial_structure_md(root: Path) -> str:
    dirs = collect_tutorial_dirs(root)
    structure_counts = {"root_only": 0, "docs_only": 0, "index_only": 0, "mixed": 0}
    for d in dirs:
        structure_counts[structure_kind(d)] += 1

    return f"""# Tutorial Structure Standard

This file defines the canonical tutorial layout and current structure status.

## Canonical Layout (Target)

```text
tutorials/<tutorial-name>/
  index.md
  01-*.md
  02-*.md
  ...
  08-*.md
```

## Current Structure Snapshot (auto-generated)

| Pattern | Count |
|:--------|:------|
| `root_only` | {structure_counts['root_only']} |
| `docs_only` | {structure_counts['docs_only']} |
| `index_only` | {structure_counts['index_only']} |
| `mixed` | {structure_counts['mixed']} |

## Policy

1. New tutorials should use the canonical top-level chapter layout.
2. Existing tutorials should avoid introducing new `docs/` chapter structures.
3. Index files must not contain dead local links.
4. Placeholder index summaries are disallowed.
5. Structural and link health are enforced by CI (`Docs Health` workflow).

## Migration Approach

1. Keep tutorial indexes aligned with published chapter reality.
2. Maintain canonical naming for new chapter files (`01-...md` to `08-...md`).
3. Regenerate machine-readable artifacts after structural/content updates:
   - `tutorials/tutorial-manifest.json`
   - discoverability assets (`discoverability/tutorial-index.json`, `llms.txt`, etc.)
4. Re-run docs health checks before merge.
"""


def generate_content_gaps_md(root: Path) -> str:
    dirs = collect_tutorial_dirs(root)

    counts = [chapter_count(d) for d in dirs]
    exactly_8 = sum(1 for c in counts if c == 8)
    more_than_8 = sum(1 for c in counts if c > 8)
    zero = sum(1 for c in counts if c == 0)
    partial = sum(1 for c in counts if 0 < c < 8)

    top_level = sorted(((chapter_count(d), d.name) for d in dirs), reverse=True)[:10]

    top_lines = "\n".join(
        f"- `{name}`: {count} numbered chapter files" for count, name in top_level
    )

    return f"""# Awesome Code Docs: Current Gaps and Roadmap

This document tracks structural and quality gaps that impact completeness and discoverability.

## Current Snapshot (auto-generated)

| Metric | Value |
|:-------|:------|
| Tutorial directories | {len(dirs)} |
| Tutorials with exactly 8 numbered chapters | {exactly_8} |
| Tutorials with >8 numbered chapters | {more_than_8} |
| Tutorials with 0 numbered chapters | {zero} |
| Tutorials with partial chapter coverage (1-7) | {partial} |

## Current Priority Gaps

### 1) Chapter-Count Variance

Most tutorials follow the standard 8-chapter shape, but some tracks intentionally include additional chapters.

Top chapter-count tutorials:
{top_lines}

### 2) Index Format Variance

Tutorial index pages use multiple historical styles. Priority is to keep all indexes:

- accurate
- up to date
- internally linked to related tutorials
- free of placeholder summaries

### 3) Discoverability Surfaces

High-impact surfaces requiring continuous maintenance:

- `README.md`
- `categories/*.md`
- `discoverability/tutorial-index.json`
- `discoverability/tutorial-directory.md`
- `llms.txt` and `llms-full.txt`

## Recommended Execution Order

1. Maintain link + structure + placeholder quality gates in CI.
2. Keep generated status/discoverability docs synchronized through scripts.
3. Prioritize formatting and snapshot refreshes on high-traffic tutorial tracks first.
4. Expand and normalize index formatting style guide usage across all tutorial families.

## Completion Criteria

A tutorial track is considered production-ready when:

- it has `index.md` with valid local links
- it has a coherent numbered chapter sequence
- its summary and snapshot language are not stale or placeholder quality
- it passes repository docs health checks
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Update repo status docs")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--structure-output",
        default="TUTORIAL_STRUCTURE.md",
        help="Output path for tutorial structure document",
    )
    parser.add_argument(
        "--gaps-output",
        default="CONTENT_GAPS_ANALYSIS.md",
        help="Output path for content gaps document",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    structure_path = (root / args.structure_output).resolve()
    gaps_path = (root / args.gaps_output).resolve()

    structure_path.write_text(generate_tutorial_structure_md(root), encoding="utf-8")
    gaps_path.write_text(generate_content_gaps_md(root), encoding="utf-8")

    print(f"Wrote: {structure_path}")
    print(f"Wrote: {gaps_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
