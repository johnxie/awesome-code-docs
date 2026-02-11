---
layout: default
title: "Chapter 5: Component System"
nav_order: 5
has_children: false
parent: "Athens Research Knowledge Graph"
---

# Chapter 5: Component System

This chapter covers how Athens structures reusable Reagent components for pages and blocks.

## Component Layers

- **Page shell**: routing context, page metadata, action controls.
- **Block tree**: recursive renderer for nested blocks.
- **Inline tools**: references, formatting controls, command hints.

## Recursive Block Renderer

```clojure
(defn block-node [{:keys [uuid children text]}]
  [:div.block
   [:div.block-content text]
   (when (seq children)
     [:div.block-children
      (for [child children]
        ^{:key (:uuid child)} [block-node child])])])
```

## Component Quality Rules

- Keep props explicit and minimal.
- Avoid hidden side effects in render functions.
- Memoize expensive derived lists where needed.

## Performance Notes

- Render only expanded block subtrees.
- Use keyed children for stable reconciliation.
- Split heavyweight UI sections into lazy modules.

## Summary

You can now navigate Athens' component boundaries and recursive rendering strategy.

Next: [Chapter 6: Event Handling](06-event-handling.md)
