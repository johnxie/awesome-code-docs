---
layout: default
title: "Chapter 8: Team Operations and Governance"
nav_order: 8
parent: OpenSrc Tutorial
---

# Chapter 8: Team Operations and Governance

For team usage, OpenSrc works best with explicit policy on what to fetch, where to reference it, and how to keep it current.

## Team Governance Checklist

- standardize allowed registries and repository hosts
- define source refresh cadence for critical dependencies
- enforce cleanup policy to limit workspace bloat
- document when imported source can be used for decisions versus package APIs

## Suggested Process

1. fetch only high-impact dependencies needed for deep reasoning
2. keep `opensrc/sources.json` aligned with active dependency review scope
3. include source-context checks in PR review guidelines for agent-generated changes

## Source References

- [OpenSrc README](https://github.com/vercel-labs/opensrc/blob/main/README.md)
- [AGENTS integration](https://github.com/vercel-labs/opensrc/blob/main/AGENTS.md)

## Summary

You now have a governance baseline for scaling OpenSrc usage across repositories and teams.
