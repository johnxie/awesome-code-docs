---
layout: default
title: "Chapter 7: Troubleshooting, Security, and Operations"
nav_order: 7
parent: Stagewise Tutorial
---

# Chapter 7: Troubleshooting, Security, and Operations

This chapter covers practical operational concerns: common runtime failures, security boundaries, and production-minded usage.

## Learning Goals

- diagnose common integration and prompt-delivery failures
- apply safe operating boundaries for workspace edits
- define team-level operational controls

## Common Failure Modes

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| prompt not received in IDE | wrong or duplicate IDE target | close extra sessions and retry |
| toolbar fails in SSH WSL remote flow | unsupported remote access pattern | run on local host workflow |
| edits target wrong repo | Stagewise not started in app root | relaunch from correct workspace |

## Security and Safety Controls

- run Stagewise only in trusted local workspaces
- keep source control and CI checks mandatory before merge
- use bridge mode intentionally when delegating to external agents

## Source References

- [Common Issues](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/troubleshooting/common-issues.mdx)
- [CLI Deep Dive](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/advanced-usage/cli-deep-dive.mdx)

## Summary

You now have a troubleshooting and operations baseline for reliable Stagewise sessions.

Next: [Chapter 8: Contribution Workflow and Ecosystem Evolution](08-contribution-workflow-and-ecosystem-evolution.md)
