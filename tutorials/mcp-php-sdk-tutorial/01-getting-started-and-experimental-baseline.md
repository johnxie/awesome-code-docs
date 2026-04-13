---
layout: default
title: "Chapter 1: Getting Started and Experimental Baseline"
nav_order: 1
parent: MCP PHP SDK Tutorial
---


# Chapter 1: Getting Started and Experimental Baseline

Welcome to **Chapter 1: Getting Started and Experimental Baseline**. In this part of **MCP PHP SDK Tutorial: Building MCP Servers in PHP with Discovery and Transport Flexibility**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter sets a reproducible starting point for the evolving PHP SDK.

## Learning Goals

- install the SDK with a pinned dependency baseline
- align expectations for an experimental API surface
- run a minimal server-first workflow before advanced integrations
- reduce upgrade risk during early adoption

## Baseline Setup

```bash
composer require mcp/sdk
```

Start with a simple stdio server and validate end-to-end tool calls before adding frameworks or custom handlers.

## Adoption Guardrails

1. pin dependency versions in `composer.lock`
2. validate each upgrade against changelog and example behavior
3. treat API surfaces as potentially shifting until major stabilization
4. isolate your MCP integration behind thin adapters for easier refactor

## Source References

- [PHP SDK README - Installation](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#installation)
- [PHP SDK README - Roadmap](https://github.com/modelcontextprotocol/php-sdk/blob/main/README.md#roadmap)
- [PHP SDK Changelog](https://github.com/modelcontextprotocol/php-sdk/blob/main/CHANGELOG.md)

## Summary

You now have a practical baseline for adopting the PHP SDK with controlled risk.

Next: [Chapter 2: Server Builder and Capability Registration](02-server-builder-and-capability-registration.md)

## Source Code Walkthrough

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


## How These Components Connect

```mermaid
flowchart TD
    A[mcp-realm]
    B[docker-compose]
    C[composer]
    A --> B
    B --> C
```
