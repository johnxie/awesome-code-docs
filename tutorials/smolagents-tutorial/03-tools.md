---
layout: default
title: "Smolagents Tutorial - Chapter 3: Tools & Functions"
nav_order: 3
has_children: false
parent: Smolagents Tutorial
---

# Chapter 3: Tools & Functions

> Add built-in tools and craft custom ones with clear contracts, type hints, and safe behaviors.

## Built-in Tools (examples)

- `DuckDuckGoSearchTool` — web search
- `VisitWebpageTool` — fetch page content
- `CalculatorTool` — math
- `PythonREPLTool` — execute Python code (use cautiously)

```python
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import DuckDuckGoSearchTool, VisitWebpageTool, CalculatorTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool(), CalculatorTool()],
    model=HfApiModel(),
    max_steps=8,
    verbose=True,
)

print(agent.run("Find the latest Mistral release, then estimate its model size in MB."))
```

## Custom Tools with `@tool`

```python
from smolagents import tool
from typing import List


@tool
def top_k(items: List[str], k: int = 3) -> List[str]:
    """Return the top-k items (first k)."""
    return items[:k]


@tool
def format_summary(title: str, bullets: List[str]) -> str:
    """Format a markdown summary."""
    lines = "\n".join(f"- {b}" for b in bullets)
    return f"## {title}\n{lines}"
```

## Register Tools on Agents

```python
from smolagents import CodeAgent, HfApiModel

agent = CodeAgent(
    tools=[top_k, format_summary],
    model=HfApiModel(),
    max_steps=6,
)

print(agent.run("Summarize the top 3 takeaways from 'agents, memory, planning, evaluation, deployment'."))
```

## Tool Design Tips

- Write **docstrings** that describe intent, args, and outputs—LLMs rely on them.
- Keep tools **deterministic** and side-effect free unless explicitly needed.
- Validate inputs and raise friendly errors; set `stop_on_error=True` when you want failures to halt.
- Return structured data (dicts/lists) so the agent can compose results.

## Testing Tools

```python
def test_top_k():
    assert top_k(["a", "b", "c", "d"], k=2) == ["a", "b"]
```

Next: **[Chapter 4: Code Execution](04-code-execution.md)** to safely run agent-written Python. 🐍
