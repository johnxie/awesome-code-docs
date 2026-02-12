---
layout: default
title: "Chapter 5: MCP Agent Integration and Tooling"
nav_order: 5
parent: Daytona Tutorial
---

# Chapter 5: MCP Agent Integration and Tooling

This chapter focuses on integrating Daytona with coding-agent hosts through MCP.

## Learning Goals

- initialize Daytona MCP integration for Claude/Cursor/Windsurf
- understand available MCP tools for sandbox, file, git, and command operations
- wire custom MCP config into non-default agent hosts
- troubleshoot common auth and connectivity failures

## Integration Pattern

Use CLI setup (`daytona mcp init ...`) for standard hosts. For custom hosts, generate JSON config via `daytona mcp config`, inject required env vars, and validate tool calls with a minimal create/execute/destroy flow.

## Source References

- [Daytona MCP Server Docs](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/mcp.mdx)
- [CLI MCP README](https://github.com/daytonaio/daytona/blob/main/apps/cli/mcp/README.md)
- [CLI Reference](https://github.com/daytonaio/daytona/blob/main/apps/docs/src/content/docs/en/tools/cli.mdx)

## Summary

You can now connect Daytona capabilities directly into MCP-compatible coding-agent environments.

Next: [Chapter 6: Configuration, API, and Deployment Models](06-configuration-api-and-deployment-models.md)
