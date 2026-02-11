---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Bolt.diy Tutorial
---

# Chapter 1: Getting Started

This chapter gets bolt.diy running locally with a clean baseline.

## Local Setup (Node + pnpm)

```bash
git clone https://github.com/stackblitz-labs/bolt.diy.git
cd bolt.diy
npm install -g pnpm
pnpm install
cp .env.example .env
cp .env.example .env.local
pnpm run dev
```

The app runs through Remix + Vite development flow.

## Docker Setup (Isolated Runtime)

```bash
pnpm run dockerbuild
# or production image
pnpm run dockerbuild:prod
```

Then run via compose profiles (`development` or `production`) according to the project’s `docker-compose.yaml` guidance.

## Desktop App Path

bolt.diy also ships Electron binaries and supports building desktop artifacts from source. This is useful for users who want local-native UX and controlled workstation installs.

## First Validation Checklist

- settings panel loads
- provider configuration tab is accessible
- first prompt can generate and apply a simple file change
- diff and snapshot controls are visible

## Summary

You now have a working bolt.diy environment and a baseline for architecture exploration.

Next: [Chapter 2: Architecture Overview](02-architecture-overview.md)
