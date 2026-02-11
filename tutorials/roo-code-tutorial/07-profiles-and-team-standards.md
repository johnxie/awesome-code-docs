---
layout: default
title: "Chapter 7: Profiles and Team Standards"
nav_order: 7
parent: Roo Code Tutorial
---

# Chapter 7: Profiles and Team Standards

Profiles are the mechanism for making Roo behavior consistent across individuals and repositories.

## Why Profiles Matter

Without shared profiles, teams get:

- inconsistent model/provider usage
- variable prompt quality
- unpredictable cost and latency
- uneven review and approval behavior

Profiles solve this by encoding defaults.

## Profile Baseline Components

| Component | Standardize |
|:----------|:------------|
| model strategy | default model tiers by task class |
| mode policy | which modes are preferred/forbidden per work type |
| tool policy | approved tools and approval thresholds |
| output format | required summary and evidence structure |
| budget controls | per-task and per-session limits |

## Example Team Profile Set

| Profile | Use Case |
|:--------|:---------|
| `dev-fast` | everyday implementation loops |
| `debug-deep` | incident and regression investigation |
| `release-safe` | high scrutiny before merge/release |
| `private-compliance` | sensitive code and restricted providers |

## Rollout Pattern

1. pilot profile in one repo
2. collect quality/cost/latency metrics
3. revise defaults and publish versioned profile
4. expand to more teams with opt-in gates

## Policy Drift Controls

- version profile definitions
- log profile changes with rationale
- run scheduled profile health checks
- review exceptions and temporary overrides

## Team Enablement Checklist

- profile docs are accessible
- onboarding includes profile selection guidance
- prompt templates are profile-aware
- incident runbooks reference profile behavior

## Anti-Patterns

- too many profiles with overlapping scope
- profiles that hide risky defaults
- no ownership for profile maintenance
- no metric feedback loop after rollout

## Chapter Summary

You now have a profile-driven scaling model for Roo Code:

- shared defaults for quality and safety
- staged rollout with measurable impact
- governance against policy drift

Next: [Chapter 8: Enterprise Operations](08-enterprise-operations.md)
