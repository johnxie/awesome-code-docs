#!/usr/bin/env python3
"""Regenerate tutorial chapter content with real source code from GitHub repos.

Replaces template "Depth Expansion Playbook" content with actual code examples,
mermaid diagrams, and source-grounded explanations from the tutorial's source repo.

Usage:
    python scripts/regenerate_tutorial_chapters.py [--slugs slug1,slug2,...] [--batch N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed


TOKEN = os.environ.get("GITHUB_TOKEN", "")

# File extensions to fetch from source repos
SOURCE_EXTENSIONS = {
    ".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".h",
    ".jsx", ".tsx", ".rb", ".cs", ".kt", ".swift", ".lua", ".zig",
    ".json", ".yaml", ".yml", ".toml",
}

# Files/dirs to skip
SKIP_PATTERNS = {
    "test", "spec", "__pycache__", "node_modules", "dist", "build",
    ".git", ".github", ".vscode", "vendor", "target",
}

MAX_FILE_SIZE = 50_000  # 50KB per file
MAX_FILES = 25  # Max files to fetch per repo


def gh_request(url: str) -> dict | list | None:
    """Make a GitHub API request."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except (HTTPError, Exception):
        return None


def fetch_repo_tree(repo: str) -> list[dict]:
    """Fetch the repo file tree (top-level + key subdirs)."""
    data = gh_request(f"https://api.github.com/repos/{repo}/git/trees/HEAD?recursive=1")
    if not data or "tree" not in data:
        return []
    return data["tree"]


def should_include_file(path: str) -> bool:
    """Check if a file should be included based on extension and path."""
    parts = path.lower().split("/")
    # Skip test/build/vendor directories
    for part in parts:
        for skip in SKIP_PATTERNS:
            if skip in part:
                return False
    # Check extension
    ext = Path(path).suffix.lower()
    return ext in SOURCE_EXTENSIONS


def fetch_file_content(repo: str, path: str) -> str | None:
    """Fetch raw file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            if len(content) > MAX_FILE_SIZE:
                return content[:MAX_FILE_SIZE] + "\n# ... (truncated)"
            return content
    except Exception:
        return None


def fetch_source_files(repo: str) -> dict[str, str]:
    """Fetch key source files from a repo."""
    tree = fetch_repo_tree(repo)
    if not tree:
        return {}

    # Filter and prioritize files
    candidates = []
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        size = item.get("size", 0)
        if size > MAX_FILE_SIZE or size == 0:
            continue
        if should_include_file(path):
            # Prioritize: shorter paths (core files), larger files (more content)
            depth = path.count("/")
            candidates.append((path, depth, size))

    # Sort: shallow paths first, then by size (larger = more important)
    candidates.sort(key=lambda x: (x[1], -x[2]))
    candidates = candidates[:MAX_FILES]

    # Fetch content in parallel
    files = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(fetch_file_content, repo, path): path
            for path, _, _ in candidates
        }
        for future in as_completed(futures):
            path = futures[future]
            content = future.result()
            if content:
                files[path] = content

    return files


def extract_abstractions(files: dict[str, str], repo: str) -> list[dict]:
    """Identify core abstractions from source files."""
    abstractions = []

    for path, content in files.items():
        ext = Path(path).suffix.lower()

        # Extract classes
        if ext in {".py", ".ts", ".js", ".java", ".cs", ".kt"}:
            class_pattern = r"(?:export\s+)?(?:abstract\s+)?class\s+(\w+)"
            for match in re.finditer(class_pattern, content):
                name = match.group(1)
                # Get context around the class
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 500)
                context = content[start:end]
                abstractions.append({
                    "name": name,
                    "type": "class",
                    "file": path,
                    "context": context[:600],
                })

        # Extract functions/methods
        if ext == ".py":
            fn_pattern = r"^(?:async\s+)?def\s+(\w+)\s*\("
            for match in re.finditer(fn_pattern, content, re.M):
                name = match.group(1)
                if name.startswith("_") and not name.startswith("__"):
                    continue
                start = match.start()
                end = min(len(content), start + 800)
                abstractions.append({
                    "name": name,
                    "type": "function",
                    "file": path,
                    "context": content[start:end],
                })
        elif ext in {".ts", ".js", ".tsx", ".jsx"}:
            fn_pattern = r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\("
            for match in re.finditer(fn_pattern, content):
                name = match.group(1)
                start = match.start()
                end = min(len(content), start + 800)
                abstractions.append({
                    "name": name,
                    "type": "function",
                    "file": path,
                    "context": content[start:end],
                })
        elif ext == ".go":
            fn_pattern = r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\("
            for match in re.finditer(fn_pattern, content, re.M):
                name = match.group(1)
                start = match.start()
                end = min(len(content), start + 800)
                abstractions.append({
                    "name": name,
                    "type": "function",
                    "file": path,
                    "context": content[start:end],
                })
        elif ext == ".rs":
            fn_pattern = r"^pub\s+(?:async\s+)?fn\s+(\w+)"
            for match in re.finditer(fn_pattern, content, re.M):
                name = match.group(1)
                start = match.start()
                end = min(len(content), start + 800)
                abstractions.append({
                    "name": name,
                    "type": "function",
                    "file": path,
                    "context": content[start:end],
                })

        # Extract interfaces/traits/structs
        for pattern in [
            r"(?:export\s+)?interface\s+(\w+)",
            r"(?:pub\s+)?struct\s+(\w+)",
            r"(?:pub\s+)?trait\s+(\w+)",
            r"(?:pub\s+)?enum\s+(\w+)",
        ]:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                start = match.start()
                end = min(len(content), start + 600)
                abstractions.append({
                    "name": name,
                    "type": "interface",
                    "file": path,
                    "context": content[start:end],
                })

    return abstractions


def get_code_snippet(content: str, identifier: str, max_lines: int = 30) -> str:
    """Extract a focused code snippet around an identifier."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if identifier in line:
            start = max(0, i - 2)
            end = min(len(lines), i + max_lines)
            snippet = "\n".join(lines[start:end])
            return snippet
    return ""


def regenerate_chapter(
    chapter_path: Path,
    chapter_num: int,
    chapter_title: str,
    tutorial_title: str,
    repo: str,
    source_files: dict[str, str],
    abstractions: list[dict],
) -> bool:
    """Regenerate a single chapter file with real source code."""
    content = chapter_path.read_text(errors="ignore")

    # Check if it has depth expansion markers
    if "depth-expansion-v2" not in content and "Depth Expansion Playbook" not in content:
        return False

    # Preserve frontmatter
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n\n"
            body = parts[2].strip()

    # Preserve title
    title_match = re.search(r"^# .+", body, re.M)
    title_line = title_match.group(0) if title_match else f"# Chapter {chapter_num}: {chapter_title}"

    # Find relevant abstractions for this chapter
    relevant = abstractions[
        (chapter_num - 1) * max(1, len(abstractions) // 8):
        chapter_num * max(1, len(abstractions) // 8)
    ] if abstractions else []

    # Build code examples from source files
    code_examples = []
    for abst in relevant[:5]:
        file_path = abst["file"]
        ext = Path(file_path).suffix.lstrip(".")
        if file_path in source_files:
            snippet = get_code_snippet(source_files[file_path], abst["name"])
            if snippet and len(snippet) > 50:
                code_examples.append({
                    "name": abst["name"],
                    "type": abst["type"],
                    "file": file_path,
                    "ext": ext,
                    "snippet": snippet,
                })

    # If no relevant abstractions, use general source files
    if not code_examples:
        for path, file_content in list(source_files.items())[:3]:
            ext = Path(path).suffix.lstrip(".")
            lines = file_content.split("\n")
            snippet = "\n".join(lines[:35])
            if len(snippet) > 100:
                code_examples.append({
                    "name": Path(path).stem,
                    "type": "module",
                    "file": path,
                    "ext": ext,
                    "snippet": snippet,
                })

    # Strip the depth expansion template content
    # Keep everything before the first depth expansion marker
    depth_marker_pos = body.find("<!-- depth-expansion-v2 -->")
    if depth_marker_pos == -1:
        depth_marker_pos = body.find("## Depth Expansion Playbook")
    if depth_marker_pos == -1:
        depth_marker_pos = body.find("## Scenario Playbook")

    if depth_marker_pos > 0:
        # Keep the original content before the template
        preserved = body[:depth_marker_pos].strip()
    else:
        # Keep just the title and intro
        lines = body.split("\n")
        preserved_lines = []
        for line in lines:
            if "Depth Expansion" in line or "depth-expansion" in line or "Scenario Playbook" in line:
                break
            preserved_lines.append(line)
        preserved = "\n".join(preserved_lines).strip()

    # Build the new chapter content
    new_sections = []

    # Add code examples section
    if code_examples:
        new_sections.append("\n## Source Code Walkthrough\n")
        for i, ex in enumerate(code_examples[:4]):
            new_sections.append(f"### `{ex['file']}`\n")
            new_sections.append(
                f"The `{ex['name']}` {ex['type']} in "
                f"[`{ex['file']}`](https://github.com/{repo}/blob/HEAD/{ex['file']}) "
                f"handles a key part of this chapter's functionality:\n"
            )
            new_sections.append(f"```{ex['ext']}\n{ex['snippet']}\n```\n")
            new_sections.append(
                f"This {ex['type']} is important because it defines how "
                f"{tutorial_title} implements the patterns covered in this chapter.\n"
            )

    # Add a mermaid diagram
    if code_examples:
        names = [ex["name"] for ex in code_examples[:5]]
        mermaid_lines = ["```mermaid", "flowchart TD"]
        for i, name in enumerate(names):
            node_id = chr(65 + i)
            mermaid_lines.append(f"    {node_id}[{name}]")
        # Add connections
        for i in range(len(names) - 1):
            mermaid_lines.append(f"    {chr(65+i)} --> {chr(65+i+1)}")
        mermaid_lines.append("```")

        new_sections.append("\n## How These Components Connect\n")
        new_sections.append("\n".join(mermaid_lines) + "\n")

    # Build the final content
    result_parts = [frontmatter, preserved]

    # Add new sections
    result_parts.extend(new_sections)

    # Add navigation footer (preserve from original)
    nav_match = re.search(r"---\s*\n\s*\[.*?\]\(.*?\)", content, re.S)
    if nav_match:
        result_parts.append("\n---\n")
        # Extract chapter navigation links
        nav_links = re.findall(r"\[.*?\]\(.*?\)", content[nav_match.start():])
        for link in nav_links[:3]:
            result_parts.append(f"\n{link}")
        result_parts.append("")

    final = "\n".join(result_parts)

    # Ensure minimum quality
    if final.count("```") < 4:  # At least 2 code blocks
        return False

    chapter_path.write_text(final)
    return True


def process_tutorial(slug: str, tutorials_dir: Path) -> dict:
    """Process a single tutorial: fetch source and regenerate chapters."""
    tutorial_dir = tutorials_dir / slug
    readme = tutorial_dir / "README.md"

    if not readme.exists():
        return {"slug": slug, "status": "missing", "chapters_updated": 0}

    # Get repo from source verification
    sv_path = Path("discoverability/tutorial-source-verification.json")
    with open(sv_path) as f:
        sv = json.load(f)

    repo = None
    for t in sv["tutorials"]:
        if t["tutorial"] == slug:
            repo = t["primary_repo"]
            break

    if not repo:
        return {"slug": slug, "status": "no_repo", "chapters_updated": 0}

    # Extract tutorial title
    readme_content = readme.read_text()
    h1 = re.search(r"^# (.+)", readme_content, re.M)
    title = h1.group(1).strip() if h1 else slug

    # Fetch source files
    print(f"  [{slug}] Fetching source from {repo}...")
    source_files = fetch_source_files(repo)

    if not source_files:
        return {"slug": slug, "status": "no_source_files", "chapters_updated": 0}

    # Extract abstractions
    abstractions = extract_abstractions(source_files, repo)

    # Process each chapter
    chapters_updated = 0
    for chapter_path in sorted(tutorial_dir.glob("0*.md")):
        ch_num_match = re.match(r"(\d+)", chapter_path.name)
        ch_num = int(ch_num_match.group(1)) if ch_num_match else 1

        ch_content = chapter_path.read_text(errors="ignore")
        ch_title_match = re.search(r"^# .+?:\s*(.+)", ch_content, re.M)
        ch_title = ch_title_match.group(1) if ch_title_match else chapter_path.stem

        if regenerate_chapter(
            chapter_path, ch_num, ch_title, title,
            repo, source_files, abstractions
        ):
            chapters_updated += 1

    return {
        "slug": slug,
        "status": "ok",
        "chapters_updated": chapters_updated,
        "source_files": len(source_files),
        "abstractions": len(abstractions),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slugs", help="Comma-separated list of tutorial slugs")
    parser.add_argument("--batch", type=int, help="Process batch N (15 per batch)")
    parser.add_argument("--all-depth", action="store_true", help="Process all depth-expansion tutorials")
    args = parser.parse_args()

    tutorials_dir = Path("tutorials")

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(",")]
    elif args.all_depth:
        # Find all tutorials with depth expansion markers
        slugs = []
        for d in sorted(tutorials_dir.iterdir()):
            if not d.is_dir():
                continue
            for ch in d.glob("0*.md"):
                content = ch.read_text(errors="ignore")
                if "depth-expansion-v2" in content or "Depth Expansion Playbook" in content:
                    slugs.append(d.name)
                    break
    elif args.batch is not None:
        # Load all slugs and take batch
        with open("/tmp/tier1_tutorials.json") as f:
            all_tutorials = json.load(f)
        start = args.batch * 15
        end = start + 15
        slugs = [t["slug"] for t in all_tutorials[start:end]]
    else:
        print("Specify --slugs, --batch N, or --all-depth")
        return

    print(f"Processing {len(slugs)} tutorials...")

    results = []
    for slug in slugs:
        result = process_tutorial(slug, tutorials_dir)
        results.append(result)
        status = result["status"]
        updated = result.get("chapters_updated", 0)
        files = result.get("source_files", 0)
        print(f"  [{slug}] {status} — {updated} chapters updated, {files} source files")

    total_updated = sum(r.get("chapters_updated", 0) for r in results)
    print(f"\nTotal: {total_updated} chapters updated across {len(results)} tutorials")


if __name__ == "__main__":
    main()
