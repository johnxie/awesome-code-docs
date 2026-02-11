---
layout: default
title: "Chapter 4: Tools, Permissions, and Execution"
nav_order: 4
parent: OpenCode Tutorial
---

# Chapter 4: Tools, Permissions, and Execution

The tool layer determines whether OpenCode is safe and reliable in real repositories.

## Execution Safety Model

| Layer | Control |
|:------|:--------|
| command scope | allowlist or reviewed command boundaries |
| file edits | review before apply |
| high-risk ops | explicit confirmation |
| audit trail | structured log of actions |

## Best Practices

- keep destructive operations behind explicit review
- treat shell commands as privileged actions
- enforce small, reversible edit batches
- run tests/lint after non-trivial patches

## Team Policy Pattern

1. define approved command families
2. require review for package and infra changes
3. log all executed operations in CI contexts
4. rotate credentials and avoid implicit env leakage

## Source References

- [OpenCode Agents Docs](https://opencode.ai/docs/agents)
- [OpenCode README](https://github.com/anomalyco/opencode/blob/dev/README.md)

## Summary

You now have a practical safety baseline for running OpenCode against important codebases.

Next: [Chapter 5: Agents, Subagents, and Planning](05-agents-subagents-and-planning.md)
