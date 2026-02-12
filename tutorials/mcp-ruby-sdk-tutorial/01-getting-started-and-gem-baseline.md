---
layout: default
title: "Chapter 1: Getting Started and Gem Baseline"
nav_order: 1
parent: MCP Ruby SDK Tutorial
---

# Chapter 1: Getting Started and Gem Baseline

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
