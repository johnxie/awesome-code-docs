---
layout: default
title: "Langfuse Tutorial - Chapter 4: Evaluation"
nav_order: 4
has_children: false
parent: Langfuse Tutorial
---

# Chapter 4: Evaluation

> Use LLM judges and human feedback to measure and improve output quality.

## Overview

Evaluation helps you quantify output quality. Langfuse supports LLM-as-judge workflows and human annotations to score traces automatically or manually.

## LLM-as-Judge Evaluation

Use a judge model to score your outputs:

```python
from langfuse import Langfuse
from openai import OpenAI

langfuse = Langfuse(public_key="pk-...", secret_key="sk-...", host="https://cloud.langfuse.com")
client = OpenAI()

def evaluate_output(output: str, criteria: str) -> float:
    resp = client.responses.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Score this output 0-1 on {criteria}. Return only the number.",
            },
            {"role": "user", "content": output},
        ],
    )
    return float(resp.choices[0].message.content.strip())

# In your app
trace = langfuse.trace(name="qa-response")
llm_resp = client.responses.create(model="gpt-4o-mini", messages=[...])
trace.span(name="llm", output=llm_resp.choices[0].message.content)

# Evaluate
helpfulness = evaluate_output(llm_resp.choices[0].message.content, "helpfulness")
trace.score(name="helpfulness", value=helpfulness)
```

## Creating Evaluation Templates

Define reusable evaluation templates in Langfuse UI:

1. Create an evaluation template named `qa_quality`.
2. Define variables like `{{output}}`, `{{criteria}}`.
3. Use it in code:

```python
evaluation = langfuse.get_eval_template("qa_quality")
result = evaluation.run(
    variables={
        "output": response,
        "criteria": "relevance, accuracy, helpfulness",
    },
    model="gpt-4o-mini",
)
trace.score(name="quality", value=float(result.output))
```

## Human Evaluation

For subjective metrics, collect human feedback:

```python
# In your UI
def submit_feedback(trace_id: str, score: float, comment: str):
    trace = langfuse.trace(id=trace_id)  # get existing trace
    trace.score(name="human_rating", value=score, comment=comment)
```

Or create annotation queues in the UI for team review.

## Automated Evaluations

Set up recurring evaluations on traces matching filters:

```python
# Run evaluations on traces tagged with "production"
langfuse.create_eval_job(
    name="daily-qa-eval",
    query={"tags": ["production"]},
    eval_template="qa_quality",
    frequency="daily",
)
```

## Evaluation Metrics

Common metrics to track:

- **Accuracy**: Factual correctness (0-1)
- **Relevance**: How well it addresses the query (0-1)
- **Helpfulness**: User satisfaction potential (0-1)
- **Toxicity**: Harmful content detection (0-1, inverted)
- **Cost Efficiency**: Quality per token spent

## Tips

- Use consistent scoring scales (0-1 or 1-5).
- Include confidence intervals when possible.
- Correlate scores with user behavior metrics (conversion, retention).
- Re-evaluate after prompt/model changes.

Next: dive into analytics and cost tracking. 