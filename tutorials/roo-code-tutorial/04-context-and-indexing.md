---
layout: default
title: "Chapter 4: Context and Indexing"
nav_order: 4
parent: Roo Code Tutorial
---


# Chapter 4: Context and Indexing

Welcome to **Chapter 4: Context and Indexing**. In this part of **Roo Code Tutorial: Run an AI Dev Team in Your Editor**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


In large repositories, quality depends on context precision. This chapter covers how to manage context and indexing strategy in Roo workflows.

## Core Principle

Relevance beats volume.

Passing too much context increases token cost and decreases reasoning quality.

## Context Pipeline

```mermaid
flowchart LR
    A[Task Goal] --> B[Index or Search Relevant Areas]
    B --> C[Curated Context Set]
    C --> D[Mode Execution]
    D --> E[Validation Results]
    E --> F[Next Context Slice]
```

## Context Slicing Strategy

| Situation | Recommended Slice |
|:----------|:------------------|
| single bugfix | one module + failing tests/logs |
| feature iteration | active files + adjacent interfaces |
| migration | architecture map + staged module batches |
| production incident | runtime logs + impacted service paths |

## Indexing Practical Guidance

Use indexing/search to discover candidates, then manually constrain final context set.

Good pattern:

1. broad discovery
2. narrow target selection
3. bounded execution
4. evidence-driven expansion if needed

## Context Mentions and Grounding

Roo docs include context and tool usage surfaces. Regardless of mechanism, include:

- exact files
- concrete errors/logs
- expected behavior
- validation command

This prevents speculative edits.

## Cost and Latency Impact

Context discipline improves:

- response latency
- token spend
- patch accuracy
- reviewer confidence

Treat context selection as an engineering activity, not a UI action.

## Failure Patterns

### Over-contexting

Symptom: unrelated edits and slow loops.

Fix: remove low-relevance files and enforce explicit scope.

### Under-contexting

Symptom: shallow fixes that ignore true root cause.

Fix: add targeted interface/dependency files and concrete error traces.

### Stale context between mode changes

Symptom: mode transitions lose constraints.

Fix: include concise state summary when switching modes.

## Chapter Summary

You now have a context/indexing model for large repos:

- discover broadly, execute narrowly
- tie context to validation evidence
- maintain continuity across mode transitions

Next: [Chapter 5: Checkpoints and Recovery](05-checkpoints-and-recovery.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `webview-ui/vite.config.ts`

The `getGitSha` function in [`webview-ui/vite.config.ts`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/webview-ui/vite.config.ts) handles a key part of this chapter's functionality:

```ts
import { sourcemapPlugin } from "./src/vite-plugins/sourcemapPlugin"

function getGitSha() {
	let gitSha: string | undefined = undefined

	try {
		gitSha = execSync("git rev-parse HEAD").toString().trim()
	} catch (_error) {
		// Do nothing.
	}

	return gitSha
}

const wasmPlugin = (): Plugin => ({
	name: "wasm",
	async load(id) {
		if (id.endsWith(".wasm")) {
			const wasmBinary = await import(id)

			return `
           			const wasmModule = new WebAssembly.Module(${wasmBinary.default});
           			export default wasmModule;
         		`
		}
	},
})

const persistPortPlugin = (): Plugin => ({
	name: "write-port-to-file",
	configureServer(viteDevServer) {
		viteDevServer?.httpServer?.once("listening", () => {
```

This function is important because it defines how Roo Code Tutorial: Run an AI Dev Team in Your Editor implements the patterns covered in this chapter.

### `scripts/find-missing-translations.js`

The `findKeys` function in [`scripts/find-missing-translations.js`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/scripts/find-missing-translations.js) handles a key part of this chapter's functionality:

```js

// Recursively find all keys in an object
function findKeys(obj, parentKey = "") {
	let keys = []

	for (const [key, value] of Object.entries(obj)) {
		const currentKey = parentKey ? `${parentKey}.${key}` : key

		if (typeof value === "object" && value !== null) {
			// If value is an object, recurse
			keys = [...keys, ...findKeys(value, currentKey)]
		} else {
			// If value is a primitive, add the key
			keys.push(currentKey)
		}
	}

	return keys
}

// Get value at a dotted path in an object
function getValueAtPath(obj, path) {
	const parts = path.split(".")
	let current = obj

	for (const part of parts) {
		if (current === undefined || current === null) {
			return undefined
		}
		current = current[part]
	}

```

This function is important because it defines how Roo Code Tutorial: Run an AI Dev Team in Your Editor implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[getGitSha]
    B[findKeys]
    A --> B
```
