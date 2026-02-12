---
layout: default
title: "Chapter 6: Customization and Extension Patterns"
nav_order: 6
parent: Create Python Server Tutorial
---

# Chapter 6: Customization and Extension Patterns

This chapter covers practical ways to evolve generated scaffolds into domain-specific services.

## Learning Goals

- extend default primitive handlers with domain logic safely
- preserve protocol contracts while changing storage or workflows
- keep template-origin code maintainable over time
- avoid coupling business logic to scaffold assumptions

## Extension Strategy

1. isolate domain logic in dedicated modules/services
2. keep handler boundaries thin and protocol-focused
3. add schema validation and error mapping early
4. maintain behavior tests as templates diverge

## Source References

- [Template Server Implementation](https://github.com/modelcontextprotocol/create-python-server/blob/main/src/create_mcp_server/template/server.py.jinja2)
- [Create Python Server README](https://github.com/modelcontextprotocol/create-python-server/blob/main/README.md)

## Summary

You now have an extension model for safely evolving generated MCP servers.

Next: [Chapter 7: Quality, Security, and Contribution Workflows](07-quality-security-and-contribution-workflows.md)
