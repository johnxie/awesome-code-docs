---
layout: default
title: "Pydantic AI Tutorial - Chapter 4: Dependencies & Tools"
nav_order: 4
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 4: Dependencies, Tools & External Integrations

> Extend Pydantic AI agents with custom tools, dependencies, and external service integrations for comprehensive task completion.

## Tool System Architecture

### Custom Tool Creation

```python
from pydantic_ai import Agent, tool
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import requests
import json
from datetime import datetime

# Define tool result models
class WeatherResult(BaseModel):
    location: str
    temperature: float
    condition: str
    humidity: int
    timestamp: datetime

class SearchResult(BaseModel):
    query: str
    results: List[Dict[str, str]]
    total_results: int

class CalculatorResult(BaseModel):
    expression: str
    result: float
    steps: List[str]

# Weather tool
@tool
def get_weather(location: str) -> WeatherResult:
    """
    Get current weather for a location.

    Args:
        location: City name or coordinates

    Returns:
        Weather information
    """
    # Mock weather API call (replace with real API)
    mock_weather = {
        "New York": {"temp": 22.5, "condition": "Sunny", "humidity": 45},
        "London": {"temp": 15.2, "condition": "Cloudy", "humidity": 72},
        "Tokyo": {"temp": 28.1, "condition": "Rainy", "humidity": 85}
    }

    weather_data = mock_weather.get(location.title(), {"temp": 20.0, "condition": "Unknown", "humidity": 50})

    return WeatherResult(
        location=location,
        temperature=weather_data["temp"],
        condition=weather_data["condition"],
        humidity=weather_data["humidity"],
        timestamp=datetime.now()
    )

# Web search tool
@tool
def web_search(query: str, num_results: int = 5) -> SearchResult:
    """
    Search the web for information.

    Args:
        query: Search query
        num_results: Number of results to return

    Returns:
        Search results
    """
    # Mock search results (replace with real search API)
    mock_results = [
        {"title": f"Result 1 for {query}", "url": f"https://example.com/1?q={query}", "snippet": f"First result about {query}"},
        {"title": f"Result 2 for {query}", "url": f"https://example.com/2?q={query}", "snippet": f"Second result about {query}"},
        {"title": f"Result 3 for {query}", "url": f"https://example.com/3?q={query}", "snippet": f"Third result about {query}"}
    ]

    return SearchResult(
        query=query,
        results=mock_results[:num_results],
        total_results=len(mock_results)
    )

# Calculator tool
@tool
def calculate(expression: str) -> CalculatorResult:
    """
    Calculate mathematical expressions safely.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Calculation result with steps
    """
    try:
        # Safe evaluation
        allowed_names = {
            k: v for k, v in __import__('math').__dict__.items()
            if not k.startswith("__")
        }

        # Basic validation
        if not all(c in "0123456789+-*/(). sqrt()cos()sin()tan()log()exp()pie " for c in expression):
            raise ValueError("Invalid characters in expression")

        result = eval(expression, {"__builtins__": {}}, allowed_names)

        return CalculatorResult(
            expression=expression,
            result=float(result),
            steps=[f"Evaluated: {expression} = {result}"]
        )

    except Exception as e:
        return CalculatorResult(
            expression=expression,
            result=0.0,
            steps=[f"Error: {str(e)}"]
        )

# Create agent with tools
tool_agent = Agent(
    'openai:gpt-4',
    tools=[get_weather, web_search, calculate]
)

# Test tool usage
result = tool_agent.run_sync("What's the weather like in Tokyo and calculate 15 * 23?")

print("Agent with tools:")
print(result.data)
```

### Tool Dependencies and Context

```python
from pydantic_ai import Agent, tool, RunContext
from typing import Dict, Any, List

# Tool with context awareness
@tool
def search_user_history(ctx: RunContext[Dict[str, Any]], query: str) -> str:
    """
    Search user's conversation history.

    Args:
        ctx: Run context containing user data
        query: Search query

    Returns:
        Relevant history information
    """
    user_data = ctx.deps
    history = user_data.get("conversation_history", [])

    # Simple keyword search
    relevant_messages = []
    for msg in history:
        if query.lower() in msg.get("content", "").lower():
            relevant_messages.append(msg)

    if relevant_messages:
        return f"Found {len(relevant_messages)} relevant messages: " + \
               ", ".join([msg["content"][:50] + "..." for msg in relevant_messages])
    else:
        return f"No relevant history found for: {query}"

@tool
def save_user_preference(ctx: RunContext[Dict[str, Any]], key: str, value: str) -> str:
    """
    Save user preference.

    Args:
        ctx: Run context
        key: Preference key
        value: Preference value

    Returns:
        Confirmation message
    """
    user_data = ctx.deps
    preferences = user_data.setdefault("preferences", {})
    preferences[key] = value

    return f"Saved preference: {key} = {value}"

# Agent with context-aware tools
context_agent = Agent(
    'openai:gpt-4',
    deps_type=Dict[str, Any],  # Type of dependencies
    tools=[search_user_history, save_user_preference]
)

# Run with context
user_context = {
    "user_id": "user123",
    "conversation_history": [
        {"role": "user", "content": "I like Python programming"},
        {"role": "user", "content": "My favorite color is blue"},
        {"role": "user", "content": "I work as a software engineer"}
    ],
    "preferences": {}
}

result = context_agent.run_sync(
    "What did I say about my favorite color? Also save that I prefer dark mode.",
    deps=user_context
)

print("Context-aware agent result:")
print(result.data)

print("Updated user context:")
print(json.dumps(user_context, indent=2))
```

## Advanced Tool Patterns

### Tool Chaining and Dependencies

```python
from pydantic_ai import Agent, tool, RunContext
from typing import List, Dict, Any, Optional

class ToolChain:
    """Chain multiple tools together."""

    def __init__(self):
        self.tools = {}
        self.dependencies = {}

    def add_tool(self, name: str, tool_func, depends_on: Optional[List[str]] = None):
        """Add a tool to the chain."""
        self.tools[name] = tool_func
        self.dependencies[name] = depends_on or []

    def get_execution_order(self, required_tools: List[str]) -> List[str]:
        """Get execution order respecting dependencies."""
        # Simple topological sort (could be enhanced)
        ordered = []
        remaining = required_tools.copy()

        while remaining:
            for tool in remaining[:]:
                deps = self.dependencies.get(tool, [])
                if all(dep in ordered for dep in deps):
                    ordered.append(tool)
                    remaining.remove(tool)
                    break
            else:
                raise ValueError("Circular dependency detected")

        return ordered

# Define chained tools
@tool
def research_topic(ctx: RunContext[Dict[str, Any]], topic: str) -> Dict[str, Any]:
    """Research a topic."""
    print(f"🔍 Researching: {topic}")

    # Simulate research
    research_data = {
        "topic": topic,
        "key_points": [
            f"Point 1 about {topic}",
            f"Point 2 about {topic}",
            f"Point 3 about {topic}"
        ],
        "sources": ["source1.com", "source2.com"]
    }

    # Store in context for dependent tools
    ctx.deps["research_data"] = research_data

    return research_data

@tool
def analyze_research(ctx: RunContext[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze research data (depends on research_topic)."""
    research_data = ctx.deps.get("research_data")
    if not research_data:
        return {"error": "No research data available"}

    print("📊 Analyzing research data")

    analysis = {
        "summary": f"Analysis of {research_data['topic']}",
        "insights": [
            "Key insight 1",
            "Key insight 2",
            "Important finding"
        ],
        "recommendations": ["Action 1", "Action 2"]
    }

    ctx.deps["analysis_data"] = analysis

    return analysis

@tool
def generate_report(ctx: RunContext[Dict[str, Any]]) -> str:
    """Generate final report (depends on analyze_research)."""
    analysis_data = ctx.deps.get("analysis_data")
    research_data = ctx.deps.get("research_data")

    if not analysis_data or not research_data:
        return "Missing required data for report generation"

    print("📝 Generating final report")

    report = f"""
# Research Report: {research_data['topic']}

## Key Findings
{chr(10).join(f"- {point}" for point in research_data['key_points'])}

## Analysis
{chr(10).join(f"- {insight}" for insight in analysis_data['insights'])}

## Recommendations
{chr(10).join(f"- {rec}" for rec in analysis_data['recommendations'])}

## Sources
{chr(10).join(f"- {source}" for source in research_data['sources'])}
"""

    return report.strip()

# Create agent with tool chain
chain_agent = Agent(
    'openai:gpt-4',
    deps_type=Dict[str, Any],
    tools=[research_topic, analyze_research, generate_report]
)

# Execute tool chain
result = chain_agent.run_sync(
    "Research artificial intelligence, analyze the findings, and generate a comprehensive report.",
    deps={}
)

print("Tool chain execution result:")
print(result.data[:500] + "..." if len(result.data) > 500 else result.data)
```

### Conditional Tool Execution

```python
from pydantic_ai import Agent, tool, RunContext

@tool
def check_conditions(ctx: RunContext[Dict[str, Any]], condition: str) -> bool:
    """Check if conditions are met for tool execution."""
    user_data = ctx.deps

    if condition == "premium_user":
        return user_data.get("subscription_tier") == "premium"
    elif condition == "has_history":
        return len(user_data.get("conversation_history", [])) > 0
    elif condition == "time_sensitive":
        return user_data.get("urgency_level", "normal") == "high"

    return False

@tool
def premium_analysis(ctx: RunContext[Dict[str, Any]], data: str) -> str:
    """Advanced analysis (premium feature)."""
    if not check_conditions(ctx, "premium_user"):
        return "This feature requires a premium subscription."

    return f"Premium analysis of: {data[:100]}..."

@tool
def quick_response(ctx: RunContext[Dict[str, Any]], query: str) -> str:
    """Quick response for urgent queries."""
    if check_conditions(ctx, "time_sensitive"):
        return f"URGENT: Quick response to '{query}' - Please handle immediately!"
    else:
        return f"Normal response to '{query}'"

@tool
def contextual_help(ctx: RunContext[Dict[str, Any]], topic: str) -> str:
    """Contextual help based on user history."""
    if check_conditions(ctx, "has_history"):
        history = ctx.deps.get("conversation_history", [])
        relevant_topics = [msg for msg in history if topic.lower() in msg.get("content", "").lower()]

        if relevant_topics:
            return f"Based on your history, here are relevant topics: " + \
                   ", ".join([msg["content"][:50] + "..." for msg in relevant_topics])

    return f"General help about {topic}"

# Create conditional agent
conditional_agent = Agent(
    'openai:gpt-4',
    deps_type=Dict[str, Any],
    tools=[premium_analysis, quick_response, contextual_help]
)

# Test with different user contexts
test_contexts = [
    {
        "subscription_tier": "free",
        "urgency_level": "normal",
        "conversation_history": []
    },
    {
        "subscription_tier": "premium",
        "urgency_level": "high",
        "conversation_history": [
            {"content": "I was asking about Python programming"},
            {"content": "We discussed machine learning algorithms"}
        ]
    }
]

for i, user_ctx in enumerate(test_contexts, 1):
    print(f"\nTest Context {i}:")
    print(f"  Subscription: {user_ctx['subscription_tier']}")
    print(f"  Urgency: {user_ctx['urgency_level']}")
    print(f"  History items: {len(user_ctx['conversation_history'])}")

    result = conditional_agent.run_sync(
        "Analyze this data and provide urgent help about programming",
        deps=user_ctx
    )

    print(f"  Result: {result.data[:150]}...")
```

## External API Integrations

### REST API Tools

```python
import aiohttp
from pydantic_ai import tool, Agent
from typing import Dict, Any, Optional, List

class APIToolkit:
    """Toolkit for external API integrations."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @tool
    async def api_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to API.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

            async with self.session.get(url, params=params) as response:
                data = await response.json()
                return {
                    "status": response.status,
                    "data": data,
                    "url": str(response.url)
                }

        except Exception as e:
            return {"error": str(e), "status": 500}

    @tool
    async def api_post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make POST request to API.

        Args:
            endpoint: API endpoint
            data: Request data

        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

            async with self.session.post(url, json=data) as response:
                response_data = await response.json()
                return {
                    "status": response.status,
                    "data": response_data,
                    "url": str(response.url)
                }

        except Exception as e:
            return {"error": str(e), "status": 500}

# GitHub API integration
class GitHubTools:
    """GitHub API integration tools."""

    def __init__(self, token: str):
        self.api = APIToolkit("https://api.github.com", token)

    @tool
    async def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get GitHub repository information.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository information
        """
        async with self.api:
            result = await self.api.api_get(f"repos/{owner}/{repo}")
            return result

    @tool
    async def search_repositories(self, query: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Search GitHub repositories.

        Args:
            query: Search query
            language: Programming language filter

        Returns:
            Search results
        """
        params = {"q": query}
        if language:
            params["q"] += f" language:{language}"

        async with self.api:
            result = await self.api.api_get("search/repositories", params)
            return result

    @tool
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Get GitHub user information.

        Args:
            username: GitHub username

        Returns:
            User information
        """
        async with self.api:
            result = await self.api.api_get(f"users/{username}")
            return result

# Create agent with GitHub integration
github_agent = Agent(
    'openai:gpt-4',
    tools=[
        GitHubTools(os.getenv("GITHUB_TOKEN", "your-token")).get_repo_info,
        GitHubTools(os.getenv("GITHUB_TOKEN", "your-token")).search_repositories,
        GitHubTools(os.getenv("GITHUB_TOKEN", "your-token")).get_user_info
    ]
)

# Test GitHub integration
result = github_agent.run_sync("Get information about the pydantic/pydantic-ai repository on GitHub")

print("GitHub integration result:")
print(result.data)
```

### Database Integration Tools

```python
import sqlite3
from contextlib import contextmanager
from pydantic_ai import tool, Agent
from typing import List, Dict, Any, Optional

class DatabaseTools:
    """Database integration tools."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize sample database."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT UNIQUE,
                    department TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    owner_id INTEGER,
                    status TEXT,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """)

            # Sample data
            conn.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", [
                (1, "Alice Johnson", "alice@company.com", "Engineering"),
                (2, "Bob Smith", "bob@company.com", "Marketing"),
                (3, "Carol Williams", "carol@company.com", "Sales")
            ])

    @contextmanager
    def _get_connection(self):
        """Database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @tool
    def query_database(self, sql: str) -> str:
        """
        Execute SQL query (read-only).

        Args:
            sql: SQL query to execute

        Returns:
            Query results as formatted string
        """
        try:
            # Security: only allow SELECT queries
            if not sql.strip().upper().startswith("SELECT"):
                return "Error: Only SELECT queries are allowed"

            with self._get_connection() as conn:
                cursor = conn.execute(sql)
                rows = cursor.fetchall()

                if not rows:
                    return "Query executed successfully. No results."

                # Format results
                columns = [desc[0] for desc in cursor.description]
                result = ", ".join(columns) + "\n"
                result += "\n".join(
                    ", ".join(str(row[col]) for col in columns)
                    for row in rows
                )

                return f"Query Results:\n{result}"

        except Exception as e:
            return f"Database error: {str(e)}"

    @tool
    def get_table_info(self, table_name: str) -> str:
        """
        Get information about a database table.

        Args:
            table_name: Name of the table

        Returns:
            Table schema information
        """
        try:
            with self._get_connection() as conn:
                # Get table schema
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                if not columns:
                    return f"Table '{table_name}' not found"

                schema = f"Table: {table_name}\nColumns:\n"
                for col in columns:
                    schema += f"  - {col[1]} ({col[2]})\n"

                # Get row count
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                schema += f"\nTotal rows: {row_count}"

                return schema

        except Exception as e:
            return f"Error getting table info: {str(e)}"

    @tool
    def analyze_table(self, table_name: str, column: str) -> str:
        """
        Analyze a table column with statistics.

        Args:
            table_name: Table name
            column: Column to analyze

        Returns:
            Column statistics
        """
        try:
            with self._get_connection() as conn:
                # Get statistics
                cursor = conn.execute(f"""
                    SELECT
                        COUNT(*) as total,
                        COUNT(DISTINCT {column}) as unique,
                        MIN({column}) as min_val,
                        MAX({column}) as max_val
                    FROM {table_name}
                    WHERE {column} IS NOT NULL
                """)

                stats = cursor.fetchone()

                if not stats:
                    return f"No data found in {table_name}.{column}"

                analysis = f"Analysis of {table_name}.{column}:\n"
                analysis += f"  Total values: {stats[0]}\n"
                analysis += f"  Unique values: {stats[1]}\n"
                analysis += f"  Min: {stats[2]}\n"
                analysis += f"  Max: {stats[3]}\n"

                # Get most common values
                cursor = conn.execute(f"""
                    SELECT {column}, COUNT(*) as count
                    FROM {table_name}
                    WHERE {column} IS NOT NULL
                    GROUP BY {column}
                    ORDER BY count DESC
                    LIMIT 5
                """)

                common = cursor.fetchall()
                if common:
                    analysis += "\nMost common values:\n"
                    for value, count in common:
                        analysis += f"  {value}: {count} times\n"

                return analysis

        except Exception as e:
            return f"Analysis error: {str(e)}"

# Create database-enabled agent
db_tools = DatabaseTools("./agent_database.db")

db_agent = Agent(
    'openai:gpt-4',
    tools=[
        db_tools.query_database,
        db_tools.get_table_info,
        db_tools.analyze_table
    ]
)

# Test database integration
db_queries = [
    "Show me all users in the database",
    "What tables are available?",
    "Analyze the department column in the users table"
]

print("Database integration test:")
for query in db_queries:
    print(f"\nQuery: {query}")
    result = db_agent.run_sync(query)
    print(f"Result: {result.data[:300]}...")
    print("-" * 80)
```

## Tool Orchestration Patterns

### Sequential Tool Execution

```python
from pydantic_ai import Agent, tool, RunContext
from typing import List, Dict, Any

class ToolOrchestrator:
    """Orchestrate complex tool execution patterns."""

    def __init__(self, agent: Agent):
        self.agent = agent
        self.execution_history = []

    async def execute_tool_sequence(self, tools: List[str], initial_input: str) -> Dict[str, Any]:
        """Execute a sequence of tools with data flow."""

        context = {"input": initial_input, "results": {}}
        current_input = initial_input

        for tool_name in tools:
            print(f"Executing tool: {tool_name}")

            # Modify prompt to include tool context
            enhanced_prompt = f"""
            {current_input}

            Previous tool results: {json.dumps(context['results'])}

            Use the {tool_name} tool to help with this task.
            """

            result = await self.agent.run(enhanced_prompt)

            # Store result for next tool
            context['results'][tool_name] = result.data
            current_input = result.data

            self.execution_history.append({
                "tool": tool_name,
                "input": enhanced_prompt,
                "output": result.data
            })

        return {
            "final_result": current_input,
            "execution_history": self.execution_history,
            "all_results": context['results']
        }

# Define workflow tools
@tool
def gather_requirements(ctx: RunContext[Dict[str, Any]], project_description: str) -> str:
    """Gather project requirements."""
    return f"Requirements for '{project_description}': functional specs, technical specs, timeline"

@tool
def estimate_effort(ctx: RunContext[Dict[str, Any]]) -> str:
    """Estimate project effort."""
    prev_results = ctx.deps.get("results", {})
    requirements = prev_results.get("gather_requirements", "")

    return f"Effort estimate based on {requirements}: 8 weeks, 3 developers"

@tool
def create_plan(ctx: RunContext[Dict[str, Any]]) -> str:
    """Create project plan."""
    prev_results = ctx.deps.get("results", {})

    return f"Project plan combining {list(prev_results.keys())}: detailed roadmap with milestones"

# Create orchestrated agent
orchestrator = ToolOrchestrator(Agent(
    'openai:gpt-4',
    deps_type=Dict[str, Any],
    tools=[gather_requirements, estimate_effort, create_plan]
))

# Execute tool sequence
workflow_result = await orchestrator.execute_tool_sequence(
    ["gather_requirements", "estimate_effort", "create_plan"],
    "Build a mobile app for task management"
)

print("Tool orchestration result:")
print(f"Final result: {workflow_result['final_result']}")
print(f"Tools executed: {len(workflow_result['execution_history'])}")
```

### Parallel Tool Execution

```python
import asyncio
from typing import List, Dict, Any

class ParallelToolExecutor:
    """Execute tools in parallel for better performance."""

    def __init__(self, agent: Agent):
        self.agent = agent

    async def execute_parallel(self, tool_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute multiple tool tasks in parallel.

        Args:
            tool_tasks: List of tasks, each with 'tool' and 'input' keys

        Returns:
            Combined results
        """
        async def execute_task(task: Dict[str, Any]) -> Dict[str, Any]:
            """Execute a single tool task."""
            tool_name = task['tool']
            input_data = task['input']

            prompt = f"Use the {tool_name} tool to process: {input_data}"

            result = await self.agent.run(prompt)

            return {
                "task": task,
                "result": result.data,
                "success": True
            }

        # Execute all tasks concurrently
        tasks = [execute_task(task) for task in tool_tasks]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful_results = []
        failed_results = []

        for result in results:
            if isinstance(result, Exception):
                failed_results.append({"error": str(result)})
            else:
                successful_results.append(result)

        return {
            "successful": successful_results,
            "failed": failed_results,
            "total_executed": len(successful_results),
            "total_failed": len(failed_results)
        }

# Create parallel executor
parallel_executor = ParallelToolExecutor(Agent(
    'openai:gpt-4',
    tools=[get_weather, web_search, calculate]
))

# Execute parallel tasks
parallel_tasks = [
    {"tool": "get_weather", "input": "Check weather in New York"},
    {"tool": "web_search", "input": "Latest AI news"},
    {"tool": "calculate", "input": "Calculate 25 * 15 + sqrt(144)"}
]

parallel_results = await parallel_executor.execute_parallel(parallel_tasks)

print("Parallel execution results:")
print(f"Successful: {parallel_results['total_executed']}")
print(f"Failed: {parallel_results['total_failed']}")

for result in parallel_results['successful']:
    task = result['task']
    output = result['result']
    print(f"  {task['tool']}: {output[:100]}...")
```

This comprehensive dependencies and tools chapter demonstrates how to extend Pydantic AI agents with powerful external integrations, tool chaining, and orchestration patterns for complex task completion. 🚀