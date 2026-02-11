---
layout: default
title: "Chapter 3: Git Server"
nav_order: 3
parent: MCP Servers Tutorial
---

# Chapter 3: Git Server

The git server demonstrates a practical balance between read-heavy analysis and controlled mutation.

## Core Tool Surface

The reference git server supports:

- repository state checks (`git_status`, diffs, logs)
- staging and commit operations
- branch creation and checkout
- commit inspection (`git_show`)

This mirrors common developer assistant workflows.

## Safe Usage Strategy

Start with read-only operations:

1. status
2. unstaged/staged diff
3. log and branch listing

Then enable mutating operations (`git_add`, `git_commit`, checkout/reset) only after adding explicit policy controls.

## Mutation Guardrails

For production adaptation, add:

- branch protections
- commit message policy checks
- allowlisted repo paths
- signer identity and audit logging

Without these controls, an agent can perform valid git operations that still violate team policy.

## Example Interaction Pattern

```text
analyze changes -> propose patch -> stage selected files -> commit with structured message
```

Split reasoning and execution. Force explicit confirmation between analysis and mutation steps.

## Common Failure Modes

| Failure | Root Cause | Mitigation |
|:--------|:-----------|:-----------|
| Wrong repository targeted | Ambiguous `repo_path` | Resolve canonical path and verify allowlist |
| Overscoped staging | Wildcard or broad file selection | Enforce explicit file list |
| Unsafe branch switch | Dirty working tree | Add pre-check and block on conflicts |
| Undocumented commit semantics | Inconsistent agent behavior | Standardize commit message template |

## Summary

You can now treat git server operations as a controllable pipeline instead of ad-hoc commands.

Next: [Chapter 4: Memory Server](04-memory-server.md)
