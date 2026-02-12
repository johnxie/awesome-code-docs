---
layout: default
title: "Chapter 4: Feedback Loops, Review Comments, and CI Repair"
nav_order: 4
parent: Sweep Tutorial
---

# Chapter 4: Feedback Loops, Review Comments, and CI Repair

Sweep outcomes improve when teams actively run comment-based feedback loops and CI repair cycles.

## Learning Goals

- distinguish issue comments from PR review comments
- use feedback channels intentionally for targeted updates
- leverage CI signals to improve generated code quality

## Feedback Channels

| Channel | Typical Effect |
|:--------|:---------------|
| issue comment | broader cross-file or full-PR rework |
| PR comment | targeted iteration on existing change set |
| code review comment | file-local fixes with explicit context |

## Practical Pattern

1. start with issue-level clarification for large mistakes
2. move to file-level review comments for precise corrections
3. use CI failures to request deterministic fixes

## Source References

- [Getting Started: Fix Sweep PRs](https://github.com/sweepai/sweep/blob/main/docs/pages/getting-started.md)
- [Advanced Usage](https://github.com/sweepai/sweep/blob/main/docs/pages/usage/advanced.mdx)

## Summary

You now know how to turn generated PRs into high-quality merge candidates through structured feedback.

Next: [Chapter 5: CLI and Self-Hosted Deployment](05-cli-and-self-hosted-deployment.md)
