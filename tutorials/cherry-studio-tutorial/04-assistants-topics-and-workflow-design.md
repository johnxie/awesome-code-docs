---
layout: default
title: "Chapter 4: Assistants, Topics, and Workflow Design"
nav_order: 4
parent: Cherry Studio Tutorial
---


# Chapter 4: Assistants, Topics, and Workflow Design

Welcome to **Chapter 4: Assistants, Topics, and Workflow Design**. In this part of **Cherry Studio Tutorial: Multi-Provider AI Desktop Workspace for Teams**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on structuring assistants and conversations for high throughput.

## Learning Goals

- use preconfigured assistants effectively
- create focused custom assistants for specific task types
- organize topics for retrieval and long-running work
- support multi-model conversation strategies

## Workflow Pattern

1. choose assistant role aligned to task
2. bind preferred model/provider profile
3. organize conversation in topic hierarchy
4. iterate and refine prompts with reusable templates

## Source References

- [Cherry Studio README: assistants and conversations](https://github.com/CherryHQ/cherry-studio/blob/main/README.md#-key-features)
- [Cherry Studio discussions](https://github.com/CherryHQ/cherry-studio/discussions)

## Summary

You now have a practical structure for assistant- and topic-driven workflows in Cherry Studio.

Next: [Chapter 5: Documents, MCP, and Tool Integrations](05-documents-mcp-and-tool-integrations.md)

## Source Code Walkthrough

### `scripts/update-app-upgrade-config.ts`

The `getBaseVersion` function in [`scripts/update-app-upgrade-config.ts`](https://github.com/CherryHQ/cherry-studio/blob/HEAD/scripts/update-app-upgrade-config.ts) handles a key part of this chapter's functionality:

```ts
  }

  const baseVersion = getBaseVersion(releaseInfo.version)
  return baseVersion ?? releaseInfo.version
}

function getBaseVersion(version: string): string | null {
  const parsed = semver.parse(version, { loose: true })
  if (!parsed) {
    return null
  }
  return `${parsed.major}.${parsed.minor}.${parsed.patch}`
}

function createEmptyVersionEntry(): VersionEntry {
  return {
    minCompatibleVersion: '',
    description: '',
    channels: {
      latest: null,
      rc: null,
      beta: null
    }
  }
}

function ensureChannelSlots(
  channels: Record<UpgradeChannel, ChannelConfig | null>
): Record<UpgradeChannel, ChannelConfig | null> {
  return CHANNELS.reduce(
    (acc, channel) => {
      acc[channel] = channels[channel] ?? null
```

This function is important because it defines how Cherry Studio Tutorial: Multi-Provider AI Desktop Workspace for Teams implements the patterns covered in this chapter.

### `scripts/update-app-upgrade-config.ts`

The `createEmptyVersionEntry` function in [`scripts/update-app-upgrade-config.ts`](https://github.com/CherryHQ/cherry-studio/blob/HEAD/scripts/update-app-upgrade-config.ts) handles a key part of this chapter's functionality:

```ts
    entry = { ...versionsCopy[existingKey], channels: { ...versionsCopy[existingKey].channels } }
  } else {
    entry = createEmptyVersionEntry()
  }

  entry.channels = ensureChannelSlots(entry.channels)

  const channelUpdated = await applyChannelUpdate(entry, segment, releaseInfo, skipReleaseValidation)
  if (!channelUpdated) {
    return { versions, updated: false }
  }

  if (shouldRename && existingKey) {
    delete versionsCopy[existingKey]
  }

  entry.metadata = {
    segmentId: segment.id,
    segmentType: segment.type
  }
  entry.minCompatibleVersion = segment.minCompatibleVersion
  entry.description = segment.description

  versionsCopy[targetKey] = entry
  return {
    versions: sortVersionMap(versionsCopy),
    updated: true
  }
}

function findVersionKeyBySegment(versions: Record<string, VersionEntry>, segmentId: string): string | null {
  for (const [key, value] of Object.entries(versions)) {
```

This function is important because it defines how Cherry Studio Tutorial: Multi-Provider AI Desktop Workspace for Teams implements the patterns covered in this chapter.

### `scripts/update-app-upgrade-config.ts`

The `ensureChannelSlots` function in [`scripts/update-app-upgrade-config.ts`](https://github.com/CherryHQ/cherry-studio/blob/HEAD/scripts/update-app-upgrade-config.ts) handles a key part of this chapter's functionality:

```ts
  }

  entry.channels = ensureChannelSlots(entry.channels)

  const channelUpdated = await applyChannelUpdate(entry, segment, releaseInfo, skipReleaseValidation)
  if (!channelUpdated) {
    return { versions, updated: false }
  }

  if (shouldRename && existingKey) {
    delete versionsCopy[existingKey]
  }

  entry.metadata = {
    segmentId: segment.id,
    segmentType: segment.type
  }
  entry.minCompatibleVersion = segment.minCompatibleVersion
  entry.description = segment.description

  versionsCopy[targetKey] = entry
  return {
    versions: sortVersionMap(versionsCopy),
    updated: true
  }
}

function findVersionKeyBySegment(versions: Record<string, VersionEntry>, segmentId: string): string | null {
  for (const [key, value] of Object.entries(versions)) {
    if (value.metadata?.segmentId === segmentId) {
      return key
    }
```

This function is important because it defines how Cherry Studio Tutorial: Multi-Provider AI Desktop Workspace for Teams implements the patterns covered in this chapter.

### `scripts/update-app-upgrade-config.ts`

The `applyChannelUpdate` function in [`scripts/update-app-upgrade-config.ts`](https://github.com/CherryHQ/cherry-studio/blob/HEAD/scripts/update-app-upgrade-config.ts) handles a key part of this chapter's functionality:

```ts
  entry.channels = ensureChannelSlots(entry.channels)

  const channelUpdated = await applyChannelUpdate(entry, segment, releaseInfo, skipReleaseValidation)
  if (!channelUpdated) {
    return { versions, updated: false }
  }

  if (shouldRename && existingKey) {
    delete versionsCopy[existingKey]
  }

  entry.metadata = {
    segmentId: segment.id,
    segmentType: segment.type
  }
  entry.minCompatibleVersion = segment.minCompatibleVersion
  entry.description = segment.description

  versionsCopy[targetKey] = entry
  return {
    versions: sortVersionMap(versionsCopy),
    updated: true
  }
}

function findVersionKeyBySegment(versions: Record<string, VersionEntry>, segmentId: string): string | null {
  for (const [key, value] of Object.entries(versions)) {
    if (value.metadata?.segmentId === segmentId) {
      return key
    }
  }
  return null
```

This function is important because it defines how Cherry Studio Tutorial: Multi-Provider AI Desktop Workspace for Teams implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[getBaseVersion]
    B[createEmptyVersionEntry]
    C[ensureChannelSlots]
    D[applyChannelUpdate]
    E[buildFeedUrls]
    A --> B
    B --> C
    C --> D
    D --> E
```
