---
layout: default
title: "Chapter 2: Skill Categories"
nav_order: 2
parent: Anthropic Skills Tutorial
---

# Chapter 2: Skill Categories

Welcome to **Chapter 2: Skill Categories**. In this part of **Anthropic Skills Tutorial: Reusable AI Agent Capabilities**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for core abstractions in this chapter so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Skill Categories` as an operating subsystem inside **Anthropic Skills Tutorial: Reusable AI Agent Capabilities**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around execution and reliability details as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Skill Categories` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `core component`.
2. **Input normalization**: shape incoming data so `execution layer` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `state model`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [anthropics/skills repository](https://github.com/anthropics/skills)
  Why it matters: authoritative reference on `anthropics/skills repository` (github.com).

Suggested trace strategy:
- search upstream code for `Skill` and `Categories` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started](01-getting-started.md)
- [Next Chapter: Chapter 3: Advanced Skill Design](03-advanced-skill-design.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
