---
layout: default
title: "Chapter 6: Agents & Tools"
parent: "LangChain Tutorial"
nav_order: 6
---

# Chapter 6: Agents & Tools

Welcome to the world of autonomous AI agents! In this chapter, we'll explore how to build intelligent agents that can use tools, make decisions, and take actions autonomously. Agents represent a major leap forward in AI applications - moving from simple question-answering to proactive problem-solving systems.

## Agent Fundamentals

### What are LangChain Agents?

Agents are AI systems that can:
- **Reason** about what actions to take
- **Use tools** to gather information or perform tasks
- **Make decisions** based on available information
- **Execute actions** in sequence
- **Learn from results** to improve future decisions

Unlike simple chains that follow predetermined paths, agents can dynamically choose which tools to use and in what order.

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Set up the language model
llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])

# Create a simple agent
agent = initialize_agent(
    tools=[],  # We'll add tools in the next section
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)
```

## Tool Creation and Integration

### Building Custom Tools

Tools are functions that agents can call to perform specific actions. Each tool has a name, description, and function that gets executed.

```python
from langchain.agents import Tool
from typing import Any, Dict, List
import requests
import json

class CustomTools:
    @staticmethod
    def create_web_search_tool() -> Tool:
        """Create a web search tool"""
        def search_web(query: str) -> str:
            """Search the web for information"""
            # In a real implementation, you'd use a search API
            return f"Search results for: {query}"

        return Tool(
            name="Web Search",
            description="Search the web for current information and news",
            func=search_web
        )

    @staticmethod
    def create_calculator_tool() -> Tool:
        """Create a calculator tool"""
        def calculate(expression: str) -> str:
            """Calculate mathematical expressions"""
            try:
                # Be careful with eval - in production, use a safer method
                result = eval(expression)
                return f"Result: {result}"
            except Exception as e:
                return f"Error calculating: {e}"

        return Tool(
            name="Calculator",
            description="Perform mathematical calculations",
            func=calculate
        )

    @staticmethod
    def create_weather_tool() -> Tool:
        """Create a weather information tool"""
        def get_weather(location: str) -> str:
            """Get weather information for a location"""
            # In a real implementation, you'd call a weather API
            return f"Weather for {location}: Sunny, 72°F"

        return Tool(
            name="Weather",
            description="Get current weather information for a location",
            func=get_weather
        )

    @staticmethod
    def create_file_reader_tool() -> Tool:
        """Create a file reading tool"""
        def read_file(filename: str) -> str:
            """Read content from a file"""
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                return f"File content: {content[:500]}..."  # Limit output
            except Exception as e:
                return f"Error reading file: {e}"

        return Tool(
            name="File Reader",
            description="Read content from text files",
            func=read_file
        )

# Create tools
tools = [
    CustomTools.create_web_search_tool(),
    CustomTools.create_calculator_tool(),
    CustomTools.create_weather_tool(),
    CustomTools.create_file_reader_tool()
]
```

### Tool Integration with Agents

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# Initialize agent with tools
llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate"
)

# Use the agent
response = agent.run("What's the weather like in New York and what's 15 * 23?")
print(response)
```

## Agent Types

### Zero-Shot ReAct Agent

The most basic agent type that can use tools without specific examples:

```python
from langchain.agents import AgentType

# Zero-shot agent - works without examples
zero_shot_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# The agent will:
# 1. Think about what to do (Reasoning)
# 2. Decide which tool to use (Action)
# 3. Execute the tool
# 4. Observe the result
# 5. Continue or finish
```

### Conversational Agent

Agents that maintain conversation context:

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

# Create a conversational agent with memory
memory = ConversationBufferMemory(memory_key="chat_history")

conversational_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# The agent can now remember previous interactions
response1 = conversational_agent.run("What's the weather in Tokyo?")
response2 = conversational_agent.run("What's the temperature difference compared to the last city?")
```

### Custom Agent with Specific Reasoning

```python
from langchain.agents import AgentExecutor, BaseSingleActionAgent
from langchain.schema import AgentAction, AgentFinish
from typing import List, Tuple, Any, Union

class CustomReasoningAgent(BaseSingleActionAgent):
    """A custom agent with specific reasoning patterns"""

    @property
    def input_keys(self):
        return ["input"]

    def plan(self, intermediate_steps: List[Tuple[AgentAction, str]],
             **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        """Plan the next action based on current state"""

        # Get the input
        user_input = kwargs.get("input", "")

        # Simple decision logic
        if "calculate" in user_input.lower():
            return AgentAction(
                tool="Calculator",
                tool_input=user_input,
                log="Using calculator for mathematical computation"
            )
        elif "weather" in user_input.lower():
            return AgentAction(
                tool="Weather",
                tool_input=user_input,
                log="Checking weather information"
            )
        elif any(word in user_input.lower() for word in ["search", "find", "look up"]):
            return AgentAction(
                tool="Web Search",
                tool_input=user_input,
                log="Searching the web for information"
            )
        else:
            return AgentFinish(
                return_values={"output": f"I can help you with calculations, weather, or web searches. You asked: {user_input}"},
                log="No suitable tool found, providing direct response"
            )

    async def aplan(self, intermediate_steps: List[Tuple[AgentAction, str]],
                   **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        """Async version of plan"""
        return self.plan(intermediate_steps, **kwargs)

# Use the custom agent
custom_agent = CustomReasoningAgent()
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=custom_agent,
    tools=tools,
    verbose=True
)

result = agent_executor.run("Calculate 25 * 17")
print(result)
```

## Advanced Tool Patterns

### Tool Chains

Create sequences of tool usage:

```python
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

class ToolChain:
    def __init__(self, tools: List[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    def create_research_chain(self):
        """Create a research chain that uses multiple tools"""

        # Step 1: Search for information
        search_prompt = PromptTemplate(
            input_variables=["topic"],
            template="Search for recent information about: {topic}"
        )

        # Step 2: Analyze the results
        analysis_prompt = PromptTemplate(
            input_variables=["search_results"],
            template="Analyze these search results and summarize key points: {search_results}"
        )

        # Create the chain
        chain = SequentialChain(
            chains=[
                {"name": "search", "input": "topic", "output": "search_results",
                 "chain": LLMChain(llm=llm, prompt=search_prompt)},
                {"name": "analyze", "input": "search_results", "output": "analysis",
                 "chain": LLMChain(llm=llm, prompt=analysis_prompt)}
            ],
            input_variables=["topic"],
            output_variables=["analysis"],
            verbose=True
        )

        return chain

# Usage
tool_chain = ToolChain(tools)
research_chain = tool_chain.create_research_chain()

result = research_chain.run(topic="artificial intelligence trends 2024")
print(result)
```

### Tool with Memory

Tools that remember their previous interactions:

```python
class MemoryEnabledTool(Tool):
    """A tool that remembers previous interactions"""

    def __init__(self, name: str, description: str, func, memory_size: int = 10):
        super().__init__(name, description, func)
        self.memory: List[Dict[str, Any]] = []
        self.memory_size = memory_size

    def _run(self, tool_input: str) -> str:
        """Run the tool with memory awareness"""
        # Add context from memory
        context = self._get_memory_context(tool_input)

        # Enhance input with context
        enhanced_input = f"{context}\nCurrent request: {tool_input}"

        # Execute the tool
        result = self.func(enhanced_input)

        # Store in memory
        self._add_to_memory(tool_input, result)

        return result

    def _get_memory_context(self, current_input: str) -> str:
        """Get relevant context from memory"""
        if not self.memory:
            return ""

        # Find similar previous interactions
        relevant_memories = []
        for memory in self.memory:
            if any(word in current_input.lower() for word in memory["input"].lower().split()):
                relevant_memories.append(memory)

        if not relevant_memories:
            return ""

        context = "Previous interactions:\n"
        for memory in relevant_memories[-3:]:  # Last 3 relevant memories
            context += f"- Input: {memory['input']}\n  Result: {memory['result'][:100]}...\n"

        return context

    def _add_to_memory(self, input_text: str, result: str):
        """Add interaction to memory"""
        self.memory.append({
            "input": input_text,
            "result": result,
            "timestamp": time.time()
        })

        # Maintain memory size
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)

# Create a memory-enabled tool
memory_calculator = MemoryEnabledTool(
    name="Memory Calculator",
    description="Calculator with memory of previous calculations",
    func=lambda x: f"Calculated: {eval(x.split('Current request: ')[-1])}"
)
```

## Agent Workflows

### Multi-Step Agent Workflow

```python
class MultiStepAgentWorkflow:
    def __init__(self, llm, tools: List[Tool]):
        self.llm = llm
        self.tools = tools
        self.workflow_history = []

    def create_analysis_workflow(self):
        """Create a multi-step analysis workflow"""

        def step1_research(topic: str) -> str:
            """Research phase"""
            search_tool = next((t for t in self.tools if t.name == "Web Search"), None)
            if search_tool:
                return search_tool.run(f"Research: {topic}")
            return f"Research completed for: {topic}"

        def step2_analyze(research_results: str) -> str:
            """Analysis phase"""
            analysis_prompt = f"""Analyze these research results and extract key insights:

{research_results}

Provide:
1. Main findings
2. Key trends
3. Important implications
"""
            return self.llm.predict(analysis_prompt)

        def step3_summarize(analysis: str) -> str:
            """Summarization phase"""
            summary_prompt = f"""Create a concise summary of this analysis:

{analysis}

Keep it under 200 words."""
            return self.llm.predict(summary_prompt)

        return {
            "research": step1_research,
            "analyze": step2_analyze,
            "summarize": step3_summarize
        }

    def execute_workflow(self, workflow_steps: dict, initial_input: str):
        """Execute the complete workflow"""
        current_result = initial_input

        for step_name, step_func in workflow_steps.items():
            print(f"Executing step: {step_name}")
            current_result = step_func(current_result)

            # Record in history
            self.workflow_history.append({
                "step": step_name,
                "input": current_result[:100] + "...",
                "timestamp": time.time()
            })

        return current_result

# Usage
workflow = MultiStepAgentWorkflow(llm, tools)
steps = workflow.create_analysis_workflow()
final_result = workflow.execute_workflow(steps, "artificial intelligence in healthcare")
print(final_result)
```

### Conditional Agent Workflow

```python
class ConditionalAgentWorkflow:
    def __init__(self, llm, tools: List[Tool]):
        self.llm = llm
        self.tools = tools

    def create_conditional_workflow(self):
        """Create a workflow with conditional logic"""

        def assess_complexity(query: str) -> str:
            """Assess query complexity"""
            assessment_prompt = f"""Assess the complexity of this query on a scale of 1-5:

Query: {query}

Consider:
- Technical depth required
- Number of steps needed
- External information required
- Analysis complexity

Return only a number (1-5):"""
            complexity = int(self.llm.predict(assessment_prompt).strip())
            return "complex" if complexity > 3 else "simple"

        def handle_simple_query(query: str) -> str:
            """Handle simple queries directly"""
            return self.llm.predict(f"Answer this question: {query}")

        def handle_complex_query(query: str) -> str:
            """Handle complex queries with full workflow"""
            # Use tools for complex queries
            agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
            return agent.run(query)

        def route_query(query: str) -> str:
            """Route query based on complexity"""
            complexity = assess_complexity(query)

            if complexity == "simple":
                return handle_simple_query(query)
            else:
                return handle_complex_query(query)

        return route_query

# Usage
conditional_workflow = ConditionalAgentWorkflow(llm, tools)
query_handler = conditional_workflow.create_conditional_workflow()

# Test with different queries
simple_result = query_handler("What is 2 + 2?")
complex_result = query_handler("Analyze the impact of AI on job markets and provide detailed recommendations")
```

## Agent Monitoring and Debugging

### Agent Performance Tracking

```python
class AgentMonitor:
    def __init__(self):
        self.agent_metrics = {}
        self.tool_usage = {}
        self.error_logs = []

    def track_agent_execution(self, agent_name: str, task: str, execution_time: float, success: bool):
        """Track agent execution metrics"""
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_time": 0,
                "average_time": 0
            }

        metrics = self.agent_metrics[agent_name]
        metrics["total_executions"] += 1
        metrics["total_time"] += execution_time

        if success:
            metrics["successful_executions"] += 1
        else:
            metrics["failed_executions"] += 1

        metrics["average_time"] = metrics["total_time"] / metrics["total_executions"]

    def track_tool_usage(self, tool_name: str, agent_name: str, success: bool):
        """Track tool usage"""
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = {
                "total_uses": 0,
                "successful_uses": 0,
                "agents": set()
            }

        usage = self.tool_usage[tool_name]
        usage["total_uses"] += 1
        usage["agents"].add(agent_name)

        if success:
            usage["successful_uses"] += 1

    def log_error(self, agent_name: str, error: str, context: Dict[str, Any]):
        """Log agent errors"""
        self.error_logs.append({
            "agent": agent_name,
            "error": error,
            "context": context,
            "timestamp": time.time()
        })

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        return {
            "agent_metrics": self.agent_metrics,
            "tool_usage": self.tool_usage,
            "error_summary": {
                "total_errors": len(self.error_logs),
                "recent_errors": self.error_logs[-5:]  # Last 5 errors
            },
            "top_performing_agents": sorted(
                self.agent_metrics.items(),
                key=lambda x: x[1]["successful_executions"] / x[1]["total_executions"] if x[1]["total_executions"] > 0 else 0,
                reverse=True
            )[:3]
        }

# Usage
monitor = AgentMonitor()

# Track agent performance
monitor.track_agent_execution("ResearchAgent", "Analyze AI trends", 2.5, True)
monitor.track_tool_usage("Web Search", "ResearchAgent", True)

# Get performance report
report = monitor.get_performance_report()
print("Performance Report:", report)
```

## Best Practices for Agents

### Agent Design Principles

```python
class AgentBestPractices:
    @staticmethod
    def create_focused_agent(specialty: str, tools: List[Tool], llm):
        """Create a focused agent with clear boundaries"""
        system_message = f"""You are a specialized {specialty} agent.

Your expertise: {specialty}
Your limitations: Stick to {specialty} related tasks
Your tools: {', '.join([t.name for t in tools])}

Always:
1. Stay within your area of expertise
2. Use appropriate tools when needed
3. Provide clear explanations
4. Ask for clarification when uncertain
"""

        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            system_message=system_message,
            verbose=True,
            max_iterations=3,  # Prevent runaway executions
            handle_parsing_errors=True
        )

    @staticmethod
    def add_safety_checks(agent_executor):
        """Add safety checks to agent execution"""
        original_run = agent_executor.run

        def safe_run(query: str) -> str:
            # Check for potentially harmful queries
            harmful_patterns = ["delete", "remove", "drop", "shutdown", "format"]

            if any(pattern in query.lower() for pattern in harmful_patterns):
                return "I'm sorry, but I cannot execute potentially harmful commands."

            # Add rate limiting
            # Add input validation

            return original_run(query)

        agent_executor.run = safe_run
        return agent_executor

    @staticmethod
    def create_agent_team(specialties: List[str], llm):
        """Create a team of specialized agents"""
        agents = {}

        for specialty in specialties:
            tools = AgentBestPractices._get_specialty_tools(specialty)
            agents[specialty] = AgentBestPractices.create_focused_agent(
                specialty, tools, llm
            )

        return agents

    @staticmethod
    def _get_specialty_tools(specialty: str) -> List[Tool]:
        """Get appropriate tools for a specialty"""
        tool_mapping = {
            "research": ["Web Search", "File Reader"],
            "analysis": ["Calculator", "Data Analysis"],
            "writing": ["File Writer", "Content Generator"],
            "coding": ["Code Executor", "File Reader"]
        }

        tool_names = tool_mapping.get(specialty, [])
        # Return actual tool instances
        return []  # Placeholder
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Agent Fundamentals** - What agents are and how they work
2. **Tool Creation** - Building custom tools for specific tasks
3. **Agent Types** - Zero-shot, conversational, and custom agents
4. **Advanced Tool Patterns** - Tool chains and memory-enabled tools
5. **Agent Workflows** - Multi-step and conditional workflows
6. **Monitoring and Debugging** - Performance tracking and error handling
7. **Best Practices** - Safety, focus, and team-based approaches

## Next Steps

Now that you understand agents and tools, let's explore advanced chains and custom implementations. In [Chapter 7: Advanced Chains](07-advanced-chains.md), we'll dive into complex workflow patterns, custom chain development, and advanced LangChain features.

---

**Practice what you've learned:**
1. Create a custom tool for a specific task in your domain
2. Build an agent that uses multiple tools to solve a complex problem
3. Implement a conditional workflow that adapts based on task complexity
4. Set up performance monitoring for your agents

*What kind of autonomous agent will you build first?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `tools`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Agents & Tools` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `memory`, `tool`, `query` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Agents & Tools` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `tools` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `tools` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Vector Stores & Retrieval](05-vector-stores.md)
- [Next Chapter: Chapter 7: Advanced Chains](07-advanced-chains.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
