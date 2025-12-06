---
layout: default
title: "Pydantic AI Tutorial - Chapter 5: Streaming & Async Operations"
nav_order: 5
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 5: Streaming Responses & Async Operations

> Master real-time streaming, asynchronous processing, and concurrent operations for high-performance Pydantic AI applications.

## Basic Streaming

### Text Streaming

```python
from pydantic_ai import Agent
import asyncio

# Create agent with streaming enabled
streaming_agent = Agent('openai:gpt-4')

async def basic_streaming():
    """Demonstrate basic text streaming."""

    print("Streaming response: ", end="", flush=True)

    # Stream the response
    async with streaming_agent.run_stream('Write a short story about a robot learning to paint') as stream:
        async for message in stream:
            print(message, end="", flush=True)

    print("\n\n--- Streaming complete ---")

# Run streaming example
asyncio.run(basic_streaming())
```

### Structured Output Streaming

```python
from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent

class BlogPost(BaseModel):
    title: str
    content: str = Field(..., min_length=100)
    tags: List[str] = Field(..., min_items=1, max_items=5)

# Agent with structured streaming output
structured_agent = Agent('openai:gpt-4', result_type=BlogPost)

async def structured_streaming():
    """Stream structured output generation."""

    print("Generating structured blog post...\n")

    # For structured outputs, we get the complete result
    # (streaming works differently for validated outputs)
    result = await structured_agent.run('Write a blog post about AI ethics')

    print("Generated Blog Post:")
    print(f"Title: {result.data.title}")
    print(f"Tags: {', '.join(result.data.tags)}")
    print(f"Content length: {len(result.data.content)} characters")
    print(f"Content preview: {result.data.content[:200]}...")

# Run structured streaming
asyncio.run(structured_streaming())
```

## Advanced Streaming Patterns

### Streaming with Progress Updates

```python
import time
from typing import Dict, Any

class StreamingProgressTracker:
    """Track progress during streaming operations."""

    def __init__(self):
        self.start_time = None
        self.tokens_received = 0
        self.last_update = 0

    def start(self):
        """Start tracking."""
        self.start_time = time.time()
        print("🚀 Starting streaming operation...")

    def update(self, new_text: str):
        """Update progress with new text."""
        self.tokens_received += len(new_text.split())
        current_time = time.time()

        # Update progress every 0.5 seconds
        if current_time - self.last_update > 0.5:
            elapsed = current_time - self.start_time
            rate = self.tokens_received / elapsed if elapsed > 0 else 0

            print(f"📊 Progress: {self.tokens_received} tokens received, "
                  f"{rate:.1f} tokens/sec", end="\r")

            self.last_update = current_time

    def finish(self):
        """Finish tracking."""
        total_time = time.time() - self.start_time
        final_rate = self.tokens_received / total_time if total_time > 0 else 0

        print(f"\n✅ Streaming complete!")
        print(f"📈 Final stats: {self.tokens_received} tokens in {total_time:.2f}s "
              f"({final_rate:.1f} tokens/sec)")

async def streaming_with_progress():
    """Stream with detailed progress tracking."""

    progress_tracker = StreamingProgressTracker()
    progress_tracker.start()

    agent = Agent('openai:gpt-4')

    async with agent.run_stream('Write a comprehensive guide about machine learning algorithms') as stream:
        async for message in stream:
            progress_tracker.update(message)
            print(message, end="", flush=True)

    progress_tracker.finish()

# Run progress tracking
asyncio.run(streaming_with_progress())
```

### Multiple Stream Processing

```python
async def parallel_streaming():
    """Process multiple streams concurrently."""

    agents = [
        Agent('openai:gpt-4'),
        Agent('anthropic:claude-3-haiku-20240307'),
        Agent('google:gemini-1.5-flash')
    ]

    prompt = "Explain the benefits of renewable energy in 3 paragraphs"

    async def stream_from_agent(agent: Agent, agent_name: str):
        """Stream from a specific agent."""
        print(f"\n🔄 Starting {agent_name} stream:")

        try:
            async with agent.run_stream(prompt) as stream:
                content = ""
                async for message in stream:
                    content += message
                    print(f"{agent_name[:3]}: {message[:50]}...", end="\r")

                return {"agent": agent_name, "content": content, "success": True}

        except Exception as e:
            return {"agent": agent_name, "error": str(e), "success": False}

    # Start all streams concurrently
    tasks = [stream_from_agent(agent, f"Agent_{i+1}") for i, agent in enumerate(agents)]
    results = await asyncio.gather(*tasks)

    # Display results
    print("\n\n📋 Streaming Results Summary:")
    for result in results:
        if result["success"]:
            content_length = len(result["content"])
            print(f"✅ {result['agent']}: {content_length} characters generated")
        else:
            print(f"❌ {result['agent']}: Failed - {result['error']}")

# Run parallel streaming
asyncio.run(parallel_streaming())
```

## Async Agent Operations

### Concurrent Agent Execution

```python
async def concurrent_agents():
    """Run multiple agents concurrently on different tasks."""

    # Different agents for different tasks
    agents = {
        "creative": Agent('openai:gpt-4', system_prompt="You are a creative writer."),
        "technical": Agent('anthropic:claude-3-sonnet-20240229', system_prompt="You are a technical expert."),
        "analytical": Agent('google:gemini-1.5-pro', system_prompt="You are a data analyst.")
    }

    tasks = [
        ("creative", "Write a short poem about artificial intelligence"),
        ("technical", "Explain how neural networks work"),
        ("analytical", "Analyze the trend of renewable energy adoption")
    ]

    async def process_task(agent_key: str, prompt: str):
        """Process a single task with appropriate agent."""
        agent = agents[agent_key]

        start_time = time.time()
        result = await agent.run(prompt)
        duration = time.time() - start_time

        return {
            "task_type": agent_key,
            "prompt": prompt,
            "result": result.data,
            "duration": duration,
            "agent": agent_key
        }

    # Execute all tasks concurrently
    concurrent_tasks = [process_task(agent_key, prompt) for agent_key, prompt in tasks]
    results = await asyncio.gather(*concurrent_tasks)

    # Display results
    print("🎯 Concurrent Agent Results:")
    for result in results:
        print(f"\n{result['task_type'].title()} Task ({result['duration']:.2f}s):")
        print(f"Prompt: {result['prompt']}")
        print(f"Response: {result['result'][:150]}...")
        print("-" * 80)

# Run concurrent agents
asyncio.run(concurrent_agents())
```

### Async Tool Execution

```python
from pydantic_ai import tool, Agent
import asyncio
import aiohttp
from typing import Dict, Any, List

# Async tool definitions
@tool
async def async_web_search(query: str, num_results: int = 3) -> Dict[str, Any]:
    """
    Perform asynchronous web search.

    Args:
        query: Search query
        num_results: Number of results to return

    Returns:
        Search results
    """
    # Simulate async web search
    await asyncio.sleep(0.5)  # Simulate network delay

    mock_results = [
        {
            "title": f"Result {i+1} for {query}",
            "url": f"https://example.com/{i+1}",
            "snippet": f"Relevant information about {query}"
        }
        for i in range(num_results)
    ]

    return {
        "query": query,
        "results": mock_results,
        "total_found": len(mock_results)
    }

@tool
async def async_api_call(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make asynchronous API call.

    Args:
        endpoint: API endpoint URL
        method: HTTP method
        data: Request data for POST/PUT

    Returns:
        API response
    """
    try:
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(endpoint) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}

            elif method.upper() == "POST":
                async with session.post(endpoint, json=data) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}

    except Exception as e:
        return {"error": str(e), "status": 500}

# Agent with async tools
async_agent = Agent(
    'openai:gpt-4',
    tools=[async_web_search, async_api_call]
)

async def async_tool_demo():
    """Demonstrate async tool usage."""

    queries = [
        "Search for latest AI developments",
        "Make API call to get weather data",
        "Search for Python tutorials"
    ]

    print("🔄 Executing async tool operations:")

    for query in queries:
        print(f"\nQuery: {query}")

        start_time = time.time()
        result = await async_agent.run(query)
        duration = time.time() - start_time

        print(f"Duration: {duration:.2f}s")
        print(f"Result: {result.data[:200]}...")
        print("-" * 60)

# Run async tool demo
asyncio.run(async_tool_demo())
```

## Streaming with Error Handling

### Robust Streaming Implementation

```python
class RobustStreamer:
    """Robust streaming with error handling and recovery."""

    def __init__(self, agent: Agent, max_retries: int = 3):
        self.agent = agent
        self.max_retries = max_retries

    async def stream_with_retry(self, prompt: str) -> str:
        """Stream with automatic retry on failures."""

        last_error = None

        for attempt in range(self.max_retries):
            try:
                print(f"🚀 Attempt {attempt + 1}: Starting stream...")

                full_response = ""
                chunk_count = 0

                async with self.agent.run_stream(prompt) as stream:
                    async for message in stream:
                        full_response += message
                        chunk_count += 1

                        # Progress indicator
                        if chunk_count % 10 == 0:
                            print(f"📦 Received {chunk_count} chunks, "
                                  f"{len(full_response)} characters...")

                print(f"✅ Stream completed successfully on attempt {attempt + 1}")
                return full_response

            except Exception as e:
                last_error = e
                print(f"❌ Attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    # Wait before retry with exponential backoff
                    wait_time = 2 ** attempt
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    print("💥 All retry attempts exhausted")

        raise RuntimeError(f"Streaming failed after {self.max_retries} attempts. "
                          f"Last error: {last_error}")

    async def stream_with_timeout(self, prompt: str, timeout: float = 30.0) -> str:
        """Stream with timeout protection."""

        async def stream_with_timeout_inner():
            return await self.stream_with_retry(prompt)

        try:
            return await asyncio.wait_for(stream_with_timeout_inner(), timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Streaming timed out after {timeout} seconds")

# Robust streaming demo
robust_streamer = RobustStreamer(Agent('openai:gpt-4'))

async def robust_streaming_demo():
    """Demonstrate robust streaming."""

    test_prompts = [
        "Write a detailed explanation of quantum computing",
        "Create a comprehensive business plan outline",
        "Write a technical specification for a web API"
    ]

    for prompt in test_prompts:
        print(f"\n🎯 Streaming: {prompt[:50]}...")

        try:
            start_time = time.time()
            result = await robust_streamer.stream_with_timeout(prompt, timeout=60.0)
            duration = time.time() - start_time

            print(f"✅ Success! Generated {len(result)} characters in {duration:.2f}s")
            print(f"Preview: {result[:150]}...")

        except Exception as e:
            print(f"❌ Failed: {e}")

        print("-" * 80)

# Run robust streaming demo
asyncio.run(robust_streaming_demo())
```

## Advanced Async Patterns

### Agent Pipelines

```python
from typing import List, Dict, Any, Callable
import asyncio

class AgentPipeline:
    """Pipeline for chaining async agent operations."""

    def __init__(self):
        self.stages: List[Dict[str, Any]] = []

    def add_stage(self, name: str, agent: Agent, processor: Callable[[str], str] = None):
        """Add a processing stage to the pipeline."""

        self.stages.append({
            "name": name,
            "agent": agent,
            "processor": processor
        })

    async def execute_pipeline(self, initial_input: str) -> Dict[str, Any]:
        """Execute the entire pipeline asynchronously."""

        current_input = initial_input
        execution_log = []

        print("🔄 Starting agent pipeline execution...")

        for i, stage in enumerate(self.stages, 1):
            stage_name = stage["name"]
            agent = stage["agent"]
            processor = stage["processor"]

            print(f"📍 Stage {i}: {stage_name}")

            # Pre-process input if processor provided
            if processor:
                processed_input = processor(current_input)
                print(f"   🔧 Pre-processed input: {len(processed_input)} chars")
            else:
                processed_input = current_input

            # Execute agent
            start_time = time.time()
            result = await agent.run(processed_input)
            duration = time.time() - start_time

            # Log execution
            stage_result = {
                "stage": i,
                "name": stage_name,
                "input": processed_input,
                "output": result.data,
                "duration": duration
            }
            execution_log.append(stage_result)

            print(f"   ✅ Completed in {duration:.2f}s")
            print(f"   📊 Output length: {len(result.data)} chars")

            # Pass output to next stage
            current_input = result.data

        return {
            "final_output": current_input,
            "execution_log": execution_log,
            "total_stages": len(self.stages),
            "total_time": sum(log["duration"] for log in execution_log)
        }

# Create agent pipeline
pipeline = AgentPipeline()

# Add stages
pipeline.add_stage(
    "research",
    Agent('openai:gpt-4', system_prompt="You are a research specialist. Gather comprehensive information."),
    lambda x: f"Research this topic thoroughly: {x}"
)

pipeline.add_stage(
    "analyze",
    Agent('anthropic:claude-3-sonnet-20240229', system_prompt="You are an analyst. Provide deep insights and patterns."),
    lambda x: f"Analyze this research data and extract key insights: {x}"
)

pipeline.add_stage(
    "summarize",
    Agent('google:gemini-1.5-flash', system_prompt="You are a summarizer. Create concise, clear summaries."),
    lambda x: f"Create a comprehensive but concise summary: {x}"
)

async def pipeline_demo():
    """Demonstrate agent pipeline."""

    topic = "The impact of artificial intelligence on healthcare"

    print(f"🎯 Pipeline Topic: {topic}")

    result = await pipeline.execute_pipeline(topic)

    print("
📋 Pipeline Results:"    print(f"Total stages: {result['total_stages']}")
    print(f"Total time: {result['total_time']:.2f}s")
    print(f"Average stage time: {result['total_time']/result['total_stages']:.2f}s")

    print("
📝 Final Output:"    print(result['final_output'])

    print("
📊 Stage Details:"    for log in result['execution_log']:
        print(f"  Stage {log['stage']} ({log['name']}): {log['duration']:.2f}s")

# Run pipeline demo
asyncio.run(pipeline_demo())
```

### Concurrent Agent Teams

```python
class AgentTeam:
    """Team of agents working concurrently on subtasks."""

    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents

    async def execute_team_task(self, main_task: str, subtasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a complex task by dividing it among team members.

        Args:
            main_task: The overall task description
            subtasks: List of subtasks with agent assignment

        Returns:
            Combined team results
        """

        print(f"🎯 Team Task: {main_task}")
        print(f"👥 Team size: {len(self.agents)} agents")

        # Execute subtasks concurrently
        async def execute_subtask(subtask: Dict[str, Any]):
            """Execute a single subtask."""
            agent_name = subtask["agent"]
            task_description = subtask["description"]

            agent = self.agents.get(agent_name)
            if not agent:
                return {"error": f"Agent {agent_name} not found", "subtask": subtask}

            # Enhance prompt with context
            enhanced_prompt = f"""
            Main Task: {main_task}

            Your Subtask: {task_description}

            Provide detailed, focused work on your assigned subtask.
            """

            start_time = time.time()
            result = await agent.run(enhanced_prompt)
            duration = time.time() - start_time

            return {
                "agent": agent_name,
                "subtask": task_description,
                "result": result.data,
                "duration": duration
            }

        # Execute all subtasks concurrently
        tasks = [execute_subtask(subtask) for subtask in subtasks]
        subtask_results = await asyncio.gather(*tasks)

        # Synthesize team results
        synthesis_agent = Agent('openai:gpt-4', system_prompt="You are a team coordinator. Synthesize diverse contributions into coherent results.")

        synthesis_prompt = f"""
        Main Task: {main_task}

        Team Contributions:
        {chr(10).join([f"• {result['agent']}: {result['result'][:200]}..." for result in subtask_results if 'result' in result])}

        Synthesize all contributions into a comprehensive, coherent final result.
        Ensure all perspectives are represented and integrated.
        """

        synthesis_result = await synthesis_agent.run(synthesis_prompt)

        return {
            "main_task": main_task,
            "subtask_results": subtask_results,
            "synthesized_result": synthesis_result.data,
            "team_size": len(self.agents),
            "total_subtasks": len(subtasks)
        }

# Create agent team
team_agents = {
    "researcher": Agent('openai:gpt-4', system_prompt="Research specialist focusing on data gathering."),
    "analyst": Agent('anthropic:claude-3-sonnet-20240229', system_prompt="Data analyst specializing in insights and patterns."),
    "writer": Agent('google:gemini-1.5-pro', system_prompt="Content writer creating clear, engaging text."),
    "reviewer": Agent('groq:mixtral-8x7b-32768', system_prompt="Critical reviewer ensuring quality and accuracy.")
}

agent_team = AgentTeam(team_agents)

# Define team task
main_task = "Create a comprehensive report on sustainable energy solutions"

subtasks = [
    {"agent": "researcher", "description": "Research current sustainable energy technologies and trends"},
    {"agent": "analyst", "description": "Analyze the economic and environmental impact of different solutions"},
    {"agent": "writer", "description": "Write engaging content about the most promising solutions"},
    {"agent": "reviewer", "description": "Review and validate all information for accuracy and completeness"}
]

async def team_execution_demo():
    """Demonstrate team execution."""

    result = await agent_team.execute_team_task(main_task, subtasks)

    print("
🏆 Team Execution Results:"    print(f"Main Task: {result['main_task']}")
    print(f"Team Size: {result['team_size']} agents")
    print(f"Subtasks Completed: {result['total_subtasks']}")

    print("
👥 Agent Contributions:"    for sub_result in result['subtask_results']:
        if 'result' in sub_result:
            print(f"• {sub_result['agent']}: {len(sub_result['result'])} chars "
                  f"({sub_result['duration']:.2f}s)")

    print("
📄 Final Synthesized Report:"    print(result['synthesized_result'][:500] + "...")

# Run team execution demo
asyncio.run(team_execution_demo())
```

## Streaming Performance Optimization

### Batched Streaming

```python
class BatchStreamer:
    """Stream multiple requests in optimized batches."""

    def __init__(self, agent: Agent, batch_size: int = 3):
        self.agent = agent
        self.batch_size = batch_size

    async def stream_batch(self, prompts: List[str]) -> List[str]:
        """Stream multiple prompts efficiently."""

        results = []

        # Process in batches
        for i in range(0, len(prompts), self.batch_size):
            batch = prompts[i:i + self.batch_size]
            print(f"🎯 Processing batch {i//self.batch_size + 1} ({len(batch)} prompts)")

            # Process batch concurrently
            batch_tasks = [self._stream_single_prompt(prompt) for prompt in batch]
            batch_results = await asyncio.gather(*batch_tasks)

            results.extend(batch_results)

            # Small delay between batches to prevent rate limiting
            if i + self.batch_size < len(prompts):
                await asyncio.sleep(1)

        return results

    async def _stream_single_prompt(self, prompt: str) -> str:
        """Stream a single prompt with error handling."""

        try:
            full_response = ""
            async with self.agent.run_stream(prompt) as stream:
                async for message in stream:
                    full_response += message

            return full_response

        except Exception as e:
            return f"Error: {str(e)}"

# Batch streaming demo
batch_streamer = BatchStreamer(Agent('openai:gpt-4'), batch_size=2)

async def batch_streaming_demo():
    """Demonstrate batch streaming."""

    prompts = [
        "Explain machine learning in simple terms",
        "Write a haiku about programming",
        "Describe the water cycle",
        "What are cloud computing benefits?",
        "Explain recursion with an example"
    ]

    print(f"🚀 Streaming {len(prompts)} prompts in batches...")

    start_time = time.time()
    results = await batch_streamer.stream_batch(prompts)
    total_time = time.time() - start_time

    print("
📊 Batch Streaming Results:"    print(f"Total prompts: {len(prompts)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per prompt: {total_time/len(prompts):.2f}s")
    print(f"Throughput: {len(prompts)/total_time:.2f} prompts/sec")

    print("
📝 Sample Results:"    for i, (prompt, result) in enumerate(zip(prompts, results)):
        print(f"{i+1}. {prompt}")
        print(f"   Response: {result[:100]}...")
        print()

# Run batch streaming demo
asyncio.run(batch_streaming_demo())
```

This comprehensive streaming and async chapter demonstrates advanced patterns for real-time response generation, concurrent processing, and high-performance agent operations. 🚀