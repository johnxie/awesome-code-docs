---
layout: default
title: "Chapter 6: Query System"
nav_order: 6
has_children: false
parent: "Teable Database Platform"
---

# Chapter 6: Query System

Teable's query system translates configurable views into performant SQL plans.

## Query Capabilities

- composable filters and sort chains
- grouped aggregations and computed fields
- relation-aware joins with scoped field projection

## Query Planning Concerns

- predicate selectivity and index usage
- join cardinality explosion in wide schemas
- pagination correctness under concurrent writes

## Performance Strategies

| Strategy | Result |
|:---------|:-------|
| index-aware filter planning | lower scan cost |
| server-side row limits | predictable load |
| plan inspection on heavy views | faster bottleneck diagnosis |
| query result caching (where safe) | reduced repeated compute |

## Summary

You now understand how Teable balances flexible table UX with predictable query performance.

Next: [Chapter 7: Frontend Architecture](07-frontend-architecture.md)
