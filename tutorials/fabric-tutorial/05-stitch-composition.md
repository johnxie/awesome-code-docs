---
layout: default
title: "Chapter 5: Stitch Composition"
parent: "Fabric Tutorial"
nav_order: 5
---

# Chapter 5: Stitch Composition

Welcome to **Chapter 5: Stitch Composition**. In this part of **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Create sophisticated AI workflows by composing patterns into reusable Stitches.

## Overview

Stitches are Fabric's way of composing multiple patterns into coherent workflows. They enable complex multi-step processing pipelines that can be saved, shared, and reused.

## Understanding Stitches

### Stitch Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                        Stitch Workflow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   INPUT                                                         │
│     │                                                           │
│     ▼                                                           │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │Pattern 1│───▶│Pattern 2│───▶│Pattern 3│───▶│Pattern 4│     │
│  │(Extract)│    │(Analyze)│    │(Enhance)│    │(Format) │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│    [Data]        [Insights]    [Enhanced]     [OUTPUT]          │
│                                                                 │
│  Stitches = Patterns + Flow Logic + State Management            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Stitch Structure

```yaml
# stitch.yaml
name: research_pipeline
description: Complete research workflow from raw content to insights
version: 1.0

steps:
  - name: extract
    pattern: extract_wisdom
    input: $input

  - name: analyze
    pattern: analyze_claims
    input: $extract.output

  - name: synthesize
    pattern: create_synthesis
    input:
      wisdom: $extract.output
      claims: $analyze.output

  - name: format
    pattern: format_report
    input: $synthesize.output

output: $format.output
```

## Creating Stitches

### Basic Stitch Definition

```yaml
# stitches/summarize_and_critique.yaml
name: summarize_and_critique
description: Summarize content then provide critical analysis

steps:
  - name: summarize
    pattern: summarize
    input: $input

  - name: critique
    pattern: analyze_claims
    input: $input

  - name: combine
    pattern: merge_analysis
    input:
      summary: $summarize.output
      critique: $critique.output

output: $combine.output
```

### Running Stitches

```bash
# Execute a stitch
fabric --stitch summarize_and_critique < article.txt

# List available stitches
fabric --list-stitches

# View stitch definition
fabric --stitch research_pipeline --show
```

### Stitch with Variables

```yaml
# stitches/customizable_analysis.yaml
name: customizable_analysis
description: Analysis workflow with customizable depth

variables:
  depth:
    default: standard
    options: [quick, standard, deep]
  focus:
    default: general
    options: [general, technical, business]

steps:
  - name: initial_pass
    pattern: "extract_{{focus}}"
    input: $input

  - name: analysis
    pattern: "analyze_{{depth}}"
    input: $initial_pass.output
    when: $depth != "quick"

  - name: final
    pattern: format_output
    input: "{{analysis.output if analysis else initial_pass.output}}"

output: $final.output
```

Usage:
```bash
fabric --stitch customizable_analysis \
    --var depth=deep \
    --var focus=technical \
    < codebase_docs.txt
```

## Flow Control

### Conditional Steps

```yaml
# stitches/smart_processor.yaml
name: smart_processor
description: Process content based on detected type

steps:
  - name: detect_type
    pattern: classify_content
    input: $input

  - name: process_code
    pattern: explain_code
    input: $input
    when: $detect_type.output.type == "code"

  - name: process_article
    pattern: summarize
    input: $input
    when: $detect_type.output.type == "article"

  - name: process_data
    pattern: analyze_data
    input: $input
    when: $detect_type.output.type == "data"

output: "$process_code.output || $process_article.output || $process_data.output"
```

### Parallel Execution

```yaml
# stitches/parallel_analysis.yaml
name: parallel_analysis
description: Run multiple analyses in parallel

steps:
  - name: analyses
    parallel:
      - name: sentiment
        pattern: analyze_sentiment
        input: $input

      - name: topics
        pattern: extract_topics
        input: $input

      - name: entities
        pattern: extract_entities
        input: $input

      - name: claims
        pattern: extract_claims
        input: $input

  - name: combine
    pattern: merge_analyses
    input:
      sentiment: $analyses.sentiment.output
      topics: $analyses.topics.output
      entities: $analyses.entities.output
      claims: $analyses.claims.output

output: $combine.output
```

### Loops and Iteration

```yaml
# stitches/iterative_refinement.yaml
name: iterative_refinement
description: Iteratively improve content

variables:
  max_iterations:
    default: 3

steps:
  - name: initial
    pattern: improve_writing
    input: $input

  - name: refine
    loop:
      max: $max_iterations
      until: $quality_check.output.score >= 0.9

      steps:
        - name: quality_check
          pattern: rate_content
          input: $current

        - name: improve
          pattern: improve_writing
          input: $current
          context:
            feedback: $quality_check.output.suggestions

output: $refine.final
```

## Error Handling

### Retry Logic

```yaml
# stitches/robust_pipeline.yaml
name: robust_pipeline
description: Pipeline with error handling

steps:
  - name: extract
    pattern: extract_wisdom
    input: $input
    retry:
      max_attempts: 3
      delay: 1s
      backoff: exponential

  - name: analyze
    pattern: analyze_claims
    input: $extract.output
    retry:
      max_attempts: 2
    on_error:
      pattern: fallback_analysis
      input: $extract.output

output: $analyze.output
```

### Fallback Patterns

```yaml
# stitches/with_fallbacks.yaml
name: with_fallbacks
description: Pipeline with fallback options

steps:
  - name: primary
    pattern: deep_analysis
    input: $input
    model: gpt-4
    on_error:
      - name: secondary
        pattern: deep_analysis
        model: claude-3-opus
      - name: fallback
        pattern: basic_analysis
        model: gpt-3.5-turbo

output: "$primary.output || $secondary.output || $fallback.output"
```

## State Management

### Storing Intermediate Results

```yaml
# stitches/stateful_workflow.yaml
name: stateful_workflow
description: Workflow that maintains state across steps

state:
  extracted_data: null
  analysis_results: []
  final_score: 0

steps:
  - name: extract
    pattern: extract_structured
    input: $input
    save_to: state.extracted_data

  - name: analyze_each
    foreach: $state.extracted_data.items
    pattern: analyze_item
    append_to: state.analysis_results

  - name: score
    pattern: calculate_score
    input: $state.analysis_results
    save_to: state.final_score

  - name: report
    pattern: generate_report
    input: $state

output: $report.output
```

### Context Accumulation

```yaml
# stitches/context_aware.yaml
name: context_aware
description: Build context as workflow progresses

context:
  accumulated: []

steps:
  - name: step1
    pattern: first_analysis
    input: $input
    add_to_context: true

  - name: step2
    pattern: second_analysis
    input: $input
    context: $context.accumulated

  - name: step3
    pattern: final_synthesis
    input: $input
    context: $context.accumulated

output: $step3.output
```

## Real-World Stitch Examples

### Research Pipeline

```yaml
# stitches/research_pipeline.yaml
name: research_pipeline
description: Complete research workflow

steps:
  - name: gather
    parallel:
      - name: main_content
        pattern: extract_wisdom
        input: $input

      - name: references
        pattern: extract_references
        input: $input

  - name: verify
    foreach: $gather.main_content.output.claims
    pattern: fact_check
    max_parallel: 5

  - name: analyze
    pattern: synthesize_research
    input:
      content: $gather.main_content.output
      references: $gather.references.output
      verification: $verify.results

  - name: format
    pattern: format_research_report
    input: $analyze.output

output: $format.output
```

### Content Creation Pipeline

```yaml
# stitches/content_pipeline.yaml
name: content_pipeline
description: Create polished content from rough ideas

variables:
  style:
    default: professional
  length:
    default: medium

steps:
  - name: outline
    pattern: create_outline
    input: $input

  - name: draft
    pattern: write_draft
    input: $outline.output
    context:
      style: $style
      length: $length

  - name: improve
    pattern: improve_writing
    input: $draft.output
    iterations: 2

  - name: final_check
    parallel:
      - pattern: check_grammar
        input: $improve.output
      - pattern: check_style
        input: $improve.output
      - pattern: check_clarity
        input: $improve.output

  - name: finalize
    pattern: apply_fixes
    input:
      content: $improve.output
      fixes: $final_check

output: $finalize.output
```

## Summary

In this chapter, you've learned:

- **Stitch Concept**: Composing patterns into workflows
- **Creating Stitches**: YAML definitions and structure
- **Flow Control**: Conditions, parallel execution, loops
- **Error Handling**: Retries, fallbacks, recovery
- **State Management**: Storing and accumulating context
- **Real Examples**: Research and content creation pipelines

## Key Takeaways

1. **Composition Power**: Complex workflows from simple patterns
2. **Flow Control**: Conditional and parallel execution
3. **Error Resilience**: Build robust pipelines with fallbacks
4. **State Matters**: Manage context across workflow steps
5. **Reusability**: Save and share stitches across projects

## Next Steps

Ready to create your own custom patterns? Let's dive into Chapter 6.

---

**Ready for Chapter 6?** [Custom Patterns](06-custom-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `input`, `name`, `output` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Stitch Composition` as an operating subsystem inside **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `pattern`, `steps`, `stitches` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Stitch Composition` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `input`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `output`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/danielmiessler/Fabric)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [Pattern Library](https://github.com/danielmiessler/fabric/tree/main/data/patterns)
  Why it matters: authoritative reference on `Pattern Library` (github.com).
- [Community Patterns](https://github.com/danielmiessler/Fabric#community-patterns)
  Why it matters: authoritative reference on `Community Patterns` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `input` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Advanced Patterns](04-advanced-patterns.md)
- [Next Chapter: Chapter 6: Custom Patterns](06-custom-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
