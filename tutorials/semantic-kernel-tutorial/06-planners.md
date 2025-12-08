---
layout: default
title: "Semantic Kernel Tutorial - Chapter 6: Planners"
nav_order: 6
has_children: false
parent: Semantic Kernel Tutorial
---

# Chapter 6: Planners

> Use planners to break down goals into executable steps using your plugins and AI services.

## Sequential Planner (Python)

```python
from semantic_kernel.planners import SequentialPlanner

# Assume plugins already registered
planner = SequentialPlanner(kernel)

plan = await planner.create_plan(
    goal="Research AI trends and email a 3-bullet summary to the team."
)

print(plan)  # See generated steps

# Execute
result = await plan.invoke(kernel)
print(result)
```

## Adding Constraints

- Provide **context**: domain, persona, length limits, data sources.
- Restrict tools: pass `excluded_plugins` or `included_plugins` when creating the plan.
- Enforce safety: add refusal policies and PII guidance in the goal text.

## Stepwise / Looping Patterns

```python
async def execute_plan_with_checks(plan):
    for step in plan.steps:
        # Approve/reject steps programmatically
        if "unsafe" in step.description.lower():
            raise ValueError("Unsafe step detected")
        result = await kernel.invoke(step)
        print(f"{step.name}: {result}")
```

## Evaluating Plans

- Log generated plans for auditability.
- Add human-in-the-loop approval for high-risk actions.
- Use metrics: success rate, average steps, latency per step.

## Planner Gotchas

- Make sure plugins have **descriptions**—planners rely on them for selection.
- Keep prompts short; planners can drift with overly vague goals.
- Consider cost: planners may call the model multiple times.

## Checklist

- [ ] Register plugins with clear descriptions
- [ ] Generate a plan for a real task
- [ ] Add constraints (length, tone, data sources)
- [ ] Review steps before execution (auto or human)
- [ ] Track metrics on plan success/latency

Next: **[Chapter 7: Agents](07-agents.md)** to build autonomous, tool-using agents. 🤖
