---
layout: default
title: "Chapter 8: Migration Strategy and Long-Term Operations"
nav_order: 8
parent: Sweep Tutorial
---

# Chapter 8: Migration Strategy and Long-Term Operations

The Sweep ecosystem has evolved over time. Teams need an explicit strategy to preserve value while adapting tooling.

## Learning Goals

- distinguish workflow assets worth preserving
- define migration criteria to adjacent agent platforms
- keep governance and auditability stable across transitions

## Preserve These Assets

| Asset | Why Preserve |
|:------|:-------------|
| issue prompt templates | reusable task decomposition patterns |
| `sweep.yaml` policy defaults | repository governance and safety constraints |
| PR review playbooks | consistent human quality control |

## Migration Planning Questions

1. which current workflows depend on GitHub issue automation?
2. what alternative agent surfaces are being adopted (IDE, CLI, browser)?
3. how will CI and review policy stay unchanged during tooling shifts?

## Source References

- [README](https://github.com/sweepai/sweep/blob/main/README.md)
- [Roadmap Notes](https://github.com/sweepai/sweep/blob/main/docs/pages/about/roadmap.mdx)
- [Contributing](https://github.com/sweepai/sweep/blob/main/CONTRIBUTING.md)

## Summary

You now have a long-term operating approach for using Sweep responsibly within a changing coding-agent landscape.

Next: compare adjacent architectures in [OpenCode](../opencode-tutorial/) and [Stagewise](../stagewise-tutorial/).
