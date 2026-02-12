---
layout: default
title: "Chapter 7: Logs, Debugging, and Operations"
nav_order: 7
parent: Crush Tutorial
---

# Chapter 7: Logs, Debugging, and Operations

This chapter covers the operator workflows you need when Crush behavior deviates from expectations.

## Learning Goals

- inspect and follow Crush logs effectively
- enable debug instrumentation for deeper troubleshooting
- manage provider list updates in connected and air-gapped contexts
- create fast diagnosis loops for production issues

## Logging Baseline

| Need | Command / Config |
|:-----|:------------------|
| recent logs | `crush logs` |
| short tail | `crush logs --tail 500` |
| live follow | `crush logs --follow` |
| debug mode | `--debug` or `options.debug: true` |

Log path reference (project-relative): `./.crush/logs/crush.log`.

## Provider Update Operations

Crush can auto-update provider metadata from Catwalk. For restricted environments:

- disable automatic updates with config or env var
- run explicit `crush update-providers` against remote/local/embedded sources

## Source References

- [Crush README: Logging](https://github.com/charmbracelet/crush/blob/main/README.md#logging)
- [Crush README: Provider Auto-Updates](https://github.com/charmbracelet/crush/blob/main/README.md#provider-auto-updates)

## Summary

You now have practical diagnostics and maintenance workflows for operating Crush reliably.

Next: [Chapter 8: Production Governance and Rollout](08-production-governance-and-rollout.md)
