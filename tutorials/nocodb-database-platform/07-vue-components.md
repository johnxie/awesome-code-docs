---
layout: default
title: "Chapter 7: Vue Components"
nav_order: 7
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 7: Vue Components

The NocoDB frontend relies on reusable Vue components to support dense data editing workflows.

## Major Component Domains

- data grid and cell editors
- schema/view configuration panels
- filter/sort/query controls
- relation pickers and form controls

## Component Architecture Goals

- keep business logic separate from presentation logic
- centralize server-state synchronization
- avoid duplicated query state handling across views

## Performance Practices

| Practice | Benefit |
|:---------|:--------|
| row virtualization | scalable rendering for large datasets |
| debounced query controls | fewer redundant server roundtrips |
| editor-state isolation | reduces UI jitter during async sync |
| memoized derived state | lower recompute overhead |

## UX Reliability Concerns

- preserve editing intent under latency
- make validation errors field-specific and actionable
- keep keyboard navigation deterministic for power users

## Summary

You can now map NocoDB's frontend responsibilities into maintainable, performance-aware Vue component layers.

Next: [Chapter 8: Realtime Features](08-realtime-features.md)
