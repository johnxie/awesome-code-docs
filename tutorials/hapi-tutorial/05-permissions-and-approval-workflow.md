---
layout: default
title: "Chapter 5: Permissions and Approval Workflow"
nav_order: 5
parent: HAPI Tutorial
---

# Chapter 5: Permissions and Approval Workflow

Permission requests are where HAPI's remote control model becomes operationally useful and safe.

## Approval Flow

1. agent requests action approval
2. CLI sends request to hub
3. hub broadcasts to PWA/Telegram
4. user approves or denies from remote device
5. decision is relayed back to session

## Policy Guidelines

| Action Class | Recommended Policy |
|:-------------|:-------------------|
| file edits in scoped repo | manual approval |
| command execution | manual approval with command visibility |
| high-risk destructive ops | deny by default |

## Reliability Practices

- require explicit request context for each approval
- track approval latency and denial rates
- maintain audit logs for approval decisions

## Summary

You can now govern remote approvals with clear safety boundaries.

Next: [Chapter 6: PWA, Telegram, and Extensions](06-pwa-telegram-and-extensions.md)
