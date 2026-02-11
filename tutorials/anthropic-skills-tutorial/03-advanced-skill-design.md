---
layout: default
title: "Chapter 3: Advanced Skill Design"
nav_order: 3
parent: Anthropic Skills Tutorial
---

# Chapter 3: Advanced Skill Design

Advanced skills are small systems. Treat them like mini-products with explicit interfaces.

## Multi-File Skill Layout

```text
customer-support-skill/
  SKILL.md
  scripts/
    classify_ticket.py
    enrich_account_context.ts
  references/
    escalation-policy.md
    sla-tiers.md
  assets/
    issue-taxonomy.csv
  templates/
    escalation-email.md
```

## Progressive Disclosure Pattern

Good skills avoid dumping all context at once. Instead:

1. Start with task intent and output contract.
2. Pull references only when relevant.
3. Call scripts only when deterministic transformation is required.

This pattern reduces token waste and improves instruction adherence.

## Frontmatter and Metadata Strategy

At minimum, keep `name` and `description` precise.

For larger catalogs, add optional metadata fields (when your runtime supports them) to improve discoverability and policy checks, such as:

- compatibility constraints
- license information
- ownership metadata
- tool allowlists

## Script Design Rules

Scripts should be boring and reliable.

- Use strict argument parsing.
- Return stable JSON structures.
- Fail loudly with actionable error messages.
- Avoid hidden network side effects unless clearly documented.

Example output contract:

```json
{
  "status": "ok",
  "severity": "high",
  "routing_queue": "support-l2",
  "confidence": 0.91
}
```

## References and Assets

- Put durable, high-signal guidance in `references/`.
- Keep `assets/` for files that are required but not convenient to inline.
- Version both in Git so skill behavior is auditable over time.

## Maintainability Checklist

- Single responsibility per script
- Explicit file paths in instructions
- Backward-compatible schema evolution
- Changelog entries for instruction changes

## Summary

You can now design skills that remain understandable as they grow beyond a single markdown file.

Next: [Chapter 4: Integration Platforms](04-integration-platforms.md)
