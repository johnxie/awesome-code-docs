---
layout: default
title: "Chapter 2: Skill Categories"
nav_order: 2
parent: Anthropic Skills Tutorial
---

# Chapter 2: Skill Categories

Category design controls maintainability. If categories are too broad, skills become brittle and hard to trust.

## Four Practical Categories

| Category | Typical Inputs | Typical Outputs | Typical Risk |
|:---------|:---------------|:----------------|:-------------|
| Document Workflows | Notes, policy docs, datasets | Structured docs/slides/sheets | Formatting drift |
| Creative and Brand | Briefs, tone rules, examples | On-brand copy or concepts | Brand inconsistency |
| Engineering and Ops | Codebase context, tickets, logs | Patches, runbooks, plans | Incorrect assumptions |
| Enterprise Process | Internal standards and controls | Audit artifacts, compliance actions | Governance gaps |

## How to Choose Category Boundaries

Use one outcome per skill. If two outcomes have different acceptance criteria, split the skill.

**Good split:**
- `incident-triage`
- `postmortem-draft`
- `stakeholder-update`

**Bad split:**
- `incident-everything`

A single giant skill creates unclear prompts, conflicting priorities, and harder testing.

## Decision Matrix

| Question | If "Yes" | If "No" |
|:---------|:----------|:----------|
| Is the output contract identical across requests? | Keep in same skill | Split into separate skills |
| Do tasks share the same references and policies? | Keep shared references | Isolate by domain |
| Can one test suite verify quality for all use cases? | Keep grouped | Split for clearer quality gates |
| Are escalation paths identical? | Keep grouped | Split by risk/approval path |

## Category-Specific Design Tips

- **Document skills:** prioritize template fidelity and deterministic section ordering.
- **Creative skills:** define what variation is allowed and what must stay fixed.
- **Technical skills:** enforce constraints on tools, files, and unsafe operations.
- **Enterprise skills:** include explicit policy references and audit fields.

## Anti-Patterns

- Category names that describe team structure instead of behavior
- Mixing high-stakes and low-stakes actions in one skill
- Using skills as a substitute for missing source documentation
- Requiring hidden tribal knowledge to run the skill

## Summary

You can now define category boundaries that keep skills focused, testable, and easier to operate.

Next: [Chapter 3: Advanced Skill Design](03-advanced-skill-design.md)
