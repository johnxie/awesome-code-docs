---
layout: default
title: "Chapter 2: Skill Categories"
nav_order: 2
parent: Anthropic Skills Tutorial
---

# Chapter 2: Skill Categories

Choosing the right skill type helps define boundaries, outputs, and test strategy.

## Common Skill Types

| Category | Typical Input | Typical Output |
|:---------|:--------------|:---------------|
| Document | Raw notes, data | Report, memo, proposal |
| Creative | Prompt intent | Copy, concepts, variants |
| Technical | Codebase context | Code changes, tests, docs |
| Enterprise | Policy/workflow rules | Structured compliance actions |

## Category Decision Rules

- Start with one narrow business outcome.
- Keep input assumptions explicit.
- Prefer deterministic output formats when possible.

## Anti-Patterns

- One mega-skill for unrelated tasks.
- Missing output contract.
- Hidden dependencies not described in `SKILL.md`.

## Summary

You can now classify skills by purpose and scope them effectively.

Next: [Chapter 3: Advanced Skill Design](03-advanced-skill-design.md)
