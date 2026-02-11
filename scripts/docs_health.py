#!/usr/bin/env python3
"""Validate markdown link health and tutorial structure consistency."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
NUMBERED_MD_PATTERN = "[0-9][0-9]*.md"


@dataclass(frozen=True)
class BrokenLink:
    source: str
    target: str

    def as_tsv(self) -> str:
        return f"{self.source}\t{self.target}"


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        yield path


def iter_links(path: Path) -> Iterable[str]:
    in_fence = False
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for link in LINK_PATTERN.findall(line):
            yield link.strip()


def normalize_local_link(raw_link: str) -> str | None:
    if not raw_link:
        return None
    if raw_link.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
        return None

    clean = raw_link.split("#", 1)[0].split("?", 1)[0].strip()
    if not clean:
        return None

    if clean.startswith("<") and clean.endswith(">"):
        clean = clean[1:-1].strip()

    if not clean:
        return None

    if clean.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
        return None

    return clean


def link_exists(root: Path, source_file: Path, target: str) -> bool:
    if target.startswith("/"):
        candidate = root / target.lstrip("/")
    else:
        candidate = source_file.parent / target

    if target.endswith("/"):
        return candidate.exists() and candidate.is_dir()
    return candidate.exists() and candidate.is_file()


def collect_broken_links(root: Path) -> list[BrokenLink]:
    broken: set[BrokenLink] = set()
    for md_file in iter_markdown_files(root):
        rel_source = md_file.relative_to(root).as_posix()
        for raw_link in iter_links(md_file):
            local_target = normalize_local_link(raw_link)
            if not local_target:
                continue
            if not link_exists(root, md_file, local_target):
                broken.add(BrokenLink(source=rel_source, target=local_target))
    return sorted(broken, key=lambda x: (x.source, x.target))


def read_baseline(path: Path) -> set[BrokenLink]:
    entries: set[BrokenLink] = set()
    if not path.exists():
        return entries

    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        entries.add(BrokenLink(source=parts[0], target=parts[1]))
    return entries


def write_baseline(path: Path, broken_links: list[BrokenLink]) -> None:
    lines = [
        "# Baseline of known broken local markdown links.",
        "# Format: <source-file>\\t<link-target>",
    ]
    lines.extend(link.as_tsv() for link in broken_links)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def classify_tutorial_structure(root: Path) -> dict:
    tutorials_dir = root / "tutorials"
    structure_counts = {
        "root_only": 0,
        "docs_only": 0,
        "index_only": 0,
        "mixed": 0,
    }
    missing_index: list[str] = []

    for tutorial_dir in sorted([p for p in tutorials_dir.iterdir() if p.is_dir()]):
        has_index = (tutorial_dir / "index.md").is_file()
        top_level_count = len(list(tutorial_dir.glob(NUMBERED_MD_PATTERN)))
        docs_count = 0
        docs_dir = tutorial_dir / "docs"
        if docs_dir.exists() and docs_dir.is_dir():
            docs_count = len(list(docs_dir.glob(NUMBERED_MD_PATTERN)))

        if top_level_count > 0 and docs_count == 0:
            structure = "root_only"
        elif top_level_count == 0 and docs_count > 0:
            structure = "docs_only"
        elif top_level_count == 0 and docs_count == 0:
            structure = "index_only"
        else:
            structure = "mixed"

        structure_counts[structure] += 1

        if not has_index:
            missing_index.append(tutorial_dir.relative_to(root).as_posix())

    return {
        "tutorial_count": sum(structure_counts.values()),
        "structure_counts": structure_counts,
        "missing_index": missing_index,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown docs health checker")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--baseline-file", help="Path to known broken-link baseline file")
    parser.add_argument("--write-baseline", action="store_true", help="Write current broken links to baseline file")
    parser.add_argument("--json-output", help="Write machine-readable report JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    broken_links = collect_broken_links(root)
    structure_report = classify_tutorial_structure(root)

    baseline_path = Path(args.baseline_file).resolve() if args.baseline_file else None
    baseline_links: set[BrokenLink] = set()
    if baseline_path:
        baseline_links = read_baseline(baseline_path)

    current_links = set(broken_links)
    new_broken = sorted(current_links - baseline_links, key=lambda x: (x.source, x.target))
    resolved = sorted(baseline_links - current_links, key=lambda x: (x.source, x.target))

    report = {
        "broken_link_count": len(broken_links),
        "new_broken_link_count": len(new_broken),
        "resolved_link_count": len(resolved),
        "missing_index_count": len(structure_report["missing_index"]),
        "structure": structure_report,
        "new_broken_links": [x.as_tsv() for x in new_broken],
        "resolved_links": [x.as_tsv() for x in resolved],
    }

    print(f"broken_link_count={len(broken_links)}")
    print(f"new_broken_link_count={len(new_broken)}")
    print(f"resolved_link_count={len(resolved)}")
    print(f"missing_index_count={len(structure_report['missing_index'])}")
    print("structure_counts=" + json.dumps(structure_report["structure_counts"], sort_keys=True))

    if new_broken:
        print("\nNew broken links detected:")
        for link in new_broken:
            print(link.as_tsv())

    if structure_report["missing_index"]:
        print("\nTutorial directories missing index.md:")
        for item in structure_report["missing_index"]:
            print(item)

    if args.json_output:
        output_path = Path(args.json_output).resolve()
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.write_baseline:
        if not baseline_path:
            raise SystemExit("--write-baseline requires --baseline-file")
        write_baseline(baseline_path, broken_links)
        print(f"Wrote baseline to {baseline_path}")

    if structure_report["missing_index"]:
        return 1

    if baseline_path:
        return 1 if new_broken else 0

    return 1 if broken_links else 0


if __name__ == "__main__":
    raise SystemExit(main())
