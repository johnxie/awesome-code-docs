---
layout: default
title: "Chapter 6: Custom Server Development"
nav_order: 6
parent: MCP Servers Tutorial
---

# Chapter 6: Custom Server Development

Use the reference servers as templates for your domain-specific tools.

## Build Workflow

1. Start from the closest reference server.
2. Replace backend adapters with your own systems.
3. Keep tool schemas explicit and versioned.
4. Add tests for success and failure paths.

## Suggested Project Layout

```text
my-mcp-server/
  src/
  tests/
  docs/
  README.md
```

## Contract Testing

- Validate request and response schema.
- Test invalid input handling.
- Confirm deterministic behavior for critical tools.

## Summary

You now have a practical path to build custom MCP servers from proven patterns.

Next: [Chapter 7: Security Considerations](07-security-considerations.md)
