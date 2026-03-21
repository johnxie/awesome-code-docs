---
layout: default
title: "Chapter 1: Getting Started and Gem Baseline"
nav_order: 1
parent: MCP Ruby SDK Tutorial
---


# Chapter 1: Getting Started and Gem Baseline

Welcome to **Chapter 1: Getting Started and Gem Baseline**. In this part of **MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter sets up a reliable Ruby baseline for MCP server/client development.

## Learning Goals

- install and pin the `mcp` gem correctly
- align Ruby runtime and dependency prerequisites
- establish a first-run workflow for server/client validation
- avoid environment drift before adding protocol features

## Baseline Setup

```ruby
gem 'mcp'
```

After adding to `Gemfile`, run `bundle install`, then validate against a simple stdio or HTTP sample.

## First-Run Checklist

1. pin gem version for reproducible builds
2. run at least one server example and one client example
3. verify JSON-RPC request/response flow before custom methods
4. add environment-level logging early for troubleshooting

## Source References

- [Ruby SDK README - Installation](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/README.md#installation)
- [Ruby Examples Index](https://github.com/modelcontextprotocol/ruby-sdk/blob/main/examples/README.md)
- [RubyGems Package](https://rubygems.org/gems/mcp)

## Summary

You now have a stable Ruby MCP baseline for deeper server/client implementation.

Next: [Chapter 2: Server Architecture and Capability Negotiation](02-server-architecture-and-capability-negotiation.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `conformance/server.rb`

The `schemas` interface in [`conformance/server.rb`](https://github.com/modelcontextprotocol/ruby-sdk/blob/HEAD/conformance/server.rb) handles a key part of this chapter's functionality:

```rb
    class TestElicitationSep1330Enums < MCP::Tool
      tool_name "test_elicitation_sep1330_enums"
      description "A tool that tests elicitation with enum schemas"

      class << self
        def call(**_args)
          MCP::Tool::Response.new(
            [MCP::Content::Text.new("Elicitation not supported in this SDK version").to_h],
            error: true,
          )
        end
      end
    end

    class TestReconnection < MCP::Tool
      tool_name "test_reconnection"
      description "A tool that triggers SSE stream closure to test client reconnection behavior"

      class << self
        def call(**_args)
          MCP::Tool::Response.new([MCP::Content::Text.new("Reconnection test completed").to_h])
        end
      end
    end
  end

  module Prompts
    class TestSimplePrompt < MCP::Prompt
      prompt_name "test_simple_prompt"
      description "A simple prompt for testing with no arguments"

      class << self
```

This interface is important because it defines how MCP Ruby SDK Tutorial: Building MCP Servers and Clients in Ruby implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[schemas]
```
