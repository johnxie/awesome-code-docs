---
layout: default
title: "Chapter 4: Custom Agents and Background Runs"
nav_order: 4
parent: Opcode Tutorial
---

# Chapter 4: Custom Agents and Background Runs

This chapter covers how Opcode supports specialized agents and non-blocking execution.

## Learning Goals

- create custom task-specific agents
- configure model and permission settings per agent
- run background executions safely
- track execution history and outcomes

## Agent Workflow

```text
CC Agents -> Create Agent -> Configure -> Execute
```

## Guardrail Practices

- restrict permissions per agent role
- document agent purpose and prompt contracts
- review execution logs before promoting outputs

## Source References

- [Opcode README: CC Agents](https://github.com/winfunc/opcode/blob/main/README.md#-cc-agents)
- [Opcode README: Creating Agents](https://github.com/winfunc/opcode/blob/main/README.md#creating-agents)

## Summary

You now know how to build and operate specialized agent workflows in Opcode.

Next: [Chapter 5: MCP and Context Management](05-mcp-and-context-management.md)
