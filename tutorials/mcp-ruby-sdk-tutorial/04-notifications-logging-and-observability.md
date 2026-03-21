---
layout: default
title: "Chapter 4: Notifications, Logging, and Observability"
nav_order: 4
parent: MCP Ruby SDK Tutorial
---


# Chapter 4: Notifications, Logging, and Observability

Welcome to **Chapter 4: Notifications, Logging, and Observability**. In this part of **MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

## Source Code Walkthrough

### `dev.yml`

The `dev` module in [`dev.yml`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/dev.yml) handles a key part of this chapter's functionality:

```yml
name: mcp-ruby

type: ruby

up:
  - ruby
  - bundler

commands:
  console:
    desc: Open console with the gem loaded
    run: bin/console
  build:
    desc: Build the gem using rake build
    run: bin/rake build
  test:
    desc: Run tests
    syntax:
      argument: file
      optional: args...
    run:  |
      if [[ $# -eq 0 ]]; then
        bin/rake test
      else
        bin/rake -I test "$@"
      fi
  style:
    desc: Run rubocop
    aliases: [rubocop, lint]
    run: bin/rake rubocop

```

This module is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.

### `examples/streamable_http_server.rb`

The `streamable_http_server` module in [`examples/streamable_http_server.rb`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/examples/streamable_http_server.rb) handles a key part of this chapter's functionality:

```rb
# frozen_string_literal: true

$LOAD_PATH.unshift(File.expand_path("../lib", __dir__))
require "mcp"
require "rack/cors"
require "rackup"
require "json"
require "logger"

# Create a logger for SSE-specific logging
sse_logger = Logger.new($stdout)
sse_logger.formatter = proc do |severity, datetime, _progname, msg|
  "[SSE] #{severity} #{datetime.strftime("%H:%M:%S.%L")} - #{msg}\n"
end

# Tool that returns a response that will be sent via SSE if a stream is active
class NotificationTool < MCP::Tool
  tool_name "notification_tool"
  description "Returns a notification message that will be sent via SSE if stream is active"
  input_schema(
    properties: {
      message: { type: "string", description: "Message to send via SSE" },
      delay: { type: "number", description: "Delay in seconds before returning (optional)" },
    },
    required: ["message"],
  )

  class << self
    attr_accessor :logger

    def call(message:, delay: 0)
      sleep(delay) if delay > 0

      logger&.info("Returning notification message: #{message}")

```

This module is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.

### `.rubocop.yml`

The `.rubocop` module in [`.rubocop.yml`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/.rubocop.yml) handles a key part of this chapter's functionality:

```yml
inherit_gem:
  rubocop-shopify: rubocop.yml

plugins:
  - rubocop-minitest
  - rubocop-rake

AllCops:
  TargetRubyVersion: 2.7

Gemspec/DevelopmentDependencies:
  Enabled: true

Lint/IncompatibleIoSelectWithFiberScheduler:
  Enabled: true

Minitest/LiteralAsActualArgument:
  Enabled: true

```

This module is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[dev]
    B[streamable_http_server]
    C[.rubocop]
    A --> B
    B --> C
```
