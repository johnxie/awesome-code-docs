---
layout: default
title: "Chapter 6: Client Communication: Sampling, Logging, and Progress"
nav_order: 6
parent: MCP PHP SDK Tutorial
---


# Chapter 6: Client Communication: Sampling, Logging, and Progress

Welcome to **Chapter 6: Client Communication: Sampling, Logging, and Progress**. In this part of **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains server-to-client communication utilities in PHP MCP handlers.

## Learning Goals

- use client gateway patterns for server-initiated communication
- apply sampling requests with clear user-control boundaries
- emit log and progress signals in protocol-compliant form
- reduce handler complexity around async-like notification flows

## Communication Surface

| Surface | Purpose |
|:--------|:--------|
| Sampling | server asks client to run model generation |
| Logging | structured diagnostics and observability |
| Progress | incremental status feedback for long-running calls |
| Notifications | out-of-band updates to client state |

## Source References

- [Client Communication Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-client-communication.md)
- [MCP Elements Guide - Logging](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/mcp-elements.md#logging)

## Summary

You now have an operational communication model for richer PHP MCP server UX.

Next: [Chapter 7: Framework Integration, Session Stores, and Dependencies](07-framework-integration-session-stores-and-dependencies.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `composer.json`

The `composer` module in [`composer.json`](https://github.com/modelcontextprotocol/php-sdk/blob/HEAD/composer.json) handles a key part of this chapter's functionality:

```json
{
  "name": "mcp/sdk",
  "description": "Model Context Protocol SDK for Client and Server applications in PHP",
  "license": "Apache-2.0",
  "type": "library",
  "authors": [
    {
      "name": "Christopher Hertel",
      "email": "mail@christopher-hertel.de"
    },
    {
      "name": "Kyrian Obikwelu",
      "email": "koshnawaza@gmail.com"
    },
    {
      "name": "Tobias Nyholm",
      "email": "tobias.nyholm@gmail.com"
    }
  ],
  "require": {
    "php": "^8.1",
    "ext-fileinfo": "*",
    "opis/json-schema": "^2.4",
    "php-http/discovery": "^1.20",
    "phpdocumentor/reflection-docblock": "^5.6 || ^6.0",
    "psr/clock": "^1.0",
    "psr/container": "^1.0 || ^2.0",
    "psr/event-dispatcher": "^1.0",
    "psr/http-client": "^1.0",
    "psr/http-factory": "^1.1",
    "psr/http-message": "^1.1 || ^2.0",
    "psr/http-server-handler": "^1.0",
    "psr/http-server-middleware": "^1.0",
    "psr/log": "^1.0 || ^2.0 || ^3.0",
    "symfony/finder": "^5.4 || ^6.4 || ^7.3 || ^8.0",
```

This module is important because it defines how MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility implements the patterns covered in this chapter.

### `examples/server/oauth-keycloak/keycloak/mcp-realm.json`

The `mcp-realm` module in [`examples/server/oauth-keycloak/keycloak/mcp-realm.json`](https://github.com/modelcontextprotocol/php-sdk/blob/HEAD/examples/server/oauth-keycloak/keycloak/mcp-realm.json) handles a key part of this chapter's functionality:

```json
{
  "realm": "mcp",
  "enabled": true,
  "registrationAllowed": false,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "bruteForceProtected": true,
  "accessTokenLifespan": 300,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "clients": [
    {
      "clientId": "mcp-client",
      "name": "MCP Client Application",
      "description": "Public client for MCP client applications",
      "enabled": true,
      "publicClient": true,
      "standardFlowEnabled": true,
      "directAccessGrantsEnabled": true,
      "serviceAccountsEnabled": false,
      "authorizationServicesEnabled": false,
      "fullScopeAllowed": true,
      "redirectUris": [
        "http://localhost:*",
        "http://127.0.0.1:*"
      ],
      "webOrigins": [
        "http://localhost:*",
        "http://127.0.0.1:*"
      ],
      "defaultClientScopes": [
        "openid",
        "profile",
```

This module is important because it defines how MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility implements the patterns covered in this chapter.

### `examples/server/oauth-microsoft/docker-compose.yml`

The `docker-compose` module in [`examples/server/oauth-microsoft/docker-compose.yml`](https://github.com/modelcontextprotocol/php-sdk/blob/HEAD/examples/server/oauth-microsoft/docker-compose.yml) handles a key part of this chapter's functionality:

```yml
services:
  php:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mcp-php-microsoft
    volumes:
      - ../../../:/app
    working_dir: /app
    env_file:
      - .env
    environment:
      AZURE_TENANT_ID: ${AZURE_TENANT_ID:-}
      AZURE_CLIENT_ID: ${AZURE_CLIENT_ID:-}
      AZURE_CLIENT_SECRET: ${AZURE_CLIENT_SECRET:-}
    command: >
      sh -c "mkdir -p /app/examples/server/oauth-microsoft/sessions;
      chmod -R 0777 /app/examples/server/oauth-microsoft/sessions;
      touch /app/examples/server/oauth-microsoft/dev.log;
      chmod 0666 /app/examples/server/oauth-microsoft/dev.log;
      touch /app/examples/server/dev.log;
      chmod 0666 /app/examples/server/dev.log;
      composer install --no-interaction --quiet 2>/dev/null || true;
      php-fpm"
    networks:
      - mcp-network

  nginx:
    image: nginx:alpine
    container_name: mcp-nginx-microsoft
    ports:
      - "${MCP_HTTP_PORT:-8000}:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ../../../:/app:ro
```

This module is important because it defines how MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[composer]
    B[mcp-realm]
    C[docker-compose]
    A --> B
    B --> C
```
