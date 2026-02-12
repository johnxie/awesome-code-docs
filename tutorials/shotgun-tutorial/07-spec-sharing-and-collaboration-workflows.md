---
layout: default
title: "Chapter 7: Spec Sharing and Collaboration Workflows"
nav_order: 7
parent: Shotgun Tutorial
---

# Chapter 7: Spec Sharing and Collaboration Workflows

Shotgun workflows are designed around reusable, versioned spec artifacts that teams can review and share.

## Artifact Model

| Artifact | Role |
|:---------|:-----|
| `.shotgun/research.md` | codebase and external findings |
| `.shotgun/specification.md` | feature definition and constraints |
| `.shotgun/plan.md` | staged implementation sequence |
| `.shotgun/tasks.md` | executable task breakdown |
| `.shotgun/AGENTS.md` | agent-facing export format |

## Collaboration Patterns

- review specs before implementation starts
- keep plan updates explicit when assumptions change
- use versioned sharing for cross-team alignment

## Source References

- [Shotgun CLI Output Files](https://github.com/shotgun-sh/shotgun/blob/main/docs/CLI.md#output-files)
- [Shotgun README: Share Specs](https://github.com/shotgun-sh/shotgun#-share-specs-with-your-team)

## Summary

You can now structure multi-person review around stable spec artifacts instead of ad hoc prompts.

Next: [Chapter 8: Production Operations, Observability, and Security](08-production-operations-observability-and-security.md)
