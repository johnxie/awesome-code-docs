---
layout: default
title: "Chapter 5: ACP and IDE Integrations"
nav_order: 5
parent: Kimi CLI Tutorial
---

# Chapter 5: ACP and IDE Integrations

Kimi CLI can run as an ACP server, enabling IDE and client integrations with multi-session agent workflows.

## ACP Entry Point

```bash
kimi acp
```

## Integration Pattern

- authenticate first in CLI (`/login`)
- configure ACP client to launch `kimi acp`
- create and manage sessions from IDE agent panels

## Use Cases

- Zed/JetBrains ACP integrations
- custom ACP clients for internal tooling
- multi-session concurrent agent workflows

## Source References

- [Kimi README: ACP integration](https://github.com/MoonshotAI/kimi-cli/blob/main/README.md)
- [ACP reference](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/reference/kimi-acp.md)

## Summary

You now have a pathway to use Kimi beyond standalone terminal sessions.

Next: [Chapter 6: Shell Mode, Print Mode, and Wire Mode](06-shell-mode-print-mode-and-wire-mode.md)
