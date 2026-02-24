---
layout: default
title: "Nanocoder - Chapter 3: Tool System Internals"
nav_order: 3
has_children: false
parent: "Nanocoder - AI Coding Agent Deep Dive"
---

# Chapter 3: Tool System Internals

Welcome to **Chapter 3: Tool System Internals**. In this part of **Nanocoder Tutorial: Building and Understanding AI Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> How AI coding agents bridge the gap between LLM reasoning and real-world file system and shell operations.

## Overview

Tools are what transform an LLM from a chatbot into a coding agent. This chapter explores how the tool system works internally: the JSON Schema-based tool definitions that LLMs understand, the registry pattern for managing tools, the execution pipeline, and the approval workflow that keeps destructive operations safe.

## Tool Definition Schema

LLMs understand tools through JSON Schema definitions. Each tool has a name, description, and parameter schema:

```typescript
interface ToolDefinition {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: {
      type: "object";
      properties: Record<string, ParameterSchema>;
      required: string[];
    };
  };
}

// Example: read_file tool definition
const readFileTool: ToolDefinition = {
  type: "function",
  function: {
    name: "read_file",
    description:
      "Read the contents of a file at the given path. " +
      "Returns the file contents as a string. " +
      "Use this to examine code before making changes.",
    parameters: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Relative or absolute path to the file to read",
        },
        offset: {
          type: "number",
          description: "Line number to start reading from (1-indexed)",
        },
        limit: {
          type: "number",
          description: "Maximum number of lines to read",
        },
      },
      required: ["path"],
    },
  },
};
```

### Why Descriptions Matter

The tool description is the LLM's only guide for when and how to use a tool. Compare:

```typescript
// Bad: vague description
{
  name: "write_file",
  description: "Writes a file"
}

// Good: specific, instructive description
{
  name: "write_file",
  description:
    "Write content to a file, creating it if it doesn't exist " +
    "or overwriting if it does. Always use read_file first to " +
    "understand existing content before overwriting. Show the " +
    "user what you plan to write before executing."
}
```

## Tool Registry Pattern

The tool registry centralizes tool management—registration, schema export, and execution dispatch:

```typescript
type ToolHandler = (args: Record<string, unknown>) => Promise<string>;

interface RegisteredTool {
  definition: ToolDefinition;
  handler: ToolHandler;
  requiresApproval: boolean;
}

class ToolRegistry {
  private tools: Map<string, RegisteredTool> = new Map();

  register(
    definition: ToolDefinition,
    handler: ToolHandler,
    options: { requiresApproval?: boolean } = {}
  ): void {
    this.tools.set(definition.function.name, {
      definition,
      handler,
      requiresApproval: options.requiresApproval ?? false,
    });
  }

  getSchemas(): ToolDefinition[] {
    return Array.from(this.tools.values()).map((t) => t.definition);
  }

  async execute(
    name: string,
    args: Record<string, unknown>
  ): Promise<string> {
    const tool = this.tools.get(name);
    if (!tool) {
      throw new Error(`Unknown tool: ${name}`);
    }
    return tool.handler(args);
  }

  requiresApproval(name: string): boolean {
    return this.tools.get(name)?.requiresApproval ?? true;
  }
}
```

## Core Tool Implementations

### read_file

The simplest tool—read a file and return its contents:

```typescript
async function readFile(args: {
  path: string;
  offset?: number;
  limit?: number;
}): Promise<string> {
  const absolutePath = resolve(process.cwd(), args.path);

  // Security: prevent path traversal
  if (!absolutePath.startsWith(process.cwd())) {
    return "Error: Cannot read files outside the working directory";
  }

  try {
    const content = await fs.readFile(absolutePath, "utf-8");
    const lines = content.split("\n");

    const start = (args.offset ?? 1) - 1;
    const end = args.limit ? start + args.limit : lines.length;
    const slice = lines.slice(start, end);

    // Add line numbers for LLM reference
    return slice
      .map((line, i) => `${start + i + 1}\t${line}`)
      .join("\n");
  } catch (error) {
    return `Error reading ${args.path}: ${error.message}`;
  }
}
```

### write_file

Writing files requires showing the diff and getting approval:

```typescript
async function writeFile(args: {
  path: string;
  content: string;
}): Promise<string> {
  const absolutePath = resolve(process.cwd(), args.path);

  if (!absolutePath.startsWith(process.cwd())) {
    return "Error: Cannot write files outside the working directory";
  }

  try {
    // Read existing content for diff
    let existingContent = "";
    try {
      existingContent = await fs.readFile(absolutePath, "utf-8");
    } catch {
      // File doesn't exist yet
    }

    // Write the file
    await fs.mkdir(dirname(absolutePath), { recursive: true });
    await fs.writeFile(absolutePath, args.content, "utf-8");

    if (existingContent) {
      const diff = createDiff(existingContent, args.content);
      return `File updated: ${args.path}\n\nDiff:\n${diff}`;
    }
    return `File created: ${args.path} (${args.content.length} bytes)`;
  } catch (error) {
    return `Error writing ${args.path}: ${error.message}`;
  }
}
```

### bash

Command execution is the most powerful—and dangerous—tool:

```typescript
async function executeBash(args: {
  command: string;
  timeout?: number;
}): Promise<string> {
  const timeout = args.timeout ?? 30000; // 30 second default

  try {
    const { stdout, stderr } = await execAsync(args.command, {
      cwd: process.cwd(),
      timeout,
      maxBuffer: 1024 * 1024, // 1 MB
      env: {
        ...process.env,
        // Prevent interactive prompts
        GIT_TERMINAL_PROMPT: "0",
        DEBIAN_FRONTEND: "noninteractive",
      },
    });

    let output = "";
    if (stdout) output += stdout;
    if (stderr) output += `\nSTDERR:\n${stderr}`;

    // Truncate very long output
    if (output.length > 10000) {
      output =
        output.slice(0, 5000) +
        "\n... (truncated) ...\n" +
        output.slice(-2000);
    }

    return output || "(no output)";
  } catch (error) {
    return `Command failed (exit code ${error.code}):\n${error.stderr || error.message}`;
  }
}
```

### search (grep/ripgrep)

Code search helps the LLM find relevant files quickly:

```typescript
async function searchCode(args: {
  pattern: string;
  path?: string;
  glob?: string;
  maxResults?: number;
}): Promise<string> {
  const searchPath = args.path || ".";
  const maxResults = args.maxResults ?? 20;

  const rgArgs = [
    "--json",
    "--max-count",
    "5", // Max matches per file
    "-n", // Line numbers
  ];

  if (args.glob) {
    rgArgs.push("--glob", args.glob);
  }

  rgArgs.push(args.pattern, searchPath);

  try {
    const { stdout } = await execAsync(`rg ${rgArgs.join(" ")}`);
    const results = parseRipgrepJson(stdout);

    return results
      .slice(0, maxResults)
      .map(
        (r) =>
          `${r.file}:${r.line}: ${r.text.trim()}`
      )
      .join("\n");
  } catch {
    return `No matches found for pattern: ${args.pattern}`;
  }
}
```

## The Approval Workflow

```mermaid
flowchart TD
    A[Tool Call Received] --> B{Requires Approval?}
    B -->|No| C[Execute Immediately]
    B -->|Yes| D[Display Preview]
    D --> E{User Decision}
    E -->|Approve| C
    E -->|Edit| F[Open Editor]
    F --> G[User Modifies]
    G --> C
    E -->|Deny| H[Return Denial to LLM]
    C --> I[Return Result to Agent Loop]
    H --> I
```

### Categorizing Tool Safety

```typescript
function registerCoreTools(registry: ToolRegistry): void {
  // Safe: read-only operations
  registry.register(readFileDefinition, readFile, {
    requiresApproval: false,
  });

  registry.register(searchDefinition, searchCode, {
    requiresApproval: false,
  });

  // Requires approval: write operations
  registry.register(writeFileDefinition, writeFile, {
    requiresApproval: true,
  });

  // Requires approval: command execution
  registry.register(bashDefinition, executeBash, {
    requiresApproval: true,
  });
}
```

### Approval UI Implementation

```typescript
async function promptApproval(
  toolName: string,
  args: Record<string, unknown>
): Promise<"approve" | "deny" | "edit"> {
  console.log(`\n🔧 Tool: ${toolName}`);

  // Display tool-specific preview
  if (toolName === "write_file") {
    console.log(`   Path: ${args.path}`);
    console.log(`   Content:`);
    console.log(
      (args.content as string)
        .split("\n")
        .map((l) => `   ${l}`)
        .join("\n")
    );
  } else if (toolName === "bash") {
    console.log(`   Command: ${args.command}`);
  }

  const answer = await readline.question(
    "\n   Approve? [y/n/e(dit)] "
  );

  switch (answer.toLowerCase()) {
    case "y":
    case "yes":
      return "approve";
    case "e":
    case "edit":
      return "edit";
    default:
      return "deny";
  }
}
```

## Advanced: Tool Composition

LLMs naturally chain tools when given well-described capabilities:

```
User: "Add error handling to the fetch function in api.ts"

LLM thinks: I need to read the file first, then modify it.

Step 1: Tool call → read_file("src/api.ts")
        Result → file contents with fetch function

Step 2: Tool call → write_file("src/api.ts", modified_content)
        Approval → user reviews diff
        Result → "File updated"

Step 3: Tool call → bash("npm run typecheck")
        Approval → user approves
        Result → "No errors found"

Step 4: Text response → "I've added try-catch blocks..."
```

This emergent behavior requires no explicit orchestration—the LLM's training on coding patterns drives it to read-modify-verify naturally.

## Custom Tool Creation

You can extend nanocoder with project-specific tools:

```typescript
// Register a custom tool for running tests
registry.register(
  {
    type: "function",
    function: {
      name: "run_tests",
      description:
        "Run the project's test suite. Returns test results " +
        "including pass/fail counts and error details.",
      parameters: {
        type: "object",
        properties: {
          pattern: {
            type: "string",
            description: "Test file pattern to match (e.g., '*.test.ts')",
          },
          watch: {
            type: "boolean",
            description: "Run in watch mode",
          },
        },
        required: [],
      },
    },
  },
  async (args) => {
    const pattern = args.pattern ? `-- ${args.pattern}` : "";
    const { stdout, stderr } = await execAsync(
      `npm test ${pattern}`,
      { timeout: 60000 }
    );
    return stdout + (stderr ? `\nWarnings:\n${stderr}` : "");
  },
  { requiresApproval: true }
);
```

## Summary

The tool system is the bridge between LLM intelligence and real-world capability. Well-defined tool schemas with clear descriptions guide the LLM's decision-making, while the registry pattern keeps tool management clean and extensible. The approval workflow ensures safety without sacrificing the agent's ability to operate autonomously on read-only tasks.

## Key Takeaways

1. Tools are defined via JSON Schema—the LLM uses descriptions to decide when and how to call them
2. The registry pattern centralizes tool registration, schema export, and execution dispatch
3. Read-only tools (read_file, search) skip approval; write operations require user consent
4. Path traversal prevention and command timeouts are essential security measures
5. LLMs naturally compose tools into multi-step workflows without explicit orchestration
6. Custom tools extend agent capability for project-specific workflows

## Next Steps

In [Chapter 4: Multi-Provider Integration](04-multi-provider-integration.md), we'll explore how nanocoder supports multiple LLM backends through a provider abstraction layer.

---

*Built with insights from the [Nanocoder](https://github.com/Nano-Collective/nanocoder) project.*

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Nanocoder Tutorial: Building and Understanding AI Coding Agents**
- tutorial slug: **nanocoder-tutorial**
- chapter focus: **Chapter 3: Tool System Internals**
- system context: **Nanocoder Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 3: Tool System Internals`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Nanocoder Repository](https://github.com/Nano-Collective/nanocoder)
- [Nanocoder Releases](https://github.com/Nano-Collective/nanocoder/releases)
- [Nanocoder Documentation Directory](https://github.com/Nano-Collective/nanocoder/tree/main/docs)
- [Nanocoder MCP Configuration Guide](https://github.com/Nano-Collective/nanocoder/blob/main/docs/mcp-configuration.md)
- [Nano Collective Website](https://nanocollective.org/)

### Cross-Tutorial Connection Map

- [Aider Tutorial](../aider-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Continue Tutorial](../continue-tutorial/)
- [OpenHands Tutorial](../openhands-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 3: Tool System Internals`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

### Scenario Playbook 1: Chapter 3: Tool System Internals

- tutorial context: **Nanocoder Tutorial: Building and Understanding AI Coding Agents**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `args`, `path`, `description` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Tool System Internals` as an operating subsystem inside **Nanocoder Tutorial: Building and Understanding AI Coding Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `file`, `requiresApproval` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Tool System Internals` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `args`.
2. **Input normalization**: shape incoming data so `path` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `description`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Nanocoder Repository](https://github.com/Nano-Collective/nanocoder)
  Why it matters: authoritative reference on `Nanocoder Repository` (github.com).
- [Nanocoder Releases](https://github.com/Nano-Collective/nanocoder/releases)
  Why it matters: authoritative reference on `Nanocoder Releases` (github.com).
- [Nanocoder Documentation Directory](https://github.com/Nano-Collective/nanocoder/tree/main/docs)
  Why it matters: authoritative reference on `Nanocoder Documentation Directory` (github.com).
- [Nanocoder MCP Configuration Guide](https://github.com/Nano-Collective/nanocoder/blob/main/docs/mcp-configuration.md)
  Why it matters: authoritative reference on `Nanocoder MCP Configuration Guide` (github.com).
- [Nano Collective Website](https://nanocollective.org/)
  Why it matters: authoritative reference on `Nano Collective Website` (nanocollective.org).

Suggested trace strategy:
- search upstream code for `args` and `path` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Architecture & Agent Loop](02-architecture-agent-loop.md)
- [Next Chapter: Chapter 4: Multi-Provider Integration](04-multi-provider-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
