---
layout: default
title: "OpenHands Tutorial - Chapter 2: Basic Operations"
nav_order: 2
has_children: false
parent: OpenHands Tutorial
---

# Chapter 2: Basic Operations - Files, Commands, and Environments

Welcome to **Chapter 2: Basic Operations - Files, Commands, and Environments**. In this part of **OpenHands Tutorial: Autonomous Software Engineering Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master file operations, command execution, environment management, and workspace navigation with OpenHands.

## Overview

OpenHands provides comprehensive capabilities for working with files, executing commands, and managing development environments. This chapter covers the fundamental operations that form the building blocks of autonomous software development.

## File Operations

### Reading and Writing Files

```python
from openhands import OpenHands
from openhands.workspace import Workspace

# Initialize OpenHands with workspace
openhands = OpenHands()
workspace = Workspace("./project_workspace")

# Create and write to files
result = openhands.run("""
Create a Python script that:
1. Defines a Person class with name and age attributes
2. Includes methods for greeting and age calculation
3. Creates example instances and demonstrates usage
""", workspace=workspace)

# Check what files were created
print("Files created:")
for file_path in result.files_created:
    print(f"  - {file_path}")

# Read the generated file
if result.files_created:
    file_content = workspace.read_file(result.files_created[0])
    print(f"\nGenerated code:\n{file_content}")
```

### File System Navigation

```python
# Directory operations
workspace_ops = OpenHands()

# Create project structure
structure_result = workspace_ops.run("""
Create a complete Python project structure with:
- src/ directory with main.py and utils.py
- tests/ directory with test_main.py
- requirements.txt file
- README.md with project description
- .gitignore file
""")

# List directory contents
def explore_workspace(ws_path="./project_workspace"):
    """Recursively explore workspace structure"""
    import os

    def print_tree(path, prefix=""):
        if os.path.isfile(path):
            print(f"{prefix}📄 {os.path.basename(path)}")
        elif os.path.isdir(path):
            print(f"{prefix}📁 {os.path.basename(path)}/")
            try:
                items = sorted(os.listdir(path))
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    new_prefix = prefix + ("└── " if is_last else "├── ")
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(os.path.join(path, item), next_prefix)
            except PermissionError:
                print(f"{prefix}    [Permission denied]")

    print_tree(ws_path)

explore_workspace()
```

### File Modification and Refactoring

```python
# Modify existing files
modification_agent = OpenHands()

# Start with a basic script
initial_result = modification_agent.run("""
Create a simple calculator.py script with basic arithmetic operations:
- add(a, b)
- subtract(a, b)
- multiply(a, b)
- divide(a, b)
""")

# Now enhance it with additional features
enhancement_result = modification_agent.run("""
Enhance the calculator.py script by adding:
1. Input validation for all functions
2. Support for multiple numbers (add(1, 2, 3, 4))
3. Error handling for division by zero
4. A Calculator class wrapper
5. History tracking for operations
6. Unit tests in a separate file
""")

print("Enhanced calculator with:")
print("- Input validation")
print("- Multiple argument support")
print("- Error handling")
print("- Class wrapper")
print("- History tracking")
print("- Unit tests")
```

## Command Execution

### Running System Commands

```python
from openhands import OpenHands

# Command execution agent
cmd_agent = OpenHands()

# Execute various commands
commands_result = cmd_agent.run("""
Execute a series of commands to set up a Python development environment:
1. Check Python version
2. Create virtual environment
3. Activate virtual environment
4. Install common packages (requests, pytest, black)
5. Run a simple test to verify installation
6. Display environment information
""")

# The agent will handle:
# - Command execution in proper order
# - Environment management
# - Error handling
# - Output parsing
```

### Package Management

```python
# Package installation and management
pkg_agent = OpenHands()

# Install and manage Python packages
package_result = pkg_agent.run("""
Set up a complete Python data science environment:
1. Create requirements.txt with essential packages
2. Install packages: numpy, pandas, matplotlib, scikit-learn, jupyter
3. Create a virtual environment
4. Install packages in the virtual environment
5. Test imports to verify installation
6. Generate a setup script for future installations
""")

# Check installed packages
verification_result = pkg_agent.run("""
Verify the data science environment by:
1. Listing installed packages
2. Running a simple data analysis script
3. Creating a Jupyter notebook example
4. Testing matplotlib plotting capabilities
""")
```

### Build and Compilation

```python
# Build system management
build_agent = OpenHands()

# Handle different build systems
python_build = build_agent.run("""
Create a Python package with proper build configuration:
1. Setup.py with package metadata
2. MANIFEST.in for package data
3. Build the package (python setup.py build)
4. Create source distribution (python setup.py sdist)
5. Create wheel distribution (python setup.py bdist_wheel)
6. Show the build artifacts
""")

# JavaScript/Node.js build
js_build = build_agent.run("""
Create a Node.js project with modern build setup:
1. package.json with dependencies and scripts
2. src/ and dist/ directories
3. TypeScript configuration
4. Webpack or Vite build configuration
5. Build the project
6. Start development server
""")
```

## Environment Management

### Virtual Environment Handling

```python
# Virtual environment management
venv_agent = OpenHands()

# Comprehensive environment setup
env_result = venv_agent.run("""
Create a complete development environment setup:
1. Python virtual environment management script
2. Node.js environment setup
3. Docker environment for containerized development
4. Environment activation scripts
5. Dependency management across environments
6. Environment switching utilities
""")

# Environment switching
switch_result = venv_agent.run("""
Create environment switching utilities:
1. Script to switch between Python virtual environments
2. Node.js version management
3. Docker container management
4. Environment variable management
5. Path management for different tools
""")
```

### Multi-Language Support

```python
# Multi-language environment management
multi_lang_agent = OpenHands()

# Handle multiple programming languages
polyglot_result = multi_lang_agent.run("""
Create a polyglot project with multiple languages:
1. Python backend with FastAPI
2. JavaScript/TypeScript frontend with React
3. Go microservice for data processing
4. Rust library for performance-critical code
5. Docker Compose for orchestration
6. Shared build and deployment scripts
""")

# Language-specific operations
python_ops = multi_lang_agent.run("""
Python-specific operations:
1. Virtual environment management
2. Package installation and dependency resolution
3. Code formatting with black
4. Linting with flake8
5. Testing with pytest
6. Documentation generation
""")

js_ops = multi_lang_agent.run("""
JavaScript/TypeScript operations:
1. Node.js version management
2. npm/yarn dependency management
3. TypeScript compilation
4. ESLint configuration and execution
5. Jest testing framework setup
6. Build optimization with Webpack/Vite
""")
```

## Process Management

### Running Background Processes

```python
# Background process management
process_agent = OpenHands()

# Web server management
server_result = process_agent.run("""
Create and manage a web development server:
1. FastAPI server with auto-reload
2. React development server
3. Database server (SQLite/PostgreSQL)
4. Background job processor
5. Process monitoring and health checks
6. Graceful shutdown handling
""")

# Long-running process management
long_running = process_agent.run("""
Handle long-running processes:
1. Background job queues (Celery, RQ)
2. WebSocket servers for real-time communication
3. File processing pipelines
4. Data streaming applications
5. Monitoring and logging for long-running processes
6. Process lifecycle management
""")
```

### Process Monitoring and Control

```python
# Process monitoring and control
monitor_agent = OpenHands()

# Comprehensive process management
monitoring_result = monitor_agent.run("""
Implement process monitoring and control:
1. Process status checking
2. Resource usage monitoring (CPU, memory, disk)
3. Log aggregation and analysis
4. Automatic restart on failure
5. Load balancing for multiple instances
6. Health check endpoints
""")

# Process control scripts
control_result = monitor_agent.run("""
Create process control utilities:
1. Start/stop/restart scripts
2. Process grouping and management
3. Dependency management between processes
4. Configuration management for different environments
5. Logging and debugging tools
""")
```

## Error Handling and Recovery

### Robust Command Execution

```python
# Error handling in command execution
robust_agent = OpenHands()

# Commands with error handling
error_handling = robust_agent.run("""
Create robust command execution with error handling:
1. Command retry logic with exponential backoff
2. Partial failure recovery
3. Command timeout handling
4. Output parsing with error detection
5. Fallback command execution
6. Detailed error reporting and logging
""")

# Recovery strategies
recovery_result = robust_agent.run("""
Implement recovery strategies for failed operations:
1. Automatic rollback mechanisms
2. State checkpointing and restoration
3. Incremental progress saving
4. Alternative approach selection
5. User notification and intervention points
6. Recovery procedure documentation
""")
```

### Debugging and Troubleshooting

```python
# Debugging and troubleshooting
debug_agent = OpenHands()

# Debug environment issues
debug_result = debug_agent.run("""
Create debugging and troubleshooting tools:
1. Environment inspection scripts
2. Dependency conflict resolution
3. Log analysis tools
4. Performance profiling utilities
5. Error reproduction scripts
6. Diagnostic information collection
""")

# Troubleshooting workflows
troubleshoot_result = debug_agent.run("""
Implement troubleshooting workflows:
1. Step-by-step diagnostic procedures
2. Common issue identification and fixes
3. Automated problem detection
4. Solution recommendation system
5. Documentation of known issues and solutions
""")
```

## Security and Permissions

### Safe File Operations

```python
# Security-conscious file operations
secure_agent = OpenHands()

# Secure file handling
secure_files = secure_agent.run("""
Implement secure file operations:
1. Path traversal protection
2. File permission management
3. Safe file content validation
4. Quarantine for suspicious files
5. Backup and recovery mechanisms
6. Audit logging for file operations
""")

# Permission management
permissions_result = secure_agent.run("""
Create permission management system:
1. User and group permission models
2. File access control lists
3. Operation logging and monitoring
4. Permission validation decorators
5. Role-based access control
6. Security policy enforcement
""")
```

### Sandboxed Execution

```python
# Sandboxed environment management
sandbox_agent = OpenHands()

# Sandbox configuration and management
sandbox_result = sandbox_agent.run("""
Implement sandboxed execution environment:
1. Isolated execution containers
2. Resource limitation and monitoring
3. Network access control
4. File system isolation
5. System call filtering
6. Security policy enforcement
""")

# Sandbox management tools
sandbox_mgmt = sandbox_agent.run("""
Create sandbox management utilities:
1. Sandbox creation and configuration
2. Resource allocation and monitoring
3. Security policy management
4. Access logging and analysis
5. Cleanup and maintenance scripts
6. Integration with CI/CD pipelines
""")
```

## Performance Optimization

### Efficient File Operations

```python
# Optimized file operations
perf_agent = OpenHands()

# High-performance file handling
optimized_files = perf_agent.run("""
Implement optimized file operations:
1. Asynchronous file I/O
2. Memory-mapped file operations
3. Streaming for large files
4. Concurrent file processing
5. Caching mechanisms
6. Compression and archiving
""")

# Batch operations
batch_ops = perf_agent.run("""
Create batch operation utilities:
1. Bulk file processing
2. Parallel command execution
3. Transaction-like file operations
4. Progress tracking and reporting
5. Error aggregation and handling
6. Performance monitoring
""")
```

### Resource Management

```python
# Resource optimization
resource_agent = OpenHands()

# Resource management and optimization
resource_mgmt = resource_agent.run("""
Implement comprehensive resource management:
1. CPU and memory monitoring
2. Disk space management
3. Network bandwidth optimization
4. Process scheduling optimization
5. Resource allocation policies
6. Performance bottleneck identification
""")

# Optimization strategies
optimization_result = resource_agent.run("""
Create optimization strategies:
1. Memory-efficient data structures
2. CPU cache optimization
3. I/O operation batching
4. Lazy loading and evaluation
5. Resource pooling and reuse
6. Performance profiling and analysis
""")
```

## Integration with Development Tools

### Version Control Integration

```python
# Git and version control integration
vcs_agent = OpenHands()

# Git operations and workflows
git_integration = vcs_agent.run("""
Implement Git integration and workflows:
1. Repository initialization and management
2. Commit, push, pull operations
3. Branch management and merging
4. Conflict resolution assistance
5. Git hook integration
6. Release management and tagging
""")

# Advanced Git workflows
git_workflows = vcs_agent.run("""
Create advanced Git workflow utilities:
1. Feature branch workflows
2. Pull request management
3. Code review automation
4. Release branching strategies
5. GitOps deployment pipelines
6. Repository analytics and reporting
""")
```

### IDE and Editor Integration

```python
# Development environment integration
ide_agent = OpenHands()

# IDE integration features
ide_integration = ide_agent.run("""
Implement IDE and editor integration:
1. Code formatting and linting
2. Intelligent code completion
3. Refactoring tools integration
4. Debugging support and breakpoints
5. Test integration and running
6. Project navigation and search
""")

# Editor automation
editor_automation = ide_agent.run("""
Create editor automation features:
1. Code generation from templates
2. Automated refactoring operations
3. Code analysis and suggestions
4. Documentation generation
5. Configuration file management
6. Plugin and extension management
""")
```

## Summary

In this chapter, we've covered:

- **File Operations** - Reading, writing, modifying, and organizing files
- **Command Execution** - Running system commands, package management, and builds
- **Environment Management** - Virtual environments, multi-language support, and isolation
- **Process Management** - Background processes, monitoring, and control
- **Error Handling** - Robust execution, debugging, and recovery strategies
- **Security** - Safe operations, permissions, and sandboxed execution
- **Performance** - Optimized operations and resource management
- **Tool Integration** - Version control, IDE integration, and development workflows

These basic operations form the foundation for OpenHands' autonomous software development capabilities.

## Key Takeaways

1. **Comprehensive Operations**: OpenHands can handle files, commands, environments, and processes
2. **Security First**: Sandboxed execution and permission management protect systems
3. **Performance Aware**: Optimized operations for efficient resource usage
4. **Error Resilient**: Robust error handling and recovery mechanisms
5. **Tool Agnostic**: Support for multiple languages, frameworks, and development tools

Next, we'll explore **code generation** - OpenHands' ability to create high-quality, functional code from natural language descriptions.

---

**Ready for the next chapter?** [Chapter 3: Code Generation](03-code-generation.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `management`, `Create`, `OpenHands` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Basic Operations - Files, Commands, and Environments` as an operating subsystem inside **OpenHands Tutorial: Autonomous Software Engineering Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `environment`, `file`, `operations` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Basic Operations - Files, Commands, and Environments` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `management`.
2. **Input normalization**: shape incoming data so `Create` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `OpenHands`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [OpenHands Repository](https://github.com/OpenHands/OpenHands)
  Why it matters: authoritative reference on `OpenHands Repository` (github.com).
- [OpenHands Docs](https://docs.openhands.dev/)
  Why it matters: authoritative reference on `OpenHands Docs` (docs.openhands.dev).
- [OpenHands Releases](https://github.com/OpenHands/OpenHands/releases)
  Why it matters: authoritative reference on `OpenHands Releases` (github.com).

Suggested trace strategy:
- search upstream code for `management` and `Create` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with OpenHands](01-getting-started.md)
- [Next Chapter: Chapter 3: Code Generation - Creating Production-Ready Code](03-code-generation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
