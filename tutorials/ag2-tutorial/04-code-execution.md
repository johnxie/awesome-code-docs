---
layout: default
title: "AG2 Tutorial - Chapter 4: Code Execution"
nav_order: 4
has_children: false
parent: AG2 Tutorial
---

# Chapter 4: Code Execution & Security

> Learn how to safely execute code within AG2 conversations using Docker sandboxing and security best practices.

## Overview

Code execution is a powerful feature that allows agents to run code, test implementations, and interact with the real world. AG2 provides secure code execution through Docker containers to prevent system compromise.

## Docker-Based Code Execution

### Basic Setup

```python
from ag2 import UserProxyAgent

# Safe code execution with Docker
code_executor = UserProxyAgent(
    name="code_executor",
    human_input_mode="NEVER",  # Fully autonomous
    code_execution_config={
        "work_dir": "workspace",     # Working directory
        "use_docker": True,          # Enable Docker sandboxing
        "timeout": 60,               # 60 second timeout
        "last_n_messages": 3         # Use last 3 messages for context
    }
)
```

### Advanced Configuration

```python
# Advanced code execution configuration
advanced_executor = UserProxyAgent(
    name="advanced_executor",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding_workspace",
        "use_docker": True,
        "timeout": 120,                      # 2 minute timeout
        "last_n_messages": 5,               # More context
        "docker_image": "python:3.9-slim",  # Custom Docker image
        "docker_container_name": "ag2_code_executor",
        "docker_run_args": ["--rm", "--network", "none"],  # Security args
    }
)
```

## Security Considerations

### Docker Sandboxing

```python
# Secure Docker configuration
secure_executor = UserProxyAgent(
    name="secure_executor",
    code_execution_config={
        "use_docker": True,
        "docker_image": "python:3.9-slim",
        "docker_run_args": [
            "--rm",                    # Remove container after execution
            "--network", "none",       # No network access
            "--read-only",             # Read-only root filesystem
            "--tmpfs", "/tmp",         # Temporary writable directory
            "--memory", "512m",        # Memory limit
            "--cpus", "0.5",           # CPU limit
            "--cap-drop", "ALL",       # Drop all capabilities
            "--security-opt", "no-new-privileges:true"
        ],
        "timeout": 30
    }
)
```

### Code Validation

```python
class SecureCodeExecutor(UserProxyAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.forbidden_patterns = [
            "import os", "import subprocess", "import sys",
            "exec(", "eval(", "open(", "file(",
            "__import__", "globals()", "locals()"
        ]

    def validate_code(self, code):
        """Validate code for security issues"""
        for pattern in self.forbidden_patterns:
            if pattern in code:
                raise SecurityError(f"Potentially unsafe code detected: {pattern}")

        # Check for network-related imports
        network_imports = ["requests", "urllib", "socket", "http"]
        for imp in network_imports:
            if f"import {imp}" in code or f"from {imp}" in code:
                raise SecurityError(f"Network access not allowed: {imp}")

        return True

    def execute_code(self, code, **kwargs):
        """Override execute_code with validation"""
        self.validate_code(code)
        return super().execute_code(code, **kwargs)

secure_executor = SecureCodeExecutor(
    name="secure_executor",
    code_execution_config={
        "use_docker": True,
        "timeout": 30
    }
)
```

## Code Execution Examples

### Python Code Execution

```python
from ag2 import AssistantAgent, UserProxyAgent

# Create agents
assistant = AssistantAgent(
    name="coding_assistant",
    system_message="""You are a Python programming expert.
    Write clean, efficient code and explain your solutions.""",
    llm_config=llm_config
)

code_executor = UserProxyAgent(
    name="code_executor",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "python_workspace",
        "use_docker": True
    }
)

# Execute Python code
code_executor.initiate_chat(
    assistant,
    message="""Write and test a Python function that:
    1. Takes a list of numbers
    2. Returns the median value
    3. Handles edge cases (empty list, even/odd length)"""
)
```

### Data Analysis Example

```python
# Data analysis with code execution
data_analyst = AssistantAgent(
    name="data_analyst",
    system_message="""You are a data analysis expert.
    Use pandas, numpy, and matplotlib for data analysis.""",
    llm_config=llm_config
)

analysis_executor = UserProxyAgent(
    name="analysis_executor",
    code_execution_config={
        "work_dir": "data_workspace",
        "use_docker": "python:3.9-slim",  # Image with data science packages
        "timeout": 300  # 5 minutes for data processing
    }
)

# Analyze sample data
analysis_executor.initiate_chat(
    data_analyst,
    message="""Create a sample dataset and perform analysis:
    1. Generate 1000 random data points
    2. Calculate basic statistics
    3. Create visualizations
    4. Identify patterns or outliers"""
)
```

### Web Scraping Example

```python
# Web scraping with security restrictions
web_scraper = AssistantAgent(
    name="web_scraper",
    system_message="""You are a web scraping expert.
    Use beautifulsoup4 and requests for data extraction.""",
    llm_config=llm_config
)

# Note: Network access is restricted in Docker
# This example shows the concept but won't work without network
scraper_executor = UserProxyAgent(
    name="scraper_executor",
    code_execution_config={
        "work_dir": "scraping_workspace",
        "use_docker": True,
        "timeout": 60
    }
)

# Attempt web scraping (will fail due to network restrictions)
scraper_executor.initiate_chat(
    web_scraper,
    message="Scrape weather data from a public API"
)
```

## Multi-Language Support

### Shell Script Execution

```python
# Shell script executor
shell_executor = UserProxyAgent(
    name="shell_executor",
    code_execution_config={
        "work_dir": "shell_workspace",
        "use_docker": "ubuntu:20.04",
        "timeout": 30
    }
)

shell_assistant = AssistantAgent(
    name="shell_assistant",
    system_message="""You are a shell scripting expert.
    Write bash scripts for common tasks.""",
    llm_config=llm_config
)

shell_executor.initiate_chat(
    shell_assistant,
    message="Write a bash script to backup files older than 7 days"
)
```

### JavaScript/Node.js Execution

```python
# JavaScript executor
js_executor = UserProxyAgent(
    name="js_executor",
    code_execution_config={
        "work_dir": "js_workspace",
        "use_docker": "node:18-slim",
        "timeout": 45
    }
)

js_assistant = AssistantAgent(
    name="js_assistant",
    system_message="""You are a JavaScript expert.
    Write modern ES6+ code with proper error handling.""",
    llm_config=llm_config
)

js_executor.initiate_chat(
    js_assistant,
    message="Create a Node.js script to process JSON data from stdin"
)
```

## Error Handling and Debugging

### Execution Error Handling

```python
class RobustCodeExecutor(UserProxyAgent):
    def __init__(self, max_retries=3, **kwargs):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.execution_history = []

    def execute_code_with_retry(self, code, assistant_agent):
        """Execute code with retry logic"""
        for attempt in range(self.max_retries):
            try:
                result = self.initiate_chat(
                    assistant_agent,
                    message=f"Execute this code and debug if needed:\n\n```python\n{code}\n```",
                    max_turns=5
                )

                # Check if execution was successful
                if "error" not in result.lower() and "exception" not in result.lower():
                    self.execution_history.append({
                        "attempt": attempt + 1,
                        "success": True,
                        "result": result
                    })
                    return result

            except Exception as e:
                self.execution_history.append({
                    "attempt": attempt + 1,
                    "success": False,
                    "error": str(e)
                })
                continue

        # If all retries failed, ask for debugging help
        debug_result = self.initiate_chat(
            assistant_agent,
            message=f"Debug this code that failed after {self.max_retries} attempts:\n\n```python\n{code}\n```\n\nExecution history: {self.execution_history}"
        )

        return debug_result

robust_executor = RobustCodeExecutor(
    name="robust_executor",
    max_retries=3,
    code_execution_config={
        "use_docker": True,
        "timeout": 60
    }
)
```

### Code Debugging Assistant

```python
debug_assistant = AssistantAgent(
    name="debug_assistant",
    system_message="""You are an expert debugger. When code fails:
    1. Analyze the error message
    2. Identify the root cause
    3. Suggest specific fixes
    4. Provide corrected code
    5. Explain the fix""",
    llm_config=llm_config
)

# Error-prone code example
buggy_code = """
def divide_numbers(a, b):
    return a / b

# This will cause ZeroDivisionError
result = divide_numbers(10, 0)
print(result)
"""

# Debug the code
robust_executor.execute_code_with_retry(buggy_code, debug_assistant)
```

## Performance Optimization

### Resource Management

```python
class OptimizedExecutor(UserProxyAgent):
    def __init__(self, resource_limits=None, **kwargs):
        super().__init__(**kwargs)
        self.resource_limits = resource_limits or {
            "memory": "1g",
            "cpu": "1.0",
            "timeout": 300
        }
        self.execution_stats = []

    def optimize_execution(self, code_complexity):
        """Adjust resource limits based on code complexity"""
        if code_complexity == "simple":
            limits = {"memory": "256m", "cpu": "0.5", "timeout": 30}
        elif code_complexity == "medium":
            limits = {"memory": "512m", "cpu": "1.0", "timeout": 120}
        else:  # complex
            limits = {"memory": "1g", "cpu": "2.0", "timeout": 600}

        return limits

    def execute_with_monitoring(self, code, complexity="medium"):
        """Execute code with performance monitoring"""
        import time
        start_time = time.time()

        limits = self.optimize_execution(complexity)

        # Update Docker configuration
        self.code_execution_config.update({
            "docker_run_args": [
                "--memory", limits["memory"],
                "--cpus", str(limits["cpu"])
            ],
            "timeout": limits["timeout"]
        })

        result = self.execute_code(code)

        execution_time = time.time() - start_time

        self.execution_stats.append({
            "complexity": complexity,
            "execution_time": execution_time,
            "memory_limit": limits["memory"],
            "cpu_limit": limits["cpu"],
            "timeout": limits["timeout"],
            "success": "error" not in result.lower()
        })

        return result

optimized_executor = OptimizedExecutor(
    name="optimized_executor",
    code_execution_config={
        "use_docker": True,
        "work_dir": "optimized_workspace"
    }
)
```

### Caching and Reuse

```python
class CachingExecutor(UserProxyAgent):
    def __init__(self, cache_dir="code_cache", **kwargs):
        super().__init__(**kwargs)
        self.cache_dir = cache_dir
        self.code_cache = {}
        self.result_cache = {}

    def get_cache_key(self, code):
        """Generate cache key from code"""
        import hashlib
        return hashlib.md5(code.encode()).hexdigest()

    def check_cache(self, code):
        """Check if code result is cached"""
        cache_key = self.get_cache_key(code)
        if cache_key in self.result_cache:
            return self.result_cache[cache_key]
        return None

    def cache_result(self, code, result):
        """Cache execution result"""
        cache_key = self.get_cache_key(code)
        self.result_cache[cache_key] = result
        self.code_cache[cache_key] = code

    def execute_with_cache(self, code):
        """Execute code with caching"""
        # Check cache first
        cached_result = self.check_cache(code)
        if cached_result:
            return f"[CACHED RESULT]\n{cached_result}"

        # Execute and cache
        result = self.execute_code(code)
        self.cache_result(code, result)

        return result

caching_executor = CachingExecutor(
    name="caching_executor",
    cache_dir="execution_cache",
    code_execution_config={
        "use_docker": True,
        "timeout": 60
    }
)
```

## Testing and Validation

### Code Testing Framework

```python
class TestingExecutor(UserProxyAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.test_results = []

    def run_tests(self, code, test_cases):
        """Run test cases against code"""
        test_code = f"""
{code}

# Test execution
import sys
test_results = []

{chr(10).join(test_cases)}

# Print results
for i, result in enumerate(test_results):
    print(f"Test {{i+1}}: {{'PASS' if result else 'FAIL'}}")
"""

        result = self.execute_code(test_code)
        self.test_results.append({
            "code": code,
            "tests": test_cases,
            "result": result
        })

        return result

# Example usage
test_executor = TestingExecutor(
    name="test_executor",
    code_execution_config={"use_docker": True}
)

fibonacci_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

test_cases = [
    "test_results.append(fibonacci(0) == 0)",
    "test_results.append(fibonacci(1) == 1)",
    "test_results.append(fibonacci(5) == 5)",
    "test_results.append(fibonacci(10) == 55)"
]

test_executor.run_tests(fibonacci_code, test_cases)
```

## Best Practices

### Security First
- **Always use Docker** for code execution in production
- **Validate code** before execution
- **Limit resources** (CPU, memory, network)
- **Monitor execution** for suspicious activity

### Performance Optimization
- **Set appropriate timeouts** based on task complexity
- **Use resource limits** to prevent system overload
- **Implement caching** for repeated operations
- **Monitor execution statistics** to identify bottlenecks

### Error Handling
- **Implement retry logic** for transient failures
- **Provide detailed error messages** for debugging
- **Log execution history** for troubleshooting
- **Graceful degradation** when execution fails

### Code Quality
- **Validate input data** before processing
- **Handle edge cases** appropriately
- **Write comprehensive tests** for critical functions
- **Document code behavior** and limitations

## Summary

In this chapter, we've covered:

- **Docker-Based Execution**: Secure code execution with containerization
- **Security Considerations**: Sandboxing, validation, and access controls
- **Multi-Language Support**: Python, shell scripts, JavaScript execution
- **Error Handling**: Retry logic, debugging assistance, and robust execution
- **Performance Optimization**: Resource management, caching, and monitoring
- **Testing Framework**: Automated testing and validation
- **Best Practices**: Security, performance, and quality guidelines

Next, we'll explore **tool integration** - connecting agents to external APIs and services.

---

**Ready for the next chapter?** [Chapter 5: Tool Integration](05-tool-integration.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*