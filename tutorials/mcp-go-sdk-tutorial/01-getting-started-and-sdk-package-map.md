---
layout: default
title: "Chapter 1: Getting Started and SDK Package Map"
nav_order: 1
parent: MCP Go SDK Tutorial
---

# Chapter 1: Getting Started and SDK Package Map

This chapter sets a reliable baseline for starting MCP in Go.

## Learning Goals

- identify the core SDK packages and their roles
- bootstrap minimal client and server programs
- align Go versioning and module policy with SDK expectations
- avoid over-importing packages before architecture is clear

## Package Map

| Package | Purpose |
|:--------|:--------|
| `github.com/modelcontextprotocol/go-sdk/mcp` | primary client/server/session API |
| `github.com/modelcontextprotocol/go-sdk/jsonrpc` | lower-level transport/message plumbing |
| `github.com/modelcontextprotocol/go-sdk/auth` | bearer token middleware and helpers |
| `github.com/modelcontextprotocol/go-sdk/oauthex` | OAuth extensions (resource metadata helpers) |

## First-Run Baseline

```bash
go mod init example.com/mcp-app
go get github.com/modelcontextprotocol/go-sdk/mcp
```

Then build one minimal server over stdio and one minimal client over `CommandTransport` before adding HTTP complexity.

## Source References

- [Go SDK README](https://github.com/modelcontextprotocol/go-sdk/blob/main/README.md)
- [Features Index](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/README.md)
- [pkg.go.dev - mcp](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk/mcp)

## Summary

You now have a clean package and module baseline for Go MCP development.

Next: [Chapter 2: Client/Server Lifecycle and Session Management](02-client-server-lifecycle-and-session-management.md)
