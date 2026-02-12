---
layout: default
title: "Chapter 2: Input Parsing and Resolution Pipeline"
nav_order: 2
parent: OpenSrc Tutorial
---

# Chapter 2: Input Parsing and Resolution Pipeline

OpenSrc routes each input through parsing logic that determines whether it is a package spec or a direct repository spec.

## Input Types

| Input | Interpreted As | Example |
|:------|:---------------|:--------|
| npm package | package | `zod`, `react@19.0.0` |
| prefixed package | package | `pypi:requests`, `crates:serde` |
| owner/repo | git repository | `facebook/react` |
| host-prefixed repo | git repository | `gitlab:owner/repo` |
| URL | git repository | `https://github.com/vercel/ai` |

## Detection Rules

- explicit registry prefixes force package mode
- repo-like patterns (`owner/repo`, URLs, host prefixes) route to repo mode
- scoped npm packages (starting with `@`) stay in package mode

## Source References

- [Input parser and registry detection](https://github.com/vercel-labs/opensrc/blob/main/src/lib/registries/index.ts)
- [Repo parsing and host support](https://github.com/vercel-labs/opensrc/blob/main/src/lib/repo.ts)

## Summary

You now understand how OpenSrc classifies and routes each input before fetching.

Next: [Chapter 3: Multi-Registry Package Fetching](03-multi-registry-package-fetching.md)
