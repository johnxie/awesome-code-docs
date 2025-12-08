---
layout: default
title: "Chapter 4: Real-time Features"
parent: "Supabase Tutorial"
nav_order: 4
---

# Chapter 4: Real-time Features

Build live experiences with subscriptions and presence using Supabase Realtime.

## Objectives
- Subscribe to table changes
- Implement live UI updates
- Use presence for collaborative features
- Handle reconnections gracefully

## Table Subscription (JS)
```javascript
const channel = supabase.channel('public:messages')
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, payload => {
    console.log('New message:', payload.new)
  })
  .subscribe()
```

## Live UI Pattern (React)
```javascript
import { useEffect, useState } from 'react'

export function useMessages() {
  const [messages, setMessages] = useState([])
  useEffect(() => {
    const channel = supabase.channel('messages')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, payload => {
        setMessages(prev => [...prev, payload.new])
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [])
  return messages
}
```

## Presence Basics
```javascript
const presence = supabase.channel('room1', { config: { presence: { key: userId } } })
  .on('presence', { event: 'sync' }, () => {
    console.log('Online users:', presence.presenceState())
  })
  .subscribe()
```

## Reconnection Strategy
- Enable auto-reconnect; backoff on failures
- Buffer outbound events when offline; flush on reconnect
- Keep channels lean—one per feature/domain

## Troubleshooting
- Missing events: confirm RLS allows `select` on the table; Realtime honors RLS
- Duplicate events: de-dup by primary key in client state
- Connection drops: add retry with exponential backoff

## Performance Notes
- Limit payload size; avoid large JSON columns in realtime streams
- Use filtered channels (schema/table) to reduce noise

## Security Notes
- Realtime respects RLS; ensure policies include `auth.uid()` checks
- Never broadcast secrets or PII to public channels

## Next Steps
In Chapter 5, add secure file storage and CDN-backed media handling.
