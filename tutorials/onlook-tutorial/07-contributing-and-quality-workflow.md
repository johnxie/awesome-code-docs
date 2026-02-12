---
layout: default
title: "Chapter 7: Contributing and Quality Workflow"
nav_order: 7
parent: Onlook Tutorial
---

# Chapter 7: Contributing and Quality Workflow

This chapter covers the contribution model and quality gates for contributing to Onlook itself.

## Learning Goals

- follow Onlook's contribution process
- run local quality checks before PRs
- structure changes for maintainable review
- reduce integration risk when modifying editor/runtime subsystems

## Contribution Flow

1. pick issue or propose scoped enhancement
2. implement in feature branch/fork
3. run tests/lint/format/type checks locally
4. open PR with architecture notes and reproduction steps
5. iterate with maintainer feedback

## Quality Baseline

Onlook developer docs reference quality tooling including testing, linting/formatting, and TypeScript checks via Bun workflows.

## Source References

- [Onlook README: Contributing](https://github.com/onlook-dev/onlook/blob/main/README.md#contributing)
- [Onlook Developer Docs](https://docs.onlook.com/developers)

## Summary

You now have the operational contribution baseline for working on Onlook core.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
