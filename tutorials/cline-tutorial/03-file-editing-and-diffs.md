---
layout: default
title: "Chapter 3: File Editing and Diffs"
nav_order: 3
parent: Cline Tutorial
---

# Chapter 3: File Editing and Diffs

Cline's editing power is useful only when diff governance is strong. This chapter covers that governance model.

## Diff-Centric Edit Lifecycle

1. Cline proposes patch
2. human reviews diff
3. approve/reject with targeted feedback
4. run validation command
5. checkpoint or finalize

Never skip step 2 or step 4.

## Review Rubric

| Lens | Key Question |
|:-----|:-------------|
| Scope | Did changes stay in intended files? |
| Semantics | Does code match requested behavior? |
| Safety | Any secret/config/auth risk introduced? |
| Compatibility | Could this break callers/contracts? |
| Maintainability | Is the patch minimal and understandable? |

## Checkpoints and Restore

Cline supports checkpoint-style workflows for comparing/restoring prior states. Use checkpoints before:

- multi-file refactors
- config or dependency changes
- uncertain bugfix attempts
- broad generated code insertions

This enables fast rollback instead of manual repair.

## Patch Acceptance Gates

Require all gates to pass:

- **Scope gate**: no unrelated files changed
- **Quality gate**: implementation matches prompt contract
- **Validation gate**: required commands pass
- **Risk gate**: no unreviewed high-risk edits

## Reject Triggers

Reject patches when you see:

- unexplained dependency/config updates
- hidden binary or generated artifact churn
- large formatting-only noise masking logic edits
- missing command evidence

Then rerun with tighter scope.

## High-Risk File Strategy

Treat these paths with elevated scrutiny:

- auth and permissions
- deployment and CI config
- billing/cost enforcement
- secret/config loaders

For these files, require explicit second review or stricter approval policy.

## Practical Diff Hygiene

- keep tasks small and file-bounded
- ask for one subsystem per iteration
- request changelog-style summary per accepted patch
- avoid accepting multi-concern patches in one step

## Timeline and Audit Value

A clear edit timeline helps with:

- incident analysis
- regression triage
- policy improvement
- compliance evidence

Make sure each accepted change has associated validation context.

## Chapter Summary

You now have a diff governance model that supports:

- safe patch acceptance
- fast rollback with checkpoints
- high-signal review patterns
- auditable change history

Next: [Chapter 4: Terminal and Runtime Tools](04-terminal-and-runtime-tools.md)
