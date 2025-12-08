---
layout: default
title: "Chapter 7: Multi-Agent Patterns"
parent: "OpenAI Swarm Tutorial"
nav_order: 7
---

# Chapter 7: Multi-Agent Patterns

Combine agents using orchestration patterns for complex tasks.

## Patterns
- **Router → Specialist**: triage then handoff
- **Planner → Executors → Reviewer**: plan then parallelize, then review
- **Round-robin**: cycle through agents for brainstorming
- **Escalation**: fallback to senior/human

## Example Planner Pattern
```python
plan = ["gather_requirements", "propose_solution", "review_risks"]
# assign steps to different agents; track progress in context
```

## Tips
- Keep loops bounded; stop on convergence
- Add reviewer to catch hallucinations

## Next Steps
Chapter 8 covers production considerations.
