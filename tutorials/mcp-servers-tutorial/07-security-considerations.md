---
layout: default
title: "Chapter 7: Security Considerations"
nav_order: 7
parent: MCP Servers Tutorial
---

# Chapter 7: Security Considerations

Security posture is the difference between a useful MCP server and a risky one.

## Threat Areas

- Prompt-driven misuse of privileged tools
- path traversal and command injection
- exfiltration through overbroad network/file access

## Required Controls

- strict input validation and schema checks
- allowlisted operations and bounded parameters
- least-privilege runtime permissions
- structured audit logs and trace IDs

## Operational Controls

- rate limits by caller identity
- anomaly detection on tool usage
- incident runbook for key rotation and containment

## Summary

You can now harden MCP servers against common abuse and failure patterns.

Next: [Chapter 8: Production Adaptation](08-production-adaptation.md)
