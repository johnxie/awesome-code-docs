---
layout: default
title: "Chapter 4: Spec Authoring, Delta Patterns, and Quality"
nav_order: 4
parent: OpenSpec Tutorial
---

# Chapter 4: Spec Authoring, Delta Patterns, and Quality

Delta spec quality determines whether OpenSpec increases predictability or just adds paperwork.

## Learning Goals

- write clear ADDED/MODIFIED/REMOVED requirement deltas
- use scenario-driven language for testable behavior
- prevent ambiguity before implementation begins

## Delta Format Essentials

```markdown
## ADDED Requirements
### Requirement: Feature X

## MODIFIED Requirements
### Requirement: Existing Behavior Y

## REMOVED Requirements
### Requirement: Deprecated Behavior Z
```

## Authoring Quality Checklist

| Check | Why |
|:------|:----|
| requirement statement is testable | improves validation and review quality |
| scenarios are concrete | reduces interpretation drift |
| modified sections preserve old behavior context | avoids accidental regressions |
| removals include migration notes | supports safer rollout |

## Common Anti-Patterns

- vague requirements like "improve UX" without measurable behavior
- tasks that introduce implementation details not reflected in specs
- archive attempts before delta specs are reconciled

## Source References

- [Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)
- [Getting Started: Delta Specs](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)
- [Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)

## Summary

You now have concrete rules for writing high-signal artifacts that agents and humans can execute against.

Next: [Chapter 5: Customization, Schemas, and Project Rules](05-customization-schemas-and-project-rules.md)
