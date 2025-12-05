---
layout: default
title: "Chapter 1: Getting Started"
parent: "OpenAI Swarm Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with OpenAI Swarm

Welcome to Swarm! In this chapter, you'll learn the fundamentals of OpenAI's educational multi-agent framework and create your first collaborative agents.

## What is Swarm?

Swarm is an experimental framework from OpenAI that makes it easy to build and orchestrate multi-agent systems. Unlike complex orchestration frameworks, Swarm focuses on being:

- **Lightweight** - Minimal abstraction over the Chat Completions API
- **Ergonomic** - Natural patterns that are easy to understand
- **Educational** - Designed to teach multi-agent concepts

> ⚠️ **Note**: Swarm is an experimental/educational framework. For production use cases, consider more robust solutions or build on top of Swarm's patterns.

## Installation

```bash
# Install Swarm directly from GitHub
pip install git+https://github.com/openai/swarm.git

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

## Core Concepts

### Agents

An Agent encapsulates a set of instructions and functions (tools). Agents are stateless and simply define behavior.

```python
from swarm import Agent

agent = Agent(
    name="Helper",
    instructions="You are a helpful assistant.",
)
```

### The Swarm Client

The `Swarm` client handles running agents and managing conversations:

```python
from swarm import Swarm, Agent

client = Swarm()

agent = Agent(
    name="Greeter",
    instructions="You greet users warmly and ask how you can help."
)

response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.messages[-1]["content"])
# "Hello! Welcome! How can I assist you today?"
```

## Your First Agent

Let's create a simple agent that can answer questions:

```python
from swarm import Swarm, Agent

# Initialize the client
client = Swarm()

# Create an agent with instructions
assistant = Agent(
    name="Assistant",
    instructions="""You are a knowledgeable assistant. 
    Answer questions clearly and concisely.
    If you don't know something, say so honestly."""
)

# Have a conversation
messages = [{"role": "user", "content": "What is the capital of France?"}]

response = client.run(agent=assistant, messages=messages)

print(f"Agent: {response.messages[-1]['content']}")
# Agent: The capital of France is Paris.
```

## Adding Functions to Agents

Agents can use functions (tools) to perform actions:

```python
from swarm import Swarm, Agent

client = Swarm()

# Define functions the agent can use
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    # In a real app, call a weather API
    weather_data = {
        "New York": "72°F, Sunny",
        "London": "58°F, Cloudy",
        "Tokyo": "68°F, Partly Cloudy"
    }
    return weather_data.get(city, f"Weather data not available for {city}")

def get_time(timezone: str) -> str:
    """Get the current time in a timezone."""
    from datetime import datetime
    import pytz
    
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz).strftime("%I:%M %p")
    except:
        return f"Unknown timezone: {timezone}"

# Create agent with functions
weather_agent = Agent(
    name="Weather Assistant",
    instructions="""You help users with weather and time information.
    Use the available functions to get accurate data.""",
    functions=[get_weather, get_time]
)

# Test the agent
response = client.run(
    agent=weather_agent,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)

print(response.messages[-1]["content"])
# The weather in Tokyo is currently 68°F and Partly Cloudy.
```

## Understanding Response Objects

The `client.run()` method returns a `Response` object:

```python
response = client.run(agent=agent, messages=messages)

# Access response attributes
print(response.messages)      # Full message history
print(response.agent)         # The final agent (may change during handoffs)
print(response.context_variables)  # Shared context between agents
```

## Multi-Turn Conversations

Maintain conversation context across turns:

```python
from swarm import Swarm, Agent

client = Swarm()

agent = Agent(
    name="Conversationalist",
    instructions="You engage in friendly conversation. Remember context from earlier in the conversation."
)

# First turn
messages = [{"role": "user", "content": "My name is Alice and I love hiking."}]
response = client.run(agent=agent, messages=messages)
print(f"Agent: {response.messages[-1]['content']}")

# Second turn - continue the conversation
messages = response.messages + [{"role": "user", "content": "What activities might I enjoy?"}]
response = client.run(agent=agent, messages=messages)
print(f"Agent: {response.messages[-1]['content']}")
# The agent remembers Alice likes hiking and suggests related activities
```

## Agent Instructions Best Practices

### Be Specific

```python
# ❌ Vague instructions
agent = Agent(
    name="Helper",
    instructions="Help users."
)

# ✅ Specific instructions
agent = Agent(
    name="Technical Support",
    instructions="""You are a technical support agent for a software company.
    
    Your responsibilities:
    1. Diagnose technical issues based on user descriptions
    2. Provide step-by-step troubleshooting instructions
    3. Escalate to a human if the issue is complex
    
    Always:
    - Ask clarifying questions when needed
    - Be patient and professional
    - Provide numbered steps for instructions
    """
)
```

### Define Boundaries

```python
agent = Agent(
    name="Sales Agent",
    instructions="""You are a sales agent for Acme Software.
    
    You CAN:
    - Explain product features and benefits
    - Provide pricing information
    - Schedule demos
    
    You CANNOT:
    - Negotiate custom pricing (transfer to manager)
    - Provide technical support (transfer to support)
    - Make promises about unreleased features
    """
)
```

## Running Multiple Agents

Preview of what's coming - agents can work together:

```python
from swarm import Swarm, Agent

client = Swarm()

# Define a transfer function
def transfer_to_spanish_agent():
    """Transfer conversation to Spanish-speaking agent."""
    return spanish_agent

# English agent
english_agent = Agent(
    name="English Agent",
    instructions="You speak English. If a user writes in Spanish, transfer to the Spanish agent.",
    functions=[transfer_to_spanish_agent]
)

# Spanish agent
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="Hablas español. Ayuda a los usuarios en español."
)

# Test - user writes in Spanish
response = client.run(
    agent=english_agent,
    messages=[{"role": "user", "content": "Hola, necesito ayuda"}]
)

print(f"Final agent: {response.agent.name}")
# Final agent: Spanish Agent
```

## What We've Accomplished

🎉 In this chapter, you've learned:

1. ✅ How to install and set up Swarm
2. ✅ Core concepts: Agents, Swarm client, and responses
3. ✅ Creating agents with custom instructions
4. ✅ Adding functions (tools) to agents
5. ✅ Managing multi-turn conversations
6. ✅ Best practices for agent instructions
7. ✅ Preview of agent handoffs

## Next Steps

In [Chapter 2: Agent Design](02-agent-design.md), we'll dive deeper into:

- Crafting effective agent personas
- Designing agent architectures
- Managing agent state and context
- Handling edge cases and errors

---

**Practice Exercises:**

1. Create an agent that can perform basic math calculations using functions
2. Build a multi-turn conversation that tracks user preferences
3. Write agent instructions for a customer service bot
4. Add error handling to your function implementations

*Ready to design professional agents? Continue to [Chapter 2](02-agent-design.md)!*
