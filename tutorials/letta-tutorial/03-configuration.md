---
layout: default
title: "Letta Tutorial - Chapter 3: Agent Configuration"
nav_order: 3
has_children: false
parent: Letta Tutorial
---

# Chapter 3: Agent Configuration

> Customize agent personalities, system prompts, models, and behavior settings.

## Overview

Letta agents are highly configurable. This chapter covers personas, system prompts, model selection, and fine-tuning agent behavior for different use cases.

## Agent Personas

Personas define the agent's character and behavior:

```bash
# Create with a detailed persona
letta create --name mentor --persona "You are Alex, an experienced software engineering mentor. You have 15 years of experience in full-stack development, DevOps, and team leadership. You speak professionally but accessibly, always explaining concepts clearly. You ask thoughtful questions to understand problems deeply before offering solutions."

# Update existing agent persona
letta update-agent --name sam --persona "You are Sam, a cheerful and helpful AI assistant who remembers everything about your conversations. You're enthusiastic about learning new things and helping users solve problems."
```

## System Prompts

System prompts provide detailed instructions:

```python
from letta import create_client

client = create_client()

# Create agent with custom system prompt
agent_config = {
    "name": "code-reviewer",
    "persona": "You are a senior code reviewer with expertise in Python, JavaScript, and Go.",
    "system": """You are a meticulous code reviewer. Follow these guidelines:

1. Check for security vulnerabilities
2. Verify code follows best practices
3. Look for performance issues
4. Ensure proper error handling
5. Suggest improvements with explanations

Always provide specific line references and explain the reasoning behind your suggestions.""",
    "model": "gpt-4o",
}

agent = client.create_agent(**agent_config)
```

## Model Configuration

Choose the right model for your use case:

```bash
# Fast and cost-effective
letta create --name fast-assistant --model gpt-4o-mini

# High-quality reasoning
letta create --name expert-assistant --model gpt-4o

# Creative tasks
letta create --name creative-writer --model gpt-4o
```

### Model Settings

Configure model parameters:

```python
agent_config = {
    "name": "creative-writer",
    "model": "gpt-4o",
    "model_settings": {
        "temperature": 0.9,  # Higher for creativity
        "max_tokens": 2000,
        "top_p": 0.9,
    }
}
```

## Memory Configuration

Customize memory behavior:

```python
# Configure memory settings
agent = client.create_agent(
    name="researcher",
    memory_config={
        "recall_memory_limit": 50,  # Messages to keep in recall
        "archival_memory_limit": 10000,  # Max archival entries
        "working_memory_limit": 10,  # Core memory blocks
    }
)
```

## Tool Integration Setup

Enable tools for enhanced capabilities:

```python
agent_config = {
    "name": "web-researcher",
    "tools": ["web_search", "web_scrape", "save_file"],
    "system": "You are a research assistant who can search the web and save findings."
}
```

## Creating Specialized Agents

### Code Assistant

```bash
letta create --name code-assistant \
  --persona "You are an expert programmer who writes clean, efficient, well-documented code." \
  --model gpt-4o \
  --system "Focus on:
- Writing readable, maintainable code
- Following language-specific best practices
- Adding helpful comments
- Considering edge cases
- Optimizing for performance when relevant"
```

### Meeting Facilitator

```python
meeting_agent = client.create_agent(
    name="meeting-facilitator",
    persona="You are a professional meeting facilitator who keeps discussions on track and ensures all voices are heard.",
    system="""Meeting facilitation guidelines:
1. Start with agenda confirmation
2. Time management - keep to schedule
3. Ensure balanced participation
4. Summarize key decisions
5. End with action items and owners""",
    model="gpt-4o-mini"
)
```

### Learning Coach

```bash
letta create --name learning-coach \
  --persona "You are a patient, encouraging learning coach who adapts to each student's pace and style." \
  --system "Adapt your teaching to the learner:
- Assess current knowledge level
- Break complex topics into digestible chunks
- Use analogies and examples
- Provide practice exercises
- Give constructive feedback"
```

## Configuration Templates

Save and reuse configurations:

```python
# Define templates
TEMPLATES = {
    "code-reviewer": {
        "persona": "Expert code reviewer with 10+ years experience",
        "model": "gpt-4o",
        "system": "Focus on security, performance, maintainability...",
        "tools": ["run_tests", "check_security"]
    },
    "customer-support": {
        "persona": "Friendly, empathetic customer support specialist",
        "model": "gpt-4o-mini",
        "system": "Be patient, ask clarifying questions, escalate when needed...",
        "tools": ["search_kb", "create_ticket"]
    }
}

# Create from template
def create_from_template(name, template_name):
    config = TEMPLATES[template_name].copy()
    config["name"] = name
    return client.create_agent(**config)
```

## Updating Agent Configuration

Modify agents after creation:

```bash
# Update model
letta update-agent --name sam --model gpt-4o

# Change persona
letta update-agent --name sam --persona "New persona description"

# Update system prompt
letta update-agent --name sam --system "New system instructions"
```

## Environment-Specific Configs

Different settings for development vs production:

```python
import os

def create_agent_for_env(name, base_config):
    config = base_config.copy()
    config["name"] = name

    if os.getenv("ENV") == "production":
        config["model"] = "gpt-4o"  # Higher quality
        config["model_settings"] = {"temperature": 0.1}  # More consistent
    else:
        config["model"] = "gpt-4o-mini"  # Faster, cheaper
        config["model_settings"] = {"temperature": 0.7}  # More creative

    return client.create_agent(**config)
```

## Configuration Best Practices

### Persona Guidelines

- **Be Specific**: Include role, experience level, communication style
- **Define Boundaries**: What the agent should/shouldn't do
- **Add Context**: Industry knowledge, specializations

### System Prompt Tips

- **Clear Instructions**: Use numbered lists for complex procedures
- **Examples**: Include input/output examples
- **Constraints**: Define limits and boundaries
- **Error Handling**: How to respond to unclear requests

### Model Selection

- **gpt-4o**: Complex reasoning, high-quality output
- **gpt-4o-mini**: Fast, cost-effective for simple tasks
- **Local Models**: Privacy, cost control (via compatibility layer)

## Testing Configurations

Validate agent behavior:

```python
def test_agent_config(agent_name, test_cases):
    """Test agent responses to ensure configuration works as expected"""
    for test_input, expected_behavior in test_cases:
        response = client.send_message(agent_name, test_input)
        # Validate response matches expected behavior
        assert expected_behavior in response.content

# Test cases for a code reviewer
test_cases = [
    ("Review this function", "security check"),
    ("Optimize this code", "performance suggestion"),
    ("What's wrong here?", "specific feedback")
]

test_agent_config("code-reviewer", test_cases)
```

## Configuration Versioning

Track configuration changes:

```python
# Save configurations
def save_config(agent, version="v1"):
    config = {
        "persona": agent.persona,
        "system": agent.system,
        "model": agent.model,
        "tools": agent.tools,
        "version": version,
        "created": datetime.now().isoformat()
    }

    with open(f"configs/{agent.name}_{version}.json", "w") as f:
        json.dump(config, f, indent=2)
```

This allows you to experiment with different configurations and roll back if needed.

Next: Add custom tools and functions to extend agent capabilities. 