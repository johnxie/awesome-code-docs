---
layout: default
title: "Langfuse Tutorial - Chapter 6: Datasets & Testing"
nav_order: 6
has_children: false
parent: Langfuse Tutorial
---

# Chapter 6: Datasets & Testing

> Create test suites from production traces and run regression tests.

## Overview

Langfuse lets you extract datasets from traces to build test suites. This helps catch regressions when you update prompts, models, or code.

## Creating Datasets from Traces

Extract production examples:

```python
# Create dataset from recent traces
dataset = langfuse.create_dataset(
    name="support-qa-v1",
    description="Real support conversations for testing",
    items=[
        {
            "input": trace.input,
            "expected_output": trace.output,
            "metadata": {"tags": trace.tags, "scores": trace.scores},
        }
        for trace in langfuse.get_traces(limit=100, filters={"tags": ["production"]})
    ]
)
```

## Dataset Structure

Each dataset item contains:

```python
{
    "input": {"messages": [...], "context": "..."},
    "expected_output": "The expected response...",
    "metadata": {
        "tags": ["production", "high-quality"],
        "scores": {"helpfulness": 0.95, "accuracy": 1.0},
        "source_trace_id": "trace_123"
    }
}
```

## Running Tests Against Datasets

Test prompt/model changes:

```python
def test_dataset(dataset_name: str, model: str = "gpt-4o-mini"):
    dataset = langfuse.get_dataset(dataset_name)
    results = []

    for item in dataset.items:
        # Run your updated pipeline
        actual_output = generate_response(item.input, model=model)

        # Evaluate against expected
        score = evaluate_similarity(actual_output, item.expected_output)

        results.append({
            "item_id": item.id,
            "expected": item.expected_output,
            "actual": actual_output,
            "score": score,
        })

    # Log test run
    test_run = langfuse.create_test_run(
        name=f"{dataset_name}-{model}-{datetime.now().isoformat()}",
        dataset=dataset,
        results=results,
    )

    return test_run
```

## Automated Regression Testing

Set up CI/CD tests:

```yaml
# .github/workflows/test.yml
name: LLM Regression Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Run Tests
        run: |
          pip install langfuse openai
          python -c "
          import os
          os.environ['LANGFUSE_PUBLIC_KEY'] = '${{ secrets.LANGFUSE_PK }}'
          os.environ['LANGFUSE_SECRET_KEY'] = '${{ secrets.LANGFUSE_SK }}'
          from test_llm import test_dataset
          result = test_dataset('support-qa-v1')
          if result.avg_score < 0.8:
            raise Exception('Regression detected!')
          "
```

## Dataset Management

Version and update datasets:

```python
# Fork dataset for A/B testing
new_dataset = langfuse.fork_dataset(
    source_dataset="support-qa-v1",
    name="support-qa-experimental",
    modifications={"add_items": [...], "remove_items": [...]}
)

# Merge successful experiments back
langfuse.merge_dataset(
    source="support-qa-experimental",
    target="support-qa-v1"
)
```

## Golden Dataset Creation

Curate high-quality examples:

1. Filter traces by high scores: `{"scores": {"helpfulness": {"gte": 0.9}}}`
2. Manually review and annotate in the UI
3. Use as golden standard for evaluations

## Test Coverage

Ensure comprehensive coverage:

- **Edge Cases**: Error scenarios, unusual inputs
- **Diversity**: Different user types, languages, contexts
- **Scale**: Various input lengths and complexity levels
- **Time**: Seasonal patterns and trends

## Tips

- Start with 50-100 examples; expand as you iterate.
- Include both positive and negative examples.
- Test on multiple models to ensure portability.
- Run tests before production deployments.

Next: integrate with popular LLM frameworks. 