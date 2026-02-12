---
layout: default
title: "Chapter 3: Authentication, OAuth Callback, and Storage"
nav_order: 3
parent: use-mcp Tutorial
---

# Chapter 3: Authentication, OAuth Callback, and Storage

This chapter covers auth design details that most often fail in browser MCP integrations.

## Learning Goals

- configure callback URL routing and `onMcpAuthorization` handling
- manage popup-based auth flows with user-triggered fallback options
- scope storage keys to avoid cross-app collisions
- clear token/state material safely for logout and recovery scenarios

## Auth Guardrails

1. ensure callback route matches server OAuth registration exactly
2. provide manual auth-link fallback when popups are blocked
3. use distinct storage key prefixes per environment/app
4. clear cached auth state on repeated token or nonce failures

## Source References

- [use-mcp README - Setting Up OAuth Callback](https://github.com/modelcontextprotocol/use-mcp/blob/main/README.md#setting-up-oauth-callback)
- [React Integration README - Callback Route](https://github.com/modelcontextprotocol/use-mcp/blob/main/src/react/README.md#setting-up-the-oauth-callback-route)

## Summary

You now have a safer OAuth and auth-state handling model for React MCP clients.

Next: [Chapter 4: Tools, Resources, Prompts, and Client Operations](04-tools-resources-prompts-and-client-operations.md)
