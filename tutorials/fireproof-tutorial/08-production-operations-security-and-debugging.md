---
layout: default
title: "Chapter 8: Production Operations, Security, and Debugging"
nav_order: 8
parent: Fireproof Tutorial
---

# Chapter 8: Production Operations, Security, and Debugging

Production Fireproof deployments need explicit practices for observability, key handling, and test discipline.

## Operations Checklist

1. define storage and sync boundaries per environment
2. validate backup/recovery behavior of persisted stores
3. enforce version pinning in lockfiles and CI
4. run representative integration tests for gateway paths

## Debugging Controls

- use `FP_DEBUG` for targeted module logging
- standardize log format options per environment (`json`, `yaml`, etc.)
- track sync and conflict behavior during load and offline/online transitions

## Security Notes

- treat key material management as a first-class deployment concern
- audit any insecure/deprecated key extraction behavior before production use
- document trust model when syncing over shared object storage

## Source References

- [Fireproof README: debug and keybag notes](https://github.com/fireproof-storage/fireproof/blob/main/README.md)
- [CI workflow set](https://github.com/fireproof-storage/fireproof/tree/main/.github/workflows)

## Summary

You now have a practical baseline for operating Fireproof in production-grade app workflows.
