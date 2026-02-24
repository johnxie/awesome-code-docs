---
layout: default
title: "Chapter 5: MCP Integration and External Tools"
nav_order: 5
parent: Kiro Tutorial
---

# Chapter 5: MCP Integration and External Tools

Welcome to **Chapter 5: MCP Integration and External Tools**. In this part of **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kiro supports the Model Context Protocol (MCP) to connect external data sources, APIs, and tools to the AI agent. This chapter teaches you how to configure MCP servers and use them within specs and autonomous tasks.

## Learning Goals

- understand the MCP protocol and how Kiro uses it to connect external tools
- configure local and remote MCP servers in `.kiro/mcp.json`
- use connected MCP tools within chat and autonomous agent tasks
- build a custom MCP server for project-specific data sources
- manage MCP server authentication and security boundaries

## Fast Start Checklist

1. create `.kiro/mcp.json` with at least one MCP server entry
2. restart the Kiro workspace to load the MCP configuration
3. verify the MCP server is listed as active in Kiro settings
4. invoke a tool from the connected server in the chat panel
5. delegate an agent task that uses the MCP tool

## What is MCP?

MCP (Model Context Protocol) is an open protocol developed by Anthropic that defines how AI models connect to external tools and data sources. Kiro implements MCP as its primary extension mechanism, allowing agents to:

- query external APIs (GitHub, Jira, Confluence, Slack)
- access databases and internal documentation systems
- call custom business logic via local servers
- retrieve real-time data that is not available in the codebase

## MCP Server Configuration

MCP servers are configured in `.kiro/mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/myapp"],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/docs"],
      "env": {}
    }
  }
}
```

## Commonly Used MCP Servers

| Server | Package | Use Case |
|:-------|:--------|:---------|
| GitHub | `@modelcontextprotocol/server-github` | read issues, PRs, and code across repos |
| PostgreSQL | `@modelcontextprotocol/server-postgres` | query and inspect database schema and data |
| Filesystem | `@modelcontextprotocol/server-filesystem` | access documents outside the workspace |
| Brave Search | `@modelcontextprotocol/server-brave-search` | web search for documentation and APIs |
| Slack | `@modelcontextprotocol/server-slack` | read channel messages and user context |
| AWS Docs | custom or community server | query AWS service documentation |

## Using MCP Tools in Chat

Once configured, MCP tools are available in every chat interaction:

```
# Query GitHub issues:
> List all open issues labeled "bug" in the kirodotdev/Kiro repository

# Query the database:
> Show me the schema of the users table in the PostgreSQL database

# Search documentation:
> Find the Confluence page describing our API versioning policy

# The agent calls the appropriate MCP tool automatically and includes
# the results in its response context.
```

## Using MCP Tools in Autonomous Agent Tasks

MCP tools extend the autonomous agent's capabilities for tasks that require external data:

```markdown
# In tasks.md:
- [ ] 7. Query the GitHub issues API to identify all bugs tagged "auth-related"
         and generate a bug summary section in docs/auth-bugs.md
```

```
# Agent execution:
[Agent] Calling MCP tool: github.listIssues(labels=["bug", "auth-related"])
[Agent] Retrieved 12 issues from kirodotdev/Kiro
[Agent] Generating summary...
[Agent] Writing docs/auth-bugs.md...
[Agent] Task 7 complete.
```

## Remote MCP Servers

For team-shared MCP servers that are not installed locally, use the SSE or HTTP transport:

```json
{
  "mcpServers": {
    "internal-api": {
      "url": "https://mcp.internal.company.com/api",
      "headers": {
        "Authorization": "Bearer ${INTERNAL_API_TOKEN}"
      }
    },
    "confluence": {
      "url": "https://mcp.internal.company.com/confluence",
      "headers": {
        "Authorization": "Bearer ${CONFLUENCE_TOKEN}"
      }
    }
  }
}
```

## Building a Custom MCP Server

For project-specific data sources, build a custom MCP server using the MCP SDK:

```typescript
// custom-mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "project-data",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "get_feature_flags",
    description: "Get the current feature flag configuration from the internal config service",
    inputSchema: {
      type: "object",
      properties: {
        environment: { type: "string", enum: ["dev", "staging", "prod"] }
      },
      required: ["environment"]
    }
  }]
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "get_feature_flags") {
    const env = request.params.arguments.environment;
    // fetch from internal config service
    const flags = await fetchFeatureFlags(env);
    return { content: [{ type: "text", text: JSON.stringify(flags) }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

Register the custom server in `.kiro/mcp.json`:

```json
{
  "mcpServers": {
    "project-data": {
      "command": "npx",
      "args": ["ts-node", "./tools/custom-mcp-server.ts"],
      "env": {
        "CONFIG_SERVICE_URL": "${CONFIG_SERVICE_URL}"
      }
    }
  }
}
```

## MCP Security Boundaries

| Security Concern | Recommended Practice |
|:----------------|:---------------------|
| Credential storage | use environment variable references like `${VAR_NAME}` in mcp.json; never hardcode tokens |
| Network access | restrict MCP servers to read-only access for data sources when possible |
| Tool scoping | list only the tools the agent needs; disable unused tools to reduce attack surface |
| Audit logging | log all MCP tool invocations with arguments for security audit trails |
| Server isolation | run untrusted MCP servers in sandboxed environments (Docker, subprocess isolation) |

## Source References

- [Kiro Docs: MCP](https://kiro.dev/docs/mcp)
- [Kiro Docs: MCP Configuration](https://kiro.dev/docs/mcp/configuration)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Kiro Repository](https://github.com/kirodotdev/Kiro)

## Summary

You now know how to configure MCP servers, use external tools in chat and autonomous tasks, and build custom MCP servers for project-specific data sources.

Next: [Chapter 6: Hooks and Automation](06-hooks-and-automation.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- tutorial slug: **kiro-tutorial**
- chapter focus: **Chapter 5: MCP Integration and External Tools**
- system context: **Kiro Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 5: MCP Integration and External Tools` — Kiro as the MCP client, external MCP servers as tool providers, and the agent as the tool consumer.
2. Separate control-plane decisions (which servers to connect, tool scoping, auth configuration) from data-plane execution (tool invocations, response parsing).
3. Capture input contracts: `.kiro/mcp.json` server definitions; output: tool results injected into agent context.
4. Trace state transitions: config written → workspace restart → server process started → tools registered → agent invokes tools → results returned.
5. Identify extension hooks: custom MCP server implementations, remote SSE/HTTP transports, per-tool access controls.
6. Map ownership boundaries: platform team owns shared remote MCP servers; individual developers own local server configs; security team approves tool scopes.
7. Specify rollback paths: remove server entry from `mcp.json` and restart workspace; revert to previous `mcp.json` via git.
8. Track observability signals: tool invocation logs, latency per tool call, error rates per MCP server, credential rotation alerts.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Server type | well-known community MCP packages | custom internal MCP server | ease vs specificity |
| Auth method | env var references in mcp.json | secret manager integration | simplicity vs security posture |
| Tool scope | all tools from a server enabled | explicit tool allowlist per server | ease vs least-privilege |
| Deployment | local npx-based servers | containerized remote servers | zero-setup vs isolation |
| Audit logging | none | full tool invocation audit log | performance vs compliance |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| MCP server not found | agent reports tool unavailable | server not started or misconfigured | verify server entry in mcp.json and restart workspace |
| credential exposure | hardcoded token in mcp.json committed to git | developer bypassed env var pattern | scan mcp.json in CI; enforce env var references |
| tool call timeout | agent stalls waiting for tool response | remote MCP server unavailable or slow | set timeout in mcp.json; add health check for remote servers |
| overprivileged tool | agent queries production data unintentionally | read-write access granted to data source | restrict MCP server to read-only role for non-production use |
| schema mismatch | tool returns unexpected response format | upstream API changed without updating server | add schema validation to custom MCP server response handler |
| context overflow from large tool responses | agent loses context after tool call | tool returns unfiltered large dataset | add response size limits and pagination to custom MCP servers |

### Implementation Runbook

1. Identify the external data sources or APIs needed for the current feature spec.
2. Select or build an MCP server for each data source.
3. Configure each server in `.kiro/mcp.json` using environment variable references for all credentials.
4. Restart the Kiro workspace to load the new MCP configuration.
5. Verify each server is listed as active in Kiro settings and test one tool call per server.
6. Update the relevant steering file (`project.md` or a new `mcp.md`) to document available MCP tools.
7. Add MCP tool invocations to relevant tasks in `tasks.md` where external data is needed.
8. Monitor tool invocation logs during the first autonomous task execution that uses MCP tools.
9. Commit `mcp.json` to version control with a note listing which environment variables must be set by each developer.

### Quality Gate Checklist

- [ ] all credentials in mcp.json use environment variable references, not hardcoded values
- [ ] each MCP server is verified active in Kiro settings before task delegation
- [ ] tool scopes are restricted to the minimum access required for each server
- [ ] a `.env.example` file documents the required environment variables for MCP servers
- [ ] remote MCP servers have a health check endpoint and a timeout configured
- [ ] tool invocation logging is enabled and accessible for audit review
- [ ] mcp.json is committed to version control with a clear setup README
- [ ] CI scans mcp.json and related files for hardcoded credentials on every PR

### Source Alignment

- [Kiro Docs: MCP](https://kiro.dev/docs/mcp)
- [Kiro Docs: MCP Configuration](https://kiro.dev/docs/mcp/configuration)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)

### Cross-Tutorial Connection Map

- [MCP TypeScript SDK Tutorial](../mcp-typescript-sdk-tutorial/)
- [MCP Python SDK Tutorial](../mcp-python-sdk-tutorial/)
- [Awesome MCP Servers Tutorial](../awesome-mcp-servers-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Chapter 6: Hooks and Automation](06-hooks-and-automation.md)

### Advanced Practice Exercises

1. Configure three different MCP servers (GitHub, PostgreSQL, and a custom one) and verify each with a targeted tool call.
2. Build a minimal custom MCP server that exposes one tool reading from a local JSON config file and register it in Kiro.
3. Simulate a credential exposure incident by hardcoding a test token in mcp.json, then fix it with env var references and add a CI scan.
4. Create a Kiro task that requires data from two different MCP servers and confirm the agent orchestrates both tool calls correctly.
5. Set up a remote MCP server with an HTTP transport and configure a timeout; test the timeout behavior by intentionally delaying the server response.

### Review Questions

1. What is the difference between a local stdio-based MCP server and a remote HTTP-based MCP server, and when should you use each?
2. Why should all credentials in mcp.json use environment variable references rather than hardcoded values?
3. What tradeoff did you make between enabling all tools from a server and restricting to an explicit allowlist?
4. How would you recover if a custom MCP server returned a schema-breaking response that corrupted an in-progress autonomous task?
5. What must be in the project's README before team members can use a shared MCP configuration?

### Scenario Playbook 1: MCP - Server Not Launching

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent reports a tool is unavailable after mcp.json was updated with a new server
- initial hypothesis: the MCP server process failed to start due to a missing npm package or wrong command path
- immediate action: run the server command manually in the terminal to see the startup error
- engineering control: add a startup health check to the mcp.json server entry and verify it passes after workspace restart
- verification target: the server appears as active in Kiro settings and a test tool call succeeds
- rollback trigger: if the server cannot start after three attempts, remove the entry from mcp.json and use a fallback approach
- communication step: document the startup error and fix in the project's MCP setup README
- learning capture: add a pre-installation step to the MCP onboarding guide that verifies the required npm packages are installed

### Scenario Playbook 2: MCP - Credential Hardcoded in mcp.json

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: a code review catches a real API token hardcoded in mcp.json before it is merged
- initial hypothesis: the developer copied a working token from a local test rather than using an env var reference
- immediate action: immediately revoke the exposed token and issue a new one before merging the PR
- engineering control: replace the hardcoded value with `${ENV_VAR_NAME}` and add the variable to `.env.example`
- verification target: gitleaks scan on the PR shows zero secrets in mcp.json after the fix
- rollback trigger: if the token was already merged to main, treat it as a confirmed secret exposure and escalate
- communication step: notify the security team and the token owner of the exposure within one hour
- learning capture: add a required gitleaks check to the PR pipeline targeting the `.kiro/` directory

### Scenario Playbook 3: MCP - Tool Call Timeout During Autonomous Task

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: autonomous agent stalls waiting for a response from a remote MCP server during task execution
- initial hypothesis: the remote MCP server is unavailable or experiencing high latency
- immediate action: interrupt the agent and check the remote server's health endpoint
- engineering control: add a `timeout` field to the mcp.json server entry and implement a fallback behavior in the task
- verification target: re-run the task with timeout configured; agent fails gracefully within the timeout window
- rollback trigger: if the remote server is consistently unavailable, switch to a local MCP server for the same data source
- communication step: file an incident report for the remote MCP server team with the timeout details and impact
- learning capture: add timeout configuration as a required field in the team's MCP server onboarding template

### Scenario Playbook 4: MCP - Overprivileged Database Access

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent accidentally modifies production database records through an MCP server with write access
- initial hypothesis: the PostgreSQL MCP server was configured with a read-write database role
- immediate action: revoke the write permissions from the MCP server's database role immediately
- engineering control: create a dedicated read-only database user for MCP server connections and update mcp.json
- verification target: confirm the agent cannot execute INSERT, UPDATE, or DELETE statements through the MCP server
- rollback trigger: if the database modification caused data corruption, initiate the database recovery runbook
- communication step: notify the DBA team and affected data owners of the unauthorized modification within 30 minutes
- learning capture: add a mandatory read-only access requirement to the security steering file for all MCP database servers

### Scenario Playbook 5: MCP - Large Tool Response Causes Context Overflow

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: agent loses coherence after receiving a large unfiltered response from an MCP tool (e.g., thousands of GitHub issues)
- initial hypothesis: the tool response exceeds the agent's effective context window, pushing out earlier task context
- immediate action: interrupt the agent and redesign the tool call to return only the top 10 most relevant results
- engineering control: add response size limits and filtering parameters to the custom MCP server's tool schema
- verification target: re-run the agent task with the filtered tool call; agent maintains context through task completion
- rollback trigger: if filtering removes critical data, implement pagination and chain two agent calls instead of one
- communication step: update the tool's documentation in the MCP server README with the recommended query parameters
- learning capture: add a maximum response size guideline to the team's custom MCP server development standards

## What Problem Does This Solve?

Agentic coding IDEs are limited to what they can see in the local workspace. Kiro's MCP integration breaks this boundary by connecting agents to the full context of an engineering organization: issue trackers, documentation wikis, internal APIs, database schemas, and feature flag systems. This means agents can generate code that references the actual current state of external systems, not just what is hardcoded in the repo.

In practical terms, this chapter helps you avoid three common failures:

- generating code against stale or assumed API contracts because the agent cannot see the live API schema
- writing tasks that require human lookups from external systems, breaking the autonomous execution flow
- integrating with external tools through ad-hoc prompt stuffing instead of structured, auditable tool calls

After working through this chapter, you should be able to treat MCP servers as the API boundary between Kiro agents and your organization's full data ecosystem.

## How it Works Under the Hood

Under the hood, `Chapter 5: MCP Integration and External Tools` follows a repeatable control path:

1. **Server registration**: at workspace load, Kiro reads `mcp.json` and starts each server process using the configured command.
2. **Tool discovery**: Kiro sends a `tools/list` request to each server and registers the returned tool schemas.
3. **Context injection**: available tool names and schemas are injected into the agent's system prompt.
4. **Tool dispatch**: when the agent decides to use a tool, Kiro sends a `tools/call` request to the appropriate server process.
5. **Response integration**: the server's response is formatted and injected into the agent's next context block.
6. **Audit logging**: each tool invocation with its arguments and response size is logged for security and debugging.

When debugging MCP issues, trace this sequence from server startup through tool registration before investigating individual tool calls.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Kiro Docs: MCP](https://kiro.dev/docs/mcp)
  Why it matters: the primary reference for how Kiro implements MCP client behavior and mcp.json format.
- [MCP Specification](https://spec.modelcontextprotocol.io)
  Why it matters: the canonical protocol definition for tools/list and tools/call message formats.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
  Why it matters: the official SDK for building custom MCP servers in TypeScript.
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
  Why it matters: the community catalog of ready-to-use MCP servers for common data sources.

Suggested trace strategy:
- check the MCP server registry before building a custom server to avoid duplicating existing work
- test each new MCP server with a direct stdio call before registering it in mcp.json to isolate startup issues

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Autonomous Agent Mode](04-autonomous-agent-mode.md)
- [Next Chapter: Chapter 6: Hooks and Automation](06-hooks-and-automation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 5: MCP Integration and External Tools

- tutorial context: **Kiro Tutorial: Spec-Driven Agentic IDE from AWS**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
