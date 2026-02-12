---
layout: default
title: "Chapter 3: Interactive Workflow and Approval Model"
nav_order: 3
parent: GitHub Copilot CLI Tutorial
---

# Chapter 3: Interactive Workflow and Approval Model

Copilot CLI emphasizes user-in-the-loop execution: proposals are shown before actions are performed.

## Interaction Pattern

1. describe task in natural language
2. agent proposes tool/action steps
3. user reviews and approves execution
4. agent iterates with visible progress in session

## Why It Matters

- keeps risky commands and edits user-controlled
- makes terminal-agent behavior auditable
- improves confidence for refactors and production-impact changes

## Source References

- [Copilot CLI README: full control model](https://github.com/github/copilot-cli/blob/main/README.md)

## Summary

You now understand the approval-first interaction style that governs Copilot CLI execution.

Next: [Chapter 4: Models, Experimental Features, and Autopilot](04-models-experimental-features-and-autopilot.md)
