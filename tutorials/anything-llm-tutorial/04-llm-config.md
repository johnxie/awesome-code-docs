---
layout: default
title: "AnythingLLM Tutorial - Chapter 4: LLM Configuration"
nav_order: 4
has_children: false
parent: AnythingLLM Tutorial
---

# Chapter 4: LLM Configuration - Connecting Language Models

> Configure and optimize different LLM providers for your AnythingLLM instance.

## Overview

AnythingLLM supports multiple LLM providers with different capabilities and pricing. This chapter covers configuring providers, optimizing settings, and choosing the right model for your use case.

## Supported LLM Providers

### OpenAI

```bash
# Most popular choice - excellent quality and speed
# Models: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo

# Configuration in AnythingLLM:
# Settings > LLM Providers > OpenAI
# - API Key: sk-your-openai-key-here
# - Model: gpt-4o (recommended)
# - Max Tokens: 4096 (adjust based on needs)
# - Temperature: 0.7 (creativity vs consistency)
```

```python
# OpenAI API key setup
export OPENAI_API_KEY="sk-your-actual-openai-api-key"

# Test connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Anthropic Claude

```bash
# Excellent reasoning and long context
# Models: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku

# Configuration:
# Settings > LLM Providers > Anthropic
# - API Key: sk-ant-your-anthropic-key
# - Model: claude-3-5-sonnet-20241022
# - Max Tokens: 4096
# - Temperature: 0.7
```

```python
# Anthropic API key setup
export ANTHROPIC_API_KEY="sk-ant-your-actual-anthropic-key"

# Test connection
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model": "claude-3-sonnet-20240229", "max_tokens": 1, "messages": []}'
```

### Local Models (Ollama)

```bash
# Complete privacy - no data leaves your machine
# Models: Llama, Mistral, Phi, and many others

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.1:70b     # Best overall
ollama pull mistral:7b       # Fast and good
ollama pull phi3:14b         # Microsoft Phi-3

# Configuration in AnythingLLM:
# Settings > LLM Providers > Ollama
# - Base URL: http://host.docker.internal:11434
# - Model: llama3.1:70b
# - Max Tokens: 4096
```

```bash
# Start Ollama service
ollama serve

# List available models
ollama list

# Test model
ollama run llama3.1:70b "Hello, test message"
```

### Other Local Options

#### LMStudio

```bash
# GUI for running local models
# Download from: https://lmstudio.ai/

# Configuration in AnythingLLM:
# Settings > LLM Providers > LMStudio
# - Base URL: http://host.docker.internal:1234
# - Model: your-loaded-model-name
```

#### LocalAI

```bash
# Drop-in OpenAI API replacement
# Run any GGUF model

# Configuration:
# Settings > LLM Providers > LocalAI
# - Base URL: http://host.docker.internal:8080
# - Model: your-model-name
```

### Cloud Alternatives

#### Azure OpenAI

```bash
# Enterprise-grade OpenAI deployment

# Configuration:
# Settings > LLM Providers > Azure OpenAI
# - API Key: your-azure-key
# - Endpoint: https://your-resource.openai.azure.com/
# - Deployment: gpt-4
# - API Version: 2024-02-15-preview
```

#### Google Gemini

```bash
# Google's multimodal models

# Configuration:
# Settings > LLM Providers > Google Gemini
# - API Key: your-gemini-key
# - Model: gemini-1.5-pro
```

## Model Selection Guide

### By Use Case

```yaml
# Chat/Conversational
Best: Claude 3.5 Sonnet, GPT-4o
Good: GPT-4 Turbo, Claude 3 Opus
Fast: GPT-3.5 Turbo, Claude 3 Haiku

# Technical/Documentation Q&A
Best: Claude 3.5 Sonnet, GPT-4o
Good: GPT-4 Turbo, Claude 3 Opus
Local: Llama 3.1 70B

# Code Generation
Best: GPT-4o, Claude 3.5 Sonnet
Good: GPT-4 Turbo, Claude 3 Opus
Local: CodeLlama 34B

# Creative Writing
Best: Claude 3 Opus, GPT-4o
Good: Claude 3.5 Sonnet, GPT-4 Turbo

# Data Analysis
Best: GPT-4o, Claude 3.5 Sonnet
Good: GPT-4 Turbo with function calling
```

### By Cost

```yaml
# Most Expensive (per token)
- Claude 3 Opus: $15/1M output tokens
- GPT-4o: $10/1M output tokens
- Claude 3.5 Sonnet: $3/1M input, $15/1M output

# Cost Effective
- GPT-3.5 Turbo: $0.50/1M input, $1.50/1M output
- Claude 3 Haiku: $0.25/1M input, $1.25/1M output
- Local models: $0 (one-time hardware cost)

# Best Value
- GPT-4o: Excellent quality at reasonable price
- Claude 3.5 Sonnet: Premium quality when needed
- GPT-4o Mini: Good balance for most tasks
```

### By Speed

```yaml
# Fastest (under 1 second response)
- GPT-3.5 Turbo
- Claude 3 Haiku
- GPT-4o Mini

# Balanced (1-3 seconds)
- GPT-4o
- Claude 3.5 Sonnet
- GPT-4 Turbo

# Slower (3+ seconds)
- Claude 3 Opus
- GPT-4
- Large local models
```

## Advanced Configuration

### Model Parameters

```yaml
# Temperature (creativity vs consistency)
# 0.0-0.3: Consistent, factual responses
# 0.4-0.7: Balanced creativity and consistency
# 0.8-1.0: Highly creative, varied responses

# Max Tokens (response length)
# 512: Short answers
# 1024: Medium responses
# 2048: Long explanations
# 4096+: Comprehensive answers

# Top P (nucleus sampling)
# 0.1: Very focused responses
# 0.5: Balanced diversity
# 0.9: High diversity

# Frequency/Presence Penalty
# -0.5 to 0.5: Reduce repetition (negative) or encourage variety (positive)
```

```json
{
  "model": "gpt-4o",
  "temperature": 0.7,
  "max_tokens": 2048,
  "top_p": 0.9,
  "frequency_penalty": 0.0,
  "presence_penalty": 0.0,
  "system_prompt": "You are a helpful assistant that answers questions based on the provided documents."
}
```

### Custom System Prompts

```yaml
# Default system prompt
"You are a helpful assistant that answers questions based on the provided documents."

# Technical documentation
"You are a technical documentation assistant. Provide accurate, detailed answers based on the provided technical documentation. Include code examples when relevant."

# Customer support
"You are a customer support assistant. Be helpful, patient, and provide step-by-step solutions based on the support documentation."

# Research assistant
"You are a research assistant. Provide comprehensive, well-referenced answers based on the academic papers and research documents provided."

# Custom domain
"You are a [DOMAIN] expert assistant. Answer questions based on the provided [DOMAIN] documentation and best practices."
```

### Workspace-Specific Settings

```bash
# Different settings per workspace
curl -X PUT http://localhost:3001/api/v1/workspace/ws-123/llm-settings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.3,
    "max_tokens": 4096,
    "system_prompt": "You are a technical documentation assistant specializing in API documentation."
  }'
```

## Performance Optimization

### Caching Strategies

```yaml
# Response caching
# AnythingLLM automatically caches responses
# Configure cache settings in advanced options

# Embedding caching
# Reuse embeddings for unchanged documents
# Reduces processing time for updates

# Model caching
# Keep models loaded in memory
# Faster response times for local models
```

### Parallel Processing

```bash
# Configure thread pool size
export UV_THREADPOOL_SIZE=20

# Multiple worker processes
# Scale horizontally for high load
docker-compose up -d --scale anythingllm=3
```

### Rate Limiting

```yaml
# Configure API rate limits
# Prevent overwhelming external APIs
# Different limits for different providers

# OpenAI: 10,000 RPM for GPT-4
# Anthropic: 50 requests per minute
# Local: Limited by hardware
```

## Multi-Model Strategies

### Model Routing

```yaml
# Route different types of queries to appropriate models
# Complex reasoning → Claude Opus
# Fast answers → GPT-3.5 Turbo
# Code generation → GPT-4o

# Configuration example:
query_routing:
  - pattern: "write.*code|function|class"
    model: "gpt-4o"
    priority: 1
  - pattern: "explain.*complex|analyze"
    model: "claude-3-5-sonnet-20241022"
    priority: 2
  - default: "gpt-3.5-turbo"
```

### Fallback Models

```yaml
# Primary model fails → fallback to secondary
# GPT-4o → GPT-3.5 Turbo
# Claude Sonnet → Claude Haiku
# Cloud → Local model

fallback_chain:
  - "gpt-4o"
  - "gpt-4-turbo"
  - "gpt-3.5-turbo"
  - "ollama/llama3.1:70b"
```

### Ensemble Methods

```yaml
# Combine multiple models for better results
# Average responses from different models
# Use strongest model for final answer
# Combine strengths of different approaches

ensemble_config:
  models:
    - name: "gpt-4o"
      weight: 0.4
      role: "primary"
    - name: "claude-3-5-sonnet-20241022"
      weight: 0.4
      role: "reasoning"
    - name: "ollama/llama3.1:70b"
      weight: 0.2
      role: "verification"
```

## Monitoring and Analytics

### Usage Tracking

```bash
# Monitor API usage and costs
curl http://localhost:3001/api/v1/analytics/usage \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "total_queries": 15420,
  "total_tokens": 2847392,
  "cost_breakdown": {
    "openai": 45.67,
    "anthropic": 23.89,
    "ollama": 0.00
  },
  "performance": {
    "average_response_time": 2.3,
    "success_rate": 0.987,
    "error_rate": 0.013
  }
}
```

### Model Performance Metrics

```bash
# Compare model performance
curl http://localhost:3001/api/v1/analytics/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Response:
{
  "models": [
    {
      "name": "gpt-4o",
      "queries": 8920,
      "avg_response_time": 1.8,
      "success_rate": 0.992,
      "avg_cost_per_query": 0.015
    },
    {
      "name": "claude-3-5-sonnet-20241022",
      "queries": 6500,
      "avg_response_time": 2.1,
      "success_rate": 0.985,
      "avg_cost_per_query": 0.023
    }
  ]
}
```

### Cost Optimization

```yaml
# Set spending limits
budget_limits:
  monthly_budget: 500.00
  per_model_limits:
    gpt-4o: 200.00
    claude-3-5-sonnet-20241022: 200.00
    ollama: 0.00  # Unlimited

# Auto-switch to cheaper models when approaching limits
cost_optimization:
  enable_auto_switch: true
  cheap_model: "gpt-3.5-turbo"
  threshold_percentage: 80
```

## Troubleshooting LLM Issues

### Connection Problems

```bash
# Test API connectivity
curl -I https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Check Ollama status
curl http://localhost:11434/api/tags

# Verify API keys
echo $OPENAI_API_KEY | wc -c  # Should be > 50 chars
echo $ANTHROPIC_API_KEY | head -c 20  # Should start with sk-ant
```

### Model Errors

```bash
# Common errors:
# - Rate limit exceeded
# - Invalid API key
# - Model not available
# - Context length exceeded
# - Content policy violation

# Check logs for details
docker logs anythingllm | grep -i error
```

### Performance Issues

```bash
# Slow responses may be due to:
# - Large context windows
# - Complex queries
# - API rate limiting
# - Network latency
# - Model overload

# Optimize by:
# - Reducing max tokens
# - Using faster models
# - Implementing caching
# - Load balancing across instances
```

### Quality Issues

```bash
# Poor answers may indicate:
# - Wrong model for the task
# - Incorrect temperature settings
# - Insufficient context
# - Poor document quality

# Solutions:
# - Switch to more capable model
# - Adjust temperature (lower for factual, higher for creative)
# - Improve document processing
# - Add better system prompts
```

## Advanced LLM Features

### Function Calling

```yaml
# Enable function calling for structured outputs
# Useful for API integrations and tool use

function_calling:
  enabled: true
  allowed_functions:
    - "search_database"
    - "execute_query"
    - "send_email"
    - "create_ticket"
```

### Streaming Responses

```yaml
# Real-time streaming for better UX
streaming:
  enabled: true
  chunk_size: 50
  retry_on_disconnect: true
```

### Custom Model Fine-tuning

```yaml
# Fine-tune models on your documents
# Create domain-specific models
# Better accuracy for specialized content

fine_tuning:
  enabled: true
  base_model: "gpt-3.5-turbo"
  training_data: "workspace_documents"
  epochs: 3
  learning_rate: 0.0001
```

## Summary

In this chapter, we've covered:

- **LLM Providers**: OpenAI, Anthropic, Ollama, and others
- **Model Selection**: Choosing models by use case, cost, and speed
- **Configuration**: Parameters, system prompts, and workspace settings
- **Performance**: Caching, parallel processing, and rate limiting
- **Multi-Model**: Routing, fallbacks, and ensemble methods
- **Monitoring**: Usage tracking and performance analytics
- **Troubleshooting**: Connection, performance, and quality issues
- **Advanced Features**: Function calling, streaming, and fine-tuning

## Key Takeaways

1. **Model Selection**: Choose based on task complexity, cost, and speed requirements
2. **Configuration**: Fine-tune parameters for optimal results
3. **Cost Management**: Monitor usage and implement cost controls
4. **Performance**: Optimize with caching and parallel processing
5. **Reliability**: Implement fallbacks and error handling
6. **Monitoring**: Track performance and usage patterns
7. **Troubleshooting**: Systematic approach to resolving issues

## Next Steps

Now that you can configure LLMs effectively, let's explore **vector stores** and choosing the right storage backend.

---

**Ready for Chapter 5?** [Vector Stores](05-vector-stores.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*