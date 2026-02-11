---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Anthropic Skills Tutorial
---

# Chapter 1: Getting Started

This chapter introduces the skill package format and builds a first working skill.

## Minimal Skill Structure

```text
my-skill/
  SKILL.md
```

## Minimal `SKILL.md`

```markdown
---
name: incident-summary
description: Summarize incident notes into an actionable report
---

When given raw incident notes, produce:
1. Timeline
2. Root cause hypothesis
3. Action items with owners
```

## Add Supporting Assets

```text
my-skill/
  SKILL.md
  templates/
    incident-report.md
  scripts/
    normalize_notes.py
```

## First Validation Checklist

- Metadata and instructions are clear.
- Inputs/outputs are explicit.
- No ambiguous or conflicting instructions.

## Summary

You now have a basic reusable skill with a standard folder layout.

Next: [Chapter 2: Skill Categories](02-skill-categories.md)
