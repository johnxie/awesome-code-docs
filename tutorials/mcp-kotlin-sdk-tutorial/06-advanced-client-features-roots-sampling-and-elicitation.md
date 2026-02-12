---
layout: default
title: "Chapter 6: Advanced Client Features: Roots, Sampling, and Elicitation"
nav_order: 6
parent: MCP Kotlin SDK Tutorial
---

# Chapter 6: Advanced Client Features: Roots, Sampling, and Elicitation

This chapter covers advanced client features that materially affect user control and context boundaries.

## Learning Goals

- manage roots and contextual scope correctly
- apply sampling flows with explicit user-governed behavior
- understand elicitation support and capability gating
- avoid overexposing local context to remote server workflows

## Advanced Feature Guardrails

1. enable only required client capabilities (`roots`, `sampling`, `elicitation`)
2. track when server requests expand context boundaries
3. keep user-facing approvals around high-impact sampling/tool actions
4. log capability and session metadata for debugging and auditability

## Source References

- [Kotlin SDK README - Client Features](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/README.md#client-features)
- [kotlin-sdk-client Module Guide - Feature Usage Highlights](https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/kotlin-sdk-client/Module.md)
- [MCP Specification - Client Features](https://modelcontextprotocol.io/specification/2025-11-25)

## Summary

You now have a control-oriented strategy for advanced Kotlin client capabilities.

Next: [Chapter 7: Testing, Conformance, and Operational Diagnostics](07-testing-conformance-and-operational-diagnostics.md)
