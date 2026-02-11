---
layout: default
title: "Chapter 5: Permissions and Approval Workflow"
nav_order: 5
parent: HAPI Tutorial
---

# Chapter 5: Permissions and Approval Workflow

Remote approvals are the core safety boundary when agents request actions.

## Approval Event Flow

1. agent emits permission request
2. CLI forwards request to hub
3. hub stores and broadcasts to PWA/Telegram
4. operator approves/denies
5. decision returns to active session

## Policy Matrix

| Request Type | Recommended Policy |
|:-------------|:-------------------|
| scoped file edits | approve with diff visibility |
| command execution | require explicit command preview |
| destructive/system-wide actions | deny by default |

## Operational Controls

- enforce timeout for unresolved approvals
- require request metadata (target file/command/context)
- retain immutable approval logs for audit and incident review

## Summary

You now have a governance model for remote permission handling in HAPI.

Next: [Chapter 6: PWA, Telegram, and Extensions](06-pwa-telegram-and-extensions.md)
