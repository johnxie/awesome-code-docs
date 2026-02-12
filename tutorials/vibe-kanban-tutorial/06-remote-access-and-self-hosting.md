---
layout: default
title: "Chapter 6: Remote Access and Self-Hosting"
nav_order: 6
parent: Vibe Kanban Tutorial
---

# Chapter 6: Remote Access and Self-Hosting

This chapter covers remote deployment patterns, editor integration, and secure remote operations.

## Learning Goals

- expose remote Vibe Kanban instances safely
- configure SSH-based project opening workflows
- use origin controls for reverse-proxy deployments
- support distributed teams with shared remote infrastructure

## Remote Operation Pattern

| Capability | Approach |
|:-----------|:---------|
| remote UI access | tunnel/proxy (Cloudflare Tunnel, ngrok, etc.) |
| remote project editing | configure remote SSH host/user integration |
| browser security | set explicit `VK_ALLOWED_ORIGINS` |

## Source References

- [Vibe Kanban README: Self-Hosting](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#self-hosting)
- [Vibe Kanban README: Remote Deployment](https://github.com/BloopAI/vibe-kanban/blob/main/README.md#remote-deployment)
- [Vibe Kanban Self-Hosting Guide](https://vibekanban.com/docs/self-hosting)

## Summary

You now know how to run Vibe Kanban beyond a single local machine safely.

Next: [Chapter 7: Development and Source Build Workflow](07-development-and-source-build-workflow.md)
