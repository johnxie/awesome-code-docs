---
layout: default
title: "Chapter 5: Production Skills"
nav_order: 5
parent: Anthropic Skills Tutorial
---

# Chapter 5: Production Skills

Production skills require strict output contracts, validation, and auditability.

## Example: Document Generation Skill

```text
Input: account_summary.json
Output: executive_report.docx + risk_register.xlsx
```

## Production Requirements

- Deterministic output sections and headings.
- Schema checks for intermediate JSON.
- Retry-safe execution for script steps.
- Trace IDs for each generated artifact.

## Typical Toolchain

- `python-docx` for DOCX
- `openpyxl` for XLSX
- `python-pptx` for PPTX
- `reportlab` for PDF

## Summary

You can now scope and harden skills for business-critical workflows.

Next: [Chapter 6: Best Practices](06-best-practices.md)
