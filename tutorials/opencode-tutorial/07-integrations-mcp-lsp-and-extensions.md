---
layout: default
title: "Chapter 7: Integrations: MCP, LSP, and Extensions"
nav_order: 7
parent: OpenCode Tutorial
---


# Chapter 7: Integrations: MCP, LSP, and Extensions

Welcome to **Chapter 7: Integrations: MCP, LSP, and Extensions**. In this part of **OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


OpenCode gains leverage when integrated with MCP servers, language tooling, and repository-specific workflows.

## Integration Surfaces

| Surface | Outcome |
|:--------|:--------|
| LSP tooling | better semantic code understanding |
| MCP servers | external tool and resource access |
| repo scripts | project-native lint/test/deploy pipelines |

## Integration Pattern

1. start with repository-local build/test tools
2. add LSP-backed code navigation flows
3. integrate MCP only for high-value external systems
4. enforce policy checks on integration boundaries

## Source References

- [OpenCode Docs](https://opencode.ai/docs)
- [MCP Servers Tutorial](../mcp-servers-tutorial/)

## Summary

You now have a blueprint for extending OpenCode safely and effectively across your stack.

Next: [Chapter 8: Production Operations and Security](08-production-operations-security.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `script/changelog.ts`

The `summarizeCommit` function in [`script/changelog.ts`](https://github.com/anomalyco/opencode/blob/HEAD/script/changelog.ts) handles a key part of this chapter's functionality:

```ts
}

async function summarizeCommit(opencode: Awaited<ReturnType<typeof createOpencode>>, message: string): Promise<string> {
  console.log("summarizing commit:", message)
  const session = await opencode.client.session.create()
  const result = await opencode.client.session
    .prompt(
      {
        sessionID: session.data!.id,
        model: { providerID: "opencode", modelID: "claude-sonnet-4-5" },
        tools: {
          "*": false,
        },
        parts: [
          {
            type: "text",
            text: `Summarize this commit message for a changelog entry. Return ONLY a single line summary starting with a capital letter. Be concise but specific. If the commit message is already well-written, just clean it up (capitalize, fix typos, proper grammar). Do not include any prefixes like "fix:" or "feat:".

Commit: ${message}`,
          },
        ],
      },
      {
        signal: AbortSignal.timeout(120_000),
      },
    )
    .then((x) => x.data?.parts?.find((y) => y.type === "text")?.text ?? message)
  return result.trim()
}

export async function generateChangelog(commits: Commit[], opencode: Awaited<ReturnType<typeof createOpencode>>) {
  // Summarize commits in parallel with max 10 concurrent requests
```

This function is important because it defines how OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale implements the patterns covered in this chapter.

### `script/changelog.ts`

The `generateChangelog` function in [`script/changelog.ts`](https://github.com/anomalyco/opencode/blob/HEAD/script/changelog.ts) handles a key part of this chapter's functionality:

```ts
}

export async function generateChangelog(commits: Commit[], opencode: Awaited<ReturnType<typeof createOpencode>>) {
  // Summarize commits in parallel with max 10 concurrent requests
  const BATCH_SIZE = 10
  const summaries: string[] = []
  for (let i = 0; i < commits.length; i += BATCH_SIZE) {
    const batch = commits.slice(i, i + BATCH_SIZE)
    const results = await Promise.all(batch.map((c) => summarizeCommit(opencode, c.message)))
    summaries.push(...results)
  }

  const grouped = new Map<string, string[]>()
  for (let i = 0; i < commits.length; i++) {
    const commit = commits[i]!
    const section = getSection(commit.areas)
    const attribution = commit.author && !Script.team.includes(commit.author) ? ` (@${commit.author})` : ""
    const entry = `- ${summaries[i]}${attribution}`

    if (!grouped.has(section)) grouped.set(section, [])
    grouped.get(section)!.push(entry)
  }

  const sectionOrder = ["Core", "TUI", "Desktop", "SDK", "Extensions"]
  const lines: string[] = []
  for (const section of sectionOrder) {
    const entries = grouped.get(section)
    if (!entries || entries.length === 0) continue
    lines.push(`## ${section}`)
    lines.push(...entries)
  }

```

This function is important because it defines how OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale implements the patterns covered in this chapter.

### `script/changelog.ts`

The `getContributors` function in [`script/changelog.ts`](https://github.com/anomalyco/opencode/blob/HEAD/script/changelog.ts) handles a key part of this chapter's functionality:

```ts
}

export async function getContributors(from: string, to: string) {
  const fromRef = from.startsWith("v") ? from : `v${from}`
  const toRef = to === "HEAD" ? to : to.startsWith("v") ? to : `v${to}`
  const compare =
    await $`gh api "/repos/anomalyco/opencode/compare/${fromRef}...${toRef}" --jq '.commits[] | {login: .author.login, message: .commit.message}'`.text()
  const contributors = new Map<string, Set<string>>()

  for (const line of compare.split("\n").filter(Boolean)) {
    const { login, message } = JSON.parse(line) as { login: string | null; message: string }
    const title = message.split("\n")[0] ?? ""
    if (title.match(/^(ignore:|test:|chore:|ci:|release:)/i)) continue

    if (login && !Script.team.includes(login)) {
      if (!contributors.has(login)) contributors.set(login, new Set())
      contributors.get(login)!.add(title)
    }
  }

  return contributors
}

export async function buildNotes(from: string, to: string) {
  const commits = await getCommits(from, to)

  if (commits.length === 0) {
    return []
  }

  console.log("generating changelog since " + from)

```

This function is important because it defines how OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale implements the patterns covered in this chapter.

### `script/changelog.ts`

The `buildNotes` function in [`script/changelog.ts`](https://github.com/anomalyco/opencode/blob/HEAD/script/changelog.ts) handles a key part of this chapter's functionality:

```ts
}

export async function buildNotes(from: string, to: string) {
  const commits = await getCommits(from, to)

  if (commits.length === 0) {
    return []
  }

  console.log("generating changelog since " + from)

  const opencode = await createOpencode({ port: 0 })
  const notes: string[] = []

  try {
    const lines = await generateChangelog(commits, opencode)
    notes.push(...lines)
    console.log("---- Generated Changelog ----")
    console.log(notes.join("\n"))
    console.log("-----------------------------")
  } catch (error) {
    if (error instanceof Error && error.name === "TimeoutError") {
      console.log("Changelog generation timed out, using raw commits")
      for (const commit of commits) {
        const attribution = commit.author && !team.includes(commit.author) ? ` (@${commit.author})` : ""
        notes.push(`- ${commit.message}${attribution}`)
      }
    } else {
      throw error
    }
  } finally {
    await opencode.server.close()
```

This function is important because it defines how OpenCode Tutorial: Open-Source Terminal Coding Agent at Scale implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[summarizeCommit]
    B[generateChangelog]
    C[getContributors]
    D[buildNotes]
    E[sendToPostHog]
    A --> B
    B --> C
    C --> D
    D --> E
```
