---
layout: default
title: "Chapter 5: Testing, Linting, and CI Alignment"
nav_order: 5
parent: AGENTS.md Tutorial
---


# Chapter 5: Testing, Linting, and CI Alignment

Welcome to **Chapter 5: Testing, Linting, and CI Alignment**. In this part of **AGENTS.md Tutorial: Open Standard for Coding-Agent Guidance in Repositories**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter connects AGENTS.md instructions to actual quality gates.

## Learning Goals

- encode required checks in agent instructions
- map local commands to CI workflows
- reduce false-positive “task complete” outcomes
- ensure agent outputs are merge-ready

## Alignment Checklist

- explicit lint/test/build commands
- required pass criteria before PR submission
- path-specific test guidance for monorepos

## Source References

- [AGENTS.md README Example Sections](https://github.com/agentsmd/agents.md/blob/main/README.md)
- [AGENTS.md README (Testing Guidance Example)](https://github.com/agentsmd/agents.md/blob/main/README.md)

## Summary

You now can align AGENTS.md behavior with enforceable CI outcomes.

Next: [Chapter 6: Team Rollout and Adoption Playbook](06-team-rollout-and-adoption-playbook.md)

## Source Code Walkthrough

### `AGENTS.md`

The testing and CI alignment patterns described in this chapter are reflected in the [`AGENTS.md`](https://github.com/agentsmd/agents.md/blob/HEAD/AGENTS.md) file itself, which documents the project's own test and lint commands. Agents reading this file know exactly which commands to run before submitting changes — the same principle this chapter teaches you to apply in your own repositories.

The upstream repo's [`package.json`](https://github.com/agentsmd/agents.md/blob/HEAD/package.json) shows how the commands listed in `AGENTS.md` map to actual scripts, demonstrating the link between the specification and the CI configuration.
