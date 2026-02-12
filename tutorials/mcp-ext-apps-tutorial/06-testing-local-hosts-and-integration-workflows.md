---
layout: default
title: "Chapter 6: Testing, Local Hosts, and Integration Workflows"
nav_order: 6
parent: MCP Ext Apps Tutorial
---

# Chapter 6: Testing, Local Hosts, and Integration Workflows

This chapter defines testing loops for app and host behavior before production rollout.

## Learning Goals

- use `basic-host` and example servers for local validation
- test against compatible MCP clients and remote exposure paths
- verify tool/UI contracts and host bridge events systematically
- catch integration regressions early with repeatable workflows

## Test Workflow

1. run local app/server against `basic-host`
2. validate behavior in MCP Apps-compatible clients
3. expose local server via `cloudflared` when needed for integration tests
4. run integration-server examples for contract-level checks

## Source References

- [Testing MCP Apps](https://github.com/modelcontextprotocol/ext-apps/blob/main/docs/testing-mcp-apps.md)
- [Basic Host Example](https://github.com/modelcontextprotocol/ext-apps/blob/main/examples/basic-host/README.md)
- [Integration Server Example](https://github.com/modelcontextprotocol/ext-apps/blob/main/examples/integration-server/README.md)
- [Quickstart Example](https://github.com/modelcontextprotocol/ext-apps/blob/main/examples/quickstart/README.md)

## Summary

You now have a repeatable validation workflow for MCP Apps integration quality.

Next: [Chapter 7: Agent Skills and OpenAI Apps Migration](07-agent-skills-and-openai-apps-migration.md)
