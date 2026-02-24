---
layout: default
title: "Phidata Tutorial - Chapter 2: Agent Architecture"
nav_order: 2
has_children: false
parent: Phidata Tutorial
---

# Chapter 2: Understanding Phidata Agent Architecture

Welcome to **Chapter 2: Understanding Phidata Agent Architecture**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Dive deep into the internal components, reasoning engine, and modular design that power Phidata agents.

## Core Agent Components

### Agent Class Structure

```python
from phidata.agent import Agent
from phidata.model import Model
from phidata.tools import Tool
from phidata.memory import Memory
from phidata.knowledge import Knowledge
from typing import List, Optional, Dict, Any

class PhidataAgent:
    """Complete breakdown of Agent class architecture."""

    def __init__(
        self,
        # Core identity
        name: str,
        instructions: str,

        # Model configuration
        model: Model,

        # Optional components
        tools: Optional[List[Tool]] = None,
        memory: Optional[Memory] = None,
        knowledge: Optional[Knowledge] = None,

        # Behavior configuration
        reasoning_steps: Optional[List[str]] = None,
        response_format: Optional[Dict[str, Any]] = None,

        # Runtime settings
        debug_mode: bool = False,
        stream: bool = False,
        **kwargs
    ):
        self.name = name
        self.instructions = instructions
        self.model = model

        # Initialize components
        self.tools = tools or []
        self.memory = memory
        self.knowledge = knowledge

        # Reasoning configuration
        self.reasoning_steps = reasoning_steps or self.default_reasoning_steps()

        # Response configuration
        self.response_format = response_format

        # Runtime settings
        self.debug_mode = debug_mode
        self.stream = stream

        # Internal state
        self.conversation_history = []
        self.run_count = 0

    def default_reasoning_steps(self) -> List[str]:
        """Default reasoning process."""
        return [
            "analyze_user_request",
            "gather_context",
            "select_tools",
            "execute_tools",
            "synthesize_response"
        ]
```

### Component Breakdown

```python
# Model Component
class ModelComponent:
    """Handles LLM interactions and response generation."""

    def __init__(self, model_config: Dict[str, Any]):
        self.provider = model_config.get("provider", "openai")
        self.model_id = model_config.get("model_id", "gpt-4")
        self.api_key = model_config.get("api_key")
        self.temperature = model_config.get("temperature", 0.7)
        self.max_tokens = model_config.get("max_tokens", 4096)

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM."""
        # Implementation depends on provider
        if self.provider == "openai":
            return self._openai_generate(prompt, **kwargs)
        elif self.provider == "anthropic":
            return self._anthropic_generate(prompt, **kwargs)
        # ... other providers

    def _openai_generate(self, prompt: str, **kwargs) -> str:
        """OpenAI-specific generation."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs
        )

        return response.choices[0].message.content

# Tool Component
class ToolComponent:
    """Manages external tools and function calling."""

    def __init__(self, tools: List[Tool]):
        self.tools = tools
        self.tool_registry = {tool.name: tool for tool in tools}

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get tool schemas for LLM function calling."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools
        ]

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a specific tool."""
        if tool_name not in self.tool_registry:
            raise ValueError(f"Tool {tool_name} not found")

        tool = self.tool_registry[tool_name]
        return tool.run(**parameters)

# Memory Component
class MemoryComponent:
    """Handles conversation memory and context retention."""

    def __init__(self, memory_type: str = "buffer", max_tokens: int = 4000):
        self.memory_type = memory_type
        self.max_tokens = max_tokens
        self.history = []

    def add_message(self, role: str, content: str):
        """Add message to memory."""
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })

        # Prune if exceeding max tokens
        self._prune_memory()

    def get_context(self, current_prompt: str) -> str:
        """Get relevant context for current prompt."""
        if self.memory_type == "buffer":
            return self._get_buffer_context()
        elif self.memory_type == "summary":
            return self._get_summary_context()
        elif self.memory_type == "vector":
            return self._get_vector_context(current_prompt)

    def _prune_memory(self):
        """Prune memory to stay within token limits."""
        # Simplified token counting
        total_tokens = sum(len(msg["content"].split()) for msg in self.history)

        while total_tokens > self.max_tokens and len(self.history) > 1:
            removed = self.history.pop(0)
            total_tokens -= len(removed["content"].split())
```

## Reasoning Engine

### Step-by-Step Reasoning Process

```python
class ReasoningEngine:
    """Implements the agent's reasoning and decision-making process."""

    def __init__(self, agent: PhidataAgent):
        self.agent = agent
        self.reasoning_steps = agent.reasoning_steps

    async def reason_and_respond(self, user_input: str) -> str:
        """Execute complete reasoning process."""

        # Step 1: Analyze user request
        analysis = await self.analyze_request(user_input)
        if self.agent.debug_mode:
            print(f"📊 Analysis: {analysis}")

        # Step 2: Gather context
        context = await self.gather_context(user_input, analysis)
        if self.agent.debug_mode:
            print(f"📚 Context: {context[:200]}...")

        # Step 3: Select relevant tools
        selected_tools = await self.select_tools(user_input, analysis, context)
        if self.agent.debug_mode:
            print(f"🛠️ Selected tools: {[t.name for t in selected_tools]}")

        # Step 4: Execute tools if needed
        tool_results = []
        if selected_tools:
            tool_results = await self.execute_tools(selected_tools, user_input, context)
            if self.agent.debug_mode:
                print(f"⚡ Tool results: {len(tool_results)} results")

        # Step 5: Synthesize final response
        response = await self.synthesize_response(
            user_input, analysis, context, tool_results
        )

        return response

    async def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """Analyze the user's request to understand intent and requirements."""

        analysis_prompt = f"""
        Analyze this user request and provide:
        1. Primary intent (question, command, request, etc.)
        2. Key topics or subjects mentioned
        3. Required capabilities or tools
        4. Complexity level (simple, moderate, complex)
        5. Expected response type (factual, creative, analytical, etc.)

        User request: {user_input}

        Provide analysis as JSON:
        """

        # Use a lightweight model for analysis
        analysis_response = await self.agent.model.generate(analysis_prompt)

        try:
            return json.loads(analysis_response)
        except:
            # Fallback analysis
            return {
                "intent": "general_query",
                "topics": [],
                "capabilities": [],
                "complexity": "moderate",
                "response_type": "informative"
            }

    async def gather_context(self, user_input: str, analysis: Dict[str, Any]) -> str:
        """Gather relevant context from memory and knowledge."""

        context_parts = []

        # Get conversation history
        if self.agent.memory:
            history_context = self.agent.memory.get_context(user_input)
            context_parts.append(f"Conversation history: {history_context}")

        # Get knowledge base context
        if self.agent.knowledge:
            knowledge_context = await self.agent.knowledge.search(user_input)
            context_parts.append(f"Knowledge: {knowledge_context}")

        # Add current analysis
        context_parts.append(f"Request analysis: {json.dumps(analysis)}")

        return "\n\n".join(context_parts)

    async def select_tools(self, user_input: str, analysis: Dict[str, Any],
                          context: str) -> List[Tool]:
        """Select appropriate tools based on request analysis."""

        available_tools = self.agent.tools
        required_capabilities = analysis.get("capabilities", [])

        selected_tools = []

        for tool in available_tools:
            # Check if tool capabilities match requirements
            tool_capabilities = getattr(tool, 'capabilities', [])

            if any(cap in tool_capabilities for cap in required_capabilities):
                selected_tools.append(tool)

        # Limit to top 3 most relevant tools
        return selected_tools[:3]

    async def execute_tools(self, tools: List[Tool], user_input: str,
                           context: str) -> List[Dict[str, Any]]:
        """Execute selected tools and collect results."""

        results = []

        for tool in tools:
            try:
                # Prepare tool input
                tool_input = self.prepare_tool_input(tool, user_input, context)

                # Execute tool
                result = await tool.run(**tool_input)

                results.append({
                    "tool": tool.name,
                    "success": True,
                    "result": result
                })

            except Exception as e:
                results.append({
                    "tool": tool.name,
                    "success": False,
                    "error": str(e)
                })

        return results

    async def synthesize_response(self, user_input: str, analysis: Dict[str, Any],
                                context: str, tool_results: List[Dict[str, Any]]) -> str:
        """Synthesize final response from all components."""

        # Build synthesis prompt
        synthesis_prompt = f"""
        Based on the following information, provide a comprehensive response to: {user_input}

        Request Analysis: {json.dumps(analysis)}

        Context: {context}

        Tool Results: {json.dumps(tool_results)}

        Instructions: {self.agent.instructions}

        Provide a clear, helpful response that addresses the user's needs.
        """

        # Generate final response
        response = await self.agent.model.generate(synthesis_prompt)

        # Update memory
        if self.agent.memory:
            self.agent.memory.add_message("user", user_input)
            self.agent.memory.add_message("assistant", response)

        return response

    def prepare_tool_input(self, tool: Tool, user_input: str, context: str) -> Dict[str, Any]:
        """Prepare appropriate input for a tool."""

        # This would be more sophisticated in practice
        # For now, pass the user input
        return {"query": user_input, "context": context}
```

## Modular Component System

### Tool Integration Architecture

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseTool(ABC):
    """Base class for all Phidata tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.capabilities = []
        self.parameters = {}

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """Execute the tool."""
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for LLM function calling."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.parameters,
                "required": [k for k, v in self.parameters.items() if v.get("required", False)]
            }
        }

class WebSearchTool(BaseTool):
    """Tool for web searching."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information"
        )

        self.capabilities = ["search", "research", "information_gathering"]
        self.parameters = {
            "query": {
                "type": "string",
                "description": "Search query",
                "required": True
            },
            "num_results": {
                "type": "integer",
                "description": "Number of results to return",
                "default": 5
            }
        }

    async def run(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Perform web search."""
        # Implementation would use search API
        return {
            "query": query,
            "results": [
                {"title": f"Result {i+1}", "url": f"https://example.com/{i+1}"}
                for i in range(num_results)
            ]
        }

class CalculatorTool(BaseTool):
    """Tool for mathematical calculations."""

    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations"
        )

        self.capabilities = ["calculation", "math", "computation"]
        self.parameters = {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate",
                "required": True
            }
        }

    async def run(self, expression: str) -> Dict[str, Any]:
        """Evaluate mathematical expression."""
        try:
            # Safe evaluation
            result = eval(expression, {"__builtins__": {}}, {})
            return {"result": result, "expression": expression}
        except Exception as e:
            return {"error": str(e), "expression": expression}

# Tool registry and management
class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}

    def register_tool(self, tool: BaseTool):
        """Register a tool."""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name."""
        return self.tools.get(name)

    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self.tools.values())

    def get_tools_by_capability(self, capability: str) -> List[BaseTool]:
        """Get tools that have specific capability."""
        return [
            tool for tool in self.tools.values()
            if capability in tool.capabilities
        ]

# Usage
registry = ToolRegistry()

# Register tools
registry.register_tool(WebSearchTool())
registry.register_tool(CalculatorTool())

# Get tools for research
research_tools = registry.get_tools_by_capability("search")
print(f"Available search tools: {[t.name for t in research_tools]}")
```

## Memory Systems

### Memory Architecture

```python
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

class BaseMemory(ABC):
    """Base class for memory systems."""

    @abstractmethod
    def add_message(self, role: str, content: str):
        """Add message to memory."""
        pass

    @abstractmethod
    def get_context(self, query: str = None) -> str:
        """Get relevant context."""
        pass

    @abstractmethod
    def clear(self):
        """Clear memory."""
        pass

class BufferMemory(BaseMemory):
    """Simple buffer memory with token limit."""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.messages: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str):
        """Add message with token counting."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tokens": self._estimate_tokens(content)
        }

        self.messages.append(message)
        self._prune_memory()

    def get_context(self, query: str = None) -> str:
        """Get recent messages as context."""
        # Return last N messages that fit in token limit
        context_messages = []
        total_tokens = 0

        for msg in reversed(self.messages):
            if total_tokens + msg["tokens"] > self.max_tokens:
                break
            context_messages.insert(0, msg)
            total_tokens += msg["tokens"]

        return self._format_messages(context_messages)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        return len(text.split()) * 1.3  # 30% overhead for punctuation/subwords

    def _prune_memory(self):
        """Remove old messages to stay within token limit."""
        while self._total_tokens() > self.max_tokens and len(self.messages) > 1:
            self.messages.pop(0)

    def _total_tokens(self) -> int:
        """Get total tokens in memory."""
        return sum(msg["tokens"] for msg in self.messages)

    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for context."""
        formatted = []
        for msg in messages:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)

    def clear(self):
        """Clear all messages."""
        self.messages = []

class SummaryMemory(BaseMemory):
    """Memory that maintains conversation summaries."""

    def __init__(self, summarizer_model=None):
        self.messages: List[Dict[str, Any]] = []
        self.summary = ""
        self.summarizer = summarizer_model

    def add_message(self, role: str, content: str):
        """Add message and update summary periodically."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        self.messages.append(message)

        # Update summary every 10 messages
        if len(self.messages) % 10 == 0:
            self._update_summary()

    def get_context(self, query: str = None) -> str:
        """Get context with summary."""
        context_parts = []

        if self.summary:
            context_parts.append(f"Conversation summary: {self.summary}")

        # Add recent messages
        recent_messages = self.messages[-5:]  # Last 5 messages
        if recent_messages:
            formatted_recent = self._format_messages(recent_messages)
            context_parts.append(f"Recent messages:\n{formatted_recent}")

        return "\n\n".join(context_parts)

    def _update_summary(self):
        """Update conversation summary."""
        if not self.summarizer:
            # Simple concatenation if no summarizer
            all_content = " ".join([msg["content"] for msg in self.messages])
            self.summary = all_content[:500] + "..." if len(all_content) > 500 else all_content
            return

        # Use summarizer model
        conversation_text = self._format_messages(self.messages)

        summary_prompt = f"""
        Summarize the following conversation, capturing the main topics,
        decisions, and current state:

        {conversation_text}

        Summary:
        """

        self.summary = self.summarizer.generate(summary_prompt)

    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for display."""
        formatted = []
        for msg in messages:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)

    def clear(self):
        """Clear memory."""
        self.messages = []
        self.summary = ""
```

## Knowledge Base Integration

### Knowledge Component Architecture

```python
from typing import List, Dict, Any
import numpy as np

class KnowledgeBase:
    """Knowledge base for agent information retrieval."""

    def __init__(self, vector_store=None, embedding_model=None):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.documents = []

    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """Add document to knowledge base."""
        doc = {
            "content": content,
            "metadata": metadata or {},
            "id": f"doc_{len(self.documents)}",
            "chunks": self._chunk_document(content)
        }

        self.documents.append(doc)

        # Generate embeddings if available
        if self.embedding_model and self.vector_store:
            self._embed_and_store(doc)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant information."""
        if not self.embedding_model or not self.vector_store:
            # Fallback to simple text search
            return self._text_search(query, top_k)

        # Vector search
        query_embedding = self.embedding_model.encode(query)
        results = self.vector_store.search(query_embedding, top_k=top_k)

        return [
            {
                "content": result["content"],
                "metadata": result["metadata"],
                "score": result["score"]
            }
            for result in results
        ]

    def _chunk_document(self, content: str, chunk_size: int = 1000) -> List[str]:
        """Split document into chunks."""
        words = content.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def _embed_and_store(self, document: Dict[str, Any]):
        """Generate embeddings and store in vector database."""
        for chunk in document["chunks"]:
            embedding = self.embedding_model.encode(chunk)
            self.vector_store.add({
                "content": chunk,
                "metadata": {
                    **document["metadata"],
                    "document_id": document["id"]
                },
                "embedding": embedding
            })

    def _text_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Simple text-based search fallback."""
        results = []

        for doc in self.documents:
            if query.lower() in doc["content"].lower():
                results.append({
                    "content": doc["content"][:500] + "...",
                    "metadata": doc["metadata"],
                    "score": 1.0  # Simple binary score
                })

        return results[:top_k]
```

## Agent Orchestration

### Agent Runner and Scheduler

```python
import asyncio
from typing import Dict, List, Any
from datetime import datetime

class AgentOrchestrator:
    """Orchestrates multiple agents and their interactions."""

    def __init__(self):
        self.agents: Dict[str, PhidataAgent] = {}
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.event_queue = asyncio.Queue()

    def register_agent(self, agent: PhidataAgent):
        """Register an agent."""
        self.agents[agent.name] = agent

    def submit_task(self, task: Dict[str, Any]) -> str:
        """Submit task for execution."""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(task))}"

        self.tasks[task_id] = {
            "task": task,
            "status": "pending",
            "created_at": datetime.now(),
            "assigned_agent": None,
            "result": None
        }

        # Add to event queue
        asyncio.create_task(self.event_queue.put({
            "type": "task_submitted",
            "task_id": task_id
        }))

        return task_id

    async def process_events(self):
        """Process events from the queue."""
        while True:
            event = await self.event_queue.get()

            if event["type"] == "task_submitted":
                await self._assign_task(event["task_id"])

            self.event_queue.task_done()

    async def _assign_task(self, task_id: str):
        """Assign task to appropriate agent."""
        task_info = self.tasks[task_id]
        task = task_info["task"]

        # Simple agent selection (would be more sophisticated)
        agent_name = task.get("preferred_agent", "default_agent")

        if agent_name in self.agents:
            task_info["assigned_agent"] = agent_name
            task_info["status"] = "running"

            # Execute task asynchronously
            asyncio.create_task(self._execute_task(task_id))

    async def _execute_task(self, task_id: str):
        """Execute assigned task."""
        task_info = self.tasks[task_id]
        agent = self.agents[task_info["assigned_agent"]]

        try:
            # Execute task
            result = await agent.run(task_info["task"]["description"])

            # Update task status
            task_info["status"] = "completed"
            task_info["result"] = result
            task_info["completed_at"] = datetime.now()

        except Exception as e:
            task_info["status"] = "failed"
            task_info["error"] = str(e)

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status."""
        return self.tasks.get(task_id, {"error": "Task not found"})

    def list_agents(self) -> List[str]:
        """List registered agents."""
        return list(self.agents.keys())

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get agent status."""
        agent = self.agents.get(agent_name)
        if not agent:
            return {"error": "Agent not found"}

        return {
            "name": agent.name,
            "model": str(agent.model),
            "run_count": getattr(agent, 'run_count', 0),
            "active": True
        }

# Usage
orchestrator = AgentOrchestrator()

# Register agents
orchestrator.register_agent(my_agent)

# Start event processing
asyncio.create_task(orchestrator.process_events())

# Submit tasks
task_id = orchestrator.submit_task({
    "description": "Analyze this quarter's sales data",
    "preferred_agent": "analyst_agent"
})

# Check status
status = orchestrator.get_task_status(task_id)
print(f"Task status: {status['status']}")
```

This comprehensive architecture breakdown shows how Phidata agents are composed of modular components that work together to provide intelligent, autonomous behavior. The next chapter explores tools and functions in detail. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `agent`, `tool` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Understanding Phidata Agent Architecture` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Dict`, `tools`, `content` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Understanding Phidata Agent Architecture` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `agent` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `tool`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `agent` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Phidata Agents](01-getting-started.md)
- [Next Chapter: Chapter 3: Tools & Functions - Extending Agent Capabilities](03-tools-functions.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
