---
layout: default
title: "Chapter 8: Production Operations and Security"
nav_order: 8
parent: Opcode Tutorial
---

# Chapter 8: Production Operations and Security

This chapter provides operational guidance for deploying Opcode in team environments.

## Learning Goals

- align Opcode with internal security and governance controls
- define safe agent execution policies
- establish rollout and incident response practices
- maintain stable operations over time

## Security Baseline

From README positioning:

- process isolation for agent operations
- permission controls per agent
- local data-first model
- open-source transparency

## Rollout Model

1. pilot with experienced maintainers
2. enforce policy templates for agent permissions
3. require review for MCP and session checkpoint policies
4. monitor usage, errors, and restore events

## Source References

- [Opcode README: Security](https://github.com/winfunc/opcode/blob/main/README.md#-security)
- [Opcode README: Contributing](https://github.com/winfunc/opcode/blob/main/README.md#-contributing)

## Summary

You now have a complete runbook for operating Opcode as a governed desktop control plane for Claude Code.

Compare higher-level orchestration in the [Vibe Kanban Tutorial](../vibe-kanban-tutorial/).
