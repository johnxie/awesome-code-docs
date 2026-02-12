---
layout: default
title: "Chapter 8: Migration, Governance, and Team Adoption"
nav_order: 8
parent: OpenSpec Tutorial
---

# Chapter 8: Migration, Governance, and Team Adoption

This final chapter covers migration from legacy workflows and long-term team operating practices.

## Learning Goals

- migrate from pre-OPSX patterns without losing intent
- define governance for artifact quality and ownership
- scale OpenSpec adoption across teams and repositories

## Migration Priorities

| Priority | Reason |
|:---------|:-------|
| clean legacy instruction files | reduce command ambiguity |
| regenerate skills with current CLI | align tool behavior |
| validate migrated artifacts | preserve spec continuity |

## Governance Model

1. assign owners for schema, rules, and workflow policy
2. define review criteria for proposal/spec/design/tasks quality
3. require validation before archive and merge
4. audit telemetry and privacy posture against team policy

## Adoption Blueprint

| Phase | Objective |
|:------|:----------|
| pilot | prove value on one active product area |
| standardization | publish templates and review guides |
| scale | expand to multi-team, multi-tool workflows |

## Source References

- [Migration Guide](https://github.com/Fission-AI/OpenSpec/blob/main/docs/migration-guide.md)
- [README](https://github.com/Fission-AI/OpenSpec/blob/main/README.md)
- [Maintainers and Advisors](https://github.com/Fission-AI/OpenSpec/blob/main/MAINTAINERS.md)

## Summary

You now have an end-to-end model for running OpenSpec as part of a production engineering workflow.

Next: compare execution patterns with [Claude Task Master](../claude-task-master-tutorial/) and [Codex CLI](../codex-cli-tutorial/).
