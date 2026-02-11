---
layout: default
title: "Cline Tutorial"
nav_order: 97
has_children: true
---

# Cline Tutorial: Agentic Coding in Your IDE

> Learn how to use and operate `cline/cline`, an open-source VS Code agent that can edit files, run terminal commands, use browser workflows, and extend itself via MCP.

[![Stars](https://img.shields.io/github/stars/cline/cline?style=social)](https://github.com/cline/cline)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![VS Code](https://img.shields.io/badge/Platform-VS_Code-blue)](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)

## What is Cline?

Cline is an open-source coding agent integrated directly in the editor. It combines model-driven reasoning with tool execution (file edits, terminal commands, browser actions, context retrieval), while keeping a human approval layer for safety.

## Current Snapshot (February 11, 2026)

- repository: `cline/cline`
- stars: ~58K
- latest release line: `v3.57.x`
- active focus areas include tool workflows, checkpoints, and enterprise controls

## Tutorial Chapters

1. **[Chapter 1: Getting Started](01-getting-started.md)** - Install and run Cline in VS Code
2. **[Chapter 2: Agent Workflow](02-agent-workflow.md)** - Task loop and human-in-the-loop approvals
3. **[Chapter 3: File Editing and Diffs](03-file-editing-and-diffs.md)** - Safe code modifications and review flows
4. **[Chapter 4: Terminal and Runtime Tools](04-terminal-and-runtime-tools.md)** - Command execution, long-running tasks, and diagnostics
5. **[Chapter 5: Browser Automation](05-browser-automation.md)** - Visual/runtime debugging with browser interactions
6. **[Chapter 6: MCP and Custom Tools](06-mcp-and-custom-tools.md)** - Extending capabilities through protocol-based tools
7. **[Chapter 7: Context and Cost Control](07-context-and-cost-control.md)** - Large-codebase context handling and token governance
8. **[Chapter 8: Team and Enterprise Operations](08-team-and-enterprise-operations.md)** - Policies, observability, and production governance

## What You Will Learn

- run Cline safely in day-to-day coding workflows
- structure high-quality prompts for deterministic edits
- integrate CLI/browser/MCP tools with approval controls
- operate Cline with cost, security, and team governance guardrails

## Related Tutorials

- [Continue Tutorial](../continue-tutorial/)
- [Aider Tutorial](../aider-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)

---

Ready to begin? Continue to [Chapter 1: Getting Started](01-getting-started.md).
