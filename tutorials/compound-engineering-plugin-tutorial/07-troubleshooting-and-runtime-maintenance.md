---
layout: default
title: "Chapter 7: Troubleshooting and Runtime Maintenance"
nav_order: 7
parent: Compound Engineering Plugin Tutorial
---

# Chapter 7: Troubleshooting and Runtime Maintenance

This chapter provides practical recovery patterns for common runtime and integration failures.

## Learning Goals

- diagnose plugin install and command resolution issues
- recover from MCP server auto-load failures
- debug cross-provider conversion/sync problems
- maintain runtime consistency during rapid iteration

## High-Frequency Issues

- marketplace install mismatch or stale plugin cache
- MCP config not loading automatically
- provider-target conversion output mismatches
- dependency/runtime version drift in Bun/Node environments

## Recovery Loop

1. verify install and plugin metadata
2. inspect command availability and namespace
3. verify MCP configuration and permissions
4. re-run narrow-scope conversion tests

## Source References

- [Known Issues](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md#known-issues)
- [Getting Started Docs Page](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/pages/getting-started.html)
- [Plugin Versioning Requirements](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/solutions/plugin-versioning-requirements.md)

## Summary

You now have a troubleshooting and maintenance playbook for compound workflows.

Next: [Chapter 8: Contribution Workflow and Versioning Discipline](08-contribution-workflow-and-versioning-discipline.md)
