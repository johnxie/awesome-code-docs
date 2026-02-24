#!/usr/bin/env python3
"""Contextualize generic chapter sections added by bulk style passes.

Targets these sections when they match generic boilerplate:
- ## What Problem Does This Solve?
- ## How it Works Under the Hood
- ## Source Walkthrough
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

NUMBERED_FILE_RE = re.compile(r"^([0-9]{2,})[-_].+\.md$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SECTION_RE_TEMPLATE = r"(^## {heading}\n\n)(.*?)(?=^## |\Z)"
CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*\n(.*?)```", re.S)
IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]{3,}\b")
STOPWORDS = {
    "this",
    "that",
    "with",
    "from",
    "return",
    "class",
    "const",
    "async",
    "await",
    "function",
    "import",
    "export",
    "string",
    "number",
    "boolean",
    "public",
    "private",
    "default",
    "value",
    "data",
    "type",
    "true",
    "false",
    "null",
    "undefined",
    "chapter",
    "tutorial",
}
IGNORED_SOURCE_URL_PARTS = (
    "github.com/The-Pocket/Tutorial-Codebase-Knowledge",
)

GENERIC_PROBLEM_HINT = "Think of this chapter as one subsystem in a larger machine"
GENERIC_UNDER_HOOD_HINT = "At runtime, this chapter's system behavior typically follows a predictable lifecycle"
GENERIC_SOURCE_HINT = "Use these upstream sources for deeper validation and implementation detail"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def first_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug_phrase(text: str) -> str:
    return text.replace("-", " ").replace("_", " ").strip()


def chapter_files(tutorial_dir: Path) -> list[Path]:
    out: list[tuple[int, str, Path]] = []
    for path in tutorial_dir.glob("*.md"):
        if path.name == "index.md":
            continue
        match = NUMBERED_FILE_RE.match(path.name)
        if not match:
            continue
        out.append((int(match.group(1)), path.name, path))
    out.sort(key=lambda x: (x[0], x[1]))
    return [p for _, _, p in out]


def extract_source_refs(index_text: str, limit: int = 8) -> list[tuple[str, str]]:
    section = extract_section_body(index_text, "Source References")
    if not section:
        section = index_text
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, url in LINK_RE.findall(section):
        label = label.strip()
        url = url.strip()
        if any(part in url for part in IGNORED_SOURCE_URL_PARTS):
            continue
        if url in seen:
            continue
        seen.add(url)
        out.append((label, url))
        if len(out) >= limit:
            break
    return out


def extract_section_body(text: str, heading: str) -> str:
    pattern = re.compile(SECTION_RE_TEMPLATE.format(heading=re.escape(heading)), re.S | re.M)
    match = pattern.search(text)
    return match.group(2).strip() if match else ""


def replace_section_body(text: str, heading: str, new_body: str) -> tuple[str, bool]:
    pattern = re.compile(SECTION_RE_TEMPLATE.format(heading=re.escape(heading)), re.S | re.M)
    match = pattern.search(text)
    if not match:
        return text, False
    new = text[: match.start(2)] + new_body.strip() + "\n\n" + text[match.end(2) :]
    return new, True


def top_identifiers(chapter_text: str, limit: int = 6) -> list[str]:
    counts: Counter[str] = Counter()
    for block in CODE_BLOCK_RE.findall(chapter_text):
        for token in IDENT_RE.findall(block):
            if token.lower() in STOPWORDS:
                continue
            if token.isupper() and len(token) > 12:
                continue
            counts[token] += 1
    out: list[str] = []
    for token, _ in counts.most_common():
        if token not in out:
            out.append(token)
        if len(out) >= limit:
            break
    return out


def title_tokens(chapter_title: str, limit: int = 6) -> list[str]:
    raw = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", chapter_title)
    out: list[str] = []
    for token in raw:
        low = token.lower()
        if low in STOPWORDS:
            continue
        if token.lower().startswith("chapter"):
            continue
        if token.isdigit():
            continue
        out.append(token)
        if len(out) >= limit:
            break
    return out


def domain_label(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or url


def build_problem_body(
    chapter_title: str,
    tutorial_title: str,
    identifiers: list[str],
    fallback_terms: list[str],
) -> str:
    id_terms = identifiers if identifiers else fallback_terms
    focus = ", ".join(f"`{x}`" for x in id_terms[:3]) if id_terms else "core abstractions in this chapter"
    ops_terms = id_terms[3:6] if len(id_terms) > 3 else id_terms[:3]
    ops = ", ".join(f"`{x}`" for x in ops_terms) if ops_terms else "execution and reliability details"
    return f"""Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for {focus} so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `{chapter_title}` as an operating subsystem inside **{tutorial_title}**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around {ops} as your checklist when adapting these patterns to your own repository."""


def build_under_hood_body(
    chapter_title: str,
    identifiers: list[str],
    fallback_terms: list[str],
) -> str:
    terms = identifiers if identifiers else fallback_terms
    id_a = terms[0] if len(terms) > 0 else "control layer"
    id_b = terms[1] if len(terms) > 1 else "execution path"
    id_c = terms[2] if len(terms) > 2 else "state transitions"
    return f"""Under the hood, `{chapter_title}` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `{id_a}`.
2. **Input normalization**: shape incoming data so `{id_b}` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `{id_c}`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions."""


def build_source_walkthrough_body(
    source_refs: list[tuple[str, str]],
    identifiers: list[str],
    fallback_terms: list[str],
) -> str:
    lines = [
        "Use the following upstream sources to verify implementation details while reading this chapter:",
        "",
    ]
    for label, url in source_refs[:8]:
        lines.append(f"- [{label}]({url})")
        lines.append(f"  Why it matters: authoritative reference on `{label}` ({domain_label(url)}).")
    if not source_refs:
        lines.append("- No explicit source links were found in the tutorial index; trace the upstream repository README and docs first.")
    terms = identifiers if identifiers else fallback_terms
    if terms:
        lines.extend(
            [
                "",
                "Suggested trace strategy:",
                f"- search upstream code for `{terms[0]}` and `{terms[min(1, len(terms)-1)]}` to map concrete implementation paths",
                "- compare docs claims against actual runtime/config code before reusing patterns in production",
            ]
        )
    return "\n".join(lines).strip()


def should_replace_problem(body: str) -> bool:
    return (GENERIC_PROBLEM_HINT in body) or len(body.splitlines()) <= 8


def should_replace_under_hood(body: str) -> bool:
    return (GENERIC_UNDER_HOOD_HINT in body) or len(body.splitlines()) <= 8


def should_replace_source(body: str) -> bool:
    if any(part in body for part in IGNORED_SOURCE_URL_PARTS):
        return True
    return (GENERIC_SOURCE_HINT in body) or len(body.splitlines()) <= 4


def process_chapter(
    chapter_path: Path,
    tutorial_title: str,
    source_refs: list[tuple[str, str]],
) -> bool:
    text = read_text(chapter_path)
    chapter_title = first_h1(text) or slug_phrase(chapter_path.stem).title()
    identifiers = top_identifiers(text, limit=6)
    fallback_terms = title_tokens(chapter_title, limit=6)
    changed_any = False

    problem_body = extract_section_body(text, "What Problem Does This Solve?")
    if problem_body and should_replace_problem(problem_body):
        new_problem = build_problem_body(chapter_title, tutorial_title, identifiers, fallback_terms)
        text, changed = replace_section_body(text, "What Problem Does This Solve?", new_problem)
        changed_any = changed_any or changed

    under_body = extract_section_body(text, "How it Works Under the Hood")
    if under_body and should_replace_under_hood(under_body):
        new_under = build_under_hood_body(chapter_title, identifiers, fallback_terms)
        text, changed = replace_section_body(text, "How it Works Under the Hood", new_under)
        changed_any = changed_any or changed

    source_body = extract_section_body(text, "Source Walkthrough")
    if source_body and should_replace_source(source_body):
        new_source = build_source_walkthrough_body(source_refs, identifiers, fallback_terms)
        text, changed = replace_section_body(text, "Source Walkthrough", new_source)
        changed_any = changed_any or changed

    if changed_any:
        write_text(chapter_path, text)
    return changed_any


def main() -> int:
    parser = argparse.ArgumentParser(description="Contextualize generic chapter sections")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    tutorials_root = root / "tutorials"

    chapter_total = 0
    chapter_changed = 0

    for tutorial_dir in sorted(p for p in tutorials_root.iterdir() if p.is_dir()):
        index_path = tutorial_dir / "index.md"
        if not index_path.is_file():
            continue
        index_text = read_text(index_path)
        tutorial_title = first_h1(index_text) or slug_phrase(tutorial_dir.name).title()
        source_refs = extract_source_refs(index_text, limit=8)

        for chapter_path in chapter_files(tutorial_dir):
            chapter_total += 1
            if process_chapter(chapter_path, tutorial_title, source_refs):
                chapter_changed += 1

    print(f"chapter_total={chapter_total}")
    print(f"chapter_changed={chapter_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
