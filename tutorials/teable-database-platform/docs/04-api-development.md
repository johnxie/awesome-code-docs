---
layout: default
title: "Chapter 4: API Development"
nav_order: 4
has_children: false
parent: "Teable Database Platform"
---

# Chapter 4: API Development

Teable exposes both REST and GraphQL APIs on top of its PostgreSQL-native model.

## API Layer Responsibilities

- map table metadata to typed API contracts
- enforce authz and workspace boundaries
- validate payloads before query execution
- return consistent error envelopes

## Endpoint Design Principles

- stable IDs over mutable labels
- pagination by default for list responses
- explicit include/select semantics for relation loading

## Summary

You now understand core API design patterns in Teable.

Next: [Chapter 5: Realtime Collaboration](05-realtime-collaboration.md)
