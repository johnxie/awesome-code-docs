# Tutorial Structure Standard

This file defines the canonical tutorial layout and current structure status.

## Canonical Layout (Target)

```text
tutorials/<tutorial-name>/
  index.md
  01-*.md
  02-*.md
  ...
  08-*.md
```

## Current Structure Snapshot (auto-generated)

| Pattern | Count |
|:--------|:------|
| `root_only` | 127 |
| `docs_only` | 0 |
| `index_only` | 0 |
| `mixed` | 0 |

## Policy

1. New tutorials should use the canonical top-level chapter layout.
2. Existing tutorials should avoid introducing new `docs/` chapter structures.
3. Index files must not contain dead local links.
4. Placeholder index summaries are disallowed.
5. Structural and link health are enforced by CI (`Docs Health` workflow).

## Migration Approach

1. Keep tutorial indexes aligned with published chapter reality.
2. Maintain canonical naming for new chapter files (`01-...md` to `08-...md`).
3. Regenerate machine-readable artifacts after structural/content updates:
   - `tutorials/tutorial-manifest.json`
   - discoverability assets (`discoverability/tutorial-index.json`, `llms.txt`, etc.)
4. Re-run docs health checks before merge.
