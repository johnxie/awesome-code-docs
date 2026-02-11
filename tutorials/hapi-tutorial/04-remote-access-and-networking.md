---
layout: default
title: "Chapter 4: Remote Access and Networking"
nav_order: 4
parent: HAPI Tutorial
---

# Chapter 4: Remote Access and Networking

Networking design determines whether HAPI is simple local tooling or production remote infrastructure.

## Access Modes

| Mode | Strength |
|:-----|:---------|
| local-only (`hapi hub`) | tight isolation and low setup overhead |
| relay (`hapi hub --relay`) | quick secure internet access |
| self-hosted tunnel/public host | full routing and policy ownership |

## Network Requirements

- stable SSE-compatible ingress path
- TLS for remote clients
- explicit host/port/public URL configuration
- firewall rules matching hub ingress and tunnel design

## Deployment Pattern

1. validate local-only mode
2. enable relay or named tunnel
3. test phone/browser connectivity and auth
4. verify reconnect behavior under network interruption

## Summary

You now have a practical network rollout sequence for safe remote HAPI access.

Next: [Chapter 5: Permissions and Approval Workflow](05-permissions-and-approval-workflow.md)
