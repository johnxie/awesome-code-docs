---
layout: default
title: "Smolagents Tutorial - Chapter 5: Multi-Step Reasoning"
nav_order: 5
has_children: false
parent: Smolagents Tutorial
---

# Chapter 5: Multi-Step Reasoning

> Break tasks into steps, control depth, and keep the agent on track.

## Configure Iterations

```python
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import DuckDuckGoSearchTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel(),
    max_steps=12,   # allow deeper reasoning
    verbose=True,
)

print(agent.run("""
Research 3 open-source RAG frameworks,
compare embeddings support, vector stores, and licensing,
then recommend one for an enterprise pilot.
"""))
```

## Guide the Plan

- Provide **structure**: ask for numbered steps, tables, or checklists.
- Add **constraints**: word limits, citation requirements, approved sources.
- Use **tool hints**: mention which tools are available to steer the agent.

## Step Auditing Pattern

```python
def run_with_review(agent, prompt):
    history = []
    result = agent.run(prompt, stream=False)
    history.append(result)
    # Persist history, analyze reasoning text, or run lint checks on code blocks
    return result, history
```

## Detecting Drift

- Cap `max_steps` to reduce wandering.
- Check outputs for policy violations; rerun with stricter instructions if needed.
- Keep prompts specific; provide examples of desired format.

## Checklist

- [ ] Set `max_steps` appropriate to task complexity
- [ ] Add structure/constraints to the prompt
- [ ] Review reasoning traces during development
- [ ] Log intermediate steps for auditing

Next: **[Chapter 6: Memory & Context](06-memory.md)** to keep conversations grounded. 🧠
