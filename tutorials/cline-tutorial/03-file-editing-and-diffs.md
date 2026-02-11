---
layout: default
title: "Chapter 3: File Editing and Diffs"
nav_order: 3
parent: Cline Tutorial
---

# Chapter 3: File Editing and Diffs

Diff quality is the primary reliability control in Cline-driven development.

## Diff-Centric Edit Lifecycle

1. Cline proposes file modifications
2. you review the exact patch
3. approve or reject with targeted feedback
4. rerun until the patch is minimal and correct

## High-Signal Diff Review Rubric

| Review Lens | Questions |
|:------------|:----------|
| Scope | Did Cline touch only expected files? |
| Logic | Does code match requested behavior? |
| Safety | Any hidden config, auth, or data-path risk? |
| Compatibility | Could this break external callers/contracts? |

## Checkpoints and Recovery

When tasks get large, checkpoint before risky edits so you can recover quickly if output quality degrades.

Recommended moments:

- before schema/config rewrites
- before multi-file refactors
- before dependency upgrades

## Patch Hygiene Rules

- prefer small, staged diffs over single large edits
- require validation evidence next to each accepted patch
- reject formatting-only churn unless intentional

## Summary

You now have a practical model for governing Cline edits through robust diff review.

Next: [Chapter 4: Terminal and Runtime Tools](04-terminal-and-runtime-tools.md)
