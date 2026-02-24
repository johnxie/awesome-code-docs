#!/usr/bin/env python3
"""Audit dated release/activity claims in tutorial index files."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

MONTH_PATTERN = "January|February|March|April|May|June|July|August|September|October|November|December"
LONG_DATE_RE = re.compile(rf"\b({MONTH_PATTERN})\s+([0-9]{{1,2}}),\s+([0-9]{{4}})\b")
ISO_DATE_RE = re.compile(r"\b(20[0-9]{2})-([0-9]{2})-([0-9]{2})\b")

CLAIM_HINTS = (
    "latest release",
    "recent activity",
    "latest visible tag",
    "recent push activity",
    "updated on",
)


@dataclass(frozen=True)
class ClaimFinding:
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


def parse_long_date(match: re.Match[str]) -> date | None:
    month, day, year = match.group(1), match.group(2), match.group(3)
    try:
        return datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date()
    except ValueError:
        return None


def parse_iso_date(match: re.Match[str]) -> date | None:
    try:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return None


def collect_claims(root: Path, targets: list[str], max_age_days: int) -> list[ClaimFinding]:
    findings: list[ClaimFinding] = []
    today = date.today()

    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in targets:
        for path in sorted(root.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.add(path)
                files.append(path)

    for path in files:
        rel = path.relative_to(root).as_posix()
        for idx, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
            lowered = line.lower()
            if not any(h in lowered for h in CLAIM_HINTS):
                continue

            parsed_dates: list[date] = []
            for match in LONG_DATE_RE.finditer(line):
                parsed = parse_long_date(match)
                if parsed:
                    parsed_dates.append(parsed)
            for match in ISO_DATE_RE.finditer(line):
                parsed = parse_iso_date(match)
                if parsed:
                    parsed_dates.append(parsed)

            for parsed in parsed_dates:
                age_days = (today - parsed).days
                if age_days >= max_age_days:
                    findings.append(
                        ClaimFinding(
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
    parser = argparse.ArgumentParser(description="Audit stale release/activity date claims")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--max-age-days", type=int, default=120, help="Age threshold for stale claim reporting")
    parser.add_argument(
        "--targets",
        nargs="*",
        default=["tutorials/*/index.md"],
        help="Glob patterns (relative to repo root) to scan",
    )
    parser.add_argument("--json-output", help="Optional JSON output path")
    parser.add_argument("--fail-on-stale", action="store_true", help="Exit non-zero if stale claims found")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = collect_claims(root, targets=args.targets, max_age_days=args.max_age_days)

    print(f"stale_release_claim_count={len(findings)}")
    if findings:
        print("stale_release_claims:")
        for finding in findings[:200]:
            print(
                f"{finding.file}:{finding.line_number} age={finding.age_days}d "
                f"date={finding.parsed_date} :: {finding.line}"
            )
        if len(findings) > 200:
            print(f"... truncated {len(findings) - 200} additional stale claims")

    if args.json_output:
        out = Path(args.json_output).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "max_age_days": args.max_age_days,
            "stale_release_claim_count": len(findings),
            "targets": args.targets,
            "findings": [f.as_json() for f in findings],
        }
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.fail_on_stale and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
