---
layout: default
title: "Chapter 7: Reliability, Rate Limits, and Version Fallbacks"
nav_order: 7
parent: OpenSrc Tutorial
---

# Chapter 7: Reliability, Rate Limits, and Version Fallbacks

Real-world source fetching must account for imperfect metadata, missing tags, and API rate limits.

## Built-In Fallback Patterns

- if exact tag is missing, clone default branch with warning
- if package repo metadata is missing, return explicit error
- if host APIs rate-limit requests, surface actionable failures

## Reliability Practices

1. pin critical imports to explicit versions where possible
2. cache fetched sources in CI workspace artifacts for repeatability
3. monitor for registry/API availability issues in automation jobs

## Source References

- [Git clone fallback behavior](https://github.com/vercel-labs/opensrc/blob/main/src/lib/git.ts)
- [GitHub/GitLab repo resolution behavior](https://github.com/vercel-labs/opensrc/blob/main/src/lib/repo.ts)

## Summary

You now understand how OpenSrc behaves under common failure modes and how to design safer workflows around them.

Next: [Chapter 8: Team Operations and Governance](08-team-operations-and-governance.md)
