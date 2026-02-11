---
layout: default
title: "Chapter 5: Human Approval and High-Stakes Actions"
nav_order: 5
parent: HumanLayer Tutorial
---

# Chapter 5: Human Approval and High-Stakes Actions

High-stakes operations require deterministic human oversight, not best-effort prompts.

## Stake Model

| Stake Level | Example |
|:------------|:--------|
| low | public data reads |
| medium | private read access |
| high | write actions and external communication |

## Governance Pattern

- classify tool calls by stake level
- require approval for all high-stakes actions
- capture decision audit trails for compliance

## Source References

- [humanlayer.md](https://github.com/humanlayer/humanlayer/blob/main/humanlayer.md)

## Summary

You now have a practical approval framework for risky coding-agent operations.

Next: [Chapter 6: IDE and CLI Integration Patterns](06-ide-and-cli-integration-patterns.md)
