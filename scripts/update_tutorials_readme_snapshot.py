#!/usr/bin/env python3
"""Update tutorials/README.md snapshot and structure metrics."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NUMBERED_MD_PATTERN = "[0-9][0-9]*.md"


def compute_metrics(root: Path) -> dict:
    tutorials_root = root / "tutorials"
    tutorial_dirs = sorted([p for p in tutorials_root.iterdir() if p.is_dir() and (p / "index.md").is_file()])

    md_files = [f for d in tutorial_dirs for f in d.glob("*.md")]
    md_lines = 0
    for f in md_files:
        with f.open("r", encoding="utf-8", errors="ignore") as handle:
            md_lines += sum(1 for _ in handle)

    structure_counts = {
        "root_only": 0,
        "docs_only": 0,
        "index_only": 0,
        "mixed": 0,
    }

    for d in tutorial_dirs:
        top_level_count = len(list(d.glob(NUMBERED_MD_PATTERN)))
        docs_dir = d / "docs"
        docs_count = len(list(docs_dir.glob(NUMBERED_MD_PATTERN))) if docs_dir.exists() else 0

        if top_level_count > 0 and docs_count == 0:
            structure = "root_only"
        elif top_level_count == 0 and docs_count > 0:
            structure = "docs_only"
        elif top_level_count == 0 and docs_count == 0:
            structure = "index_only"
        else:
            structure = "mixed"

        structure_counts[structure] += 1

    return {
        "tutorial_directories": len(tutorial_dirs),
        "tutorial_markdown_files": len(md_files),
        "tutorial_markdown_lines": md_lines,
        "structure_counts": structure_counts,
    }


def update_readme_content(content: str, metrics: dict) -> str:
    content = re.sub(
        r"## Snapshot \([^\n]+\)",
        "## Snapshot (auto-generated)",
        content,
    )

    replacements = {
        r"\| Tutorial directories \| .* \|": f"| Tutorial directories | {metrics['tutorial_directories']} |",
        r"\| Tutorial markdown files \| .* \|": f"| Tutorial markdown files | {metrics['tutorial_markdown_files']} |",
        r"\| Tutorial markdown lines \| .* \|": f"| Tutorial markdown lines | {metrics['tutorial_markdown_lines']:,} |",
        r"\| Root chapter files \| .* \|": f"| Root chapter files | {metrics['structure_counts']['root_only']} | `index.md` + top-level `01-...md` to `08-...md` |",
        r"\| `docs/` chapter files \| .* \|": f"| `docs/` chapter files | {metrics['structure_counts']['docs_only']} | Deprecated and fully migrated |",
        r"\| Index-only roadmap \| .* \|": f"| Index-only roadmap | {metrics['structure_counts']['index_only']} | All catalog entries publish full chapter sets |",
        r"\| Mixed root \+ `docs/` \| .* \|": f"| Mixed root + `docs/` | {metrics['structure_counts']['mixed']} | Legacy hybrid layout removed |",
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    source_report = metrics.get("source_verification_summary")
    if source_report:
        source_replacements = {
            r"\| Tutorials scanned \| .* \|": f"| Tutorials scanned | {source_report['tutorial_count']} |",
            r"\| Tutorials with source repos \| .* \|": f"| Tutorials with source repos | {source_report['tutorials_with_source_repos']} |",
            r"\| Tutorials with unverified source repos \| .* \|": f"| Tutorials with unverified source repos | {source_report['tutorials_with_unverified_source_repos']} |",
            r"\| Unique verified source repos \| .* \|": f"| Unique verified source repos | {source_report['unique_verified_repo_count']} |",
        }
        for pattern, replacement in source_replacements.items():
            content = re.sub(pattern, replacement, content)

    return content


def maybe_load_source_verification(root: Path) -> dict | None:
    report_path = root / "discoverability" / "tutorial-source-verification.json"
    if not report_path.is_file():
        return None

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        summary = report.get("summary", {})
        required = (
            "tutorial_count",
            "tutorials_with_source_repos",
            "tutorials_with_unverified_source_repos",
            "unique_verified_repo_count",
        )
        if not all(key in summary for key in required):
            return None
        return summary
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Update tutorials/README snapshot metrics")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--output",
        default="",
        help="Write updated content to this path instead of tutorials/README.md",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    readme_path = root / "tutorials" / "README.md"

    original = readme_path.read_text(encoding="utf-8")
    metrics = compute_metrics(root)
    metrics["source_verification_summary"] = maybe_load_source_verification(root)
    updated = update_readme_content(original, metrics)

    output_path = Path(args.output).resolve() if args.output else readme_path
    output_path.write_text(updated, encoding="utf-8")

    print(f"Wrote: {output_path}")
    print(f"tutorial_directories={metrics['tutorial_directories']}")
    print(f"tutorial_markdown_files={metrics['tutorial_markdown_files']}")
    print(f"tutorial_markdown_lines={metrics['tutorial_markdown_lines']}")
    print(f"structure_counts={metrics['structure_counts']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
