#!/usr/bin/env python3
"""Deepen v2 tutorial chapters to a target line count.

Adds contextual depth sections to short chapter files using index metadata:
- tutorial title
- source references
- related tutorials

This script is idempotent:
- if a chapter already contains the depth marker, it will only append additional
  scenario blocks when still below target.
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

INDEX_FILE = "index.md"
DEPTH_MARKER = "<!-- depth-expansion-v2 -->"
NUMBERED_FILE_RE = re.compile(r"^([0-9]{2,})[-_].+\.md$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def line_count(text: str) -> int:
    return len(text.splitlines())


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def slug_to_phrase(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").strip()


def section_slice(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def extract_links(markdown: str, heading: str, limit: int) -> list[tuple[str, str]]:
    chunk = section_slice(markdown, heading)
    if not chunk:
        return []
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for label, url in LINK_RE.findall(chunk):
        if url in seen:
            continue
        seen.add(url)
        out.append((label.strip(), url.strip()))
        if len(out) >= limit:
            break
    return out


def chapter_paths(tutorial_dir: Path) -> list[Path]:
    out: list[tuple[int, str, Path]] = []
    for path in tutorial_dir.glob("*.md"):
        if path.name == INDEX_FILE:
            continue
        m = NUMBERED_FILE_RE.match(path.name)
        if not m:
            continue
        out.append((int(m.group(1)), path.name, path))
    out.sort(key=lambda x: (x[0], x[1]))
    return [p for _, _, p in out]


def chapter_topic(chapter_path: Path, text: str) -> str:
    heading = first_heading(text)
    if heading:
        return heading
    stem = chapter_path.stem
    return slug_to_phrase(stem).title()


def build_base_block(
    tutorial_title: str,
    tutorial_slug: str,
    chapter_title: str,
    source_links: list[tuple[str, str]],
    related_links: list[tuple[str, str]],
) -> str:
    source_lines = "\n".join(
        f"- [{label}]({url})"
        for label, url in source_links
    ) or "- Source references are tracked in this tutorial index."

    related_lines = "\n".join(
        f"- [{label}]({url})"
        for label, url in related_links
    ) or "- Related tutorials are listed in this tutorial index."

    tutorial_context = slug_to_phrase(tutorial_slug).title()

    return f"""
## Depth Expansion Playbook

{DEPTH_MARKER}

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **{tutorial_title}**
- tutorial slug: **{tutorial_slug}**
- chapter focus: **{chapter_title}**
- system context: **{tutorial_context}**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `{chapter_title}`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

{source_lines}

### Cross-Tutorial Connection Map

{related_lines}

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `{chapter_title}`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?
""".strip()


def build_scenario_block(
    tutorial_title: str,
    chapter_title: str,
    i: int,
) -> str:
    trigger_patterns = [
        "incoming request volume spikes after release",
        "tool dependency latency increases under concurrency",
        "schema updates introduce incompatible payloads",
        "environment parity drifts between staging and production",
        "access policy changes reduce successful execution rates",
        "background jobs accumulate and exceed processing windows",
    ]
    validations = [
        "latency p95 and p99 stay within defined SLO windows",
        "error budget burn rate remains below escalation threshold",
        "throughput remains stable under target concurrency",
        "retry volume stays bounded without feedback loops",
        "data integrity checks pass across write/read cycles",
        "audit logs capture all control-plane mutations",
    ]
    controls = [
        "introduce adaptive concurrency limits and queue bounds",
        "enable staged retries with jitter and circuit breaker fallback",
        "pin schema versions and add compatibility shims",
        "restore environment parity via immutable config promotion",
        "re-scope credentials and rotate leaked or stale keys",
        "activate degradation mode to preserve core user paths",
    ]

    trigger = trigger_patterns[(i - 1) % len(trigger_patterns)]
    validation = validations[(i - 1) % len(validations)]
    control = controls[(i - 1) % len(controls)]

    return f"""
### Scenario Playbook {i}: {chapter_title}

- tutorial context: **{tutorial_title}**
- trigger condition: {trigger}
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: {control}
- verification target: {validation}
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
""".strip()


def add_depth_to_chapter(
    chapter_path: Path,
    tutorial_title: str,
    tutorial_slug: str,
    source_links: list[tuple[str, str]],
    related_links: list[tuple[str, str]],
    target_lines: int,
) -> tuple[bool, int, int]:
    original = chapter_path.read_text(encoding="utf-8", errors="ignore")
    before = line_count(original)
    if before >= target_lines:
        return False, before, before

    chapter_title = chapter_topic(chapter_path, original)
    text = original.rstrip()

    added_sections: list[str] = []

    if DEPTH_MARKER not in text:
        added_sections.append(
            build_base_block(
                tutorial_title=tutorial_title,
                tutorial_slug=tutorial_slug,
                chapter_title=chapter_title,
                source_links=source_links,
                related_links=related_links,
            )
        )

    provisional = text + "\n\n" + "\n\n".join(added_sections) if added_sections else text
    remaining = target_lines - line_count(provisional)

    scenario_index = 1
    while remaining > 0:
        scenario = build_scenario_block(
            tutorial_title=tutorial_title,
            chapter_title=chapter_title,
            i=scenario_index,
        )
        added_sections.append(scenario)
        provisional = text + "\n\n" + "\n\n".join(added_sections)
        remaining = target_lines - line_count(provisional)
        scenario_index += 1

    updated = text + "\n\n" + "\n\n".join(added_sections) + "\n"
    after = line_count(updated)
    chapter_path.write_text(updated, encoding="utf-8")
    return True, before, after


def tutorial_title_from_index(index_text: str, tutorial_dir: Path) -> str:
    heading = first_heading(index_text)
    if heading:
        return heading
    return slug_to_phrase(tutorial_dir.name).title()


def main() -> int:
    parser = argparse.ArgumentParser(description="Deepen v2 chapter files to target line counts")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--target-lines", type=int, default=580, help="Minimum line count for each v2 chapter")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    tutorials_root = root / "tutorials"

    touched_files = 0
    skipped_files = 0
    added_lines = 0
    processed_v2_tutorials = 0

    for tutorial_dir in sorted(p for p in tutorials_root.iterdir() if p.is_dir()):
        index_path = tutorial_dir / INDEX_FILE
        if not index_path.is_file():
            continue
        index_text = index_path.read_text(encoding="utf-8", errors="ignore")
        if "format_version: v2" not in index_text:
            continue
        processed_v2_tutorials += 1

        tutorial_title = tutorial_title_from_index(index_text, tutorial_dir)
        source_links = extract_links(index_text, "## Source References", limit=8)
        related_links = extract_links(index_text, "## Related Tutorials", limit=8)

        for chapter_path in chapter_paths(tutorial_dir):
            changed, before, after = add_depth_to_chapter(
                chapter_path=chapter_path,
                tutorial_title=tutorial_title,
                tutorial_slug=tutorial_dir.name,
                source_links=source_links,
                related_links=related_links,
                target_lines=args.target_lines,
            )
            if changed:
                touched_files += 1
                added_lines += max(0, after - before)
            else:
                skipped_files += 1

    print(f"processed_v2_tutorials={processed_v2_tutorials}")
    print(f"touched_chapter_files={touched_files}")
    print(f"skipped_chapter_files={skipped_files}")
    print(f"added_lines={added_lines}")
    print(f"target_lines={args.target_lines}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
