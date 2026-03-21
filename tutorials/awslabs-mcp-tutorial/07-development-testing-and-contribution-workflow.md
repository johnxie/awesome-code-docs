---
layout: default
title: "Chapter 7: Development, Testing, and Contribution Workflow"
nav_order: 7
parent: awslabs/mcp Tutorial
---


# Chapter 7: Development, Testing, and Contribution Workflow

Welcome to **Chapter 7: Development, Testing, and Contribution Workflow**. In this part of **awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on contributor workflows in the monorepo.

## Learning Goals

- set up local tooling and pre-commit quality gates
- run server-level unit/integration tests reliably
- align docs updates with server changes
- prepare pull requests that satisfy repository standards

## Contribution Workflow

Adopt the repository pre-commit and test pipeline locally before opening PRs. Keep server changes, tests, and docs synchronized to reduce review churn.

## Source References

- [Developer Guide](https://github.com/awslabs/mcp/blob/main/DEVELOPER_GUIDE.md)
- [Design Guidelines](https://github.com/awslabs/mcp/blob/main/DESIGN_GUIDELINES.md)
- [Contributing](https://github.com/awslabs/mcp/blob/main/CONTRIBUTING.md)

## Summary

You now have a reliable workflow for shipping server changes in the `awslabs/mcp` ecosystem.

Next: [Chapter 8: Production Operations and Governance](08-production-operations-and-governance.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/verify_tool_names.py`

The `extract_package_name` function in [`scripts/verify_tool_names.py`](https://github.com/awslabs/mcp/blob/HEAD/scripts/verify_tool_names.py) handles a key part of this chapter's functionality:

```py


def extract_package_name(pyproject_path: Path) -> str:
    """Extract the package name from pyproject.toml file."""
    try:
        with open(pyproject_path, 'rb') as f:
            data = tomllib.load(f)
        return data['project']['name']
    except (FileNotFoundError, KeyError) as e:
        raise ValueError(f'Failed to extract package name from {pyproject_path}: {e}')
    except Exception as e:
        if 'TOML' in str(type(e).__name__):
            raise ValueError(f'Failed to parse TOML file {pyproject_path}: {e}')
        else:
            raise ValueError(f'Failed to extract package name from {pyproject_path}: {e}')


def convert_package_name_to_server_format(package_name: str) -> str:
    """Convert package name to the format used in fully qualified tool names.

    Examples:
        awslabs.git-repo-research-mcp-server -> git_repo_research_mcp_server
        awslabs.nova-canvas-mcp-server -> nova_canvas_mcp_server
    """
    # Remove 'awslabs.' prefix if present
    if package_name.startswith('awslabs.'):
        package_name = package_name[8:]

    # Replace hyphens with underscores
    return package_name.replace('-', '_')


```

This function is important because it defines how awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[extract_package_name]
```
