---
layout: default
title: "Chapter 2: Server Builder and Capability Registration"
nav_order: 2
parent: MCP PHP SDK Tutorial
---


# Chapter 2: Server Builder and Capability Registration

Welcome to **Chapter 2: Server Builder and Capability Registration**. In this part of **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how `Server::builder()` composes MCP runtime behavior.

## Learning Goals

- understand builder-driven server composition
- configure server info, instructions, pagination, and discovery
- register capabilities manually when discovery is not enough
- add dependency wiring (container/logger/event dispatcher) safely

## Builder Responsibilities

| Area | Typical Controls |
|:-----|:-----------------|
| Server metadata | name, version, instructions |
| Capability setup | discovery scan or explicit registration |
| Runtime dependencies | container, logger, event dispatcher |
| Session behavior | session store + TTL strategy |

## Design Guidance

- use the static builder method as the default setup path.
- keep explicit registration for business-critical handlers requiring strict ownership.
- keep capability declarations and actual handler availability aligned.

## Source References

- [Server Builder Guide](https://github.com/modelcontextprotocol/php-sdk/blob/main/docs/server-builder.md)
- [PHP SDK README - Quick Start](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#quick-start)

## Summary

You now have a builder-centric model for composing PHP MCP servers.

Next: [Chapter 3: MCP Elements: Tools, Resources, Prompts, and Schemas](03-mcp-elements-tools-resources-prompts-and-schemas.md)

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
