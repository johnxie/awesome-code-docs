---
layout: default
title: "Chapter 4: Codebase Indexing and Context Retrieval"
nav_order: 4
parent: Shotgun Tutorial
---

# Chapter 4: Codebase Indexing and Context Retrieval

Shotgun builds a local code graph so agent outputs are grounded in actual repository structure.

## Indexing Workflow

1. ingest repository files
2. build searchable code relationships
3. use the graph during research/spec/planning phases

## Why It Improves Output

- reduces hallucinated project structure
- improves dependency awareness before edits
- helps break large work into staged PRs

## Privacy Posture

Shotgun docs emphasize local indexing storage and no code upload during indexing itself.

## Source References

- [Shotgun README: code graph behavior](https://github.com/shotgun-sh/shotgun#faq)
- [CLI codebase commands](https://github.com/shotgun-sh/shotgun/blob/main/docs/CLI.md)

## Summary

You now understand how codebase indexing improves planning and reduces execution drift.

Next: [Chapter 5: CLI Automation and Scripting](05-cli-automation-and-scripting.md)
