---
layout: default
title: "Chapter 4: Client Architecture and Transport Patterns"
nav_order: 4
parent: FastMCP Tutorial
---


# Chapter 4: Client Architecture and Transport Patterns

Welcome to **Chapter 4: Client Architecture and Transport Patterns**. In this part of **FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on client-side design patterns for reliable server communication.

## Learning Goals

- apply client lifecycle and context patterns correctly
- configure transport inference intentionally
- manage multi-server and environment-specific connection logic
- structure callback and error pathways for production diagnostics

## Client Design Checklist

| Area | Baseline Practice |
|:-----|:------------------|
| connection lifecycle | use explicit async contexts and cleanup |
| transport config | avoid implicit assumptions in mixed environments |
| multi-server routing | isolate server responsibilities by workflow |
| error handling | preserve structured error detail for observability |

## Source References

- [Client Guide](https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx)
- [Client Transports](https://github.com/jlowin/fastmcp/blob/main/docs/clients/transports.mdx)

## Summary

You now have a client architecture baseline for robust FastMCP integrations.

Next: [Chapter 5: Integrations: Claude Code, Cursor, and Tooling](05-integrations-claude-code-cursor-and-tooling.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/benchmark_imports.py`

The `print_table` function in [`scripts/benchmark_imports.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/benchmark_imports.py) handles a key part of this chapter's functionality:

```py


def print_table(results: list[dict[str, float | str | None]]) -> None:
    current_group = None
    print(f"\n{'Module':<45} {'Median':>8} {'Min':>8} {'Max':>8}")
    print("-" * 71)
    for r in results:
        if r["group"] != current_group:
            current_group = r["group"]
            group_labels = {
                "floor": "--- Unavoidable floor ---",
                "auth": "--- Auth stack (incremental over mcp) ---",
                "docket": "--- Docket stack (incremental over mcp) ---",
                "other": "--- Other deps (incremental over mcp) ---",
                "fastmcp": "--- FastMCP totals ---",
            }
            print(f"\n{group_labels.get(current_group, current_group)}")
        if r["median_ms"] is not None:
            print(
                f"  {r['label']:<43} {r['median_ms']:>7.1f}ms"
                f" {r['min_ms']:>7.1f}ms {r['max_ms']:>7.1f}ms"
            )
        else:
            print(f"  {r['label']:<43}    error")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark fastmcp import times")
    parser.add_argument(
        "--runs", type=int, default=5, help="Number of runs per measurement (default 5)"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
```

This function is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `scripts/benchmark_imports.py`

The `main` function in [`scripts/benchmark_imports.py`](https://github.com/jlowin/fastmcp/blob/HEAD/scripts/benchmark_imports.py) handles a key part of this chapter's functionality:

```py


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark fastmcp import times")
    parser.add_argument(
        "--runs", type=int, default=5, help="Number of runs per measurement (default 5)"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    print(f"Benchmarking import times ({args.runs} runs each)...")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")

    results = []
    for case in CASES:
        r = measure(case, args.runs)
        results.append(r)
        if not args.json:
            ms = f"{r['median_ms']:.1f}ms" if r["median_ms"] is not None else "error"
            print(f"  {case.label}: {ms}")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_table(results)


if __name__ == "__main__":
    main()

```

This function is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `examples/memory.py`

The `from` class in [`examples/memory.py`](https://github.com/jlowin/fastmcp/blob/HEAD/examples/memory.py) handles a key part of this chapter's functionality:

```py
import math
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Any, Self

import asyncpg
import numpy as np
from openai import AsyncOpenAI
from pgvector.asyncpg import register_vector
from pydantic import BaseModel, Field
from pydantic_ai import Agent

import fastmcp
from fastmcp import FastMCP

MAX_DEPTH = 5
SIMILARITY_THRESHOLD = 0.7
DECAY_FACTOR = 0.99
REINFORCEMENT_FACTOR = 1.1

DEFAULT_LLM_MODEL = "openai:gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

# Dependencies are configured in memory.fastmcp.json
mcp = FastMCP("memory")

DB_DSN = "postgresql://postgres:postgres@localhost:54320/memory_db"
# reset memory by deleting the profile directory
PROFILE_DIR = (
    fastmcp.settings.home / os.environ.get("USER", "anon") / "memory"
).resolve()
```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.

### `examples/memory.py`

The `class` class in [`examples/memory.py`](https://github.com/jlowin/fastmcp/blob/HEAD/examples/memory.py) handles a key part of this chapter's functionality:

```py
import math
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Any, Self

import asyncpg
import numpy as np
from openai import AsyncOpenAI
from pgvector.asyncpg import register_vector
from pydantic import BaseModel, Field
from pydantic_ai import Agent

import fastmcp
from fastmcp import FastMCP

MAX_DEPTH = 5
SIMILARITY_THRESHOLD = 0.7
DECAY_FACTOR = 0.99
REINFORCEMENT_FACTOR = 1.1

DEFAULT_LLM_MODEL = "openai:gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

# Dependencies are configured in memory.fastmcp.json
mcp = FastMCP("memory")

DB_DSN = "postgresql://postgres:postgres@localhost:54320/memory_db"
# reset memory by deleting the profile directory
PROFILE_DIR = (
    fastmcp.settings.home / os.environ.get("USER", "anon") / "memory"
).resolve()
```

This class is important because it defines how FastMCP Tutorial: Building and Operating MCP Servers with Pythonic Control implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[print_table]
    B[main]
    C[from]
    D[class]
    E[MemoryNode]
    A --> B
    B --> C
    C --> D
    D --> E
```
