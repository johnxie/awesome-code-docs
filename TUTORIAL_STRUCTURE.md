# Tutorial Structure Standard

This repository currently contains multiple historical tutorial layouts. The goal is to converge on one canonical layout while keeping existing content navigable.

## Canonical Layout (Target)

```text
tutorials/<tutorial-name>/
  index.md
  01-*.md
  02-*.md
  ...
  08-*.md
```

## Legacy Layouts Still Present

- `docs_only`: chapter files live under `docs/`
- `index_only`: roadmap `index.md` exists, chapter files not yet published
- `mixed`: both top-level chapter files and `docs/` chapter files

## Policy

1. New tutorials should use the canonical top-level chapter layout.
2. Existing tutorials can remain on legacy layouts until migrated.
3. Index files must not contain dead local links.
4. Structural and link health are enforced by CI (`Docs Health` workflow).

## Migration Approach

1. Fix index navigation first.
2. Ensure README matches published chapter reality.
3. Move or publish chapter files in canonical order.
4. Regenerate `tutorials/tutorial-manifest.json` after structural changes.
