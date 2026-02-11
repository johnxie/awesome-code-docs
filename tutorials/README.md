# Tutorial Directory Guide

This file describes the structure of `tutorials/` and points to the authoritative catalog.

## Source of Truth

- Full catalog and learning paths: [../README.md](../README.md)
- Contribution guidelines: [../CONTRIBUTING.md](../CONTRIBUTING.md)

## Snapshot (February 11, 2026)

| Metric | Value |
|:-------|:------|
| Tutorial directories | 91 |
| Tutorial markdown files | 753 |
| Tutorial markdown lines | 440,098 |

## Content Structure Patterns

| Pattern | Count | Description |
|:--------|:------|:------------|
| Root chapter files | 75 | `index.md` + top-level `01-...md` to `08-...md` |
| `docs/` chapter files | 8 | `index.md` with chapter files under `docs/` |
| Index-only roadmap | 7 | `index.md` exists, chapter files not yet published |
| Mixed root + `docs/` | 1 | Hybrid layout (legacy) |

## Why This Exists

The repository has grown quickly, and tutorial folders currently use multiple historical structures. This file helps contributors navigate those patterns while the project converges on stricter validation and consistency checks.

## Quick Navigation

- Browse all tutorials: [../README.md#-tutorial-catalog](../README.md#-tutorial-catalog)
- Start a new tutorial proposal: <https://github.com/johnxie/awesome-code-docs/issues/new?template=new-entry.md>
