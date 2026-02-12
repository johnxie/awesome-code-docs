---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: awslabs/mcp Tutorial
---

# Chapter 8: Production Operations and Governance

This chapter closes with production operating patterns for long-term reliability.

## Learning Goals

- define deployment boundaries for local vs remote MCP use
- standardize release validation across selected servers
- monitor and prune server/tool sprawl over time
- maintain governance around approvals, logging, and incident response

## Operations Playbook

1. scope each deployment to explicit roles and use cases
2. run versioned validation suites before each upgrade window
3. centralize observability signals and security review outcomes
4. review client/server configs regularly for drift and overexposure
5. keep rollback runbooks tied to specific server versions

## Source References

- [Repository README](https://github.com/awslabs/mcp/blob/main/README.md)
- [Developer Guide](https://github.com/awslabs/mcp/blob/main/DEVELOPER_GUIDE.md)
- [Samples README](https://github.com/awslabs/mcp/blob/main/samples/README.md)

## Summary

You now have an end-to-end model for operating AWS MCP servers with stronger governance and maintainability.
