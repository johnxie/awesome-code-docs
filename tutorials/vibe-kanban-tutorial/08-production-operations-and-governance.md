---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Vibe Kanban Tutorial
---

# Chapter 8: Production Operations and Governance

This chapter defines operational and governance practices for production Vibe Kanban deployments.

## Learning Goals

- establish secure rollout strategy for multi-agent orchestration
- govern configuration and infrastructure changes safely
- define team-level quality and escalation policies
- maintain reliability as agent volume grows

## Governance Baseline

| Area | Recommended Baseline |
|:-----|:---------------------|
| execution policy | define which tasks can run parallel vs gated |
| config governance | version all runtime/MCP settings |
| review gates | enforce merge readiness checks per task type |
| observability | track throughput, failures, and regressions by board column |
| upgrades | stage new versions in pilot environment first |

## Source References

- [Vibe Kanban Repository](https://github.com/BloopAI/vibe-kanban)
- [Vibe Kanban Docs](https://vibekanban.com/docs)
- [Vibe Kanban Discussions](https://github.com/BloopAI/vibe-kanban/discussions)

## Summary

You now have a full operational runbook for managing coding-agent orchestration with Vibe Kanban.

Continue with the [Opcode Tutorial](../opcode-tutorial/) for GUI-native Claude Code workflows.
