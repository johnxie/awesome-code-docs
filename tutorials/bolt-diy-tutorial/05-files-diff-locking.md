---
layout: default
title: "Chapter 5: Files, Diff, and Locking"
nav_order: 5
parent: Bolt.diy Tutorial
---

# Chapter 5: Files, Diff, and Locking

Diff visibility, locking, and snapshots are the core safety controls in bolt.diy workflows.

## Safety Controls

| Control | Purpose |
|:--------|:--------|
| diff review | detect unintended file or logic changes |
| file locking | protect critical config/security files |
| snapshots | enable quick rollback after poor generations |

## Recommended Policy

1. review all generated diffs before apply
2. lock high-risk files (infra/auth/secrets/config)
3. snapshot before multi-file or irreversible operations
4. validate immediately after apply

## Diff Review Checklist

| Check | Goal |
|:------|:-----|
| file scope | reject unrelated file modifications |
| logic intent | confirm patch matches prompt objective |
| config/security impact | catch risky changes early |
| test evidence | require command output before acceptance |

## Why This Matters

AI assistance increases change velocity; these controls keep correctness and auditability intact as velocity rises.

## Summary

You now have a practical governance pattern for safely accepting or rejecting generated changes.

Next: [Chapter 6: Integrations and MCP](06-integrations-and-mcp.md)
