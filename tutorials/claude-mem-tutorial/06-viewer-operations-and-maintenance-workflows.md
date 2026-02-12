---
layout: default
title: "Chapter 6: Viewer Operations and Maintenance Workflows"
nav_order: 6
parent: Claude-Mem Tutorial
---

# Chapter 6: Viewer Operations and Maintenance Workflows

This chapter focuses on day-to-day operation of the viewer, worker, and memory maintenance routines.

## Learning Goals

- use the web viewer for memory inspection and debugging
- manage worker lifecycle and health checks
- run routine maintenance and sanity checks
- keep memory data quality high over long-lived projects

## Operational Surfaces

- viewer UI (`http://localhost:37777`)
- worker status and logs
- session/observation inspection queries
- optional CLI utilities for queue and recovery operations

## Maintenance Checklist

- confirm worker health before major coding sessions
- inspect recent observations for malformed entries
- prune or archive stale data based on team policy
- validate search response quality periodically

## Source References

- [Usage Getting Started](https://docs.claude-mem.ai/usage/getting-started)
- [Architecture Worker Service](https://docs.claude-mem.ai/architecture/worker-service)
- [Export and Import Guide](https://docs.claude-mem.ai/usage/export-import)

## Summary

You now have a repeatable operations checklist for ongoing Claude-Mem usage.

Next: [Chapter 7: Troubleshooting, Recovery, and Reliability](07-troubleshooting-recovery-and-reliability.md)
