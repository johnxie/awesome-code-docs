---
layout: default
title: "Chapter 5: Checkpoints and Recovery"
nav_order: 5
parent: Roo Code Tutorial
---

# Chapter 5: Checkpoints and Recovery

Checkpoint workflows make autonomous experimentation safer.

## Checkpoint Pattern

- snapshot workspace before risky edits
- compare output against checkpoint state
- restore quickly when changes regress behavior

## Use Cases

- trying alternative implementation strategies
- testing aggressive refactors
- recovering from prompt overreach

## Recovery Rules

| Rule | Why |
|:-----|:----|
| checkpoint before multi-file edits | fast rollback |
| annotate checkpoints with intent | easier comparison |
| restore with validation rerun | confirm clean recovery |

## Summary

You now have a controlled rollback strategy for agent-assisted development.

Next: [Chapter 6: MCP and Tool Extensions](06-mcp-and-tool-extensions.md)
