---
layout: default
title: "Chapter 4: Application Architecture"
nav_order: 4
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 4: Application Architecture

Welcome to **Chapter 4: Application Architecture**. In this part of **Athens Research: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains Athens' app architecture around Re-frame event flow and UI composition.

## Core Architecture Pattern

Athens uses a classic Re-frame loop:

1. UI dispatches an event.
2. Event handler produces effects.
3. Effects update Datascript-backed app state.
4. Subscriptions recompute derived views.
5. Reagent components re-render.

## Important Design Boundaries

- Keep data normalization in event handlers and effects.
- Keep view components declarative and subscription-driven.
- Keep business workflows explicit in event namespaces.

## Event and Subscription Layout

```clojure
(ns athens.events)
(reg-event-fx
  :page/open
  (fn [{:keys [db]} [_ page-id]]
    {:db (assoc db :ui/current-page page-id)
     :dispatch [:graph/load-page page-id]}))

(reg-sub
  :ui/current-page
  (fn [db _] (:ui/current-page db)))
```

## Reliability Practices

- Prefer idempotent handlers for repeated UI actions.
- Separate optimistic UI updates from persistence effects.
- Log event IDs for debugging long state transitions.

## Summary

You can now reason about Athens' event-driven architecture and where to place logic.

Next: [Chapter 5: Component System](05-component-system.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `page`, `current`, `athens` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Application Architecture` as an operating subsystem inside **Athens Research: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `events`, `event`, `open` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Application Architecture` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `page`.
2. **Input normalization**: shape incoming data so `current` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `athens`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Athens Research](https://github.com/athensresearch/athens)
  Why it matters: authoritative reference on `Athens Research` (github.com).

Suggested trace strategy:
- search upstream code for `page` and `current` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Schema Design](03-schema-design.md)
- [Next Chapter: Chapter 5: Component System](05-component-system.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
