---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: awslabs/mcp Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gives a practical first-run path through the AWS MCP ecosystem.

## Learning Goals

- identify one or two servers that match immediate needs
- configure installation for your primary MCP host client
- validate first tool calls with minimal environment risk
- establish baseline profiles and runtime settings

## Fast Start Loop

1. select an initial server (for example documentation, API, or IaC)
2. install via your MCP host pattern (`uvx`-based paths are common)
3. set minimal environment variables (region/profile/log level)
4. run a low-risk read-only query end to end
5. capture this configuration as your baseline template

## Source References

- [Repository README](https://github.com/awslabs/mcp/blob/main/README.md)
- [AWS Documentation MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-documentation-mcp-server/README.md)
- [AWS API MCP Server README](https://github.com/awslabs/mcp/blob/main/src/aws-api-mcp-server/README.md)

## Summary

You now have a stable onboarding path for first AWS MCP server usage.

Next: [Chapter 2: Server Catalog and Role Composition](02-server-catalog-and-role-composition.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/verify_package_name.py`

The `extract_package_name` function in [`scripts/verify_package_name.py`](https://github.com/awslabs/mcp/blob/HEAD/scripts/verify_package_name.py) handles a key part of this chapter's functionality:

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
        # Handle both tomllib.TOMLDecodeError and tomli.TOMLDecodeError
        if 'TOML' in str(type(e).__name__):
            raise ValueError(f'Failed to parse TOML file {pyproject_path}: {e}')
        else:
            raise ValueError(f'Failed to extract package name from {pyproject_path}: {e}')


def extract_dependencies(pyproject_path: Path) -> List[str]:
    """Extract dependency names from pyproject.toml file."""
    try:
        with open(pyproject_path, 'rb') as f:
            data = tomllib.load(f)
        dependencies = data.get('project', {}).get('dependencies', [])
        # Extract just the package names (remove version constraints)
        dep_names = []
        for dep in dependencies:
            # Remove version constraints (>=, ==, etc.) and extract just the package name
            dep_name = re.split(r'[>=<!=]', dep)[0].strip()
            dep_names.append(dep_name)
        return dep_names
    except (FileNotFoundError, KeyError):
```

This function is important because it defines how awslabs/mcp Tutorial: Operating a Large-Scale MCP Server Ecosystem for AWS Workloads implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[extract_package_name]
```
