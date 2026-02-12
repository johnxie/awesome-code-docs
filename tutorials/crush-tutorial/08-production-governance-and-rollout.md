---
layout: default
title: "Chapter 8: Production Governance and Rollout"
nav_order: 8
parent: Crush Tutorial
---

# Chapter 8: Production Governance and Rollout

This chapter provides a governance framework for deploying Crush across real engineering teams.

## Learning Goals

- define production configuration and policy baselines
- enforce attribution, metrics, and privacy preferences intentionally
- standardize rollout stages across teams and repos
- maintain operational quality over time

## Governance Baseline

| Area | Recommended Policy |
|:-----|:-------------------|
| config management | publish approved `.crush.json` templates per repo class |
| tool safety | start with restrictive `allowed_tools` and `disabled_tools` |
| attribution | choose `assisted-by`, `co-authored-by`, or `none` explicitly |
| telemetry | configure `disable_metrics` or `DO_NOT_TRACK` where required |
| rollout | pilot -> expand -> enforce policy checks |

## Rollout Stages

1. run pilot with senior maintainers and strict permissions
2. refine model/provider defaults and command packs
3. publish team onboarding docs + starter configs
4. expand to broader teams with monitored issue intake
5. audit quarterly for drift in models, tools, and policies

## Source References

- [Crush README: Attribution Settings](https://github.com/charmbracelet/crush/blob/main/README.md#attribution-settings)
- [Crush README: Metrics](https://github.com/charmbracelet/crush/blob/main/README.md#metrics)
- [Crush README: Configuration](https://github.com/charmbracelet/crush/blob/main/README.md#configuration)

## Summary

You now have an end-to-end framework for adopting Crush as a governed coding-agent platform.

Compare terminal-first practices in the [Goose Tutorial](../goose-tutorial/).
