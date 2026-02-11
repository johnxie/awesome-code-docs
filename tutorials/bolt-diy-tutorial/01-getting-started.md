---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Bolt.diy Tutorial
---

# Chapter 1: Getting Started

This chapter gets bolt.diy running locally and verifies the full prompt-to-edit loop.

## Setup Options

| Path | Best For |
|:-----|:---------|
| local Node + pnpm | active development and customization |
| Docker | isolated, reproducible runtime |
| desktop build | local-first user workflows |

## Local Development Flow

```bash
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy
npm install -g pnpm
pnpm install
cp .env.example .env
cp .env.example .env.local
pnpm run dev
```

## Baseline First Task

After startup, run a small bounded prompt that:

- modifies one component or utility
- shows a reviewable diff
- runs a validation command

This confirms provider setup, file mutation, and runtime validation are all healthy.

## Initial Verification Checklist

- settings panel and provider config load correctly
- prompt returns structured output rather than raw text only
- diff panel exposes exact file-level changes
- validation command results are visible and interpretable

## Summary

You now have bolt.diy running with a safe first-task baseline.

Next: [Chapter 2: Architecture Overview](02-architecture-overview.md)
