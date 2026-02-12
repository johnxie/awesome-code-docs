---
layout: default
title: "Chapter 5: Security, Auth, and Network Hardening"
nav_order: 5
parent: MCP Inspector Tutorial
---

# Chapter 5: Security, Auth, and Network Hardening

Inspector's proxy can spawn local processes and connect to arbitrary endpoints, so hardening defaults matters.

## Learning Goals

- keep authentication enabled and token scope tight
- use local-only binding as a default posture
- configure allowed origins for DNS rebinding defense
- understand risks of disabling auth

## Hardening Checklist

| Control | Recommended Setting | Why |
|:--------|:--------------------|:----|
| Proxy auth | enabled | blocks unauthorized requests to process-spawning proxy |
| Binding | localhost only | reduces LAN exposure |
| Origins | explicit allowlist | protects against DNS rebinding attacks |
| `DANGEROUSLY_OMIT_AUTH` | never in routine dev | large local compromise risk |

## High-Risk Anti-Pattern

Avoid using `DANGEROUSLY_OMIT_AUTH=true` unless you are in a tightly isolated throwaway environment with a clear security reason.

## Source References

- [Inspector README - Security Considerations](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#security-considerations)
- [Inspector README - Local-only Binding](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#local-only-binding)
- [Inspector README - DNS Rebinding Protection](https://github.com/modelcontextprotocol/inspector/blob/main/README.md#dns-rebinding-protection)

## Summary

You now have a concrete baseline for safer Inspector operation.

Next: [Chapter 6: Configuration, Timeouts, and Runtime Tuning](06-configuration-timeouts-and-runtime-tuning.md)
