---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Kimi CLI Tutorial
---

# Chapter 8: Production Operations and Governance

Team-scale Kimi usage needs clear policy around approvals, skills, integrations, and update workflows.

## Governance Checklist

1. standardize approved agent/skill directories and naming
2. enforce review for MCP server additions and auth scopes
3. define policy for `--yolo` usage in CI and local development
4. document session retention and context compaction practices
5. pin and test version upgrades before broad rollout

## Ops Baseline

- keep changelog review in upgrade process
- use print mode for deterministic automation cases
- use wire/acp integrations only with known client trust boundaries

## Source References

- [Kimi CLI README](https://github.com/MoonshotAI/kimi-cli/blob/main/README.md)
- [Kimi changelog](https://github.com/MoonshotAI/kimi-cli/blob/main/CHANGELOG.md)
- [Agent skills docs](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/skills.md)

## Summary

You now have a production-ready operating framework for Kimi CLI across developer teams.
