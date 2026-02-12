---
layout: default
title: "Chapter 7: Tooling Surface and Automation Patterns"
nav_order: 7
parent: Playwright MCP Tutorial
---

# Chapter 7: Tooling Surface and Automation Patterns

This chapter translates the full tool catalog into reliable automation patterns.

## Learning Goals

- group tools by workflow stage (observe, act, verify, export)
- design robust loops with snapshot-first actioning
- prefer verification tools over fragile visual assumptions
- build smaller, testable automation steps

## Useful Tool Grouping

| Stage | Representative Tools |
|:------|:---------------------|
| observe | `browser_snapshot`, `browser_console_messages`, `browser_network_requests` |
| act | `browser_click`, `browser_fill_form`, `browser_type`, `browser_select_option` |
| verify | `browser_verify_element_visible`, `browser_verify_text_visible`, `browser_verify_value` |
| artifacts | `browser_take_screenshot`, `browser_pdf_save`, traces/log outputs |

## Source References

- [README: Tools](https://github.com/microsoft/playwright-mcp/blob/main/README.md#tools)
- [README: Key Features](https://github.com/microsoft/playwright-mcp/blob/main/README.md#key-features)

## Summary

You now have a repeatable pattern for stable browser automation loops in agent workflows.

Next: [Chapter 8: Troubleshooting, Security, and Contribution](08-troubleshooting-security-and-contribution.md)
