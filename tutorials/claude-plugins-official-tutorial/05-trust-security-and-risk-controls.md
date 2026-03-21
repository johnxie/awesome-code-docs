---
layout: default
title: "Chapter 5: Trust, Security, and Risk Controls"
nav_order: 5
parent: Claude Plugins Official Tutorial
---


# Chapter 5: Trust, Security, and Risk Controls

Welcome to **Chapter 5: Trust, Security, and Risk Controls**. In this part of **Claude Plugins Official Tutorial: Anthropic's Managed Plugin Directory**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on safe plugin adoption and third-party risk controls.

## Learning Goals

- evaluate trust boundaries before plugin installation
- apply security controls for plugins with MCP/tool integrations
- document risk posture for internal approval workflows
- reduce blast radius of plugin misbehavior

## Baseline Risk Controls

- install only trusted and reviewed plugins
- audit plugin README and metadata before install
- inspect `.mcp.json` and hook behaviors for sensitive operations
- isolate experimental plugins from production-critical workflows

## Operational Safety Pattern

- pilot plugins in non-critical projects first
- require explicit approval for plugins with external network actions
- maintain an allowlist of approved plugin names and versions

## Source References

- [Directory Trust Warning](https://github.com/anthropics/claude-plugins-official/blob/main/README.md)
- [Official Plugin Docs](https://code.claude.com/docs/en/plugins)
- [External Plugins Directory](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)

## Summary

You now have a practical safety model for directory plugin adoption.

Next: [Chapter 6: Installation, Operations, and Update Strategy](06-installation-operations-and-update-strategy.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `external_plugins/telegram/server.ts`

The `defaultAccess` function in [`external_plugins/telegram/server.ts`](https://github.com/anthropics/claude-plugins-official/blob/HEAD/external_plugins/telegram/server.ts) handles a key part of this chapter's functionality:

```ts
}

function defaultAccess(): Access {
  return {
    dmPolicy: 'pairing',
    allowFrom: [],
    groups: {},
    pending: {},
  }
}

const MAX_CHUNK_LIMIT = 4096
const MAX_ATTACHMENT_BYTES = 50 * 1024 * 1024

// reply's files param takes any path. .env is ~60 bytes and ships as a
// document. Claude can already Read+paste file contents, so this isn't a new
// exfil channel for arbitrary paths — but the server's own state is the one
// thing Claude has no reason to ever send.
function assertSendable(f: string): void {
  let real, stateReal: string
  try {
    real = realpathSync(f)
    stateReal = realpathSync(STATE_DIR)
  } catch { return } // statSync will fail properly; or STATE_DIR absent → nothing to leak
  const inbox = join(stateReal, 'inbox')
  if (real.startsWith(stateReal + sep) && !real.startsWith(inbox + sep)) {
    throw new Error(`refusing to send channel state: ${f}`)
  }
}

function readAccessFile(): Access {
  try {
```

This function is important because it defines how Claude Plugins Official Tutorial: Anthropic's Managed Plugin Directory implements the patterns covered in this chapter.

### `external_plugins/telegram/server.ts`

The `assertSendable` function in [`external_plugins/telegram/server.ts`](https://github.com/anthropics/claude-plugins-official/blob/HEAD/external_plugins/telegram/server.ts) handles a key part of this chapter's functionality:

```ts
// exfil channel for arbitrary paths — but the server's own state is the one
// thing Claude has no reason to ever send.
function assertSendable(f: string): void {
  let real, stateReal: string
  try {
    real = realpathSync(f)
    stateReal = realpathSync(STATE_DIR)
  } catch { return } // statSync will fail properly; or STATE_DIR absent → nothing to leak
  const inbox = join(stateReal, 'inbox')
  if (real.startsWith(stateReal + sep) && !real.startsWith(inbox + sep)) {
    throw new Error(`refusing to send channel state: ${f}`)
  }
}

function readAccessFile(): Access {
  try {
    const raw = readFileSync(ACCESS_FILE, 'utf8')
    const parsed = JSON.parse(raw) as Partial<Access>
    return {
      dmPolicy: parsed.dmPolicy ?? 'pairing',
      allowFrom: parsed.allowFrom ?? [],
      groups: parsed.groups ?? {},
      pending: parsed.pending ?? {},
      mentionPatterns: parsed.mentionPatterns,
      ackReaction: parsed.ackReaction,
      replyToMode: parsed.replyToMode,
      textChunkLimit: parsed.textChunkLimit,
      chunkMode: parsed.chunkMode,
    }
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === 'ENOENT') return defaultAccess()
    try {
```

This function is important because it defines how Claude Plugins Official Tutorial: Anthropic's Managed Plugin Directory implements the patterns covered in this chapter.

### `external_plugins/telegram/server.ts`

The `readAccessFile` function in [`external_plugins/telegram/server.ts`](https://github.com/anthropics/claude-plugins-official/blob/HEAD/external_plugins/telegram/server.ts) handles a key part of this chapter's functionality:

```ts
}

function readAccessFile(): Access {
  try {
    const raw = readFileSync(ACCESS_FILE, 'utf8')
    const parsed = JSON.parse(raw) as Partial<Access>
    return {
      dmPolicy: parsed.dmPolicy ?? 'pairing',
      allowFrom: parsed.allowFrom ?? [],
      groups: parsed.groups ?? {},
      pending: parsed.pending ?? {},
      mentionPatterns: parsed.mentionPatterns,
      ackReaction: parsed.ackReaction,
      replyToMode: parsed.replyToMode,
      textChunkLimit: parsed.textChunkLimit,
      chunkMode: parsed.chunkMode,
    }
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === 'ENOENT') return defaultAccess()
    try {
      renameSync(ACCESS_FILE, `${ACCESS_FILE}.corrupt-${Date.now()}`)
    } catch {}
    process.stderr.write(`telegram channel: access.json is corrupt, moved aside. Starting fresh.\n`)
    return defaultAccess()
  }
}

// In static mode, access is snapshotted at boot and never re-read or written.
// Pairing requires runtime mutation, so it's downgraded to allowlist with a
// startup warning — handing out codes that never get approved would be worse.
const BOOT_ACCESS: Access | null = STATIC
  ? (() => {
```

This function is important because it defines how Claude Plugins Official Tutorial: Anthropic's Managed Plugin Directory implements the patterns covered in this chapter.

### `external_plugins/telegram/server.ts`

The `loadAccess` function in [`external_plugins/telegram/server.ts`](https://github.com/anthropics/claude-plugins-official/blob/HEAD/external_plugins/telegram/server.ts) handles a key part of this chapter's functionality:

```ts
  : null

function loadAccess(): Access {
  return BOOT_ACCESS ?? readAccessFile()
}

// Outbound gate — reply/react/edit can only target chats the inbound gate
// would deliver from. Telegram DM chat_id == user_id, so allowFrom covers DMs.
function assertAllowedChat(chat_id: string): void {
  const access = loadAccess()
  if (access.allowFrom.includes(chat_id)) return
  if (chat_id in access.groups) return
  throw new Error(`chat ${chat_id} is not allowlisted — add via /telegram:access`)
}

function saveAccess(a: Access): void {
  if (STATIC) return
  mkdirSync(STATE_DIR, { recursive: true, mode: 0o700 })
  const tmp = ACCESS_FILE + '.tmp'
  writeFileSync(tmp, JSON.stringify(a, null, 2) + '\n', { mode: 0o600 })
  renameSync(tmp, ACCESS_FILE)
}

function pruneExpired(a: Access): boolean {
  const now = Date.now()
  let changed = false
  for (const [code, p] of Object.entries(a.pending)) {
    if (p.expiresAt < now) {
      delete a.pending[code]
      changed = true
    }
  }
```

This function is important because it defines how Claude Plugins Official Tutorial: Anthropic's Managed Plugin Directory implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[defaultAccess]
    B[assertSendable]
    C[readAccessFile]
    D[loadAccess]
    E[assertAllowedChat]
    A --> B
    B --> C
    C --> D
    D --> E
```
