---
layout: default
title: "Chapter 4: Configuration, Capabilities, and Runtime Modes"
nav_order: 4
parent: Playwright MCP Tutorial
---

# Chapter 4: Configuration, Capabilities, and Runtime Modes

This chapter covers high-impact runtime flags and capability controls.

## Learning Goals

- tune browser, snapshot, and output settings for your workload
- understand capability flags (`vision`, `pdf`, `devtools`)
- pick headed/headless and shared/isolated modes intentionally
- reduce flaky runs through explicit runtime defaults

## High-Impact Configuration Areas

| Area | Key Flags |
|:-----|:----------|
| browser runtime | `--browser`, `--headless`, `--viewport-size` |
| security/network boundaries | `--allowed-origins`, `--blocked-origins` |
| session mode | `--isolated`, `--shared-browser-context`, `--storage-state` |
| response shape | `--snapshot-mode`, `--output-mode`, `--save-trace` |

## Source References

- [README: Configuration](https://github.com/microsoft/playwright-mcp/blob/main/README.md#configuration)
- [README: Configuration File](https://github.com/microsoft/playwright-mcp/blob/main/README.md#configuration-file)

## Summary

You now know which configuration levers matter most for stable operation.

Next: [Chapter 5: Profile State, Extension, and Auth Sessions](05-profile-state-extension-and-auth-sessions.md)
