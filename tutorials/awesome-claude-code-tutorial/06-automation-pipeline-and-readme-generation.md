---
layout: default
title: "Chapter 6: Automation Pipeline and README Generation"
nav_order: 6
parent: Awesome Claude Code Tutorial
---

# Chapter 6: Automation Pipeline and README Generation

This chapter explains how the repository stays maintainable as resource volume grows.

## Learning Goals

- understand the single-source-of-truth model
- know which commands regenerate list views and assets
- validate that generated outputs remain deterministic
- avoid accidental drift between source data and rendered docs

## Pipeline Core

- `THE_RESOURCES_TABLE.csv` is the source of truth
- `make generate` sorts data and regenerates README views/assets
- style-specific generators produce multiple README variants
- docs tree and regeneration checks protect maintainability

## High-Value Maintainer Commands

```bash
make generate
make validate
make test
make ci
make docs-tree-check
make test-regenerate
```

## Source References

- [README Generation Guide](https://github.com/hesreallyhim/awesome-claude-code/blob/main/docs/README-GENERATION.md)
- [Makefile](https://github.com/hesreallyhim/awesome-claude-code/blob/main/Makefile)
- [Generator Entrypoint](https://github.com/hesreallyhim/awesome-claude-code/blob/main/scripts/readme/generate_readme.py)

## Summary

You now understand the maintenance pipeline that keeps the list coherent at scale.

Next: [Chapter 7: Link Health, Validation, and Drift Control](07-link-health-validation-and-drift-control.md)
