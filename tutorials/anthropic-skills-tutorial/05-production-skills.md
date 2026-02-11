---
layout: default
title: "Chapter 5: Production Skills"
nav_order: 5
parent: Anthropic Skills Tutorial
---

# Chapter 5: Production Skills

Production skill systems prioritize predictability over novelty.

## Define Output Contracts First

Every production skill should define:

- required sections
- required fields
- accepted enum values
- maximum lengths
- failure behavior

Example contract fragment:

```yaml
output:
  format: markdown
  required_sections:
    - executive_summary
    - risk_register
    - action_items
  action_item_fields:
    - owner
    - due_date
    - severity
```

## Deterministic Transformation Layer

Push high-risk transformations into scripts:

- numeric calculations
- date normalization
- schema mapping
- cross-system ID handling

Keep natural language synthesis for summarization and explanation, not critical arithmetic or routing logic.

## Document Generation Workflows

The official skills repo includes document-focused references. A stable pattern is:

1. Generate intermediate structured JSON.
2. Validate schema.
3. Render final artifacts (DOCX/PDF/PPTX/XLSX) via script.
4. Return validation report with artifact metadata.

## Reliability Checklist

- Idempotent run identifiers
- Retry-safe script steps
- Explicit timeout budgets
- Structured error taxonomy
- Artifact checksums for integrity

## Security Checklist

- Never embed secrets in skill instructions
- Restrict script execution environment
- Validate all external inputs
- Redact sensitive logs
- Track skill ownership and on-call routing

## Summary

You now have the backbone for operating skills in business-critical workflows.

Next: [Chapter 6: Best Practices](06-best-practices.md)
