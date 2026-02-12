---
layout: default
title: "Chapter 4: Notifications, Logging, and Observability"
nav_order: 4
parent: MCP Ruby SDK Tutorial
---

# Chapter 4: Notifications, Logging, and Observability

This chapter explains runtime observability patterns for Ruby MCP servers.

## Learning Goals

- send list-change notifications correctly for tools/prompts/resources
- configure and emit structured log messages across severity levels
- align server logging behavior with client `logging/setLevel` controls
- avoid noisy or sensitive telemetry in production environments

## Notification and Logging Surfaces

| Surface | Method |
|:--------|:-------|
| Tool list changes | `notify_tools_list_changed` |
| Prompt list changes | `notify_prompts_list_changed` |
| Resource list changes | `notify_resources_list_changed` |
| Structured logs | `notify_log_message` |

## Operational Notes

- notifications require an active transport/session context.
- logging emission is filtered by client-selected log level.
- redact secrets before serialization into log message payloads.

## Source References

- [Ruby SDK README - Notifications](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#notifications)
- [Ruby SDK README - Logging](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#logging)
- [MCP Logging Spec](https://modelcontextprotocol.io/specification/latest/server/utilities/logging)

## Summary

You now have a practical observability model for Ruby MCP services.

Next: [Chapter 5: Transports: stdio, Streamable HTTP, and Session Modes](05-transports-stdio-streamable-http-and-session-modes.md)
