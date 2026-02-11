---
layout: default
title: "Chapter 6: Integrations and MCP"
nav_order: 6
parent: Bolt.diy Tutorial
---

# Chapter 6: Integrations and MCP

bolt.diy supports a growing integration surface, including MCP-oriented tool extensions.

## Integration Categories

- model provider APIs
- deployment providers
- data/service integrations (for example Supabase workflows)
- tool protocol integrations such as MCP patterns

## MCP-Oriented Capability

MCP support allows richer external tool interaction patterns, enabling AI workflows to call structured tools beyond plain text generation.

## Integration Design Rules

1. validate external payloads before execution
2. bound side effects behind explicit confirmation paths
3. isolate credentials by integration and environment
4. log integration calls for troubleshooting and audit

## Extension Checklist

- clear contract for tool inputs/outputs
- timeout and retry behavior
- failure fallback path
- versioned integration configuration

## Summary

You can now treat bolt.diy integrations as governed system components rather than ad hoc add-ons.

Next: [Chapter 7: Deployment and Distribution](07-deployment-distribution.md)
