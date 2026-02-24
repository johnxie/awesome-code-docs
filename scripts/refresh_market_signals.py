#!/usr/bin/env python3
"""Refresh live GitHub market signals and update README trending block.

Outputs:
- discoverability/market-signals.json
- discoverability/trending-vibe-coding.md
- README.md (or custom output path)
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TRACKED_REPOS: tuple[dict[str, str], ...] = (
    {
        "repo": "open-webui/open-webui",
        "tutorial_path": "tutorials/open-webui-tutorial/",
        "tutorial_label": "Open WebUI Tutorial",
        "why": "self-hosted AI interface and model operations",
    },
    {
        "repo": "anomalyco/opencode",
        "tutorial_path": "tutorials/opencode-tutorial/",
        "tutorial_label": "OpenCode Tutorial",
        "why": "terminal-native coding agent with strong provider and tool controls",
    },
    {
        "repo": "browser-use/browser-use",
        "tutorial_path": "tutorials/browser-use-tutorial/",
        "tutorial_label": "Browser Use Tutorial",
        "why": "browser-native AI automation and agent execution",
    },
    {
        "repo": "cline/cline",
        "tutorial_path": "tutorials/cline-tutorial/",
        "tutorial_label": "Cline Tutorial",
        "why": "agentic coding with terminal, browser, and MCP workflows",
    },
    {
        "repo": "daytonaio/daytona",
        "tutorial_path": "tutorials/daytona-tutorial/",
        "tutorial_label": "Daytona Tutorial",
        "why": "sandbox infrastructure for secure AI code execution",
    },
    {
        "repo": "TabbyML/tabby",
        "tutorial_path": "tutorials/tabby-tutorial/",
        "tutorial_label": "Tabby Tutorial",
        "why": "self-hosted coding assistant platform for teams",
    },
    {
        "repo": "continuedev/continue",
        "tutorial_path": "tutorials/continue-tutorial/",
        "tutorial_label": "Continue Tutorial",
        "why": "IDE-native AI coding assistant architecture",
    },
    {
        "repo": "Mintplex-Labs/anything-llm",
        "tutorial_path": "tutorials/anything-llm-tutorial/",
        "tutorial_label": "AnythingLLM Tutorial",
        "why": "self-hosted RAG workspaces and agent workflows",
    },
    {
        "repo": "Fission-AI/OpenSpec",
        "tutorial_path": "tutorials/openspec-tutorial/",
        "tutorial_label": "OpenSpec Tutorial",
        "why": "spec-driven workflow layer for predictable AI-assisted delivery",
    },
    {
        "repo": "RooCodeInc/Roo-Code",
        "tutorial_path": "tutorials/roo-code-tutorial/",
        "tutorial_label": "Roo Code Tutorial",
        "why": "multi-mode coding agents and approval workflows",
    },
    {
        "repo": "vercel/ai",
        "tutorial_path": "tutorials/vercel-ai-tutorial/",
        "tutorial_label": "Vercel AI SDK Tutorial",
        "why": "production TypeScript AI app and agent SDK patterns",
    },
    {
        "repo": "stackblitz-labs/bolt.diy",
        "tutorial_path": "tutorials/bolt-diy-tutorial/",
        "tutorial_label": "bolt.diy Tutorial",
        "why": "open-source Bolt-style product builder stack",
    },
    {
        "repo": "dyad-sh/dyad",
        "tutorial_path": "tutorials/dyad-tutorial/",
        "tutorial_label": "Dyad Tutorial",
        "why": "local-first AI app generation workflows",
    },
    {
        "repo": "sweepai/sweep",
        "tutorial_path": "tutorials/sweep-tutorial/",
        "tutorial_label": "Sweep Tutorial",
        "why": "issue-to-PR coding agent workflows and GitHub automation",
    },
    {
        "repo": "stagewise-io/stagewise",
        "tutorial_path": "tutorials/stagewise-tutorial/",
        "tutorial_label": "Stagewise Tutorial",
        "why": "browser-context frontend coding agent workflows",
    },
    {
        "repo": "cloudflare/vibesdk",
        "tutorial_path": "tutorials/vibesdk-tutorial/",
        "tutorial_label": "VibeSDK Tutorial",
        "why": "Cloudflare-native prompt-to-app platform architecture",
    },
)

BEGIN_MARKER = "<!-- BEGIN: TRENDING_VIBE_CODING -->"
END_MARKER = "<!-- END: TRENDING_VIBE_CODING -->"


@dataclass(frozen=True)
class RepoSignal:
    repo: str
    repo_url: str
    tutorial_path: str
    tutorial_label: str
    why: str
    stars: int
    forks: int
    open_issues: int
    pushed_at: str
    pushed_date: str
    days_since_push: int

    def as_json(self) -> dict[str, Any]:
        return {
            "repo": self.repo,
            "repo_url": self.repo_url,
            "tutorial_path": self.tutorial_path,
            "tutorial_label": self.tutorial_label,
            "why": self.why,
            "stars": self.stars,
            "forks": self.forks,
            "open_issues": self.open_issues,
            "pushed_at": self.pushed_at,
            "pushed_date": self.pushed_date,
            "days_since_push": self.days_since_push,
        }


def fetch_repo(repo: str, token: str | None = None) -> dict[str, Any]:
    req = Request(f"https://api.github.com/repos/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "awesome-code-docs-refresh-market-signals")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub API request failed for {repo}: HTTP {exc.code} {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub API request failed for {repo}: {exc.reason}") from exc


def to_signal(config: dict[str, str], payload: dict[str, Any], now: datetime) -> RepoSignal:
    pushed_at = payload.get("pushed_at")
    if not isinstance(pushed_at, str) or not pushed_at:
        raise ValueError(f"Missing pushed_at for {config['repo']}")

    try:
        pushed_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Invalid pushed_at for {config['repo']}: {pushed_at}") from exc

    days_since_push = (now.date() - pushed_dt.date()).days

    return RepoSignal(
        repo=config["repo"],
        repo_url=payload.get("html_url") or f"https://github.com/{config['repo']}",
        tutorial_path=config["tutorial_path"],
        tutorial_label=config["tutorial_label"],
        why=config["why"],
        stars=int(payload.get("stargazers_count", 0)),
        forks=int(payload.get("forks_count", 0)),
        open_issues=int(payload.get("open_issues_count", 0)),
        pushed_at=pushed_at,
        pushed_date=pushed_dt.date().isoformat(),
        days_since_push=days_since_push,
    )


def sort_signals(signals: list[RepoSignal]) -> list[RepoSignal]:
    return sorted(signals, key=lambda s: (s.stars, -s.days_since_push), reverse=True)


def render_trending_block(signals: list[RepoSignal], generated_on: str) -> str:
    lines = [
        BEGIN_MARKER,
        f"## 📈 Trending Vibe-Coding Repos (Auto-updated {generated_on})",
        "",
        "Live GitHub market signals for high-impact open-source coding-agent and vibe-coding ecosystems with direct tutorial coverage.",
        "",
        "| Ecosystem Repo | Tutorial | Stars | Last Push | Why It Matters |",
        "|:---------------|:---------|------:|:----------|:---------------|",
    ]

    for signal in signals:
        lines.append(
            "| "
            f"[`{signal.repo}`]({signal.repo_url}) | "
            f"[{signal.tutorial_label}]({signal.tutorial_path}) | "
            f"{signal.stars:,} | "
            f"{signal.pushed_date} ({signal.days_since_push}d ago) | "
            f"{signal.why} |"
        )

    lines.extend(
        [
            "",
            "Data source: GitHub REST API (`stargazers_count`, `pushed_at`) via `scripts/refresh_market_signals.py`.",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def update_readme_section(readme_text: str, block: str) -> str:
    if BEGIN_MARKER in readme_text and END_MARKER in readme_text:
        prefix, rest = readme_text.split(BEGIN_MARKER, 1)
        _, suffix = rest.split(END_MARKER, 1)
        return prefix.rstrip() + "\n\n" + block + "\n" + suffix.lstrip("\n")

    start_heading = "## 📈 Trending Vibe-Coding Repos"
    next_heading = "## 📚 Tutorial Catalog"
    start_idx = readme_text.find(start_heading)
    end_idx = readme_text.find(next_heading)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        raise ValueError("Unable to locate trending section in README for replacement")

    return readme_text[:start_idx].rstrip() + "\n\n" + block + "\n\n" + readme_text[end_idx:].lstrip()


def render_market_markdown(signals: list[RepoSignal], generated_on: str) -> str:
    lines = [
        "# Market Signals Snapshot",
        "",
        "Auto-generated competitive snapshot for tracked coding-agent and vibe-coding ecosystems.",
        "",
        f"- generated_on: **{generated_on}**",
        f"- tracked_repositories: **{len(signals)}**",
        "",
        "| Repo | Stars | Forks | Last Push | Tutorial |",
        "|:-----|------:|------:|:----------|:---------|",
    ]

    for signal in signals:
        lines.append(
            "| "
            f"[`{signal.repo}`]({signal.repo_url}) | "
            f"{signal.stars:,} | "
            f"{signal.forks:,} | "
            f"{signal.pushed_date} ({signal.days_since_push}d ago) | "
            f"[{signal.tutorial_label}](../{signal.tutorial_path}) |"
        )

    lines.append("")
    return "\n".join(lines)


def write_json(path: Path, signals: list[RepoSignal], generated_at: datetime) -> None:
    payload = {
        "generated_at_utc": generated_at.isoformat().replace("+00:00", "Z"),
        "generated_on": generated_at.date().isoformat(),
        "tracked_repository_count": len(signals),
        "signals": [s.as_json() for s in signals],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh market signals and README trending section")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--source-readme",
        default="README.md",
        help="Input README path relative to root",
    )
    parser.add_argument(
        "--readme-output",
        default="README.md",
        help="Output README path relative to root",
    )
    parser.add_argument(
        "--market-json",
        default="discoverability/market-signals.json",
        help="Market signals JSON output path relative to root",
    )
    parser.add_argument(
        "--market-md",
        default="discoverability/trending-vibe-coding.md",
        help="Market signals markdown output path relative to root",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source_readme = (root / args.source_readme).resolve()
    readme_output = (root / args.readme_output).resolve()
    market_json_path = (root / args.market_json).resolve()
    market_md_path = (root / args.market_md).resolve()

    now = datetime.now(timezone.utc)
    generated_on = now.date().isoformat()
    token = os.getenv("GITHUB_TOKEN")

    signals: list[RepoSignal] = []
    for config in TRACKED_REPOS:
        payload = fetch_repo(config["repo"], token=token)
        signals.append(to_signal(config, payload, now=now))

    sorted_signals = sort_signals(signals)
    trending_block = render_trending_block(sorted_signals, generated_on=generated_on)

    readme_text = source_readme.read_text(encoding="utf-8")
    updated_readme = update_readme_section(readme_text, trending_block)

    market_md_path.parent.mkdir(parents=True, exist_ok=True)
    market_md_path.write_text(render_market_markdown(sorted_signals, generated_on=generated_on), encoding="utf-8")
    write_json(market_json_path, sorted_signals, generated_at=now)

    readme_output.parent.mkdir(parents=True, exist_ok=True)
    readme_output.write_text(updated_readme, encoding="utf-8")

    print(f"Wrote: {market_json_path}")
    print(f"Wrote: {market_md_path}")
    print(f"Wrote: {readme_output}")
    print(f"tracked_repository_count={len(sorted_signals)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
