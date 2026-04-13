---
layout: default
title: "Chapter 4: TypeScript Server Framework and UI Widgets"
nav_order: 4
parent: MCP Use Tutorial
---


# Chapter 4: TypeScript Server Framework and UI Widgets

Welcome to **Chapter 4: TypeScript Server Framework and UI Widgets**. In this part of **MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


TypeScript server workflows in mcp-use emphasize developer speed, UI integration, and inspector-first iteration.

## Learning Goals

- scaffold server projects with `create-mcp-use-app`
- implement tools/resources with typed schemas
- expose UI widgets for richer chat/app experiences
- use dev-mode inspector and hot reload effectively

## Build Loop

1. scaffold project
2. define first tools and resources
3. add UI widgets for high-value interactions
4. run inspector-driven test loop before deploy

## Source References

- [TypeScript Quickstart](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/getting-started/quickstart.mdx)
- [TypeScript Server Configuration](https://github.com/mcp-use/mcp-use/blob/main/docs/typescript/server/configuration.mdx)
- [TypeScript Library README](https://github.com/mcp-use/mcp-use/blob/main/libraries/typescript/README.md)
- [create-mcp-use-app README](https://github.com/mcp-use/mcp-use/blob/main/libraries/typescript/packages/create-mcp-use-app/README.md)

## Summary

You now have a complete TypeScript server workflow, from scaffold to interactive UI surfaces.

Next: [Chapter 5: Python Server Framework and Debug Endpoints](05-python-server-framework-and-debug-endpoints.md)

## Source Code Walkthrough

### `libraries/python/examples/example_middleware.py`

The `MutationMiddleware` class in [`libraries/python/examples/example_middleware.py`](https://github.com/mcp-use/mcp-use/blob/HEAD/libraries/python/examples/example_middleware.py) handles a key part of this chapter's functionality:

```py

    # Middleware that demonstrates mutating params and adding headers-like metadata
    class MutationMiddleware(Middleware):
        async def on_call_tool(self, context: MiddlewareContext[Any], call_next: NextFunctionT) -> Any:
            # Defensive mutation of params: ensure `arguments` exists before writing
            try:
                print("[MutationMiddleware] context.params=", context.params)
                args = getattr(context.params, "arguments", None)
                if args is None:
                    args = {}

                # Inject a URL argument (example) and a trace id
                args["url"] = "https://github.com"
                meta = args.setdefault("meta", {})
                meta["trace_id"] = "trace-123"

                # Write back the mutated arguments to the params object
                context.params.arguments = args

                # Also demonstrate carrying header-like info via metadata
                context.metadata.setdefault("headers", {})["X-Trace-Id"] = "trace-123"
                # Debug: show the mutated params/metadata immediately
                print("[AddTraceMiddleware] after mutation:", context.params, context.metadata)

            except Exception as e:
                # Don't break the request flow in an example
                print(f"[AddTraceMiddleware] failed to mutate params: {e}")

            return await call_next(context)

    config = {
        "mcpServers": {"playwright": {"command": "npx", "args": ["@playwright/mcp@latest"], "env": {"DISPLAY": ":1"}}}
```

This class is important because it defines how MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector implements the patterns covered in this chapter.

### `libraries/python/examples/example_middleware.py`

The `main` function in [`libraries/python/examples/example_middleware.py`](https://github.com/mcp-use/mcp-use/blob/HEAD/libraries/python/examples/example_middleware.py) handles a key part of this chapter's functionality:

```py


async def main():
    """Run the example with default logging and optional custom middleware."""
    # Load environment variables
    load_dotenv()

    # Create custom middleware
    class TimingMiddleware(Middleware):
        async def on_request(self, context: MiddlewareContext[Any], call_next: NextFunctionT) -> Any:
            start = time.time()
            try:
                print("--------------------------------")
                print(f"{context.method} started")
                print("--------------------------------")
                print(f"{context.params}, {context.metadata}, {context.timestamp}, {context.connection_id}")
                print("--------------------------------")
                result = await call_next(context)
                return result
            finally:
                duration = time.time() - start
                print("--------------------------------")
                print(f"{context.method} took {int(1000 * duration)}ms")
                print("--------------------------------")

    # Middleware that demonstrates mutating params and adding headers-like metadata
    class MutationMiddleware(Middleware):
        async def on_call_tool(self, context: MiddlewareContext[Any], call_next: NextFunctionT) -> Any:
            # Defensive mutation of params: ensure `arguments` exists before writing
            try:
                print("[MutationMiddleware] context.params=", context.params)
                args = getattr(context.params, "arguments", None)
```

This function is important because it defines how MCP Use Tutorial: Full-Stack MCP Development Across Agents, Clients, Servers, and Inspector implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[MutationMiddleware]
    B[main]
    A --> B
```
