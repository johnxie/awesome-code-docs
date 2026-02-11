---
layout: default
title: "Chapter 7: Deployment and Distribution"
nav_order: 7
parent: Bolt.diy Tutorial
---

# Chapter 7: Deployment and Distribution

bolt.diy supports several deployment and packaging paths depending on your use case.

## Web Deployment Targets

The project documents deployment options such as:

- Netlify
- Vercel
- GitHub Pages

These are useful for browser-accessible team instances and demo environments.

## Containerized Deployment

Docker-based profiles support reproducible runtime environments and easier infra automation.

## Desktop Distribution

Electron builds provide native app delivery for macOS, Windows, and Linux workflows where local-first operation is preferred.

## Deployment Decision Matrix

| Target | Best For |
|:-------|:---------|
| Browser-hosted | team sharing and central management |
| Docker/self-hosted | controlled infra and compliance alignment |
| Desktop | local-only power-user workflows |

## Summary

You can now choose and implement the correct distribution strategy for your bolt.diy audience.

Next: [Chapter 8: Production Operations](08-production-operations.md)
