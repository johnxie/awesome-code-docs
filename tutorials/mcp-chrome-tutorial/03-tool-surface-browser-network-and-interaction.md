---
layout: default
title: "Chapter 3: Tool Surface: Browser, Network, and Interaction"
nav_order: 3
parent: MCP Chrome Tutorial
---

# Chapter 3: Tool Surface: Browser, Network, and Interaction

MCP Chrome exposes a broad tool API that spans tab management, page interaction, network capture, and data operations.

## Learning Goals

- choose the right tool family for each task
- avoid over-broad automation sequences
- design safer multi-step browser workflows

## Tool Families

| Family | Example Tools |
|:-------|:--------------|
| browser management | `get_windows_and_tabs`, `chrome_navigate`, `chrome_switch_tab` |
| network monitoring | capture start/stop, debugger start/stop, custom request |
| content analysis | `chrome_get_web_content`, `search_tabs_content`, interactive element discovery |
| interaction | click, fill/select, keyboard operations |
| data management | history and bookmark operations |

## Selection Heuristics

1. use content extraction before interaction when you need grounding
2. prefer explicit tab targeting in multi-tab sessions
3. gate destructive actions (close/delete) with confirmations in client prompts

## Source References

- [Tools Reference](https://github.com/hangwin/mcp-chrome/blob/master/docs/TOOLS.md)
- [README Tool Summary](https://github.com/hangwin/mcp-chrome/blob/master/README.md)

## Summary

You now understand how to map tasks to the right MCP Chrome tool group with lower failure risk.

Next: [Chapter 4: Semantic Search and Vector Processing](04-semantic-search-and-vector-processing.md)
