---
layout: default
title: "Chapter 6: Client Primitives: Roots, Sampling, Elicitation, and Tasks"
nav_order: 6
parent: MCP Specification Tutorial
---

# Chapter 6: Client Primitives: Roots, Sampling, Elicitation, and Tasks

Client capabilities are where host policy and model behavior meet.

## Learning Goals

- scope server access with roots and explicit boundaries
- implement sampling loops without losing operator control
- use elicitation form and URL modes safely for sensitive data
- evaluate experimental task workflows before production rollout

## Capability Discipline

- `roots`: keep filesystem or URI boundaries narrow and auditable
- `sampling`: require host/user policy checks before model-mediated execution
- `elicitation`: validate requested schema and use URL mode with strong trust checks
- `tasks`: treat as experimental and isolate behind feature flags until stabilized

## Operational Advice

1. declare only capabilities your host UI and policy engine can enforce
2. log high-risk capability invocations (sampling, elicitation URL mode)
3. test downgrade behavior when peer capability support differs
4. document client behavior for each capability in product security docs

## Source References

- [Client Roots](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/roots.mdx)
- [Client Sampling](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/sampling.mdx)
- [Client Elicitation](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/client/elicitation.mdx)
- [Lifecycle Capability Negotiation](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/lifecycle.mdx)
- [Changelog - Tasks and Elicitation Updates](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)

## Summary

You now have a client capability strategy that keeps power features usable without giving up host control.

Next: [Chapter 7: Authorization and Security Best Practices](07-authorization-and-security-best-practices.md)
