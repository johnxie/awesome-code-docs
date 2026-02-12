---
layout: default
title: "Chapter 4: Ledger, CRDT, and Causal Consistency"
nav_order: 4
parent: Fireproof Tutorial
---

# Chapter 4: Ledger, CRDT, and Causal Consistency

Fireproof uses ledger and CRDT structures to preserve causal order and integrity across concurrent writers.

## Integrity Model

- write operations go through a queue
- CRDT clock tracks causal progression
- content-addressed history enables verifiable state evolution

## Why It Matters

In collaborative or AI-assisted editing scenarios, this reduces the chance of silent state corruption when concurrent updates happen.

## Source References

- [Ledger implementation](https://github.com/fireproof-storage/fireproof/blob/main/core/base/ledger.ts)
- [Database implementation](https://github.com/fireproof-storage/fireproof/blob/main/core/base/database.ts)
- [Architecture docs](https://use-fireproof.com/docs/architecture)

## Summary

You now understand the core consistency model behind Fireproof write and merge behavior.

Next: [Chapter 5: Storage Gateways and Sync Topology](05-storage-gateways-and-sync-topology.md)
