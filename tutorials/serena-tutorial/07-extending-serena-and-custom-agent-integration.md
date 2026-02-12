---
layout: default
title: "Chapter 7: Extending Serena and Custom Agent Integration"
nav_order: 7
parent: Serena Tutorial
---

# Chapter 7: Extending Serena and Custom Agent Integration

This chapter targets advanced users integrating Serena into custom frameworks or extending tool capabilities.

## Learning Goals

- integrate Serena tools into custom agent frameworks
- understand extension points for adding new tools
- map custom additions to existing workflow patterns
- preserve stability while extending functionality

## Integration Paths

| Path | Best For |
|:-----|:---------|
| MCP server mode | rapid use with existing clients |
| OpenAPI bridge via mcpo | clients without MCP support |
| direct framework integration | custom agent stacks requiring deeper control |

## Extension Pattern

Serena documents tool extension via subclassing and implementing tool behavior methods, enabling custom AI capabilities tied to your code domain.

## Source References

- [Custom Agent Guide](https://github.com/oraios/serena/blob/main/docs/03-special-guides/custom_agent.md)
- [Serena on ChatGPT via mcpo](https://github.com/oraios/serena/blob/main/docs/03-special-guides/serena_on_chatgpt.md)
- [Extending Serena](https://github.com/oraios/serena/blob/main/README.md#customizing-and-extending-serena)

## Summary

You now know how to plug Serena into bespoke agent systems and extend it safely.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)
