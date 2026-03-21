---
layout: default
title: "Chapter 5: Data, Knowledge, and Agent Workflows"
nav_order: 5
parent: awslabs/mcp Tutorial
---


# Chapter 5: Data, Knowledge, and Agent Workflows

Welcome to **Chapter 5: Data, Knowledge, and Agent Workflows**. In this part of **awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how documentation and data-oriented servers improve context quality for coding and operations agents.

## Learning Goals

- use documentation/knowledge servers to reduce stale-model assumptions
- combine data-oriented servers for richer troubleshooting and planning
- structure workflows that separate retrieval from action execution
- choose server combinations by task complexity and risk

## Workflow Pattern

Use knowledge and documentation servers first to build accurate context, then invoke mutating or operational servers only after intent and constraints are clear.

## Source References

- [AWS Documentation MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-documentation-mcp-server/README.md)
- [Repository README Knowledge/Data Sections](https://github.com/awslabs/mcp/blob/main/README.md)
- [Samples README](https://github.com/awslabs/mcp/blob/main/samples/README.md)

## Summary

You now have a context-first approach for data and knowledge enriched MCP workflows.

Next: [Chapter 6: Security, Credentials, and Risk Controls](06-security-credentials-and-risk-controls.md)

## Source Code Walkthrough

### `scripts/verify_tool_names.py`

The `find_all_tools_in_package` function in [`scripts/verify_tool_names.py`](https://github.com/awslabs/mcp/blob/HEAD/scripts/verify_tool_names.py) handles a key part of this chapter's functionality:

```py


def find_all_tools_in_package(package_dir: Path) -> List[Tuple[str, Path, int]]:
    """Find all tool definitions in a package directory.

    Returns:
        List of tuples: (tool_name, file_path, line_number)
    """
    all_tools = []

    # Search for Python files in the package
    for python_file in package_dir.rglob('*.py'):
        # Skip test files and virtual environments
        if (
            'test' in str(python_file)
            or '.venv' in str(python_file)
            or '__pycache__' in str(python_file)
        ):
            continue

        tools = find_tool_decorators(python_file)
        for tool_name, line_number in tools:
            all_tools.append((tool_name, python_file, line_number))

    return all_tools


def validate_tool_name(tool_name: str) -> Tuple[List[str], List[str]]:
    """Validate a tool name against naming conventions.

    Returns:
        Tuple of (errors, warnings)
```

This function is important because it defines how awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[find_all_tools_in_package]
```
