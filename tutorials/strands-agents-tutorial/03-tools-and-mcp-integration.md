---
layout: default
title: "Chapter 3: Tools and MCP Integration"
nav_order: 3
parent: Strands Agents Tutorial
---


# Chapter 3: Tools and MCP Integration

Welcome to **Chapter 3: Tools and MCP Integration**. In this part of **Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers tool composition and MCP usage patterns for real capability expansion.

## Learning Goals

- build custom Python tools with decorators
- attach MCP servers through `MCPClient`
- manage tool discovery and lifecycle
- avoid hanging and stability pitfalls

## Integration Patterns

- static tool lists for predictable behavior
- directory-based tool loading for rapid iteration
- MCP-backed tool surfaces for external capabilities

## Reliability Considerations

Strands runs MCP communication through a background-thread architecture to hide async complexity. Treat MCP connection lifecycle and error handling as first-class operational concerns.

## Source References

- [Strands Tools Concepts](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/)
- [Strands MCP Tools Concepts](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/)
- [Strands MCP Client Architecture](https://github.com/strands-agents/sdk-python/blob/main/docs/MCP_CLIENT_ARCHITECTURE.md)

## Summary

You now have practical patterns for integrating tools and MCP safely in Strands.

Next: [Chapter 4: Model Providers and Runtime Strategy](04-model-providers-and-runtime-strategy.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/strands/tools/decorator.py`

The `tool` function in [`src/strands/tools/decorator.py`](https://github.com/strands-agents/sdk-python/blob/HEAD/src/strands/tools/decorator.py) handles a key part of this chapter's functionality:

```py
"""Tool decorator for SDK.

This module provides the @tool decorator that transforms Python functions into SDK Agent tools with automatic metadata
extraction and validation.

The @tool decorator performs several functions:

1. Extracts function metadata (name, description, parameters) from docstrings and type hints
2. Generates a JSON schema for input validation
3. Handles two different calling patterns:
   - Standard function calls (func(arg1, arg2))
   - Tool use calls (agent.my_tool(param1="hello", param2=123))
4. Provides error handling and result formatting
5. Works with both standalone functions and class methods

Example:
    ```python
    from strands import Agent, tool

    @tool
    def my_tool(param1: str, param2: int = 42) -> dict:
        '''
        Tool description - explain what it does.

        #Args:
            param1: Description of first parameter.
            param2: Description of second parameter (default: 42).

        #Returns:
            A dictionary with the results.
        '''
        result = do_something(param1, param2)
```

This function is important because it defines how Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support implements the patterns covered in this chapter.

### `src/strands/tools/decorator.py`

The `tool` function in [`src/strands/tools/decorator.py`](https://github.com/strands-agents/sdk-python/blob/HEAD/src/strands/tools/decorator.py) handles a key part of this chapter's functionality:

```py
"""Tool decorator for SDK.

This module provides the @tool decorator that transforms Python functions into SDK Agent tools with automatic metadata
extraction and validation.

The @tool decorator performs several functions:

1. Extracts function metadata (name, description, parameters) from docstrings and type hints
2. Generates a JSON schema for input validation
3. Handles two different calling patterns:
   - Standard function calls (func(arg1, arg2))
   - Tool use calls (agent.my_tool(param1="hello", param2=123))
4. Provides error handling and result formatting
5. Works with both standalone functions and class methods

Example:
    ```python
    from strands import Agent, tool

    @tool
    def my_tool(param1: str, param2: int = 42) -> dict:
        '''
        Tool description - explain what it does.

        #Args:
            param1: Description of first parameter.
            param2: Description of second parameter (default: 42).

        #Returns:
            A dictionary with the results.
        '''
        result = do_something(param1, param2)
```

This function is important because it defines how Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support implements the patterns covered in this chapter.

### `src/strands/tools/decorator.py`

The `tool` function in [`src/strands/tools/decorator.py`](https://github.com/strands-agents/sdk-python/blob/HEAD/src/strands/tools/decorator.py) handles a key part of this chapter's functionality:

```py
"""Tool decorator for SDK.

This module provides the @tool decorator that transforms Python functions into SDK Agent tools with automatic metadata
extraction and validation.

The @tool decorator performs several functions:

1. Extracts function metadata (name, description, parameters) from docstrings and type hints
2. Generates a JSON schema for input validation
3. Handles two different calling patterns:
   - Standard function calls (func(arg1, arg2))
   - Tool use calls (agent.my_tool(param1="hello", param2=123))
4. Provides error handling and result formatting
5. Works with both standalone functions and class methods

Example:
    ```python
    from strands import Agent, tool

    @tool
    def my_tool(param1: str, param2: int = 42) -> dict:
        '''
        Tool description - explain what it does.

        #Args:
            param1: Description of first parameter.
            param2: Description of second parameter (default: 42).

        #Returns:
            A dictionary with the results.
        '''
        result = do_something(param1, param2)
```

This function is important because it defines how Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support implements the patterns covered in this chapter.

### `src/strands/tools/decorator.py`

The `del` interface in [`src/strands/tools/decorator.py`](https://github.com/strands-agents/sdk-python/blob/HEAD/src/strands/tools/decorator.py) handles a key part of this chapter's functionality:

```py

import docstring_parser
from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo
from pydantic_core import PydanticSerializationError
from typing_extensions import override

from ..interrupt import InterruptException
from ..types._events import ToolInterruptEvent, ToolResultEvent, ToolStreamEvent
from ..types.tools import AgentTool, JSONSchema, ToolContext, ToolGenerator, ToolResult, ToolSpec, ToolUse

logger = logging.getLogger(__name__)


# Type for wrapped function
T = TypeVar("T", bound=Callable[..., Any])


class FunctionToolMetadata:
    """Helper class to extract and manage function metadata for tool decoration.

    This class handles the extraction of metadata from Python functions including:

    - Function name and description from docstrings
    - Parameter names, types, and descriptions
    - Return type information
    - Creation of Pydantic models for input validation

    The extracted metadata is used to generate a tool specification that can be used by Strands Agent to understand and
    validate tool usage.
    """

```

This interface is important because it defines how Strands Agents Tutorial: Model-Driven Agent Systems with Native MCP Support implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[tool]
    B[tool]
    C[tool]
    D[del]
    E[class]
    A --> B
    B --> C
    C --> D
    D --> E
```
