---
layout: default
title: "Chapter 6: Shell Mode, Print Mode, and Wire Mode"
nav_order: 6
parent: Kimi CLI Tutorial
---

# Chapter 6: Shell Mode, Print Mode, and Wire Mode

Kimi offers multiple operating modes optimized for interactive coding, automation, or protocol-level integration.

## Mode Matrix

| Mode | Best For |
|:-----|:---------|
| default shell mode | interactive development with approvals |
| `--print` | non-interactive scripting pipelines |
| `--wire` | custom UIs and bidirectional protocol integrations |

## Automation Shortcut

```bash
kimi --quiet -p "Generate a Conventional Commits message for staged diff"
```

## Source References

- [Print mode docs](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/print-mode.md)
- [Wire mode docs](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/wire-mode.md)

## Summary

You now know when to use interactive mode versus automation/protocol modes.

Next: [Chapter 7: Loop Control, Retries, and Long Tasks](07-loop-control-retries-and-long-tasks.md)
