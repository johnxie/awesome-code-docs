---
layout: default
title: "Chapter 5: Prebuilt Connectors and Database Patterns"
nav_order: 5
parent: GenAI Toolbox Tutorial
---

# Chapter 5: Prebuilt Connectors and Database Patterns

This chapter covers prebuilt source/tool configurations and connector scaling patterns.

## Learning Goals

- use prebuilt connector options to accelerate onboarding
- evaluate connector choice by operational constraints
- structure multi-database coverage with explicit boundaries
- avoid overloading one toolbox instance with conflicting toolsets

## Connector Strategy

Start with one production-critical source type, validate latency and reliability, then expand connector surface area incrementally using toolsets aligned to concrete use cases.

## Source References

- [Prebuilt Tools Reference](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/reference/prebuilt-tools.md)
- [Source Type Docs](https://github.com/googleapis/genai-toolbox/tree/main/docs/en/resources/sources)
- [Tool Type Docs](https://github.com/googleapis/genai-toolbox/tree/main/docs/en/resources/tools)

## Summary

You now understand how to scale database coverage without losing operational clarity.

Next: [Chapter 6: Deployment and Observability Patterns](06-deployment-and-observability-patterns.md)
