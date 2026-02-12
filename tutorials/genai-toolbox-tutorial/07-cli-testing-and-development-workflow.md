---
layout: default
title: "Chapter 7: CLI, Testing, and Development Workflow"
nav_order: 7
parent: GenAI Toolbox Tutorial
---

# Chapter 7: CLI, Testing, and Development Workflow

This chapter focuses on iterative development quality gates.

## Learning Goals

- use CLI flags and invoke helpers for fast validation
- run lint/unit/integration loops consistently
- align local test behavior with CI expectations
- keep naming/version conventions coherent across tool surfaces

## Engineering Loop

Treat `go run . --help`, direct tool invocation, and targeted tests as your shortest quality loop. Promote changes only after link, lint, and integration checks align.

## Source References

- [CLI Reference](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/reference/cli.md)
- [Developer Guide](https://github.com/googleapis/genai-toolbox/blob/main/DEVELOPER.md)
- [Contributing](https://github.com/googleapis/genai-toolbox/blob/main/CONTRIBUTING.md)

## Summary

You now have a repeatable workflow for shipping Toolbox changes with lower regression risk.

Next: [Chapter 8: Production Governance and Release Strategy](08-production-governance-and-release-strategy.md)
