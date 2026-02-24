---
layout: default
title: "Phidata Tutorial - Chapter 7: Integrations"
nav_order: 7
has_children: false
parent: Phidata Tutorial
---

# Chapter 7: Integrations - Connecting Phidata Agents to External Systems

Welcome to **Chapter 7: Integrations - Connecting Phidata Agents to External Systems**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Integrate Phidata agents with databases, APIs, web services, and enterprise systems for comprehensive automation capabilities.

## Database Integrations

### SQL Database Integration

```python
from phidata.agent import Agent
from phidata.tools import tool
import sqlite3
from typing import List, Dict, Any, Optional
import json

class DatabaseIntegration:
    """Comprehensive database integration for agents."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = None
        self._init_database()

    def _init_database(self):
        """Initialize database with sample schema."""
        with self._get_connection() as conn:
            # Create sample tables
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    department TEXT,
                    hire_date DATE,
                    salary REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    owner_id INTEGER,
                    status TEXT DEFAULT 'active',
                    created_date DATE,
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    project_id INTEGER,
                    assignee_id INTEGER,
                    status TEXT DEFAULT 'todo',
                    priority TEXT DEFAULT 'medium',
                    due_date DATE,
                    FOREIGN KEY (project_id) REFERENCES projects(id),
                    FOREIGN KEY (assignee_id) REFERENCES users(id)
                )
            """)

            # Insert sample data
            self._insert_sample_data(conn)

    def _insert_sample_data(self, conn):
        """Insert sample data for demonstration."""
        users_data = [
            (1, "Alice Johnson", "alice@company.com", "Engineering", "2023-01-15", 95000),
            (2, "Bob Smith", "bob@company.com", "Marketing", "2023-02-20", 75000),
            (3, "Carol Williams", "carol@company.com", "Sales", "2023-03-10", 80000),
            (4, "David Brown", "david@company.com", "Engineering", "2023-04-05", 105000),
            (5, "Eva Davis", "eva@company.com", "HR", "2023-05-12", 70000)
        ]

        projects_data = [
            (1, "AI Chatbot", "Develop an AI-powered customer service chatbot", 1, "active", "2023-06-01"),
            (2, "Mobile App Redesign", "Complete redesign of mobile application", 4, "planning", "2023-07-15"),
            (3, "Data Analytics Platform", "Build comprehensive analytics dashboard", 1, "active", "2023-08-01")
        ]

        tasks_data = [
            (1, "Design chatbot architecture", "Create technical design for chatbot system", 1, 1, "in_progress", "high", "2023-12-15"),
            (2, "Implement NLP processing", "Develop natural language processing pipeline", 1, 4, "todo", "high", "2023-12-20"),
            (3, "Create UI mockups", "Design mobile app user interface", 2, 2, "completed", "medium", "2023-11-30"),
            (4, "Set up analytics infrastructure", "Configure data collection and processing", 3, 1, "in_progress", "high", "2023-12-10")
        ]

        conn.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", users_data)
        conn.executemany("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?, ?, ?)", projects_data)
        conn.executemany("INSERT OR IGNORE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?)", tasks_data)

    def _get_connection(self):
        """Get database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    @tool
    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> str:
        """
        Execute a SQL query and return results.

        Args:
            query: SQL query to execute
            params: Query parameters (optional)

        Returns:
            Query results as formatted string
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params or [])

                if query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    if not rows:
                        return "Query executed successfully. No results returned."

                    # Format results
                    columns = [desc[0] for desc in cursor.description]
                    result_lines = [", ".join(columns)]

                    for row in rows:
                        values = [str(row[col]) for col in columns]
                        result_lines.append(", ".join(values))

                    return "\n".join(result_lines)
                else:
                    conn.commit()
                    return f"Query executed successfully. {conn.total_changes} rows affected."

        except Exception as e:
            return f"Database error: {str(e)}"

    @tool
    def get_table_schema(self, table_name: str) -> str:
        """
        Get schema information for a table.

        Args:
            table_name: Name of the table

        Returns:
            Table schema as string
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                if not columns:
                    return f"Table '{table_name}' not found."

                schema_lines = [f"Table: {table_name}"]
                schema_lines.append("Columns:")

                for col in columns:
                    col_info = f"  - {col[1]} ({col[2]})"
                    if col[3]:  # NOT NULL
                        col_info += " NOT NULL"
                    if col[4]:  # DEFAULT
                        col_info += f" DEFAULT {col[4]}"
                    if col[5]:  # PRIMARY KEY
                        col_info += " PRIMARY KEY"
                    schema_lines.append(col_info)

                return "\n".join(schema_lines)

        except Exception as e:
            return f"Error getting schema: {str(e)}"

    @tool
    def analyze_data(self, table_name: str, column: str) -> str:
        """
        Perform basic data analysis on a table column.

        Args:
            table_name: Name of the table
            column: Column to analyze

        Returns:
            Analysis results as string
        """
        try:
            with self._get_connection() as conn:
                # Get basic statistics
                cursor = conn.execute(f"""
                    SELECT
                        COUNT(*) as total_count,
                        COUNT(DISTINCT {column}) as unique_count,
                        MIN({column}) as min_value,
                        MAX({column}) as max_value,
                        AVG(CAST({column} as REAL)) as avg_value
                    FROM {table_name}
                    WHERE {column} IS NOT NULL
                """)

                stats = cursor.fetchone()

                if not stats:
                    return f"No data found in table '{table_name}' column '{column}'"

                analysis = f"Data Analysis for {table_name}.{column}:\n"
                analysis += f"- Total records: {stats[0]}\n"
                analysis += f"- Unique values: {stats[1]}\n"
                analysis += f"- Min value: {stats[2]}\n"
                analysis += f"- Max value: {stats[3]}\n"
                analysis += f"- Average value: {stats[4]:.2f}\n"

                # Get most common values
                cursor = conn.execute(f"""
                    SELECT {column}, COUNT(*) as count
                    FROM {table_name}
                    WHERE {column} IS NOT NULL
                    GROUP BY {column}
                    ORDER BY count DESC
                    LIMIT 5
                """)

                common_values = cursor.fetchall()
                if common_values:
                    analysis += "\nMost common values:\n"
                    for value, count in common_values:
                        analysis += f"- {value}: {count} times\n"

                return analysis

        except Exception as e:
            return f"Analysis error: {str(e)}"

# Create database integration
db_integration = DatabaseIntegration("./agent_database.db")

# Create database-enabled agent
db_agent = Agent(
    name="DatabaseAgent",
    instructions="""
    You are a database specialist. You can query databases, analyze data,
    and provide insights from structured information. Always explain your
    database operations and their results clearly.
    """,
    model="gpt-4",
    tools=[
        db_integration.execute_query,
        db_integration.get_table_schema,
        db_integration.analyze_data
    ]
)

# Demonstrate database integration
db_queries = [
    "What tables are available in the database?",
    "Show me the schema for the users table",
    "List all active projects with their owners",
    "Analyze the salary distribution in the users table",
    "Find all high-priority tasks that are still todo"
]

print("Database Integration Demonstration:")
for query in db_queries:
    print(f"\nQuery: {query}")
    result = db_agent.run(query)
    print(f"Result: {result}")
    print("-" * 80)
```

## API Integrations

### REST API Integration

```python
from phidata.tools import tool
import aiohttp
import json
from typing import Dict, Any, Optional, List
import asyncio

class APIIntegration:
    """Comprehensive API integration toolkit."""

    def __init__(self, base_url: str = None, headers: Dict[str, str] = None):
        self.base_url = base_url.rstrip('/') if base_url else None
        self.default_headers = headers or {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.default_headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        if self.base_url and not endpoint.startswith(('http://', 'https://')):
            return f"{self.base_url}/{endpoint.lstrip('/')}"
        return endpoint

    @tool
    async def api_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> str:
        """
        Make a GET request to an API endpoint.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers

        Returns:
            API response as formatted string
        """
        try:
            url = self._build_url(endpoint)
            request_headers = {**self.default_headers}
            if headers:
                request_headers.update(headers)

            async with self.session.get(url, params=params, headers=request_headers) as response:
                response_data = await response.json()
                response.headers = dict(response.headers)

                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "data": response_data
                }

                return f"API GET Response:\n{json.dumps(result, indent=2)}"

        except Exception as e:
            return f"API GET Error: {str(e)}"

    @tool
    async def api_post(self, endpoint: str, data: Dict[str, Any],
                      headers: Optional[Dict[str, str]] = None) -> str:
        """
        Make a POST request to an API endpoint.

        Args:
            endpoint: API endpoint
            data: Request body data
            headers: Additional headers

        Returns:
            API response as formatted string
        """
        try:
            url = self._build_url(endpoint)
            request_headers = {**self.default_headers, "Content-Type": "application/json"}
            if headers:
                request_headers.update(headers)

            async with self.session.post(url, json=data, headers=request_headers) as response:
                response_data = await response.json()

                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "data": response_data
                }

                return f"API POST Response:\n{json.dumps(result, indent=2)}"

        except Exception as e:
            return f"API POST Error: {str(e)}"

    @tool
    async def api_put(self, endpoint: str, data: Dict[str, Any],
                     headers: Optional[Dict[str, str]] = None) -> str:
        """
        Make a PUT request to an API endpoint.

        Args:
            endpoint: API endpoint
            data: Request body data
            headers: Additional headers

        Returns:
            API response as formatted string
        """
        try:
            url = self._build_url(endpoint)
            request_headers = {**self.default_headers, "Content-Type": "application/json"}
            if headers:
                request_headers.update(headers)

            async with self.session.put(url, json=data, headers=request_headers) as response:
                response_data = await response.json()

                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers),
                    "data": response_data
                }

                return f"API PUT Response:\n{json.dumps(result, indent=2)}"

        except Exception as e:
            return f"API PUT Error: {str(e)}"

    @tool
    async def api_delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> str:
        """
        Make a DELETE request to an API endpoint.

        Args:
            endpoint: API endpoint
            headers: Additional headers

        Returns:
            API response as formatted string
        """
        try:
            url = self._build_url(endpoint)
            request_headers = {**self.default_headers}
            if headers:
                request_headers.update(headers)

            async with self.session.delete(url, headers=request_headers) as response:
                result = {
                    "status_code": response.status,
                    "headers": dict(response.headers)
                }

                try:
                    response_data = await response.json()
                    result["data"] = response_data
                except:
                    result["data"] = await response.text()

                return f"API DELETE Response:\n{json.dumps(result, indent=2)}"

        except Exception as e:
            return f"API DELETE Error: {str(e)}"

    @tool
    async def test_api_endpoint(self, endpoint: str, method: str = "GET",
                               data: Optional[Dict[str, Any]] = None) -> str:
        """
        Test an API endpoint with different HTTP methods.

        Args:
            endpoint: API endpoint to test
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request data for POST/PUT

        Returns:
            Test results as formatted string
        """
        try:
            url = self._build_url(endpoint)

            result = f"API Endpoint Test: {method} {url}\n"
            result += "=" * 50 + "\n"

            if method.upper() == "GET":
                response_text = await self.api_get(endpoint)
            elif method.upper() == "POST":
                response_text = await self.api_post(endpoint, data or {})
            elif method.upper() == "PUT":
                response_text = await self.api_put(endpoint, data or {})
            elif method.upper() == "DELETE":
                response_text = await self.api_delete(endpoint)
            else:
                return f"Unsupported HTTP method: {method}"

            result += response_text
            return result

        except Exception as e:
            return f"API Test Error: {str(e)}"

# Create API integration
api_integration = APIIntegration(
    base_url="https://jsonplaceholder.typicode.com",
    headers={"User-Agent": "Phidata-Agent/1.0"}
)

# Create API-enabled agent
api_agent = Agent(
    name="APIIntegrationAgent",
    instructions="""
    You are an API integration specialist. You can make HTTP requests to REST APIs,
    test endpoints, and work with JSON data. Always explain what you're doing with APIs
    and format responses clearly.
    """,
    model="gpt-4",
    tools=[
        api_integration.api_get,
        api_integration.api_post,
        api_integration.api_put,
        api_integration.api_delete,
        api_integration.test_api_endpoint
    ]
)

# Demonstrate API integration
async def demonstrate_api_integration():
    async with api_integration:
        api_operations = [
            "Get a list of posts from the JSONPlaceholder API",
            "Test the posts endpoint with GET method",
            "Create a new post using POST method with title 'Test Post' and body 'This is a test'",
            "Test the users endpoint"
        ]

        print("API Integration Demonstration:")
        for operation in api_operations:
            print(f"\nOperation: {operation}")
            result = api_agent.run(operation)
            print(f"Result: {result[:300]}...")
            print("-" * 80)

asyncio.run(demonstrate_api_integration())
```

## Web Scraping Integration

### Web Scraping Tools

```python
from phidata.tools import tool
import aiohttp
from bs4 import BeautifulSoup
import json
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
import re

class WebScrapingIntegration:
    """Web scraping and content extraction tools."""

    def __init__(self, user_agent: str = "Phidata-Agent/1.0"):
        self.user_agent = user_agent
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        headers = {"User-Agent": self.user_agent}
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @tool
    async def scrape_webpage(self, url: str, extract_text: bool = True,
                           extract_links: bool = False, extract_images: bool = False) -> str:
        """
        Scrape content from a webpage.

        Args:
            url: URL to scrape
            extract_text: Extract main text content
            extract_links: Extract all links
            extract_images: Extract image URLs

        Returns:
            Scraped content as formatted string
        """
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return f"HTTP {response.status}: Failed to fetch {url}"

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                result_parts = []

                if extract_text:
                    # Extract main text content
                    for script in soup(["script", "style"]):
                        script.decompose()

                    text = soup.get_text()
                    # Clean up whitespace
                    lines = [line.strip() for line in text.splitlines() if line.strip()]
                    text_content = '\n'.join(lines)

                    result_parts.append(f"TEXT CONTENT:\n{text_content[:1000]}...")

                if extract_links:
                    links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            parsed_url = urlparse(url)
                            href = f"{parsed_url.scheme}://{parsed_url.netloc}{href}"
                        elif not href.startswith(('http://', 'https://')):
                            href = urljoin(url, href)

                        links.append(f"{link.get_text().strip()}: {href}")

                    result_parts.append(f"LINKS ({len(links)}):\n" + '\n'.join(links[:20]))

                if extract_images:
                    images = []
                    for img in soup.find_all('img', src=True):
                        src = img['src']
                        alt = img.get('alt', 'No alt text')

                        # Convert relative URLs
                        if src.startswith('/'):
                            parsed_url = urlparse(url)
                            src = f"{parsed_url.scheme}://{parsed_url.netloc}{src}"
                        elif not src.startswith(('http://', 'https://')):
                            src = urljoin(url, src)

                        images.append(f"{alt}: {src}")

                    result_parts.append(f"IMAGES ({len(images)}):\n" + '\n'.join(images[:10]))

                return f"Scraped content from {url}:\n\n" + '\n\n'.join(result_parts)

        except Exception as e:
            return f"Scraping error: {str(e)}"

    @tool
    async def search_and_scrape(self, query: str, num_results: int = 3) -> str:
        """
        Search for information and scrape relevant pages.

        Args:
            query: Search query
            num_results: Number of pages to scrape

        Returns:
            Combined search and scrape results
        """
        try:
            # This is a simplified implementation
            # In practice, you'd integrate with a search API like SerpApi or Bing Search

            # Mock search results for demonstration
            search_results = [
                {"title": f"Result 1 for {query}", "url": f"https://example.com/result1?q={query.replace(' ', '+')}"},
                {"title": f"Result 2 for {query}", "url": f"https://example.com/result2?q={query.replace(' ', '+')}"},
                {"title": f"Result 3 for {query}", "url": f"https://example.com/result3?q={query.replace(' ', '+')}"}
            ]

            scraped_content = []

            for result in search_results[:num_results]:
                print(f"Scraping: {result['title']}")
                content = await self.scrape_webpage(result['url'], extract_text=True, extract_links=False)
                scraped_content.append(f"## {result['title']}\n{content}")

            return f"Search results for '{query}':\n\n" + '\n\n'.join(scraped_content)

        except Exception as e:
            return f"Search and scrape error: {str(e)}"

    @tool
    async def extract_structured_data(self, url: str, schema: Dict[str, Any]) -> str:
        """
        Extract structured data from a webpage using a schema.

        Args:
            url: URL to scrape
            schema: Schema defining what to extract

        Returns:
            Structured data as JSON
        """
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    return f"HTTP {response.status}: Failed to fetch {url}"

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                extracted_data = {}

                # Extract based on schema
                for field_name, field_config in schema.items():
                    field_type = field_config.get('type', 'text')
                    selector = field_config.get('selector')
                    attribute = field_config.get('attribute')

                    if selector:
                        element = soup.select_one(selector)
                        if element:
                            if attribute:
                                value = element.get(attribute, '')
                            else:
                                value = element.get_text().strip()

                            # Type conversion
                            if field_type == 'number':
                                try:
                                    value = float(value.replace('$', '').replace(',', ''))
                                except:
                                    pass
                            elif field_type == 'boolean':
                                value = bool(value.lower() in ['true', 'yes', '1'])

                            extracted_data[field_name] = value

                return f"Extracted structured data from {url}:\n{json.dumps(extracted_data, indent=2)}"

        except Exception as e:
            return f"Structured extraction error: {str(e)}"

# Create web scraping integration
web_scraper = WebScrapingIntegration()

# Create web scraping agent
scraping_agent = Agent(
    name="WebScrapingAgent",
    instructions="""
    You are a web scraping specialist. You can extract information from websites,
    search for content online, and structure data from web pages. Always respect
    website terms of service and robots.txt when scraping.
    """,
    model="gpt-4",
    tools=[
        web_scraper.scrape_webpage,
        web_scraper.search_and_scrape,
        web_scraper.extract_structured_data
    ]
)

# Demonstrate web scraping integration
async def demonstrate_web_scraping():
    async with web_scraper:
        scraping_tasks = [
            "Scrape the content from https://httpbin.org/html",
            "Extract structured data from a product page with schema: {'title': {'selector': 'h1', 'type': 'text'}, 'price': {'selector': '.price', 'type': 'number'}}"
        ]

        print("Web Scraping Integration Demonstration:")
        for task in scraping_tasks:
            print(f"\nTask: {task}")
            result = scraping_agent.run(task)
            print(f"Result: {result[:500]}...")
            print("-" * 80)

asyncio.run(demonstrate_web_scraping())
```

## File System Integration

### File Operations Tools

```python
from phidata.tools import tool
import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import shutil

class FileSystemIntegration:
    """File system operations and data processing tools."""

    def __init__(self, base_directory: str = "./workspace"):
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(exist_ok=True)

    @tool
    def list_directory(self, path: str = ".", show_hidden: bool = False) -> str:
        """
        List contents of a directory.

        Args:
            path: Directory path (relative to base directory)
            show_hidden: Include hidden files

        Returns:
            Directory listing as formatted string
        """
        try:
            full_path = self.base_directory / path
            full_path = full_path.resolve()

            # Security check - ensure we're within base directory
            if not str(full_path).startswith(str(self.base_directory.resolve())):
                return "Access denied: Cannot access directories outside base directory"

            if not full_path.exists():
                return f"Directory not found: {path}"

            if not full_path.is_dir():
                return f"Not a directory: {path}"

            items = []
            for item in sorted(full_path.iterdir()):
                if not show_hidden and item.name.startswith('.'):
                    continue

                item_type = "DIR" if item.is_dir() else "FILE"
                size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
                items.append(f"{item_type}: {item.name}{size}")

            return f"Contents of {path}:\n" + "\n".join(items)

        except Exception as e:
            return f"Error listing directory: {str(e)}"

    @tool
    def read_file(self, path: str, max_lines: int = 50) -> str:
        """
        Read content from a file.

        Args:
            path: File path (relative to base directory)
            max_lines: Maximum number of lines to read

        Returns:
            File content as string
        """
        try:
            full_path = self.base_directory / path
            full_path = full_path.resolve()

            # Security check
            if not str(full_path).startswith(str(self.base_directory.resolve())):
                return "Access denied: Cannot access files outside base directory"

            if not full_path.exists():
                return f"File not found: {path}"

            if not full_path.is_file():
                return f"Not a file: {path}"

            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            content = "".join(lines[:max_lines])

            if len(lines) > max_lines:
                content += f"\n... ({len(lines) - max_lines} more lines)"

            return f"Content of {path}:\n{content}"

        except UnicodeDecodeError:
            return f"Binary file or encoding error: {path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @tool
    def write_file(self, path: str, content: str, append: bool = False) -> str:
        """
        Write content to a file.

        Args:
            path: File path (relative to base directory)
            content: Content to write
            append: Append to file instead of overwriting

        Returns:
            Success message
        """
        try:
            full_path = self.base_directory / path
            full_path = full_path.resolve()

            # Security check
            if not str(full_path).startswith(str(self.base_directory.resolve())):
                return "Access denied: Cannot write files outside base directory"

            # Ensure parent directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)

            mode = 'a' if append else 'w'
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)

            action = "Appended to" if append else "Written to"
            return f"Successfully {action} file: {path}"

        except Exception as e:
            return f"Error writing file: {str(e)}"

    @tool
    def analyze_csv(self, path: str, max_rows: int = 10) -> str:
        """
        Analyze a CSV file and provide summary statistics.

        Args:
            path: CSV file path
            max_rows: Maximum rows to analyze

        Returns:
            CSV analysis as formatted string
        """
        try:
            full_path = self.base_directory / path
            full_path = full_path.resolve()

            # Security check
            if not str(full_path).startswith(str(self.base_directory.resolve())):
                return "Access denied: Cannot access files outside base directory"

            import csv
            with open(full_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            if not rows:
                return "CSV file is empty or has no data rows"

            analysis = f"CSV Analysis: {path}\n"
            analysis += f"Total rows: {len(rows)}\n"
            analysis += f"Columns: {', '.join(rows[0].keys())}\n\n"

            # Show sample data
            analysis += f"Sample data (first {min(max_rows, len(rows))} rows):\n"
            for i, row in enumerate(rows[:max_rows]):
                analysis += f"Row {i+1}: {dict(row)}\n"

            # Basic statistics for numeric columns
            numeric_cols = []
            for col in rows[0].keys():
                try:
                    float(rows[0][col])
                    numeric_cols.append(col)
                except (ValueError, TypeError):
                    continue

            if numeric_cols:
                analysis += f"\nNumeric column statistics:\n"
                for col in numeric_cols:
                    values = []
                    for row in rows:
                        try:
                            values.append(float(row[col]))
                        except (ValueError, TypeError):
                            continue

                    if values:
                        analysis += f"{col}: min={min(values):.2f}, max={max(values):.2f}, avg={sum(values)/len(values):.2f}\n"

            return analysis

        except Exception as e:
            return f"Error analyzing CSV: {str(e)}"

    @tool
    def search_files(self, pattern: str, path: str = ".", case_sensitive: bool = False) -> str:
        """
        Search for files matching a pattern.

        Args:
            pattern: Search pattern (supports wildcards)
            path: Directory to search in
            case_sensitive: Case sensitive search

        Returns:
            Matching files as formatted string
        """
        try:
            import fnmatch
            import glob

            full_path = self.base_directory / path
            full_path = full_path.resolve()

            # Security check
            if not str(full_path).startswith(str(self.base_directory.resolve())):
                return "Access denied: Cannot search outside base directory"

            # Find all files recursively
            all_files = []
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    all_files.append(os.path.relpath(os.path.join(root, file), self.base_directory))

            # Filter by pattern
            flags = 0 if case_sensitive else fnmatch.FNM_IGNORECASE
            matches = [f for f in all_files if fnmatch.fnmatch(f, pattern, flags=flags)]

            if not matches:
                return f"No files found matching pattern: {pattern}"

            return f"Files matching '{pattern}':\n" + "\n".join(matches[:50])  # Limit results

        except Exception as e:
            return f"Error searching files: {str(e)}"

# Create file system integration
file_system = FileSystemIntegration("./agent_workspace")

# Create file system agent
fs_agent = Agent(
    name="FileSystemAgent",
    instructions="""
    You are a file system specialist. You can read and write files, analyze data,
    search for content, and manage file operations. Always be careful with file
    operations and respect the workspace boundaries.
    """,
    model="gpt-4",
    tools=[
        file_system.list_directory,
        file_system.read_file,
        file_system.write_file,
        file_system.analyze_csv,
        file_system.search_files
    ]
)

# Demonstrate file system integration
fs_operations = [
    "List the contents of the current directory",
    "Create a new file called 'notes.txt' with some sample content",
    "Read the content of 'notes.txt'",
    "Search for all .txt files in the workspace"
]

print("File System Integration Demonstration:")
for operation in fs_operations:
    print(f"\nOperation: {operation}")
    result = fs_agent.run(operation)
    print(f"Result: {result}")
    print("-" * 80)
```

This comprehensive integrations chapter demonstrates how Phidata agents can connect with databases, APIs, web services, and file systems to perform complex automation tasks across multiple systems. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `headers`, `endpoint` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Integrations - Connecting Phidata Agents to External Systems` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `path`, `full_path` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Integrations - Connecting Phidata Agents to External Systems` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `headers` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `endpoint`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `headers` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving](06-advanced-reasoning.md)
- [Next Chapter: Chapter 8: Production Deployment & Scaling Phidata Agents](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
