# Tutorial Directory Guide

This file describes the structure of `tutorials/` and points to the authoritative catalog.

## Source of Truth

- Full catalog and learning paths: [../README.md](../README.md)
- Contribution guidelines: [../CONTRIBUTING.md](../CONTRIBUTING.md)

## Snapshot (auto-generated)

| Metric | Value |
|:-------|:------|
| Tutorial directories | 96 |
| Tutorial markdown files | 877 |
| Tutorial markdown lines | 442,230 |

## Content Structure Patterns

| Pattern | Count | Description |
|:--------|:------|:------------|
| Root chapter files | 96 | `index.md` + top-level `01-...md` to `08-...md` |
| `docs/` chapter files | 0 | Deprecated and fully migrated |
| Index-only roadmap | 0 | All catalog entries publish full chapter sets |
| Mixed root + `docs/` | 0 | Legacy hybrid layout removed |

## Why This Exists

The repository now uses a single canonical tutorial structure. This file helps contributors keep that structure consistent and avoid reintroducing legacy layouts.

## Quick Navigation

- Browse all tutorials: [../README.md#-tutorial-catalog](../README.md#-tutorial-catalog)
- Start a new tutorial proposal: <https://github.com/johnxie/awesome-code-docs/issues/new?template=new-entry.md>

## Structure Contract

Each tutorial directory should contain:

- `index.md`
- `01-...md` through `08-...md` at the tutorial root (not under `docs/`)
