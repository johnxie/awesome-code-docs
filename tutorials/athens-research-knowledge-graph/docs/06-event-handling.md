---
layout: default
title: "Chapter 6: Event Handling"
nav_order: 6
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 6: Event Handling

Event handling in Athens coordinates editing, linking, and graph updates.

## Event Categories

- Editing events (`:block/update`, `:block/insert`).
- Navigation events (`:page/open`, `:search/select`).
- Sync events (`:sync/push`, `:sync/pull`).

## Example: Safe Block Update

```clojure
(reg-event-fx
  :block/update-text
  (fn [{:keys [db]} [_ block-id new-text]]
    {:db (assoc-in db [:blocks block-id :text] new-text)
     :dispatch-later [{:ms 300 :dispatch [:persist/block block-id]}]}))
```

## Error Strategy

- Validate payload shape at event boundaries.
- Route persistence failures to retry queues.
- Surface actionable user errors in non-blocking banners.

## Summary

You now understand how Athens converts interactions into deterministic state transitions.

Next: [Chapter 7: Block Editor](07-block-editor.md)
