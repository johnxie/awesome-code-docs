---
layout: default
title: "Chapter 5: Block Data Model"
nav_order: 5
has_children: false
parent: "Logseq Knowledge Management"
---

# Chapter 5: Block Data Model

Blocks are the atomic units of content and graph connectivity in Logseq.

## Block Structure

A robust block model typically includes:

- stable UUID/ID
- textual content
- parent-child ordering metadata
- page association
- references/tags/properties
- creation/update metadata

## Invariants

- hierarchy must remain acyclic
- sibling order must be deterministic
- references should survive text edits and reformatting
- deleted/moved blocks should not leave dangling graph edges

## Mutation Types

1. content edit
2. reorder/reparent
3. reference/property change
4. delete/restore

Each mutation should update both hierarchy and graph indexes consistently.

## Validation Practices

- schema validation before persisting
- invariant checks in development/test mode
- repair routines for broken references

## Summary

You can now map user operations to block-level graph mutations and identify where consistency bugs emerge.

Next: [Chapter 6: Block Editor](06-block-editor.md)
