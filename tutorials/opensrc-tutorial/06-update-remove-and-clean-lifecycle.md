---
layout: default
title: "Chapter 6: Update, Remove, and Clean Lifecycle"
nav_order: 6
parent: OpenSrc Tutorial
---

# Chapter 6: Update, Remove, and Clean Lifecycle

OpenSrc includes commands for incremental refresh and cleanup of source caches.

## Lifecycle Commands

```bash
opensrc zod                # refresh source for package
opensrc remove zod         # remove package source
opensrc remove owner/repo  # remove repository source
opensrc clean              # remove all tracked sources
opensrc clean --npm        # remove only npm package sources
```

## Maintenance Strategy

- re-run fetch for packages tied to updated lockfiles
- remove stale imports to reduce local noise
- use targeted clean modes per ecosystem when needed

## Source References

- [remove command](https://github.com/vercel-labs/opensrc/blob/main/src/commands/remove.ts)
- [clean command](https://github.com/vercel-labs/opensrc/blob/main/src/commands/clean.ts)
- [list command](https://github.com/vercel-labs/opensrc/blob/main/src/commands/list.ts)

## Summary

You now have operational control over source import lifecycle and cache hygiene.

Next: [Chapter 7: Reliability, Rate Limits, and Version Fallbacks](07-reliability-rate-limits-and-version-fallbacks.md)
