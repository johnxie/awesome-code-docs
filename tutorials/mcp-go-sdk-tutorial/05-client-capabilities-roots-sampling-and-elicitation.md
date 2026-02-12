---
layout: default
title: "Chapter 5: Client Capabilities: Roots, Sampling, and Elicitation"
nav_order: 5
parent: MCP Go SDK Tutorial
---

# Chapter 5: Client Capabilities: Roots, Sampling, and Elicitation

Client capability behavior should be explicit and policy-aware.

## Learning Goals

- configure roots and roots change notifications predictably
- implement sampling and elicitation handlers with strong controls
- manage inferred vs explicit capabilities in `ClientOptions`
- prevent accidental capability over-advertising

## Capability Strategy

- use `Client.AddRoots`/`RemoveRoots` for dynamic boundary updates
- wire `CreateMessageHandler` only when sampling behavior is governed
- wire `ElicitationHandler` and declare form/URL support explicitly
- override defaults by setting `ClientOptions.Capabilities` when needed

## Practical Guardrails

1. treat URL-mode elicitation as higher-risk than form mode
2. validate elicited content against requested schema before use
3. disable unnecessary default capabilities for minimal hosts
4. document capabilities for every deployment profile

## Source References

- [Client Features](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/client.md)
- [Protocol Security Section](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md#security)
- [pkg.go.dev - ClientOptions](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk/mcp#ClientOptions)

## Summary

You now have a client capability model that keeps advanced features controlled and observable.

Next: [Chapter 6: Auth, Security, and Runtime Hardening](06-auth-security-and-runtime-hardening.md)
