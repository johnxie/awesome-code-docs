#!/usr/bin/env python3
"""Validate required section structure for tutorial indexes that opt into format v2."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SectionRule:
    name: str
    exact: tuple[str, ...] = ()
    prefixes: tuple[str, ...] = ()


RULES: tuple[SectionRule, ...] = (
    SectionRule(
        name="why",
        exact=("## Why This Track Matters", "## Why This Tutorial Exists"),
    ),
    SectionRule(
        name="snapshot",
        prefixes=("## Current Snapshot",),
    ),
    SectionRule(
        name="mental_model",
        exact=("## Mental Model", "## Cline Operating Model", "## Roo Code Mental Model"),
    ),
    SectionRule(
        name="chapter_map",
        exact=("## Chapter Guide", "## Learning Path", "## Chapter Map"),
    ),
    SectionRule(
        name="learning_outcomes",
        exact=("## What You Will Learn", "## Skill Outcomes"),
    ),
    SectionRule(
        name="sources",
        exact=("## Source References",),
    ),
)


def parse_frontmatter(md_text: str) -> dict[str, str]:
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip("'\"")
    return frontmatter


def collect_h2_headings(md_text: str) -> list[str]:
    return [line.strip() for line in md_text.splitlines() if line.startswith("## ")]


def has_rule_match(headings: list[str], rule: SectionRule) -> bool:
    for heading in headings:
        if heading in rule.exact:
            return True
        if any(heading.startswith(prefix) for prefix in rule.prefixes):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate format v2 tutorial index structure")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    index_paths = sorted((root / "tutorials").glob("*/index.md"))

    opted_in: list[Path] = []
    failures: list[tuple[Path, list[str]]] = []

    for index_path in index_paths:
        text = index_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter.get("format_version") != "v2":
            continue

        opted_in.append(index_path)
        headings = collect_h2_headings(text)
        missing = [rule.name for rule in RULES if not has_rule_match(headings, rule)]
        if missing:
            failures.append((index_path, missing))

    print(f"v2_index_count={len(opted_in)}")
    if not opted_in:
        print("No tutorial indexes are opted into format_version: v2.")
        return 0

    if failures:
        for path, missing in failures:
            rel = path.relative_to(root)
            print(f"{rel}: missing_sections={','.join(missing)}")
        return 1

    print("All format_version: v2 indexes contain required section categories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
