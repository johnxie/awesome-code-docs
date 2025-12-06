---
layout: default
title: "Open WebUI Tutorial - Chapter 2: Model Management"
nav_order: 2
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 2: Model Management & Backend Configuration

> Connect multiple LLM backends, manage models, and optimize performance across different providers.

## Backend Architecture

Open WebUI supports multiple LLM backends simultaneously:

```
┌─────────────────┐
│   Open WebUI    │
│  Load Balancer  │
└─────────────────┘
         │
    ┌────┼────┐
    │         │
┌───▼───┐ ┌───▼───┐
│ Ollama │ │OpenAI │
│ Local  │ │ Cloud │
└───────┘ └───────┘
    │         │
┌───▼───┐ ┌───▼───┐
│Anthropic│ │LocalAI│
│  Cloud  │ │ Local │
└────────┘ └───────┘
```

## Ollama Backend Setup

### Advanced Ollama Configuration

```bash
# Start Ollama with custom settings
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MAX_LOADED_MODELS=3
export OLLAMA_MAX_QUEUE=512
export OLLAMA_RUNNERS_DIR=/opt/ollama/runners

ollama serve
```

### Model Management

```bash
# List available models
ollama list

# Pull multiple models
ollama pull llama2:13b
ollama pull codellama:13b
ollama pull mistral:7b

# Create custom model
echo 'FROM llama2:7b
SYSTEM "You are a helpful coding assistant."
PARAMETER temperature 0.7
PARAMETER top_p 0.9' > Modelfile

ollama create coding-assistant -f Modelfile
```

### GPU Acceleration

```bash
# Check GPU support
ollama show llama2:7b | grep -A 10 "modelfile"

# Configure GPU layers (GGUF models)
echo 'FROM llama2:7b
PARAMETER num_gpu 35  # Use 35 GPU layers
PARAMETER num_thread 8 # CPU threads' > gpu_modelfile

ollama create llama2-gpu -f gpu_modelfile
```

## OpenAI API Configuration

### Multiple API Keys & Load Balancing

```python
# config.py - Advanced OpenAI setup
import os
from typing import List, Dict

class OpenAIConfig:
    def __init__(self):
        self.api_keys = [
            os.getenv('OPENAI_API_KEY_1'),
            os.getenv('OPENAI_API_KEY_2'),
            os.getenv('OPENAI_API_KEY_3')
        ]

        self.models = {
            'gpt-4': {'priority': 1, 'cost_per_token': 0.03},
            'gpt-4-turbo': {'priority': 2, 'cost_per_token': 0.01},
            'gpt-3.5-turbo': {'priority': 3, 'cost_per_token': 0.002}
        }

        self.rate_limits = {
            'gpt-4': {'rpm': 200, 'tpm': 40000},
            'gpt-4-turbo': {'rpm': 500, 'tpm': 60000},
            'gpt-3.5-turbo': {'rpm': 3500, 'tpm': 90000}
        }

    def get_best_available_key(self, model: str) -> str:
        """Get the best available API key based on usage."""
        # Implement key rotation logic
        return self.api_keys[0]  # Simplified

    def get_model_config(self, model: str) -> Dict:
        return self.models.get(model, {})

# Environment variables
OPENAI_API_KEY_1=sk-key1...
OPENAI_API_KEY_2=sk-key2...
OPENAI_API_KEY_3=sk-key3...

# Model aliases
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

### Cost Tracking & Optimization

```python
import time
from collections import defaultdict

class CostTracker:
    def __init__(self):
        self.usage = defaultdict(lambda: {'tokens': 0, 'cost': 0.0, 'calls': 0})
        self.model_pricing = {
            'gpt-4': {'input': 0.03, 'output': 0.06},
            'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
            'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002}
        }

    def track_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        pricing = self.model_pricing.get(model, {'input': 0, 'output': 0})

        input_cost = (prompt_tokens / 1000) * pricing['input']
        output_cost = (completion_tokens / 1000) * pricing['output']
        total_cost = input_cost + output_cost

        self.usage[model]['tokens'] += prompt_tokens + completion_tokens
        self.usage[model]['cost'] += total_cost
        self.usage[model]['calls'] += 1

    def get_usage_report(self):
        return dict(self.usage)

# Integration with Open WebUI
cost_tracker = CostTracker()

# Track costs after each API call
def track_openai_cost(response, model):
    usage = response.usage
    cost_tracker.track_usage(
        model,
        usage.prompt_tokens,
        usage.completion_tokens
    )

    print(f"Cost for {model}: ${cost_tracker.usage[model]['cost']:.4f}")
```

## Anthropic Claude Integration

### Advanced Claude Configuration

```python
# Claude configuration for Open WebUI
import anthropic

class ClaudeManager:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.models = {
            'claude-3-opus': {
                'max_tokens': 4096,
                'context_window': 200000,
                'cost_per_token': 0.015
            },
            'claude-3-sonnet': {
                'max_tokens': 4096,
                'context_window': 200000,
                'cost_per_token': 0.008
            },
            'claude-3-haiku': {
                'max_tokens': 4096,
                'context_window': 200000,
                'cost_per_token': 0.0025
            }
        }

    async def generate_response(self, messages, model='claude-3-sonnet', **kwargs):
        response = await self.client.messages.create(
            model=model,
            max_tokens=self.models[model]['max_tokens'],
            messages=messages,
            **kwargs
        )

        return {
            'content': response.content[0].text,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
        }

# Environment configuration
ANTHROPIC_API_KEY=sk-ant-key...
ANTHROPIC_BASE_URL=https://api.anthropic.com
```

### Vision Models Support

```python
# Claude Vision integration
async def analyze_image_with_claude(image_url: str, prompt: str):
    """Analyze images using Claude Vision."""

    # Download image (in practice, handle base64 or URLs)
    import base64
    with open('image.jpg', 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()

    response = await claude_client.messages.create(
        model="claude-3-opus",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }
        ]
    )

    return response.content[0].text
```

## LocalAI Backend

### LocalAI Setup

```bash
# Run LocalAI with GPU support
docker run -p 8080:8080 \
  -v $PWD/models:/models \
  -e GPU_LAYERS=35 \
  -e THREADS=8 \
  localai/localai:latest \
  --models-path /models \
  --context-size 2048 \
  --threads 8
```

### Model Configuration

```yaml
# models.yaml for LocalAI
models:
  - name: "llama2-7b-chat"
    backend: llama
    model_path: "/models/llama-2-7b-chat.Q4_K_M.gguf"
    model_type: "llama"
    context_size: 2048
    threads: 8
    gpu_layers: 35

  - name: "codellama-13b"
    backend: llama
    model_path: "/models/codellama-13b.Q4_K_M.gguf"
    model_type: "llama"
    context_size: 4096
    threads: 12
    gpu_layers: 40

  - name: "mistral-7b"
    backend: llama
    model_path: "/models/mistral-7b-v0.1.Q4_K_M.gguf"
    model_type: "llama"
    context_size: 8192
    threads: 8
    gpu_layers: 35
```

### Performance Tuning

```bash
# LocalAI performance configuration
export LOCALAI_THREADS=8
export LOCALAI_CONTEXT_SIZE=4096
export LOCALAI_GPU_LAYERS=35
export LOCALAI_MLOCK=true  # Lock model in memory
export LOCALAI_MMAP=true   # Memory map model

# For high-performance setups
export LOCALAI_PARALLEL_REQUESTS=4
export LOCALAI_STREAMING=true
```

## Model Load Balancing

### Intelligent Model Selection

```python
class ModelRouter:
    def __init__(self):
        self.models = {
            'fast': ['gpt-3.5-turbo', 'claude-3-haiku', 'mistral-7b'],
            'balanced': ['gpt-4-turbo', 'claude-3-sonnet', 'llama2-13b'],
            'premium': ['gpt-4', 'claude-3-opus', 'codellama-13b']
        }

        self.model_specs = {
            'gpt-3.5-turbo': {'speed': 9, 'quality': 7, 'cost': 1},
            'gpt-4': {'speed': 5, 'quality': 10, 'cost': 10},
            'claude-3-haiku': {'speed': 9, 'quality': 8, 'cost': 2},
            'claude-3-opus': {'speed': 6, 'quality': 10, 'cost': 12},
            'mistral-7b': {'speed': 8, 'quality': 7, 'cost': 0},
            'llama2-13b': {'speed': 6, 'quality': 8, 'cost': 0}
        }

    def select_model(self, requirements: Dict[str, Any]) -> str:
        """Select best model based on requirements."""

        priority = requirements.get('priority', 'balanced')
        max_cost = requirements.get('max_cost', float('inf'))
        min_quality = requirements.get('min_quality', 0)
        prefer_speed = requirements.get('prefer_speed', False)

        candidates = self.models[priority]

        # Filter by cost and quality
        filtered = []
        for model in candidates:
            specs = self.model_specs[model]
            if specs['cost'] <= max_cost and specs['quality'] >= min_quality:
                filtered.append((model, specs))

        if not filtered:
            return self.models['balanced'][0]  # Fallback

        # Sort by preference
        if prefer_speed:
            filtered.sort(key=lambda x: (-x[1]['speed'], x[1]['cost']))
        else:
            filtered.sort(key=lambda x: (-x[1]['quality'], x[1]['cost']))

        return filtered[0][0]

# Usage
router = ModelRouter()

# Select for different use cases
fast_model = router.select_model({'priority': 'fast'})
premium_model = router.select_model({
    'priority': 'premium',
    'max_cost': 5,
    'min_quality': 9
})
```

### Backend Health Monitoring

```python
import asyncio
import aiohttp

class BackendHealthChecker:
    def __init__(self):
        self.backends = {
            'ollama': {'url': 'http://localhost:11434/api/tags', 'healthy': True},
            'openai': {'url': 'https://api.openai.com/v1/models', 'healthy': True},
            'anthropic': {'url': 'https://api.anthropic.com/v1/messages', 'healthy': True},
            'localai': {'url': 'http://localhost:8080/v1/models', 'healthy': True}
        }

    async def check_health(self):
        """Check health of all backends."""

        async with aiohttp.ClientSession() as session:
            tasks = []

            for name, config in self.backends.items():
                task = self.check_backend(session, name, config)
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for name, result in zip(self.backends.keys(), results):
                if isinstance(result, Exception):
                    self.backends[name]['healthy'] = False
                    print(f"❌ {name} backend unhealthy: {result}")
                else:
                    self.backends[name]['healthy'] = True
                    print(f"✅ {name} backend healthy")

    async def check_backend(self, session, name, config):
        """Check individual backend health."""

        try:
            if name == 'openai':
                headers = {'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'}
                async with session.get(config['url'], headers=headers, timeout=5) as resp:
                    resp.raise_for_status()
            else:
                async with session.get(config['url'], timeout=5) as resp:
                    resp.raise_for_status()

        except Exception as e:
            raise e

    def get_healthy_backends(self):
        """Get list of healthy backends."""
        return [name for name, config in self.backends.items() if config['healthy']]

# Continuous monitoring
health_checker = BackendHealthChecker()

async def monitor_backends():
    while True:
        await health_checker.check_health()
        await asyncio.sleep(60)  # Check every minute

# Start monitoring
asyncio.create_task(monitor_backends())
```

## Model Performance Optimization

### Caching Strategies

```python
from cachetools import TTLCache
import hashlib

class ModelCache:
    def __init__(self, maxsize=1000, ttl=3600):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.hit_count = 0
        self.miss_count = 0

    def get_cache_key(self, messages, model, **kwargs):
        """Generate cache key from request parameters."""
        content = str(messages) + str(model) + str(sorted(kwargs.items()))
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, messages, model, **kwargs):
        key = self.get_cache_key(messages, model, **kwargs)
        result = self.cache.get(key)

        if result:
            self.hit_count += 1
            return result
        else:
            self.miss_count += 1
            return None

    def set(self, messages, model, result, **kwargs):
        key = self.get_cache_key(messages, model, **kwargs)
        self.cache[key] = result

    def get_stats(self):
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        return {
            'hit_rate': hit_rate,
            'hits': self.hit_count,
            'misses': self.miss_count,
            'cache_size': len(self.cache)
        }

# Usage
cache = ModelCache(maxsize=5000, ttl=1800)  # 30 min TTL

def cached_generate_response(messages, model, **kwargs):
    # Check cache first
    cached_result = cache.get(messages, model, **kwargs)
    if cached_result:
        return cached_result

    # Generate response
    result = generate_response(messages, model, **kwargs)

    # Cache result
    cache.set(messages, model, result, **kwargs)

    return result
```

### Model Warm-up & Preloading

```python
class ModelWarmer:
    def __init__(self):
        self.warmup_queries = [
            "Hello, how are you?",
            "What is the capital of France?",
            "Explain quantum computing in simple terms.",
            "Write a Python function to calculate fibonacci numbers."
        ]

    async def warmup_model(self, model_name: str, backend: str):
        """Warm up a model with sample queries."""

        print(f"Warming up {model_name} on {backend}...")

        for query in self.warmup_queries:
            try:
                # Send warmup query
                await self.send_query(backend, model_name, query)
                await asyncio.sleep(0.1)  # Small delay between queries

            except Exception as e:
                print(f"Warmup query failed: {e}")
                continue

        print(f"✅ {model_name} warmed up successfully")

    async def warmup_all_models(self):
        """Warm up all configured models."""

        warmup_tasks = []

        # Ollama models
        ollama_models = ['llama2:7b', 'codellama:7b', 'mistral:7b']
        for model in ollama_models:
            task = self.warmup_model(model, 'ollama')
            warmup_tasks.append(task)

        # Cloud models (limited warmup)
        cloud_models = ['gpt-3.5-turbo']
        for model in cloud_models:
            task = self.warmup_model(model, 'openai')
            warmup_tasks.append(task)

        await asyncio.gather(*warmup_tasks, return_exceptions=True)

# Scheduled warmup
warmer = ModelWarmer()

async def scheduled_warmup():
    while True:
        await warmer.warmup_all_models()
        await asyncio.sleep(3600)  # Warm up every hour
```

## Configuration Best Practices

### Environment-Based Configuration

```bash
# .env.production
# Model Backends
ENABLE_OLLAMA=true
ENABLE_OPENAI=true
ENABLE_ANTHROPIC=true
ENABLE_LOCALAI=false

# Model Settings
DEFAULT_MODEL=gpt-4-turbo
FALLBACK_MODEL=gpt-3.5-turbo

# Performance
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=60
CACHE_TTL=1800

# Cost Control
MAX_COST_PER_HOUR=50.0
COST_ALERT_THRESHOLD=40.0

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Model Selection Logic

```python
def select_optimal_model(user_query: str, user_tier: str = 'free') -> str:
    """Select optimal model based on query and user tier."""

    # Analyze query complexity
    query_length = len(user_query.split())
    has_code = any(keyword in user_query.lower() for keyword in
                   ['function', 'class', 'import', 'def ', 'var '])

    # Tier-based model limits
    tier_limits = {
        'free': {'max_cost': 0.01, 'models': ['gpt-3.5-turbo', 'mistral-7b']},
        'pro': {'max_cost': 0.05, 'models': ['gpt-4-turbo', 'claude-3-sonnet']},
        'enterprise': {'max_cost': float('inf'), 'models': ['gpt-4', 'claude-3-opus']}
    }

    available_models = tier_limits[user_tier]['models']
    max_cost = tier_limits[user_tier]['max_cost']

    # Select based on complexity and cost
    if query_length > 100 or has_code:
        # Complex query - use better model
        candidates = [m for m in available_models if m in ['gpt-4', 'gpt-4-turbo', 'claude-3-opus', 'claude-3-sonnet']]
    else:
        # Simple query - use efficient model
        candidates = available_models

    # Return best available candidate
    model_priority = ['gpt-4', 'claude-3-opus', 'gpt-4-turbo', 'claude-3-sonnet', 'gpt-3.5-turbo', 'mistral-7b']

    for model in model_priority:
        if model in candidates:
            return model

    return available_models[0]  # Fallback
```

This comprehensive model management setup ensures optimal performance, cost efficiency, and reliability across multiple LLM backends. The next chapter covers interface customization and theming. 🚀