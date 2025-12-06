---
layout: default
title: "Semantic Kernel Tutorial - Chapter 7: Agents"
nav_order: 7
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 7: Agents & Tool Use

> Combine plugins, memory, and planners to build autonomous, tool-using agents.

## Simple Agent Loop

```python
import asyncio
import semantic_kernel as sk
from semantic_kernel.functions import kernel_function
from semantic_kernel.planners import SequentialPlanner


class SearchPlugin:
    @kernel_function(name="web_search", description="Search the web for a topic")
    def web_search(self, query: str) -> str:
        # Replace with real search API
        return f"Pretend results for {query}"


async def main():
    kernel = sk.Kernel()
    kernel.add_plugin(SearchPlugin(), "search")

    planner = SequentialPlanner(kernel)
    goal = "Find the top 3 AI orchestration frameworks and summarize differences."
    plan = await planner.create_plan(goal)

    # Execute plan step by step (tool use)
    for step in plan.steps:
        result = await kernel.invoke(step)
        print(f"[{step.name}] {result}")


asyncio.run(main())
```

## Chat-Oriented Agent (turn-based)

```python
async def chat_agent(message: str, history: list[str]):
    # Compose context from memory/history
    context = "\n".join(history[-5:])
    response = await kernel.invoke(
        kernel.create_function_from_prompt(
            "chat",
            "Assistant",
            prompt="You are a helpful agent.\nHistory:\n{{$history}}\nUser: {{$input}}\nAssistant:",
        ),
        history=context,
        input=message,
    )
    history.append(f"User: {message}")
    history.append(f"Assistant: {response}")
    return response, history
```

## Tool Governance

- **Allowlist plugins** per environment.
- Require approval for **side-effectful tools** (e.g., file system, HTTP POST).
- Add **rate limits** and **budget caps** per conversation/session.
- Log tool calls with arguments for audit.

## Memory & Personas

- Attach **long-term memory** (vector store) for facts; **short-term memory** for dialog.
- Support **personas** by injecting system prompts or per-user preferences.
- Provide **session state** (timezone, locale, org role) as variables.

## Agent Patterns

- **Researcher/Writer** pair: one gathers context, the other synthesizes.
- **Planner/Executor**: planner creates steps, executor runs them with validation.
- **Validator**: post-processes outputs for quality and safety.

## Checklist

- [ ] Define the tools/plugins your agent may call
- [ ] Add guardrails for side effects (approvals, limits)
- [ ] Maintain short- and long-term memory
- [ ] Log conversations and tool calls
- [ ] Test agent flows with real tasks

Next: **[Chapter 8: Production Deployment](08-production.md)** for scaling and operations. 🏭
