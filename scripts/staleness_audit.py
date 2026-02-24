#!/usr/bin/env python3
"""Audit freshness markers and dated claims in high-impact docs surfaces."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

MONTH_PATTERN = "January|February|March|April|May|June|July|August|September|October|November|December"
LONG_DATE_RE = re.compile(rf"\b({MONTH_PATTERN})\s+([0-9]{{1,2}}),\s+([0-9]{{4}})\b")
ISO_DATE_RE = re.compile(r"\b(20[0-9]{2})-([0-9]{2})-([0-9]{2})\b")

FRESHNESS_HINTS = (
    "verified",
    "last updated",
    "last verified",
    "snapshot",
    "auto-updated",
    "generated_on",
    "generated on",
)

DEFAULT_TARGET_GLOBS = (
    "README.md",
    "tutorials/README.md",
    "tutorials/*/index.md",
    "categories/*.md",
    "discoverability/*.md",
    "CONTENT_GAPS_ANALYSIS.md",
    "TUTORIAL_STRUCTURE.md",
    "IMPORT_ROADMAP_TODO.md",
)


@dataclass(frozen=True)
class Finding:
    file: str
    line_number: int
    line: str
    parsed_date: str
    age_days: int

    def as_json(self) -> dict[str, object]:
        return {
            "file": self.file,
            "line_number": self.line_number,
            "line": self.line,
            "parsed_date": self.parsed_date,
            "age_days": self.age_days,
        }


def candidate_files(root: Path, globs: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    seen: set[Path] = set()
    for pattern in globs:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            if path in seen:
                continue
            seen.add(path)
            out.append(path)
    return out


def parse_long_date(match: re.Match[str]) -> date | None:
    month, day, year = match.group(1), match.group(2), match.group(3)
    try:
        dt = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
    except ValueError:
        return None
    return dt.date()


def parse_iso_date(match: re.Match[str]) -> date | None:
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def should_check_line(line: str) -> bool:
    lower = line.lower()
    return any(hint in lower for hint in FRESHNESS_HINTS)


def collect_findings(root: Path, max_age_days: int, globs: Iterable[str]) -> list[Finding]:
    today = date.today()
    findings: list[Finding] = []

    for path in candidate_files(root, globs):
        rel = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

        for idx, line in enumerate(lines, start=1):
            if not should_check_line(line):
                continue

            for match in LONG_DATE_RE.finditer(line):
                parsed = parse_long_date(match)
                if not parsed:
                    continue
                age_days = (today - parsed).days
                if age_days > max_age_days:
                    findings.append(
                        Finding(
                            file=rel,
                            line_number=idx,
                            line=line.strip(),
                            parsed_date=parsed.isoformat(),
                            age_days=age_days,
                        )
                    )

            for match in ISO_DATE_RE.finditer(line):
                parsed = parse_iso_date(match)
                if not parsed:
                    continue
                age_days = (today - parsed).days
                if age_days > max_age_days:
                    findings.append(
                        Finding(
                            file=rel,
                            line_number=idx,
                            line=line.strip(),
                            parsed_date=parsed.isoformat(),
                            age_days=age_days,
                        )
                    )

    findings.sort(key=lambda f: (f.file, f.line_number, f.parsed_date))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit stale freshness markers in docs")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--max-age-days", type=int, default=10, help="Maximum allowed age for freshness markers")
    parser.add_argument("--json-output", help="Write JSON report to this path")
    parser.add_argument("--fail-on-stale", action="store_true", help="Exit non-zero if stale findings exist")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=list(DEFAULT_TARGET_GLOBS),
        help="Glob patterns (relative to repo root) to scan",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = collect_findings(root, max_age_days=args.max_age_days, globs=args.targets)

    print(f"stale_marker_count={len(findings)}")
    if findings:
        print("stale_markers:")
        for finding in findings:
            print(
                f"{finding.file}:{finding.line_number} age={finding.age_days}d "
                f"date={finding.parsed_date} :: {finding.line}"
            )

    if args.json_output:
        output = Path(args.json_output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "stale_marker_count": len(findings),
            "max_age_days": args.max_age_days,
            "targets": args.targets,
            "findings": [f.as_json() for f in findings],
        }
        output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.fail_on_stale and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
