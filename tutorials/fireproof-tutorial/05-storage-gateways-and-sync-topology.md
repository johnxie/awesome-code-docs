---
layout: default
title: "Chapter 5: Storage Gateways and Sync Topology"
nav_order: 5
parent: Fireproof Tutorial
---

# Chapter 5: Storage Gateways and Sync Topology

Fireproof supports multiple storage gateways and environment-aware persistence paths.

## Gateway Landscape

| Gateway | Typical Runtime |
|:--------|:----------------|
| IndexedDB | browser local persistence |
| File-based gateways | Node and filesystem runtimes |
| Memory gateway | tests and ephemeral sessions |
| Cloud protocols | synchronized multi-device flows |

## Topology Guidance

- start local with browser/file gateway
- layer sync after local behavior is correct
- test conflict and recovery paths early for collaboration-heavy apps

## Source References

- [IndexedDB gateway](https://github.com/fireproof-storage/fireproof/blob/main/core/gateways/indexeddb/gateway-impl.ts)
- [Gateway modules tree](https://github.com/fireproof-storage/fireproof/tree/main/core/gateways)

## Summary

You now have a storage and sync topology model for different deployment targets.

Next: [Chapter 6: Files, Attachments, and Rich Data Flows](06-files-attachments-and-rich-data-flows.md)
