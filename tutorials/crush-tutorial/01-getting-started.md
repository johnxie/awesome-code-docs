---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Crush Tutorial
---

# Chapter 1: Getting Started

This chapter gets Crush installed and ready for real coding work in minutes.

## Learning Goals

- install Crush using your preferred platform path
- authenticate a provider and run first prompt
- validate session baseline in a local project
- fix common startup misconfigurations quickly

## Installation Paths

| Path | Command | Best For |
|:-----|:--------|:---------|
| Homebrew | `brew install charmbracelet/tap/crush` | macOS/Linux package-managed setup |
| NPM | `npm install -g @charmland/crush` | Node-centric environments |
| Winget | `winget install charmbracelet.crush` | Windows environments |
| Go install | `go install github.com/charmbracelet/crush@latest` | Go-native toolchain users |

## First Run Checklist

1. launch `crush`
2. configure provider credentials when prompted (or set env vars first)
3. open a project directory and ask for a scoped code task
4. verify tool calls and file operations behave as expected

## Quick Environment Baseline

```bash
export ANTHROPIC_API_KEY=...
# or OPENAI_API_KEY, OPENROUTER_API_KEY, etc.
crush
```

## Common Startup Issues

| Symptom | Cause | First Fix |
|:--------|:------|:----------|
| provider not available | missing env var | set provider key and restart Crush |
| unstable output quality | model mismatch for coding tasks | switch to coding-optimized model |
| unexpected filesystem actions | loose permissions/tool policy | set explicit permission controls in config |

## Source References

- [Crush README](https://github.com/charmbracelet/crush/blob/main/README.md#installation)
- [Getting Started section](https://github.com/charmbracelet/crush/blob/main/README.md#getting-started)

## Summary

You now have Crush installed and running with a valid provider path.

Next: [Chapter 2: Architecture and Session Model](02-architecture-and-session-model.md)
