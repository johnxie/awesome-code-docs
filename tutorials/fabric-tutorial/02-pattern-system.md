---
layout: default
title: "Chapter 2: Pattern System"
parent: "Fabric Tutorial"
nav_order: 2
---

# Chapter 2: Pattern System

Welcome to **Chapter 2: Pattern System**. In this part of **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understand Fabric's modular pattern architecture for creating reusable AI-powered cognitive workflows.

## Overview

Patterns are the core building blocks of Fabric. They are carefully crafted prompt templates that encode expert knowledge for specific cognitive tasks. This chapter explores how patterns work and how to use them effectively.

## What is a Pattern?

### Pattern Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                       Fabric Pattern                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────┐                    │
│  │           SYSTEM PROMPT                  │                    │
│  │  - Role definition                       │                    │
│  │  - Expertise area                        │                    │
│  │  - Behavioral guidelines                 │                    │
│  └─────────────────────────────────────────┘                    │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────┐                    │
│  │           USER PROMPT                    │                    │
│  │  - Task instructions                     │                    │
│  │  - Output format                         │                    │
│  │  - Constraints                           │                    │
│  └─────────────────────────────────────────┘                    │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────┐                    │
│  │           INPUT PLACEHOLDER              │                    │
│  │  - {{input}} for content                 │                    │
│  │  - Dynamic substitution                  │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern Files

```bash
# Pattern directory structure
patterns/
├── summarize/
│   └── system.md       # System prompt
├── extract_wisdom/
│   └── system.md
├── analyze_claims/
│   └── system.md
└── create_outline/
    └── system.md
```

## Core Patterns

### summarize

```markdown
# IDENTITY and PURPOSE

You are an expert content summarizer. You take content in and output
a summary in a structured format.

# STEPS

1. Read the entire content carefully
2. Identify the main topic and key themes
3. Extract the most important points
4. Create a concise summary

# OUTPUT FORMAT

- Start with a one-sentence overview
- List 5-10 key points as bullet points
- End with a brief conclusion

# INPUT

{{input}}
```

Usage:
```bash
# Summarize a file
fabric -p summarize < article.txt

# Summarize from clipboard
pbpaste | fabric -p summarize

# Summarize URL content
curl -s https://example.com/article | fabric -p summarize
```

### extract_wisdom

```markdown
# IDENTITY and PURPOSE

You extract surprising, insightful, and interesting information from
text content. You are interested in insights related to the purpose
and meaning of life, human flourishing, and making the world better.

# STEPS

1. Extract main ideas and concepts
2. Identify surprising or counterintuitive insights
3. Note actionable recommendations
4. Find memorable quotes

# OUTPUT SECTIONS

## SUMMARY
One paragraph summary of the content.

## IDEAS
- Interesting ideas from the content

## INSIGHTS
- Deeper insights derived from the ideas

## QUOTES
- Memorable quotes from the content

## HABITS
- Actionable habits mentioned or implied

## FACTS
- Factual claims made in the content

## REFERENCES
- Sources, books, or resources mentioned

# INPUT

{{input}}
```

### analyze_claims

```markdown
# IDENTITY and PURPOSE

You are an expert fact-checker and claim analyst. Your role is to
evaluate claims for accuracy, identify potential biases, and assess
the strength of evidence.

# STEPS

1. Identify all claims made in the content
2. Categorize claims by type (factual, opinion, prediction)
3. Assess evidence strength for each claim
4. Note potential biases or logical fallacies

# OUTPUT FORMAT

## CLAIMS IDENTIFIED
For each claim:
- CLAIM: [The claim]
- TYPE: [Factual/Opinion/Prediction]
- EVIDENCE: [Strong/Moderate/Weak/None]
- ASSESSMENT: [Analysis]

## OVERALL ASSESSMENT
Summary of content credibility.

## RECOMMENDATIONS
What to verify or research further.

# INPUT

{{input}}
```

## Pattern Categories

### Content Processing

```bash
# Summarization patterns
fabric -p summarize        # General summarization
fabric -p summarize_micro  # Ultra-short summary
fabric -p summarize_paper  # Academic paper summary

# Extraction patterns
fabric -p extract_wisdom       # Extract insights
fabric -p extract_ideas        # Extract main ideas
fabric -p extract_references   # Extract citations
fabric -p extract_questions    # Extract questions raised
```

### Analysis Patterns

```bash
# Analytical patterns
fabric -p analyze_claims      # Fact-check content
fabric -p analyze_prose       # Writing quality analysis
fabric -p analyze_tech        # Technical analysis
fabric -p rate_content        # Quality rating
fabric -p find_logical_fallacies  # Logic analysis
```

### Creative Patterns

```bash
# Writing assistance
fabric -p improve_writing     # Enhance text quality
fabric -p create_outline      # Generate outline
fabric -p write_essay         # Generate essay
fabric -p create_summary      # Create executive summary
```

### Development Patterns

```bash
# Code-related patterns
fabric -p explain_code        # Code explanation
fabric -p review_code         # Code review
fabric -p improve_code        # Code improvement
fabric -p write_tests         # Generate tests
fabric -p explain_docs        # Documentation explanation
```

## Pattern Variables

### Input Substitution

```bash
# Basic input
echo "Some content" | fabric -p summarize
# {{input}} becomes "Some content"

# From file
fabric -p summarize < document.txt

# Multiple inputs with context
fabric -p analyze_claims --context "Article from 2024" < article.txt
```

### Custom Variables

```markdown
# Pattern with custom variables
# IDENTITY and PURPOSE

You are a {{role}} expert specializing in {{domain}}.

# TASK

Analyze the following {{content_type}} and provide {{output_type}}.

# INPUT

{{input}}
```

Usage:
```bash
fabric -p custom_pattern \
  --var role="security" \
  --var domain="web applications" \
  --var content_type="code" \
  --var output_type="vulnerability assessment"
```

## Pattern Selection

### Choosing the Right Pattern

```bash
# List available patterns
fabric --list

# Search patterns by name
fabric --list | grep -i summary

# View pattern content
fabric -p summarize --show

# Pattern recommendations
# Task: Summarize an article
fabric -p summarize

# Task: Extract actionable insights
fabric -p extract_wisdom

# Task: Verify claims
fabric -p analyze_claims

# Task: Improve writing
fabric -p improve_writing
```

### Pattern Comparison

```bash
# Compare pattern outputs
echo "Content here" | fabric -p summarize > summary.txt
echo "Content here" | fabric -p extract_wisdom > wisdom.txt

# Use different patterns for different needs
# Quick overview: summarize
# Deep insights: extract_wisdom
# Fact-check: analyze_claims
```

## Pattern Execution

### Basic Execution

```bash
# Pipe input
cat article.txt | fabric -p summarize

# File input
fabric -p summarize -i article.txt

# URL input
fabric -p summarize --url https://example.com/article

# Clipboard
pbpaste | fabric -p summarize | pbcopy
```

### Output Control

```bash
# Output to file
fabric -p summarize -o output.txt < input.txt

# JSON output
fabric -p summarize --json < input.txt

# Markdown formatting
fabric -p summarize --format markdown < input.txt

# Stream output
fabric -p summarize --stream < input.txt
```

### Model Selection

```bash
# Use specific model
fabric -p summarize --model gpt-4 < input.txt

# Use Claude
fabric -p summarize --model claude-3-opus-20240229 < input.txt

# Use local model via Ollama
fabric -p summarize --model ollama:llama2 < input.txt
```

## Pattern Internals

### System Prompt Components

```markdown
# IDENTITY and PURPOSE
Defines WHO the AI should act as and WHY.

# STEPS
Explicit procedure the AI should follow.

# OUTPUT FORMAT
Specific structure for the response.

# OUTPUT INSTRUCTIONS
Additional constraints and guidelines.

# INPUT
Where the user content goes ({{input}}).

# EXAMPLE (optional)
Example input/output pair for clarity.
```

### Effective Patterns

```markdown
# Best practices for patterns

1. Clear Identity
   - Specific role ("expert summarizer" not "assistant")
   - Defined expertise area

2. Explicit Steps
   - Numbered, actionable instructions
   - Clear sequence of operations

3. Structured Output
   - Consistent format
   - Markdown sections for organization
   - Bullet points for lists

4. Constraints
   - Length limits where appropriate
   - Style guidelines
   - What to include/exclude
```

## Summary

In this chapter, you've learned:

- **Pattern Structure**: System prompts, user prompts, and placeholders
- **Core Patterns**: summarize, extract_wisdom, analyze_claims
- **Pattern Categories**: Processing, analysis, creative, development
- **Pattern Execution**: Input methods, output control, model selection
- **Pattern Internals**: Components of effective patterns

## Key Takeaways

1. **Patterns Encode Expertise**: Each pattern is a refined prompt template
2. **Choose Wisely**: Select patterns matching your specific task
3. **Output Format Matters**: Patterns define structured output
4. **Composability**: Patterns can be chained together
5. **Model Flexibility**: Same pattern works with different AI models

## Next Steps

Now that you understand the pattern system, let's explore basic usage workflows in Chapter 3.

---

**Ready for Chapter 3?** [Basic Usage](03-basic-usage.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `fabric`, `summarize`, `input` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Pattern System` as an operating subsystem inside **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `patterns`, `summary` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Pattern System` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `fabric`.
2. **Input normalization**: shape incoming data so `summarize` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `input`.
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
- search upstream code for `fabric` and `summarize` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Fabric](01-getting-started.md)
- [Next Chapter: Chapter 3: Basic Usage](03-basic-usage.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
