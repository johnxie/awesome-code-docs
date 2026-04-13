---
layout: default
title: "Chapter 3: Modes, Prompts, and Approval Workflow"
nav_order: 3
parent: Kilo Code Tutorial
---


# Chapter 3: Modes, Prompts, and Approval Workflow

Welcome to **Chapter 3: Modes, Prompts, and Approval Workflow**. In this part of **Kilo Code Tutorial: Agentic Engineering from IDE and CLI Surfaces**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Kilo supports different run modes and approval paths that balance autonomy with safety.

## Practical Controls

- mode selection (code/architect/debug variants)
- non-interactive auto-approval mode where appropriate
- ask routing for commands, tools, and followup decisions

## Source References

- [CLI usage in apps/cli README](https://github.com/Kilo-Org/kilocode/blob/main/apps/cli/README.md)
- [Ask dispatcher and prompt manager](https://github.com/Kilo-Org/kilocode/tree/main/apps/cli/src/agent)

## Summary

You now have a mode-selection and approval strategy for safer Kilo sessions.

Next: [Chapter 4: Authentication and Provider Routing](04-authentication-and-provider-routing.md)

## Source Code Walkthrough

### `script/stats.ts`

The `fetchNpmDownloads` function in [`script/stats.ts`](https://github.com/Kilo-Org/kilocode/blob/HEAD/script/stats.ts) handles a key part of this chapter's functionality:

```ts
}

async function fetchNpmDownloads(packageName: string): Promise<number> {
  try {
    // Use a range from 2020 to current year + 5 years to ensure it works forever
    const currentYear = new Date().getFullYear()
    const endYear = currentYear + 5
    const response = await fetch(`https://api.npmjs.org/downloads/range/2020-01-01:${endYear}-12-31/${packageName}`)
    if (!response.ok) {
      console.warn(`Failed to fetch npm downloads for ${packageName}: ${response.status}`)
      return 0
    }
    const data: NpmDownloadsRange = await response.json()
    return data.downloads.reduce((total, day) => total + day.downloads, 0)
  } catch (error) {
    console.warn(`Error fetching npm downloads for ${packageName}:`, error)
    return 0
  }
}

async function fetchReleases(): Promise<Release[]> {
  const releases: Release[] = []
  let page = 1
  const per = 100

  while (true) {
    const url = `https://api.github.com/repos/Kilo-Org/kilocode/releases?page=${page}&per_page=${per}`

    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status} ${response.statusText}`)
    }
```

This function is important because it defines how Kilo Code Tutorial: Agentic Engineering from IDE and CLI Surfaces implements the patterns covered in this chapter.

### `script/stats.ts`

The `fetchReleases` function in [`script/stats.ts`](https://github.com/Kilo-Org/kilocode/blob/HEAD/script/stats.ts) handles a key part of this chapter's functionality:

```ts
}

async function fetchReleases(): Promise<Release[]> {
  const releases: Release[] = []
  let page = 1
  const per = 100

  while (true) {
    const url = `https://api.github.com/repos/Kilo-Org/kilocode/releases?page=${page}&per_page=${per}`

    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`GitHub API error: ${response.status} ${response.statusText}`)
    }

    const batch: Release[] = await response.json()
    if (batch.length === 0) break

    releases.push(...batch)
    console.log(`Fetched page ${page} with ${batch.length} releases`)

    if (batch.length < per) break
    page++
    await new Promise((resolve) => setTimeout(resolve, 1000))
  }

  return releases
}

function calculate(releases: Release[]) {
  let total = 0
  const stats = []
```

This function is important because it defines how Kilo Code Tutorial: Agentic Engineering from IDE and CLI Surfaces implements the patterns covered in this chapter.

### `script/stats.ts`

The `calculate` function in [`script/stats.ts`](https://github.com/Kilo-Org/kilocode/blob/HEAD/script/stats.ts) handles a key part of this chapter's functionality:

```ts
}

function calculate(releases: Release[]) {
  let total = 0
  const stats = []

  for (const release of releases) {
    let downloads = 0
    const assets = []

    for (const asset of release.assets) {
      downloads += asset.download_count
      assets.push({
        name: asset.name,
        downloads: asset.download_count,
      })
    }

    total += downloads
    stats.push({
      tag: release.tag_name,
      name: release.name,
      downloads,
      assets,
    })
  }

  return { total, stats }
}

async function save(githubTotal: number, npmDownloads: number) {
  const file = "STATS.md"
```

This function is important because it defines how Kilo Code Tutorial: Agentic Engineering from IDE and CLI Surfaces implements the patterns covered in this chapter.

### `script/stats.ts`

The `save` function in [`script/stats.ts`](https://github.com/Kilo-Org/kilocode/blob/HEAD/script/stats.ts) handles a key part of this chapter's functionality:

```ts
}

async function save(githubTotal: number, npmDownloads: number) {
  const file = "STATS.md"
  const date = new Date().toISOString().split("T")[0]
  const total = githubTotal + npmDownloads

  let previousGithub = 0
  let previousNpm = 0
  let previousTotal = 0
  let content = ""

  try {
    content = await Bun.file(file).text()
    const lines = content.trim().split("\n")

    for (let i = lines.length - 1; i >= 0; i--) {
      const line = lines[i].trim()
      if (line.startsWith("|") && !line.includes("Date") && !line.includes("---")) {
        const match = line.match(
          /\|\s*[\d-]+\s*\|\s*([\d,]+)\s*(?:\([^)]*\))?\s*\|\s*([\d,]+)\s*(?:\([^)]*\))?\s*\|\s*([\d,]+)\s*(?:\([^)]*\))?\s*\|/,
        )
        if (match) {
          previousGithub = parseInt(match[1].replace(/,/g, ""))
          previousNpm = parseInt(match[2].replace(/,/g, ""))
          previousTotal = parseInt(match[3].replace(/,/g, ""))
          break
        }
      }
    }
  } catch {
    content =
```

This function is important because it defines how Kilo Code Tutorial: Agentic Engineering from IDE and CLI Surfaces implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[fetchNpmDownloads]
    B[fetchReleases]
    C[calculate]
    D[save]
    A --> B
    B --> C
    C --> D
```
