---
layout: default
title: "AG2 Tutorial - Chapter 5: Tool Integration"
nav_order: 5
has_children: false
parent: AG2 Tutorial
---

# Chapter 5: Tool Integration & Function Calling

Welcome to **Chapter 5: Tool Integration & Function Calling**. In this part of **AG2 Tutorial: Next-Generation Multi-Agent Framework**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Extend agent capabilities by integrating external tools, APIs, and services through function calling.

## Overview

Tool integration allows agents to interact with the real world by calling external functions, APIs, and services. This transforms agents from conversational assistants into powerful automation systems.

## Function Calling Basics

### Simple Function Tools

```python
from ag2 import AssistantAgent, UserProxyAgent
import requests

# Define tool functions
def get_weather(city):
    """Get current weather for a city"""
    api_key = "your-weather-api-key"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        return f"Weather in {city}: {temp}°C, {condition}"
    except Exception as e:
        return f"Error getting weather: {str(e)}"

def calculate_distance(origin, destination):
    """Calculate distance between two cities"""
    # Simplified distance calculation
    distances = {
        ("New York", "London"): 5585,
        ("London", "Paris"): 344,
        ("Paris", "Berlin"): 878,
        ("Berlin", "New York"): 6389
    }

    key = (origin, destination)
    reverse_key = (destination, origin)

    if key in distances:
        return f"Distance from {origin} to {destination}: {distances[key]} km"
    elif reverse_key in distances:
        return f"Distance from {origin} to {destination}: {distances[reverse_key]} km"
    else:
        return f"Distance data not available for {origin} to {destination}"

# Create agent with tool functions
assistant = AssistantAgent(
    name="tool_assistant",
    system_message="""You are a helpful assistant with access to various tools.
    Use the available functions to help users with their requests.""",
    llm_config=llm_config
)

# Register functions (AG2 will automatically detect and use them)
assistant.register_function(get_weather)
assistant.register_function(calculate_distance)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False
)

# Test tool integration
user_proxy.initiate_chat(
    assistant,
    message="What's the weather like in London and how far is it from Paris?"
)
```

### Function Registration

```python
# Manual function registration with descriptions
assistant.register_function(
    function_map={
        "get_weather": get_weather,
        "calculate_distance": calculate_distance
    }
)

# With custom descriptions
assistant.register_function(
    function_map={
        "get_weather": {
            "function": get_weather,
            "description": "Retrieve current weather information for any city worldwide"
        },
        "calculate_distance": {
            "function": calculate_distance,
            "description": "Calculate driving distance between two cities in kilometers"
        }
    }
)
```

## Advanced Tool Integration

### Database Tools

```python
import sqlite3
from typing import List, Dict

def query_database(sql_query: str) -> List[Dict]:
    """Execute SQL query on a sample database"""
    try:
        conn = sqlite3.connect('sample.db')
        cursor = conn.cursor()

        # Create sample table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                age INTEGER
            )
        ''')

        # Insert sample data
        cursor.executemany('''
            INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)
        ''', [
            ('Alice', 'alice@example.com', 25),
            ('Bob', 'bob@example.com', 30),
            ('Charlie', 'charlie@example.com', 35)
        ])

        conn.commit()

        # Execute the user's query
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()

        # Convert to list of dictionaries
        result_dicts = [dict(zip(columns, row)) for row in results]

        conn.close()
        return result_dicts

    except Exception as e:
        return [{"error": str(e)}]

# Database assistant
db_assistant = AssistantAgent(
    name="database_assistant",
    system_message="""You are a database expert. Help users query and analyze data.
    Always explain what the query does before executing it.""",
    llm_config=llm_config
)

db_assistant.register_function(query_database)

db_user = UserProxyAgent(
    name="db_user",
    human_input_mode="NEVER",
    code_execution_config=False
)

# Database query example
db_user.initiate_chat(
    db_assistant,
    message="Show me all users older than 28 years"
)
```

### File System Tools

```python
import os
import json
from pathlib import Path

def read_file(file_path: str) -> str:
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def list_directory(dir_path: str = ".") -> List[str]:
    """List contents of a directory"""
    try:
        return os.listdir(dir_path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

def analyze_codebase(directory: str) -> Dict:
    """Analyze codebase structure and statistics"""
    try:
        stats = {
            "total_files": 0,
            "code_files": 0,
            "directories": 0,
            "languages": {}
        }

        for root, dirs, files in os.walk(directory):
            stats["directories"] += len(dirs)

            for file in files:
                stats["total_files"] += 1

                if file.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                    stats["code_files"] += 1

                    ext = file.split('.')[-1]
                    stats["languages"][ext] = stats["languages"].get(ext, 0) + 1

        return stats
    except Exception as e:
        return {"error": str(e)}

# File system assistant
fs_assistant = AssistantAgent(
    name="filesystem_assistant",
    system_message="""You are a file system expert. Help users manage files and directories.
    Always be careful with file operations and confirm destructive actions.""",
    llm_config=llm_config
)

fs_assistant.register_function(read_file)
fs_assistant.register_function(write_file)
fs_assistant.register_function(list_directory)
fs_assistant.register_function(analyze_codebase)
```

### Web Tools

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def web_search(query: str, num_results: int = 5) -> List[Dict]:
    """Search the web for information (simplified example)"""
    # Note: In practice, you'd use a real search API like Google Custom Search
    # or Bing Web Search API

    try:
        # Mock search results for demonstration
        mock_results = [
            {
                "title": f"Result 1 for {query}",
                "url": f"https://example.com/result1",
                "snippet": f"This is a sample result about {query}..."
            },
            {
                "title": f"Result 2 for {query}",
                "url": f"https://example.com/result2",
                "snippet": f"Another sample result about {query}..."
            }
        ]

        return mock_results[:num_results]
    except Exception as e:
        return [{"error": str(e)}]

def scrape_webpage(url: str) -> Dict:
    """Scrape basic information from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract basic information
        title = soup.title.string if soup.title else "No title found"
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else "No description found"

        # Extract main headings
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3'])[:5]:
            headings.append(h.get_text().strip())

        return {
            "url": url,
            "title": title,
            "description": description,
            "headings": headings,
            "status_code": response.status_code
        }
    except Exception as e:
        return {"error": str(e), "url": url}

# Web assistant
web_assistant = AssistantAgent(
    name="web_assistant",
    system_message="""You are a web research expert. Help users find and analyze online information.
    Always respect website terms of service and robots.txt files.""",
    llm_config=llm_config
)

web_assistant.register_function(web_search)
web_assistant.register_function(scrape_webpage)
```

## API Integration

### REST API Tools

```python
def call_rest_api(endpoint: str, method: str = "GET", headers: Dict = None, data: Dict = None) -> Dict:
    """Generic REST API caller"""
    try:
        headers = headers or {}
        headers.setdefault('User-Agent', 'AG2-Agent/1.0')
        headers.setdefault('Content-Type', 'application/json')

        if method.upper() == "GET":
            response = requests.get(endpoint, headers=headers, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(endpoint, headers=headers, json=data, timeout=30)
        elif method.upper() == "PUT":
            response = requests.put(endpoint, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            response = requests.delete(endpoint, headers=headers, timeout=30)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}

        response.raise_for_status()

        # Try to parse JSON response
        try:
            return response.json()
        except:
            return {"text_response": response.text}

    except Exception as e:
        return {"error": str(e), "endpoint": endpoint, "method": method}

def github_api_call(endpoint: str, token: str = None) -> Dict:
    """GitHub API integration"""
    base_url = "https://api.github.com"
    full_url = urljoin(base_url, endpoint)

    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'

    return call_rest_api(full_url, headers=headers)

def search_github_repos(query: str, language: str = None) -> List[Dict]:
    """Search GitHub repositories"""
    search_query = f"{query}+language:{language}" if language else query
    endpoint = f"/search/repositories?q={search_query}&sort=stars&order=desc"

    result = github_api_call(endpoint)

    if "items" in result:
        repos = []
        for repo in result["items"][:5]:  # Top 5 results
            repos.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "url": repo["html_url"]
            })
        return repos
    else:
        return result

# GitHub assistant
github_assistant = AssistantAgent(
    name="github_assistant",
    system_message="""You are a GitHub expert. Help users find repositories, analyze code, and work with GitHub features.
    Always respect API rate limits and GitHub's terms of service.""",
    llm_config=llm_config
)

github_assistant.register_function(search_github_repos)
```

### GraphQL API Tools

```python
def graphql_query(endpoint: str, query: str, variables: Dict = None, headers: Dict = None) -> Dict:
    """Execute GraphQL query"""
    try:
        headers = headers or {}
        headers.setdefault('Content-Type', 'application/json')

        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        return response.json()
    except Exception as e:
        return {"error": str(e)}

def github_graphql_query(query: str, token: str) -> Dict:
    """GitHub GraphQL API"""
    endpoint = "https://api.github.com/graphql"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    return graphql_query(endpoint, query, headers=headers)

# Example GraphQL query for repository information
repo_query = """
query GetRepository($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    description
    stargazers {
      totalCount
    }
    issues(states: OPEN) {
      totalCount
    }
    pullRequests(states: OPEN) {
      totalCount
    }
  }
}
"""

def get_repo_details(owner: str, repo: str, token: str) -> Dict:
    """Get detailed repository information using GraphQL"""
    result = github_graphql_query(repo_query, token)

    if "data" in result and "repository" in result["data"]:
        repo_data = result["data"]["repository"]
        return {
            "name": repo_data["name"],
            "description": repo_data["description"],
            "stars": repo_data["stargazers"]["totalCount"],
            "open_issues": repo_data["issues"]["totalCount"],
            "open_prs": repo_data["pullRequests"]["totalCount"]
        }
    else:
        return result
```

## Tool Orchestration

### Tool Chain Pattern

```python
class ToolOrchestrator:
    def __init__(self):
        self.tools = {}
        self.tool_chains = {}

    def register_tool(self, name: str, function, description: str = ""):
        """Register a tool"""
        self.tools[name] = {
            "function": function,
            "description": description
        }

    def create_tool_chain(self, chain_name: str, tool_sequence: List[str]):
        """Create a sequence of tools to execute"""
        self.tool_chains[chain_name] = tool_sequence

    def execute_tool_chain(self, chain_name: str, initial_input: Dict) -> Dict:
        """Execute a tool chain with data flow"""
        if chain_name not in self.tool_chains:
            return {"error": f"Tool chain '{chain_name}' not found"}

        result = initial_input
        execution_log = []

        for tool_name in self.tool_chains[chain_name]:
            if tool_name not in self.tools:
                execution_log.append(f"Error: Tool '{tool_name}' not found")
                break

            try:
                tool_func = self.tools[tool_name]["function"]
                result = tool_func(**result) if isinstance(result, dict) else tool_func(result)
                execution_log.append(f"Executed {tool_name}: Success")
            except Exception as e:
                execution_log.append(f"Executed {tool_name}: Error - {str(e)}")
                break

        return {
            "final_result": result,
            "execution_log": execution_log
        }

# Create tool orchestrator
orchestrator = ToolOrchestrator()

# Register tools
orchestrator.register_tool("web_search", web_search, "Search the web")
orchestrator.register_tool("scrape_page", scrape_webpage, "Extract webpage content")
orchestrator.register_tool("analyze_content", lambda x: {"analysis": f"Analysis of: {x}"}, "Analyze content")

# Create tool chain
orchestrator.create_tool_chain("research_chain", ["web_search", "scrape_page", "analyze_content"])

# Execute chain
result = orchestrator.execute_tool_chain("research_chain", {"query": "machine learning"})
```

### Conditional Tool Execution

```python
class ConditionalToolExecutor:
    def __init__(self):
        self.tools = {}
        self.conditions = {}

    def register_conditional_tool(self, name: str, function, condition_func):
        """Register a tool with execution condition"""
        self.tools[name] = function
        self.conditions[name] = condition_func

    def execute_if_condition(self, tool_name: str, context: Dict) -> Dict:
        """Execute tool only if condition is met"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not registered"}

        if tool_name not in self.conditions:
            return {"error": f"No condition defined for '{tool_name}'"}

        # Check condition
        if not self.conditions[tool_name](context):
            return {"skipped": True, "reason": "Condition not met"}

        # Execute tool
        try:
            result = self.tools[tool_name](**context)
            return {"executed": True, "result": result}
        except Exception as e:
            return {"executed": True, "error": str(e)}

# Create conditional executor
conditional_executor = ConditionalToolExecutor()

# Define conditions
def needs_weather_data(context):
    return "weather" in context.get("query", "").lower()

def needs_location_data(context):
    return any(word in context.get("query", "").lower() for word in ["distance", "location", "map"])

# Register conditional tools
conditional_executor.register_conditional_tool("get_weather", get_weather, needs_weather_data)
conditional_executor.register_conditional_tool("calculate_distance", calculate_distance, needs_location_data)

# Execute based on query content
query_context = {"query": "What's the weather like and how far is it to Paris?"}

weather_result = conditional_executor.execute_if_condition("get_weather", query_context)
distance_result = conditional_executor.execute_if_condition("calculate_distance", query_context)
```

## Error Handling and Validation

### Tool Error Recovery

```python
class RobustToolExecutor:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries
        self.execution_stats = {}

    def execute_with_retry(self, tool_name: str, tool_func, **kwargs):
        """Execute tool with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = tool_func(**kwargs)

                # Track successful execution
                self._update_stats(tool_name, True, attempt + 1)
                return result

            except Exception as e:
                error_msg = str(e)
                self._update_stats(tool_name, False, attempt + 1)

                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    return {"error": error_msg, "attempts": attempt + 1}

                # Wait before retry (exponential backoff)
                time.sleep(2 ** attempt)

    def _update_stats(self, tool_name: str, success: bool, attempts: int):
        """Update execution statistics"""
        if tool_name not in self.execution_stats:
            self.execution_stats[tool_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "average_attempts": 0
            }

        stats = self.execution_stats[tool_name]
        stats["total_calls"] += 1

        if success:
            stats["successful_calls"] += 1
        else:
            stats["failed_calls"] += 1

        # Update average attempts
        stats["average_attempts"] = (
            (stats["average_attempts"] * (stats["total_calls"] - 1)) + attempts
        ) / stats["total_calls"]

# Robust tool executor
robust_executor = RobustToolExecutor(max_retries=3)
```

### Input Validation

```python
def validate_tool_input(func):
    """Decorator for tool input validation"""
    def wrapper(*args, **kwargs):
        # Validate common parameters
        if 'api_key' in kwargs and not kwargs['api_key']:
            raise ValueError("API key is required")

        if 'url' in kwargs:
            url = kwargs['url']
            if not url.startswith(('http://', 'https://')):
                raise ValueError("URL must start with http:// or https://")

        return func(*args, **kwargs)
    return wrapper

@validate_tool_input
def secure_web_scrape(url: str, api_key: str = None) -> Dict:
    """Secure web scraping with validation"""
    # Implementation here
    pass

# Apply validation to tools
secure_web_scrape = validate_tool_input(scrape_webpage)
```

## Best Practices

### Tool Design
- **Single Responsibility**: Each tool should do one thing well
- **Clear Interfaces**: Well-defined inputs and outputs
- **Error Handling**: Comprehensive error handling and recovery
- **Documentation**: Clear descriptions and usage examples

### Security Considerations
- **Input Validation**: Validate all inputs before processing
- **Rate Limiting**: Implement rate limits for API calls
- **Authentication**: Secure API keys and credentials
- **Access Control**: Limit tool capabilities appropriately

### Performance Optimization
- **Caching**: Cache results for expensive operations
- **Async Execution**: Use async patterns for I/O operations
- **Resource Limits**: Set timeouts and resource constraints
- **Monitoring**: Track tool usage and performance

### Maintenance
- **Versioning**: Version tool interfaces
- **Testing**: Comprehensive test coverage
- **Monitoring**: Log tool usage and errors
- **Updates**: Keep dependencies and APIs current

## Summary

In this chapter, we've covered:

- **Function Calling Basics**: Simple tool registration and usage
- **Advanced Integration**: Database, file system, and web tools
- **API Integration**: REST and GraphQL API tools
- **Tool Orchestration**: Chains, conditional execution, and workflows
- **Error Handling**: Retry logic, validation, and recovery
- **Best Practices**: Design, security, performance, and maintenance

Next, we'll explore **group chat** - coordinating multiple agents in collaborative conversations.

---

**Ready for the next chapter?** [Chapter 6: Group Chat](06-group-chat.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `headers`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Tool Integration & Function Calling` as an operating subsystem inside **AG2 Tutorial: Next-Generation Multi-Agent Framework**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `result`, `Dict` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Tool Integration & Function Calling` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `headers` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/ag2ai/ag2)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [github.com/microsoft/autogen](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `github.com/microsoft/autogen` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `headers` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Code Execution & Security](04-code-execution.md)
- [Next Chapter: Chapter 6: Group Chat & Multi-Agent Collaboration](06-group-chat.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
