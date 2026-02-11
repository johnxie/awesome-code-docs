---
layout: default
title: "Chapter 4: Remote Access and Networking"
nav_order: 4
parent: HAPI Tutorial
---

# Chapter 4: Remote Access and Networking

HAPI can run local-only or exposed remotely through relay and tunnel strategies.

## Access Modes

| Mode | Best For |
|:-----|:---------|
| local-only (`hapi hub`) | single-machine private usage |
| relay (`hapi hub --relay`) | fast secure remote access |
| self-managed tunnels | custom infra and network governance |

## Networking Considerations

- ensure reachable public URL for remote devices
- preserve SSE compatibility in chosen tunnel setup
- maintain TLS and token-based access controls

## Self-Hosted Tunnel Options

Common patterns include Cloudflare Tunnel (named tunnel), Tailscale, or ngrok-style access.

## Summary

You now have a decision framework for exposing HAPI safely to remote clients.

Next: [Chapter 5: Permissions and Approval Workflow](05-permissions-and-approval-workflow.md)
