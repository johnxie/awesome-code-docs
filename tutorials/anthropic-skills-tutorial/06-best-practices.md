---
layout: default
title: "Chapter 6: Best Practices"
nav_order: 6
parent: Anthropic Skills Tutorial
---

# Chapter 6: Best Practices

Strong skills are explicit, testable, and easy to review.

## Authoring Principles

- Prefer concrete verbs over broad goals.
- Define what to do when inputs are missing.
- State prohibited actions directly.
- Include examples for tricky edge cases.

## Testing Strategy

Use three test layers:

1. **Golden tests**: stable prompts with expected output shape
2. **Adversarial tests**: malformed or ambiguous inputs
3. **Regression tests**: replay historical failures

Keep test fixtures in version control with the skill.

## Versioning and Changelogs

Treat prompt changes as code changes.

- Use semantic versioning for skills distributed broadly.
- Keep a changelog with behavioral deltas.
- Call out breaking output changes explicitly.

## Review Checklist

| Check | Why |
|:------|:----|
| Output contract unchanged or migrated | Prevent downstream breakage |
| References updated and valid | Avoid stale policy behavior |
| Script interfaces still compatible | Prevent runtime failures |
| Security notes updated | Keep operators informed |

## Observability

Capture at least:

- skill name + version
- request category
- validation pass/fail
- major error class
- latency/cost envelope

This data is essential for continuous improvement.

## Summary

You now have a concrete quality system for maintaining skills over time.

Next: [Chapter 7: Publishing and Sharing](07-publishing-sharing.md)
