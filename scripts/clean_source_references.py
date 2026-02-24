#!/usr/bin/env python3
"""Clean low-signal links from tutorial index source reference sections."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SECTION_PATTERN = re.compile(r"(^## Source References\n\n)(.*?)(?=^## |\Z)", re.S | re.M)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IGNORED_URL_PARTS = (
    "github.com/The-Pocket/Tutorial-Codebase-Knowledge",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def extract_fallback_links(full_text: str, limit: int = 6) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, url in LINK_RE.findall(full_text):
        if any(part in url for part in IGNORED_URL_PARTS):
            continue
        if "github.com" not in url and "docs." not in url and "help." not in url:
            continue
        if url in seen:
            continue
        seen.add(url)
        out.append((label.strip(), url.strip()))
        if len(out) >= limit:
            break
    return out


def clean_source_section(text: str) -> tuple[str, bool]:
    match = SECTION_PATTERN.search(text)
    if not match:
        return text, False

    prefix = match.group(1)
    body = match.group(2)
    lines = body.splitlines()
    cleaned_lines: list[str] = []
    changed = False

    for line in lines:
        low = line.lower()
        if any(part.lower() in low for part in IGNORED_URL_PARTS):
            changed = True
            continue
        cleaned_lines.append(line)

    bullets = [ln for ln in cleaned_lines if ln.strip().startswith("- [")]
    if not bullets:
        fallback = extract_fallback_links(text, limit=6)
        if fallback:
            cleaned_lines = [f"- [{label}]({url})" for label, url in fallback]
            changed = True

    new_body = "\n".join(cleaned_lines).strip()
    new_text = text[: match.start()] + prefix + new_body + "\n\n" + text[match.end() :]
    return new_text, changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean tutorial index source references")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    tutorials = root / "tutorials"

    changed_files = 0
    for tutorial_dir in sorted(p for p in tutorials.iterdir() if p.is_dir()):
        idx = tutorial_dir / "index.md"
        if not idx.is_file():
            continue
        text = read(idx)
        new_text, changed = clean_source_section(text)
        if changed:
            write(idx, new_text)
            changed_files += 1

    print(f"changed_index_files={changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
