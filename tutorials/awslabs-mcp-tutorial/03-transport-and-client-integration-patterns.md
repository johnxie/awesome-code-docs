---
layout: default
title: "Chapter 3: Transport and Client Integration Patterns"
nav_order: 3
parent: awslabs/mcp Tutorial
---


# Chapter 3: Transport and Client Integration Patterns

Welcome to **Chapter 3: Transport and Client Integration Patterns**. In this part of **awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers integration patterns across IDE and chat MCP clients.

## Learning Goals

- understand default transport assumptions in the ecosystem
- map client configuration differences across hosts
- evaluate when HTTP modes are available for specific servers
- avoid brittle configuration drift across teams

## Integration Rule

Standardize one primary transport/client path per environment first, then add alternative modes only when you have a concrete operational requirement.

## Source References

- [Repository README Transport Section](https://github.com/awslabs/mcp/blob/main/README.md)
- [AWS API MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-api-mcp-server/README.md)
- [AWS Documentation MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-documentation-mcp-server/README.md)

## Summary

You now have a repeatable integration pattern for client configuration and transport selection.

Next: [Chapter 4: Infrastructure and IaC Workflows](04-infrastructure-and-iac-workflows.md)

## Source Code Walkthrough

### `scripts/verify_tool_names.py`

The `calculate_fully_qualified_name` function in [`scripts/verify_tool_names.py`](https://github.com/awslabs/mcp/blob/HEAD/scripts/verify_tool_names.py) handles a key part of this chapter's functionality:

```py


def calculate_fully_qualified_name(server_name: str, tool_name: str) -> str:
    """Calculate the fully qualified tool name as used by MCP clients.

    Format: awslabs<server_name>___<tool_name>

    Examples:
        awslabs + git_repo_research_mcp_server + ___ + search_repos_on_github
        = awslabsgit_repo_research_mcp_server___search_repos_on_github
    """
    return f'awslabs{server_name}___{tool_name}'


def find_tool_decorators(file_path: Path) -> List[Tuple[str, int]]:
    """Find all tool definitions in a Python file and extract tool names.

    Supports all tool registration patterns:
    - Pattern 1: @mcp.tool(name='tool_name')
    - Pattern 2: @mcp.tool() (uses function name)
    - Pattern 3: app.tool('tool_name')(function)
    - Pattern 4: mcp.tool()(function) (uses function name)
    - Pattern 5: self.mcp.tool(name='tool_name')(function)
    - Pattern 6: @<var>.tool(name='tool_name')

    Returns:
        List of tuples: (tool_name, line_number)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError):
```

This function is important because it defines how awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[calculate_fully_qualified_name]
```
