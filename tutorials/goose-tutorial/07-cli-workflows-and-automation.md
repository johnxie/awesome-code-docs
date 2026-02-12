---
layout: default
title: "Chapter 7: CLI Workflows and Automation"
nav_order: 7
parent: Goose Tutorial
---

# Chapter 7: CLI Workflows and Automation

This chapter focuses on making Goose reliable inside repeatable terminal workflows.

## Learning Goals

- use Goose CLI commands with predictable flag patterns
- embed Goose into scripted engineering loops
- standardize diagnostics and update flows
- improve reproducibility across developer machines

## Core Commands to Operationalize

| Command | Purpose |
|:--------|:--------|
| `goose configure` | provider, extensions, and settings setup |
| `goose info` | inspect version and runtime config locations |
| `goose session` | interactive session in terminal |
| `goose run` | headless/task automation mode |
| `goose update` | upgrade to stable/canary builds |
| `goose completion zsh` | shell completion for faster operation |

## Automation Pattern

1. pin install/update strategy
2. verify provider credentials at runtime
3. run bounded task with max-turn controls
4. collect logs and outputs for review
5. fail fast on permission or tool-surface mismatch

## Troubleshooting Baseline

- run `goose info` during incident triage
- inspect logs before retry loops
- ensure command flags use current naming conventions

## Source References

- [Goose CLI Commands](https://block.github.io/goose/docs/guides/goose-cli-commands)
- [Updating goose](https://block.github.io/goose/docs/guides/updating-goose)
- [Diagnostics and Reporting](https://block.github.io/goose/docs/troubleshooting/diagnostics-and-reporting)

## Summary

You now have a production-friendly CLI operating model for Goose automation.

Next: [Chapter 8: Production Operations and Security](08-production-operations-and-security.md)
