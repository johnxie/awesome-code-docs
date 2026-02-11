---
layout: default
title: "Chapter 4: Application Architecture"
nav_order: 4
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 4: Application Architecture

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
