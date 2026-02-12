---
layout: default
title: "Chapter 7: Troubleshooting, Safety, and Cost Controls"
nav_order: 7
parent: Refly Tutorial
---

# Chapter 7: Troubleshooting, Safety, and Cost Controls

This chapter provides pragmatic recovery and guardrail practices for production usage.

## Learning Goals

- triage common failure modes across API, webhook, and runtime
- enforce safe key handling and permission boundaries
- reduce wasted runs through validation-first execution
- keep costs and failure blast radius under control

## Common Failure Patterns

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| unauthorized API calls | invalid or missing API key | rotate/reconfigure auth header |
| webhook not triggering | webhook disabled or invalid URL | re-enable webhook and verify endpoint |
| run fails mid-execution | invalid variables or dependent service issues | validate input schema and service health |
| high token/runtime cost | oversized workflow scope | split into smaller composable skills |

## Safety Baselines

- keep API keys out of logs and committed files
- test changes in constrained environments before broad rollout
- prefer deterministic, validated workflows over opaque one-shot prompts
- retain run history and telemetry for postmortem analysis

## Source References

- [OpenAPI Error and Endpoint Details](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/openapi.md)
- [Webhook Guide](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/webhook.md)
- [Contributing Guide](https://github.com/refly-ai/refly/blob/main/CONTRIBUTING.md)

## Summary

You now have a practical troubleshooting and safety playbook for Refly operations.

Next: [Chapter 8: Contribution Workflow and Governance](08-contribution-workflow-and-governance.md)
