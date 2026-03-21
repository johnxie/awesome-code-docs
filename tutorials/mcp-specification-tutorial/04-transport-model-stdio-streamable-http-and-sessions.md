---
layout: default
title: "Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions"
nav_order: 4
parent: MCP Specification Tutorial
---


# Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions

Welcome to **Chapter 4: Transport Model: stdio, Streamable HTTP, and Sessions**. In this part of **MCP Specification Tutorial: Designing Production-Grade MCP Clients and Servers From the Source of Truth**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Transport behavior drives most production incidents in MCP systems.

## Learning Goals

- choose between stdio and Streamable HTTP based on deployment context
- implement session headers and protocol-version headers correctly
- handle SSE polling and resumability without breaking message ordering
- apply required security controls for remote/local HTTP endpoints

## Transport Decision Matrix

| Transport | Best Fit | Core Risks |
|:----------|:---------|:-----------|
| `stdio` | local subprocess servers | stdout contamination, process lifecycle leaks |
| Streamable HTTP | remote/shared servers and multi-client deployments | origin validation, session hijack, reconnection loss |

## Streamable HTTP Must-Haves

- validate `Origin` and reject invalid origin with `403`
- include and honor `MCP-Session-Id` when server assigns stateful sessions
- include `MCP-Protocol-Version` on follow-up HTTP requests
- support both `application/json` and `text/event-stream` response paths
- plan explicit behavior for resumability/redelivery and session expiration

## Source References

- [Transports](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/transports.mdx)
- [Lifecycle](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/lifecycle.mdx)
- [Security Best Practices - Session Hijacking](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/security_best_practices.mdx)

## Summary

You now have a transport operations model that is compatible with current session and security requirements.

Next: [Chapter 5: Server Primitives: Tools, Resources, and Prompts](05-server-primitives-tools-resources-and-prompts.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `schema/2025-06-18/schema.ts`

The `ElicitRequest` interface in [`schema/2025-06-18/schema.ts`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/HEAD/schema/2025-06-18/schema.ts) handles a key part of this chapter's functionality:

```ts
 * @category `elicitation/create`
 */
export interface ElicitRequest extends Request {
  method: "elicitation/create";
  params: {
    /**
     * The message to present to the user.
     */
    message: string;
    /**
     * A restricted subset of JSON Schema.
     * Only top-level properties are allowed, without nesting.
     */
    requestedSchema: {
      type: "object";
      properties: {
        [key: string]: PrimitiveSchemaDefinition;
      };
      required?: string[];
    };
  };
}

/**
 * Restricted schema definitions that only allow primitive types
 * without nested objects or arrays.
 *
 * @category `elicitation/create`
 */
export type PrimitiveSchemaDefinition =
  | StringSchema
  | NumberSchema
```

This interface is important because it defines how MCP Specification Tutorial: Designing Production-Grade MCP Clients and Servers From the Source of Truth implements the patterns covered in this chapter.

### `schema/2025-06-18/schema.ts`

The `StringSchema` interface in [`schema/2025-06-18/schema.ts`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/HEAD/schema/2025-06-18/schema.ts) handles a key part of this chapter's functionality:

```ts
 */
export type PrimitiveSchemaDefinition =
  | StringSchema
  | NumberSchema
  | BooleanSchema
  | EnumSchema;

/**
 * @category `elicitation/create`
 */
export interface StringSchema {
  type: "string";
  title?: string;
  description?: string;
  minLength?: number;
  maxLength?: number;
  format?: "email" | "uri" | "date" | "date-time";
}

/**
 * @category `elicitation/create`
 */
export interface NumberSchema {
  type: "number" | "integer";
  title?: string;
  description?: string;
  minimum?: number;
  maximum?: number;
}

/**
 * @category `elicitation/create`
```

This interface is important because it defines how MCP Specification Tutorial: Designing Production-Grade MCP Clients and Servers From the Source of Truth implements the patterns covered in this chapter.

### `schema/2025-06-18/schema.ts`

The `NumberSchema` interface in [`schema/2025-06-18/schema.ts`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/HEAD/schema/2025-06-18/schema.ts) handles a key part of this chapter's functionality:

```ts
export type PrimitiveSchemaDefinition =
  | StringSchema
  | NumberSchema
  | BooleanSchema
  | EnumSchema;

/**
 * @category `elicitation/create`
 */
export interface StringSchema {
  type: "string";
  title?: string;
  description?: string;
  minLength?: number;
  maxLength?: number;
  format?: "email" | "uri" | "date" | "date-time";
}

/**
 * @category `elicitation/create`
 */
export interface NumberSchema {
  type: "number" | "integer";
  title?: string;
  description?: string;
  minimum?: number;
  maximum?: number;
}

/**
 * @category `elicitation/create`
 */
```

This interface is important because it defines how MCP Specification Tutorial: Designing Production-Grade MCP Clients and Servers From the Source of Truth implements the patterns covered in this chapter.

### `schema/2025-06-18/schema.ts`

The `BooleanSchema` interface in [`schema/2025-06-18/schema.ts`](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/HEAD/schema/2025-06-18/schema.ts) handles a key part of this chapter's functionality:

```ts
  | StringSchema
  | NumberSchema
  | BooleanSchema
  | EnumSchema;

/**
 * @category `elicitation/create`
 */
export interface StringSchema {
  type: "string";
  title?: string;
  description?: string;
  minLength?: number;
  maxLength?: number;
  format?: "email" | "uri" | "date" | "date-time";
}

/**
 * @category `elicitation/create`
 */
export interface NumberSchema {
  type: "number" | "integer";
  title?: string;
  description?: string;
  minimum?: number;
  maximum?: number;
}

/**
 * @category `elicitation/create`
 */
export interface BooleanSchema {
```

This interface is important because it defines how MCP Specification Tutorial: Designing Production-Grade MCP Clients and Servers From the Source of Truth implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[ElicitRequest]
    B[StringSchema]
    C[NumberSchema]
    D[BooleanSchema]
    E[EnumSchema]
    A --> B
    B --> C
    C --> D
    D --> E
```
