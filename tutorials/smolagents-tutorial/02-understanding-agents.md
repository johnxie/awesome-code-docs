---
layout: default
title: "Smolagents Tutorial - Chapter 2: Understanding Agents"
nav_order: 2
has_children: false
parent: Smolagents Tutorial
---

# Chapter 2: Understanding Smolagents

> Compare agent types, execution modes, and configuration knobs to pick the right setup.

## Agent Types

| Agent | Best For | How it works |
|:------|:---------|:-------------|
| **CodeAgent** | Flexible reasoning, data wrangling, calling many tools | LLM writes Python, executes code, loops with tools |
| **ToolCallingAgent** | Strict, auditable tool calls | LLM chooses from registered tools via function-calling interface |

## Config Options (common)

- `model`: LLM backend (`HfApiModel`, `OpenAIServerModel`, `AnthropicModel`, `LiteLLMModel`)
- `tools`: list of callable tools (decorated with `@tool`)
- `max_steps`: cap iterations to prevent runaway loops
- `verbose`: print reasoning/actions (useful for debugging)
- `stop_on_error`: stop at first tool error (default False; set True for safety)

## CodeAgent Example (analysis heavy)

```python
from smolagents import CodeAgent, HfApiModel
from smolagents.tools import DuckDuckGoSearchTool

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel(model_id="meta-llama/Llama-3.1-70B-Instruct"),
    max_steps=10,
    verbose=True,
)

print(agent.run("Find the top 3 vector databases and compare features in a table."))
```

## ToolCallingAgent Example (strict tools)

```python
from smolagents import ToolCallingAgent, OpenAIServerModel, tool


@tool
def fetch_repo_stars(repo: str) -> int:
    """Mock: return stars for a repo (replace with GitHub API)."""
    return {"microsoft/semantic-kernel": 25000, "huggingface/smolagents": 6000}.get(repo, 0)


agent = ToolCallingAgent(
    tools=[fetch_repo_stars],
    model=OpenAIServerModel(model_id="gpt-4o-mini"),
    max_steps=5,
    stop_on_error=True,
)

print(agent.run("Compare stars for microsoft/semantic-kernel and huggingface/smolagents."))
```

## Picking the Right Agent

- Choose **CodeAgent** when tasks need scripting, data transformations, or chaining many tools.
- Choose **ToolCallingAgent** when you need predictable, schema-validated tool calls.
- Start with `verbose=True`, then disable in production.
- Tune `max_steps` based on typical task complexity (3–12 is common).

Next: **[Chapter 3: Tools & Functions](03-tools.md)** to build and reuse tools. 🛠️
