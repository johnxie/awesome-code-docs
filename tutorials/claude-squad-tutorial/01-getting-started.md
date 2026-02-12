---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Claude Squad Tutorial
---

# Chapter 1: Getting Started

This chapter gets Claude Squad installed and ready for your first multi-session run.

## Install

```bash
brew install claude-squad
ln -s "$(brew --prefix)/bin/claude-squad" "$(brew --prefix)/bin/cs"
```

Alternative manual install:

```bash
curl -fsSL https://raw.githubusercontent.com/smtg-ai/claude-squad/main/install.sh | bash
```

## Prerequisites

- `tmux`
- `gh` (GitHub CLI)

## Launch

```bash
cs
```

## Source References

- [Claude Squad README](https://github.com/smtg-ai/claude-squad/blob/main/README.md)

## Summary

You now have Claude Squad installed with prerequisites for multi-session execution.

Next: [Chapter 2: tmux and Worktree Architecture](02-tmux-and-worktree-architecture.md)
