---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: FastMCP Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter gives you a quick path from installation to a working FastMCP server and first client call.

## Learning Goals

- create and run a minimal server with one tool
- validate a basic client-server call loop
- understand local stdio versus HTTP first-run choices
- establish a repeatable baseline for future extension

## Fast Start Loop

1. install FastMCP from the [installation guide](https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/installation.mdx)
2. create a minimal server with `FastMCP(...)` and one `@mcp.tool`
3. run locally using `mcp.run()` or `fastmcp run ...`
4. call the tool from a client to verify end-to-end behavior
5. capture this setup as your baseline template for new services

## Source References

- [Quickstart](https://github.com/jlowin/fastmcp/blob/main/docs/getting-started/quickstart.mdx)
- [README](https://github.com/jlowin/fastmcp/blob/main/README.md)

## Summary

You now have a reliable baseline for expanding FastMCP servers beyond toy examples.

Next: [Chapter 2: Core Abstractions: Components, Providers, Transforms](02-core-abstractions-components-providers-transforms.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/auto_close_needs_mre.py`

The `from` class in [`scripts/auto_close_needs_mre.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/auto_close_needs_mre.py) handles a key part of this chapter's functionality:

```py

This script runs on a schedule to automatically close issues that have been
marked as "needs MRE" and haven't received activity from the issue author
within 7 days.
"""

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx


@dataclass
class Issue:
    """Represents a GitHub issue."""

    number: int
    title: str
    state: str
    created_at: str
    user_id: int
    user_login: str
    body: str | None


@dataclass
class Comment:
    """Represents a GitHub comment."""

    id: int
    body: str
```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `scripts/auto_close_needs_mre.py`

The `class` class in [`scripts/auto_close_needs_mre.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/auto_close_needs_mre.py) handles a key part of this chapter's functionality:

```py

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx


@dataclass
class Issue:
    """Represents a GitHub issue."""

    number: int
    title: str
    state: str
    created_at: str
    user_id: int
    user_login: str
    body: str | None


@dataclass
class Comment:
    """Represents a GitHub comment."""

    id: int
    body: str
    created_at: str
    user_id: int
    user_login: str


```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `scripts/auto_close_needs_mre.py`

The `class` class in [`scripts/auto_close_needs_mre.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/auto_close_needs_mre.py) handles a key part of this chapter's functionality:

```py

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx


@dataclass
class Issue:
    """Represents a GitHub issue."""

    number: int
    title: str
    state: str
    created_at: str
    user_id: int
    user_login: str
    body: str | None


@dataclass
class Comment:
    """Represents a GitHub comment."""

    id: int
    body: str
    created_at: str
    user_id: int
    user_login: str


```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `scripts/auto_close_needs_mre.py`

The `class` class in [`scripts/auto_close_needs_mre.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/auto_close_needs_mre.py) handles a key part of this chapter's functionality:

```py

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx


@dataclass
class Issue:
    """Represents a GitHub issue."""

    number: int
    title: str
    state: str
    created_at: str
    user_id: int
    user_login: str
    body: str | None


@dataclass
class Comment:
    """Represents a GitHub comment."""

    id: int
    body: str
    created_at: str
    user_id: int
    user_login: str


```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[from]
    B[class]
    C[class]
    D[class]
    E[GitHubClient]
    A --> B
    B --> C
    C --> D
    D --> E
```
