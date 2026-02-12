---
layout: default
title: "Chapter 3: Command Surface and Agent Workflows"
nav_order: 3
parent: OpenSpec Tutorial
---

# Chapter 3: Command Surface and Agent Workflows

This chapter separates human CLI operations from agent-facing commands so workflows stay predictable.

## Learning Goals

- distinguish terminal-oriented CLI commands from slash workflows
- decide when to use interactive vs non-interactive command paths
- reduce ambiguity in multi-agent environments

## Two Command Planes

| Plane | Examples | Typical Owner |
|:------|:---------|:--------------|
| OPSX slash commands | `/opsx:new`, `/opsx:apply`, `/opsx:archive` | coding agent interaction loop |
| CLI commands | `openspec list`, `openspec status`, `openspec validate` | human operators and CI scripts |

## Agent-Friendly CLI Operations

OpenSpec exposes structured outputs for automation:

```bash
openspec status --json
openspec validate --all --json
openspec list --json
```

## Reliability Practices

1. keep one active change focus per implementation thread
2. run `status` before and after `/opsx:apply`
3. use `validate` in CI before merge
4. treat archive as the final state transition, not a side effect

## Source References

- [Commands Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
- [CLI Reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)
- [OPSX Workflow](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)

## Summary

You now know how to coordinate human and agent command usage without workflow collisions.

Next: [Chapter 4: Spec Authoring, Delta Patterns, and Quality](04-spec-authoring-delta-patterns-and-quality.md)
