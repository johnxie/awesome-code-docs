---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Goose Tutorial
---

# Chapter 1: Getting Started

This chapter establishes a clean Goose baseline so you can move into advanced workflows without setup drift.

## Learning Goals

- install Goose Desktop or CLI on your platform
- configure your first LLM provider
- run your first session in a target repository
- identify common startup failures and quick fixes

## Installation Paths

| Path | Command / Flow | Best For |
|:-----|:---------------|:---------|
| Desktop app | Download from Goose releases and launch | Visual workflows and session management in UI |
| CLI install script | `curl -fsSL https://github.com/block/goose/releases/download/stable/download_cli.sh \| bash` | Fast terminal bootstrap |
| Homebrew CLI | `brew install block-goose-cli` | macOS/Linux environments using package managers |

## First Configuration Checklist

1. run `goose configure`
2. select a provider and authenticate
3. choose a model suitable for tool calling
4. start a session from your working directory
5. run a low-risk task (for example, repo summary + TODO extraction)

## First Session Flow

```bash
cd /path/to/repo
goose session
```

Inside the session, start with a scoped prompt such as:

- "Summarize this repo structure and propose a 3-step refactor plan."

## Early Failure Triage

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| no model response | provider not configured correctly | rerun `goose configure` and re-authenticate |
| tool calls fail unexpectedly | permission mode mismatch | switch mode or adjust per-tool permissions |
| noisy or irrelevant context | wrong working directory | restart session from repo root |

## Source References

- [Goose Quickstart](https://block.github.io/goose/docs/quickstart)
- [Install goose](https://block.github.io/goose/docs/getting-started/installation)
- [Configure LLM Provider](https://block.github.io/goose/docs/getting-started/providers)

## Summary

You now have Goose installed, configured, and running in a real project context.

Next: [Chapter 2: Architecture and Agent Loop](02-architecture-and-agent-loop.md)
