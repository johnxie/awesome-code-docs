---
layout: default
title: "Phidata Tutorial - Chapter 3: Tools & Functions"
nav_order: 3
has_children: false
parent: Phidata Tutorial
---

# Chapter 3: Tools & Functions - Extending Agent Capabilities

Welcome to **Chapter 3: Tools & Functions - Extending Agent Capabilities**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Equip your Phidata agents with powerful tools and functions for real-world task completion.

## Built-in Tools

### Function Calling Setup

```python
from phidata.agent import Agent
from phidata.tools import tool
import json

# Create agent with function calling
agent = Agent(
    name="ToolAgent",
    instructions="You are an assistant with access to various tools. Use them when appropriate to help users.",
    model="gpt-4",
    tools=[],  # Will add tools below
    show_tool_calls=True  # Show which tools are being used
)
```

### Web Search Tool

```python
from phidata.tools import DuckDuckGo

# Add web search capability
web_search_tool = DuckDuckGo()

agent_with_search = Agent(
    name="ResearchAgent",
    instructions="You are a research assistant. Use web search to find accurate, up-to-date information.",
    model="gpt-4",
    tools=[web_search_tool]
)

# Test web search
result = agent_with_search.run("What are the latest developments in quantum computing?")
print(result)
```

### Calculator and Math Tools

```python
# Built-in calculator tool
agent_with_calc = Agent(
    name="MathAgent",
    instructions="You are a mathematics assistant. Use calculations when solving math problems.",
    model="gpt-4",
    tools=[{"type": "function", "function": {"name": "calculator", "description": "Calculate mathematical expressions"}}]
)

# Custom calculator function
def calculator(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    try:
        # Use a safe evaluation method
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# The agent can now perform calculations
result = agent_with_calc.run("What is 123 * 456 + sqrt(144)?")
print(result)
```

### File System Tools

```python
from phidata.tools import FileTools
import os

# File operations tool
file_tools = FileTools(
    base_dir="./workspace",  # Restrict to specific directory
    read_files=True,
    write_files=True,
    list_dir=True
)

file_agent = Agent(
    name="FileManager",
    instructions="You are a file management assistant. Help users with file operations.",
    model="gpt-4",
    tools=[file_tools]
)

# File operations
commands = [
    "List all files in the current directory",
    "Create a new file called 'notes.txt' with some content",
    "Read the content of 'notes.txt'"
]

for command in commands:
    result = file_agent.run(command)
    print(f"Command: {command}")
    print(f"Result: {result}")
    print("-" * 50)
```

## Custom Tool Development

### Basic Custom Tool

```python
from phidata.tools import tool
from typing import Dict, Any

@tool
def weather_lookup(city: str) -> str:
    """
    Get current weather for a city.

    Args:
        city: Name of the city to get weather for

    Returns:
        Weather information as string
    """
    # Mock weather API call
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Rainy, 15°C",
        "Tokyo": "Cloudy, 22°C",
        "Paris": "Partly cloudy, 18°C"
    }

    city_clean = city.strip().title()
    weather = weather_data.get(city_clean, f"Weather data not available for {city}")

    return f"Current weather in {city_clean}: {weather}"

# Create agent with custom tool
weather_agent = Agent(
    name="WeatherAssistant",
    instructions="You are a weather assistant. Help users check weather conditions.",
    model="gpt-4",
    tools=[weather_lookup]
)

# Test the tool
result = weather_agent.run("What's the weather like in Tokyo?")
print(result)
```

### Advanced Custom Tool with Error Handling

```python
from phidata.tools import tool
from typing import Optional, Dict, Any
import requests
import json

class WeatherAPITool:
    """Professional weather API tool with error handling."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    @tool
    def get_weather(self, city: str, units: str = "metric") -> str:
        """
        Get current weather information for a city.

        Args:
            city: City name (e.g., 'London', 'New York,US')
            units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit)

        Returns:
            Formatted weather information
        """
        try:
            if not self.api_key:
                return "Weather API key not configured. Please set OPENWEATHER_API_KEY."

            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Format weather data
            weather = data['weather'][0]['description'].title()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            unit_symbol = "°C" if units == "metric" else "°F"

            result = f"""Weather in {data['name']}, {data['sys']['country']}:
• Condition: {weather}
• Temperature: {temp}{unit_symbol}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s"""

            return result

        except requests.exceptions.RequestException as e:
            return f"Network error getting weather: {str(e)}"
        except KeyError as e:
            return f"Unexpected API response format: {str(e)}"
        except Exception as e:
            return f"Error getting weather: {str(e)}"

# Create tool instance
weather_tool = WeatherAPITool()

# Agent with professional weather tool
pro_weather_agent = Agent(
    name="ProfessionalWeatherAgent",
    instructions="""
    You are a professional weather consultant. Provide accurate, helpful weather information.
    Always specify the location clearly and give context about what the weather means.
    """,
    model="gpt-4",
    tools=[weather_tool.get_weather]
)

# Test with different cities
cities = ["London", "New York", "Tokyo", "InvalidCityName"]

for city in cities:
    result = pro_weather_agent.run(f"What's the weather like in {city}?")
    print(f"Weather query for {city}:")
    print(result)
    print("-" * 60)
```

### Tool with Structured Output

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class StockInfo(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    price: float = Field(..., description="Current stock price")
    change: float = Field(..., description="Price change from previous day")
    change_percent: float = Field(..., description="Percentage change")
    volume: Optional[int] = Field(None, description="Trading volume")
    market_cap: Optional[float] = Field(None, description="Market capitalization")

class StockAnalysis(BaseModel):
    stock: StockInfo
    recommendation: str = Field(..., enum=["BUY", "SELL", "HOLD"], description="Trading recommendation")
    analysis: str = Field(..., description="Brief analysis of the stock")
    risk_level: str = Field(..., enum=["LOW", "MEDIUM", "HIGH"], description="Risk assessment")

@tool
def analyze_stock(symbol: str) -> StockAnalysis:
    """
    Analyze a stock and provide trading recommendation.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        Structured stock analysis
    """
    # Mock stock data (in reality, you'd call a financial API)
    mock_data = {
        "AAPL": {"price": 175.50, "change": 2.30, "change_percent": 1.33, "volume": 52847392, "market_cap": 2.8e12},
        "GOOGL": {"price": 138.25, "change": -1.75, "change_percent": -1.25, "volume": 28394756, "market_cap": 1.7e12},
        "TSLA": {"price": 245.80, "change": 8.90, "change_percent": 3.76, "volume": 89473829, "market_cap": 780e9}
    }

    symbol = symbol.upper()

    if symbol not in mock_data:
        # Return neutral analysis for unknown stocks
        return StockAnalysis(
            stock=StockInfo(
                symbol=symbol,
                price=0.0,
                change=0.0,
                change_percent=0.0
            ),
            recommendation="HOLD",
            analysis=f"Stock symbol {symbol} not found in our database.",
            risk_level="HIGH"
        )

    data = mock_data[symbol]

    # Simple analysis logic
    if data["change_percent"] > 2:
        recommendation = "BUY"
        analysis = f"{symbol} is showing strong upward momentum with {data['change_percent']:.2f}% gain."
        risk_level = "MEDIUM"
    elif data["change_percent"] < -2:
        recommendation = "SELL"
        analysis = f"{symbol} is experiencing significant downward pressure with {data['change_percent']:.2f}% loss."
        risk_level = "HIGH"
    else:
        recommendation = "HOLD"
        analysis = f"{symbol} is trading within normal ranges with {data['change_percent']:.2f}% change."
        risk_level = "LOW"

    return StockAnalysis(
        stock=StockInfo(**data, symbol=symbol),
        recommendation=recommendation,
        analysis=analysis,
        risk_level=risk_level
    )

# Agent with structured stock analysis
finance_agent = Agent(
    name="StockAnalyst",
    instructions="""
    You are a professional stock analyst. Provide clear, data-driven analysis
    and recommendations based on current market data.
    """,
    model="gpt-4",
    tools=[analyze_stock],
    response_model=StockAnalysis  # Structured output
)

# Analyze stocks
stocks_to_analyze = ["AAPL", "GOOGL", "TSLA", "UNKNOWN"]

for stock in stocks_to_analyze:
    result = finance_agent.run(f"Analyze {stock} stock for me")
    print(f"Analysis for {stock}:")
    print(f"Price: ${result.stock.price}")
    print(f"Change: {result.stock.change:+.2f} ({result.stock.change_percent:+.2f}%)")
    print(f"Recommendation: {result.recommendation}")
    print(f"Analysis: {result.analysis}")
    print(f"Risk Level: {result.risk_level}")
    print("-" * 80)
```

## Function Libraries

### Utility Function Collection

```python
from phidata.tools import tool
from typing import List, Dict, Any, Optional
import datetime
import re

class UtilityTools:
    """Collection of utility tools for agents."""

    @staticmethod
    @tool
    def get_current_time(timezone: Optional[str] = None) -> str:
        """Get current date and time."""
        now = datetime.datetime.now()

        if timezone:
            # In practice, you'd use pytz or similar
            return f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S')}"

        return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    @staticmethod
    @tool
    def calculate(expression: str) -> str:
        """Calculate mathematical expressions safely."""
        try:
            # Very restrictive evaluation
            allowed_names = {
                k: v for k, v in math.__dict__.items()
                if not k.startswith("__") and k in ['sin', 'cos', 'tan', 'sqrt', 'log', 'exp', 'pi', 'e']
            }

            # Only allow basic operations
            if not re.match(r'^[0-9+\-*/().\s sqrt()cos()sin()tan()log()exp()pie]+$', expression):
                return "Error: Invalid characters in expression"

            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"

        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    @tool
    def convert_units(value: float, from_unit: str, to_unit: str) -> str:
        """Convert between different units."""
        conversions = {
            ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
            ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
            ("meters", "feet"): lambda x: x * 3.28084,
            ("feet", "meters"): lambda x: x / 3.28084,
            ("kilograms", "pounds"): lambda x: x * 2.20462,
            ("pounds", "kilograms"): lambda x: x / 2.20462,
        }

        key = (from_unit.lower(), to_unit.lower())
        reverse_key = (to_unit.lower(), from_unit.lower())

        if key in conversions:
            result = conversions[key](value)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        elif reverse_key in conversions:
            result = conversions[reverse_key](value)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"

        return f"Conversion from {from_unit} to {to_unit} not supported"

    @staticmethod
    @tool
    def search_list(items: List[str], query: str) -> List[str]:
        """Search for items in a list that match a query."""
        query_lower = query.lower()
        matches = [item for item in items if query_lower in item.lower()]
        return matches[:10]  # Limit results

    @staticmethod
    @tool
    def format_text(text: str, format_type: str) -> str:
        """Format text in different styles."""
        if format_type.lower() == "uppercase":
            return text.upper()
        elif format_type.lower() == "lowercase":
            return text.lower()
        elif format_type.lower() == "title":
            return text.title()
        elif format_type.lower() == "sentence":
            return text.capitalize()
        else:
            return f"Unsupported format: {format_type}"

# Create agent with utility tools
utility_agent = Agent(
    name="UtilityAssistant",
    instructions="""
    You are a utility assistant with access to various helpful tools.
    Use the appropriate tool for each user request.
    """,
    model="gpt-4",
    tools=[
        UtilityTools.get_current_time,
        UtilityTools.calculate,
        UtilityTools.convert_units,
        UtilityTools.search_list,
        UtilityTools.format_text
    ]
)

# Test utility functions
test_queries = [
    "What time is it?",
    "Calculate 15 * 23 + sqrt(144)",
    "Convert 25 celsius to fahrenheit",
    "Format this text in uppercase: hello world"
]

for query in test_queries:
    result = utility_agent.run(query)
    print(f"Query: {query}")
    print(f"Result: {result}")
    print("-" * 50)
```

## API Integration Tools

### REST API Tool

```python
import requests
from phidata.tools import tool
from typing import Dict, Any, Optional

class APITool:
    """Generic tool for making API calls."""

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}

    @tool
    def api_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Make a GET request to an API endpoint.

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters

        Returns:
            API response as formatted string
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            return f"API Response:\n{json.dumps(data, indent=2)}"

        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    @tool
    def api_post(self, endpoint: str, data: Dict[str, Any]) -> str:
        """
        Make a POST request to an API endpoint.

        Args:
            endpoint: API endpoint (without base URL)
            data: Request body data

        Returns:
            API response as formatted string
        """
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"

            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()

            result = response.json()
            return f"API Response:\n{json.dumps(result, indent=2)}"

        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

# GitHub API tool
github_tool = APITool(
    base_url="https://api.github.com",
    headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
)

# Create GitHub assistant agent
github_agent = Agent(
    name="GitHubAssistant",
    instructions="""
    You are a GitHub assistant. Help users with GitHub-related tasks using the available API tools.
    Always be helpful and provide clear explanations.
    """,
    model="gpt-4",
    tools=[
        github_tool.api_get,
        github_tool.api_post
    ]
)

# Test GitHub API integration
github_queries = [
    "Get information about the phidata repository",
    "List recent commits in the phidata repo"
]

for query in github_queries:
    result = github_agent.run(query)
    print(f"GitHub Query: {query}")
    print(f"Result: {result}")
    print("-" * 80)
```

### Database Query Tool

```python
import sqlite3
from phidata.tools import tool
from typing import List, Dict, Any, Optional

class DatabaseTool:
    """Tool for database operations."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database with sample data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    department TEXT
                )
            """)

            # Insert sample data
            sample_users = [
                (1, "Alice Johnson", "alice@company.com", "Engineering"),
                (2, "Bob Smith", "bob@company.com", "Marketing"),
                (3, "Carol Williams", "carol@company.com", "Sales"),
                (4, "David Brown", "david@company.com", "Engineering"),
                (5, "Eva Davis", "eva@company.com", "HR")
            ]

            conn.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", sample_users)

    @tool
    def query_database(self, sql_query: str) -> str:
        """
        Execute a SQL query on the database.

        Args:
            sql_query: SQL query to execute (SELECT only for safety)

        Returns:
            Query results as formatted string
        """
        try:
            # Safety check - only allow SELECT queries
            if not sql_query.strip().upper().startswith("SELECT"):
                return "Error: Only SELECT queries are allowed for security"

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(sql_query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

            if not rows:
                return "Query executed successfully. No results returned."

            # Format results
            result_lines = [", ".join(columns)]  # Header
            result_lines.extend([", ".join(str(cell) for cell in row) for row in rows])

            return f"Query Results:\n" + "\n".join(result_lines)

        except Exception as e:
            return f"Database Error: {str(e)}"

# Create database assistant
db_tool = DatabaseTool()

db_agent = Agent(
    name="DatabaseAssistant",
    instructions="""
    You are a database assistant. Help users query and analyze data.
    Always explain what you're doing and format results clearly.
    """,
    model="gpt-4",
    tools=[db_tool.query_database]
)

# Test database queries
db_queries = [
    "Show me all users in the database",
    "Find all users in the Engineering department",
    "Count users by department"
]

for query in db_queries:
    result = db_agent.run(query)
    print(f"DB Query: {query}")
    print(f"Result: {result}")
    print("-" * 80)
```

## Tool Orchestration

### Multi-Tool Workflows

```python
from phidata.workflow import Workflow, Task
from phidata.agent import Agent

# Create specialized agents for different tasks
research_agent = Agent(
    name="ResearchAgent",
    instructions="You are a research specialist. Find and analyze information.",
    model="gpt-4",
    tools=[web_search_tool]  # Assuming web_search_tool is defined
)

analysis_agent = Agent(
    name="AnalysisAgent",
    instructions="You are an analysis specialist. Process and interpret data.",
    model="gpt-4",
    tools=[calculator_tool]  # Assuming calculator_tool is defined
)

# Create workflow
research_workflow = Workflow(
    name="ResearchAnalysisWorkflow",
    description="Research a topic and provide analysis",
    tasks=[
        Task(
            name="research",
            description="Research the given topic using web search",
            agent=research_agent,
            output_key="research_results"
        ),
        Task(
            name="analyze",
            description="Analyze the research results and provide insights",
            agent=analysis_agent,
            input_key="research_results",
            output_key="analysis"
        )
    ]
)

# Execute workflow
result = research_workflow.run(topic="Latest developments in AI")
print("Workflow Result:")
print(result)
```

### Tool Selection Strategies

```python
class ToolSelector:
    """Intelligent tool selection based on query analysis."""

    def __init__(self):
        self.tool_capabilities = {
            "search": ["web_search", "database_query"],
            "calculate": ["calculator"],
            "file_ops": ["read_file", "write_file"],
            "api_calls": ["api_get", "api_post"],
            "analysis": ["analyze_data", "generate_report"]
        }

    def analyze_query(self, query: str) -> List[str]:
        """Analyze query to determine needed capabilities."""
        capabilities = []

        query_lower = query.lower()

        if any(word in query_lower for word in ["search", "find", "lookup"]):
            capabilities.append("search")

        if any(word in query_lower for word in ["calculate", "compute", "math"]):
            capabilities.append("calculate")

        if any(word in query_lower for word in ["file", "read", "write", "save"]):
            capabilities.append("file_ops")

        if any(word in query_lower for word in ["api", "request", "call"]):
            capabilities.append("api_calls")

        if any(word in query_lower for word in ["analyze", "report", "insights"]):
            capabilities.append("analysis")

        return capabilities

    def select_tools(self, capabilities: List[str], available_tools: List[Dict]) -> List[Dict]:
        """Select appropriate tools based on capabilities."""
        selected_tools = []

        for capability in capabilities:
            if capability in self.tool_capabilities:
                tool_names = self.tool_capabilities[capability]

                for tool in available_tools:
                    if tool.get("name") in tool_names:
                        selected_tools.append(tool)

        # Remove duplicates
        seen = set()
        unique_tools = []
        for tool in selected_tools:
            if tool["name"] not in seen:
                unique_tools.append(tool)
                seen.add(tool["name"])

        return unique_tools

# Intelligent tool selection
tool_selector = ToolSelector()

intelligent_agent = Agent(
    name="IntelligentAssistant",
    instructions="You are an intelligent assistant that selects the right tools for each task.",
    model="gpt-4",
    tools=[]  # Tools will be selected dynamically
)

# Override tool selection
def dynamic_tool_selection(query: str) -> List[Dict]:
    capabilities = tool_selector.analyze_query(query)

    # Define available tools
    available_tools = [
        {"name": "web_search", "capability": "search"},
        {"name": "calculator", "capability": "calculate"},
        {"name": "api_get", "capability": "api_calls"}
    ]

    return tool_selector.select_tools(capabilities, available_tools)

# Test dynamic tool selection
test_queries = [
    "Search for the latest news about AI",
    "Calculate 15 * 23 + sqrt(144)",
    "Get user information from the API"
]

for query in test_queries:
    selected_tools = dynamic_tool_selection(query)
    print(f"Query: {query}")
    print(f"Selected tools: {[t['name'] for t in selected_tools]}")
    print("-" * 50)
```

This comprehensive tools and functions chapter demonstrates how to extend Phidata agents with powerful capabilities for real-world task completion. The modular tool system allows for easy integration of custom functionality while maintaining security and reliability. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `tool`, `result`, `tools` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Tools & Functions - Extending Agent Capabilities` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `print`, `self`, `name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Tools & Functions - Extending Agent Capabilities` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `tool`.
2. **Input normalization**: shape incoming data so `result` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `tools`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `tool` and `result` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Understanding Phidata Agent Architecture](02-agent-architecture.md)
- [Next Chapter: Chapter 4: Memory Systems - Building Context-Aware Agents](04-memory-systems.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
