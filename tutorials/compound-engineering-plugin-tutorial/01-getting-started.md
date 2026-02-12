---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Compound Engineering Plugin Tutorial
---

# Chapter 1: Getting Started

This chapter gets the compound-engineering plugin installed and running in Claude Code.

## Learning Goals

- add the marketplace and install `compound-engineering`
- run the core workflow commands at least once
- verify generated behaviors align to documented flow
- understand initial setup requirements for team rollout

## Install Commands

```bash
/plugin marketplace add https://github.com/EveryInc/compound-engineering-plugin
/plugin install compound-engineering
```

## First-Run Validation

- run `/workflows:plan` on a small feature request
- run `/workflows:work` for scoped implementation
- run `/workflows:review` and inspect findings
- run `/workflows:compound` to capture reusable learnings

## Source References

- [Repository README Install](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md#claude-code-install)
- [Workflow Overview](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md#workflow)
- [Compound Plugin README](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md)

## Summary

You now have a working compound-engineering baseline in Claude Code.

Next: [Chapter 2: Compound Engineering Philosophy and Workflow Loop](02-compound-engineering-philosophy-and-workflow-loop.md)
