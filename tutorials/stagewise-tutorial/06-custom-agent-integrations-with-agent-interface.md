---
layout: default
title: "Chapter 6: Custom Agent Integrations with Agent Interface"
nav_order: 6
parent: Stagewise Tutorial
---

# Chapter 6: Custom Agent Integrations with Agent Interface

Stagewise provides a dedicated interface for wiring custom agents while keeping toolbar protocol behavior stable.

## Learning Goals

- bootstrap a basic custom agent server
- manage availability and state transitions
- handle user messages and streamed responses

## Basic Server Bootstrap

```typescript
import { createAgentServer } from '@stagewise/agent-interface/agent';

const server = await createAgentServer();
server.interface.availability.set(true);
```

## Integration Responsibilities

| Responsibility | Description |
|:---------------|:------------|
| availability | report when agent can accept requests |
| state | communicate working/thinking/completed lifecycle |
| messaging | consume user context and send responses |
| cleanup | remove listeners and free resources |

## Source References

- [Build Custom Agent Integrations](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/developer-guides/build-custom-agent-integrations.mdx)
- [Use Different Agents](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/advanced-usage/use-different-agents.mdx)

## Summary

You now have an implementation map for connecting custom agents into Stagewise workflows.

Next: [Chapter 7: Troubleshooting, Security, and Operations](07-troubleshooting-security-and-operations.md)
