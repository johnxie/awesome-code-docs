---
layout: default
title: "Chapter 7: Operations, Upgrades, and Observability"
nav_order: 7
parent: Tabby Tutorial
---

# Chapter 7: Operations, Upgrades, and Observability

Long-term reliability comes from disciplined upgrades, backup paths, and visibility into failures.

## Learning Goals

- design an upgrade process with rollback safety in mind
- establish backup and restore routines for metadata and config
- define basic service-level observability for Tabby

## Upgrade Runbook

1. back up Tabby metadata before each upgrade
2. read release notes and changelog for breaking behavior
3. roll out to staging first with representative repositories
4. upgrade production and monitor completion/chat health

## Upgrade Paths

| Deployment Mode | Upgrade Action |
|:----------------|:---------------|
| Docker | pull new image tag and restart service |
| standalone binary | download from releases and replace binary |
| source-based | rebuild from target commit/release |

## Observability Baseline

- service health and uptime checks on API endpoints
- completion latency and error-rate tracking
- indexing job success/failure monitoring
- client connectivity alerts from extension support logs

## Source References

- [Upgrade Guide](https://tabby.tabbyml.com/docs/administration/upgrade)
- [Backup Guide](https://tabby.tabbyml.com/docs/administration/backup)
- [Tabby Releases](https://github.com/TabbyML/tabby/releases)
- [Tabby Changelog](https://github.com/TabbyML/tabby/blob/main/CHANGELOG.md)

## Summary

You now have a practical operations frame for safely evolving Tabby over time.

Next: [Chapter 8: Contribution, Roadmap, and Team Adoption](08-contribution-roadmap-and-team-adoption.md)
