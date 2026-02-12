---
layout: default
title: "Chapter 3: Transport and Client Integration Patterns"
nav_order: 3
parent: awslabs/mcp Tutorial
---

# Chapter 3: Transport and Client Integration Patterns

This chapter covers integration patterns across IDE and chat MCP clients.

## Learning Goals

- understand default transport assumptions in the ecosystem
- map client configuration differences across hosts
- evaluate when HTTP modes are available for specific servers
- avoid brittle configuration drift across teams

## Integration Rule

Standardize one primary transport/client path per environment first, then add alternative modes only when you have a concrete operational requirement.

## Source References

- [Repository README Transport Section](https://github.com/awslabs/mcp/blob/main/README.md)
- [AWS API MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-api-mcp-server/README.md)
- [AWS Documentation MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-documentation-mcp-server/README.md)

## Summary

You now have a repeatable integration pattern for client configuration and transport selection.

Next: [Chapter 4: Infrastructure and IaC Workflows](04-infrastructure-and-iac-workflows.md)
