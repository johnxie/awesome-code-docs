---
layout: default
title: "Chapter 3: Multi-Registry Package Fetching"
nav_order: 3
parent: OpenSrc Tutorial
---

# Chapter 3: Multi-Registry Package Fetching

OpenSrc supports package resolution across npm, PyPI, and crates.io using registry-specific metadata paths.

## Registry Coverage

| Registry | Prefix | Resolution Source |
|:---------|:-------|:------------------|
| npm | `npm:` (optional) | npm registry metadata |
| PyPI | `pypi:` / `pip:` / `python:` | PyPI JSON API |
| crates.io | `crates:` / `cargo:` / `rust:` | crates.io API |

## Resolution Behavior

- resolves repository URL from package metadata
- attempts version-aware cloning behavior
- tracks fetched outputs in a unified local index

## Example Commands

```bash
opensrc npm:zod
opensrc pypi:requests
opensrc crates:serde
```

## Source References

- [npm resolver](https://github.com/vercel-labs/opensrc/blob/main/src/lib/registries/npm.ts)
- [PyPI resolver](https://github.com/vercel-labs/opensrc/blob/main/src/lib/registries/pypi.ts)
- [crates resolver](https://github.com/vercel-labs/opensrc/blob/main/src/lib/registries/crates.ts)

## Summary

You now have a model for how OpenSrc maps package ecosystems to repository source retrieval.

Next: [Chapter 4: Git Repository Source Imports](04-git-repository-source-imports.md)
