---
layout: default
title: "Chapter 6: Security, Credentials, and Risk Controls"
nav_order: 6
parent: awslabs/mcp Tutorial
---

# Chapter 6: Security, Credentials, and Risk Controls

This chapter covers credential boundaries, mutating-operation risk, and environment controls.

## Learning Goals

- map IAM role scope to operational blast radius
- apply read-only and mutation-consent style safeguards where supported
- enforce single-tenant assumptions for server instances
- reduce file-system and command execution risk through explicit policy

## Security Baseline

Treat IAM as the primary control plane, then layer server-side safety flags and client approval flows on top. Do not run single-user servers as shared multi-tenant services.

## Source References

- [AWS API MCP Server Security Sections](https://github.com/awslabs/mcp/blob/main/src/aws-api-mcp-server/README.md)
- [Repository README Security Notes](https://github.com/awslabs/mcp/blob/main/README.md)
- [Vibe Coding Tips](https://github.com/awslabs/mcp/blob/main/VIBE_CODING_TIPS_TRICKS.md)

## Summary

You now have a practical risk-control framework for production MCP usage on AWS.

Next: [Chapter 7: Development, Testing, and Contribution Workflow](07-development-testing-and-contribution-workflow.md)
