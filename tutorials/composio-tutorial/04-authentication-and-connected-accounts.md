---
layout: default
title: "Chapter 4: Authentication and Connected Accounts"
nav_order: 4
parent: Composio Tutorial
---

# Chapter 4: Authentication and Connected Accounts

This chapter covers authentication architecture and connected-account lifecycle management.

## Learning Goals

- distinguish auth configs from connected accounts clearly
- choose between in-chat and manual authentication flows
- model token lifecycle and account state transitions safely
- enforce least-privilege scope and account governance practices

## Authentication Model

Composio uses Connect Links and auth configs to standardize OAuth/API key setup across users. Connected accounts bind user-specific credentials to toolkit access.

For product UX, two common approaches exist:

- in-chat auth prompts for conversational agents
- manual onboarding flows for app-managed account linking

## Governance Checklist

| Control | Baseline |
|:--------|:---------|
| scope control | request only required toolkit permissions |
| account visibility | expose connected-account status in admin/debug views |
| lifecycle events | handle disabled/revoked/expired states explicitly |
| multi-account support | support work/personal account separation where needed |

## Source References

- [Authentication](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/authentication.mdx)
- [Manual Authentication](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/authenticating-users/manually-authenticating.mdx)
- [Connected Accounts](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/auth-configuration/connected-accounts.mdx)

## Summary

You now have a safer authentication foundation for multi-user production systems.

Next: [Chapter 5: Tool Execution Modes and Modifiers](05-tool-execution-modes-and-modifiers.md)
