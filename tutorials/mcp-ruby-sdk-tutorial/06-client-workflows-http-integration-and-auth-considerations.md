---
layout: default
title: "Chapter 6: Client Workflows, HTTP Integration, and Auth Considerations"
nav_order: 6
parent: MCP Ruby SDK Tutorial
---


# Chapter 6: Client Workflows, HTTP Integration, and Auth Considerations

Welcome to **Chapter 6: Client Workflows, HTTP Integration, and Auth Considerations**. In this part of **MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers client-side interaction patterns for Ruby MCP deployments.

## Learning Goals

- use the Ruby client transport interface for HTTP MCP interactions
- orchestrate capability-aware request flows (`tools/list`, `tools/call`, resource/prompt operations)
- handle authorization and session headers cleanly in HTTP contexts
- integrate MCP endpoints into Rails-style controller workflows when needed

## Client Workflow Baseline

1. initialize session and capture protocol/session metadata
2. list server primitives before issuing calls
3. invoke tools/prompts/resources with explicit argument maps
4. process responses/errors and close session state cleanly

## Source References

- [Ruby SDK README - Building an MCP Client](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#building-an-mcp-client)
- [Ruby SDK README - HTTP Transport Layer](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#http-transport-layer)
- [Ruby SDK README - HTTP Authorization](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#http-authorization)
- [Ruby Examples - HTTP Client](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/examples/README.md#3-http-client-example-http_clientrb)

## Summary

You now have a reliable client integration pattern for Ruby MCP over HTTP.

Next: [Chapter 7: Quality, Security, and Release Workflows](07-quality-security-and-release-workflows.md)

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
