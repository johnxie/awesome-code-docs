---
layout: default
title: "Chapter 8: Production Operations and Security"
nav_order: 8
parent: Goose Tutorial
---

# Chapter 8: Production Operations and Security

This chapter turns Goose from a useful local assistant into a controlled team platform.

## Learning Goals

- define production guardrails for Goose usage
- enforce extension and tool policies per environment
- build incident response paths around logs and diagnostics
- establish upgrade and governance cadences

## Production Guardrails

| Domain | Recommended Baseline |
|:-------|:---------------------|
| permissions | default to manual/smart approval in production repos |
| extensions | allowlist approved MCP commands and sources |
| context/cost | tune compaction thresholds and max turns |
| observability | collect logs and diagnostics on failures |
| upgrades | stage canary usage before broad rollout |

## Secure Adoption Flow

1. define approved provider/model matrix
2. define approved extension/tool matrix
3. publish `.gooseignore` and session conventions
4. run pilot with monitored repositories
5. review incidents and tighten defaults

## Governance Cadence

- weekly: check release notes and open security issues
- monthly: audit permission and extension policies
- quarterly: review provider costs, model quality, and policy drift

## Source References

- [Staying Safe with goose](https://block.github.io/goose/docs/guides/security/)
- [goose Extension Allowlist](https://block.github.io/goose/docs/guides/allowlist)
- [goose Governance](https://github.com/block/goose/blob/main/GOVERNANCE.md)
- [Responsible AI-Assisted Coding Guide](https://github.com/block/goose/blob/main/HOWTOAI.md)

## Summary

You now have a complete framework for running Goose with strong safety, consistency, and operational reliability.

Continue by comparing workflows in the [Crush Tutorial](../crush-tutorial/).
