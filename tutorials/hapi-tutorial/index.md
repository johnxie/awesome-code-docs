---
layout: default
title: "HAPI Tutorial"
nav_order: 100
has_children: true
---

# HAPI Tutorial: Remote Control for Local AI Coding Sessions

> Learn `tiann/hapi`, a local-first hub that lets you run Claude Code/Codex/Gemini/OpenCode sessions locally while controlling and approving them remotely.

[![Stars](https://img.shields.io/github/stars/tiann/hapi?style=social)](https://github.com/tiann/hapi)
[![License](https://img.shields.io/badge/License-AGPL_3.0-blue.svg)](https://opensource.org/licenses/AGPL-3.0)
[![Docs](https://img.shields.io/badge/Docs-hapi.run-orange)](https://hapi.run)

## What is HAPI?

HAPI wraps existing coding agents and adds a hub/web control plane so sessions can be handed off between terminal and phone/browser without restarting context.

## Current Snapshot (February 11, 2026)

- repository: `tiann/hapi`
- stars: ~1.4K
- latest release line: `v0.15.x` (`v0.15.2` published February 11, 2026)
- license: AGPL-3.0
- key capabilities: remote approvals, PWA control, Telegram integration, multi-machine session routing

## Tutorial Chapters

1. **[Chapter 1: Getting Started](01-getting-started.md)** - install HAPI, start hub, and launch first wrapped agent session
2. **[Chapter 2: System Architecture](02-system-architecture.md)** - CLI, hub, web app, and protocol boundaries
3. **[Chapter 3: Session Lifecycle and Handoff](03-session-lifecycle-and-handoff.md)** - local-to-remote control flow and state continuity
4. **[Chapter 4: Remote Access and Networking](04-remote-access-and-networking.md)** - relay mode, tunnels, and secure exposure patterns
5. **[Chapter 5: Permissions and Approval Workflow](05-permissions-and-approval-workflow.md)** - mobile approvals, policy boundaries, and safety controls
6. **[Chapter 6: PWA, Telegram, and Extensions](06-pwa-telegram-and-extensions.md)** - user interfaces, notifications, and ecosystem integration
7. **[Chapter 7: Configuration and Security](07-configuration-and-security.md)** - tokens, env vars, secrets handling, and access governance
8. **[Chapter 8: Production Operations](08-production-operations.md)** - observability, scaling, and incident runbooks

## What You Will Learn

- run a local-first AI coding stack with remote control
- design safe approval policies for agent tool access
- operate HAPI across multiple machines and networks
- harden and monitor HAPI for team usage

## Related Tutorials

- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [MCP Servers Tutorial](../mcp-servers-tutorial/)

---

Ready to begin? Continue to [Chapter 1: Getting Started](01-getting-started.md).
