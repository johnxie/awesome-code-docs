---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Anthropic Skills Tutorial
---

# Chapter 1: Getting Started

This chapter gets you from zero to a functioning skill you can iterate on.

## Skill Anatomy

A minimal skill is one folder plus one file:

```text
my-first-skill/
  SKILL.md
```

`SKILL.md` has two important parts:

1. **Frontmatter** for identity and routing metadata
2. **Instruction body** that defines behavior, constraints, and output expectations

## Minimal Valid `SKILL.md`

```markdown
---
name: incident-summary
description: Summarize incident notes into a concise operations report
---

When given incident notes:
1. Produce a timeline of events.
2. List likely contributing factors.
3. Propose prioritized action items with owners.
```

## First Upgrade: Add Determinism

Most teams should move immediately from free-form instructions to explicit output contracts.

```markdown
## Output Contract
- Return markdown only.
- Include sections: `Timeline`, `Contributing Factors`, `Actions`.
- Each action must include `owner`, `due_date`, and `risk_if_missed`.
```

This single addition usually reduces variance more than model-level tuning.

## Add Supporting Files

As tasks become operational, move from one-file skills to structured packages:

```text
incident-skill/
  SKILL.md
  templates/
    postmortem.md
  scripts/
    normalize_incident_json.py
  references/
    severity-matrix.md
```

Use this rule:

- Put **policy and behavior** in `SKILL.md`
- Put **deterministic transforms** in `scripts/`
- Put **stable source context** in `references/`

## Local Iteration Loop

1. Run the skill against 5 to 10 representative prompts.
2. Save outputs as golden snapshots.
3. Tighten instructions where variance or ambiguity appears.
4. Re-run snapshots after every instruction change.

This gives you fast regression detection without heavyweight tooling.

## Common Early Mistakes

| Mistake | Symptom | Fix |
|:--------|:--------|:----|
| Broad description | Skill triggers for unrelated requests | Narrow the `description` to explicit use cases |
| No output schema | Inconsistent format between runs | Add required sections and field-level constraints |
| Hidden dependencies | Skill fails on missing files/scripts | Document all dependencies in `SKILL.md` |
| Conflicting instructions | Internal contradiction in outputs | Remove overlap and define precedence |

## Summary

You now have a valid, testable skill package and a repeatable iteration loop.

Next: [Chapter 2: Skill Categories](02-skill-categories.md)
