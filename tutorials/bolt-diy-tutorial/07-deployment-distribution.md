---
layout: default
title: "Chapter 7: Deployment and Distribution"
nav_order: 7
parent: Bolt.diy Tutorial
---

# Chapter 7: Deployment and Distribution

bolt.diy supports browser-hosted, containerized, and desktop distribution models.

## Deployment Matrix

| Target | Best For |
|:-------|:---------|
| Vercel/Netlify/GitHub Pages | shared web usage and demos |
| Docker/self-hosted | controlled infrastructure and compliance |
| Electron desktop | local-first power users |

## Selection Criteria

- choose web deployment for broad team accessibility
- choose Docker when policy and environment control matter
- choose desktop for offline/local-only user profiles

## Release Hygiene

- pin environment variables per target environment
- version deployment configs with application changes
- maintain rollback-ready release artifacts

## Pre-Release Validation Steps

1. smoke test generation and diff flow
2. run target-platform build/deploy command
3. validate auth/provider settings in deployed environment
4. test rollback path before promoting broadly

## Summary

You can now select and operate the right delivery model for your bolt.diy audience.

Next: [Chapter 8: Production Operations](08-production-operations.md)
