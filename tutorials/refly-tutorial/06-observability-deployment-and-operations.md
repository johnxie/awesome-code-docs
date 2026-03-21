---
layout: default
title: "Chapter 6: Observability, Deployment, and Operations"
nav_order: 6
parent: Refly Tutorial
---


# Chapter 6: Observability, Deployment, and Operations

Welcome to **Chapter 6: Observability, Deployment, and Operations**. In this part of **Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers operating Refly with visibility into metrics, traces, logs, and deployment surfaces.

## Learning Goals

- run local observability stack for deeper runtime debugging
- correlate workflow behavior across traces, logs, and metrics
- understand deployment artifacts for self-hosted operations
- establish operational baselines before scaling usage

## Operations Building Blocks

| Domain | Key Assets |
|:-------|:-----------|
| deployment | `deploy/docker/docker-compose*.yml` |
| runtime telemetry | `deploy/docker/trace/` stack (Grafana, Prometheus, Tempo, Loki) |
| API verification | OpenAPI status/output endpoints |
| workload stability | middleware health + execution history |

## Trace Stack Quick Start

```bash
cd deploy/docker/trace
docker-compose up -d
```

Then verify data flow in Grafana and API checks before diagnosing workflow-level behavior.

## Source References

- [Trace Stack README](https://github.com/refly-ai/refly/blob/main/deploy/docker/trace/README.md)
- [Docker Deployment Assets](https://github.com/refly-ai/refly/tree/main/deploy/docker)
- [OpenAPI Guide](https://github.com/refly-ai/refly/blob/main/docs/en/guide/api/openapi.md)

## Summary

You now have a baseline operational model for running Refly beyond local experimentation.

Next: [Chapter 7: Troubleshooting, Safety, and Cost Controls](07-troubleshooting-safety-and-cost-controls.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `cypress/support/commands.ts`

The `Chainable` interface in [`cypress/support/commands.ts`](https://github.com/refly-ai/refly/blob/HEAD/cypress/support/commands.ts) handles a key part of this chapter's functionality:

```ts
// declare global {
//   namespace Cypress {
//     interface Chainable {
//       login(email: string, password: string): Chainable<void>
//       drag(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       dismiss(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       visit(originalFn: CommandOriginalFn, url: string, options: Partial<VisitOptions>): Chainable<Element>
//     }
//   }
// }

declare namespace Cypress {
  interface Chainable {
    /**
     * Execute SQL query through Docker container
     * @param query - SQL query to execute
     * @example
     * cy.execSQL('SELECT * FROM users')
     */
    execSQL(query: string): Chainable<string>;
    /**
     * Login to the app
     * @param email - Email to login with
     * @param password - Password to login with
     * @example
     * cy.login('test@example.com', 'testPassword123')
     */
    login(email: string, password: string): Chainable<void>;
  }
}

Cypress.Commands.add('execSQL', (query: string) => {
```

This interface is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.

### `cypress/support/commands.ts`

The `Chainable` interface in [`cypress/support/commands.ts`](https://github.com/refly-ai/refly/blob/HEAD/cypress/support/commands.ts) handles a key part of this chapter's functionality:

```ts
// declare global {
//   namespace Cypress {
//     interface Chainable {
//       login(email: string, password: string): Chainable<void>
//       drag(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       dismiss(subject: string, options?: Partial<TypeOptions>): Chainable<Element>
//       visit(originalFn: CommandOriginalFn, url: string, options: Partial<VisitOptions>): Chainable<Element>
//     }
//   }
// }

declare namespace Cypress {
  interface Chainable {
    /**
     * Execute SQL query through Docker container
     * @param query - SQL query to execute
     * @example
     * cy.execSQL('SELECT * FROM users')
     */
    execSQL(query: string): Chainable<string>;
    /**
     * Login to the app
     * @param email - Email to login with
     * @param password - Password to login with
     * @example
     * cy.login('test@example.com', 'testPassword123')
     */
    login(email: string, password: string): Chainable<void>;
  }
}

Cypress.Commands.add('execSQL', (query: string) => {
```

This interface is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[Chainable]
    B[Chainable]
    A --> B
```
