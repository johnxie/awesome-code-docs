#!/usr/bin/env python3
"""Verify upstream GitHub source repositories referenced by tutorial indexes.

Outputs:
- discoverability/tutorial-source-verification.json
- discoverability/tutorial-source-verification.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

GITHUB_LINK_RE = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:[/?#][^)\s\"'>]*)?")
LOCAL_REPO_OWNER = "johnxie"
LOCAL_REPO_NAME = "awesome-code-docs"
IGNORED_REPOS = {
    "The-Pocket/Tutorial-Codebase-Knowledge",
}


@dataclass(frozen=True)
class TutorialSourceRecord:
    tutorial: str
    index_path: str
    source_repos: tuple[str, ...]


def extract_source_repos(index_text: str) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()

    for owner, repo in GITHUB_LINK_RE.findall(index_text):
        repo_clean = repo[:-4] if repo.endswith(".git") else repo
        full = f"{owner}/{repo_clean}"
        if owner.lower() == LOCAL_REPO_OWNER and repo_clean.lower() == LOCAL_REPO_NAME:
            continue
        if full in IGNORED_REPOS:
            continue
        if full in seen:
            continue
        seen.add(full)
        ordered.append(full)

    return tuple(ordered)


def collect_tutorial_records(root: Path) -> list[TutorialSourceRecord]:
    tutorials_root = root / "tutorials"
    records: list[TutorialSourceRecord] = []

    for tutorial_dir in sorted(p for p in tutorials_root.iterdir() if p.is_dir()):
        index_path = tutorial_dir / "index.md"
        if not index_path.is_file():
            continue
        text = index_path.read_text(encoding="utf-8", errors="ignore")
        source_repos = extract_source_repos(text)
        records.append(
            TutorialSourceRecord(
                tutorial=tutorial_dir.name,
                index_path=index_path.relative_to(root).as_posix(),
                source_repos=source_repos,
            )
        )

    return records


def fetch_repo_metadata(repo: str, token: str | None, timeout: float) -> dict[str, Any]:
    req = Request(f"https://api.github.com/repos/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "awesome-code-docs-source-verification")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return {
                "repo": repo,
                "verified": True,
                "http_status": response.status,
                "stars": int(payload.get("stargazers_count", 0)),
                "forks": int(payload.get("forks_count", 0)),
                "open_issues": int(payload.get("open_issues_count", 0)),
                "default_branch": payload.get("default_branch"),
                "archived": bool(payload.get("archived", False)),
                "pushed_at": payload.get("pushed_at"),
                "updated_at": payload.get("updated_at"),
                "html_url": payload.get("html_url") or f"https://github.com/{repo}",
                "reason": "",
            }
    except HTTPError as exc:
        reason = f"HTTP {exc.code}"
        try:
            body = exc.read().decode("utf-8", errors="ignore")
            if body:
                reason = f"{reason}: {body[:240]}"
        except Exception:
            pass
        return {
            "repo": repo,
            "verified": False,
            "http_status": exc.code,
            "stars": None,
            "forks": None,
            "open_issues": None,
            "default_branch": None,
            "archived": None,
            "pushed_at": None,
            "updated_at": None,
            "html_url": f"https://github.com/{repo}",
            "reason": reason,
        }
    except URLError as exc:
        return {
            "repo": repo,
            "verified": False,
            "http_status": None,
            "stars": None,
            "forks": None,
            "open_issues": None,
            "default_branch": None,
            "archived": None,
            "pushed_at": None,
            "updated_at": None,
            "html_url": f"https://github.com/{repo}",
            "reason": f"Network error: {exc.reason}",
        }


def verify_repositories(
    repos: list[str], token: str | None, timeout: float, max_workers: int
) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    if not repos:
        return results

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {
            pool.submit(fetch_repo_metadata, repo, token, timeout): repo
            for repo in repos
        }
        for future in as_completed(future_map):
            repo = future_map[future]
            try:
                results[repo] = future.result()
            except Exception as exc:
                results[repo] = {
                    "repo": repo,
                    "verified": False,
                    "http_status": None,
                    "stars": None,
                    "forks": None,
                    "open_issues": None,
                    "default_branch": None,
                    "archived": None,
                    "pushed_at": None,
                    "updated_at": None,
                    "html_url": f"https://github.com/{repo}",
                    "reason": f"Unhandled verification error: {exc}",
                }

    return results


def tutorial_report(
    records: list[TutorialSourceRecord], repo_results: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    tutorials: list[dict[str, Any]] = []
    tutorials_with_sources = 0
    tutorials_without_sources = 0
    tutorials_with_unverified = 0

    for record in records:
        per_repo = [repo_results[r] for r in record.source_repos]
        verified_count = sum(1 for item in per_repo if item["verified"])
        unverified_count = len(per_repo) - verified_count
        has_sources = len(per_repo) > 0
        has_unverified = unverified_count > 0

        if has_sources:
            tutorials_with_sources += 1
        else:
            tutorials_without_sources += 1

        if has_unverified:
            tutorials_with_unverified += 1

        primary_repo = record.source_repos[0] if record.source_repos else None
        primary_repo_data = repo_results.get(primary_repo) if primary_repo else None

        tutorials.append(
            {
                "tutorial": record.tutorial,
                "index_path": record.index_path,
                "source_repo_count": len(per_repo),
                "source_repos": list(record.source_repos),
                "primary_repo": primary_repo,
                "primary_repo_verified": bool(primary_repo_data and primary_repo_data["verified"]),
                "verified_repo_count": verified_count,
                "unverified_repo_count": unverified_count,
                "repositories": per_repo,
            }
        )

    unique_repos = sorted(repo_results.keys())
    verified_unique_repos = [r for r in unique_repos if repo_results[r]["verified"]]
    unverified_unique_repos = [r for r in unique_repos if not repo_results[r]["verified"]]

    by_popularity = sorted(
        [repo_results[r] for r in verified_unique_repos],
        key=lambda item: item.get("stars") or 0,
        reverse=True,
    )

    now = datetime.now(timezone.utc)

    return {
        "generated_at_utc": now.isoformat().replace("+00:00", "Z"),
        "generated_on": now.date().isoformat(),
        "summary": {
            "tutorial_count": len(records),
            "tutorials_with_source_repos": tutorials_with_sources,
            "tutorials_without_source_repos": tutorials_without_sources,
            "tutorials_with_unverified_source_repos": tutorials_with_unverified,
            "unique_source_repo_count": len(unique_repos),
            "unique_verified_repo_count": len(verified_unique_repos),
            "unique_unverified_repo_count": len(unverified_unique_repos),
        },
        "top_verified_repos_by_stars": by_popularity[:25],
        "unverified_repositories": [repo_results[r] for r in unverified_unique_repos],
        "tutorials": tutorials,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Tutorial Source Verification Report",
        "",
        "Automated verification of GitHub source repositories referenced by `tutorials/*/index.md`.",
        "",
        f"- generated_on: **{report['generated_on']}**",
        f"- tutorials scanned: **{summary['tutorial_count']}**",
        f"- tutorials with source repos: **{summary['tutorials_with_source_repos']}**",
        f"- tutorials without source repos: **{summary['tutorials_without_source_repos']}**",
        f"- tutorials with unverified repos: **{summary['tutorials_with_unverified_source_repos']}**",
        f"- unique source repos: **{summary['unique_source_repo_count']}**",
        f"- unique verified repos: **{summary['unique_verified_repo_count']}**",
        f"- unique unverified repos: **{summary['unique_unverified_repo_count']}**",
        "",
        "## Top Verified Repositories by Stars",
        "",
        "| Repository | Stars | Last Push | Archived |",
        "|:-----------|------:|:----------|:---------|",
    ]

    for repo in report["top_verified_repos_by_stars"]:
        lines.append(
            "| "
            f"[`{repo['repo']}`]({repo['html_url']}) | "
            f"{repo.get('stars', 0):,} | "
            f"{(repo.get('pushed_at') or 'n/a')[:10]} | "
            f"{'yes' if repo.get('archived') else 'no'} |"
        )

    lines.extend(["", "## Tutorials Missing Source Repository Links", ""])
    lines.append("| Tutorial | Index Path |")
    lines.append("|:---------|:-----------|")

    for tutorial in report["tutorials"]:
        if tutorial["source_repo_count"] == 0:
            lines.append(
                f"| `{tutorial['tutorial']}` | `{tutorial['index_path']}` |"
            )

    lines.extend(["", "## Tutorials with Unverified Source Repositories", ""])
    lines.append("| Tutorial | Primary Repo | Unverified Count |")
    lines.append("|:---------|:-------------|-----------------:|")
    for tutorial in report["tutorials"]:
        if tutorial["unverified_repo_count"] > 0:
            primary = tutorial["primary_repo"] or "n/a"
            lines.append(
                f"| `{tutorial['tutorial']}` | `{primary}` | {tutorial['unverified_repo_count']} |"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify tutorial source repository links")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--json-output",
        default="discoverability/tutorial-source-verification.json",
        help="JSON output path",
    )
    parser.add_argument(
        "--markdown-output",
        default="discoverability/tutorial-source-verification.md",
        help="Markdown output path",
    )
    parser.add_argument("--timeout-seconds", type=float, default=20.0, help="HTTP request timeout")
    parser.add_argument("--max-workers", type=int, default=16, help="Concurrent verification workers")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    token = os.getenv("GITHUB_TOKEN")

    records = collect_tutorial_records(root)
    all_repos = sorted({repo for rec in records for repo in rec.source_repos})
    repo_results = verify_repositories(
        repos=all_repos,
        token=token,
        timeout=args.timeout_seconds,
        max_workers=args.max_workers,
    )

    report = tutorial_report(records, repo_results)

    json_output = (root / args.json_output).resolve()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md_output = (root / args.markdown_output).resolve()
    md_output.parent.mkdir(parents=True, exist_ok=True)
    md_output.write_text(render_markdown(report) + "\n", encoding="utf-8")

    summary = report["summary"]
    print(f"tutorial_count={summary['tutorial_count']}")
    print(f"tutorials_with_source_repos={summary['tutorials_with_source_repos']}")
    print(f"tutorials_without_source_repos={summary['tutorials_without_source_repos']}")
    print(f"tutorials_with_unverified_source_repos={summary['tutorials_with_unverified_source_repos']}")
    print(f"unique_source_repo_count={summary['unique_source_repo_count']}")
    print(f"unique_verified_repo_count={summary['unique_verified_repo_count']}")
    print(f"unique_unverified_repo_count={summary['unique_unverified_repo_count']}")
    print(f"json_output={json_output}")
    print(f"markdown_output={md_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
