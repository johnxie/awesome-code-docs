---
layout: default
title: "Chapter 1: Getting Started"
nav_order: 1
parent: Roo Code Tutorial
---


# Chapter 1: Getting Started

Welcome to **Chapter 1: Getting Started**. In this part of **Roo Code Tutorial: Run an AI Dev Team in Your Editor**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter establishes a stable Roo Code baseline in a VS Code-compatible workflow.

## Objectives

By the end, you will have:

1. Roo Code installed and running
2. one provider configured successfully
3. a deterministic first task completed
4. a minimum approval policy for safe usage

## Prerequisites

| Requirement | Why It Matters |
|:------------|:---------------|
| VS Code-compatible editor | Roo Code extension runtime |
| API credentials for at least one provider | model-backed execution |
| sandbox repository | low-risk calibration environment |
| canonical lint/test command | repeatable validation signal |

## Installation Paths

### Marketplace install

Install Roo Code from the VS Code marketplace and reload the editor.

### VSIX install (team/internal path)

Roo Code repository docs include VSIX build/install flows.

Typical dev workflow commands:

```bash
git clone https://github.com/RooCodeInc/Roo-Code.git
cd Roo-Code
pnpm install
pnpm install:vsix
```

Alternative manual VSIX flow:

```bash
pnpm vsix
code --install-extension bin/roo-cline-<version>.vsix
```

## Provider Setup

Start with one known-good provider/model pair. Add more only after first task reliability is proven.

Initial policy:

- approvals enabled for file edits and commands
- no broad automation modes during first-day onboarding
- explicit task summaries required

## First Task Prompt

```text
Analyze src/services/session.ts,
refactor one function for readability without changing behavior,
run the target test command,
and summarize changed files and validation output.
```

Success criteria:

- proposed patch is reviewable
- expected file scope is respected
- command output is captured
- summary maps changes to results

## Baseline Safety Defaults

Set and document:

- default mode for routine coding tasks
- approval threshold for mutating commands
- required validation command for each task class
- rollback expectation for risky changes

## First-Run Checklist

| Area | Check | Pass Signal |
|:-----|:------|:------------|
| Install | extension loads correctly | Roo interface opens without errors |
| Provider | model call succeeds | initial task response is actionable |
| Edit flow | diffs are visible before apply | review step works consistently |
| Command flow | test/lint command executes | output attached to task result |
| Summary | results are clear and complete | reviewer can understand outcome quickly |

## Common Startup Issues

### Provider mismatch

- confirm selected provider and key are aligned
- reduce to one provider first

### Unstable task outputs

- tighten task scope to one file/module
- include explicit non-goals
- require final summary format

### Command confusion

- specify exact command in prompt
- avoid ambiguous phrasing like "run checks"

## Chapter Summary

You now have Roo Code running with:

- installation complete
- provider baseline validated
- deterministic first task executed
- initial safety policy in place

Next: [Chapter 2: Modes and Task Design](02-modes-and-task-design.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `scripts/find-missing-i18n-key.js`

The `getLocaleDirs` function in [`scripts/find-missing-i18n-key.js`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/scripts/find-missing-i18n-key.js) handles a key part of this chapter's functionality:

```js

// Get all language directories for a specific locales directory
function getLocaleDirs(localesDir) {
	try {
		const allLocales = fs.readdirSync(localesDir).filter((file) => {
			const stats = fs.statSync(path.join(localesDir, file))
			return stats.isDirectory() // Do not exclude any language directories
		})

		// Filter to a specific language if specified
		return args.locale ? allLocales.filter((locale) => locale === args.locale) : allLocales
	} catch (error) {
		if (error.code === "ENOENT") {
			console.warn(`Warning: Locales directory not found: ${localesDir}`)
			return []
		}
		throw error
	}
}

// Get the value from JSON by path
function getValueByPath(obj, path) {
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

### `scripts/find-missing-i18n-key.js`

The `getValueByPath` function in [`scripts/find-missing-i18n-key.js`](https://github.com/RooCodeInc/Roo-Code/blob/HEAD/scripts/find-missing-i18n-key.js) handles a key part of this chapter's functionality:

```js

// Get the value from JSON by path
function getValueByPath(obj, path) {
	const parts = path.split(".")
	let current = obj

	for (const part of parts) {
		if (current === undefined || current === null) {
			return undefined
		}
		current = current[part]
	}

	return current
}

// Check if the key exists in all language files, return a list of missing language files
function checkKeyInLocales(key, localeDirs, localesDir) {
	const [file, ...pathParts] = key.split(":")
	const jsonPath = pathParts.join(".")

	const missingLocales = []

	localeDirs.forEach((locale) => {
		const filePath = path.join(localesDir, locale, `${file}.json`)
		if (!fs.existsSync(filePath)) {
			missingLocales.push(`${locale}/${file}.json`)
			return
		}

		const json = JSON.parse(fs.readFileSync(filePath, "utf8"))
		if (getValueByPath(json, jsonPath) === undefined) {
```

This function is important because it defines how Roo Code Tutorial: Run an AI Dev Team in Your Editor implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[getLocaleDirs]
    B[getValueByPath]
    A --> B
```
