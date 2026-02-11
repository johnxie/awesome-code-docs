---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: HAPI Tutorial
---

# Chapter 1: Getting Started

This chapter gets HAPI installed and validates a complete first session from terminal to mobile/web control.

## Prerequisites

| Requirement | Purpose |
|:------------|:--------|
| Claude/Codex/Gemini/OpenCode CLI | underlying coding agent runtime |
| Node/npm or Homebrew | HAPI installation path |
| phone/browser access | remote control and approval validation |

## Install and Boot Sequence

```bash
npm install -g @twsxtd/hapi
hapi hub --relay
hapi
```

`hapi server` remains available as an alias for hub startup.

## First Validation Checklist

- hub prints URL + QR code
- login with access token works
- terminal session appears in web UI
- sending message from phone reaches active terminal session

## Fast Troubleshooting

- verify target agent CLI is installed and authenticated
- confirm `HAPI_API_URL` and token values if not using localhost
- check firewall/tunnel settings when remote device cannot connect

## Summary

You now have HAPI installed and a working first local-to-remote control loop.

Next: [Chapter 2: System Architecture](02-system-architecture.md)
