---
layout: default
title: "Pydantic AI Tutorial - Chapter 2: Model Configuration"
nav_order: 2
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 2: Advanced Model Configuration & Provider Setup

> Master multi-provider setups, fallback strategies, and advanced model configuration for robust AI agent systems.

## Multi-Provider Setup

### Provider Configuration

```python
from pydantic_ai import Agent
from typing import List, Dict, Any
import os

class MultiProviderConfig:
    """Configuration for multiple AI providers with fallback."""

    def __init__(self):
        self.providers = {
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
                'priority': 1,
                'cost_per_token': {'input': 0.03, 'output': 0.06}
            },
            'anthropic': {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'models': ['claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
                'priority': 2,
                'cost_per_token': {'input': 15, 'output': 75}  # per million tokens
            },
            'google': {
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'models': ['gemini-1.5-pro', 'gemini-1.5-flash'],
                'priority': 3,
                'cost_per_token': {'input': 0.5, 'output': 1.5}  # per million chars
            },
            'groq': {
                'api_key': os.getenv('GROQ_API_KEY'),
                'models': ['mixtral-8x7b-32768', 'llama3-70b-8192'],
                'priority': 4,
                'cost_per_token': {'input': 0.27, 'output': 0.27}  # per million tokens
            }
        }

    def get_best_provider(self, requirements: Dict[str, Any] = None) -> str:
        """Get the best provider based on requirements."""

        if not requirements:
            # Return highest priority provider
            return min(self.providers.keys(), key=lambda x: self.providers[x]['priority'])

        # Check specific requirements
        if requirements.get('speed') == 'fast':
            return 'groq'  # Fastest inference
        elif requirements.get('quality') == 'high':
            return 'openai'  # GPT-4
        elif requirements.get('cost') == 'low':
            return 'groq'  # Lowest cost
        elif requirements.get('multimodal'):
            return 'google'  # Best multimodal support

        return min(self.providers.keys(), key=lambda x: self.providers[x]['priority'])

    def create_agent_with_fallback(self, primary_provider: str = None) -> Agent:
        """Create agent with automatic fallback to other providers."""

        if not primary_provider:
            primary_provider = self.get_best_provider()

        # Create agent with primary provider
        agent = Agent(f"{primary_provider}:{self.providers[primary_provider]['models'][0]}")

        # Add fallback logic (this would be implemented in a custom agent class)
        agent.fallback_providers = [
            p for p in self.providers.keys()
            if p != primary_provider
        ]

        return agent

# Create multi-provider configuration
config = MultiProviderConfig()

# Create agents optimized for different use cases
fast_agent = config.create_agent_with_fallback('groq')        # Speed optimized
quality_agent = config.create_agent_with_fallback('openai')   # Quality optimized
cost_agent = config.create_agent_with_fallback('groq')        # Cost optimized
multimodal_agent = config.create_agent_with_fallback('google') # Multimodal optimized

# Test different agents
query = "Explain the concept of recursion in programming"

print("Testing different agent configurations:")
print("\nFast Agent (Groq):")
result_fast = fast_agent.run_sync(query)
print(f"Response time: ~0.5-2s, Cost: Low")

print("\nQuality Agent (OpenAI):")
result_quality = quality_agent.run_sync(query)
print(f"Response time: ~2-5s, Cost: Medium")

print("\nCost Agent (Groq):")
result_cost = cost_agent.run_sync(query)
print(f"Response time: ~0.5-2s, Cost: Low")
```

### Provider-Specific Settings

```python
from pydantic_ai import Agent

# OpenAI-specific configuration
openai_agent = Agent(
    'openai:gpt-4',
    model_settings={
        'temperature': 0.7,
        'max_tokens': 1000,
        'top_p': 0.9,
        'frequency_penalty': 0.1,
        'presence_penalty': 0.1,
        'logit_bias': {"1234": -100},  # Discourage certain tokens
        'user': 'my-app-user',  # For usage tracking
    }
)

# Anthropic-specific configuration
anthropic_agent = Agent(
    'anthropic:claude-3-sonnet-20240229',
    model_settings={
        'max_tokens': 4096,
        'temperature': 0.7,
        'top_p': 0.9,
        'top_k': 250,  # Anthropic-specific parameter
        'stop_sequences': ['Human:', 'Assistant:'],
        'metadata': {'user_id': '12345'}  # Custom metadata
    }
)

# Google Gemini configuration
google_agent = Agent(
    'google:gemini-1.5-pro',
    model_settings={
        'temperature': 0.8,
        'max_output_tokens': 2048,
        'top_p': 0.8,
        'top_k': 40,
        'candidate_count': 1,
        'safety_settings': [
            {
                'category': 'HARM_CATEGORY_HARASSMENT',
                'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
            }
        ]
    }
)

# Groq configuration (minimal settings)
groq_agent = Agent(
    'groq:mixtral-8x7b-32768',
    model_settings={
        'temperature': 0.6,
        'max_tokens': 4096,
        'top_p': 0.9
    }
)

# Test provider-specific behavior
test_prompts = [
    "Write a haiku about artificial intelligence",
    "Solve this math problem: 15 * 23 + sqrt(144)",
    "What are the benefits of renewable energy?"
]

providers = {
    'OpenAI GPT-4': openai_agent,
    'Anthropic Claude': anthropic_agent,
    'Google Gemini': google_agent,
    'Groq Mixtral': groq_agent
}

print("Provider comparison:")
for prompt in test_prompts:
    print(f"\nPrompt: {prompt[:50]}...")
    for provider_name, agent in providers.items():
        try:
            result = agent.run_sync(prompt)
            response_length = len(result.data.split())
            print(f"  {provider_name}: {response_length} words")
        except Exception as e:
            print(f"  {provider_name}: Error - {e}")
```

## Fallback and Retry Strategies

### Automatic Fallback System

```python
from typing import List, Optional, Dict, Any
from pydantic_ai import Agent, UnexpectedModelBehavior
import time
import asyncio

class FallbackAgent:
    """Agent with automatic fallback to multiple providers."""

    def __init__(self, providers: List[Dict[str, Any]], result_type=None):
        self.providers = providers  # List of provider configs
        self.result_type = result_type
        self.current_provider_idx = 0
        self.failures = {i: 0 for i in range(len(providers))}

    def get_current_agent(self) -> Agent:
        """Get agent for current provider."""
        provider_config = self.providers[self.current_provider_idx]

        model_string = f"{provider_config['name']}:{provider_config['model']}"

        return Agent(
            model_string,
            result_type=self.result_type,
            model_settings=provider_config.get('settings', {})
        )

    def switch_to_next_provider(self):
        """Switch to next provider in rotation."""
        self.current_provider_idx = (self.current_provider_idx + 1) % len(self.providers)
        print(f"Switching to provider: {self.providers[self.current_provider_idx]['name']}")

    async def run_with_fallback(self, prompt: str, max_attempts: int = 3) -> Any:
        """Run with automatic fallback on failures."""

        last_error = None

        for attempt in range(max_attempts):
            try:
                agent = self.get_current_agent()
                result = await agent.run(prompt)

                # Success - reset failure count for this provider
                self.failures[self.current_provider_idx] = 0

                return result

            except UnexpectedModelBehavior as e:
                print(f"Provider {self.providers[self.current_provider_idx]['name']} failed: {e}")
                last_error = e

                # Record failure
                self.failures[self.current_provider_idx] += 1

                # Switch to next provider
                self.switch_to_next_provider()

            except Exception as e:
                print(f"Unexpected error with {self.providers[self.current_provider_idx]['name']}: {e}")
                last_error = e
                self.failures[self.current_provider_idx] += 1
                self.switch_to_next_provider()

        raise RuntimeError(f"All providers failed after {max_attempts} attempts. Last error: {last_error}")

# Define fallback providers
fallback_providers = [
    {
        'name': 'openai',
        'model': 'gpt-4',
        'settings': {'temperature': 0.7, 'max_tokens': 1000}
    },
    {
        'name': 'anthropic',
        'model': 'claude-3-sonnet-20240229',
        'settings': {'temperature': 0.7, 'max_tokens': 1000}
    },
    {
        'name': 'google',
        'model': 'gemini-1.5-flash',
        'settings': {'temperature': 0.7, 'max_output_tokens': 1000}
    },
    {
        'name': 'groq',
        'model': 'mixtral-8x7b-32768',
        'settings': {'temperature': 0.7, 'max_tokens': 1000}
    }
]

# Create fallback agent
fallback_agent = FallbackAgent(fallback_providers)

# Test with problematic prompt that might be filtered
test_prompt = "Explain how to make a simple calculator program"

print("Testing fallback system:")
result = asyncio.run(fallback_agent.run_with_fallback(test_prompt))
print(f"Final result from: {fallback_agent.providers[fallback_agent.current_provider_idx]['name']}")
print(result.data[:200] + "...")
```

### Circuit Breaker Pattern

```python
import asyncio
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, requests rejected
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker for provider failure handling."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60,
                 success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.success_count = 0

    def can_execute(self) -> bool:
        """Check if request can be executed."""

        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True

        return False

    def record_success(self):
        """Record successful execution."""

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._reset()
        else:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self):
        """Record failed execution."""

        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""

        if self.last_failure_time is None:
            return True

        time_since_failure = datetime.now() - self.last_failure_time
        return time_since_failure.total_seconds() >= self.recovery_timeout

    def _reset(self):
        """Reset circuit to closed state."""

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        print("Circuit breaker reset - service recovered")

# Enhanced fallback agent with circuit breaker
class CircuitBreakerAgent(FallbackAgent):
    """Agent with circuit breaker protection."""

    def __init__(self, providers: List[Dict[str, Any]], result_type=None):
        super().__init__(providers, result_type)
        self.circuit_breakers = {
            i: CircuitBreaker() for i in range(len(providers))
        }

    async def run_with_fallback(self, prompt: str, max_attempts: int = 3) -> Any:
        """Run with circuit breaker protection."""

        for attempt in range(max_attempts):
            provider_idx = self.current_provider_idx
            circuit_breaker = self.circuit_breakers[provider_idx]

            # Check if circuit breaker allows execution
            if not circuit_breaker.can_execute():
                print(f"Circuit breaker OPEN for provider {provider_idx}, skipping")
                self.switch_to_next_provider()
                continue

            try:
                agent = self.get_current_agent()
                result = await agent.run(prompt)

                # Record success
                circuit_breaker.record_success()
                self.failures[provider_idx] = 0

                return result

            except Exception as e:
                print(f"Provider {provider_idx} failed: {e}")

                # Record failure
                circuit_breaker.record_failure()
                self.failures[provider_idx] += 1

                # Switch to next provider
                self.switch_to_next_provider()

        raise RuntimeError("All providers failed or circuit breakers are open")

# Test circuit breaker
circuit_agent = CircuitBreakerAgent(fallback_providers)

print("Testing circuit breaker (this may take a moment):")
try:
    result = asyncio.run(circuit_agent.run_with_fallback("Hello, world!"))
    print("Success:", result.data[:100] + "...")
except Exception as e:
    print("All attempts failed:", e)
```

## Model Selection Strategies

### Context-Aware Model Selection

```python
from enum import Enum

class TaskType(Enum):
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    CODING = "coding"
    CONVERSATIONAL = "conversational"
    MATHEMATICAL = "mathematical"
    RESEARCH = "research"

class IntelligentModelSelector:
    """Select models based on task characteristics."""

    def __init__(self):
        # Model capabilities and optimal use cases
        self.model_profiles = {
            'openai:gpt-4': {
                'strengths': [TaskType.ANALYTICAL, TaskType.CODING, TaskType.RESEARCH, TaskType.CONVERSATIONAL],
                'cost': 'high',
                'speed': 'medium',
                'context_window': 8192,
                'multimodal': False
            },
            'openai:gpt-4-turbo': {
                'strengths': [TaskType.ANALYTICAL, TaskType.CODING, TaskType.RESEARCH],
                'cost': 'medium',
                'speed': 'medium',
                'context_window': 128000,
                'multimodal': True
            },
            'anthropic:claude-3-opus-20240229': {
                'strengths': [TaskType.ANALYTICAL, TaskType.CREATIVE, TaskType.RESEARCH],
                'cost': 'high',
                'speed': 'slow',
                'context_window': 200000,
                'multimodal': False
            },
            'anthropic:claude-3-haiku-20240307': {
                'strengths': [TaskType.CONVERSATIONAL, TaskType.CODING],
                'cost': 'low',
                'speed': 'fast',
                'context_window': 200000,
                'multimodal': False
            },
            'google:gemini-1.5-pro': {
                'strengths': [TaskType.ANALYTICAL, TaskType.CREATIVE, TaskType.RESEARCH],
                'cost': 'medium',
                'speed': 'medium',
                'context_window': 1000000,
                'multimodal': True
            },
            'groq:mixtral-8x7b-32768': {
                'strengths': [TaskType.CONVERSATIONAL, TaskType.CODING, TaskType.MATHEMATICAL],
                'cost': 'low',
                'speed': 'fast',
                'context_window': 32768,
                'multimodal': False
            }
        }

    def analyze_task(self, prompt: str) -> TaskType:
        """Analyze task type from prompt."""

        prompt_lower = prompt.lower()

        # Code-related keywords
        if any(word in prompt_lower for word in ['function', 'class', 'import', 'def ', 'code', 'program']):
            return TaskType.CODING

        # Math-related keywords
        if any(word in prompt_lower for word in ['calculate', 'equation', 'solve', 'math', 'formula']):
            return TaskType.MATHEMATICAL

        # Research keywords
        if any(word in prompt_lower for word in ['research', 'analyze', 'study', 'investigate', 'find']):
            return TaskType.RESEARCH

        # Creative keywords
        if any(word in prompt_lower for word in ['write', 'create', 'design', 'story', 'poem', 'art']):
            return TaskType.CREATIVE

        # Analytical keywords
        if any(word in prompt_lower for word in ['explain', 'analyze', 'compare', 'evaluate', 'assess']):
            return TaskType.ANALYTICAL

        # Default to conversational
        return TaskType.CONVERSATIONAL

    def select_model(self, task_type: TaskType, constraints: Dict[str, Any] = None) -> str:
        """Select best model for task type."""

        constraints = constraints or {}

        # Filter models by constraints
        available_models = {}

        for model_name, profile in self.model_profiles.items():
            # Check if model supports task type
            if task_type not in profile['strengths']:
                continue

            # Check cost constraint
            if 'max_cost' in constraints:
                if profile['cost'] == 'high' and constraints['max_cost'] == 'low':
                    continue

            # Check speed constraint
            if 'min_speed' in constraints:
                if profile['speed'] == 'slow' and constraints['min_speed'] == 'fast':
                    continue

            # Check multimodal requirement
            if constraints.get('multimodal_required') and not profile['multimodal']:
                continue

            # Check context length requirement
            if 'min_context' in constraints:
                if profile['context_window'] < constraints['min_context']:
                    continue

            available_models[model_name] = profile

        if not available_models:
            # Fallback to GPT-4
            return 'openai:gpt-4'

        # Score and rank models
        scored_models = []
        for model_name, profile in available_models.items():
            score = 0

            # Prefer models where task is primary strength
            if task_type == profile['strengths'][0]:
                score += 3

            # Prefer faster models for speed
            if profile['speed'] == 'fast':
                score += 2
            elif profile['speed'] == 'medium':
                score += 1

            # Prefer lower cost models
            if profile['cost'] == 'low':
                score += 2
            elif profile['cost'] == 'medium':
                score += 1

            scored_models.append((score, model_name))

        # Return highest scoring model
        scored_models.sort(reverse=True)
        return scored_models[0][1]

# Create intelligent selector
selector = IntelligentModelSelector()

# Test model selection for different tasks
test_tasks = [
    "Write a Python function to sort a list",
    "Calculate the area of a circle with radius 5",
    "Research the history of artificial intelligence",
    "Write a creative story about time travel",
    "Analyze the pros and cons of electric vehicles",
    "Hello, how are you today?"
]

print("Intelligent Model Selection:")
for task in test_tasks:
    task_type = selector.analyze_task(task)
    selected_model = selector.select_model(task_type)

    print(f"Task: {task[:40]}...")
    print(f"  Type: {task_type.value}")
    print(f"  Model: {selected_model}")
    print()

# Test with constraints
constrained_model = selector.select_model(
    TaskType.RESEARCH,
    constraints={
        'max_cost': 'medium',
        'min_speed': 'medium',
        'multimodal_required': False
    }
)

print(f"Constrained selection: {constrained_model}")
```

## Custom Model Settings

### Dynamic Configuration

```python
from typing import Dict, Any, Callable

class DynamicModelConfigurator:
    """Dynamically configure models based on context."""

    def __init__(self):
        self.config_strategies: Dict[str, Callable] = {}

    def add_strategy(self, task_type: str, config_func: Callable[[str], Dict[str, Any]]):
        """Add configuration strategy for task type."""
        self.config_strategies[task_type] = config_func

    def get_config(self, task_type: str, prompt: str) -> Dict[str, Any]:
        """Get configuration for task type and prompt."""
        if task_type in self.config_strategies:
            return self.config_strategies[task_type](prompt)

        return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'temperature': 0.7,
            'max_tokens': 1000,
            'top_p': 0.9
        }

# Create configurator
configurator = DynamicModelConfigurator()

# Strategy for creative tasks
def creative_config(prompt: str) -> Dict[str, Any]:
    """Configuration for creative tasks."""
    length = len(prompt.split())

    return {
        'temperature': 0.9,  # Higher creativity
        'max_tokens': 500 if length < 10 else 1000,
        'top_p': 0.95,
        'presence_penalty': 0.3,  # Encourage diverse content
        'frequency_penalty': 0.3
    }

# Strategy for analytical tasks
def analytical_config(prompt: str) -> Dict[str, Any]:
    """Configuration for analytical tasks."""
    return {
        'temperature': 0.1,  # Lower randomness for consistency
        'max_tokens': 1500,  # Allow longer responses
        'top_p': 0.8,
        'presence_penalty': 0.0,  # Allow repetition if needed
        'frequency_penalty': 0.1
    }

# Strategy for coding tasks
def coding_config(prompt: str) -> Dict[str, Any]:
    """Configuration for coding tasks."""
    return {
        'temperature': 0.2,  # Low randomness for correctness
        'max_tokens': 2000,  # Allow long code responses
        'top_p': 0.85,
        'stop_sequences': ['```'],  # Stop at code block end
        'frequency_penalty': 0.0  # Allow code patterns to repeat
    }

# Add strategies
configurator.add_strategy('creative', creative_config)
configurator.add_strategy('analytical', analytical_config)
configurator.add_strategy('coding', coding_config)

# Create agent with dynamic configuration
class DynamicConfigAgent(Agent):
    """Agent with dynamic model configuration."""

    def __init__(self, model_string: str, configurator: DynamicModelConfigurator, **kwargs):
        super().__init__(model_string, **kwargs)
        self.configurator = configurator

    def run_sync(self, prompt: str, **kwargs):
        """Run with dynamic configuration."""
        # Analyze task type (simplified)
        task_type = self._analyze_task_type(prompt)

        # Get dynamic config
        dynamic_config = self.configurator.get_config(task_type, prompt)

        # Update model settings
        if hasattr(self, 'model_settings'):
            self.model_settings.update(dynamic_config)
        else:
            self.model_settings = dynamic_config

        return super().run_sync(prompt, **kwargs)

    def _analyze_task_type(self, prompt: str) -> str:
        """Simple task type analysis."""
        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ['write', 'create', 'story', 'poem']):
            return 'creative'
        elif any(word in prompt_lower for word in ['explain', 'analyze', 'compare']):
            return 'analytical'
        elif any(word in prompt_lower for word in ['code', 'function', 'class', 'program']):
            return 'coding'

        return 'default'

# Test dynamic configuration
dynamic_agent = DynamicConfigAgent('openai:gpt-4', configurator)

test_prompts = [
    "Write a short poem about the ocean",
    "Explain how machine learning algorithms work",
    "Create a Python function to calculate fibonacci numbers"
]

for prompt in test_prompts:
    print(f"Prompt: {prompt[:40]}...")
    result = dynamic_agent.run_sync(prompt)
    print(f"Response length: {len(result.data)} characters")
    print("-" * 50)
```

## Provider Health Monitoring

### Health Checks and Load Balancing

```python
import aiohttp
import asyncio
from typing import Dict, Any, List
import time

class ProviderHealthMonitor:
    """Monitor health and performance of AI providers."""

    def __init__(self, providers: Dict[str, Any]):
        self.providers = providers
        self.health_status = {}
        self.response_times = {}
        self.error_rates = {}

        # Initialize tracking
        for provider_name in providers.keys():
            self.health_status[provider_name] = True
            self.response_times[provider_name] = []
            self.error_rates[provider_name] = 0.0

    async def check_provider_health(self, provider_name: str) -> bool:
        """Check if provider is responding."""

        provider_config = self.providers.get(provider_name)
        if not provider_config:
            return False

        try:
            # Simple health check - try to create agent and run basic query
            test_agent = Agent(f"{provider_name}:{provider_config['models'][0]}")

            start_time = time.time()
            result = await test_agent.run("Hello")
            response_time = time.time() - start_time

            # Record metrics
            self.response_times[provider_name].append(response_time)
            self.error_rates[provider_name] = 0.0  # Reset on success

            # Keep only last 10 response times
            if len(self.response_times[provider_name]) > 10:
                self.response_times[provider_name] = self.response_times[provider_name][-10:]

            return True

        except Exception as e:
            print(f"Health check failed for {provider_name}: {e}")

            # Update error rate
            self.error_rates[provider_name] = min(1.0, self.error_rates[provider_name] + 0.1)

            return False

    async def monitor_all_providers(self):
        """Monitor all providers periodically."""

        while True:
            print("Checking provider health...")

            tasks = []
            for provider_name in self.providers.keys():
                task = self.check_provider_health(provider_name)
                tasks.append((provider_name, task))

            # Run health checks concurrently
            results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)

            # Update health status
            for (provider_name, _), healthy in zip(tasks, results):
                if isinstance(healthy, Exception):
                    self.health_status[provider_name] = False
                else:
                    self.health_status[provider_name] = healthy

            # Print status
            healthy_providers = [p for p, h in self.health_status.items() if h]
            print(f"Healthy providers: {', '.join(healthy_providers)}")

            await asyncio.sleep(60)  # Check every minute

    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report."""

        report = {
            'overall_health': 'healthy',
            'provider_status': {},
            'performance_metrics': {}
        }

        # Check if any providers are down
        if not any(self.health_status.values()):
            report['overall_health'] = 'critical'
        elif not all(self.health_status.values()):
            report['overall_health'] = 'degraded'

        # Provider status
        for provider_name, healthy in self.health_status.items():
            provider_info = {
                'healthy': healthy,
                'error_rate': self.error_rates[provider_name]
            }

            # Performance metrics
            if self.response_times[provider_name]:
                provider_info['avg_response_time'] = sum(self.response_times[provider_name]) / len(self.response_times[provider_name])
                provider_info['min_response_time'] = min(self.response_times[provider_name])
                provider_info['max_response_time'] = max(self.response_times[provider_name])

            report['provider_status'][provider_name] = provider_info

        return report

    def get_best_provider(self, requirements: Dict[str, Any] = None) -> str:
        """Get best available provider based on health and requirements."""

        healthy_providers = [p for p, h in self.health_status.items() if h]

        if not healthy_providers:
            raise RuntimeError("No healthy providers available")

        if not requirements:
            # Return provider with lowest error rate
            return min(healthy_providers, key=lambda p: self.error_rates[p])

        # Apply requirements
        if requirements.get('speed') == 'fast':
            # Return provider with lowest average response time
            return min(healthy_providers,
                      key=lambda p: sum(self.response_times[p]) / len(self.response_times[p]) if self.response_times[p] else float('inf'))

        # Default: lowest error rate
        return min(healthy_providers, key=lambda p: self.error_rates[p])

# Usage
providers_config = {
    'openai': {'models': ['gpt-4'], 'priority': 1},
    'anthropic': {'models': ['claude-3-sonnet-20240229'], 'priority': 2},
    'google': {'models': ['gemini-1.5-flash'], 'priority': 3}
}

health_monitor = ProviderHealthMonitor(providers_config)

# Start monitoring
asyncio.create_task(health_monitor.monitor_all_providers())

# Get health report
report = health_monitor.get_health_report()
print("Health Report:")
print(f"Overall: {report['overall_health']}")
for provider, status in report['provider_status'].items():
    print(f"  {provider}: {'✓' if status['healthy'] else '✗'} (error rate: {status['error_rate']:.1f})")

# Get best provider
best_provider = health_monitor.get_best_provider({'speed': 'fast'})
print(f"Best provider for speed: {best_provider}")
```

This comprehensive model configuration chapter covers advanced provider setup, fallback strategies, intelligent model selection, and health monitoring for robust, production-ready AI agent systems. 🚀