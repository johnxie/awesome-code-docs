---
layout: default
title: "Chapter 2: Command Surface and Session Controls"
nav_order: 2
parent: Kimi CLI Tutorial
---

# Chapter 2: Command Surface and Session Controls

Kimi CLI exposes rich command-line controls for model selection, directories, sessions, and execution boundaries.

## High-Value Flags

| Flag | Purpose |
|:-----|:--------|
| `--model` | select active model |
| `--work-dir` | set workspace root |
| `--continue` / `--session` | resume prior sessions |
| `--max-steps-per-turn` | cap per-turn execution length |
| `--max-retries-per-step` | control retry behavior |
| `--yolo` | auto-approve operations |

## Session Control Basics

- resume most recent with `--continue`
- resume specific with `--session <id>`
- manage in runtime with `/sessions` or `/resume`

## Source References

- [Kimi command reference](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/reference/kimi-command.md)
- [Sessions and context guide](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/guides/sessions.md)

## Summary

You now understand the core startup/session controls for predictable Kimi workflows.

Next: [Chapter 3: Agents, Subagents, and Skills](03-agents-subagents-and-skills.md)
