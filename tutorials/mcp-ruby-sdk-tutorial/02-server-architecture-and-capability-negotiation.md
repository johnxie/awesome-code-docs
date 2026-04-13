---
layout: default
title: "Chapter 2: Server Architecture and Capability Negotiation"
nav_order: 2
parent: MCP Ruby SDK Tutorial
---


# Chapter 2: Server Architecture and Capability Negotiation

Welcome to **Chapter 2: Server Architecture and Capability Negotiation**. In this part of **MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how `MCP::Server` handles initialization, method routing, and capability exposure.

## Learning Goals

- map `MCP::Server` responsibilities to JSON-RPC protocol flow
- configure capability surfaces intentionally
- understand built-in MCP methods and extension points
- keep custom method behavior isolated from core protocol methods

## Core Server Method Groups

| Method Group | Purpose |
|:-------------|:--------|
| `initialize`, `ping` | protocol startup and health checks |
| `tools/*`, `prompts/*`, `resources/*` | primitive discovery and execution |
| custom methods | domain-specific RPC extensions |

## Design Guardrails

- do not overload standard MCP methods with application semantics.
- use `define_custom_method` only for non-protocol behaviors.
- keep initialize capability claims synchronized with implemented handlers.

## Source References

- [Ruby SDK README - Building an MCP Server](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#building-an-mcp-server)
- [Ruby SDK README - Supported Methods](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#supported-methods)
- [Ruby SDK README - Custom Methods](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#custom-methods)

## Summary

You now have a server architecture baseline aligned to MCP method and capability semantics.

Next: [Chapter 3: Tools, Prompts, Resources, and Schema Discipline](03-tools-prompts-resources-and-schema-discipline.md)

## Source Code Walkthrough

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

### `conformance/server.rb`

The `server` module in [`conformance/server.rb`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/conformance/server.rb) handles a key part of this chapter's functionality:

```rb
# frozen_string_literal: true

require "rackup"
require "json"
require "uri"
require_relative "../lib/mcp"

module Conformance
  # 1x1 red PNG pixel (matches TypeScript SDK and Python SDK)
  BASE64_1X1_PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

  # Minimal WAV file (matches TypeScript SDK and Python SDK)
  BASE64_MINIMAL_WAV = "UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAA="

  module Tools
    class TestSimpleText < MCP::Tool
      tool_name "test_simple_text"
      description "A tool that returns simple text content"

      class << self
        def call(**_args)
          MCP::Tool::Response.new([MCP::Content::Text.new("This is a simple text response for testing.").to_h])
        end
      end
    end

    class TestImageContent < MCP::Tool
      tool_name "test_image_content"
      description "A tool that returns image content"

      class << self
        def call(**_args)
          MCP::Tool::Response.new([MCP::Content::Image.new(BASE64_1X1_PNG, "image/png").to_h])
        end
      end
```

This module is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.

### `lib/json_rpc_handler.rb`

The `json_rpc_handler` module in [`lib/json_rpc_handler.rb`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/lib/json_rpc_handler.rb) handles a key part of this chapter's functionality:

```rb
# frozen_string_literal: true

require "json"

module JsonRpcHandler
  class Version
    V1_0 = "1.0"
    V2_0 = "2.0"
  end

  class ErrorCode
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    PARSE_ERROR = -32700
  end

  DEFAULT_ALLOWED_ID_CHARACTERS = /\A[a-zA-Z0-9_-]+\z/

  extend self

  def handle(request, id_validation_pattern: DEFAULT_ALLOWED_ID_CHARACTERS, &method_finder)
    if request.is_a?(Array)
      return error_response(id: :unknown_id, id_validation_pattern: id_validation_pattern, error: {
        code: ErrorCode::INVALID_REQUEST,
        message: "Invalid Request",
        data: "Request is an empty array",
      }) if request.empty?

      # Handle batch requests
      responses = request.map { |req| process_request(req, id_validation_pattern: id_validation_pattern, &method_finder) }.compact

      # A single item is hoisted out of the array
      return responses.first if responses.one?
```

This module is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[.rubocop]
    B[server]
    C[json_rpc_handler]
    A --> B
    B --> C
```
