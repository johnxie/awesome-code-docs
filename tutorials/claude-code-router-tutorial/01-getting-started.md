---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Claude Code Router Tutorial
---

# Chapter 1: Getting Started

This chapter gets Claude Code Router installed with a minimal working configuration.

## Learning Goals

- install CLI and verify command availability
- initialize a valid `config.json` baseline
- route first Claude Code session through CCR
- verify service restart behavior after config changes

## Baseline Commands

```bash
npm install -g @musistudio/claude-code-router
ccr start
ccr code
```

## First Validation Checklist

- `ccr` commands available
- `~/.claude-code-router/config.json` exists and parses
- routing path works for at least one provider/model
- logs are being written in expected locations

## Source References

- [README: Getting Started](https://github.com/musistudio/claude-code-router/blob/main/README.md#getting-started)
- [CLI Intro](https://github.com/musistudio/claude-code-router/blob/main/docs/docs/cli/intro.md)

## Summary

You now have a working CCR baseline for deeper routing configuration.

Next: [Chapter 2: Architecture and Package Topology](02-architecture-and-package-topology.md)
