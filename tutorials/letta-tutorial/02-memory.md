---
layout: default
title: "Letta Tutorial - Chapter 2: Memory Architecture"
nav_order: 2
has_children: false
parent: Letta Tutorial
---

# Chapter 2: Memory Architecture in Letta

Welcome to **Chapter 2: Memory Architecture in Letta**. In this part of **Letta Tutorial: Stateful LLM Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understand core memory, archival memory, and recall memory - the three pillars of persistent agent memory.

## Overview

Letta's memory system is hierarchical and designed to give agents virtually unlimited context. This chapter explores the three types of memory and how they work together.

## The Three Memory Types

### 1. Core Memory

**Core memory** is the agent's "working memory" - the most important information that should always be accessible. It includes:

- Agent identity and persona
- Key facts about the user
- Current goals and context
- Critical instructions

```python
from letta import create_client

client = create_client()

# Get an agent's core memory
agent = client.get_agent("sam")
core_memory = agent.memory

print("Core Memory:")
for memory_block in core_memory:
    print(f"- {memory_block.name}: {memory_block.value}")
```

### 2. Archival Memory

**Archival memory** is long-term storage for facts, events, and information that might be relevant later but isn't needed immediately. It's like the agent's "external hard drive".

```python
# Add to archival memory
client.add_to_archival_memory("sam", "John's favorite programming language is Python")

# Search archival memory
results = client.search_archival_memory("sam", "programming")
```

### 3. Recall Memory

**Recall memory** contains recent conversation history and context. It's automatically managed and provides the immediate conversational context.

```python
# Get recent messages
messages = client.get_messages("sam", limit=10)

for msg in messages:
    print(f"{msg.role}: {msg.content}")
```

## Memory Hierarchy

```
┌─────────────────┐
│   Core Memory   │ ← Always in context, high priority
│   (Identity,    │
│    Key Facts)   │
├─────────────────┤
│  Recall Memory  │ ← Recent conversation, auto-managed
│  (Last N turns) │
├─────────────────┤
│ Archival Memory │ ← Long-term storage, searchable
│  (Facts, Events)│
└─────────────────┘
```

## How Memory Works in Practice

When you send a message:

1. **Core memory** is always included in the context
2. **Recall memory** provides recent conversation history
3. **Archival memory** is searched for relevant information
4. The LLM generates a response
5. New information is automatically stored in appropriate memory types

## Inspecting Memory

View what your agent knows:

```bash
# View core memory
letta get-agent --name sam

# Search archival memory
letta search-memory --name sam --query "python"

# View recent conversations
letta get-messages --name sam --limit 5
```

## Memory Management

### Adding to Core Memory

```python
# Update core memory blocks
client.update_memory_block("sam", "human", "Name: John, Occupation: Developer, Location: SF")
```

### Manual Archival Storage

```python
# Store important facts
client.add_to_archival_memory("sam", "John completed the Python certification on 2024-01-15")
client.add_to_archival_memory("sam", "John prefers dark mode in all applications")
```

### Memory Retrieval

```python
# Semantic search
results = client.search_archival_memory("sam", "certification", top_k=3)

for result in results:
    print(f"Score: {result.score}, Content: {result.content}")
```

## Memory Limits and Optimization

### Context Window Management

Letta automatically manages context to fit within LLM limits:

- **Core memory**: Always included (highest priority)
- **Recall memory**: Recent messages, truncated if needed
- **Archival memory**: Relevant chunks retrieved via search

### Memory Compression

For very long conversations, Letta can compress or summarize older recall memory to save space.

## Practical Examples

### Remembering User Preferences

```bash
$ letta chat --name sam
Human: I prefer coffee over tea, and I'm allergic to nuts.

Assistant: I'll remember you prefer coffee and have a nut allergy. I'll keep this in mind for any food/drink recommendations.

Human: What should I drink in the morning?

Assistant: Based on what you've told me, you prefer coffee over tea. Would you like coffee recommendations?
```

### Learning Over Time

```python
# Agent learns about user's work
client.add_to_archival_memory("sam", "John works on machine learning projects at TechCorp")
client.add_to_archival_memory("sam", "John uses PyTorch for deep learning")
client.add_to_archival_memory("sam", "John is preparing for an ML conference talk")

# Later conversations will reference this knowledge
```

## Memory Persistence

All memory is stored in a local database (SQLite by default) and persists across:

- Agent restarts
- System reboots
- Letta version updates

## Advanced Memory Features

### Memory Blocks

Core memory is organized into blocks:

```python
# View memory blocks
blocks = client.get_memory_blocks("sam")
for block in blocks:
    print(f"{block.name}: {block.value}")
```

### Custom Memory Types

For advanced users, you can create custom memory blocks and retrieval strategies.

## Best Practices

1. **Core Memory**: Keep only essential, frequently-used information
2. **Archival Memory**: Store detailed facts, events, and preferences
3. **Regular Cleanup**: Periodically review and clean up outdated information
4. **Structured Storage**: Use consistent formats for better retrieval

## Memory vs. Traditional Chatbots

| Aspect | Traditional Chatbot | Letta Agent |
|--------|-------------------|-------------|
| Context | Limited to current conversation | Unlimited via hierarchical memory |
| Learning | None | Learns and remembers over time |
| Personalization | Basic | Deeply personalized experiences |
| Consistency | May contradict itself | Maintains consistent knowledge |

Next: Configure agent personalities and behavior with system prompts and models.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `client`, `memory`, `John` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Memory Architecture in Letta` as an operating subsystem inside **Letta Tutorial: Stateful LLM Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `add_to_archival_memory`, `letta` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Memory Architecture in Letta` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `client`.
2. **Input normalization**: shape incoming data so `memory` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `John`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/letta-ai/letta)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `client` and `memory` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Letta](01-getting-started.md)
- [Next Chapter: Chapter 3: Agent Configuration](03-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
