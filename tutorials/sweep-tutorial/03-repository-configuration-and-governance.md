---
layout: default
title: "Chapter 3: Repository Configuration and Governance"
nav_order: 3
parent: Sweep Tutorial
---

# Chapter 3: Repository Configuration and Governance

This chapter focuses on `sweep.yaml`, the main behavior contract for repository-level Sweep usage.

## Learning Goals

- configure branch, CI usage, and directory restrictions
- encode repository-specific guidance for better outputs
- prevent unsafe edits through policy and structure

## Key `sweep.yaml` Settings

| Key | Role |
|:----|:-----|
| `branch` | base branch for generated changes |
| `gha_enabled` | enable CI signal consumption |
| `blocked_dirs` | prevent edits in sensitive paths |
| `draft` | control PR draft behavior |
| `description` | provide repository context and coding rules |

## Baseline Config Example

```yaml
branch: main
gha_enabled: true
blocked_dirs: [".github/"]
draft: false
description: "Python 3.10 repo; follow PEP8 and update tests when modifying business logic."
```

## Governance Checklist

1. block sensitive infra and compliance directories
2. include style and testing expectations in description
3. review config changes like code with PR approval

## Source References

- [Config Docs](https://github.com/sweepai/sweep/blob/main/docs/pages/usage/config.mdx)
- [Default sweep.yaml](https://github.com/sweepai/sweep/blob/main/sweep.yaml)

## Summary

You now have a policy foundation for safer, more consistent Sweep behavior.

Next: [Chapter 4: Feedback Loops, Review Comments, and CI Repair](04-feedback-loops-review-comments-and-ci-repair.md)
