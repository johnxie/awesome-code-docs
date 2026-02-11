---
layout: default
title: "Chapter 5: Memory, RAG, and Context"
nav_order: 5
parent: Mastra Tutorial
---

# Chapter 5: Memory, RAG, and Context

Reliable agents depend on structured context, not ever-growing transcripts.

## Context Layers

| Layer | Purpose |
|:------|:--------|
| conversation history | short-term turn continuity |
| working memory | active task state |
| semantic recall | long-term retrieval of prior knowledge |
| RAG context | external knowledge grounding |

## Best Practices

- summarize stale history into compact state
- keep memory writes explicit and scoped
- validate retrieval quality before response generation

## Source References

- [Mastra Memory Docs](https://mastra.ai/docs/memory/conversation-history)
- [Mastra RAG Overview](https://mastra.ai/docs/rag/overview)

## Summary

You now have a maintainable context strategy for long-lived Mastra systems.

Next: [Chapter 6: MCP and Integration Patterns](06-mcp-and-integration-patterns.md)
