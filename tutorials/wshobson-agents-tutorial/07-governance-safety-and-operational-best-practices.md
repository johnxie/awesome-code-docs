---
layout: default
title: "Chapter 7: Governance, Safety, and Operational Best Practices"
nav_order: 7
parent: Wshobson Agents Tutorial
---

# Chapter 7: Governance, Safety, and Operational Best Practices

This chapter establishes team-level controls so plugin scale does not become operational chaos.

## Learning Goals

- define plugin governance for consistent team usage
- enforce quality/safety checks in automated workflows
- manage plugin drift and command-surface growth
- document runbooks for repeatable outcomes

## Governance Baseline

- maintain approved-plugin lists by team function
- review plugin additions through change-management process
- pair automation workflows with review checkpoints
- track risky command categories with stronger scrutiny

## Safety Controls

- require security scanning commands for production-bound changes
- standardize code-review command usage before merge
- prefer explicit slash commands in sensitive workflows
- isolate experimental plugins from core CI/CD paths

## Operational Best Practices

- start with small scope and expand progressively
- keep workflow templates for common tasks
- record failures and fixes in internal runbooks
- periodically prune unused plugins

## Source References

- [Usage Best Practices](https://github.com/wshobson/agents/blob/main/docs/usage.md#best-practices)
- [Plugin Design Principles](https://github.com/wshobson/agents/blob/main/docs/plugins.md#plugin-design-principles)
- [Contributing Guidelines](https://github.com/wshobson/agents/blob/main/.github/CONTRIBUTING.md)

## Summary

You now have a governance model for scaling plugin-based agent operations.

Next: [Chapter 8: Contribution Workflow and Plugin Authoring Patterns](08-contribution-workflow-and-plugin-authoring-patterns.md)
