---
layout: default
title: "Chapter 2: System Architecture: App, Worker, Engine"
nav_order: 2
parent: Activepieces Tutorial
---


# Chapter 2: System Architecture: App, Worker, Engine

Welcome to **Chapter 2: System Architecture: App, Worker, Engine**. In this part of **Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains the execution architecture that powers scale and reliability.

## Learning Goals

- understand responsibilities of app, worker, engine, and UI layers
- map queue/database dependencies to execution behavior
- identify likely bottlenecks under load spikes
- plan scaling steps without breaking flow reliability

## Architecture Summary

Activepieces separates concerns:

- app handles APIs, validation, and orchestration entrypoints
- worker pulls jobs and executes flows via the engine
- engine parses flow JSON and runs execution logic
- Postgres + Redis back persistent state and queueing behavior

## Scaling Heuristic

Start by scaling workers for execution pressure, then app replicas for ingress/API load, while keeping Redis/Postgres availability and capacity visible through monitoring.

## Source References

- [Architecture Overview](https://github.com/activepieces/activepieces/blob/main/docs/install/architecture/overview.mdx)

## Summary

You now understand the runtime surfaces that matter for production scaling decisions.

Next: [Chapter 3: Flow Design, Versioning, and Debugging](03-flow-design-versioning-and-debugging.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `.eslintrc.json`

The `.eslintrc` module in [`.eslintrc.json`](https://github.com/activepieces/activepieces/blob/HEAD/.eslintrc.json) handles a key part of this chapter's functionality:

```json
{
  "root": true,
  "ignorePatterns": ["**/*", "deploy/**/*"],
  "overrides": [
    {
      "files": ["*.ts", "*.tsx", "*.js", "*.jsx"],
      "rules": {
        "no-restricted-imports": [
          "error",
          {
            "patterns": ["lodash", "lodash/*"]
          }
        ]
      }
    },
    {
      "files": ["*.ts", "*.tsx"],
      "extends": ["plugin:@typescript-eslint/recommended"],
      "rules": {
        "@typescript-eslint/no-extra-semi": "error",
        "@typescript-eslint/no-unused-vars": "warn",
        "@typescript-eslint/no-explicit-any": "warn",
        "no-extra-semi": "off"
      }
    },
    {
      "files": ["*.js", "*.jsx"],
      "rules": {
        "@typescript-eslint/no-extra-semi": "error",
        "no-extra-semi": "off"
      }
    },
    {
      "files": ["*.spec.ts", "*.spec.tsx", "*.spec.js", "*.spec.jsx"],
      "env": {
```

This module is important because it defines how Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations implements the patterns covered in this chapter.

### `package.json`

The `package` module in [`package.json`](https://github.com/activepieces/activepieces/blob/HEAD/package.json) handles a key part of this chapter's functionality:

```json
{
  "name": "activepieces",
  "version": "0.79.2",
  "rcVersion": "0.80.0-rc.0",
  "packageManager": "bun@1.3.3",
  "scripts": {
    "prebuild": "node tools/scripts/install-bun.js",
    "serve:frontend": "turbo run serve --filter=web",
    "serve:backend": "turbo run serve --filter=api",
    "serve:engine": "turbo run serve --filter=@activepieces/engine",
    "serve:worker": "turbo run serve --filter=worker",
    "push": "turbo run lint && git push",
    "dev": "node tools/scripts/install-bun.js && turbo run serve --filter=web --filter=api --filter=@activepieces/engine --filter=worker --ui stream",
    "dev:backend": "turbo run serve --filter=api --filter=@activepieces/engine --ui stream",
    "dev:frontend": "turbo run serve --filter=web --filter=api --filter=@activepieces/engine --ui stream",
    "start": "node tools/setup-dev.js && npm run dev",
    "test:e2e": "npx playwright test --config=packages/tests-e2e/playwright.config.ts",
    "db-migration": "npx turbo run db-migration --filter=api --",
    "check-migrations": "npx turbo run check-migrations --filter=api",
    "lint": "turbo run lint",
    "lint-dev": "turbo run lint --filter='!@activepieces/piece-*' --force -- --fix",
    "cli": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json  packages/cli/src/index.ts",
    "create-piece": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json  packages/cli/src/index.ts pieces create",
    "create-action": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json  packages/cli/src/index.ts actions create",
    "create-trigger": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json packages/cli/src/index.ts triggers create",
    "sync-pieces": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json packages/cli/src/index.ts pieces sync",
    "build-piece": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json packages/cli/src/index.ts pieces build",
    "publish-piece-to-api": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json packages/cli/src/index.ts pieces publish piece",
    "publish-piece": "npx ts-node -r tsconfig-paths/register --project tools/tsconfig.tools.json tools/scripts/pieces/publish-piece.ts",
    "workers": "npx ts-node -r tsconfig-paths/register --project packages/cli/tsconfig.json packages/cli/src/index.ts workers",
    "pull-i18n": "crowdin pull --config crowdin.yml",
    "push-i18n": "crowdin upload sources",
    "i18n:extract": "i18next --config packages/web/i18next-parser.config.js",
    "bump-translated-pieces": "npx ts-node --project tools/tsconfig.tools.json tools/scripts/pieces/bump-translated-pieces.ts",
    "bump-all-pieces-patch-version": "npx ts-node --project tools/tsconfig.tools.json tools/scripts/pieces/bump-all-pieces-patch-version.ts"
```

This module is important because it defines how Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations implements the patterns covered in this chapter.

### `.typos.toml`

The `.typos` module in [`.typos.toml`](https://github.com/activepieces/activepieces/blob/HEAD/.typos.toml) handles a key part of this chapter's functionality:

```toml
[files]
extend-exclude = [
    ".git/",
    "**/database/**",
    "packages/ui/core/src/locale/",
    # French
    "packages/pieces/community/wedof/src/",
]
ignore-hidden = false

[default]
extend-ignore-re = [
    "[0-9A-Za-z]{34}",
    "name: 'referal'",
    "getRepository\\('referal'\\)",
    "label: 'FO Language', value: 'fo'",
    "649c83111c9cbe6ba1d4cabe",
    "hYy9pRFVxpDsO1FB05SunFWUe9JZY",
    "lod6JEdKyPlvrnErdnrGa",
]

[default.extend-identifiers]
"crazyTweek" = "crazyTweek"
"optin_ip" = "optin_ip"

# Typos
"Github" = "GitHub"

```

This module is important because it defines how Activepieces Tutorial: Open-Source Automation, Pieces, and AI-Ready Workflow Operations implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[.eslintrc]
    B[package]
    C[.typos]
    A --> B
    B --> C
```
