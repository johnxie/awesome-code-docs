---
layout: default
title: "Chapter 4: Multi-Provider Conversion and Config Sync"
nav_order: 4
parent: Compound Engineering Plugin Tutorial
---

# Chapter 4: Multi-Provider Conversion and Config Sync

This chapter covers cross-platform conversion features for teams using multiple coding-agent runtimes.

## Learning Goals

- convert compound plugin assets to OpenCode, Codex, and Droid targets
- sync personal Claude config into alternate runtimes
- understand output paths and provider-specific constraints
- avoid format-loss pitfalls in cross-provider migration

## Conversion Commands

```bash
bunx @every-env/compound-plugin install compound-engineering --to opencode
bunx @every-env/compound-plugin install compound-engineering --to codex
bunx @every-env/compound-plugin install compound-engineering --to droid
```

## Sync Commands

```bash
bunx @every-env/compound-plugin sync --target opencode
bunx @every-env/compound-plugin sync --target codex
```

## Portability Considerations

- command/skill semantics differ by runtime
- some provider limits require description truncation or schema adaptation
- output directories and file contracts differ per target

## Source References

- [README Multi-Target Install](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md#opencode-codex--droid-experimental-install)
- [README Sync Personal Config](https://github.com/EveryInc/compound-engineering-plugin/blob/main/README.md#sync-personal-config)
- [Codex Spec Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/specs/codex.md)
- [OpenCode Spec Notes](https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/specs/opencode.md)

## Summary

You now understand how to move compound workflows across different coding-agent stacks.

Next: [Chapter 5: MCP Integrations and Browser Automation](05-mcp-integrations-and-browser-automation.md)
