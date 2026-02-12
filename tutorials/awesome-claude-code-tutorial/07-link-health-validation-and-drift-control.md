---
layout: default
title: "Chapter 7: Link Health, Validation, and Drift Control"
nav_order: 7
parent: Awesome Claude Code Tutorial
---

# Chapter 7: Link Health, Validation, and Drift Control

This chapter focuses on operational checks that keep a fast-moving curated list trustworthy.

## Learning Goals

- run link and structure checks before merging changes
- understand automation labels and state transitions
- detect generation drift early
- recover quickly when resources go stale or break

## Verification Stack

| Check | Command | Failure Signal |
|:------|:--------|:---------------|
| link validation | `make validate` | inaccessible or invalid URLs |
| unit and integration checks | `make test` | parser/generator regressions |
| full CI gate | `make ci` | formatting/types/tests/docs-tree mismatch |
| regeneration determinism | `make test-regenerate` | generated output drift |

## Source References

- [How It Works](https://github.com/hesreallyhim/awesome-claude-code/blob/main/docs/HOW_IT_WORKS.md)
- [Testing Guide](https://github.com/hesreallyhim/awesome-claude-code/blob/main/docs/TESTING.md)
- [Makefile Checks](https://github.com/hesreallyhim/awesome-claude-code/blob/main/Makefile)

## Summary

You now have the operational health model for keeping curated docs accurate over time.

Next: [Chapter 8: Contribution Workflow and Governance](08-contribution-workflow-and-governance.md)
