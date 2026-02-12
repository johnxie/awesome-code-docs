---
layout: default
title: "Chapter 7: Configuration and State Management"
nav_order: 7
parent: Claude Squad Tutorial
---

# Chapter 7: Configuration and State Management

Claude Squad keeps configuration and session artifacts in a dedicated user config directory.

## Configuration Model

- config dir: `~/.claude-squad`
- configurable defaults: program, branch prefix, AutoYes, polling interval
- session/worktree metadata persisted for lifecycle operations

## Team Practice

- standardize default program and branch prefix conventions
- document reset/recovery flow for corrupted local state
- keep config introspection in onboarding (`cs debug`)

## Source References

- [Config implementation](https://github.com/smtg-ai/claude-squad/blob/main/config/config.go)
- [Claude Squad README: debug command](https://github.com/smtg-ai/claude-squad/blob/main/README.md)

## Summary

You now have an operational model for Claude Squad configuration and local state behavior.

Next: [Chapter 8: Production Team Operations](08-production-team-operations.md)
