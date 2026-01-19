---
layout: default
title: "Chapter 1: Getting Started with AG2"
parent: "AG2 Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with AG2

Set up AG2, understand its architecture, create your first assistant+user agents, and run conversations with different configurations.

## Objectives

- Install AG2 and configure dependencies
- Understand AG2's core architecture
- Configure API keys and LLM providers
- Create and configure basic agents
- Run single and multi-turn conversations
- Handle errors and debug common issues

## Prerequisites

- Python 3.10+ (3.11 recommended)
- OpenAI-compatible API key (OpenAI, Azure, or local models)
- Basic understanding of async Python
- Docker (optional, for code execution)

## Understanding AG2 Architecture

Before diving into code, let's understand how AG2 works under the hood.

```
┌─────────────────────────────────────────────────────────────┐
│                     AG2 Architecture                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     Messages      ┌──────────────┐       │
│  │  Assistant   │◄────────────────►│  UserProxy    │       │
│  │    Agent     │                   │    Agent      │       │
│  └──────┬───────┘                   └──────┬───────┘       │
│         │                                  │                │
│         ▼                                  ▼                │
│  ┌──────────────┐                   ┌──────────────┐       │
│  │  LLM Config  │                   │Code Executor │       │
│  │  (GPT-4,etc) │                   │ (Docker/Local)│       │
│  └──────────────┘                   └──────────────┘       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Conversation Manager                    │   │
│  │  - Message history    - Termination conditions       │   │
│  │  - Turn management    - Human input handling         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent** | An autonomous entity that can send/receive messages |
| **Conversation** | Message exchange between agents |
| **LLM Config** | Configuration for the language model backend |
| **Code Executor** | Environment for executing generated code |
| **Termination** | Conditions that end a conversation |

## Installation

### Basic Installation

```bash
# Install core AG2 package
pip install ag2

# Verify installation
python -c "import ag2; print(ag2.__version__)"
```

### Installation with Extras

```bash
# Full installation with all features
pip install ag2[all]

# Specific feature sets
pip install ag2[openai]          # OpenAI integration
pip install ag2[anthropic]       # Anthropic/Claude integration
pip install ag2[local]           # Local model support
pip install ag2[retrievechat]    # RAG capabilities
pip install ag2[teachable]       # Teachable agents
pip install ag2[graphs]          # Graph-based workflows
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/ag2ai/ag2.git
cd ag2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,test]"
```

### Docker Setup (Recommended for Code Execution)

```bash
# Pull the official AG2 Docker image
docker pull ag2ai/ag2

# Or build locally
docker build -t ag2-executor -f docker/Dockerfile.executor .
```

## Environment Configuration

### Setting Up API Keys

Create a `.env` file in your project root:

```bash
# .env file
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# For Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01

# For local models (Ollama, vLLM, etc.)
LOCAL_MODEL_BASE_URL=http://localhost:11434/v1
```

### Loading Environment Variables

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify keys are loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

### Configuration File (OAI_CONFIG_LIST)

AG2 supports a JSON configuration file for managing multiple models:

```json
// OAI_CONFIG_LIST.json
[
    {
        "model": "gpt-4-turbo",
        "api_key": "sk-...",
        "api_type": "openai"
    },
    {
        "model": "gpt-3.5-turbo",
        "api_key": "sk-...",
        "api_type": "openai"
    },
    {
        "model": "claude-3-opus",
        "api_key": "sk-ant-...",
        "api_type": "anthropic",
        "api_base": "https://api.anthropic.com"
    },
    {
        "model": "llama3:70b",
        "api_base": "http://localhost:11434/v1",
        "api_type": "ollama"
    }
]
```

Load the configuration:

```python
from ag2 import config_list_from_json

# Load all configurations
config_list = config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={
        "model": ["gpt-4-turbo", "gpt-4"]
    }
)

# Use in LLM config
llm_config = {
    "config_list": config_list,
    "cache_seed": 42,  # For reproducibility
    "temperature": 0.7
}
```

## Creating Your First Agents

### Basic Two-Agent Conversation

```python
from ag2 import AssistantAgent, UserProxyAgent

# Create the assistant agent (AI-powered)
assistant = AssistantAgent(
    name="Assistant",
    system_message="""You are a helpful AI assistant.
    Provide clear, accurate, and concise responses.
    When asked to write code, provide well-commented examples.""",
    llm_config={
        "model": "gpt-4-turbo",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.7
    }
)

# Create the user proxy agent (represents the user)
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # Run autonomously
    max_consecutive_auto_reply=5,  # Limit conversation turns
    code_execution_config=False  # Disable code execution for now
)

# Start a conversation
result = user_proxy.initiate_chat(
    assistant,
    message="Explain the difference between lists and tuples in Python.",
    max_turns=3
)

# Access the conversation history
for message in result.chat_history:
    print(f"{message['role']}: {message['content'][:100]}...")
```

### Understanding Agent Parameters

```python
# AssistantAgent Configuration
assistant = AssistantAgent(
    name="CodeHelper",                    # Unique identifier
    system_message="You are an expert Python developer.",  # Role definition
    llm_config={
        "model": "gpt-4-turbo",
        "api_key": api_key,
        "temperature": 0.3,               # Lower = more deterministic
        "max_tokens": 2000,               # Response length limit
        "top_p": 0.95,                    # Nucleus sampling
        "frequency_penalty": 0.0,         # Reduce repetition
        "presence_penalty": 0.0           # Encourage new topics
    },
    max_consecutive_auto_reply=10,        # Auto-reply limit
    human_input_mode="NEVER",             # NEVER, TERMINATE, or ALWAYS
    description="Expert Python assistant for code help"  # For group chat routing
)

# UserProxyAgent Configuration
user_proxy = UserProxyAgent(
    name="Developer",
    human_input_mode="TERMINATE",         # Ask human when terminating
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "workspace",          # Working directory for code
        "use_docker": True,               # Isolate execution
        "timeout": 60,                    # Execution timeout in seconds
        "last_n_messages": 3              # Messages to consider for code
    },
    default_auto_reply="Please continue. If the task is complete, say TERMINATE.",
    function_map={}                       # Custom function mappings
)
```

### Human Input Modes

```python
# NEVER - Fully autonomous, no human input
user_proxy_auto = UserProxyAgent(
    name="AutoUser",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10
)

# TERMINATE - Human input only when conversation ends
user_proxy_terminate = UserProxyAgent(
    name="TermUser",
    human_input_mode="TERMINATE"
)

# ALWAYS - Human input after every response
user_proxy_always = UserProxyAgent(
    name="HumanUser",
    human_input_mode="ALWAYS"
)
```

## Running Conversations

### Single-Turn Conversation

```python
# Quick one-shot interaction
result = user_proxy.initiate_chat(
    assistant,
    message="What is the capital of France?",
    max_turns=1
)

print(result.chat_history[-1]["content"])
```

### Multi-Turn Conversation

```python
# Extended conversation with multiple exchanges
result = user_proxy.initiate_chat(
    assistant,
    message="I need help building a web scraper. Let's start with the requirements.",
    max_turns=10,
    summary_method="reflection_with_llm"  # Auto-summarize at end
)

# Get the summary
print(f"Summary: {result.summary}")
```

### Conversation with Code Execution

```python
# Enable code execution in Docker
user_proxy = UserProxyAgent(
    name="Developer",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding_workspace",
        "use_docker": True,
        "timeout": 120,
        "last_n_messages": "auto"
    }
)

# Start a coding task
result = user_proxy.initiate_chat(
    assistant,
    message="""Write a Python script that:
    1. Fetches the current Bitcoin price from a public API
    2. Saves it to a CSV file with timestamp
    3. Shows the last 5 entries

    Please execute and show the results."""
)
```

### Custom Termination Conditions

```python
def custom_termination(message):
    """Custom logic to determine when to end conversation."""
    content = message.get("content", "")

    # End on explicit termination
    if "TERMINATE" in content:
        return True

    # End on task completion signals
    completion_phrases = [
        "task is complete",
        "successfully finished",
        "here is the final result"
    ]
    return any(phrase in content.lower() for phrase in completion_phrases)

user_proxy = UserProxyAgent(
    name="User",
    is_termination_msg=custom_termination,
    max_consecutive_auto_reply=20
)
```

## Working with Different LLM Providers

### OpenAI Configuration

```python
openai_config = {
    "model": "gpt-4-turbo",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "api_type": "openai"
}

assistant = AssistantAgent(
    name="GPT4Assistant",
    llm_config=openai_config
)
```

### Azure OpenAI Configuration

```python
azure_config = {
    "model": "gpt-4",  # Deployment name in Azure
    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    "api_type": "azure",
    "api_base": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "api_version": "2024-02-01"
}

assistant = AssistantAgent(
    name="AzureAssistant",
    llm_config=azure_config
)
```

### Local Models (Ollama)

```python
# First, start Ollama: ollama serve
# Pull a model: ollama pull llama3:70b

ollama_config = {
    "model": "llama3:70b",
    "api_base": "http://localhost:11434/v1",
    "api_key": "ollama"  # Placeholder, not used
}

assistant = AssistantAgent(
    name="LocalAssistant",
    llm_config=ollama_config
)
```

### Multiple Models with Fallback

```python
# Configure multiple models for fallback
config_list = [
    {
        "model": "gpt-4-turbo",
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    {
        "model": "gpt-3.5-turbo",  # Fallback
        "api_key": os.getenv("OPENAI_API_KEY")
    }
]

llm_config = {
    "config_list": config_list,
    "timeout": 120,
    "cache_seed": 42
}

assistant = AssistantAgent(
    name="RobustAssistant",
    llm_config=llm_config
)
```

## Practical Examples

### Research Assistant

```python
from ag2 import AssistantAgent, UserProxyAgent

# Create a research-focused assistant
researcher = AssistantAgent(
    name="Researcher",
    system_message="""You are a research assistant specializing in:
    - Finding and synthesizing information
    - Providing accurate citations
    - Breaking down complex topics
    - Identifying knowledge gaps

    Always cite your sources and indicate certainty levels.""",
    llm_config=llm_config
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5
)

# Run research task
result = user.initiate_chat(
    researcher,
    message="""Research the current state of quantum computing:
    1. What are the leading approaches (superconducting, trapped ion, etc.)?
    2. What are the main challenges?
    3. Which companies are leading?
    4. What are realistic timeline expectations?"""
)
```

### Code Review Assistant

```python
code_reviewer = AssistantAgent(
    name="CodeReviewer",
    system_message="""You are an expert code reviewer. For each code submission:
    1. Check for bugs and edge cases
    2. Evaluate code quality and readability
    3. Suggest performance improvements
    4. Identify security vulnerabilities
    5. Recommend best practices

    Provide specific, actionable feedback with code examples.""",
    llm_config=llm_config
)

developer = UserProxyAgent(
    name="Developer",
    human_input_mode="NEVER",
    code_execution_config=False
)

code_to_review = '''
def process_user_data(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            result.append({
                'name': item['name'],
                'email': item['email'],
                'score': item['points'] / item['total']
            })
    return result
'''

result = developer.initiate_chat(
    code_reviewer,
    message=f"Please review this Python code:\n```python\n{code_to_review}\n```"
)
```

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `APIError: Invalid API key` | Missing or wrong key | Check `.env` file and `OPENAI_API_KEY` |
| `RateLimitError` | Too many requests | Add delays or use retry logic |
| `ImportError: No module named 'ag2'` | Not installed | Run `pip install ag2` |
| `Docker not found` | Docker not running | Start Docker Desktop |
| `Timeout error` | Long-running code | Increase `timeout` in config |

### Debugging Tips

```python
import logging

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)
ag2_logger = logging.getLogger("ag2")
ag2_logger.setLevel(logging.DEBUG)

# Add custom logging to track conversation
class LoggingAssistant(AssistantAgent):
    def receive(self, message, sender, request_reply=True, silent=False):
        print(f"[{self.name}] Received from {sender.name}: {message['content'][:100]}...")
        return super().receive(message, sender, request_reply, silent)
```

### Validating Configuration

```python
def validate_ag2_setup():
    """Validate AG2 installation and configuration."""
    import ag2

    # Check version
    print(f"AG2 Version: {ag2.__version__}")

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    print(f"API Key: {api_key[:8]}...{api_key[-4:]}")

    # Test simple conversation
    assistant = AssistantAgent(
        name="TestAssistant",
        llm_config={"model": "gpt-3.5-turbo", "api_key": api_key}
    )
    user = UserProxyAgent(name="TestUser", human_input_mode="NEVER")

    result = user.initiate_chat(assistant, message="Say 'Hello, AG2!'", max_turns=1)
    print(f"Test Response: {result.chat_history[-1]['content']}")
    print("✓ AG2 setup validated successfully!")

validate_ag2_setup()
```

## Summary

In this chapter, you learned:

- **AG2 Architecture**: Agents communicate through messages, with LLM backends powering responses
- **Installation**: Multiple installation options from basic to development setups
- **Configuration**: Managing API keys and model configurations
- **Basic Agents**: Creating AssistantAgent and UserProxyAgent with various settings
- **Conversations**: Running single and multi-turn conversations
- **LLM Providers**: Configuring OpenAI, Azure, and local models
- **Troubleshooting**: Common issues and debugging techniques

## Key Takeaways

1. AG2 agents are autonomous entities that exchange messages
2. `AssistantAgent` uses LLMs; `UserProxyAgent` represents humans/executes code
3. Configuration can be file-based (`OAI_CONFIG_LIST.json`) or inline
4. Human input modes control the level of automation
5. Proper termination conditions prevent infinite loops

## Next Steps

In [Chapter 2: Agent Types](02-agent-types.md), you'll explore:
- Different built-in agent types and their use cases
- Creating custom agents
- Configuring agent personalities and behaviors
- Combining agents for complex tasks
