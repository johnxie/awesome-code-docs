---
layout: default
title: "Aider Tutorial - Chapter 6: Model Configuration"
nav_order: 6
has_children: false
parent: Aider Tutorial
---

# Chapter 6: Model Configuration

Welcome to **Chapter 6: Model Configuration**. In this part of **Aider Tutorial: AI Pair Programming in Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Configure and optimize different AI models for various coding tasks, including cost optimization, performance tuning, and model selection strategies.

## Overview

Different AI models have different strengths, costs, and performance characteristics. This chapter covers how to configure and optimize Aider for various models and use cases.

## Model Selection Strategy

### Understanding Model Characteristics

| Model | Strengths | Best For | Cost |
|:------|:----------|:---------|:-----|
| **Claude 3.5 Sonnet** | Best overall performance, complex reasoning | Architecture design, refactoring, debugging | High |
| **GPT-4o** | Fast, good all-rounder, multimodal | General coding, quick iterations | Medium-High |
| **GPT-4o Mini** | Cost-effective, fast | Simple tasks, prototyping | Low |
| **Claude 3 Haiku** | Fast, good for coding | Routine tasks, documentation | Low-Medium |
| **Gemini 1.5 Pro** | Long context, multimodal | Large codebases, documentation | Medium |
| **Local Models** | Privacy, offline | Sensitive code, no API costs | Free |

### Task-Based Model Selection

```bash
# Architecture and design - use most capable model
aider --model claude-3-5-sonnet-20241022

# Complex refactoring - needs strong reasoning
aider --model claude-3-5-sonnet-20241022

# Routine coding tasks - use faster/cheaper model
aider --model gpt-4o-mini

# Documentation and comments - can use smaller model
aider --model claude-3-haiku-20240307

# Large codebase work - use long context model
aider --model gemini/gemini-1.5-pro
```

## Architect Mode

### When to Use Architect Mode

Architect mode uses two models: a powerful "architect" model for planning and a fast "editor" model for implementation.

```bash
# Use for complex multi-file changes
aider --architect \
      --model claude-3-5-sonnet-20241022 \
      --editor-model gpt-4o-mini

# Benefits:
# - Claude does complex planning and reasoning
# - GPT-4o-mini does fast, accurate editing
# - Cost-effective for complex tasks
```

### Architect Mode Workflow

```bash
# Architect model analyzes the request and plans changes
> Refactor the entire authentication system to use dependency injection

# Architect creates detailed plan:
# 1. Extract interfaces for authentication services
# 2. Create dependency injection container
# 3. Refactor existing classes to use DI
# 4. Update initialization code
# 5. Add configuration for DI container

# Editor model implements each step quickly and accurately
```

## Cost Optimization

### Model Cost Comparison

```bash
# Cost per 1K tokens (approximate, as of 2024)
# Input tokens:
# - Claude 3.5 Sonnet: $3/1K
# - GPT-4o: $2.50/1K
# - GPT-4o Mini: $0.15/1K
# - Claude 3 Haiku: $0.25/1K

# Output tokens:
# - Claude 3.5 Sonnet: $15/1K
# - GPT-4o: $10/1K
# - GPT-4o Mini: $0.60/1K
# - Claude 3 Haiku: $1.25/1K
```

### Cost Optimization Strategies

```bash
# Use smaller models for routine tasks
aider --model gpt-4o-mini

# Use architect mode for complex tasks
aider --architect --model claude-3-5-sonnet-20241022 --editor-model gpt-4o-mini

# Be specific in prompts to reduce back-and-forth
> Add input validation to the user registration form with specific rules: email format, password strength (8+ chars, uppercase, lowercase, number), username uniqueness

# Use /diff to review before accepting expensive changes
> /diff
```

### Monitoring Usage

```bash
# Aider shows token usage
Aider v0.50.0
Models: claude-3-5-sonnet-20241022 with diff edit format
Git repo: .git with 12 files
Repo-map: using 1024 tokens  # Input tokens for context
API calls: 5 total, 1200 input tokens, 800 output tokens  # Running totals
```

## Performance Tuning

### Token Limits and Context Management

```bash
# Adjust repo-map tokens for your codebase size
export AIDER_MAP_TOKENS="2048"  # Increase for larger codebases

# Maximum chat history tokens
export AIDER_MAX_CHAT_HISTORY_TOKENS="8192"

# Configuration file
cat > .aider.conf.yml << EOF
map-tokens: 4096
max-chat-history-tokens: 16384
EOF
```

### Model-Specific Optimizations

```bash
# Claude models work better with explicit instructions
> Implement a REST API using Flask with the following requirements:
> - Use blueprints for organization
> - Include proper error handling
> - Add input validation with marshmallow
> - Use SQLAlchemy for database operations

# GPT models respond well to examples
> Create a function similar to the existing validate_email function but for phone numbers. Use regex pattern ^\+?1?\d{9,15}$

# Local models may need simpler instructions
ollama serve  # Start Ollama server first
aider --model ollama/llama3.1:70b
```

## Model Configuration Files

### Project-Specific Configuration

```yaml
# .aider.conf.yml - Project-specific settings
model: claude-3-5-sonnet-20241022
editor-model: gpt-4o-mini
auto-commits: true
dark-mode: true
map-tokens: 2048
max-chat-history-tokens: 4096

# File type associations (for better context)
file-associations:
  - "*.py": "python"
  - "*.js": "javascript"
  - "*.ts": "typescript"
```

### User-Specific Configuration

```yaml
# ~/.aider.conf.yml - Global user preferences
model: gpt-4o
auto-commits: true
dark-mode: true
editor: code
git: true
gitignore: true

# API keys (or use environment variables)
# openai-api-key: sk-...
# anthropic-api-key: sk-ant-...
```

### Environment-Specific Models

```bash
# Development - use faster models
export AIDER_MODEL="gpt-4o-mini"

# Production code - use most capable models
export AIDER_MODEL="claude-3-5-sonnet-20241022"

# Documentation - use cost-effective models
export AIDER_MODEL="claude-3-haiku-20240307"
```

## Working with Local Models

### Ollama Integration

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.1:70b
ollama pull mistral:7b
ollama pull codellama:34b

# Use with Aider
aider --model ollama/llama3.1:70b
aider --model ollama/mistral:7b
aider --model ollama/codellama:34b
```

### Local Model Advantages

```bash
# Privacy - no data sent to external APIs
aider --model ollama/llama3.1:70b

# Cost - no API charges
aider --model ollama/mistral:7b

# Offline capability
aider --model ollama/codellama:34b
```

### Local Model Limitations

```bash
# Generally slower than cloud models
# May have less up-to-date knowledge
# Smaller context windows
# May need simpler prompts
```

## Cloud Model Providers

### OpenAI Models

```bash
# GPT-4o (recommended for most users)
aider --model gpt-4o

# GPT-4o Mini (cost-effective)
aider --model gpt-4o-mini

# GPT-4 Turbo (good balance)
aider --model gpt-4-turbo

# Azure OpenAI
export AZURE_OPENAI_API_KEY="your-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-4"
aider --model azure/gpt-4
```

### Anthropic Models

```bash
# Claude 3.5 Sonnet (best overall)
aider --model claude-3-5-sonnet-20241022

# Claude 3 Opus (most capable, expensive)
aider --model claude-3-opus-20240229

# Claude 3 Haiku (fast, cost-effective)
aider --model claude-3-haiku-20240307

# Claude 3 Sonnet (good balance)
aider --model claude-3-sonnet-20240229
```

### Google Models

```bash
# Gemini 1.5 Pro (long context)
aider --model gemini/gemini-1.5-pro

# Gemini 1.0 Pro (faster, cheaper)
aider --model gemini/gemini-1.0-pro
```

## Model Switching During Sessions

### Dynamic Model Switching

```bash
# Start with one model
aider --model gpt-4o-mini

# Switch models mid-session (if needed)
> /model claude-3-5-sonnet-20241022

# Aider will switch models for subsequent requests
```

### Task-Based Switching

```bash
# Use different models for different phases
# Planning phase - use capable model
aider --model claude-3-5-sonnet-20241022

# Implementation phase - switch to faster model
> /model gpt-4o-mini

# Continue with faster model for routine tasks
```

## Troubleshooting Model Issues

### API Rate Limits

```bash
# If you hit rate limits, switch to different model or wait
# OpenAI: 10,000 RPM for GPT-4, higher for GPT-3.5
# Anthropic: 50 requests per minute

# Use retry logic (Aider handles this automatically)
# Or switch to a different provider
aider --model claude-3-haiku-20240307
```

### Model-Specific Errors

```bash
# Claude context length exceeded
# Solution: Reduce repo-map tokens or be more specific about files
export AIDER_MAP_TOKENS="1024"

# GPT model hallucinations
# Solution: Be more specific in prompts and review changes carefully
> /diff

# Local model slow responses
# Solution: Use smaller local models or cloud models for speed
aider --model ollama/mistral:7b
```

### Cost Monitoring

```bash
# Monitor API usage and costs
# OpenAI: https://platform.openai.com/usage
# Anthropic: https://console.anthropic.com/

# Set spending limits
# Use cost-effective models for routine tasks
aider --model gpt-4o-mini
```

## Advanced Model Features

### Multimodal Models

```bash
# GPT-4o and Gemini support images
# Can analyze screenshots, diagrams, etc.
> Look at this architecture diagram [attach image] and implement the user service according to this design

# Useful for:
# - UI implementation from designs
# - Code generation from diagrams
# - Documentation from screenshots
```

### Function Calling

```bash
# Some models support function calling
# Aider can use this for external integrations
> Run the test suite and fix any failing tests

# Model can call testing functions directly
```

## Best Practices for Model Selection

### Match Model to Task Complexity

```bash
# Simple tasks: GPT-4o Mini or Claude Haiku
> Add type hints to this function

# Medium complexity: GPT-4o or Claude Sonnet
> Create a REST API endpoint with validation

# High complexity: Claude Opus or GPT-4
> Design and implement a microservices architecture

# Very large tasks: Use architect mode
aider --architect --model claude-3-5-sonnet-20241022 --editor-model gpt-4o-mini
```

### Cost-Performance Balance

```bash
# Budget-conscious development
# Use GPT-4o Mini for most tasks (85% cost savings vs GPT-4)
aider --model gpt-4o-mini

# Reserve expensive models for critical tasks
aider --model claude-3-5-sonnet-20241022  # Only when needed
```

### Team Model Standards

```yaml
# .aider.conf.yml for team consistency
model: gpt-4o-mini          # Default for all developers
architect: claude-3-5-sonnet-20241022  # For complex tasks
editor-model: gpt-4o-mini   # Fast implementation

# Override for specific projects
# high-security-project: use local models
# performance-critical: use Claude Opus
```

## Summary

In this chapter, we've covered:

- **Model Selection**: Choosing the right model for different tasks
- **Architect Mode**: Using two models for planning and implementation
- **Cost Optimization**: Balancing cost and performance
- **Performance Tuning**: Token limits and context management
- **Configuration**: Project and user-specific settings
- **Local Models**: Privacy and cost benefits of local models
- **Cloud Providers**: OpenAI, Anthropic, and Google model options
- **Troubleshooting**: Handling rate limits and errors
- **Advanced Features**: Multimodal and function calling capabilities

## Key Takeaways

1. **Task Matching**: Choose models based on task complexity and requirements
2. **Cost Awareness**: Use cost-effective models for routine tasks
3. **Architect Mode**: Leverage two-model approach for complex work
4. **Local Options**: Consider privacy and offline capabilities
5. **Configuration**: Set up project-specific model preferences
6. **Performance Tuning**: Adjust token limits for your codebase
7. **Troubleshooting**: Handle API limits and model-specific issues

## Next Steps

Now that you can configure models effectively, let's explore **voice workflows** and automation features.

---

**Ready for Chapter 7?** [Voice & Workflows](07-workflows.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Aider Tutorial: AI Pair Programming in Your Terminal**
- tutorial slug: **aider-tutorial**
- chapter focus: **Chapter 6: Model Configuration**
- system context: **Aider Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 6: Model Configuration`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Aider Repository](https://github.com/Aider-AI/aider)
- [Aider Releases](https://github.com/Aider-AI/aider/releases)
- [Aider Docs](https://aider.chat/)

### Cross-Tutorial Connection Map

- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Continue Tutorial](../continue-tutorial/)
- [Codex Analysis Platform](../codex-analysis-platform/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 6: Model Configuration`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

### Scenario Playbook 1: Chapter 6: Model Configuration

- tutorial context: **Aider Tutorial: AI Pair Programming in Your Terminal**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `model`, `aider`, `claude` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Model Configuration` as an operating subsystem inside **Aider Tutorial: AI Pair Programming in Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `models`, `mini`, `Claude` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Model Configuration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `model`.
2. **Input normalization**: shape incoming data so `aider` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `claude`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Aider Repository](https://github.com/Aider-AI/aider)
  Why it matters: authoritative reference on `Aider Repository` (github.com).
- [Aider Releases](https://github.com/Aider-AI/aider/releases)
  Why it matters: authoritative reference on `Aider Releases` (github.com).
- [Aider Docs](https://aider.chat/)
  Why it matters: authoritative reference on `Aider Docs` (aider.chat).

Suggested trace strategy:
- search upstream code for `model` and `aider` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Advanced Prompting](05-prompting.md)
- [Next Chapter: Chapter 7: Voice & Workflows](07-workflows.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
