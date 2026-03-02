#!/usr/bin/env python3
"""Refresh Current Snapshot sections in tutorial README.md files.

For each tutorial:
1. Read the README.md
2. Look up source repo from tutorial-source-verification.json
3. Fetch latest repo metadata and release from GitHub API
4. Update or insert the Current Snapshot section
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def _gh_request(url: str, token: str | None) -> dict[str, Any] | None:
    req = Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "awesome-code-docs-snapshot-refresh")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404:
            return None
        if exc.code == 403:
            print(f"  RATE LIMITED on {url}", file=sys.stderr)
            return None
        print(f"  HTTP {exc.code} on {url}", file=sys.stderr)
        return None
    except URLError as exc:
        print(f"  URL error on {url}: {exc.reason}", file=sys.stderr)
        return None


def fetch_repo_data(repo: str, token: str | None) -> dict[str, Any]:
    """Fetch repo metadata + latest release for a GitHub repo."""
    base = _gh_request(f"https://api.github.com/repos/{repo}", token)
    if not base:
        return {"repo": repo, "stars": None, "release_tag": None}

    stars = base.get("stargazers_count", 0)
    archived = base.get("archived", False)
    pushed_at = base.get("pushed_at", "")

    release = _gh_request(
        f"https://api.github.com/repos/{repo}/releases/latest", token
    )
    release_tag = None
    release_date = None
    if release and not release.get("prerelease"):
        release_tag = release.get("tag_name")
        pub = release.get("published_at", "")
        if pub:
            try:
                release_date = datetime.fromisoformat(
                    pub.replace("Z", "+00:00")
                ).strftime("%Y-%m-%d")
            except ValueError:
                pass

    return {
        "repo": repo,
        "stars": stars,
        "archived": archived,
        "pushed_at": pushed_at,
        "release_tag": release_tag,
        "release_date": release_date,
    }


# ---------------------------------------------------------------------------
# Source mapping
# ---------------------------------------------------------------------------

def load_source_mapping(root: Path) -> dict[str, str]:
    """Build {tutorial_slug: primary_repo} from verification JSON."""
    verify_path = root / "discoverability" / "tutorial-source-verification.json"
    if not verify_path.is_file():
        print(f"Missing {verify_path}", file=sys.stderr)
        return {}

    data = json.loads(verify_path.read_text(encoding="utf-8"))
    tutorials_root = root / "tutorials"

    # Build repo -> tutorial slug mapping from the per-tutorial records
    slug_to_repo: dict[str, str] = {}
    for entry in data.get("top_verified_repos_by_stars", []):
        repo = entry.get("repo", "")
        if not repo:
            continue
        # Find which tutorial(s) reference this repo
        # We need to scan tutorial README.md files for the repo URL
        pass

    # Alternative approach: scan each tutorial README.md for the first GitHub repo link
    github_re = re.compile(
        r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
    )
    for tdir in sorted(tutorials_root.iterdir()):
        if not tdir.is_dir():
            continue
        readme = tdir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        # Look for repo in Current Snapshot section first
        snapshot_match = re.search(
            r"repository:\s*\[`([^`]+)`\]", text
        )
        if snapshot_match:
            slug_to_repo[tdir.name] = snapshot_match.group(1)
            continue
        # Fall back to first GitHub repo badge
        badge_match = re.search(
            r"GitHub-([A-Za-z0-9_.-]+%2F[A-Za-z0-9_.-]+)", text
        )
        if badge_match:
            slug_to_repo[tdir.name] = badge_match.group(1).replace("%2F", "/")
            continue
        # Fall back to first GitHub link after the title
        links = github_re.findall(text)
        # Filter out common non-repo links
        for link in links:
            parts = link.split("/")
            if len(parts) >= 2 and parts[0] not in (
                "johnxie", "The-Pocket", "actions",
            ):
                slug_to_repo[tdir.name] = link
                break

    return slug_to_repo


# ---------------------------------------------------------------------------
# Snapshot formatting
# ---------------------------------------------------------------------------

def format_stars(count: int) -> str:
    """Format star count as human-readable string."""
    if count >= 1000:
        val = count / 1000
        if val >= 100:
            return f"**{val:,.0f}k**"
        return f"**{val:,.1f}k**".replace(".0k", "k")
    return f"**{count}**"


def build_snapshot_lines(data: dict[str, Any]) -> list[str]:
    """Build the Current Snapshot section lines."""
    repo = data["repo"]
    lines = [
        "## Current Snapshot (auto-updated)",
        "",
        f"- repository: [`{repo}`](https://github.com/{repo})",
    ]
    if data.get("stars") is not None:
        lines.append(f"- stars: about {format_stars(data['stars'])}")
    if data.get("release_tag"):
        tag = data["release_tag"]
        release_line = f"- latest release: [`{tag}`](https://github.com/{repo}/releases/tag/{tag})"
        if data.get("release_date"):
            release_line += f" (published {data['release_date']})"
        lines.append(release_line)
    if data.get("archived"):
        lines.append("- status: **archived**")
    return lines


# ---------------------------------------------------------------------------
# README.md update logic
# ---------------------------------------------------------------------------

SNAPSHOT_HEADING = re.compile(r"^## Current Snapshot", re.MULTILINE)
NEXT_H2 = re.compile(r"^## ", re.MULTILINE)


def update_readme_snapshot(readme_path: Path, snapshot_lines: list[str]) -> bool:
    """Update or insert Current Snapshot section in a tutorial README.md.

    Returns True if the file was modified.
    """
    text = readme_path.read_text(encoding="utf-8")
    new_section = "\n".join(snapshot_lines)

    m = SNAPSHOT_HEADING.search(text)
    if m:
        # Find the end of this section (next ## heading or EOF)
        rest = text[m.end():]
        next_h2 = NEXT_H2.search(rest)
        if next_h2:
            end_pos = m.end() + next_h2.start()
        else:
            end_pos = len(text)
        # Replace the section
        updated = text[:m.start()] + new_section + "\n\n" + text[end_pos:]
    else:
        # Insert after ## Why This Track Matters / ## Why This Tutorial Exists
        insert_re = re.compile(
            r"^(## Why This (?:Track Matters|Tutorial Exists).*?)(?=^## )",
            re.MULTILINE | re.DOTALL,
        )
        im = insert_re.search(text)
        if im:
            insert_pos = im.end()
            updated = text[:insert_pos] + new_section + "\n\n" + text[insert_pos:]
        else:
            # Insert after first ## heading section
            first_h2 = NEXT_H2.search(text)
            if first_h2:
                rest_after = text[first_h2.end():]
                second_h2 = NEXT_H2.search(rest_after)
                if second_h2:
                    insert_pos = first_h2.end() + second_h2.start()
                else:
                    insert_pos = len(text)
                updated = text[:insert_pos] + new_section + "\n\n" + text[insert_pos:]
            else:
                # Append at end
                updated = text.rstrip() + "\n\n" + new_section + "\n"

    if updated == text:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh Current Snapshot sections in tutorial README.md files"
    )
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--workers", type=int, default=16, help="API concurrency")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Warning: GITHUB_TOKEN not set; API rate limit is 60 req/hr", file=sys.stderr)

    # Load tutorial -> repo mapping
    slug_to_repo = load_source_mapping(root)
    print(f"tutorials_mapped={len(slug_to_repo)}")

    # Deduplicate repos and fetch data
    unique_repos = sorted(set(slug_to_repo.values()))
    print(f"unique_repos_to_fetch={len(unique_repos)}")

    repo_data: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(fetch_repo_data, repo, token): repo
            for repo in unique_repos
        }
        for i, future in enumerate(as_completed(futures), 1):
            repo = futures[future]
            try:
                result = future.result()
                repo_data[repo] = result
            except Exception as exc:
                print(f"  FAILED {repo}: {exc}", file=sys.stderr)
                repo_data[repo] = {"repo": repo, "stars": None, "release_tag": None}
            if i % 50 == 0:
                print(f"  fetched {i}/{len(unique_repos)}")

    print(f"repos_fetched={len(repo_data)}")

    # Update each tutorial
    updated_count = 0
    skipped_count = 0
    for slug, repo in sorted(slug_to_repo.items()):
        readme_path = root / "tutorials" / slug / "README.md"
        if not readme_path.is_file():
            continue

        data = repo_data.get(repo)
        if not data or data.get("stars") is None:
            skipped_count += 1
            continue

        snapshot_lines = build_snapshot_lines(data)

        if args.dry_run:
            print(f"  WOULD UPDATE {slug}: {data.get('stars')} stars, release={data.get('release_tag')}")
            updated_count += 1
        else:
            if update_readme_snapshot(readme_path, snapshot_lines):
                updated_count += 1

    print(f"tutorials_updated={updated_count}")
    print(f"tutorials_skipped={skipped_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
