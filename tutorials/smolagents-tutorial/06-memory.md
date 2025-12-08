---
layout: default
title: "Smolagents Tutorial - Chapter 6: Memory & Context"
nav_order: 6
has_children: false
parent: Smolagents Tutorial
---

# Chapter 6: Memory & Context

> Manage conversation history, short-term scratchpads, and external knowledge for grounded answers.

## Lightweight Conversation Memory

Smolagents does not impose a memory store—pass context yourself.

```python
from smolagents import CodeAgent, HfApiModel

history: list[str] = []
agent = CodeAgent(model=HfApiModel(), tools=[], max_steps=6, verbose=False)


def chat(message: str):
    history.append(f"User: {message}")
    context = "\n".join(history[-6:])  # last 6 turns
    reply = agent.run(f"Conversation so far:\n{context}\n\nUser: {message}\nAssistant:")
    history.append(f"Assistant: {reply}")
    return reply


print(chat("Remember my name is Riley."))
print(chat("What's my name?"))
```

## Integrating External Memory (RAG)

Use your favorite vector store (e.g., Chroma/Qdrant) to retrieve context, then prepend to the prompt.

```python
def answer_with_context(question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n".join(retrieved_chunks)
    prompt = f"Use ONLY this context:\n{context}\n\nQuestion: {question}\nAnswer succinctly."
    return agent.run(prompt)
```

## Tool-Based Knowledge Access

Expose retrieval as a tool so the agent can decide when to call it.

```python
from smolagents import tool


@tool
def search_docs(query: str) -> str:
    """Search internal docs (mock)."""
    return "Doc result for: " + query
```

## Context Hygiene

- Limit history length to avoid token bloat.
- Include **source markers** so the model can cite or decline when missing info.
- Strip PII or sensitive data before storing/passing to models.

## Checklist

- [ ] Keep a rolling conversation history
- [ ] Add retrieval results explicitly to prompts
- [ ] Offer retrieval as a tool when autonomy is needed
- [ ] Prune/clean context to control tokens and protect data

Next: **[Chapter 7: Advanced Patterns](07-advanced.md)** for routing, multi-agent, and safety. 🛠️
