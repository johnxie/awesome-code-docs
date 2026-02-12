---
layout: default
title: "Chapter 7: Conformance Testing and Quality Workflows"
nav_order: 7
parent: MCP Java SDK Tutorial
---

# Chapter 7: Conformance Testing and Quality Workflows

Conformance testing gives Java teams a concrete way to verify protocol fidelity.

## Learning Goals

- run client/server conformance scenarios and interpret output
- understand current known gaps and warning classes
- combine conformance checks with module-level integration tests
- build CI gates that track protocol behavior drift

## Conformance Loop

1. run conformance server scenarios and inspect failing checks
2. run conformance client scenarios against reference servers
3. store check artifacts (`checks.json`, stdout/stderr logs)
4. track pass-rate changes over time, not just one-off success

## Source References

- [Conformance Client README](https://github.com/modelcontextprotocol/java-sdk/blob/main/conformance-tests/client-jdk-http-client/README.md)
- [Conformance Server README](https://github.com/modelcontextprotocol/java-sdk/blob/main/conformance-tests/server-servlet/README.md)
- [SDK Integration Guidance (Referenced)](https://github.com/modelcontextprotocol/conformance/blob/main/SDK_INTEGRATION.md)

## Summary

You now have a repeatable testing process for preventing protocol regressions in Java SDK deployments.

Next: [Chapter 8: Spring Integration and Upgrade Strategy](08-spring-integration-and-upgrade-strategy.md)
