# PocketFlow-Inspired Tutorial Index Style (v2)

This style is inspired by the clarity and onboarding flow used in
`The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge`, adapted for
`awesome-code-docs`.

## Purpose

A tutorial index is the landing page for a track. In v2, the index must:

- orient the reader quickly
- establish source-backed trust
- explain the system mental model
- show a chapter roadmap at a glance
- make outcomes and references explicit

## Opt-In Contract

Add this to tutorial index frontmatter:

```yaml
format_version: v2
```

Any index that opts into `v2` is validated in CI by
`scripts/check_index_format_v2.py`.

## Required Section Set

Use headings that match the required section categories:

1. Why section
2. Current snapshot
3. Mental model
4. Chapter guide/map
5. Learning outcomes
6. Source references

Accepted heading variants are enforced by the validator script.

## Recommended Index Structure

```markdown
# <Tutorial Title>

> One-paragraph value proposition.

Badges...

## Why This Track Matters

Short context + problem framing.

## Current Snapshot (Verified <Month Day, Year>)

- repo
- stars
- release/version
- notable current-state details

## <Tool> Mental Model

Mermaid diagram that explains workflow boundaries.

## Chapter Guide

Markdown table mapping chapter -> key question -> outcome.

## What You Will Learn

Bullet list of concrete skills.

## Source References

Official repo/docs/release links only.

## Related Tutorials

Internal links to adjacent tracks.
```

## Writing Style Guidance

- Keep opening paragraphs practical and concrete.
- Prefer operational language over marketing language.
- Use tables for decision frameworks and chapter maps.
- Use one mental-model diagram on every v2 index.
- Include exact verification date in snapshot sections.

## Link and Accuracy Guidance

- Prefer primary sources (official docs/repos/releases).
- Avoid stale version claims without date context.
- Keep internal related links local and valid.
- Regenerate discoverability assets after index updates:
  - `python3 scripts/generate_discoverability_assets.py`
  - `python3 scripts/update_tutorials_readme_snapshot.py`
