---
layout: default
title: "Phidata Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Phidata Tutorial
---

# Chapter 1: Getting Started with Phidata Agents

> Create your first autonomous AI agent with Phidata - from installation to intelligent conversation.

## Installation and Setup

### Basic Installation

```bash
# Install Phidata
pip install phidata

# For development with latest features
pip install git+https://github.com/phidatahq/phidata.git

# Optional: Install with specific providers
pip install phidata[openai]      # OpenAI integration
pip install phidata[anthropic]   # Anthropic Claude
pip install phidata[groq]        # Groq integration
pip install phidata[ollama]      # Local Ollama models
```

### Environment Setup

```bash
# Create environment variables
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# Install python-dotenv for .env support
pip install python-dotenv
```

## Your First Agent

### Basic Agent Creation

```python
from phidata.agent import Agent

# Create a simple agent
agent = Agent(
    name="BasicAssistant",
    instructions="You are a helpful AI assistant that provides clear, accurate responses.",
    model="gpt-4",
    markdown=True  # Enable markdown formatting
)

# Run the agent
response = agent.run("What is the capital of France?")
print(response)

# Output:
# The capital of France is Paris.
```

### Agent with Custom Instructions

```python
# Create a specialized agent
coding_agent = Agent(
    name="CodeAssistant",
    instructions="""
    You are an expert software developer with deep knowledge of multiple programming languages.
    When providing code solutions:
    1. Always include clear comments explaining the code
    2. Consider edge cases and error handling
    3. Provide examples of usage
    4. Suggest best practices and potential improvements
    """,
    model="gpt-4-turbo",
    add_datetime_to_instructions=True  # Add current date/time context
)

# Ask for coding help
code_help = coding_agent.run("""
Create a Python function that calculates the fibonacci sequence up to n terms.
Include proper error handling and type hints.
""")

print(code_help)
```

### Streaming Responses

```python
import asyncio

# Create agent with streaming
streaming_agent = Agent(
    name="StreamingAssistant",
    instructions="You are a helpful assistant that provides detailed explanations.",
    model="gpt-4",
    stream=True  # Enable streaming responses
)

async def stream_response():
    """Handle streaming response asynchronously."""

    response_stream = await streaming_agent.arun("Explain how neural networks work")

    async for chunk in response_stream:
        print(chunk, end="", flush=True)

    print("\n--- Streaming complete ---")

# Run streaming example
asyncio.run(stream_response())
```

## Agent Configuration Options

### Model Selection and Configuration

```python
from phidata.model.openai import OpenAIChat
from phidata.model.anthropic import Claude
from phidata.model.groq import Groq

# OpenAI GPT-4 agent
gpt4_agent = Agent(
    name="GPT4Agent",
    model=OpenAIChat(
        id="gpt-4",
        api_key="your-openai-key",
        max_tokens=4096,
        temperature=0.7
    ),
    instructions="You are an expert at providing detailed technical explanations."
)

# Anthropic Claude agent
claude_agent = Agent(
    name="ClaudeAgent",
    model=Claude(
        id="claude-3-sonnet-20240229",
        api_key="your-anthropic-key",
        max_tokens=4096,
        temperature=0.7
    ),
    instructions="You are an expert at providing detailed technical explanations."
)

# Groq fast inference agent
groq_agent = Agent(
    name="FastAgent",
    model=Groq(
        id="mixtral-8x7b-32768",
        api_key="your-groq-key"
    ),
    instructions="You are a fast and efficient assistant."
)

# Local Ollama agent
ollama_agent = Agent(
    name="LocalAgent",
    model="llama2:7b",  # Uses Ollama
    instructions="You are a local AI assistant."
)
```

### Agent Personality and Behavior

```python
# Professional consultant agent
consultant_agent = Agent(
    name="BusinessConsultant",
    instructions="""
    You are an experienced business consultant with 20 years of experience.
    Always structure your responses professionally with:
    - Executive summary
    - Key recommendations
    - Implementation steps
    - Potential risks and mitigation strategies
    - Success metrics

    Be data-driven and provide actionable insights.
    """,
    model="gpt-4",
    add_datetime_to_instructions=True
)

# Creative writing agent
creative_agent = Agent(
    name="CreativeWriter",
    instructions="""
    You are a creative writing assistant specializing in fiction and storytelling.
    Focus on:
    - Engaging narratives
    - Vivid descriptions
    - Character development
    - Plot structure
    - Emotional depth

    Encourage creativity and provide constructive feedback.
    """,
    model="claude-3-haiku-20240307",
    markdown=True
)

# Technical documentation agent
docs_agent = Agent(
    name="TechnicalWriter",
    instructions="""
    You are a technical documentation specialist.
    Create clear, comprehensive documentation that includes:
    - Overview and purpose
    - Prerequisites and dependencies
    - Step-by-step instructions
    - Code examples with explanations
    - Troubleshooting section
    - Best practices and tips

    Use clear language and proper formatting.
    """,
    model="gpt-4-turbo",
    markdown=True
)
```

## Agent Communication Patterns

### Single Message Interaction

```python
# Simple single-turn conversation
agent = Agent(
    name="SimpleAgent",
    instructions="Answer questions concisely and accurately."
)

# Single message
response = agent.run("What is 2 + 2?")
print(f"Answer: {response}")

# With context
context_response = agent.run("Explain quantum computing in simple terms")
print(f"Explanation: {context_response}")
```

### Multi-Turn Conversations

```python
# Agent with conversation memory
conversational_agent = Agent(
    name="ChatAgent",
    instructions="You are a friendly conversational AI. Remember previous messages and maintain context.",
    model="gpt-4",
    # Phidata automatically maintains conversation context
)

# Multi-turn conversation
messages = [
    "Hello! My name is Alice.",
    "I'm interested in learning about Python programming.",
    "Can you show me a simple example?",
    "How do I handle errors in Python?",
]

for message in messages:
    response = conversational_agent.run(message)
    print(f"User: {message}")
    print(f"Agent: {response}")
    print("-" * 50)
```

### Structured Output Agents

```python
from pydantic import BaseModel, Field
from typing import List, Optional

# Define structured output models
class TaskBreakdown(BaseModel):
    task_name: str = Field(..., description="Name of the main task")
    estimated_time: str = Field(..., description="Estimated time to complete")
    difficulty: str = Field(..., enum=["easy", "medium", "hard"], description="Task difficulty")
    steps: List[str] = Field(..., description="Step-by-step breakdown")
    prerequisites: Optional[List[str]] = Field(None, description="Required prerequisites")

class CodeReview(BaseModel):
    overall_score: int = Field(..., ge=1, le=10, description="Overall code quality score")
    strengths: List[str] = Field(..., description="What the code does well")
    improvements: List[str] = Field(..., description="Suggested improvements")
    critical_issues: Optional[List[str]] = Field(None, description="Critical issues that must be fixed")

# Structured output agents
task_agent = Agent(
    name="TaskBreaker",
    instructions="Break down complex tasks into manageable steps.",
    model="gpt-4",
    response_model=TaskBreakdown
)

review_agent = Agent(
    name="CodeReviewer",
    instructions="Review code for quality, maintainability, and best practices.",
    model="gpt-4",
    response_model=CodeReview
)

# Generate structured outputs
task_breakdown = task_agent.run("Learn how to build a web application from scratch")
print("Task Breakdown:")
print(f"Task: {task_breakdown.task_name}")
print(f"Time: {task_breakdown.estimated_time}")
print(f"Steps: {len(task_breakdown.steps)}")

code_review = review_agent.run("""
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
""")

print("
Code Review:")
print(f"Score: {code_review.overall_score}/10")
print(f"Strengths: {len(code_review.strengths)}")
print(f"Improvements: {len(code_review.improvements)}")
```

## Error Handling and Debugging

### Agent Error Handling

```python
def safe_agent_run(agent: Agent, prompt: str, max_retries: int = 3):
    """Run agent with error handling and retries."""

    for attempt in range(max_retries):
        try:
            response = agent.run(prompt)
            return {"success": True, "response": response, "attempts": attempt + 1}

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < max_retries - 1:
                # Wait before retry (exponential backoff)
                import time
                time.sleep(2 ** attempt)
            else:
                return {
                    "success": False,
                    "error": str(e),
                    "attempts": attempt + 1
                }

# Usage with error handling
agent = Agent(name="TestAgent", model="gpt-4")

result = safe_agent_run(agent, "This is a test prompt")

if result["success"]:
    print(f"Success after {result['attempts']} attempts")
    print(f"Response: {result['response']}")
else:
    print(f"Failed after {result['attempts']} attempts")
    print(f"Error: {result['error']}")
```

### Agent Debugging

```python
from phidata.utils.log import logger

# Enable detailed logging
logger.setLevel("DEBUG")

# Create agent with debug information
debug_agent = Agent(
    name="DebugAgent",
    instructions="You are a debugging assistant.",
    model="gpt-4",
    debug_mode=True  # Enable debug mode
)

# Run with detailed logging
response = debug_agent.run("Debug this Python code: print('Hello')")
print(f"Response: {response}")

# Access agent metadata
print(f"Agent name: {debug_agent.name}")
print(f"Model: {debug_agent.model}")
print(f"Instructions length: {len(debug_agent.instructions)}")

# Check agent status
print(f"Agent active: {debug_agent.is_active}")
print(f"Agent runs: {debug_agent.run_count}")
```

## Agent Storage and Persistence

### Basic Agent Storage

```python
import json
import os
from datetime import datetime

class AgentStorage:
    """Simple agent storage and retrieval."""

    def __init__(self, storage_dir: str = "./agent_storage"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_agent(self, agent: Agent, filename: str = None):
        """Save agent configuration."""

        if filename is None:
            filename = f"{agent.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        config = {
            "name": agent.name,
            "instructions": agent.instructions,
            "model": str(agent.model) if hasattr(agent.model, '__str__') else agent.model,
            "created_at": datetime.now().isoformat(),
            "run_count": getattr(agent, 'run_count', 0)
        }

        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Agent saved to {filepath}")
        return filepath

    def load_agent_config(self, filename: str) -> dict:
        """Load agent configuration."""

        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, 'r') as f:
            config = json.load(f)

        return config

    def recreate_agent(self, config: dict) -> Agent:
        """Recreate agent from configuration."""

        return Agent(
            name=config["name"],
            instructions=config["instructions"],
            model=config.get("model", "gpt-4")
        )

# Usage
storage = AgentStorage()

# Create and save agent
my_agent = Agent(
    name="MySavedAgent",
    instructions="You are a helpful assistant.",
    model="gpt-4"
)

# Run agent a few times
my_agent.run("Hello")
my_agent.run("How are you?")

# Save agent
saved_path = storage.save_agent(my_agent)

# Load and recreate agent
config = storage.load_agent_config(os.path.basename(saved_path))
recreated_agent = storage.recreate_agent(config)

print(f"Recreated agent: {recreated_agent.name}")
```

## Next Steps

Now that you have created your first Phidata agents, let's explore:

- **[Chapter 2: Agent Architecture](02-agent-architecture.md)** - Understanding the internal components of Phidata agents
- **[Chapter 3: Tools & Functions](03-tools-functions.md)** - Adding capabilities through tools and functions

## Quick Start Checklist

- [ ] Install Phidata and dependencies
- [ ] Set up API keys for your preferred LLM provider
- [ ] Create your first basic agent
- [ ] Experiment with different models and instructions
- [ ] Try structured output with Pydantic models
- [ ] Implement error handling for robustness
- [ ] Save and load agent configurations

You're now ready to explore the full power of autonomous AI agents! 🚀