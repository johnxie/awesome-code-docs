---
layout: default
title: "Chapter 9: Enterprise Operations & Advanced Patterns"
parent: "AG2 Tutorial"
nav_order: 9
---

# Chapter 9: Enterprise Operations & Advanced Patterns

Harden AG2 for production: governance, evals, safety, observability, and cost/performance tuning.

## Objectives
- Design enterprise-grade multi-agent patterns
- Add safety and guardrails
- Evaluate agents with automated tests
- Monitor cost, latency, and quality

## Enterprise Patterns
- **Role graph**: define agent graph (planner, worker, reviewer, router)
- **Reusable routines**: templatize workflows (triage → plan → execute → review)
- **Escalation**: fallback to human or senior agent on risk/low confidence

## Safety & Guardrails
- Input/output filters (PII, toxicity) before/after agent steps
- Tool allowlists; enforce auth scopes per tool
- Rate limits per agent; budget caps per conversation

## Evaluations (Python sketch)
```python
from ag2 import eval_chat

test_cases = [
    {"prompt": "Add two numbers", "expected": "4"},
    {"prompt": "Summarize GDPR", "contains": "data protection"},
]

results = eval_chat(assistant=assistant, cases=test_cases)
for r in results:
    print(r.passed, r.reason)
```

## Observability
- Log every agent turn: prompt, tool calls, tokens, latency
- Traces: link conversation → tool call → model response
- Dashboards: cost per workflow, p95 latency, success rate, safety flags

## Cost & Performance
- Use smaller models for classification/routing
- Cache intermediate steps (plans, retrieved docs)
- Parallelize independent subtasks; batch tool calls when possible

## Runbook Essentials
- On-call steps: identify failing agent/tool; roll back model/weight; disable risky tools
- SLOs: latency, success rate, budget per task
- Drills: simulated outages of tools/models; test fallbacks

## Deployment Tips
- Version prompts and workflows
- Canary new models/agents on a small traffic slice
- Keep configuration in code + config files for repeatability

## Next Steps
Integrate evaluations into CI and add organization-wide guardrails and cost budgets.
