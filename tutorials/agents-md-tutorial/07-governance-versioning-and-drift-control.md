---
layout: default
title: "Chapter 7: Governance, Versioning, and Drift Control"
nav_order: 7
parent: AGENTS.md Tutorial
---


# Chapter 7: Governance, Versioning, and Drift Control

Welcome to **Chapter 7: Governance, Versioning, and Drift Control**. In this part of **AGENTS.md Tutorial: Open Standard for Coding-Agent Guidance in Repositories**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter ensures AGENTS.md stays trustworthy as repositories evolve.

## Learning Goals

- establish ownership and review cadence
- detect stale instructions and command drift
- version instruction changes deliberately
- tie guidance updates to codebase changes

## Governance Practices

- require AGENTS.md updates when build/test workflows change
- include instruction drift checks in periodic repo audits
- assign clear document owners per repository

## Source References

- [AGENTS.md Repository Governance Discussions](https://github.com/agentsmd/agents.md/issues)
- [AGENTS.md Sample File](https://github.com/agentsmd/agents.md/blob/main/AGENTS.md)

## Summary

You now have governance patterns to keep agent guidance accurate over time.

Next: [Chapter 8: Ecosystem Contribution and Standard Evolution](08-ecosystem-contribution-and-standard-evolution.md)

## Source Code Walkthrough

### `AGENTS.md`

Governance and drift control depend on treating `AGENTS.md` as a version-controlled artifact with the same discipline as code. The upstream [`AGENTS.md`](https://github.com/agentsmd/agents.md/blob/HEAD/AGENTS.md) itself is managed through standard pull requests and reviewed like any other file — the commit history for this file in the upstream repo illustrates how the specification evolves incrementally without breaking existing consumers.

Review the git log for `AGENTS.md` in the upstream repository to see what kinds of changes are considered breaking versus additive, which directly informs the versioning strategy described in this chapter.
