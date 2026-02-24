---
layout: default
title: "Chapter 1: Getting Started with Turborepo"
parent: "Turborepo Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Turborepo

Welcome to Turborepo! If you've ever struggled with slow builds in large monorepos, you're in the right place. Turborepo is the high-performance build system that makes your monorepo feel as fast as a single package, using intelligent caching and parallel execution.

## What Makes Turborepo Special?

Turborepo revolutionizes monorepo development by:

- **Intelligent Caching** - Never rebuild unchanged code
- **Parallel Execution** - Run tasks simultaneously across packages
- **Smart Scheduling** - Only run tasks when dependencies change
- **Remote Caching** - Share build artifacts across your team
- **Zero Configuration** - Works out of the box with sensible defaults
- **Framework Agnostic** - Supports any JavaScript/TypeScript tool

## Installing Turborepo

### Creating Your First Monorepo

```bash
# Create a new Turborepo
npx create-turbo@latest my-monorepo
cd my-monorepo

# Or add to existing project
npm install turbo --save-dev

# Initialize Turborepo in existing monorepo
npx turbo init
```

### Basic Project Structure

```bash
my-monorepo/
├── packages/
│   ├── ui/           # Shared UI components
│   ├── utils/        # Shared utilities
│   └── config/       # Shared configuration
├── apps/
│   ├── web/          # Next.js application
│   └── docs/         # Documentation site
├── package.json
├── turbo.json        # Turborepo configuration
└── yarn.lock
```

## Your First Turborepo Pipeline

Let's create a simple monorepo with Turborepo:

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    "**/.env.*local"
  ],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "test/**/*.ts", "test/**/*.tsx"]
    }
  }
}
```

## Understanding Turborepo Concepts

### Task Dependencies

```json
// turbo.json with dependencies
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],  // Wait for dependencies to build first
      "outputs": ["dist/**"]    // Cache these outputs
    },
    "test": {
      "dependsOn": ["build"],   // Must build before testing
      "inputs": ["src/**", "test/**"]  // Watch these files for changes
    },
    "lint": {
      "dependsOn": []           // No dependencies
    }
  }
}
```

### Package Structure

```json
// packages/ui/package.json
{
  "name": "@my-monorepo/ui",
  "version": "1.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/**/*.ts",
    "test": "jest"
  },
  "dependencies": {
    "react": "^18.2.0"
  },
  "devDependencies": {
    "tsup": "^7.2.0",
    "typescript": "^5.2.0"
  }
}
```

```json
// apps/web/package.json
{
  "name": "@my-monorepo/web",
  "version": "1.0.0",
  "scripts": {
    "build": "next build",
    "dev": "next dev",
    "lint": "next lint",
    "start": "next start"
  },
  "dependencies": {
    "@my-monorepo/ui": "*",
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

## Running Tasks

### Basic Commands

```bash
# Run build for all packages
turbo run build

# Run dev for specific packages
turbo run dev --filter=@my-monorepo/web

# Run tests with dependencies
turbo run test --filter=@my-monorepo/ui

# Run lint for all packages
turbo run lint

# Dry run to see what would execute
turbo run build --dry-run
```

### Filtering Packages

```bash
# Run only for specific package
turbo run build --filter=@my-monorepo/ui

# Run for package and its dependencies
turbo run build --filter=@my-monorepo/web

# Run for packages matching pattern
turbo run test --filter="./packages/*"

# Exclude specific packages
turbo run lint --filter="!@my-monorepo/docs"
```

## Caching in Action

### Understanding the Cache

```bash
# Check cache status
turbo run build --filter=@my-monorepo/ui

# Output shows:
# • Packages in scope: @my-monorepo/ui
# • Running build in 1 packages
# • Remote caching enabled

# Run again (should use cache)
turbo run build --filter=@my-monorepo/ui

# Output shows:
# • Packages in scope: @my-monorepo/ui
# • Running build in 1 packages
# • Remote cache hit: 100% (1/1)
```

### Cache Configuration

```json
// turbo.json with cache configuration
{
  "tasks": {
    "build": {
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**"
      ],
      "inputs": [
        "src/**",
        "package.json",
        "tsconfig.json"
      ]
    },
    "test": {
      "inputs": [
        "src/**/*.ts",
        "test/**/*.ts",
        "jest.config.js"
      ],
      "outputs": [
        "coverage/**"
      ]
    }
  }
}
```

## Pipeline Execution

### Task Scheduling

```bash
# Build entire monorepo
turbo run build

# Turborepo automatically:
# 1. Analyzes dependencies between packages
# 2. Schedules tasks in optimal order
# 3. Runs independent tasks in parallel
# 4. Caches outputs for future runs
# 5. Handles failures gracefully
```

### Execution Graph

```mermaid
graph TD
    A[config] --> C[ui]
    A --> D[utils]
    C --> E[web]
    D --> E
    C --> F[docs]
    D --> F

    classDef package fill:#e1f5fe,stroke:#01579b
    classDef app fill:#f3e5f5,stroke:#4a148c

    class A,C,D package
    class E,F app
```

## Error Handling and Debugging

### Debugging Pipeline Issues

```bash
# Get detailed execution information
turbo run build --log-order=stream

# See dependency graph
turbo run build --graph

# Debug specific package
turbo run build --filter=@my-monorepo/ui --log-level=debug

# Continue after failure
turbo run build --continue
```

### Common Issues

```bash
# Clear cache if issues occur
turbo run build --force

# Clear all caches
rm -rf node_modules/.cache/turbo

# Check for configuration issues
turbo run build --dry-run --log-level=debug
```

## Integration with Tools

### TypeScript Configuration

```json
// packages/ui/tsconfig.json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["dist", "node_modules"]
}
```

### ESLint Configuration

```json
// packages/ui/.eslintrc.js
module.exports = {
  extends: ['../../.eslintrc.js'],
  rules: {
    // Package-specific rules
  }
}
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed Turborepo** and created your first monorepo
2. **Configured workspaces** with proper package structure
3. **Set up task pipelines** with dependencies and caching
4. **Executed parallel builds** with intelligent scheduling
5. **Implemented caching** for faster subsequent builds
6. **Debugged pipeline issues** and handled errors
7. **Integrated with development tools** like TypeScript and ESLint

## Next Steps

Now that you understand Turborepo basics, let's explore workspace configuration in depth. In [Chapter 2: Workspace Configuration](02-workspace-configuration.md), we'll dive into advanced workspace setup, package management, and configuration patterns.

---

**Practice what you've learned:**
1. Create a monorepo with multiple packages
2. Set up build pipelines with dependencies
3. Experiment with different filtering options
4. Implement caching for your tasks
5. Debug and optimize your pipeline execution

*What's your biggest monorepo performance challenge?* ⚡

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `turbo`, `build`, `monorepo` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Turborepo` as an operating subsystem inside **Turborepo Tutorial: High-Performance Monorepo Build System**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `packages`, `json`, `package` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Turborepo` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `turbo`.
2. **Input normalization**: shape incoming data so `build` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `monorepo`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/vercel/turborepo)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `turbo` and `build` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Workspace Configuration](02-workspace-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
