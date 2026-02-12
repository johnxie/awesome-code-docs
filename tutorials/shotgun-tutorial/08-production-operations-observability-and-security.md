---
layout: default
title: "Chapter 8: Production Operations, Observability, and Security"
nav_order: 8
parent: Shotgun Tutorial
---

# Chapter 8: Production Operations, Observability, and Security

Production use of Shotgun requires clear controls across CI, runtime telemetry, and deployment boundaries.

## Production Checklist

1. enforce CI gates (lint, tests, typing, secret scan)
2. pin installation/runtime versions in automation
3. manage API keys and telemetry environment variables explicitly
4. monitor errors and performance with configured observability backends

## Deployment Modes

- local/TUI for daily engineering loops
- scripted CLI for CI or batch pipelines
- containerized runtime for isolated web workflows

## Risk Controls

- keep secret scanning active in pipelines
- isolate config and credentials per environment
- treat generated plans/specs as reviewable artifacts before execution

## Source References

- [CI/CD Docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/CI_CD.md)
- [Observability Docs](https://github.com/shotgun-sh/shotgun/blob/main/docs/OBSERVABILITY.md)
- [Docker Guide](https://github.com/shotgun-sh/shotgun/blob/main/docs/DOCKER.md)

## Summary

You now have an operating baseline for running Shotgun in team and production workflows.
