---
layout: default
title: "Chapter 1: Getting Started with Microsoft AutoGen"
parent: "Microsoft AutoGen Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Microsoft AutoGen

Welcome to Microsoft AutoGen! If you've ever wanted to build AI systems where multiple agents collaborate, communicate, and solve complex problems together, you're in the right place. AutoGen makes it easy to create sophisticated multi-agent AI applications with specialized roles and intelligent coordination.

## What Makes AutoGen Special?

AutoGen revolutionizes AI development by:
- **Multi-Agent Collaboration** - Agents work together to solve complex tasks
- **Flexible Communication** - Agents can negotiate, delegate, and coordinate
- **Tool Integration** - Easy connection to external APIs and services
- **Customizable Agents** - Build agents with specialized capabilities
- **Production-Ready** - Scalable architecture for real-world applications

## Installing AutoGen

### Basic Installation

```bash
# Install AutoGen via pip
pip install pyautogen

# Or install from source
git clone https://github.com/microsoft/autogen.git
cd autogen
pip install -e .
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/microsoft/autogen.git
cd autogen

# Install in development mode with all dependencies
pip install -e ".[test,docs]"

# Run tests to verify installation
python -m pytest tests/
```

## Your First Multi-Agent Conversation

Let's create your first conversation between AI agents:

### Step 1: Basic Setup

```python
import os
from autogen import AssistantAgent, UserProxyAgent

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

print("🤖 AutoGen initialized successfully!")
```

### Step 2: Create Your First Agents

```python
# Create an assistant agent
assistant = AssistantAgent(
    name="Assistant",
    llm_config={
        "model": "gpt-4",
        "api_key": os.environ["OPENAI_API_KEY"]
    },
    system_message="You are a helpful AI assistant."
)

# Create a user proxy agent
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # No human input required
    code_execution_config=False  # Disable code execution for now
)

print("🎭 Agents created successfully!")
```

### Step 3: Start a Conversation

```python
# Initiate a conversation
user_proxy.initiate_chat(
    assistant,
    message="Hello! Can you help me understand how AutoGen works?"
)

print("💬 Conversation completed!")
```

### Step 4: Advanced Multi-Agent Setup

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create multiple specialized agents
researcher = AssistantAgent(
    name="Researcher",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You are a research specialist. You find and analyze information."
)

writer = AssistantAgent(
    name="Writer",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You are a content writer. You create engaging written content."
)

reviewer = AssistantAgent(
    name="Reviewer",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You are a content reviewer. You ensure quality and accuracy."
)

# Create a group chat
groupchat = GroupChat(
    agents=[researcher, writer, reviewer],
    messages=[],
    max_round=6
)

# Create a group chat manager
manager = GroupChatManager(
    groupchat=groupchat,
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
)

# Start a group conversation
user_proxy.initiate_chat(
    manager,
    message="Write a comprehensive guide about renewable energy sources."
)
```

## Understanding Agent Types

### Core Agent Types

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChatManager

# 1. Assistant Agent - AI-powered agent with LLM capabilities
assistant_agent = AssistantAgent(
    name="Assistant",
    llm_config={
        "model": "gpt-4",
        "temperature": 0.7,
        "api_key": os.environ["OPENAI_API_KEY"]
    },
    system_message="You are a helpful AI assistant with expertise in various domains."
)

# 2. User Proxy Agent - Represents human users or handles external interactions
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",  # Requires human input
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False
    }
)

# 3. Function-Calling Agent - Specialized for tool usage
function_agent = AssistantAgent(
    name="FunctionCaller",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You can use various tools and functions to accomplish tasks.",
    function_map={
        "search_web": search_web_function,
        "calculate": calculate_function,
        "send_email": send_email_function
    }
)
```

### Agent Configuration Options

```python
# Advanced agent configuration
advanced_agent = AssistantAgent(
    name="AdvancedAgent",

    # LLM Configuration
    llm_config={
        "model": "gpt-4-turbo",
        "temperature": 0.3,
        "max_tokens": 2000,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1,
        "api_key": os.environ["OPENAI_API_KEY"]
    },

    # System Message
    system_message="""You are an expert AI assistant with the following capabilities:
    - Deep knowledge across multiple domains
    - Ability to break down complex problems
    - Clear communication and explanation skills
    - Proactive problem-solving approach""",

    # Interaction Settings
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
    code_execution_config=False,

    # Custom Functions
    function_map={
        "web_search": web_search_tool,
        "data_analysis": data_analysis_tool,
        "file_operations": file_operations_tool
    }
)
```

## Real-World Multi-Agent Applications

### Research and Writing Team

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

class ResearchWritingTeam:
    def __init__(self):
        self.researcher = AssistantAgent(
            name="Researcher",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a research specialist. Your role is to:
            - Find reliable sources and information
            - Analyze data and trends
            - Provide evidence-based insights
            - Cite sources properly"""
        )

        self.writer = AssistantAgent(
            name="Writer",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a content writer. Your role is to:
            - Create engaging, well-structured content
            - Use clear and concise language
            - Organize information logically
            - Ensure content flows naturally"""
        )

        self.editor = AssistantAgent(
            name="Editor",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a content editor. Your role is to:
            - Review content for accuracy and clarity
            - Ensure consistency and coherence
            - Check for grammar and style issues
            - Provide constructive feedback"""
        )

        self.coordinator = AssistantAgent(
            name="Coordinator",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are the team coordinator. Your role is to:
            - Manage the workflow and assign tasks
            - Ensure quality and deadlines
            - Facilitate communication between team members
            - Make final decisions on content direction"""
        )

    def create_research_report(self, topic):
        """Create a comprehensive research report using the team"""

        # Set up group chat
        groupchat = GroupChat(
            agents=[self.researcher, self.writer, self.editor, self.coordinator],
            messages=[],
            max_round=12,
            speaker_selection_method="round_robin"
        )

        manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
        )

        # Create user proxy to initiate
        user_proxy = UserProxyAgent(
            name="ProjectManager",
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Start the collaborative process
        user_proxy.initiate_chat(
            manager,
            message=f"Create a comprehensive research report on: {topic}"
        )

        return groupchat.messages

# Usage
team = ResearchWritingTeam()
messages = team.create_research_report("The impact of AI on healthcare")
print("Research report completed!")
```

### Customer Support System

```python
from autogen import AssistantAgent, UserProxyAgent

class CustomerSupportSystem:
    def __init__(self):
        self.triage_agent = AssistantAgent(
            name="TriageAgent",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a customer support triage specialist. Your role is to:
            - Assess the urgency and complexity of customer issues
            - Categorize problems (billing, technical, general inquiry)
            - Route to appropriate specialists
            - Provide initial responses for simple issues"""
        )

        self.technical_agent = AssistantAgent(
            name="TechnicalAgent",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a technical support specialist. Your role is to:
            - Troubleshoot technical problems
            - Provide step-by-step solutions
            - Escalate complex issues when needed
            - Document solutions for future reference"""
        )

        self.billing_agent = AssistantAgent(
            name="BillingAgent",
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
            system_message="""You are a billing support specialist. Your role is to:
            - Handle payment and billing inquiries
            - Process refunds and credits
            - Explain billing policies and charges
            - Assist with account management"""
        )

    def handle_customer_inquiry(self, customer_message):
        """Handle customer inquiry with appropriate agent routing"""

        # Initial triage
        triage_response = self.triage_agent.generate_reply(
            messages=[{"role": "user", "content": customer_message}]
        )

        # Determine which agent to route to based on triage
        if "billing" in customer_message.lower() or "payment" in customer_message.lower():
            specialist = self.billing_agent
        elif "error" in customer_message.lower() or "not working" in customer_message.lower():
            specialist = self.technical_agent
        else:
            specialist = self.technical_agent  # Default to technical

        # Get specialist response
        specialist_response = specialist.generate_reply(
            messages=[
                {"role": "system", "content": f"Triage assessment: {triage_response}"},
                {"role": "user", "content": customer_message}
            ]
        )

        return {
            "triage": triage_response,
            "specialist": specialist.name,
            "response": specialist_response
        }

# Usage
support_system = CustomerSupportSystem()
result = support_system.handle_customer_inquiry(
    "My account shows an incorrect charge from last month"
)

print(f"Triage: {result['triage']}")
print(f"Routed to: {result['specialist']}")
print(f"Response: {result['response']}")
```

## Configuration and Optimization

### Basic Configuration

```python
import os
from autogen import AssistantAgent

# Set API keys
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Configure agent with optimized settings
agent = AssistantAgent(
    name="OptimizedAgent",
    llm_config={
        "model": "gpt-4",
        "temperature": 0.3,  # Lower temperature for more consistent responses
        "max_tokens": 1000,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1,
        "api_key": os.environ["OPENAI_API_KEY"]
    },
    system_message="You are a highly capable AI assistant.",
    max_consecutive_auto_reply=5,  # Limit conversation length
    human_input_mode="NEVER"
)
```

### Environment Configuration

```bash
# .env file
OPENAI_API_KEY=your-openai-api-key
AUTOGEN_CACHE_DIR=./cache
AUTOGEN_LOG_LEVEL=INFO
AUTOGEN_MAX_CONSECUTIVE_REPLIES=10
AUTOGEN_CODE_EXECUTION_TIMEOUT=30
```

### Performance Optimization

```python
# Optimized group chat configuration
groupchat = GroupChat(
    agents=[agent1, agent2, agent3],
    messages=[],
    max_round=6,  # Limit conversation rounds
    speaker_selection_method="round_robin",  # Structured conversation flow
    allow_repeat_speaker=False  # Prevent agents from speaking consecutively
)

# Optimized LLM configuration
llm_config = {
    "model": "gpt-4",
    "temperature": 0.3,
    "max_tokens": 500,  # Shorter responses for faster interaction
    "cache_seed": 42,   # Enable caching for repeated requests
    "api_key": os.environ["OPENAI_API_KEY"]
}
```

## Conversation Management

### Basic Conversation Flow

```python
from autogen import AssistantAgent, UserProxyAgent

# Create agents
assistant = AssistantAgent(
    name="Assistant",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER"
)

# Start conversation
chat_result = user_proxy.initiate_chat(
    assistant,
    message="Explain quantum computing in simple terms",
    max_turns=3  # Limit conversation length
)

# Access conversation history
for message in chat_result.chat_history:
    print(f"{message['role']}: {message['content']}")
```

### Advanced Conversation Patterns

```python
# Sequential conversation
def sequential_conversation(agents, initial_message):
    """Run agents in sequence"""
    current_message = initial_message

    for agent in agents:
        response = agent.generate_reply(
            messages=[{"role": "user", "content": current_message}]
        )
        current_message = response
        print(f"{agent.name}: {response}")

    return current_message

# Parallel conversation processing
def parallel_conversation(agents, message):
    """Process message with multiple agents in parallel"""
    import asyncio

    async def process_with_agent(agent):
        return await agent.agenerate_reply(
            messages=[{"role": "user", "content": message}]
        )

    async def run_parallel():
        tasks = [process_with_agent(agent) for agent in agents]
        responses = await asyncio.gather(*tasks)
        return responses

    # Run in event loop
    responses = asyncio.run(run_parallel())

    for agent, response in zip(agents, responses):
        print(f"{agent.name}: {response}")
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Microsoft AutoGen** and set up your development environment
2. **Created your first multi-agent conversation** with specialized roles
3. **Built real-world applications** like research teams and customer support systems
4. **Understood agent types** and their different capabilities
5. **Configured agents** with optimized settings and conversation management
6. **Implemented advanced patterns** like sequential and parallel conversations
7. **Explored group chat dynamics** and agent coordination

## Next Steps

Now that you understand the basics of multi-agent systems, let's explore the different types of agents and their roles. In [Chapter 2: Agent Architecture & Roles](02-agent-architecture.md), we'll dive into the technical details of how different agent types work and how to choose the right agent for your use case.

---

**Practice what you've learned:**
1. Create a multi-agent system for content creation (researcher, writer, editor)
2. Build a customer support system with specialized agents
3. Implement a collaborative coding team with different specialties
4. Experiment with different conversation patterns and agent configurations

*What kind of multi-agent system would you build first?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `AssistantAgent`, `name`, `environ` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Microsoft AutoGen` as an operating subsystem inside **Microsoft AutoGen Tutorial: Building Multi-Agent AI Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `llm_config`, `model`, `api_key` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Microsoft AutoGen` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `AssistantAgent`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `environ`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `AssistantAgent` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Agent Architecture & Roles](02-agent-architecture.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
