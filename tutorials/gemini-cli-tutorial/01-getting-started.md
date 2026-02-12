---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Gemini CLI Tutorial
---

# Chapter 1: Getting Started

This chapter gets Gemini CLI running quickly and validates first successful interactions.

## Learning Goals

- install Gemini CLI with the fastest path for your environment
- launch the CLI and complete initial auth
- run first interactive and headless prompts
- confirm baseline command and model behavior

## Quick Install Paths

```bash
npx @google/gemini-cli
# or
npm install -g @google/gemini-cli
# or
brew install gemini-cli
```

Minimum prerequisites:

- Node.js 20+
- macOS, Linux, or Windows

## First-Run Validation

1. Start interactive mode:

```bash
gemini
```

2. Run a simple headless prompt:

```bash
gemini -p "Summarize this repository architecture"
```

3. Run structured output mode:

```bash
gemini -p "List top risks in this codebase" --output-format json
```

## Baseline Checks

- auth prompt completes successfully
- tool-enabled response includes actionable output
- no startup errors in current working directory

## Source References

- [README Installation](https://github.com/google-gemini/gemini-cli/blob/main/README.md#-installation)
- [Get Started Installation Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/installation.md)
- [Headless Mode Docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md)

## Summary

You now have a working Gemini CLI baseline for both interactive and scripted usage.

Next: [Chapter 2: Architecture, Tools, and Agent Loop](02-architecture-tools-and-agent-loop.md)
