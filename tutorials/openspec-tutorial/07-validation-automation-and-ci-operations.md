---
layout: default
title: "Chapter 7: Validation, Automation, and CI Operations"
nav_order: 7
parent: OpenSpec Tutorial
---

# Chapter 7: Validation, Automation, and CI Operations

This chapter focuses on quality gates so OpenSpec artifacts remain trusted inputs to implementation.

## Learning Goals

- apply validation commands in local and CI contexts
- use JSON outputs for automation pipelines
- prevent broken artifact states from reaching merge

## Core Validation Commands

```bash
openspec validate --all
openspec status
openspec instructions proposal --change <name>
```

For automation pipelines:

```bash
openspec validate --all --json
openspec status --json
```

## CI Gate Suggestions

| Gate | Purpose |
|:-----|:--------|
| artifact validation | catch malformed or inconsistent specs early |
| status checks | ensure no ambiguous lifecycle state before merge |
| implementation verification | detect mismatch between tasks and delivered behavior |

## Operating Pattern

1. run validation before `/opsx:archive`
2. enforce validation in pull request checks
3. keep artifacts updated with code changes in the same branch

## Source References

- [CLI Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)

## Summary

You now have an actionable quality-gate model for integrating OpenSpec into CI/CD.

Next: [Chapter 8: Migration, Governance, and Team Adoption](08-migration-governance-and-team-adoption.md)
