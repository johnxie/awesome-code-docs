---
layout: default
title: "Smolagents Tutorial - Chapter 4: Code Execution"
nav_order: 4
has_children: false
parent: Smolagents Tutorial
---

# Chapter 4: Safe Code Execution

> Let agents write and run Python while keeping execution safe, bounded, and observable.

## Enabling Code Execution

`CodeAgent` executes Python that the model writes. Control it with limits:

```python
from smolagents import CodeAgent, HfApiModel

agent = CodeAgent(
    tools=[],
    model=HfApiModel(),
    max_steps=8,
    max_tokens=512,  # per completion
    verbose=True,
    additional_authorized_imports=["numpy", "pandas"],  # allowlisted imports
)

print(agent.run("Create a dataframe of 5 cities and populations, then sort descending."))
```

## Restricting Capabilities

- **Allowlist imports**: `additional_authorized_imports=["numpy"]`
- **Limit iterations**: `max_steps` to prevent infinite loops
- **Cap tokens**: set `max_tokens` to control cost
- **Disallow network access** unless tools explicitly provide it

## Handling Errors

```python
from smolagents import CodeAgent, HfApiModel

agent = CodeAgent(
    tools=[],
    model=HfApiModel(),
    max_steps=4,
    verbose=True,
    stop_on_error=True,  # stop at first failure
)

try:
    agent.run("Import a missing library and handle the error gracefully.")
except Exception as e:
    print(f"Agent stopped: {e}")
```

## Observability

- Enable `verbose=True` to print reasoning, code, and outputs during development.
- Log code cells the agent executes for auditability.
- Capture execution time and token usage per step.

## Safety Checklist

- [ ] Keep a tight import allowlist
- [ ] Set `max_steps` and `max_tokens`
- [ ] Disable or proxy network access via safe tools
- [ ] Log executed code for review
- [ ] Use `stop_on_error=True` for strict pipelines

Next: **[Chapter 5: Multi-Step Reasoning](05-multi-step.md)** to structure complex tasks. 🧭
