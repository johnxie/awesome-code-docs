---
layout: default
title: "Chapter 4: Tool Integration"
parent: "Microsoft AutoGen Tutorial"
nav_order: 4
---

# Chapter 4: Tool Integration

Welcome to tool integration! In this chapter, we'll explore how AutoGen agents can extend their capabilities by integrating with external tools, APIs, and services. Tools allow agents to perform real-world actions and access external data sources.

## Tool Fundamentals

### Tool Definition and Structure

```python
from typing import Dict, Any, List, Callable, Optional
from enum import Enum
import time

class ToolCategory(Enum):
    WEB = "web"
    DATA = "data"
    COMPUTATION = "computation"
    COMMUNICATION = "communication"
    FILE_SYSTEM = "file_system"
    API = "api"

class ToolParameter:
    def __init__(self, name: str, type: str, description: str, required: bool = False, default: Any = None):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.default = default

class Tool:
    def __init__(self, name: str, description: str, category: ToolCategory, parameters: List[ToolParameter]):
        self.name = name
        self.description = description
        self.category = category
        self.parameters = parameters
        self.usage_count = 0
        self.last_used = None
        self.success_rate = 1.0

    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        self.usage_count += 1
        self.last_used = time.time()

        try:
            result = await self._execute_impl(**kwargs)
            return result
        except Exception as e:
            self.success_rate = (self.success_rate * (self.usage_count - 1) + 0) / self.usage_count
            raise e

    async def _execute_impl(self, **kwargs) -> Any:
        """Implementation of tool execution"""
        raise NotImplementedError("Subclasses must implement _execute_impl")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the tool"""
        return {
            "usage_count": self.usage_count,
            "last_used": self.last_used,
            "success_rate": self.success_rate,
            "category": self.category.value
        }
```

### Tool Registry

```python
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[ToolCategory, List[str]] = {}

    def register_tool(self, tool: Tool):
        """Register a tool in the registry"""
        self.tools[tool.name] = tool

        # Add to category index
        if tool.category not in self.categories:
            self.categories[tool.category] = []
        self.categories[tool.category].append(tool.name)

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def get_tools_by_category(self, category: ToolCategory) -> List[Tool]:
        """Get all tools in a category"""
        tool_names = self.categories.get(category, [])
        return [self.tools[name] for name in tool_names if name in self.tools]

    def search_tools(self, query: str) -> List[Tool]:
        """Search tools by name or description"""
        query_lower = query.lower()
        return [
            tool for tool in self.tools.values()
            if query_lower in tool.name.lower() or query_lower in tool.description.lower()
        ]

    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools"""
        return list(self.tools.values())

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_tools": len(self.tools),
            "categories": {cat.value: len(tools) for cat, tools in self.categories.items()},
            "most_used": max(self.tools.values(), key=lambda t: t.usage_count, default=None)
        }
```

## Web Tools

### Web Search Tool

```python
import requests
import json
from typing import List, Dict, Any

class WebSearchTool(Tool):
    def __init__(self, api_key: str):
        super().__init__(
            name="web_search",
            description="Search the web for information using a search API",
            category=ToolCategory.WEB,
            parameters=[
                ToolParameter("query", "string", "Search query", required=True),
                ToolParameter("num_results", "integer", "Number of results to return", default=5)
            ]
        )
        self.api_key = api_key
        self.base_url = "https://api.searchservice.com/search"

    async def _execute_impl(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Execute web search"""
        params = {
            "q": query,
            "num": num_results,
            "key": self.api_key
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        results = response.json()

        return {
            "query": query,
            "results": [
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", "")
                }
                for result in results.get("items", [])
            ],
            "total_results": len(results.get("items", []))
        }

# Usage
search_tool = WebSearchTool(api_key="your-api-key")
registry = ToolRegistry()
registry.register_tool(search_tool)
```

### Web Scraping Tool

```python
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from urllib.parse import urljoin, urlparse

class WebScrapingTool(Tool):
    def __init__(self):
        super().__init__(
            name="web_scraper",
            description="Extract content from web pages",
            category=ToolCategory.WEB,
            parameters=[
                ToolParameter("url", "string", "URL to scrape", required=True),
                ToolParameter("selectors", "object", "CSS selectors to extract", default={}),
                ToolParameter("follow_links", "boolean", "Whether to follow links", default=False)
            ]
        )

    async def _execute_impl(self, url: str, selectors: Dict[str, str] = None, follow_links: bool = False) -> Dict[str, Any]:
        """Execute web scraping"""
        if selectors is None:
            selectors = {}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    response.raise_for_status()
                    html = await response.text()

                soup = BeautifulSoup(html, 'html.parser')

                # Extract basic page information
                result = {
                    "url": url,
                    "title": soup.title.string if soup.title else "",
                    "text_content": soup.get_text(),
                    "links": [link.get('href') for link in soup.find_all('a') if link.get('href')]
                }

                # Extract content using selectors
                extracted_content = {}
                for name, selector in selectors.items():
                    elements = soup.select(selector)
                    extracted_content[name] = [
                        element.get_text().strip() for element in elements
                    ]

                result["extracted_content"] = extracted_content

                # Follow links if requested
                if follow_links:
                    result["followed_pages"] = await self._follow_links(session, result["links"][:5])

                return result

            except Exception as e:
                return {
                    "error": str(e),
                    "url": url
                }

    async def _follow_links(self, session: aiohttp.ClientSession, links: List[str]) -> List[Dict[str, Any]]:
        """Follow links and extract basic information"""
        followed_pages = []

        for link in links[:5]:  # Limit to 5 links
            try:
                # Convert relative URLs to absolute
                if not link.startswith('http'):
                    continue

                async with session.get(link, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        followed_pages.append({
                            "url": link,
                            "title": soup.title.string if soup.title else "",
                            "status": response.status
                        })
            except Exception as e:
                followed_pages.append({
                    "url": link,
                    "error": str(e)
                })

        return followed_pages

# Usage
scraper_tool = WebScrapingTool()
registry.register_tool(scraper_tool)
```

## Data Processing Tools

### Data Analysis Tool

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import json

class DataAnalysisTool(Tool):
    def __init__(self):
        super().__init__(
            name="data_analyzer",
            description="Analyze data and provide insights",
            category=ToolCategory.DATA,
            parameters=[
                ToolParameter("data", "array", "Data to analyze", required=True),
                ToolParameter("analysis_type", "string", "Type of analysis to perform", default="summary")
            ]
        )

    async def _execute_impl(self, data: List[Dict[str, Any]], analysis_type: str = "summary") -> Dict[str, Any]:
        """Execute data analysis"""
        try:
            df = pd.DataFrame(data)

            if analysis_type == "summary":
                return self._generate_summary(df)
            elif analysis_type == "correlation":
                return self._analyze_correlations(df)
            elif analysis_type == "trends":
                return self._identify_trends(df)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}"}

        except Exception as e:
            return {"error": str(e)}

    def _generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate data summary"""
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "summary_stats": df.describe().to_dict(),
            "unique_values": {col: df[col].nunique() for col in df.columns}
        }

    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between variables"""
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            return {"error": "No numeric columns found for correlation analysis"}

        correlation_matrix = numeric_df.corr()

        # Find strongest correlations
        correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                col1 = correlation_matrix.columns[i]
                col2 = correlation_matrix.columns[j]
                corr_value = correlation_matrix.iloc[i, j]
                correlations.append({
                    "variables": [col1, col2],
                    "correlation": corr_value,
                    "strength": self._interpret_correlation(abs(corr_value))
                })

        correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)

        return {
            "correlation_matrix": correlation_matrix.to_dict(),
            "top_correlations": correlations[:10]
        }

    def _identify_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify trends in the data"""
        trends = {}

        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                # Calculate trend using linear regression
                x = np.arange(len(df))
                y = df[column].values

                # Simple trend calculation
                if len(y) > 1:
                    trend = (y[-1] - y[0]) / len(y)
                    trends[column] = {
                        "trend": trend,
                        "direction": "increasing" if trend > 0 else "decreasing",
                        "magnitude": abs(trend)
                    }

        return {
            "trends": trends,
            "summary": f"Found trends in {len(trends)} numeric columns"
        }

    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation strength"""
        if correlation >= 0.8:
            return "very strong"
        elif correlation >= 0.6:
            return "strong"
        elif correlation >= 0.4:
            return "moderate"
        elif correlation >= 0.2:
            return "weak"
        else:
            return "very weak"

# Usage
analysis_tool = DataAnalysisTool()
registry.register_tool(analysis_tool)
```

### Database Query Tool

```python
import asyncpg
import sqlite3
from typing import Dict, Any, List

class DatabaseTool(Tool):
    def __init__(self, connection_string: str):
        super().__init__(
            name="database_query",
            description="Execute database queries",
            category=ToolCategory.DATA,
            parameters=[
                ToolParameter("query", "string", "SQL query to execute", required=True),
                ToolParameter("database_type", "string", "Database type (postgres, sqlite)", default="postgres")
            ]
        )
        self.connection_string = connection_string

    async def _execute_impl(self, query: str, database_type: str = "postgres") -> Dict[str, Any]:
        """Execute database query"""
        try:
            if database_type == "postgres":
                return await self._execute_postgres(query)
            elif database_type == "sqlite":
                return self._execute_sqlite(query)
            else:
                return {"error": f"Unsupported database type: {database_type}"}
        except Exception as e:
            return {"error": str(e)}

    async def _execute_postgres(self, query: str) -> Dict[str, Any]:
        """Execute PostgreSQL query"""
        conn = await asyncpg.connect(self.connection_string)
        try:
            if query.strip().upper().startswith("SELECT"):
                rows = await conn.fetch(query)
                return {
                    "query_type": "SELECT",
                    "rows": [dict(row) for row in rows],
                    "row_count": len(rows)
                }
            else:
                result = await conn.execute(query)
                return {
                    "query_type": "MODIFY",
                    "result": result
                }
        finally:
            await conn.close()

    def _execute_sqlite(self, query: str) -> Dict[str, Any]:
        """Execute SQLite query"""
        conn = sqlite3.connect(self.connection_string)
        try:
            cursor = conn.cursor()

            if query.strip().upper().startswith("SELECT"):
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                return {
                    "query_type": "SELECT",
                    "columns": columns,
                    "rows": [dict(zip(columns, row)) for row in rows],
                    "row_count": len(rows)
                }
            else:
                cursor.execute(query)
                conn.commit()

                return {
                    "query_type": "MODIFY",
                    "rows_affected": cursor.rowcount
                }
        finally:
            conn.close()

# Usage
db_tool = DatabaseTool("postgresql://user:password@localhost:5432/mydb")
registry.register_tool(db_tool)
```

## Communication Tools

### Email Tool

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List

class EmailTool(Tool):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        super().__init__(
            name="email_sender",
            description="Send emails",
            category=ToolCategory.COMMUNICATION,
            parameters=[
                ToolParameter("to", "string", "Recipient email address", required=True),
                ToolParameter("subject", "string", "Email subject", required=True),
                ToolParameter("body", "string", "Email body", required=True),
                ToolParameter("cc", "array", "CC recipients", default=[]),
                ToolParameter("bcc", "array", "BCC recipients", default=[])
            ]
        )
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def _execute_impl(self, to: str, subject: str, body: str, cc: List[str] = None, bcc: List[str] = None) -> Dict[str, Any]:
        """Send email"""
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = ', '.join(cc)

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)

            # Send email
            recipients = [to] + cc + bcc
            text = msg.as_string()
            server.sendmail(self.username, recipients, text)
            server.quit()

            return {
                "success": True,
                "recipients": len(recipients),
                "subject": subject
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Usage
email_tool = EmailTool(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    username="your-email@gmail.com",
    password="your-app-password"
)
registry.register_tool(email_tool)
```

### Slack Integration Tool

```python
import slack_sdk
from slack_sdk.web.async_client import AsyncWebClient
from typing import Dict, Any, List

class SlackTool(Tool):
    def __init__(self, bot_token: str):
        super().__init__(
            name="slack_messenger",
            description="Send messages and interact with Slack",
            category=ToolCategory.COMMUNICATION,
            parameters=[
                ToolParameter("channel", "string", "Slack channel", required=True),
                ToolParameter("message", "string", "Message to send", required=True),
                ToolParameter("action", "string", "Action to perform", default="send_message")
            ]
        )
        self.client = AsyncWebClient(token=bot_token)

    async def _execute_impl(self, channel: str, message: str, action: str = "send_message") -> Dict[str, Any]:
        """Execute Slack action"""
        try:
            if action == "send_message":
                result = await self._send_message(channel, message)
            elif action == "get_channel_info":
                result = await self._get_channel_info(channel)
            elif action == "list_users":
                result = await self._list_users()
            else:
                return {"error": f"Unknown action: {action}"}

            return result

        except Exception as e:
            return {"error": str(e)}

    async def _send_message(self, channel: str, message: str) -> Dict[str, Any]:
        """Send message to Slack channel"""
        response = await self.client.chat_postMessage(
            channel=channel,
            text=message
        )

        return {
            "success": True,
            "channel": channel,
            "message_ts": response["ts"],
            "message": message
        }

    async def _get_channel_info(self, channel: str) -> Dict[str, Any]:
        """Get information about a Slack channel"""
        response = await self.client.conversations_info(channel=channel)

        return {
            "channel_name": response["channel"]["name"],
            "member_count": response["channel"]["num_members"],
            "topic": response["channel"]["topic"]["value"],
            "purpose": response["channel"]["purpose"]["value"]
        }

    async def _list_users(self) -> Dict[str, Any]:
        """List users in the workspace"""
        response = await self.client.users_list()

        users = [
            {
                "id": user["id"],
                "name": user["name"],
                "real_name": user["real_name"],
                "is_admin": user.get("is_admin", False)
            }
            for user in response["members"]
            if not user["is_bot"]
        ]

        return {
            "total_users": len(users),
            "users": users
        }

# Usage
slack_tool = SlackTool(bot_token="your-slack-bot-token")
registry.register_tool(slack_tool)
```

## File System Tools

### File Operations Tool

```python
import aiofiles
import os
from pathlib import Path
from typing import Dict, Any, List

class FileOperationsTool(Tool):
    def __init__(self, allowed_paths: List[str] = None):
        super().__init__(
            name="file_operations",
            description="Perform file system operations",
            category=ToolCategory.FILE_SYSTEM,
            parameters=[
                ToolParameter("operation", "string", "Operation to perform", required=True),
                ToolParameter("path", "string", "File or directory path", required=True),
                ToolParameter("content", "string", "Content for write operations"),
                ToolParameter("destination", "string", "Destination path for move/copy operations")
            ]
        )
        self.allowed_paths = allowed_paths or ["/tmp", "./workspace"]

    async def _execute_impl(self, operation: str, path: str, content: str = None, destination: str = None) -> Dict[str, Any]:
        """Execute file operation"""
        # Security check
        if not self._is_path_allowed(path):
            return {"error": f"Access denied to path: {path}"}

        try:
            if operation == "read":
                return await self._read_file(path)
            elif operation == "write":
                return await self._write_file(path, content)
            elif operation == "list":
                return await self._list_directory(path)
            elif operation == "delete":
                return await self._delete_file(path)
            elif operation == "move":
                return await self._move_file(path, destination)
            else:
                return {"error": f"Unknown operation: {operation}"}

        except Exception as e:
            return {"error": str(e)}

    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed directories"""
        try:
            resolved_path = Path(path).resolve()
            for allowed_path in self.allowed_paths:
                allowed_resolved = Path(allowed_path).resolve()
                if resolved_path.is_relative_to(allowed_resolved):
                    return True
            return False
        except:
            return False

    async def _read_file(self, path: str) -> Dict[str, Any]:
        """Read file content"""
        async with aiofiles.open(path, 'r') as f:
            content = await f.read()

        return {
            "operation": "read",
            "path": path,
            "content": content,
            "size": len(content)
        }

    async def _write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to file"""
        async with aiofiles.open(path, 'w') as f:
            await f.write(content)

        return {
            "operation": "write",
            "path": path,
            "size": len(content)
        }

    async def _list_directory(self, path: str) -> Dict[str, Any]:
        """List directory contents"""
        entries = []
        for entry in os.scandir(path):
            entries.append({
                "name": entry.name,
                "type": "directory" if entry.is_dir() else "file",
                "size": entry.stat().st_size if entry.is_file() else 0,
                "modified": entry.stat().st_mtime
            })

        return {
            "operation": "list",
            "path": path,
            "entries": entries,
            "count": len(entries)
        }

    async def _delete_file(self, path: str) -> Dict[str, Any]:
        """Delete file"""
        os.remove(path)
        return {
            "operation": "delete",
            "path": path,
            "success": True
        }

    async def _move_file(self, path: str, destination: str) -> Dict[str, Any]:
        """Move file to new location"""
        if not self._is_path_allowed(destination):
            return {"error": f"Access denied to destination: {destination}"}

        os.rename(path, destination)
        return {
            "operation": "move",
            "from": path,
            "to": destination,
            "success": True
        }

# Usage
file_tool = FileOperationsTool(allowed_paths=["./workspace", "/tmp"])
registry.register_tool(file_tool)
```

## Tool Integration with Agents

### Function Calling Agent

```python
from autogen import AssistantAgent
from typing import Dict, Any

class ToolEnabledAgent(AssistantAgent):
    def __init__(self, name: str, tools: List[Tool], **kwargs):
        super().__init__(name=name, **kwargs)
        self.tools = {tool.name: tool for tool in tools}
        self.function_map = self._create_function_map()

    def _create_function_map(self) -> Dict[str, callable]:
        """Create function map for tool execution"""
        function_map = {}

        for tool_name, tool in self.tools.items():
            function_map[tool_name] = self._create_tool_function(tool)

        return function_map

    def _create_tool_function(self, tool: Tool) -> callable:
        """Create a function that executes the tool"""
        async def tool_function(**kwargs):
            try:
                result = await tool.execute(**kwargs)
                return result
            except Exception as e:
                return {"error": str(e)}

        # Set function metadata
        tool_function.__name__ = tool.name
        tool_function.__doc__ = tool.description

        return tool_function

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get information about available tools"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.type,
                        "description": param.description,
                        "required": param.required
                    }
                    for param in tool.parameters
                ]
            }
            for tool in self.tools.values()
        ]

# Usage
agent = ToolEnabledAgent(
    name="ToolAgent",
    tools=[search_tool, analysis_tool, email_tool],
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="""You are an agent with access to various tools.
    Use the appropriate tools to accomplish tasks effectively."""
)

# The agent can now use tools via function calling
```

## Tool Performance Monitoring

```python
class ToolMonitor:
    def __init__(self):
        self.metrics = {}
        self.alerts = []

    def record_tool_usage(self, tool_name: str, execution_time: float, success: bool, error: str = None):
        """Record tool usage metrics"""
        if tool_name not in self.metrics:
            self.metrics[tool_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "total_execution_time": 0,
                "average_execution_time": 0,
                "errors": []
            }

        metrics = self.metrics[tool_name]
        metrics["total_calls"] += 1
        metrics["total_execution_time"] += execution_time
        metrics["average_execution_time"] = metrics["total_execution_time"] / metrics["total_calls"]

        if success:
            metrics["successful_calls"] += 1
        else:
            metrics["failed_calls"] += 1
            if error:
                metrics["errors"].append(error)

        # Check for performance issues
        self._check_performance_alerts(tool_name, execution_time, success)

    def _check_performance_alerts(self, tool_name: str, execution_time: float, success: bool):
        """Check for performance issues and create alerts"""
        if execution_time > 30:  # Slow execution
            self.alerts.append({
                "type": "slow_execution",
                "tool": tool_name,
                "execution_time": execution_time,
                "timestamp": time.time()
            })

        if not success and len(self.metrics[tool_name]["errors"]) > 5:
            self.alerts.append({
                "type": "high_error_rate",
                "tool": tool_name,
                "error_count": len(self.metrics[tool_name]["errors"]),
                "timestamp": time.time()
            })

    def get_tool_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        report = {}

        for tool_name, metrics in self.metrics.items():
            success_rate = metrics["successful_calls"] / metrics["total_calls"] if metrics["total_calls"] > 0 else 0

            report[tool_name] = {
                "total_calls": metrics["total_calls"],
                "success_rate": success_rate,
                "average_execution_time": metrics["average_execution_time"],
                "error_count": len(metrics["errors"]),
                "performance_score": self._calculate_performance_score(metrics, success_rate)
            }

        return report

    def _calculate_performance_score(self, metrics: Dict[str, Any], success_rate: float) -> float:
        """Calculate overall performance score"""
        execution_score = max(0, 1 - (metrics["average_execution_time"] / 10))  # Better if faster
        reliability_score = success_rate
        usage_score = min(1, metrics["total_calls"] / 100)  # Better if more used

        return (execution_score + reliability_score + usage_score) / 3

# Usage
monitor = ToolMonitor()

# Record tool usage
monitor.record_tool_usage("web_search", 2.5, True)
monitor.record_tool_usage("database_query", 15.2, False, "Connection timeout")

# Get performance report
report = monitor.get_tool_performance_report()
print("Tool Performance Report:", report)
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Tool Fundamentals** - Tool definition, structure, and registry
2. **Web Tools** - Search tools and web scraping capabilities
3. **Data Processing Tools** - Analysis and database query tools
4. **Communication Tools** - Email and Slack integration
5. **File System Tools** - File operations with security
6. **Tool Integration with Agents** - Function calling and tool-enabled agents
7. **Tool Performance Monitoring** - Metrics and performance tracking

## Next Steps

Now that you understand tool integration, let's explore task decomposition strategies. In [Chapter 5: Task Decomposition](05-task-decomposition.md), we'll learn how agents break complex tasks into manageable subtasks and coordinate their execution.

---

**Practice what you've learned:**
1. Create a custom tool for your specific use case
2. Build a tool-enabled agent with multiple capabilities
3. Implement tool performance monitoring and alerting
4. Set up a tool registry with different categories of tools

*What kind of tool would you create first for your agent?* 🔧

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `name`, `Dict` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Tool Integration` as an operating subsystem inside **Microsoft AutoGen Tutorial: Building Multi-Agent AI Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `tool`, `path`, `metrics` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Tool Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `name` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Dict`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `name` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Agent Communication](03-agent-communication.md)
- [Next Chapter: Chapter 5: Task Decomposition](05-task-decomposition.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
