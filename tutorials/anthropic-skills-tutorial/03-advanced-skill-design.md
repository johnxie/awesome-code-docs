---
layout: default
title: "Chapter 3: Advanced Skill Design"
nav_order: 3
parent: Anthropic Skills Tutorial
---

# Chapter 3: Advanced Skill Design

Advanced skills combine instructions, scripts, templates, and contextual resources.

## Multi-File Layout Pattern

```text
customer-support-skill/
  SKILL.md
  scripts/
    classify_ticket.py
    fetch_account_data.ts
  templates/
    escalation-email.md
  resources/
    policy_matrix.csv
```

## Design Principles

- Keep each script single-purpose.
- Make templates explicit and versioned.
- Treat resources as read-only context when possible.

## Script Invocation Guidelines

- Validate all script input.
- Return structured output (JSON preferred).
- Handle failure modes with actionable errors.

## Summary

You can now design composable, multi-file skills with predictable behavior.

Next: [Chapter 4: Integration Platforms](04-integration-platforms.md)
