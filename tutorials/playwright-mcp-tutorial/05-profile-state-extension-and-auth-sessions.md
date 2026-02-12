---
layout: default
title: "Chapter 5: Profile State, Extension, and Auth Sessions"
nav_order: 5
parent: Playwright MCP Tutorial
---

# Chapter 5: Profile State, Extension, and Auth Sessions

This chapter explains how to handle authenticated browser contexts safely and reliably.

## Learning Goals

- choose between persistent profile, isolated contexts, and extension mode
- connect to existing browser sessions when needed
- use storage state patterns safely for automation
- avoid leaking sensitive session material in shared environments

## State Strategy

| Mode | Best For | Caution |
|:-----|:---------|:--------|
| persistent profile | ongoing personal workflows | avoid mixing unrelated automations |
| isolated mode | reproducible test-style runs | requires explicit auth state injection |
| extension mode | leveraging already logged-in browser state | protect extension token and profile scope |

## Source References

- [README: User Profile](https://github.com/microsoft/playwright-mcp/blob/main/README.md#user-profile)
- [README: Initial State](https://github.com/microsoft/playwright-mcp/blob/main/README.md#initial-state)
- [Chrome Extension Guide](https://github.com/microsoft/playwright-mcp/blob/main/packages/extension/README.md)

## Summary

You now have a practical model for handling auth/session continuity in browser automation.

Next: [Chapter 6: Standalone and Docker Deployment](06-standalone-and-docker-deployment.md)
