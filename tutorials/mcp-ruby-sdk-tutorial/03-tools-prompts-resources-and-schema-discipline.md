---
layout: default
title: "Chapter 3: Tools, Prompts, Resources, and Schema Discipline"
nav_order: 3
parent: MCP Ruby SDK Tutorial
---


# Chapter 3: Tools, Prompts, Resources, and Schema Discipline

Welcome to **Chapter 3: Tools, Prompts, Resources, and Schema Discipline**. In this part of **MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on modeling MCP primitives with predictable behavior and schema quality.

## Learning Goals

- design tool schemas that validate arguments and output shapes reliably
- structure prompt and resource handlers for maintainable growth
- use annotations and metadata consistently across primitives
- avoid schema drift that breaks client interoperability

## Primitive Implementation Checklist

1. define explicit tool argument schemas and output contracts
2. model prompt arguments with stable names and titles
3. expose resource identifiers and templates with clear naming patterns
4. test edge cases for empty, invalid, and over-broad input payloads

## Source References

- [Ruby SDK README - Tools](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#tools)
- [Ruby SDK README - Tool Output Schemas](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#tool-output-schemas)
- [Ruby SDK README - Prompts](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#prompts)
- [Ruby SDK README - Resources](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#resources)

## Summary

You now have a schema-first primitive strategy for Ruby MCP servers.

Next: [Chapter 4: Notifications, Logging, and Observability](04-notifications-logging-and-observability.md)

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
