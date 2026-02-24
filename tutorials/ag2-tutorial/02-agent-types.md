---
layout: default
title: "AG2 Tutorial - Chapter 2: Agent Types"
nav_order: 2
has_children: false
parent: AG2 Tutorial
---

# Chapter 2: Agent Types & Configuration

Welcome to **Chapter 2: Agent Types & Configuration**. In this part of **AG2 Tutorial: Next-Generation Multi-Agent Framework**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understanding the different agent types in AG2 and how to configure them for various use cases.

## Overview

AG2 provides several built-in agent types, each designed for specific interaction patterns and use cases. This chapter explores the core agent classes and their configuration options.

## Core Agent Types

### AssistantAgent

The `AssistantAgent` is the primary agent type for AI-powered task solving. It's designed to use LLMs to reason about tasks and execute them through natural language interaction.

```python
from ag2 import AssistantAgent

# Basic configuration
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={
        "model": "gpt-4",
        "api_key": "your-api-key"
    }
)

# Advanced configuration with multiple models
assistant = AssistantAgent(
    name="advanced_assistant",
    system_message="""You are an expert software developer.
    Always provide code examples and explain your reasoning.""",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": "your-primary-key",
                "max_tokens": 1000
            },
            {
                "model": "gpt-3.5-turbo",
                "api_key": "your-fallback-key"
            }
        ],
        "temperature": 0.7,
        "cache_seed": 42  # For reproducible responses
    }
)
```

### UserProxyAgent

The `UserProxyAgent` represents human users in conversations and can execute code safely in Docker containers.

```python
from ag2 import UserProxyAgent

# Basic user proxy
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",  # Always ask for human input
    code_execution_config=False  # Disable code execution
)

# Code-executing user proxy
code_executor = UserProxyAgent(
    name="code_executor",
    human_input_mode="NEVER",  # Automatic mode
    code_execution_config={
        "work_dir": "coding_workspace",
        "use_docker": True,
        "timeout": 60
    }
)

# Interactive user proxy
interactive_user = UserProxyAgent(
    name="interactive_user",
    human_input_mode="TERMINATE",  # Ask until user says TERMINATE
    max_consecutive_auto_reply=5  # Auto-reply up to 5 times
)
```

### ConversableAgent

The base class for all agents, providing the core conversation functionality. You can extend this to create custom agents.

```python
from ag2 import ConversableAgent

class CustomAgent(ConversableAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation_history = []

    def send(self, message, recipient, request_reply=True):
        # Custom send logic
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": time.time()
        })
        return super().send(message, recipient, request_reply)

    def receive(self, message, sender, request_reply=None):
        # Custom receive logic
        self.conversation_history.append({
            "role": "assistant",
            "content": message,
            "timestamp": time.time()
        })
        return super().receive(message, sender, request_reply)

custom_agent = CustomAgent(
    name="custom_agent",
    llm_config=llm_config
)
```

## Agent Configuration Options

### LLM Configuration

```python
# Single model configuration
llm_config_single = {
    "model": "gpt-4",
    "api_key": "your-key",
    "temperature": 0.7,
    "max_tokens": 1000
}

# Multiple models with fallback
llm_config_fallback = {
    "config_list": [
        {"model": "gpt-4", "api_key": "primary-key"},
        {"model": "gpt-3.5-turbo", "api_key": "fallback-key"}
    ]
}

# Advanced configuration
llm_config_advanced = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": "your-key",
            "temperature": 0.1,
            "max_tokens": 2000,
            "top_p": 0.9
        }
    ],
    "cache_seed": 42,  # Reproducible responses
    "filter_dict": {    # Model filtering
        "model": ["gpt-4", "gpt-3.5-turbo"]
    }
}
```

### System Messages

System messages define the agent's personality, capabilities, and behavior patterns.

```python
# Specialized agents with detailed system messages
researcher = AssistantAgent(
    name="researcher",
    system_message="""You are an expert researcher with deep knowledge in:
    - Academic literature review
    - Data analysis and interpretation
    - Scientific methodology

    When researching:
    1. Formulate clear research questions
    2. Identify credible sources
    3. Analyze information objectively
    4. Provide evidence-based conclusions
    5. Suggest follow-up research directions""",
    llm_config=llm_config
)

coder = AssistantAgent(
    name="coder",
    system_message="""You are an expert software developer specializing in:
    - Clean, maintainable code
    - Best practices and design patterns
    - Error handling and testing
    - Performance optimization

    Always provide:
    - Well-commented code
    - Error handling
    - Unit tests when appropriate
    - Documentation""",
    llm_config=llm_config
)

reviewer = AssistantAgent(
    name="reviewer",
    system_message="""You are a senior technical reviewer who:
    - Identifies potential issues and improvements
    - Ensures code quality and best practices
    - Verifies requirements are met
    - Suggests optimizations and alternatives

    Be constructive, specific, and actionable in your feedback.""",
    llm_config=llm_config
)
```

## Human Input Modes

### ALWAYS Mode
Always requests human input before taking actions.

```python
agent_always = UserProxyAgent(
    name="human_supervised",
    human_input_mode="ALWAYS",
    code_execution_config=False
)
```

### NEVER Mode
Never asks for human input - fully autonomous.

```python
agent_autonomous = UserProxyAgent(
    name="autonomous_agent",
    human_input_mode="NEVER",
    code_execution_config={
        "use_docker": True,
        "timeout": 30
    }
)
```

### TERMINATE Mode
Continues automatically until the user says "TERMINATE".

```python
agent_terminate = UserProxyAgent(
    name="semi_autonomous",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10
)
```

## Code Execution Configuration

### Docker-based Execution (Recommended)

```python
safe_executor = UserProxyAgent(
    name="safe_executor",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": True,          # Sandbox execution
        "timeout": 60,               # 60 second timeout
        "last_n_messages": 3         # Only use last 3 messages for context
    }
)
```

### Local Execution (Advanced Users)

```python
local_executor = UserProxyAgent(
    name="local_executor",
    code_execution_config={
        "work_dir": "local_workspace",
        "use_docker": False,         # Direct local execution
        "timeout": 30
    }
)
```

## Advanced Agent Patterns

### Multi-Model Agents

```python
class MultiModelAgent(AssistantAgent):
    def __init__(self, models_config, **kwargs):
        super().__init__(**kwargs)
        self.models = models_config

    def select_model(self, task_complexity):
        """Select appropriate model based on task complexity"""
        if task_complexity == "high":
            return self.models["gpt-4"]
        elif task_complexity == "medium":
            return self.models["gpt-3.5-turbo"]
        else:
            return self.models["gpt-3.5-turbo-instruct"]

multi_model_agent = MultiModelAgent(
    name="adaptive_agent",
    models_config={
        "gpt-4": {"model": "gpt-4", "temperature": 0.1},
        "gpt-3.5-turbo": {"model": "gpt-3.5-turbo", "temperature": 0.3},
        "gpt-3.5-turbo-instruct": {"model": "gpt-3.5-turbo-instruct", "temperature": 0.7}
    },
    llm_config={"config_list": [models_config["gpt-4"]]}
)
```

### Context-Aware Agents

```python
class ContextAwareAgent(AssistantAgent):
    def __init__(self, context_window=10, **kwargs):
        super().__init__(**kwargs)
        self.context_window = context_window
        self.conversation_context = []

    def update_context(self, message, role="user"):
        self.conversation_context.append({"role": role, "content": message})
        if len(self.conversation_context) > self.context_window:
            self.conversation_context.pop(0)

    def get_context_summary(self):
        return "\n".join([
            f"{msg['role']}: {msg['content'][:100]}..."
            for msg in self.conversation_context[-5:]
        ])

context_agent = ContextAwareAgent(
    name="context_aware_agent",
    context_window=15,
    llm_config=llm_config
)
```

## Best Practices

### Agent Naming
- Use descriptive, unique names
- Avoid special characters
- Keep names concise but meaningful

### System Message Design
- Be specific about capabilities and limitations
- Include behavioral guidelines
- Define output format preferences
- Specify error handling approaches

### Configuration Management
- Store API keys securely (environment variables)
- Use consistent LLM configurations
- Document configuration choices
- Test configurations thoroughly

### Resource Management
- Set appropriate timeouts
- Monitor token usage
- Implement rate limiting
- Clean up temporary files

## Example: Complete Agent Setup

```python
from ag2 import AssistantAgent, UserProxyAgent
import os

# Configuration
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0.7
        }
    ]
}

# Create specialized agents
task_planner = AssistantAgent(
    name="task_planner",
    system_message="""You are a task planning expert. Break down complex requests into manageable steps.
    Always consider dependencies, risks, and alternative approaches.""",
    llm_config=llm_config
)

code_executor = UserProxyAgent(
    name="code_executor",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": True,
        "timeout": 120
    }
)

quality_reviewer = AssistantAgent(
    name="quality_reviewer",
    system_message="""You are a code quality expert. Review code for:
    - Correctness and efficiency
    - Best practices and patterns
    - Security considerations
    - Maintainability""",
    llm_config=llm_config
)

# Agent team ready for collaborative tasks
agents = {
    "planner": task_planner,
    "executor": code_executor,
    "reviewer": quality_reviewer
}
```

## Summary

In this chapter, we've explored:

- **Core Agent Types**: AssistantAgent, UserProxyAgent, and ConversableAgent
- **Configuration Options**: LLM settings, system messages, and execution parameters
- **Human Input Modes**: ALWAYS, NEVER, and TERMINATE modes
- **Code Execution**: Safe Docker-based execution vs local execution
- **Advanced Patterns**: Multi-model and context-aware agents
- **Best Practices**: Naming, configuration, and resource management

Next, we'll learn about **conversation patterns** - how these agents interact and collaborate.

---

**Ready for the next chapter?** [Chapter 3: Conversation Patterns](03-conversation-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `name`, `llm_config` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Agent Types & Configuration` as an operating subsystem inside **AG2 Tutorial: Next-Generation Multi-Agent Framework**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `AssistantAgent`, `UserProxyAgent` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Agent Types & Configuration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `llm_config`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ag2ai/ag2)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [github.com/microsoft/autogen](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `github.com/microsoft/autogen` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with AG2](01-getting-started.md)
- [Next Chapter: Chapter 3: Conversation Patterns](03-conversation-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
