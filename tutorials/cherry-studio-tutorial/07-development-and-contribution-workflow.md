---
layout: default
title: "Chapter 7: Development and Contribution Workflow"
nav_order: 7
parent: Cherry Studio Tutorial
---

# Chapter 7: Development and Contribution Workflow

This chapter targets maintainers and contributors shipping changes to Cherry Studio itself.

## Learning Goals

- set up development environment correctly
- run local dev/test/build workflows
- follow branching and PR expectations
- align contributions with current project constraints

## Dev Commands

```bash
pnpm install
pnpm dev
pnpm test
pnpm build:win
pnpm build:mac
pnpm build:linux
```

## Contribution Controls

- follow defined branch naming and PR process
- ensure tests and quality checks are complete
- respect temporary restrictions documented for data-model/schema changes

## Source References

- [Development guide](https://github.com/CherryHQ/cherry-studio/blob/main/docs/en/guides/development.md)
- [Branching strategy](https://github.com/CherryHQ/cherry-studio/blob/main/docs/en/guides/branching-strategy.md)
- [Contributing guide](https://github.com/CherryHQ/cherry-studio/blob/main/CONTRIBUTING.md)

## Summary

You now have a contributor-ready workflow for building and submitting Cherry Studio changes.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
