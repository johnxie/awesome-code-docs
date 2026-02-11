---
layout: default
title: "Chapter 5: Files, Diff, and Locking"
nav_order: 5
parent: Bolt.diy Tutorial
---

# Chapter 5: Files, Diff, and Locking

File safety features are central to making AI-assisted coding trustworthy.

## Diff-Centric Review

bolt.diy exposes AI-generated changes through diff-oriented interfaces. This enables:

- quick impact review
- selective acceptance/rejection patterns
- safer collaboration on generated edits

## File Locking Model

The project includes file locking capabilities aimed at reducing collision and overwrite risks during generation loops.

## Snapshot and Restore

Project snapshots and restoration flows let users revert or recover workspace states after unsuccessful generations.

## Practical Safety Policy

| Policy | Why |
|:-------|:----|
| review diffs before apply | catches unintended broad edits |
| lock critical files | protects infra/security config |
| snapshot before risky prompts | fast rollback path |
| validate after apply | prevents silent runtime breakage |

## Summary

You now have a concrete change-governance model for AI-generated edits in bolt.diy.

Next: [Chapter 6: Integrations and MCP](06-integrations-and-mcp.md)
