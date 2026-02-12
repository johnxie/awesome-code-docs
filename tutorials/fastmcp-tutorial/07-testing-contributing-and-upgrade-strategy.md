---
layout: default
title: "Chapter 7: Testing, Contributing, and Upgrade Strategy"
nav_order: 7
parent: FastMCP Tutorial
---

# Chapter 7: Testing, Contributing, and Upgrade Strategy

This chapter covers change safety: test strategy, contributor workflow, and version migration.

## Learning Goals

- apply fast feedback loops for transport and tool behavior changes
- follow contributor expectations for clean review cycles
- handle breaking changes intentionally during upgrades
- keep documentation and tests synchronized with runtime behavior

## Change-Safety Workflow

| Stage | Focus |
|:------|:------|
| local test loop | in-memory and targeted integration tests |
| PR quality gate | lint, test markers, docs consistency |
| upgrade review | explicit migration notes and breaking-change checks |
| rollout | staged validation before production promotion |

## Source References

- [Tests Guide](https://github.com/jlowin/fastmcp/blob/main/docs/development/tests.mdx)
- [Contributing Guide](https://github.com/jlowin/fastmcp/blob/main/docs/development/contributing.mdx)
- [Upgrade Guide](https://github.com/jlowin/fastmcp/blob/main/docs/development/upgrade-guide.mdx)

## Summary

You now have a safer maintenance model for evolving FastMCP server/client systems.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
