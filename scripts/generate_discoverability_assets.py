#!/usr/bin/env python3
"""Generate discoverability assets for SEO and LLM retrieval.

Outputs:
- discoverability/tutorial-index.json
- discoverability/tutorial-directory.md
- llms.txt
- llms-full.txt
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

TUTORIALS_DIR = "tutorials"
COMMON_STOPWORDS = {
    "a",
    "an",
    "and",
    "the",
    "of",
    "for",
    "to",
    "in",
    "on",
    "with",
    "by",
    "from",
    "how",
    "your",
    "you",
    "guide",
    "tutorial",
}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[1]
    return text


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def first_quote(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("> "):
            return line[2:].strip()
    return ""


def extract_keywords(slug: str, title: str, summary: str) -> list[str]:
    blob = f"{slug} {title} {summary}".lower()
    tokens = re.findall(r"[a-z0-9]+", blob)

    keywords: list[str] = []
    seen: set[str] = set()
    for t in tokens:
        if len(t) < 3:
            continue
        if t.isdigit():
            continue
        if t in COMMON_STOPWORDS:
            continue
        if t.startswith(("http", "www")):
            continue
        if t in {"github", "com", "johnxie", "main", "tree", "blob", "docs"}:
            continue
        if t in seen:
            continue
        seen.add(t)
        keywords.append(t)

    # keep compact and deterministic
    return keywords[:18]


def tutorial_dirs(root: Path) -> Iterable[Path]:
    tutorials_root = root / TUTORIALS_DIR
    for path in sorted([p for p in tutorials_root.iterdir() if p.is_dir()], key=lambda p: p.name):
        if (path / "index.md").is_file():
            yield path


def build_records(root: Path) -> list[dict]:
    records: list[dict] = []

    for tdir in tutorial_dirs(root):
        index_path = tdir / "index.md"
        raw = index_path.read_text(encoding="utf-8", errors="ignore")
        body = strip_frontmatter(raw)

        title = first_heading(body) or tdir.name.replace("-", " ").title()
        summary = first_quote(body)

        rel_dir = tdir.relative_to(root).as_posix()
        records.append(
            {
                "slug": tdir.name,
                "title": title,
                "summary": summary,
                "path": rel_dir,
                "index_path": f"{rel_dir}/index.md",
                "repo_url": f"https://github.com/johnxie/awesome-code-docs/tree/main/{rel_dir}",
                "file_url": f"https://github.com/johnxie/awesome-code-docs/blob/main/{rel_dir}/index.md",
                "keywords": extract_keywords(tdir.name, title, summary),
            }
        )

    return records


def write_json(output_path: Path, records: list[dict]) -> None:
    payload = {
        "project": "awesome-code-docs",
        "tutorial_count": len(records),
        "tutorials": records,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_llms_txt(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Awesome Code Docs",
        "> Deep-dive tutorials for popular open-source AI, developer-tooling, and data platforms.",
        "",
        "## Start Here",
        "- https://github.com/johnxie/awesome-code-docs",
        "- https://github.com/johnxie/awesome-code-docs/blob/main/README.md",
        "- https://github.com/johnxie/awesome-code-docs/blob/main/CONTRIBUTING.md",
        "- https://github.com/johnxie/awesome-code-docs/tree/main/tutorials",
        "",
        "## Priority Tutorial Clusters",
        "- AI Coding Tools: Cline, Roo Code, bolt.diy, OpenHands, Continue",
        "- Vibe Coding Platforms: Dyad, bolt.diy, VibeSDK, HAPI",
        "- LLM Frameworks: LangChain, LangGraph, LlamaIndex, DSPy",
        "- Infrastructure: Ollama, vLLM, LiteLLM, llama.cpp",
        "",
        "## Tutorial Directory",
    ]

    for record in records:
        lines.append(f"- {record['title']}: {record['repo_url']}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_llms_full_txt(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Awesome Code Docs (Full Tutorial Index)",
        "",
        "Main repository:",
        "- https://github.com/johnxie/awesome-code-docs",
        "",
    ]

    for record in records:
        lines.extend(
            [
                f"## {record['title']}",
                f"- Path: {record['path']}",
                f"- Index: {record['file_url']}",
                f"- Summary: {record['summary'] or 'N/A'}",
                f"- Keywords: {', '.join(record['keywords']) if record['keywords'] else 'N/A'}",
                "",
            ]
        )

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_directory_markdown(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Tutorial Directory (A-Z)",
        "",
        "This page is auto-generated from the tutorial index and is intended as a fast browse surface for contributors and search crawlers.",
        "",
        f"- Total tutorials: **{len(records)}**",
        "- Source: `scripts/generate_discoverability_assets.py`",
        "",
    ]

    grouped: dict[str, list[dict]] = {}
    for record in records:
        key = record["title"][:1].upper() if record["title"] else "#"
        if not key.isalpha():
            key = "#"
        grouped.setdefault(key, []).append(record)

    for key in sorted(grouped.keys()):
        lines.append(f"## {key}")
        lines.append("")
        for record in grouped[key]:
            summary = record["summary"] or "Deep technical walkthrough."
            lines.append(f"- [{record['title']}]({record['file_url']})")
            lines.append(f"  - {summary}")
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate discoverability assets")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--output-json",
        default="discoverability/tutorial-index.json",
        help="JSON output path",
    )
    parser.add_argument("--llms", default="llms.txt", help="llms.txt output path")
    parser.add_argument("--llms-full", default="llms-full.txt", help="llms-full.txt output path")
    parser.add_argument(
        "--directory-md",
        default="discoverability/tutorial-directory.md",
        help="A-Z markdown directory output path",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    json_path = (root / args.output_json).resolve()
    llms_path = (root / args.llms).resolve()
    llms_full_path = (root / args.llms_full).resolve()
    directory_md_path = (root / args.directory_md).resolve()

    json_path.parent.mkdir(parents=True, exist_ok=True)
    llms_path.parent.mkdir(parents=True, exist_ok=True)
    llms_full_path.parent.mkdir(parents=True, exist_ok=True)
    directory_md_path.parent.mkdir(parents=True, exist_ok=True)

    records = build_records(root)
    write_json(json_path, records)
    write_llms_txt(llms_path, records)
    write_llms_full_txt(llms_full_path, records)
    write_directory_markdown(directory_md_path, records)

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote llms.txt: {llms_path}")
    print(f"Wrote llms-full.txt: {llms_full_path}")
    print(f"Wrote directory markdown: {directory_md_path}")
    print(f"tutorial_count={len(records)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
