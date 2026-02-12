---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Fireproof Tutorial
---

# Chapter 1: Getting Started

This chapter gets Fireproof running with both React-hook and core API entry points.

## Quick Start

```bash
npm install use-fireproof
```

Or core API only:

```bash
npm install @fireproof/core
```

## Minimal Core Example

```js
import { fireproof } from "@fireproof/core";

const db = fireproof("music-app");
await db.put({ _id: "beyonce", name: "Beyonce", hitSingles: 29 });
const doc = await db.get("beyonce");
```

## Learning Goals

- initialize a Fireproof database
- write and read documents
- confirm local-first behavior in your runtime

## Source References

- [Fireproof README: installation](https://github.com/fireproof-storage/fireproof/blob/main/README.md)

## Summary

You now have Fireproof running with a minimal document lifecycle.

Next: [Chapter 2: Core Document API and Query Lifecycle](02-core-document-api-and-query-lifecycle.md)
