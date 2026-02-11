---
layout: default
title: "Chapter 8: Realtime Features"
nav_order: 8
has_children: false
parent: "NocoDB Database Platform"
---

# Chapter 8: Realtime Features

Realtime features keep shared tables consistent across concurrent collaborators.

## Realtime Model

- backend emits row/schema change events
- connected clients subscribe by workspace/table
- clients reconcile updates with local optimistic edits

## Conflict Strategy

- use version counters or timestamps per record
- rebase pending local edits on incoming server events
- surface conflict states explicitly in UI

## Final Summary

You now have complete NocoDB foundations from architecture through realtime collaboration.

Related:
- [NocoDB Index](index.md)
- [Setup Guide](docs/setup.md)
