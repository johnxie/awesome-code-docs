---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Kimi CLI Tutorial
---

# Chapter 1: Getting Started

This chapter gets Kimi CLI installed, configured, and running in a project directory.

## Quick Install

```bash
# Linux / macOS
curl -LsSf https://code.kimi.com/install.sh | bash

# Verify
kimi --version
```

Alternative install with `uv`:

```bash
uv tool install --python 3.13 kimi-cli
```

## First Run

```bash
cd your-project
kimi
```

Then run `/login` to configure provider access.

## Source References

- [Kimi Getting Started](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/guides/getting-started.md)

## Summary

You now have Kimi CLI running with authenticated provider access.

Next: [Chapter 2: Command Surface and Session Controls](02-command-surface-and-session-controls.md)
