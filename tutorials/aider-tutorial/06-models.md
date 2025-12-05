---
layout: default
title: "Aider Tutorial - Chapter 6: Model Configuration"
nav_order: 6
has_children: false
parent: Aider Tutorial
---

# Chapter 6: Model Configuration

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