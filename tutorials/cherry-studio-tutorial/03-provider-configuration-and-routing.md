---
layout: default
title: "Chapter 3: Provider Configuration and Routing"
nav_order: 3
parent: Cherry Studio Tutorial
---

# Chapter 3: Provider Configuration and Routing

This chapter covers safe configuration across multiple cloud and local model providers.

## Learning Goals

- configure provider credentials and model options
- combine cloud and local model paths
- design fallback and cost-aware routing patterns
- reduce provider drift across team usage

## Provider Categories

| Category | Examples |
|:---------|:---------|
| cloud model APIs | OpenAI, Gemini, Anthropic and others |
| web service integrations | Claude, Perplexity, Poe |
| local model runtimes | Ollama, LM Studio |

## Control Practices

- keep credentials centralized and rotated
- define approved model list per task class
- separate exploratory and production model presets

## Source References

- [Cherry Studio README: provider support](https://github.com/CherryHQ/cherry-studio/blob/main/README.md#-key-features)
- [Cherry Studio docs](https://docs.cherry-ai.com/docs/en-us)

## Summary

You now can configure provider routing in Cherry Studio with better reliability and governance.

Next: [Chapter 4: Assistants, Topics, and Workflow Design](04-assistants-topics-and-workflow-design.md)
