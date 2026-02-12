---
layout: default
title: "Chapter 3: Client Integrations and Setup Patterns"
nav_order: 3
parent: Context7 Tutorial
---

# Chapter 3: Client Integrations and Setup Patterns

This chapter covers repeatable integration patterns across different MCP clients.

## Learning Goals

- compare local vs remote deployment tradeoffs
- use API key and OAuth modes correctly
- standardize configuration templates for teams
- prevent client-specific drift

## Integration Modes

| Mode | Benefits | Tradeoffs |
|:-----|:---------|:----------|
| remote HTTP MCP | no local runtime dependency | network dependency |
| local stdio MCP | local execution control | Node/runtime setup overhead |
| OAuth (remote) | token-managed authentication | client OAuth support required |

## Team Template Strategy

- maintain one known-good MCP config per client
- include fallback local config for restricted networks
- keep key/header handling out of committed plaintext configs

## Source References

- [All clients docs](https://context7.com/docs/resources/all-clients)
- [OAuth setup](https://context7.com/docs/howto/oauth)
- [Context7 README client snippets](https://github.com/upstash/context7/blob/master/README.md)

## Summary

You now can deploy Context7 consistently across heterogeneous coding-agent clients.

Next: [Chapter 4: Prompting Strategies and Rules](04-prompting-strategies-and-rules.md)
