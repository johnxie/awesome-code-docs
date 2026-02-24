---
layout: default
title: "Chapter 1: Getting Started with CrewAI"
parent: "CrewAI Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with CrewAI

Welcome to CrewAI! If you've ever wondered how to orchestrate multiple AI agents to work together like a well-coordinated team, you're in the right place. CrewAI is a powerful framework that enables you to create collaborative AI agent teams that can tackle complex tasks through specialization and cooperation.

## What Makes CrewAI Special?

CrewAI revolutionizes AI development by enabling:

- **Role-based collaboration** - Agents with specialized roles working together
- **Intelligent task delegation** - Automatic assignment of tasks to appropriate agents
- **Seamless communication** - Agents that can share information and coordinate actions
- **Scalable architectures** - From simple crews to complex multi-agent hierarchies
- **Production-ready deployment** - Built for real-world applications and scaling

## Installing CrewAI

### Basic Installation

```bash
# Install CrewAI
pip install crewai

# Optional: Install with additional tools
pip install crewai[tools]

# For development and examples
pip install crewai[all]
```

### Environment Setup

```bash
# Create a virtual environment
python -m venv crewai-env
source crewai-env/bin/activate  # On Windows: crewai-env\Scripts\activate

# Install dependencies
pip install crewai crewai[tools]
```

### API Keys Setup

```bash
# Set up environment variables
export OPENAI_API_KEY="your-openai-key-here"
export SERPAPI_API_KEY="your-serpapi-key-here"  # Optional for web search
```

## Your First AI Crew

### Basic Crew Structure

```python
from crewai import Crew, Agent, Task
import os

# Set up API keys
os.environ["OPENAI_API_KEY"] = "your-openai-key-here"

# Create your first agent
researcher = Agent(
    role="Research Analyst",
    goal="Gather and analyze information on given topics",
    backstory="You are an expert research analyst with years of experience in data collection and analysis.",
    verbose=True
)

# Create a task
research_task = Task(
    description="Research the latest developments in artificial intelligence for 2024",
    agent=researcher,
    expected_output="A comprehensive report on AI developments in 2024"
)

# Create and run the crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

# Execute the crew
result = crew.kickoff()
print(result)
```

### Understanding the Components

#### Agents
```python
from crewai import Agent

# Basic agent configuration
agent = Agent(
    role="Content Writer",                    # Agent's role/purpose
    goal="Create engaging content",           # Primary objective
    backstory="Expert writer with 10+ years", # Background context
    verbose=True,                            # Enable detailed logging
    allow_delegation=False                   # Can delegate to other agents
)
```

#### Tasks
```python
from crewai import Task

# Task definition
task = Task(
    description="Write a blog post about AI trends",    # What to do
    agent=agent,                                       # Which agent handles it
    expected_output="A 1000-word blog post",           # Expected result format
    context=[],                                        # Previous task context
    async_execution=False                              # Synchronous execution
)
```

#### Crew
```python
from crewai import Crew

# Crew configuration
crew = Crew(
    agents=[agent1, agent2, agent3],    # List of agents
    tasks=[task1, task2, task3],        # List of tasks
    verbose=True,                       # Enable logging
    process="sequential"                # Execution mode
)
```

## Building a Simple Research Crew

Let's create a more comprehensive example:

```python
from crewai import Crew, Agent, Task
from crewai_tools import SerperDevTool
import os

# Set API keys
os.environ["OPENAI_API_KEY"] = "your-openai-key-here"
os.environ["SERPER_API_KEY"] = "your-serper-key-here"

# Create specialized agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Conduct thorough research on complex topics",
    backstory="""You are a senior research analyst with expertise in 
    gathering and synthesizing information from multiple sources.""",
    tools=[SerperDevTool()],
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging and well-structured content",
    backstory="""You are an experienced content writer who excels at 
    transforming complex information into readable content.""",
    verbose=True
)

reviewer = Agent(
    role="Quality Assurance Specialist",
    goal="Ensure content quality and accuracy",
    backstory="""You are a meticulous QA specialist who reviews content 
    for accuracy, clarity, and completeness.""",
    verbose=True
)

# Define tasks
research_task = Task(
    description="""Research the impact of AI on healthcare industry in 2024. 
    Focus on: telemedicine, drug discovery, patient care, and regulatory changes.""",
    agent=researcher,
    expected_output="Comprehensive research findings with key insights and data points"
)

writing_task = Task(
    description="""Write a detailed article about AI's impact on healthcare based on the research findings.
    Include: introduction, key areas of impact, case studies, challenges, and future outlook.""",
    agent=writer,
    context=[research_task],
    expected_output="Well-structured 1500-word article ready for publication"
)

review_task = Task(
    description="""Review the article for accuracy, clarity, and completeness.
    Check for: factual accuracy, logical flow, grammar, and engagement.""",
    agent=reviewer,
    context=[writing_task],
    expected_output="Reviewed article with feedback and suggested improvements"
)

# Create the crew
healthcare_crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    verbose=True
)

# Execute the crew
result = healthcare_crew.kickoff()
print("Crew execution completed!")
print("Final result:", result)
```

## Understanding Crew Execution

### Execution Flow

```mermaid
graph TD
    A[Crew Kickoff] --> B[Task Assignment]
    B --> C[Agent Execution]
    C --> D[Result Generation]
    D --> E[Context Passing]
    E --> F[Next Task]
    F --> G{Crew Complete?}
    G -->|No| B
    G -->|Yes| H[Final Result]

    classDef start fill:#e1f5fe,stroke:#01579b
    classDef process fill:#fff3e0,stroke:#ef6c00
    classDef decision fill:#fce4ec,stroke:#c2185b
    classDef end fill:#e8f5e8,stroke:#1b5e20

    class A start
    class B,C,D,E,F process
    class G decision
    class H end
```

### Process Types

```python
# Sequential execution (default)
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process="sequential"  # Tasks execute one after another
)

# Hierarchical execution
crew = Crew(
    agents=[manager, worker1, worker2],
    tasks=[main_task, subtask1, subtask2],
    process="hierarchical"  # Manager delegates to workers
)
```

## Agent Configuration Deep Dive

### Advanced Agent Properties

```python
from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool

# Advanced agent configuration
senior_researcher = Agent(
    role="Senior Research Analyst",
    goal="Conduct comprehensive research and analysis",
    backstory="""PhD in Computer Science with 15 years of experience 
    in AI research and analysis.""",

    # Tools for enhanced capabilities
    tools=[
        SerperDevTool(),
        WebsiteSearchTool()
    ],

    # Behavioral settings
    verbose=True,
    allow_delegation=True,
    max_execution_time=300,  # 5 minutes timeout

    # Memory and context
    memory=True,
    max_memory_items=100,

    # Custom settings
    temperature=0.7,  # Creativity level
    model="gpt-4"     # LLM model to use
)
```

### Tool Integration

```python
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    FileReadTool,
    DirectoryReadTool
)

# Tool-enabled agent
research_agent = Agent(
    role="Research Specialist",
    goal="Gather information from various sources",
    tools=[
        SerperDevTool(),        # Web search
        WebsiteSearchTool(),    # Website content extraction
        FileReadTool(),         # File reading capabilities
        DirectoryReadTool()     # Directory exploration
    ],
    verbose=True
)
```

## Error Handling and Debugging

### Basic Error Handling

```python
from crewai import Crew

try:
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task]
    )

    result = crew.kickoff()
    print("Success:", result)

except Exception as e:
    print(f"Crew execution failed: {e}")
    # Implement fallback logic
    fallback_result = handle_crew_failure(e)
```

### Debugging Crew Execution

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True,           # Enable crew-level logging
    debug=True             # Enable debug mode
)

# Monitor execution
result = crew.kickoff()

# Access execution details
print("Execution summary:", crew.execution_summary)
print("Agent performance:", crew.agent_performance)
print("Task status:", crew.task_status)
```

## Best Practices for Getting Started

### Crew Design Principles

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Clear Communication**: Define expected inputs and outputs clearly
3. **Progressive Complexity**: Start simple and gradually add complexity
4. **Error Handling**: Always plan for potential failures
5. **Monitoring**: Track performance and iterate on design

### Common Pitfalls to Avoid

```python
# ❌ Bad: Overloaded agent
overloaded_agent = Agent(
    role="Everything Expert",
    goal="Do research, writing, analysis, and project management"
)

# ✅ Good: Specialized agents
researcher = Agent(role="Research Specialist", goal="Gather information")
writer = Agent(role="Content Writer", goal="Create content")
analyst = Agent(role="Data Analyst", goal="Analyze data")
```

## What We've Accomplished

✅ **Installed CrewAI** and set up the development environment
✅ **Created your first AI agent** with basic capabilities
✅ **Built a simple crew** with multiple agents and tasks
✅ **Understood crew execution flow** and process types
✅ **Configured advanced agent properties** and tool integration
✅ **Implemented error handling** and debugging techniques

## Next Steps

Ready to explore specialized agent roles? In [Chapter 2: Agent Roles & Specializations](02-agent-roles.md), we'll dive into creating agents with specific expertise areas and capabilities.

---

**Practice what you've learned:**
1. Create a crew for a different domain (marketing, product development, etc.)
2. Experiment with different agent configurations and tools
3. Try sequential vs hierarchical execution modes
4. Implement error handling for your crew executions

*Remember: Great crews start with well-defined roles and clear communication patterns!*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `Agent`, `crew`, `Crew` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with CrewAI` as an operating subsystem inside **CrewAI Tutorial: Building Collaborative AI Agent Teams**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `crewai`, `agent`, `Task` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with CrewAI` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `Agent`.
2. **Input normalization**: shape incoming data so `crew` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Crew`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/crewAIInc/crewAI)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `Agent` and `crew` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Agent Roles & Specializations](02-agent-roles.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
