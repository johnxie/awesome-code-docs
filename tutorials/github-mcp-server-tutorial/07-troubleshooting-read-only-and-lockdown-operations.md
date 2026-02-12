---
layout: default
title: "Chapter 7: Troubleshooting, Read-Only, and Lockdown Operations"
nav_order: 7
parent: GitHub MCP Server Tutorial
---

# Chapter 7: Troubleshooting, Read-Only, and Lockdown Operations

This chapter provides practical recovery patterns for operational issues.

## Learning Goals

- diagnose missing tools and permission mismatches
- fix common read-only and scope-related failures
- use lockdown mode where public-content filtering is required
- recover quickly when host/server config drifts

## Common Failure Triage

| Symptom | Likely Cause | First Fix |
|:--------|:-------------|:----------|
| expected tool missing | toolset not enabled or filtered by scope | expand toolset or verify token scopes |
| write operations blocked | read-only mode enabled | remove `readonly` configuration for write workflows |
| dynamic mode not working | running remote mode | use local server for dynamic discovery |
| unexpected content limits | lockdown mode active | verify `lockdown` header/flag intent |

## Source References

- [Server Configuration Troubleshooting](https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md#troubleshooting)
- [Remote Server URL and Header Modes](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)
- [README: Read-Only Mode](https://github.com/github/github-mcp-server/blob/main/README.md#read-only-mode)

## Summary

You now have a troubleshooting runbook for stable GitHub MCP operations.

Next: [Chapter 8: Contribution and Upgrade Workflow](08-contribution-and-upgrade-workflow.md)
