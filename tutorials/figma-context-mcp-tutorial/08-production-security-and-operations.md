---
layout: default
title: "Chapter 8: Production Security and Operations"
nav_order: 8
parent: Figma Context MCP Tutorial
---

# Chapter 8: Production Security and Operations

This chapter covers secure deployment and operational policies for Figma context pipelines.

## Security Checklist

- store Figma tokens in secret manager, not plain files
- scope token usage to required access only
- rotate credentials on schedule
- audit MCP requests and response metadata

## Operational Metrics

| Metric | Why It Matters |
|:-------|:---------------|
| design-to-code success rate | outcome quality |
| average retries per screen | prompt/context quality signal |
| mean implementation latency | productivity and cost |

## Summary

You now have the security and operations baseline for running Figma Context MCP in production teams.
