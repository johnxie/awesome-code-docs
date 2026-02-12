---
layout: default
title: "Chapter 4: Permissions and Tool Governance"
nav_order: 4
parent: Goose Tutorial
---

# Chapter 4: Permissions and Tool Governance

This chapter covers the controls that separate fast automation from unsafe automation.

## Learning Goals

- choose the right Goose permission mode for each task class
- configure per-tool controls for sensitive operations
- reduce unnecessary tool surface to improve safety and quality
- enforce extension policy in constrained environments

## Permission Modes

| Mode | Behavior | Best For |
|:-----|:---------|:---------|
| Completely Autonomous | executes changes and tools without approval prompts | trusted local prototyping |
| Manual Approval | asks before tool actions | high-control sessions |
| Smart Approval | risk-based approvals | balanced day-to-day workflows |
| Chat Only | no tool execution | analysis-only tasks |

## Tool Governance Practices

1. prefer `Manual` or `Smart` for production repositories
2. explicitly deny destructive tools where not needed
3. keep active tool set small to reduce model confusion
4. use `.gooseignore` to exclude sensitive or noisy paths

## Corporate Policy Control

For restricted environments, Goose can enforce extension allowlists via `GOOSE_ALLOWLIST` and a hosted YAML allowlist policy.

## Source References

- [goose Permission Modes](https://block.github.io/goose/docs/guides/goose-permissions)
- [Managing Tool Permissions](https://block.github.io/goose/docs/guides/managing-tools/tool-permissions)
- [goose Extension Allowlist](https://block.github.io/goose/docs/guides/allowlist)
- [Using .gooseignore](https://block.github.io/goose/docs/guides/using-gooseignore)

## Summary

You now have a concrete security-control model for tool execution in Goose.

Next: [Chapter 5: Sessions and Context Management](05-sessions-and-context-management.md)
