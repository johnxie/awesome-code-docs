---
layout: default
title: "Chapter 5: Review, Checkout, and Push Workflow"
nav_order: 5
parent: Claude Squad Tutorial
---

# Chapter 5: Review, Checkout, and Push Workflow

Claude Squad emphasizes reviewing isolated changes before pushing them upstream.

## Built-In Workflow Actions

- review session diffs in the TUI
- checkout/pause session state when ready
- commit and push branch from session context

## Delivery Pattern

1. run task in isolated worktree
2. inspect diff and session output
3. commit/push only validated branch
4. merge through normal PR process

## Source References

- [Claude Squad README: review and push controls](https://github.com/smtg-ai/claude-squad/blob/main/README.md)

## Summary

You now have a branch-safe path from agent output to PR-ready changes.

Next: [Chapter 6: AutoYes, Daemon Polling, and Safety Controls](06-autoyes-daemon-polling-and-safety-controls.md)
