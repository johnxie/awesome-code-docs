# Tutorials Workspace Guide

Use this guide to navigate all tutorial tracks, understand structure rules, and jump to the right discovery surface quickly.

## Primary Entry Points

- Main catalog and learning paths: [../README.md](../README.md)
- A-Z tutorial directory: [../discoverability/tutorial-directory.md](../discoverability/tutorial-directory.md)
- Intent-based discovery: [../discoverability/query-hub.md](../discoverability/query-hub.md)
- Search intent mapping: [../discoverability/search-intent-map.md](../discoverability/search-intent-map.md)
- Contribution workflow: [../CONTRIBUTING.md](../CONTRIBUTING.md)

## Snapshot (auto-generated)

| Metric | Value |
|:-------|:------|
| Tutorial directories | 188 |
| Tutorial markdown files | 1705 |
| Tutorial markdown lines | 996,885 |

## Source Verification Snapshot

Repository-source verification run against tutorial index references (GitHub API, 2026-02-24):

| Signal | Value |
|:-------|------:|
| Tutorials scanned | 188 |
| Tutorials with source repos | 188 |
| Tutorials with unverified source repos | 0 |
| Unique verified source repos | 199 |

- Report: [../discoverability/tutorial-source-verification.md](../discoverability/tutorial-source-verification.md)
- JSON: [../discoverability/tutorial-source-verification.json](../discoverability/tutorial-source-verification.json)
- Script: [../scripts/verify_tutorial_sources.py](../scripts/verify_tutorial_sources.py)

## Content Structure Patterns

| Pattern | Count | Description |
|:--------|:------|:------------|
| Root chapter files | 188 | `index.md` + top-level `01-...md` to `08-...md` |
| `docs/` chapter files | 0 | Deprecated and fully migrated |
| Index-only roadmap | 0 | All catalog entries publish full chapter sets |
| Mixed root + `docs/` | 0 | Legacy hybrid layout removed |

## Tutorial UX Contract

Each tutorial index should provide:

- a clear chapter guide with direct links
- source references to upstream docs/repos
- related tutorial links for cross-track navigation
- a **Navigation & Backlinks** section to connect back to core discovery surfaces

## Structure Contract

Each tutorial directory should contain:

- `index.md`
- `01-...md` through `08-...md` at the tutorial root (not under `docs/`)

## Maintainer Commands

```bash
# Refresh tutorial metrics and structure snapshot
python3 scripts/update_tutorials_readme_snapshot.py --root .

# Re-verify tutorial source repositories
python3 scripts/verify_tutorial_sources.py --root .

# Run docs health checks
python3 scripts/docs_health.py --root .
```

## Quick Actions

- Browse all tutorials: [../README.md#-tutorial-catalog](../README.md#-tutorial-catalog)
- Explore category hubs: [../README.md#category-hubs](../README.md#category-hubs)
- Open new tutorial request: <https://github.com/johnxie/awesome-code-docs/issues/new?template=new-entry.md>
