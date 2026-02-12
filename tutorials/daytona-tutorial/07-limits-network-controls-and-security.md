---
layout: default
title: "Chapter 7: Limits, Network Controls, and Security"
nav_order: 7
parent: Daytona Tutorial
---

# Chapter 7: Limits, Network Controls, and Security

This chapter covers resource governance, rate-limit behavior, and network isolation controls.

## Learning Goals

- map organization tiers to resource and request limits
- implement graceful retry behavior for rate-limited APIs
- use network allow/block controls to reduce risk
- connect sandbox policy choices to broader security posture

## Governance Baseline

Treat quotas and egress policy as first-class architecture constraints. Build retry and throttling by default, and explicitly choose `networkAllowList` or `networkBlockAll` for untrusted workflows.

## Source References

- [Limits](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/limits.mdx)
- [Network Limits (Firewall)](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/network-limits.mdx)
- [Security Policy](https://github.com/daytonaio/daytona/blob/main/SECURITY.md)

## Summary

You now have a policy framework for scaling usage while constraining abuse and blast radius.

Next: [Chapter 8: Production Operations and Contribution](08-production-operations-and-contribution.md)
