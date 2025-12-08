---
layout: default
title: "Smolagents Tutorial - Chapter 7: Advanced Patterns"
nav_order: 7
has_children: false
parent: Smolagents Tutorial
---

# Chapter 7: Advanced Patterns

> Build router agents, multi-agent teams, and add safety layers.

## Router Pattern

```python
from smolagents import CodeAgent, ToolCallingAgent, HfApiModel, OpenAIServerModel

analysis_agent = CodeAgent(model=HfApiModel(), tools=[], max_steps=6)
strict_agent = ToolCallingAgent(model=OpenAIServerModel(model_id="gpt-4o-mini"), tools=[], max_steps=4)


def route(task: str):
    if "database" in task or "system change" in task:
        return strict_agent.run(task)  # safer tool calls
    return analysis_agent.run(task)    # more flexible reasoning


print(route("Summarize the latest smolagents release notes."))
print(route("Update database schema for customers table."))  # would be routed to strict_agent with DB tools
```

## Multi-Agent Hand-off

```python
from smolagents import CodeAgent, HfApiModel

researcher = CodeAgent(model=HfApiModel(), tools=[], max_steps=6)
writer = CodeAgent(model=HfApiModel(), tools=[], max_steps=4)


def research_and_write(topic: str):
    findings = researcher.run(f"Find 5 key points about {topic}. Return bullet list.")
    article = writer.run(f"Draft a concise blog post using these points:\n{findings}")
    return article


print(research_and_write("Lightweight agent frameworks"))
```

## Safety & Governance

- Use **allowlisted tools** only; avoid raw network access unless via vetted tools.
- Set **rate limits** and **budget caps** per session/user.
- Require human approval for steps tagged as **destructive** (e.g., file writes, DB changes).
- Log reasoning, tool calls, and code for audits.

## Evaluation Hooks

- Create regression prompts and expected outputs; diff against new runs.
- Score outputs for **faithfulness** and **safety**; block responses that fail checks.
- Add lint checks for generated code (e.g., `flake8`/`ruff`) before execution in prod.

## Checklist

- [ ] Implement routing for risky vs flexible tasks
- [ ] Consider multi-agent hand-offs for specialization
- [ ] Enforce tool allowlists and human approval for side effects
- [ ] Add evaluation hooks before shipping changes

Next: **[Chapter 8: Production Deployment](08-production.md)** to ship reliable agent services. 🚀
