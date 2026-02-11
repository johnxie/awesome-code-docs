---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: OpenCode Tutorial
---

# Chapter 1: Getting Started

This chapter gets OpenCode running and establishes a clean baseline for deeper customization.

## Learning Goals

- install OpenCode using your preferred package path
- validate local model/provider connectivity
- run first tasks in terminal agent mode
- understand the difference between `build` and `plan` modes

## Installation Paths

| Path | Command | Best For |
|:-----|:--------|:---------|
| install script | `curl -fsSL https://opencode.ai/install | bash` | fastest bootstrap |
| npm | `npm i -g opencode-ai@latest` | Node-centric environments |
| Homebrew | `brew install anomalyco/tap/opencode` | macOS/Linux package-managed setup |

## First Run Checklist

1. launch `opencode`
2. confirm provider credentials are available
3. run a simple repo analysis task
4. switch between `build` and `plan` modes
5. verify output and suggested edits are coherent

## Early Failure Triage

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| no model responses | missing provider credentials | configure provider key and retry |
| unsafe command concerns | wrong agent mode for task | use `plan` mode for analysis-first sessions |
| poor repo understanding | insufficient context scope | add clearer task framing and target files |

## Source References

- [OpenCode README](https://github.com/anomalyco/opencode/blob/dev/README.md)
- [OpenCode Install Docs](https://opencode.ai/docs)

## Summary

You now have OpenCode installed and validated for day-to-day terminal workflows.

Next: [Chapter 2: Architecture and Agent Loop](02-architecture-agent-loop.md)
