---
layout: default
title: "Chapter 6: OAuth, Security, and Auth Workflows"
nav_order: 6
parent: MCP Rust SDK Tutorial
---

# Chapter 6: OAuth, Security, and Auth Workflows

Auth complexity rises quickly in remote MCP deployments; rmcp provides explicit OAuth pathways.

## Learning Goals

- enable OAuth features correctly in build/runtime config
- implement authorization-code flow handling with safer state management
- protect streamable HTTP endpoints and client callbacks
- troubleshoot common OAuth discovery and token-refresh failures

## Security Checklist

- enforce PKCE and secure callback handling
- validate authorization server metadata and discovery fallbacks
- avoid token leakage in logs or panic paths
- test refresh and expiry paths before production rollout

## Source References

- [OAuth Support Guide](https://github.com/modelcontextprotocol/rust-sdk/blob/main/docs/OAUTH_SUPPORT.md)
- [Server Examples - Auth](https://github.com/modelcontextprotocol/rust-sdk/blob/main/examples/servers/README.md)
- [rmcp Changelog - OAuth Fixes](https://github.com/modelcontextprotocol/rust-sdk/blob/main/crates/rmcp/CHANGELOG.md)

## Summary

You now have an OAuth implementation baseline for Rust MCP services and clients.

Next: [Chapter 7: Conformance, Changelog, and Release Discipline](07-conformance-changelog-and-release-discipline.md)
