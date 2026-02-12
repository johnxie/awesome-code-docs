---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Onlook Tutorial
---

# Chapter 8: Production Operations and Governance

This chapter provides a practical adoption model for using Onlook in production teams.

## Learning Goals

- define governance boundaries for AI-assisted visual editing
- keep generated code quality high over time
- align Onlook workflows with enterprise delivery controls
- create a sustainable rollout roadmap

## Governance Baseline

| Area | Recommended Baseline |
|:-----|:---------------------|
| repository control | all generated changes through PR review |
| quality gates | enforce lint/test/build before merge |
| branch strategy | isolate large design experiments |
| security/compliance | manage provider keys and secrets centrally |
| training | publish prompt and visual-edit playbooks |

## Rollout Stages

1. pilot with a single product team and clear metrics
2. compare throughput/quality vs existing UI workflow
3. standardize branch and review conventions
4. expand gradually to additional teams and repositories

## Source References

- [Onlook Documentation](https://docs.onlook.com)
- [Onlook Architecture Docs](https://docs.onlook.com/developers/architecture)
- [Onlook Repository](https://github.com/onlook-dev/onlook)

## Summary

You now have a complete model for operationalizing Onlook in real product-engineering environments.

Compare semantic agent augmentation in the [Serena Tutorial](../serena-tutorial/).
